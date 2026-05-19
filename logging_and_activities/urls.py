from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Time Tracking Logs
    path('logs/list/', LogMasterAPI.as_view()),
    path('logs/create/', LogMasterAPI.as_view()),
    path('logs/update/<int:pk>/', LogMasterAPI.as_view()),
    path('logs/delete/<int:pk>/', LogMasterAPI.as_view()),
    
    # Audit Trail / Activity Logs
    path('activities/list/', ActivityLogAPI.as_view()),
    path('activities/create/', ActivityLogAPI.as_view()),
    path('activities/update/<int:pk>/', ActivityLogAPI.as_view()),
    path('activities/delete/<int:pk>/', ActivityLogAPI.as_view()),
]