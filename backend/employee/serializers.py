#——————serializer—————-
from rest_framework import serializers
from .models import Designation,Department,Employee,Qualification,EmployeeQualification

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'designation_name']  
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']  
class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields= "__all__"

class EmployeefilterSerializers(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    designation_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'type', 'department_name', 'designation_name']  # Include any other fields you need

    def get_department_name(self, obj):
        return obj.department.department_name if obj.department else None  # Access the related department name

    def get_designation_name(self, obj):
        return obj.designation.designation_name if obj.designation else None        

class EmployeeQualificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeQualification
        fields='__all__'        
class QualificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields='__all__'