from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    # Auth Tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('customers/list/', CustomerMasterAPI.as_view()),
    path('customers/create/', CustomerMasterAPI.as_view()),
    path('customers/update/<int:pk>/', CustomerMasterAPI.as_view()),
    path('customers/delete/<int:pk>/', CustomerMasterAPI.as_view()),
    
    # Project Routes
    path('projects/list/', ProjectMasterAPI.as_view()),
    path('projects/create/', ProjectMasterAPI.as_view()),
    path('projects/update/<int:pk>/', ProjectMasterAPI.as_view()),
    path('projects/delete/<int:pk>/', ProjectMasterAPI.as_view()),

    # Phase Routes
    path('phases/list/', PhaseMasterAPI.as_view()),
    path('phases/create/', PhaseMasterAPI.as_view()),
    path('phases/update/<int:pk>/', PhaseMasterAPI.as_view()),
    path('phases/delete/<int:pk>/', PhaseMasterAPI.as_view()),
]