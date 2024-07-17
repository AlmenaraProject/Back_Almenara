import uuid
from django.db import models
from .managers import UsuarioManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class Persona(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    numero_documento = models.CharField(max_length=20)
    tipo_documento = models.ForeignKey('TipoDocumento', on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
class TipoDocumento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    persona = models.OneToOneField('Persona', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    rol = models.ForeignKey('Rol', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
 
    USERNAME_FIELD = 'email'
    
    objects = UsuarioManager()

class Rol(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    
class Universidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    coordinador_general = models.ForeignKey('Persona', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    