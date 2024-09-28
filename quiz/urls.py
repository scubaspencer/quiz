# quiz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("api/questions/", views.manage_questions, name="manage-questions"),
    path("api/questions/<int:pk>/", views.modify_question, name="modify-question"),
]
