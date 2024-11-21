from django.contrib import admin
from .models import Department, Designation, Employee, EmployeeQualification, Qualification
# Register your models here.


admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(EmployeeQualification)
admin.site.register(Qualification)