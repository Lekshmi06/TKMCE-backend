from django.db import models

class Department(models.Model):
    # dept_id is automatically created as the primary key
    department_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=10, null=True, blank=True)  # New field for department code
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'departments'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.department_code} - {self.department_name}"
    

class Designation(models.Model):
    # designation_id = models.AutoField(primary_key=True)  # Use AutoField for primary key
    designation_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'designations'
        verbose_name_plural = 'Designations'
    def __str__(self):
        return self.designation_name



class Employee(models.Model):
    TYPE_CHOICES = [
        (0, 'Permanent Teaching'),
        (1, 'Guest Teaching'),
        (2, 'Permanent Non-Teaching'),
        (3, 'Temporary Non-Teaching'),
    ]
    
    pen = models.CharField(max_length=20)
    pan = models.CharField(max_length=10)
    password = models.CharField(max_length=10, default='', editable=False)
    name = models.CharField(max_length=255)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    mob_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address = models.TextField(null=True, blank=True)
    type = models.IntegerField(choices=TYPE_CHOICES)
    date_of_joining = models.DateField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.password:
            self.password = self.pan  # Default password is set to PAN
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Employees'
        verbose_name_plural = 'employees'

    def __str__(self):
        return self.name


class Qualification(models.Model):
    name = models.CharField(max_length=100)  # E.g., "Bachelor's Degree", "Master's Degree"
    rank = models.IntegerField()  # Rank field to define the qualification level, with higher numbers representing higher qualifications

    class Meta:
        db_table = 'qualifications'

    def __str__(self):
        return self.name


class EmployeeQualification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    stream = models.CharField(max_length=100, null=True, blank=True)  # Allows blank values

    class Meta:
        db_table = 'EmployeeQualifications'

    # date_obtained = models.DateField(null=True, blank=True)  # Optional date

    class Meta:
        db_table = 'employee_qualifications'
        unique_together = ('employee', 'qualification', 'stream')  # Ensures unique entries for employee-qualification-stream