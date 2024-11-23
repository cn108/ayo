from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,time

class Student(models.Model):
    name = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=3, decimal_places=2)
    
class StudyGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(User)
    schedule = models.TextField(default="No schedule provided")
    meeting_time = models.TimeField(default=time(0, 0))  # Add this
    location = models.CharField(max_length=255, default="TBD")  # Add this
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    grade = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    credit = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    grade_points = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
# models.py

class Schedule(models.Model):
    name = models.CharField(max_length=255)
    time = models.TimeField()
    day = models.CharField(max_length=10)  # e.g., 'Monday', 'Tuesday', etc.

    def __str__(self):
        return f"{self.name} on {self.day} at {self.time}"
