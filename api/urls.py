from django.urls import path
from . import views


urlpatterns = [
    # Student URLs
    path('students/', views.studentsView),
    path('students/<int:pk>/', views.studentDetailView),
    
    # Employee URLs
    path('employees/', views.Employees.as_view()),  # Class-based view for Employee list/create
    path('employees/<int:pk>/', views.EmployeeDetail.as_view()),
] 