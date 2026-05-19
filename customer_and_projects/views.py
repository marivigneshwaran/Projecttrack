from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CustomerMaster, ProjectMaster, PhaseMaster
from .serializers import CustomerMasterSerializer, ProjectMasterSerializer, PhaseMasterSerializer

# ==========================================
# CUSTOMER MASTER API VIEW
# ==========================================
class CustomerMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            customer = get_object_or_404(CustomerMaster, pk=pk)
            serializer = CustomerMasterSerializer(customer)
            return Response(serializer.data)
        customers = CustomerMaster.objects.all()
        serializer = CustomerMasterSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        customer = get_object_or_404(CustomerMaster, pk=pk)
        serializer = CustomerMasterSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = get_object_or_404(CustomerMaster, pk=pk)
        customer.delete()
        return Response({"message": "Customer record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==========================================
# PROJECT MASTER API VIEW
# ==========================================
class ProjectMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            project = get_object_or_404(ProjectMaster, pk=pk)
            serializer = ProjectMasterSerializer(project)
            return Response(serializer.data)
        projects = ProjectMaster.objects.all()
        serializer = ProjectMasterSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        project = get_object_or_404(ProjectMaster, pk=pk)
        serializer = ProjectMasterSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = get_object_or_404(ProjectMaster, pk=pk)
        project.delete()
        return Response({"message": "Project record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==========================================
# PHASE MASTER API VIEW
# ==========================================
class PhaseMasterAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            phase = get_object_or_404(PhaseMaster, pk=pk)
            serializer = PhaseMasterSerializer(phase)
            return Response(serializer.data)
        phases = PhaseMaster.objects.all()
        serializer = PhaseMasterSerializer(phases, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PhaseMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        phase = get_object_or_404(PhaseMaster, pk=pk)
        serializer = PhaseMasterSerializer(phase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        phase = get_object_or_404(PhaseMaster, pk=pk)
        phase.delete()
        return Response({"message": "Phase record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)