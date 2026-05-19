from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RoleAPI, UserMasterAPI, UserSkillAPI, UserMediaAPI

urlpatterns = [
    # Auth Tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # ////////////Roles/////////////////
    path('roles/list/', RoleAPI.as_view()),
    path('roles/create/', RoleAPI.as_view()),
    path('roles/update/<int:pk>/', RoleAPI.as_view()),
    path('roles/delete/<int:pk>/', RoleAPI.as_view()),

    # ////////////Users/////////////////
    path('users/list/', UserMasterAPI.as_view()),
    path('users/create/', UserMasterAPI.as_view()),
    path('users/update/<int:pk>/', UserMasterAPI.as_view()),
    path('users/delete/<int:pk>/', UserMasterAPI.as_view()),

    # ////////////UserSkills/////////////////
    path('userskills/list/', UserSkillAPI.as_view()),
    path('userskills/create/', UserSkillAPI.as_view()),
    path('userskills/update/<int:pk>/', UserSkillAPI.as_view()),
    path('userskills/delete/<int:pk>/', UserSkillAPI.as_view()),

    # ////////////UserMedia/////////////////
    path('usermedia/list/', UserMediaAPI.as_view()),
    path('usermedia/create/', UserMediaAPI.as_view()),
    path('usermedia/update/<int:pk>/', UserMediaAPI.as_view()),
    path('usermedia/delete/<int:pk>/', UserMediaAPI.as_view()),
]