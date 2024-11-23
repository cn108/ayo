from rest_framework import serializers
from .models import StudyGroup

class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'meeting_time', 'location']