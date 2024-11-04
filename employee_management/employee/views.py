from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from rest_framework_simplejwt.tokens import RefreshToken


class EmployeePagination(PageNumberPagination):
    """
    Pagination class
    """
    page_size = 10

class EmployeeListCreateView(APIView):
    """
    List and Create Employees
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        department = request.query_params.get('department')
        role = request.query_params.get('role')
        
        employees = Employee.objects.all()
        if department:
            employees = employees.filter(department=department)
        if role:
            employees = employees.filter(role=role)
        
        paginator = Paginator(employees, EmployeePagination.page_size)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serializer = EmployeeSerializer(page_obj, many=True)
        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page_number,
            'results': serializer.data
        })

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeRetrieveUpdateDeleteView(APIView):
    """
    Retrieve, Update, and Delete Employee by ID
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return None

    def get(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
