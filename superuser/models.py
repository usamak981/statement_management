from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
statusChoices = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]


class EventCategory(models.Model):
    title = models.CharField(max_length=2000, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='media')
    background_img = models.ImageField(upload_to='media', null=True, blank=True)
    title = models.CharField(max_length=2000, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=200, choices=statusChoices, default='Pending')
    event_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    cpd_approval_no = models.CharField(max_length=512, null=True, blank=True)
    cpd_org_no = models.CharField(max_length=512, null=True, blank=True)
    location = models.CharField(max_length=512, null=True, blank=True)
    points = models.FloatField(null=True, blank=True)
    mumaris_days = models.IntegerField(null=True, blank=True)
    accreditation_no = models.CharField(max_length=512, null=True, blank=True)
    facility_number = models.CharField(max_length=512, null=True, blank=True)
    is_quiz_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " of " + self.category.title


class EventParticipant(models.Model):
    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    firstName = models.CharField(max_length=2000)
    lastName = models.CharField(max_length=2000)
    email = models.EmailField()
    SCFHS_No = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstName + " " + self.lastName


class EventCertificate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, null=True, blank=True)
    eventParticipant = models.ForeignKey(EventParticipant, on_delete=models.CASCADE)
    certificate_number = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.event is not None:
            return f"{self.certificate_number} - {self.event.title}"
        else:
            return f"{self.certificate_number} - <no event>"


class Quiz(models.Model):
    eventCategory = models.ForeignKey(EventCategory, on_delete=models.CASCADE, default=None, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, null=True, blank=True)
    title = models.CharField(max_length=2000, unique=True)
    description = models.CharField(max_length=2000, unique=True)
    end_Date_Time = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class SubmittedAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_submitted_answer_correct = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
