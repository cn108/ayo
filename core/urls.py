# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudyGroupViewSet
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'study-groups', StudyGroupViewSet)


urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('schedule/', views.schedule, name='schedule'),
    path('assignments/edit/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),
    path('assignments/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('assignments/', views.assignments, name='assignments'),
    path('study-groups/', views.study_groups, name='study_groups'),
    path('create-study-group/', views.create_study_group, name='create_study_group'),
    path('edit-study-group/<int:pk>/', views.edit_study_group, name='edit_study_group'),
    path('delete-study-group/<int:pk>/', views.delete_study_group, name='delete_study_group'),
    path('study-group-data/', views.study_group_data, name='study_group_data'),
    path('search/', views.search_study_groups, name='search_study_groups'),
    path('grades/', views.grades, name='grades'),
    path('grades/update/<int:pk>/', views.update_grade, name='update_grade'),
    path('grades/delete/<int:pk>/', views.delete_grade, name='delete_grade'),
    path('schedule/add/', views.add_schedule, name='add_schedule'),
    path('schedule-get/', views.get_schedules, name='get_schedules'),
    path('schedule/update/<int:id>/', views.update_schedule, name='update_schedule'),
    path('schedule/delete/<int:id>/', views.delete_schedule, name='delete_schedule'),
]