# quiz/serializers.py
from rest_framework import serializers
from .models import Question, Answer, Profile


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)  # Remove the `source='answers'` argument

    class Meta:
        model = Question
        fields = ["id", "text", "answers"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "points"]
