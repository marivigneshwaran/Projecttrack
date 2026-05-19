from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskListMasterAPI, TaskMasterAPI, SubTaskMasterAPI, TaskAssigneeAPI

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Task List Routing
    path('task-lists/list/', TaskListMasterAPI.as_view()), # Added /list/
    path('task-lists/create/', TaskListMasterAPI.as_view()),
    path('task-lists/update/<int:pk>/', TaskListMasterAPI.as_view()),
    path('task-lists/delete/<int:pk>/', TaskListMasterAPI.as_view()),
    
    # Task Routing
    path('tasks/list/', TaskMasterAPI.as_view()), # Added /list/
    path('tasks/create/', TaskMasterAPI.as_view()),
    path('tasks/update/<int:pk>/', TaskMasterAPI.as_view()),
    path('tasks/delete/<int:pk>/', TaskMasterAPI.as_view()),
    
    # Sub Task Routing
    path('sub-tasks/list/', SubTaskMasterAPI.as_view()), # Added /list/ to match your Postman request
    path('sub-tasks/create/', SubTaskMasterAPI.as_view()),
    path('sub-tasks/update/<int:pk>/', SubTaskMasterAPI.as_view()),
    path('sub-tasks/delete/<int:pk>/', SubTaskMasterAPI.as_view()),
    
    # Assignment Routing
    path('assignments/list/', TaskAssigneeAPI.as_view()), # Added /list/
    path('assignments/create/', TaskAssigneeAPI.as_view()),
    path('assignments/update/<int:pk>/', TaskAssigneeAPI.as_view()),
    path('assignments/delete/<int:pk>/', TaskAssigneeAPI.as_view()),
]