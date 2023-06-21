from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from .forms import *
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.db.models import Q
import pandas as pd
import openpyxl
import pdfkit
from django.template.loader import render_to_string


# Create your views here.


def create_event_manager(request):
    form = SignupForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            email = data['email']
            username = data['username']
            password = data['password']
            user = User.objects.create(username=username, email=email, is_staff=True)
            user.set_password(password)
            user.save()
            # assign_role(user, 'managers')
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            return redirect('list_event_managers')

    return render(request, 'event_managers/create.html', {'form': form})


def list_event_managers(request):
    if request.user.is_superuser:
        context = {
            'user_list': User.objects.filter(is_staff=True).exclude(id=request.user.id)
        }
        return render(request, 'event_managers/index3.html', context)
    elif request.user.is_staff:
        return redirect('event_list')
    else:
        return redirect('logout')


def delete_event_manager(request, id):
    # print(User.objects.get(id=id).groups)
    # for grp in User.objects.get(id=id).groups.all():
    #     print(grp.name)
    User.objects.get(id=id).delete()
    return redirect('list_event_managers')


def event_category_list(request):
    context = {
        'event_category_list': EventCategory.objects.all()
    }
    return render(request, 'event_category/index.html', context)


def quiz_attempt_form(request, quiz_id):
    question = Question.objects.filter(quiz_id=quiz_id).order_by("id").first()
    answer_set = Answer.objects.filter(question_id=question.id)
    atempted = request.POST.get('atemptted_question') or ""
    quiz = Quiz.objects.get(id=quiz_id)

    message = None
    if request.method == "POST":

        answer = Answer.objects.get(id=request.POST.get('answer'), question=request.POST.get('question_id'))
        if answer.is_correct:

            if request.POST.get('question_id') and request.POST.get('atemptted_question'):
                atempted = atempted + "," +request.POST.get('question_id')
            else:
                atempted = request.POST.get('question_id')
            question_list = atempted.split(",")
            if question_list is None:
                question_list = [99999999999999999]
            question = Question.objects.filter(quiz_id=quiz_id).exclude(id__in=question_list).order_by("id").first()
            if question:
                answer_set = Answer.objects.filter(question_id=question.id)
            else:
                message = "You Completed the certificate."

                context = {
                    'quiz': quiz,
                    'question': question,
                    'message': message,
                    'answer_set': answer_set,
                    'atemptted_question': atempted
                }
                return render(request, 'quiz/quiz.html', context)
        else:
            question = None
            message = "You provided the wrong answer. Better luck next time."
            print(request.POST.get('atemptted_question'))
        print(request)

    context = {
        'quiz': quiz,
        'question': question,
        'message': message,
        'answer_set': answer_set,
        'atemptted_question': atempted
    }
    return render(request, 'quiz/quiz.html', context)


def create_event_category(request):
    form = EventCategoryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            unsaved_form = form.save(commit=False)
            print(request.user)
            unsaved_form.created_by = request.user
            unsaved_form.save()
            return redirect('event_category_list')

    return render(request, 'event_category/create.html', {'form': form})


def edit_event_category(request, id):
    event_category = get_object_or_404(EventCategory, pk=id)

    # if answer.created_by != request.user:
    #     return HttpResponseForbidden()

    form = EventCategoryForm(request.POST or None, instance=event_category)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('event_category_list')

    return render(request, 'event_category/create.html', {'form': form})


def delete_event_category(request, id):
    EventCategory.objects.get(id=id).delete()
    return redirect('event_category_list')


