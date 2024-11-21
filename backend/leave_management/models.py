from django.db import models



class LeaveMaster(models.Model):
    leave_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    leave_code = models.CharField(max_length=10)
    leave_description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)  # Defaults to 0 (False)

    class Meta:
        db_table = 'leave_master'
        verbose_name_plural = 'Leave Masters'

    def str(self):
        return self.leave_description


class LeaveDetails(models.Model):
    leave_details_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    leave = models.ForeignKey(LeaveMaster, on_delete=models.CASCADE, related_name='leave_details')
    employee_id = models.ForeignKey('employee.employee', on_delete=models.CASCADE, related_name='leave_details')  # Referencing employee model from employee app
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'leave_details'
        verbose_name_plural = 'Leave Details'

    def str(self):
        return f"Leave {self.leave.leave_code} for {self.emp_id.name} from {self.start_date} to {self.end_date}"


#leave_management app