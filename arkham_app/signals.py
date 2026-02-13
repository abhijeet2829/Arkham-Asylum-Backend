from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import InmateProfile, MedicalFile, AuditLog
from .middleware import get_current_user
import datetime

@receiver(post_save, sender=InmateProfile)
@receiver(post_save, sender=MedicalFile)
def log_save(sender, instance, created, **kwargs):
    user = get_current_user()
    actor_name = user.username if user else "System/Unknown"
    
    action_type = "CREATE" if created else "UPDATE"
    target_model = sender.__name__
    
    AuditLog.objects.create(
        actor_name=actor_name,
        action_type=action_type,
        target_model=target_model,
        target_id=instance.id,
        timestamp=datetime.datetime.now()
    )

@receiver(post_delete, sender=InmateProfile)
@receiver(post_delete, sender=MedicalFile)
def log_delete(sender, instance, **kwargs):
    user = get_current_user()
    actor_name = user.username if user else "System/Unknown"
    
    AuditLog.objects.create(
        actor_name=actor_name,
        action_type="DELETE",
        target_model=sender.__name__,
        target_id=instance.id,
        timestamp=datetime.datetime.now()
    )