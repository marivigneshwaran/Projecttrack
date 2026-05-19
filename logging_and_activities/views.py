from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import LogMaster, ActivityLog
from .serializers import LogMasterSerializer, ActivityLogSerializer

# ==========================================
# LOG MASTER API VIEW
# ==========================================
class LogMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            log = get_object_or_404(LogMaster, pk=pk)
            serializer = LogMasterSerializer(log)
            return Response(serializer.data)
        logs = LogMaster.objects.all()
        serializer = LogMasterSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LogMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        log = get_object_or_404(LogMaster, pk=pk)
        serializer = LogMasterSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        log = get_object_or_404(LogMaster, pk=pk)
        log.delete()
        return Response({"message": "Time log successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


# ==========================================
# ACTIVITY LOG API VIEW
# ==========================================
class ActivityLogAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            activity = get_object_or_404(ActivityLog, pk=pk)
            serializer = ActivityLogSerializer(activity)
            return Response(serializer.data)
        # Ordering by '-timestamp' keeps the newest activities at the top of the timeline
        activities = ActivityLog.objects.all().order_by('-timestamp')
        serializer = ActivityLogSerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActivityLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        activity = get_object_or_404(ActivityLog, pk=pk)
        serializer = ActivityLogSerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        activity = get_object_or_404(ActivityLog, pk=pk)
        activity.delete()
        return Response({"message": "Activity history log removed"}, status=status.HTTP_204_NO_CONTENT)