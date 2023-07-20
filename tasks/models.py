from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    # Fields of the Task model
    title = models.CharField(max_length=200)  # CharField for the task title with a maximum length of 200 characters.
    description = models.TextField(max_length=1000)  # TextField for the task description with a maximum length of 1000 characters.
    created = models.DateTimeField(auto_now_add=True)  # DateTimeField to store the creation date and time of the task. It is automatically set to the current date and time when the object is created.
    datecompleted = models.DateTimeField(null=True, blank=True)  # DateTimeField to store the completion date and time of the task. It can be left empty (null=True) and can be shown as an empty string in the template (blank=True).
    important = models.BooleanField(default=False)  # BooleanField to indicate whether the task is important or not. It is set to False by default.
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link the task with a user. If a user is deleted, all related tasks will also be deleted (on_delete=models.CASCADE).

    # Method to display a string representation of the Task object.
    def __str__(self):
        return self.title + ' - ' + self.user.username

