from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username  

class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)  # Auto-incremented ID
    topic_name = models.CharField(max_length=255)  # Topic Name
    gif_url = models.URLField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = "topics"  # Explicitly set the correct table name

    def __str__(self):
        return self.topic_name  # Fix: Use the correct field name

class Formula(models.Model):
    formula_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Link formulas to a topic
    formula_text = models.TextField()

    class Meta:
        db_table = "formulas"

    def __str__(self):
        # You can return a short version or the first 50 characters of the formula
        return self.formula_text[:50]

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  
    question_text = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    answer = models.TextField()  

    class Meta:
        db_table = "questions"

    def __str__(self):
        return f"{self.question_text[:50]}..."
