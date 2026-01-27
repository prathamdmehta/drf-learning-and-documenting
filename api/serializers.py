from rest_framework import serializers
from students.models import Student
from employees.models import Employee


class StudentSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for Student model - automatically generates serializer fields
    from Django model fields. Handles both serialization (model → JSON) and
    deserialization (JSON → model instance).
    
    Key Features:
    - Automatic field generation from Student model
    - Built-in validation using model field constraints
    - Supports create/update operations automatically
    - Handles querysets (many=True) and single instances
    """
    
    class Meta:
        """
        ModelSerializer configuration - tells DRF which model and fields to use
        
        ATTRIBUTES:
        - model: Links serializer to Student Django model
        - fields = "__all__": Includes ALL fields from Student model automatically
                         (name, email, age, etc. - whatever your model has)
                         
        Alternative options (for future reference):
        - fields = ['name', 'email']  # Specific fields only
        - fields = '__all__'          # All model fields (current)
        - exclude = ['created_at']    # All except these fields
        - read_only_fields = ['id']   # Fields that can't be updated
        """
        model = Student
        fields = "__all__"

# Serializer for Employee Model
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"