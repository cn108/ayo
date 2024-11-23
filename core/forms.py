from django import forms
from .models import StudyGroup, Subject, Assignment

class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'members', 'schedule', 'meeting_time', 'location']
        
class GradeForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'grade', 'credit')
    
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'due_date', 'status']