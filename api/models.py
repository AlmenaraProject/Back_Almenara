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
 
class Coordinador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=250, null=True)
    estado = models.BooleanField(default=True)
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
    
class Profesor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=250, null=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
class Especialidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    coordinador = models.ForeignKey('Coordinador',on_delete=models.CASCADE, null=True)
    universidad = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    
class Universidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    coordinador = models.ForeignKey('Coordinador',on_delete=models.CASCADE, null=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    
class Sede_Adjudicacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre   

class Plaza(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    
class Entidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Centro_Asistencial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)

class Tipo_profesional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Plan_trabajo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.BooleanField(default=True)

class Profesional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    persona = models.OneToOneField('Persona', on_delete=models.CASCADE)
    CMP = models.CharField(max_length=20)
    especialidad = models.ForeignKey('Especialidad', on_delete=models.CASCADE)
    plaza = models.OneToOneField('Plaza', on_delete=models.CASCADE)
    entidad = models.ForeignKey('Entidad', on_delete=models.CASCADE)
    centro_Asistencial = models.ForeignKey('Centro_Asistencial', on_delete=models.CASCADE)
    universidad_procedencia = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    tipo_profesional = models.ForeignKey('Tipo_profesional', on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField()
    fecha_modificacion = models.DateField()
    usuario_modificacion = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

class Curso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    postulacion = models.ManyToManyField('Postulacion', blank=True)
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE, null=True)
    modalidad = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.BooleanField(default=True)

class Postulacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profesional = models.ForeignKey('Profesional', on_delete=models.CASCADE)
    plan_trabajo = models.ForeignKey('Plan_trabajo', on_delete=models.CASCADE)
    fecha_postulacion = models.DateField()
    estado = models.BooleanField(default=True)
