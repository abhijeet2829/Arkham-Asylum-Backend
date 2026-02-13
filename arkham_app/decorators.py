from functools import wraps
from .models import AuditLog
from .middleware import get_current_user
import datetime

def audit_read(model_class):
    def decorator(func):
        @wraps(func)
        def wrapper(view_instance, request, *args, **kwargs):
            response = func(view_instance, request, *args, **kwargs)
            if response.status_code == 200:
                try:
                    obj = response.data
                    target_id = obj.get('id') if isinstance(obj, dict) else getattr(obj, 'id', None)
                    if target_id:
                        user = get_current_user()
                        actor_name = user.username if user else "Anonymous"

                        AuditLog.objects.create(
                            actor_name=actor_name,
                            action_type="READ",
                            target_model=model_class.__name__,
                            target_id=target_id,
                            timestamp=datetime.datetime.now()
                        )
                except Exception as e:
                    print(f"Audit Log Error: {e}")
            
            return response
        return wrapper
    return decorator