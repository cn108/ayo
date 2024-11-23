from django.contrib import admin
from .models import Assignment, StudyGroup, Grade, Student, Schedule


admin.site.register(Assignment)
admin.site.register(StudyGroup)
admin.site.register(Grade)
admin.site.register(Student)
admin.site.register(Schedule)