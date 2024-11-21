from django.db import models,transaction
from employee.models import Employee
from django.utils import timezone

class Committe(models.Model):
    order_number = models.CharField(max_length=150)
    committe_Name = models.CharField(max_length=255, null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)
    order_Text = models.CharField(max_length=500, null=True, blank=True)
    order_Description = models.TextField(null=True, blank=True)
    committe_Expiry = models.IntegerField(default=1)  # Expiry period in years
    is_active = models.BooleanField(default=True)  # Track active/inactive status

    class Meta:
        db_table = 'committe'
        verbose_name_plural = 'Committees'

    def check_expiration(self):
        """Check if the committee has expired based on expiry period."""
        if self.order_date:
            expiration_date = self.order_date + timezone.timedelta(days=self.committe_Expiry * 365)
            if timezone.now().date() > expiration_date:
                self.is_active = False
                self.save()
                
                # Set all related CommitteeDetails entries as past members
                with transaction.atomic():
                    CommitteeDetails.objects.filter(committee_id=self.id).update(is_past_member=True)
    
    def __str__(self):
        return self.committe_Name if self.committe_Name else "Unnamed Committee"


class SubCommittee(models.Model):
    committee_id = models.ForeignKey('Committe', on_delete=models.CASCADE, related_name='sub_committees')
    sub_committee_name = models.CharField(max_length=255)
    sub_committee_Text = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'sub_committee'
        verbose_name_plural = 'Sub Committees'


class CommitteeDetails(models.Model):
    committee_id = models.ForeignKey('Committe', on_delete=models.CASCADE, null=True, blank=True)
    subcommittee_id = models.ForeignKey('SubCommittee', on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='committees_employee')
    role = models.CharField(max_length=250)
    score = models.IntegerField()
    is_past_member = models.BooleanField(default=False)  

    class Meta:
        db_table = 'committee_details'
        verbose_name_plural = 'Committee Details'