def certificate_for_participant(request, event_id):
    event = Event.objects.get(id=event_id)
    is_quiz_required = event.is_quiz_required
    if event.is_quiz_required:
        quiz_list = Quiz.objects.filter(event_id=event_id).order_by('-id')
        if not quiz_list:
            return redirect('error_page')

        try:
            quiz_attempted = request.GET.get('quiz_attempted')
        except:
            quiz_attempted = "None"
        if quiz_attempted != "attempted":
            if quiz_list:
                quid_id = quiz_list.first().id
                return redirect('quiz_attempt_form', quid_id)
            else:
                return redirect('error_page')
        is_quiz_required = False

    if "SCFHS" in event.category.title:
        form = EventCertificateParticipantFormSCHFS(event_id, request.POST or None)
    else:
        form = EventCertificateParticipantForm(event_id, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.filter(is_superuser=True).first()
            try:
                if event and event.created_by:
                    user = event.created_by
            except:
                pass

            data = form.cleaned_data
            firstName = data["firstName"]
            lastName = data["lastName"]
            email = data["email"]
            if "SCFHS" in event.category.title:
                SCFHS_No = data["SCFHS_No"]
            else:
                SCFHS_No = "none"
            phone = data["phone"]
            country = data["country"]
            obj = EventParticipant.objects.create(event_id=event_id, firstName=firstName,
                                                  lastName=lastName,
                                                  email=email,
                                                  SCFHS_No=SCFHS_No,
                                                  phone=phone,
                                                  country=country, created_by=user)
            try:
                print("----------Envent-------",event)
                certificate = EventCertificate.objects.filter(event=event).latest('created_at')
                print(certificate.certificate_number)
                print(certificate.certificate_number)
                print(certificate.certificate_number)
                print(certificate.certificate_number)
                print(certificate.certificate_number)
                print(certificate.certificate_number)
                print(certificate.certificate_number)
                numbers = ''.join(filter(str.isdigit, certificate.certificate_number))
                numbers = int(numbers)
                numbers +=1
                try:
                    numbers = int(numbers)
                    numbers = "{:04d}".format(numbers)
                except ValueError:
                    print("Invalid integer value")
                if 'UK' in event.category.title:
                    e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id, certificate_number='CERTIFICATE SERIAL NUMBER_'+numbers,
                                                          created_by=user)
                    print('CERTIFICATE SERIAL NUMBER_'+numbers)
                else:
                    e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id, certificate_number='ML-'+numbers,
                                                          created_by=user)
                    print('ML-'+numbers)
            except:
                numbers = 1
                try:
                    numbers = int(numbers)
                    numbers = "{:04d}".format(numbers)
                    print(numbers)
                except ValueError:
                    print("Invalid integer value")
                if 'UK' in event.category.title:
                    e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                              certificate_number='CERTIFICATE SERIAL NUMBER_' + numbers,
                                                              created_by=user)
                    print('CERTIFICATE SERIAL NUMBER_' + numbers)
                else:
                    e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                              certificate_number='ML-' + numbers,
                                                              created_by=user)
                    print('ML-' + numbers)

            return redirect('preview_certificate', e_c_obj.id)

    context = {
        'form': form,
        'event': event,
        'quiz_required': is_quiz_required
    }
    return render(request, 'event_certificate/create.html', context)


def preview_certificate(request, id):
    certificate = EventCertificate.objects.get(id=id)
    event = None

    if certificate.event:
        event = certificate.event or certificate.eventParticipant.event

    context = {
        'event': event,
        'certificate': certificate
    }
    return render(request, 'event_certificate/certificate.html', context)


def event_list(request):
    user_created_events = Event.objects.filter(created_by=request.user)
    if request.user.is_superuser:
        user_created_events = Event.objects.filter()
    context = {
        'user_created_events': user_created_events
    }
    return render(request, 'events/index.html', context)


def create_event(request):
    form = ManagerEventForm(request.POST or None, request.FILES or None)

    if request.user.is_superuser:
        form = EventForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            unsaved_form = form.save(commit=False)
            unsaved_form.created_by = request.user
            unsaved_form.save()
            instance = form.instance
            if instance.is_quiz_required:
                return HttpResponseRedirect('/dashboard/quiz/create/' + f'?event_id={instance.id}')

            return redirect('event_list')

    return render(request, 'events/create.html', {'form': form})


def edit_event(request, id):
    event = get_object_or_404(Event, pk=id)

    # if answer.created_by != request.user:
    #     return HttpResponseForbidden()
    form = ManagerEventForm(request.POST or None, request.FILES or None, instance=event)
    if request.user.is_superuser:
        form = EventForm(request.POST or None, request.FILES or None, instance=event)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('event_list')

    return render(request, 'events/create.html', {'form': form})


def delete_event(request, id):
    try:
        Event.objects.get(id=id, created_by=request.user).delete()
    except:
        pass
    return redirect('event_list')


