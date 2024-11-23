from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import StudyGroupForm, GradeForm, AssignmentForm
import logging
from django.utils import timezone
from rest_framework import viewsets
from .serializers import StudyGroupSerializer
from rest_framework.permissions import IsAuthenticated
from .models import StudyGroup, Subject, Assignment, Schedule
from django.db.models import Sum
import requests, json

logger = logging.getLogger(__name__)

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def schedule(request):
    return render(request, 'core/schedule.html')

@csrf_exempt
def add_schedule(request):
    if request.method == "POST":
        data = json.loads(request.body)
        schedule_item = Schedule.objects.create(
            name=data['name'],
            time=data['time'],
            day=data['day']
        )
        return JsonResponse({'id': schedule_item.id, 'name': schedule_item.name, 'time': str(schedule_item.time), 'day': schedule_item.day})

def get_schedules(request):
    schedules = Schedule.objects.all()
    schedule_list = [{'id': schedule.id, 'name': schedule.name, 'time': str(schedule.time), 'day': schedule.day} for schedule in schedules]
    return JsonResponse(schedule_list, safe=False)

@csrf_exempt
def update_schedule(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        schedule_item = Schedule.objects.get(id=id)
        schedule_item.name = data['name']
        schedule_item.time = data['time']
        schedule_item.day = data['day']
        schedule_item.save()
        return JsonResponse({'id': schedule_item.id, 'name': schedule_item.name, 'time': str(schedule_item.time), 'day': schedule_item.day})

@csrf_exempt
def delete_schedule(request, id):
    if request.method == "DELETE":
        schedule_item = Schedule.objects.get(id=id)
        schedule_item.delete()
        return JsonResponse({'status': 'success'})


@login_required
def assignments(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            logger.info(f'Assignment "{assignment.title}" saved for user {request.user.username} at {timezone.now()}')
            return redirect('assignments')
        else:
            logger.warning(f'Form errors: {form.errors}')
    else:
        form = AssignmentForm()

    user_assignments = Assignment.objects.filter(user=request.user)
    return render(request, 'core/assignments.html', {'assignments': user_assignments, 'form': form})

@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            logger.info(f'Assignment "{assignment.title}" updated for user {request.user.username} at {timezone.now()}')
            return redirect('assignments')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'core/edit_assignment.html', {'form': form})

@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
    if request.method == 'POST':
        assignment.delete()
        logger.info(f'Assignment "{assignment.title}" deleted for user {request.user.username} at {timezone.now()}')
        return redirect('assignments')
    return render(request, 'core/delete_assignment.html', {'assignment': assignment})


@login_required
def study_groups(request):
    study_groups = StudyGroup.objects.all()
    logger.info(f"Retrieved {study_groups.count()} study groups.")
    return render(request, 'core/study_groups.html', {'study_groups': study_groups})

from django.contrib.auth.models import User

@login_required
def create_study_group(request):
    users = User.objects.all()  # Fetch all users to display in the form
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("Study group created successfully.")
            return redirect('study_groups')
        else:
            logger.error(f"Form is not valid. Errors: {form.errors}")
    else:
        form = StudyGroupForm()
    return render(request, 'core/create_study_group.html', {'form': form, 'users': users})

@login_required
def edit_study_group(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)
    if request.method == 'POST':
        form = StudyGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('study_groups')  # Redirect to the study groups list page
    else:
        form = StudyGroupForm(instance=group)
    return render(request, 'core/edit_study_group.html', {'form': form})

@login_required
def delete_study_group(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('study_groups')  # Redirect to the study groups list page
    return render(request, 'core/delete_study_group.html', {'group': group})

@login_required
def study_group_data(request):
    study_groups = StudyGroup.objects.all()
    data = {
        'names': [group.name for group in study_groups],
        'meeting_times': [group.meeting_time.strftime('%H:%M') for group in study_groups],  # Ensure correct format
        'locations': [group.location for group in study_groups],
    }
    return JsonResponse(data)

@login_required
def search_study_groups(request):
    query = request.GET.get('q', '')
    results = StudyGroup.objects.filter(name__icontains=query)
    data = [{'id': group.id, 'name': group.name, 'meeting_time': group.meeting_time, 'location': group.location} for group in results]
    return JsonResponse(data, safe=False)

@login_required
def grades(request):
    subjects = Subject.objects.filter(user=request.user)

    total_credits = subjects.aggregate(Sum('credit'))['credit__sum'] or 0
    total_grade_points = subjects.aggregate(Sum('grade_points'))['grade_points__sum'] or 0
    cgpa = total_grade_points / total_credits if total_credits > 0 else 0

    form = GradeForm(request.POST or None)
    if form.is_valid():
        grade = form.save(commit=False)
        grade.user = request.user  # Assign the current user to the grade
        grade.save()
        return redirect('grades')

    return render(request, 'core/grades.html', {'subjects': subjects, 'cgpa': cgpa, 'form': form})

@login_required
def update_grade(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = GradeForm(instance=subject)
    return render(request, 'core/update_grade.html', {'form': form})

@login_required
def delete_grade(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        subject.delete()
        return redirect('grades')
    return render(request, 'core/delete_grade.html', {'subject': subject})

class StudyGroupViewSet(viewsets.ModelViewSet):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    permission_classes = [IsAuthenticated]