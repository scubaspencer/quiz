# quiz/urls.py
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Endpoints for managing questions
    path(
        "api/questions/", views.manage_questions, name="manage-questions"
    ),  # GET and POST questions
    path(
        "api/questions/<int:pk>/", views.modify_question, name="modify-question"
    ),  # PUT and DELETE questions
    # Endpoint for submitting the quiz and updating scores
    path(
        "api/submit-quiz/", views.submit_quiz, name="submit-quiz"
    ),  # POST quiz answers and update score
    # Endpoint for gifting points
    path(
        "api/gift-points/", views.gift_points, name="gift-points"
    ),  # POST to gift points to another user
    # JWT Authentication endpoints
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # For login and token creation
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # For refreshing JWT tokens
]
