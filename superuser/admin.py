from django.contrib import admin
from .models import *

admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(EventParticipant)
admin.site.register(EventCertificate)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(SubmittedAnswer)
