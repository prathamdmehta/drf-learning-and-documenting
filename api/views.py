from django.shortcuts import render
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee
from django.http import Http404

"""
Complete CRUD API for Student model using Django REST Framework Function-Based Views (FBVs)

Supports:
- GET /api/students/          - List all students
- POST /api/students/         - Create new student  
- GET /api/students/<pk>/     - Retrieve single student
- PUT /api/students/<pk>/     - Update student (full update)
- DELETE /api/students/<pk>/  - Delete student
"""


@api_view(['GET', 'POST'])
def studentsView(request):
    """
    LIST & CREATE Student API View
    
    GET: Returns all students from database as JSON
    POST: Creates new student from request data
    
    URL Patterns:
    - GET /api/students/ 
    - POST /api/students/
    """
    if request.method == 'GET':
        # Fetch all students from Student model
        students = Student.objects.all()
        # Serialize queryset (many=True for multiple objects)
        serializer = StudentSerializer(students, many=True)
        # Return 200 OK with serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Deserialize incoming JSON data into StudentSerializer
        serializer = StudentSerializer(data=request.data)
        # Validate data against model fields
        if serializer.is_valid():
            # Save validated data to database
            serializer.save()
            # Return 201 Created with new student data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return 400 Bad Request with validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Fixed: .errors not .error

#function based views

@api_view(['GET', 'PUT', 'DELETE'])
def studentDetailView(request, pk):
    """
    RETRIEVE, UPDATE & DELETE Student API View
    
    GET: Returns single student by primary key
    PUT: Updates existing student (complete replacement)
    DELETE: Permanently removes student from database
    
    URL Patterns:
    - GET /api/students/<pk>/
    - PUT /api/students/<pk>/
    - DELETE /api/students/<pk>/
    """
    # Try to fetch student by primary key (pk)
    try:
        student = Student.objects.get(pk=pk)  # Renamed for singular clarity
    except Student.DoesNotExist:
        # Return 404 Not Found if student doesn't exist
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Serialize single student instance
        serializer = StudentSerializer(student)  # No many=True for single object
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        # PUT = Complete replacement of student data
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Fixed: .errors
    
    elif request.method == 'DELETE':
        # Permanently delete student from database
        student.delete()  # Fixed: was students.delete()
        # Return 204 No Content (successful deletion, no data returned)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class based views for Employee model
class Employees(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)