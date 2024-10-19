# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator  # For CSRF exemption decorator
from django.contrib.auth.models import User
from .models import Question, Profile
from .serializers import QuestionSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])  # Require authentication for managing questions
def manage_questions(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])  # Require authentication for modifying questions
def modify_question(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response({"error": "Question not found."}, status=404)

    if request.method == "PUT":
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        question.delete()
        return Response({"message": "Question deleted successfully."}, status=204)


@api_view(["POST"])
@permission_classes(
    [IsAuthenticated]
)  # Require authentication for submitting quiz answers
def submit_quiz(request):
    """
    Endpoint to submit quiz answers, calculate score, and update user's total score.
    """
    user = request.user  # The authenticated user
    data = request.data  # Data from the frontend, including selected answers
    correct_answers = 0  # Track the number of correct answers

    # Ensure 'answers' is in the request data
    if not data.get("answers"):
        return Response({"error": "Answers data is required."}, status=400)

    for answer_data in data["answers"]:
        question_id = answer_data.get("question_id")
        selected_answer_id = answer_data.get("selected_answer")

        if not question_id or not selected_answer_id:
            continue

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            continue

        # Check if the selected answer is correct
        if question.answers.filter(id=selected_answer_id, is_correct=True).exists():
            correct_answers += 1

    # Update user's total score
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found."}, status=404)

    profile.total_score += correct_answers
    profile.save()

    return Response(
        {
            "message": "Quiz submitted successfully.",
            "correct_answers": correct_answers,
            "total_score": profile.total_score,
        },
        status=200,
    )


@csrf_exempt  # Add CSRF exemption here to ensure it's recognized
@api_view(["POST"])
@permission_classes([IsAuthenticated])  # Require authentication for gifting points
def gift_points(request):
    """
    Endpoint to allow a user to gift points to another user.
    """
    sender = request.user
    recipient_username = request.data.get("recipient")
    points_to_gift = request.data.get("points")

    # Validate points_to_gift
    try:
        points_to_gift = int(points_to_gift)
        if points_to_gift <= 0:
            raise ValueError("Points must be a positive number.")
    except (TypeError, ValueError):
        return Response({"error": "Points must be a positive integer."}, status=400)

    try:
        recipient = User.objects.get(username=recipient_username)
        recipient_profile = Profile.objects.get(user=recipient)
    except User.DoesNotExist:
        return Response({"error": "Recipient not found."}, status=404)
    except Profile.DoesNotExist:
        return Response({"error": "Recipient profile not found."}, status=404)

    # Check if the sender has enough points
    try:
        sender_profile = Profile.objects.get(user=sender)
        if sender_profile.points < points_to_gift:
            return Response({"error": "Insufficient points."}, status=400)
    except Profile.DoesNotExist:
        return Response({"error": "Sender profile not found."}, status=404)

    # Transfer points
    sender_profile.points -= points_to_gift
    recipient_profile.points += points_to_gift
    sender_profile.save()
    recipient_profile.save()

    return Response(
        {"message": "Points gifted successfully.", "points_gifted": points_to_gift},
        status=200,
    )
