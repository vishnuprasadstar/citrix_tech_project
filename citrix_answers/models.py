from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.TextField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    citrix_username = models.TextField(max_length=500, blank=True)
    description = models.TextField(max_length=500, blank=True)
    designation = models.CharField(max_length=30, blank=True)
    team = models.CharField(max_length=30, blank=True)
    rating = models.IntegerField(default=10)

    def __unicode__(self):
        return self.citrix_username

class Question(models.Model):
    title = models.TextField(max_length=500, blank=True)
    description = models.TextField(max_length=500, blank=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    has_solution = models.IntegerField(default=0)

    user = models.ForeignKey(User, related_name="user_name_question")
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title

class Answer(models.Model):
    content = models.TextField(max_length=500, blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    is_solution = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    question = models.ForeignKey(Question, related_name="question_answer")

    user = models.ForeignKey(User, related_name="user_name_answer")

    #upvoted_users = models.ManyToManyField(User, related_name="upvoted_user")
    #downvoted_users = models.ManyToManyField(User, related_name="downvoted_user")

    def __unicode__(self):
        return self.content
