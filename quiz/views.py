from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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

    for answer_data in data["answers"]:
        question_id = answer_data.get("question_id")
        selected_answer_id = answer_data.get("selected_answer")

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            continue

        # Check if the selected answer is correct
        if question.answers.filter(id=selected_answer_id, is_correct=True).exists():
            correct_answers += 1

    # Update user's total score
    profile = Profile.objects.get(user=user)
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
