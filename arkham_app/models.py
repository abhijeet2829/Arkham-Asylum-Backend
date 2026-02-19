from django.db import models

class InmateProfile(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('DISCHARGED', 'Discharged'),
        ('TRANSFERRED', 'Transferred'),
        ('ESCAPED', 'Escaped'),
        ('DECEASED', 'Deceased'),
    ]

    CELL_BLOCK_CHOICES = [
        ('Block-A', 'Block A'),
        ('Block-B', 'Block B'),
        ('Block-C', 'Block C'),
        ('Block-D', 'Block D'),
        ('Block-E', 'Block E'),
    ]

    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=50)
    cell_block = models.CharField(max_length=20, choices=CELL_BLOCK_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    def __str__(self):
        return self.name
    
    
class MedicalFile(models.Model):
    inmate = models.OneToOneField(InmateProfile, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=100)
    meds = models.CharField(max_length=150)
    
    def __str__(self):
        return f"Medical Record for {self.inmate.name}"
    
    
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('DETAILED_READ', 'Detailed Read'),
        ('UPDATE', 'Update'),
        ('CREATE', 'Create'),
        ('DELETE', 'Delete'),
    ]

    actor_name = models.CharField(max_length=100)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_model = models.CharField(max_length=50)  # InmateProfile/MedicalFile
    target_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta: # sort by most recent logs
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.action_type} by {self.actor_name} on {self.target_model}#{self.target_id}"