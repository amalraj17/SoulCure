from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Payment)
admin.site.register(TherapySessionFeedbacks)
admin.site.register(FeedbackQuestions)
admin.site.register(FeedbackOption)
admin.site.register(QuestionnaireQuestions)
admin.site.register(QuestionnaireOption)
admin.site.register(Questionnaire)


