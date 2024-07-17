import datetime
from django.contrib.auth.models import BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password, persona=None, rol=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not persona:
            raise ValueError('Persona field is required')

        user = self.model(
            username=email,
            persona=persona,
            rol=rol,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, persona=None, rol=None, **extra_fields):
        extra_fields.setdefault('fecha_creacion', datetime.now())

        return self.create_user(email, password, persona, rol, **extra_fields)
