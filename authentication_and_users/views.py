from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import * 
from .serializers import *

# --- ROLE API ---
class RoleAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            role = get_object_or_404(Role, pk=pk)
            serializer = RoleSerializer(role)
            return Response(serializer.data)
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        return Response({"message": "Role deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# ///////////////UserMaster
class UserMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(UserMaster, pk=pk)
            serializer = UserMasterSerializer(user)
            return Response(serializer.data)
        users = UserMaster.objects.all()
        serializer = UserMasterSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = get_object_or_404(UserMaster, pk=pk)
        serializer = UserMasterSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(UserMaster, pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class UserSkillAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            skill = get_object_or_404(UserSkill, pk=pk)
            serializer = UserSkillSerializer(skill)
            return Response(serializer.data)
        skills = UserSkill.objects.all()
        serializer = UserSkillSerializer(skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        skill = get_object_or_404(UserSkill, pk=pk)
        serializer = UserSkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        skill = get_object_or_404(UserSkill, pk=pk)
        skill.delete()
        return Response({"message": "Skill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# --- USER MEDIA API ---
class UserMediaAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            media = get_object_or_404(UserMedia, pk=pk)
            serializer = UserMediaSerializer(media)
            return Response(serializer.data)
        media_list = UserMedia.objects.all()
        serializer = UserMediaSerializer(media_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Note: When uploading files, you must use request.FILES along with request.data
        serializer = UserMediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        media = get_object_or_404(UserMedia, pk=pk)
        serializer = UserMediaSerializer(media, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        media = get_object_or_404(UserMedia, pk=pk)
        media.delete()
        return Response({"message": "Media deleted successfully"}, status=status.HTTP_204_NO_CONTENT)