def event_participant(request, id):
    try:
        user_events = [Event.objects.get(id=id, created_by=request.user).id]
    except:
        user_events = []
    eventList = Event.objects.filter(id=id, created_by=request.user)
    if request.method == "POST":
        try:
            # read by default 1st sheet of an excel file
            event = Event.objects.get(id=request.POST.get('events_id'))
            user = User.objects.filter(is_superuser=True).first()
            if event and event.created_by:
                user = event.created_by
            if request.FILES['file']:
                file = request.FILES['file']
            df = pd.read_excel(file)
            start_certificate_id = None
            for index, row in df.iterrows():
                firstName = row["firstName"]
                lastName = row["lastName"]
                email = row["email"]
                if "SCFHS" in event.category.title:
                    SCFHS_No = row["SCFHS_No"]
                else:
                    SCFHS_No = "none"
                phone = row["phone"]
                country = row["country"]
                obj = EventParticipant.objects.create(event=event, firstName=firstName,
                                                      lastName=lastName,
                                                      email=email,
                                                      SCFHS_No=SCFHS_No,
                                                      phone=phone,
                                                      country=country, created_by=user)
                try:
                    certificate = EventCertificate.objects.filter(event=event).latest('created_at')
                    print(certificate.certificate_number)
                    numbers = ''.join(filter(str.isdigit, certificate.certificate_number))
                    numbers = int(numbers)
                    numbers += 1
                    try:
                        numbers = int(numbers)
                        numbers = "{:04d}".format(numbers)
                    except ValueError:
                        print("Invalid integer value")

                    if 'UK' in event.category.title:
                        e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                                  certificate_number='CERTIFICATE SERIAL NUMBER_' + numbers,
                                                                  created_by=user)
                        print('CERTIFICATE SERIAL NUMBER_' + numbers)

                    else:
                        e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                                  certificate_number='ML-' + numbers,
                                                                  created_by=user)
                        print('ML-' + numbers)
                    if not start_certificate_id:
                        start_certificate_id = e_c_obj.id
                    if not index < 50:
                        break
                except:
                    numbers = 1
                    try:
                        numbers = int(numbers)
                        numbers = "{:04d}".format(numbers)
                        print(numbers)
                    except ValueError:
                        print("Invalid integer value")

                    if 'UK' in event.category.title:
                        e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                                  certificate_number='CERTIFICATE SERIAL NUMBER_' + numbers,
                                                                  created_by=user)
                        print('CERTIFICATE SERIAL NUMBER_' + numbers)

                    else:
                        e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                                  certificate_number='ML-' + numbers,
                                                                  created_by=user)

                        print('ML-' + numbers)
                    if not start_certificate_id:
                        start_certificate_id = e_c_obj.id
            return redirect('generate_bulk_certificate', event.id, start_certificate_id)
        except:
            participants = EventParticipant.objects.filter(created_by=request.user)
            # Create a new workbook and sheet
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            # Add headers to the sheet
            headers = ['firstName', 'lastName', 'Email', 'Event', 'Phone', 'Country']
            sheet.append(headers)
            # Add data to the sheet
            for row in participants:
                row_data = [row.firstName, row.lastName, row.email, row.event.title, row.phone, row.country]
                sheet.append(row_data)
            # Set the response headers
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=participants.xlsx'
            # Write the workbook to the response
            workbook.save(response)
            return response
    context = {
        'eventList': eventList,
        'event_participants': EventParticipant.objects.filter(event_id__in=user_events)
    }
    return render(request, 'event_participant/index.html', context)


