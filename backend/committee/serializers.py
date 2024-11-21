from rest_framework import serializers
from .models import Committe, CommitteeDetails, SubCommittee
from employee.models import Employee, Department

class CommitteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committe
        fields = ['id', 'order_number', 'committe_Name', 'order_date', 'order_Text', 'order_Description', 'committe_Expiry']

class SubCommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCommittee
        fields = ['id','committee_id', 'sub_committee_name', 'sub_committee_Text']

class CommitteeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeDetails
        fields = ['committee_id', 'subcommittee_id', 'employee_id', 'role', 'score', 'is_past_member']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department  # Assuming you have a Department model
        fields = ['id', 'department_name'] 

class EmployeeSerializerForFetch(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name')  # Correctly access department_name

    class Meta:
        model = Employee
        fields = ['id', 'name', 'department_name']   # Include fields for name and department

class CommitteeDetailsSerializerForFetch(serializers.ModelSerializer):
    employee = EmployeeSerializerForFetch(source='employee_id')  # Use source to link to the employee model

    class Meta:
        model = CommitteeDetails
        fields = ['id','committee_id', 'subcommittee_id', 'employee', 'role', 'score', 'is_past_member']

class SubCommitteeSerializerForFetch(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = SubCommittee
        fields = ['id', 'sub_committee_name', 'sub_committee_Text', 'members']

        def get_members(self, obj):
            members = CommitteeDetails.objects.filter(subcommittee_id=obj.id)
            return CommitteeDetailsSerializerForFetch(members, many=True).data

    def get_members(self, obj):
        members = CommitteeDetails.objects.filter(subcommittee_id=obj.id)
        return CommitteeDetailsSerializerForFetch(members, many=True).data


class  CommitteSerializerForFetch(serializers.ModelSerializer):
    sub_committees = serializers.SerializerMethodField()
    main_committee_members = serializers.SerializerMethodField()  # New field for main committee members

    class Meta:
        model = Committe
        fields = ['id','order_number', 'committe_Name', 'order_date', 'order_Text', 'order_Description', 'committe_Expiry', 'sub_committees', 'main_committee_members']

    def get_sub_committees(self, obj):
        sub_committees = SubCommittee.objects.filter(committee_id=obj.id)
        return SubCommitteeSerializerForFetch(sub_committees, many=True).data

    def get_main_committee_members(self, obj):
        members = CommitteeDetails.objects.filter(committee_id=obj.id, subcommittee_id=None)  # Fetch main committee members
        return CommitteeDetailsSerializerForFetch(members, many=True).data