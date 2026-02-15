from django.urls import path
from . import views
from .views import chatbot

urlpatterns = [
    path("chatbot/", chatbot, name="chatbot"),
    path("faculty/attendance/", views.faculty_attendance, name="faculty_attendance"),
    path("faculty/assignments/", views.faculty_assignments, name="faculty_assignments"),
    path("faculty/study-materials/", views.faculty_study_materials, name="faculty_study_materials"),
]