def user_created_participant(request):

    eventList = Event.objects.filter(created_by=request.user)
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        try:
            # read by default 1st sheet of an excel file
            event = Event.objects.get(id=request.POST.get('events_id'))
            user = User.objects.filter(is_superuser=True).first()
            if event and event.created_by:
                user = event.created_by
            if request.FILES['file']:
                file = request.FILES['file']
            df = pd.read_excel(file)
            start_certificate_id = None
            for index, row in df.iterrows():
                firstName = row["firstName"]
                lastName = row["lastName"]
                email = row["email"]
                if "SCFHS" in event.category.title:
                    SCFHS_No = row["SCFHS_No"]
                else:
                    SCFHS_No = "none"
                phone = row["phone"]
                country = row["country"]
                obj = EventParticipant.objects.create(event=event, firstName=firstName,
                                                      lastName=lastName,
                                                      email=email,
                                                      SCFHS_No=SCFHS_No,
                                                      phone=phone,
                                                      country=country, created_by=user)
                try:
                    certificate = EventCertificate.objects.filter(event=event).latest('created_at')
                    print(certificate.certificate_number)
                    numbers = ''.join(filter(str.isdigit, certificate.certificate_number))
                    numbers = int(numbers)
                    numbers += 1
                    try:
                        numbers = int(numbers)
                        numbers = "{:04d}".format(numbers)
                    except ValueError:
                        print("Invalid integer value")

                    if 'UK' in event.category.title:
                        e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                                  certificate_number='CERTIFICATE SERIAL NUMBER_' + numbers,
                                                                  created_by=user)
                        print('CERTIFICATE SERIAL NUMBER_' + numbers)

                    else:
                        e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                                  certificate_number='ML-' + numbers,
                                                                  created_by=user)
                        print('ML-' + numbers)
                    if not start_certificate_id:
                        start_certificate_id = e_c_obj.id
                    if not index < 50:
                        break
                except:
                    numbers = 1
                    try:
                        numbers = int(numbers)
                        numbers = "{:04d}".format(numbers)
                        print(numbers)
                    except ValueError:
                        print("Invalid integer value")

                    if 'UK' in event.category.title:
                        e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                                  certificate_number='CERTIFICATE SERIAL NUMBER_' + numbers,
                                                                  created_by=user)
                        print('CERTIFICATE SERIAL NUMBER_' + numbers)

                    else:
                        e_c_obj = EventCertificate.objects.create(event=event, eventParticipant_id=obj.id,
                                                                  certificate_number='ML-' + numbers,
                                                                  created_by=user)
                        print('ML-' + numbers)
                    if not start_certificate_id:
                        start_certificate_id = e_c_obj.id
            return redirect('generate_bulk_certificate', event.id, start_certificate_id)
        except:
            participants = EventParticipant.objects.filter(created_by=request.user)
            # Create a new workbook and sheet
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            # Add headers to the sheet
            headers = ['firstName', 'lastName', 'Email', 'Event', 'Phone', 'Country']
            sheet.append(headers)
            # Add data to the sheet
            for row in participants:
                row_data = [row.firstName, row.lastName, row.email, row.event.title, row.phone, row.country]
                sheet.append(row_data)
            # Set the response headers
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=participants.xlsx'
            # Write the workbook to the response
            workbook.save(response)
            return response

    context = {
        'event_participants': EventParticipant.objects.filter(created_by=request.user),
        'eventList': eventList
    }

    return render(request, 'event_participant/index.html', context)


