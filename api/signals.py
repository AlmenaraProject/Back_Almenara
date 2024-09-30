from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Profesional, Persona

@receiver(post_delete, sender=Profesional)
def delete_persona_on_profesional_delete(sender, instance, **kwargs):
    if instance.persona:
        instance.persona.delete()