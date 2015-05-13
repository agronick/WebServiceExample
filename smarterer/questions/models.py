from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=200)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    choice = models.CharField(max_length=50)
    correct = models.BooleanField()