def create_event_participant(request):
    form = EventParticipantForm(request.user.id, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            unsaved_form = form.save(commit=False)
            unsaved_form.created_by = request.user
            unsaved_form.save()
            return redirect('user_created_participant')

    return render(request, 'event_participant/create.html', {'form': form})


def delete_event_participant(request, id):
    event_participant = get_object_or_404(EventParticipant, pk=id)

    # Ensure that only the user who created the event participant can delete it
    if event_participant.created_by != request.user:
        return HttpResponseForbidden()

    # if request.method == 'POST':
    event_participant.delete()
    return redirect('user_created_participant')

    # context = {'event_participant': event_participant}
    # return render(request, 'event_participant/index.html', context)


def edit_event_participant(request, id):
    event_participant = get_object_or_404(EventParticipant, pk=id)

    # Ensure that only the user who created the event participant can edit it
    if event_participant.created_by != request.user:
        return HttpResponseForbidden()

    form = EventParticipantForm(request.user.id, request.POST or None, instance=event_participant)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('user_created_participant')

    return render(request, 'event_participant/create.html', {'form': form})


def event_certificates(request):
    context = {
        'certificate_list': EventCertificate.objects.filter(created_by=request.user)
    }
    return render(request, 'event_certificate/index.html', context)


def generate_bulk_certificate(request, event_id, id):
    event = Event.objects.get(id=event_id)
    context = {
        'event': event,
        'certificate_list': EventCertificate.objects.filter(event_id=event_id,id__gte=id, created_by=request.user)
    }
    return render(request, 'event_certificate/bulk_certificate.html', context)


def delete_event_certificate(request, id):
    try:
        EventCertificate.objects.get(id=id, created_by=request.user).delete()
    except:
        pass
    return redirect('event_certificates')


def create_quiz(request):
    form = QuizForm(request.user, request.GET.get('event_id'), request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            unsaved_form = form.save(commit=False)
            unsaved_form.created_by = request.user
            unsaved_form.save()
            instance = form.instance

            return redirect('add_quiz_questions', instance.id)

    return render(request, 'quiz/create.html', {'form': form})


def edit_quiz(request, id):
    quiz = get_object_or_404(Quiz, pk=id)

    # if answer.created_by != request.user:
    #     return HttpResponseForbidden()

    form = QuizForm(request.user, request.GET.get('event_id'), request.POST or None, instance=quiz)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('quiz')

    return render(request, 'quiz/create.html', {'form': form, 'quiz': quiz})


def all_user_quiz(request):
    context = {
        'all_user_quiz': Quiz.objects.filter(created_by=request.user)
    }
    return render(request, 'quiz/index.html', context)


def delete_quiz(request, id):
    try:
        Quiz.objects.get(id=id, created_by=request.user).delete()
    except:
        pass
    return redirect('quiz')


def quiz_questions(request, quiz_id):
    context = {
        'quiz': Quiz.objects.get(id=quiz_id),
        'questions': Question.objects.filter(quiz_id=quiz_id, quiz__created_by=request.user)
    }
    return render(request, 'questions/index.html', context)


def add_quiz_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    is_correct = False
    if request.method == 'POST':
        question = Question.objects.create(quiz_id=quiz_id, text=request.POST.get('question'))
        for text in request.POST.getlist('answer'):
            if text and not text == '':
                if text == 'on':
                    is_correct = True
                else:
                    ans = Answer.objects.create(question_id=question.id, text=text, is_correct=is_correct)
                    is_correct = False

        return redirect('quiz_questions', quiz_id)

    return render(request, 'questions/create.html', {'quiz': quiz})


def edit_question(request, id):
    question = get_object_or_404(Question, pk=id)

    # if answer.created_by != request.user:
    #     return HttpResponseForbidden()

    form = QuizQuestionForm(request.POST or None, instance=question)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('quiz_questions', question.quiz_id)

    return render(request, 'questions/edit.html', {'form': form, 'quiz': question.quiz})


def delete_question(request, id):
    question = Question.objects.get(id=id, quiz__created_by=request.user)
    quiz_id = question.quiz_id
    question.delete()
    return redirect('quiz_questions', quiz_id)


def answers_of_question(request, question_id):
    context = {
        'question': Question.objects.get(id=question_id),
        'answers': Answer.objects.filter(question_id=question_id, question__quiz__created_by=request.user)
    }
    return render(request, 'answers/index.html', context)


def add_answers_to_question(request, question_id):
    question = Question.objects.get(id=question_id)
    form = AnswerForm(request.POST or None)

    if request.method == 'POST':
        for text in request.POST.getlist('text[]'):
            if text and not text == '':
                ans = Answer.objects.create(question_id=question_id, text=text)

        return redirect('quiz_questions', question.quiz_id)

    return render(request, 'answers/create.html', {'form': form, 'question': question})


def edit_answer(request, id):
    answer = get_object_or_404(Answer, pk=id)

    # if answer.created_by != request.user:
    #     return HttpResponseForbidden()

    form = AnswerForm(request.POST or None, instance=answer)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('quiz_questions', answer.question.quiz_id)

    return render(request, 'answers/edit.html', {'form': form, 'question': answer.question})


def mark_answer_as_correct(request, id):
    answer = get_object_or_404(Answer, pk=id)
    other_asnwers = Answer.objects.filter(question_id=answer.question_id).exclude(id=id)
    other_asnwers.update(is_correct=False)
    answer.is_correct = True
    answer.save()
    return redirect('quiz_questions', answer.question.quiz_id)


def delete_answer(request, id):
    try:
        answer = Answer.objects.get(id=id, question__quiz__created_by=request.user)
        quiz_id = answer.question.quiz_id
        answer.delete()
    except:
        pass
    return redirect('quiz_questions', quiz_id)
