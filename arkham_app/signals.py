from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import InmateProfile, MedicalFile, AuditLog
from .middleware import get_current_user
from django.utils import timezone

@receiver(post_save, sender=InmateProfile)
@receiver(post_save, sender=MedicalFile)
def log_save(sender, instance, created, **kwargs):
    user = get_current_user()
    actor_name = user.username if user else "System/Unknown"
    actor_group = user.groups.first().name if user and user.groups.exists() else "Super Admin"
    
    action_type = "CREATE" if created else "UPDATE"
    target_model = sender.__name__
    
    AuditLog.objects.create(
        actor_name=actor_name,
        actor_group=actor_group,
        action_type=action_type,
        target_model=target_model,
        target_id=instance.id,
        timestamp=timezone.now()
    )

@receiver(post_delete, sender=InmateProfile)
@receiver(post_delete, sender=MedicalFile)
def log_delete(sender, instance, **kwargs):
    user = get_current_user()
    actor_name = user.username if user else "System/Unknown"
    actor_group = user.groups.first().name if user and user.groups.exists() else "Super Admin"
    
    AuditLog.objects.create(
        actor_name=actor_name,
        actor_group=actor_group,
        action_type="DELETE",
        target_model=sender.__name__,
        target_id=instance.id,
        timestamp=timezone.now()
    )