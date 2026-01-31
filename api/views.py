from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee
from django.http import Http404
from rest_framework import generics, mixins, viewsets

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

# function based views

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
    
# ------------------------------------------------------------
# 1. Class-Based Views using DRF's APIView
# ------------------------------------------------------------
# These views inherit directly from APIView, giving you full control
# over HTTP methods (GET, POST, PUT, DELETE) logic.
# This approach is more verbose, but it's great for understanding the basics.
# ------------------------------------------------------------

'''
class Employees(APIView):
    # Handles GET request to list all employees
    def get(self, request):
        # Retrieve all Employee objects from database
        employees = Employee.objects.all()
        # Serialize the queryset to Python data types (JSON-ready)
        serializer = EmployeeSerializer(employees, many=True)
        # Return serialized data with HTTP 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Handles POST request to create a new employee
    def post(self, request):
        # Deserialize and validate incoming data
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            # Save new employee record to database
            serializer.save()
            # Return created employee data with HTTP 201 Created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return validation errors if invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    # Utility method to fetch a single Employee instance by primary key (pk)
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            # Raise HTTP 404 if not found
            raise Http404
        
    # Handles GET request to retrieve one employee by ID
    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Handles PUT request to update an existing employee
    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Handles DELETE request to remove an employee
    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

# ------------------------------------------------------------
# 2. Class-Based Views using Mixins + GenericAPIView
# ------------------------------------------------------------
# DRF provides mixins (ListModelMixin, CreateModelMixin, etc.) that
# implement common CRUD behavior. We just need to call their helper methods.
# This reduces code duplication.
# ------------------------------------------------------------

'''
class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # Use mixin-provided methods to handle requests
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)

class EmployeeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)
'''

# ------------------------------------------------------------
# 3. Generic Class-Based Views
# ------------------------------------------------------------
# These are even more concise. DRF’s generic views combine common
# mixins with GenericAPIView internally, so you just declare the view type.
# ------------------------------------------------------------

'''
class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'  # Explicitly tells DRF which field to use for lookups
'''

# ------------------------------------------------------------
# 4. ViewSets
# ------------------------------------------------------------
# ViewSets group related logic (list, create, retrieve, update, delete)
# into a single class. You don't explicitly define URLs — the DRF router
# automatically creates them for you.
# ------------------------------------------------------------

'''
class EmployeeViewset(viewsets.ViewSet):
    # List all employees
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)

    # Create a new employee
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve a specific employee by ID
    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update an existing employee
    def update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # Delete an employee
    def delete(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

class EmployeeViewset(viewsets.ModelViewSet):
    
    # Employee ViewSet using ModelViewSet
    
    # This ViewSet automatically provides implementations for:
    # - list()      - GET /employees/
    # - create()    - POST /employees/
    # - retrieve()  - GET /employees/<pk>/
    # - update()    - PUT /employees/<pk>/
    # - partial_update() - PATCH /employees/<pk>/
    # - destroy()   - DELETE /employees/<pk>/
    
    # By inheriting from ModelViewSet, we get all CRUD operations
    # with minimal code. The queryset and serializer_class attributes
    # define which data to operate on and how to serialize it.
    
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer