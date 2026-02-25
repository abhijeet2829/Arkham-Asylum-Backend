from django.db import models
from django.contrib.auth.models import User

class CellBlock(models.Model):
    name = models.CharField(max_length=20, unique=True)
    max_capacity = models.PositiveIntegerField(default=10)

    @property
    def current_count(self):
        return self.inmates.filter(status='ACTIVE').count()

    def __str__(self):
        return self.name


class InmateProfile(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('DISCHARGED', 'Discharged'),
        ('TRANSFERRED', 'Transferred'),
        ('ESCAPED', 'Escaped'),
        ('DECEASED', 'Deceased'),
    ]

    name = models.CharField(max_length=100, unique=True)
    alias = models.CharField(max_length=50, unique=True)
    cell_block = models.ForeignKey(CellBlock, on_delete=models.PROTECT, related_name='inmates')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    def __str__(self):
        return self.name
    
    
class MedicalFile(models.Model):
    inmate = models.OneToOneField(InmateProfile, on_delete=models.CASCADE)
    referral_diagnosis = models.CharField(max_length=200)
    internal_diagnosis = models.CharField(max_length=200, blank=True, default='Pending evaluation')
    meds = models.CharField(max_length=150)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_files')
    
    def __str__(self):
        return f"{self.inmate.name}"
    
    
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('DETAILED_READ', 'Detailed Read'),
        ('UPDATE', 'Update'),
        ('CREATE', 'Create'),
        ('DELETE', 'Delete'),
    ]

    actor_name = models.CharField(max_length=100)
    actor_group = models.CharField(max_length=50, default='Unknown')
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_model = models.CharField(max_length=50)  # InmateProfile/MedicalFile
    target_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta: # sort by most recent logs
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.action_type} by {self.actor_name} on {self.target_model}#{self.target_id}"