from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import TaskListMaster, TaskMaster, SubTaskMaster, TaskAssignee
from .serializers import (
    TaskListMasterSerializer, TaskMasterSerializer, 
    SubTaskMasterSerializer, TaskAssigneeSerializer
)

# --- TASK LIST API ---
class TaskListMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            task_list = get_object_or_404(TaskListMaster, pk=pk)
            serializer = TaskListMasterSerializer(task_list)
            return Response(serializer.data)
        task_lists = TaskListMaster.objects.all()
        serializer = TaskListMasterSerializer(task_lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskListMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task_list = get_object_or_404(TaskListMaster, pk=pk)
        serializer = TaskListMasterSerializer(task_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task_list = get_object_or_404(TaskListMaster, pk=pk)
        task_list.delete()
        return Response({"message": "Task list deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# --- TASK MASTER API ---
class TaskMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            task = get_object_or_404(TaskMaster, pk=pk)
            serializer = TaskMasterSerializer(task)
            return Response(serializer.data)
        tasks = TaskMaster.objects.all()
        serializer = TaskMasterSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = get_object_or_404(TaskMaster, pk=pk)
        serializer = TaskMasterSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(TaskMaster, pk=pk)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# --- SUB TASK API ---
class SubTaskMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            sub_task = get_object_or_404(SubTaskMaster, pk=pk)
            serializer = SubTaskMasterSerializer(sub_task)
            return Response(serializer.data)
        sub_tasks = SubTaskMaster.objects.all()
        serializer = SubTaskMasterSerializer(sub_tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        sub_task = get_object_or_404(SubTaskMaster, pk=pk)
        serializer = SubTaskMasterSerializer(sub_task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        sub_task = get_object_or_404(SubTaskMaster, pk=pk)
        sub_task.delete()
        return Response({"message": "Sub-task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# --- TASK ASSIGNEE API ---
class TaskAssigneeAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            assignee = get_object_or_404(TaskAssignee, pk=pk)
            serializer = TaskAssigneeSerializer(assignee)
            return Response(serializer.data)
        assignees = TaskAssignee.objects.all()
        serializer = TaskAssigneeSerializer(assignees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskAssigneeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        assignee = get_object_or_404(TaskAssignee, pk=pk)
        serializer = TaskAssigneeSerializer(assignee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        assignee = get_object_or_404(TaskAssignee, pk=pk)
        assignee.delete()
        return Response({"message": "Assignment record removed"}, status=status.HTTP_204_NO_CONTENT)