from django import forms
from .models import *
from django.core.validators import validate_email, ValidationError
import re
from django.forms import DateTimeInput


class SignupForm(forms.ModelForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your Username'}),
                               error_messages={'required': 'Username is required.'})

    email = forms.CharField(max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}),
                            error_messages={'required': 'Email is required.'})

    password = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
                               error_messages={'required': 'Please enter password'})

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        raiseValidation = False

        if re.match(r"\w[\w\.-]*@\w[\w\.-]+\.\w+", email) == None:
            raise forms.ValidationError('Email is not valid')
        if not email:
            raise forms.ValidationError('Enter email address.')
        try:
            validate_email(email)

        except ValidationError as e:
            raise forms.ValidationError('Invalid email address')
        if User.objects.filter(email__iexact=email).count() > 0 or User.objects.filter(
                email__iexact=email).count() > 0:
            raise forms.ValidationError('Email already exists.')
        return email


class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['title', 'description', 'created_by']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['category', 'logo', 'background_img', 'title', 'description', 'status', 'location', 'points', 'event_date',
                  'cpd_approval_no', 'cpd_org_no', 'mumaris_days', 'accreditation_no', 'facility_number', 'is_quiz_required']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        self.fields['cpd_approval_no'].label = "CPD Approval Number"
        self.fields['mumaris_days'].widget.attrs['placeholder'] = "No of Days"
        self.fields['mumaris_days'].label = "The SCFHS CME Hours will be automatically registered in your account on MUMARIS PLUS within ______ Days. "
        print(self.fields['cpd_approval_no'].widget)
        self.fields['cpd_org_no'].label = "CPD Organization Number"
        self.fields['accreditation_no'].label = "Under Accreditation ID Number"
        self.fields['facility_number'].label = "Facility Number"
        self.fields['background_img'].label = "Background Image"
        self.fields['points'].label = "No. CPD Hours/Points"
        self.fields['event_date'].widget.attrs.update({
            'type': 'date',
            'data-format': 'yyyy-MM-dd hh:mm:ss',
            'placeholder': 'yyyy-MM-dd hh:mm:ss',
        })
        self.fields['event_date'].label = "Date of CPD Activity"
        # self.fields['event_date'].widget.attrs['data-format'] = "yyyy-MM-dd hh:mm:ss"
        # self.fields['event_date'].widget.attrs['placeholder'] = "yyyy-MM-dd hh:mm:ss"


class ManagerEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['category', 'logo', 'background_img', 'title', 'description', 'location', 'points', 'event_date', 'cpd_approval_no',
                  'cpd_org_no', 'mumaris_days', 'accreditation_no', 'facility_number', 'is_quiz_required']

    def __init__(self, *args, **kwargs):
        super(ManagerEventForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        self.fields['cpd_approval_no'].label = "CPD Approval Number"
        print(self.fields['cpd_approval_no'].widget)
        self.fields['cpd_org_no'].label = "CPD Organization Number"
        self.fields['background_img'].label = "Background Image"
        self.fields['points'].label = "No. CPD Hours/Points"
        self.fields['mumaris_days'].widget.attrs['placeholder'] = "No of Days"
        self.fields['mumaris_days'].label = "The SCFHS CME Hours will be automatically registered in your account on MUMARIS PLUS within ______ Days. "
        self.fields['event_date'].widget.attrs['data-format'] = "yyyy-MM-dd hh:mm:ss"
        self.fields['event_date'].widget.attrs['placeholder'] = "yyyy-mm-dd hh:mm:ss"


class EventParticipantForm(forms.ModelForm):
    class Meta:
        model = EventParticipant
        fields = ['event', 'firstName', 'lastName', 'email', 'phone', 'country']

    def __init__(self, user_id, *args, **kwargs):
        super(EventParticipantForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].label = "First Name"
        self.fields['lastName'].label = "Last Name"
        self.fields['event'] = forms.ModelChoiceField(required=True,
                                                      queryset=Event.objects.filter(created_by_id=user_id),
                                                      empty_label=None)


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['event', 'title', 'description', 'end_Date_Time']
        widgets = {'end_Date_Time': DateTimeInput()}

    def __init__(self, user_id, event_id, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        if not event_id:
            query = Event.objects.filter(created_by=user_id)
        else:
            query = Event.objects.filter(id=event_id)

        self.fields['event'] = forms.ModelChoiceField(required=True, queryset=query, empty_label=None)


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']


class EventCertificateParticipantForm(forms.ModelForm):
    class Meta:
        model = EventParticipant
        fields = ['event', 'firstName', 'lastName', 'email', 'phone', 'country']

    def __init__(self, event_id, *args, **kwargs):
        super(EventCertificateParticipantForm, self).__init__(*args, **kwargs)
        self.fields['event'] = forms.ModelChoiceField(required=True, queryset=Event.objects.filter(id=event_id),
                                                      empty_label=None)
        self.fields['event'].widget.attrs['class'] = "form-control"
        self.fields['firstName'].widget.attrs['class'] = "form-control"
        self.fields['lastName'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['class'] = "form-control"
        self.fields['phone'].widget.attrs['class'] = "form-control"
        self.fields['country'].widget.attrs['class'] = "form-control"
        self.fields['firstName'].label = "First Name"
        self.fields['lastName'].label = "Last Name"


class EventCertificateParticipantFormSCHFS(forms.ModelForm):
    class Meta:
        model = EventParticipant
        fields = ['event', 'firstName', 'lastName', 'email', 'SCFHS_No', 'phone', 'country']

    def __init__(self, event_id, *args, **kwargs):
        super(EventCertificateParticipantFormSCHFS, self).__init__(*args, **kwargs)
        self.fields['event'] = forms.ModelChoiceField(required=True, queryset=Event.objects.filter(id=event_id),
                                                      empty_label=None)
        self.fields['event'].widget.attrs['class'] = "form-control"
        self.fields['firstName'].widget.attrs['class'] = "form-control"
        self.fields['lastName'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['class'] = "form-control"
        self.fields['SCFHS_No'].widget.attrs['class'] = "form-control"
        self.fields['phone'].widget.attrs['class'] = "form-control"
        self.fields['phone'].required = True
        self.fields['country'].widget.attrs['class'] = "form-control"
        self.fields['country'].required = True
        self.fields['firstName'].label = "First Name"
        self.fields['lastName'].label = "Last Name"
