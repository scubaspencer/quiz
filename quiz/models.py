# models.py
from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)  # Field to store the total score
    points = models.IntegerField(
        default=0
    )  # Field to store points available for gifting

    def __str__(self):
        return f"{self.user.username} - Total Score: {self.total_score}, Points: {self.points}"


class Question(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
