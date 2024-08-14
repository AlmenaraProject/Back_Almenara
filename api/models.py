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
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        self.direccion = self.direccion.upper()
        super(Persona, self).save(*args, **kwargs)
 
class Coordinador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=250, null=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre + ' ' + self.apellido
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        super(Coordinador, self).save(*args, **kwargs) 

class TipoDocumento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(TipoDocumento, self).save(*args, **kwargs)

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
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.descripcion = self.descripcion.upper()
        super(Rol, self).save(*args, **kwargs)
    
class Profesor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=250, null=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre + ' ' + self.apellido
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        super(Profesor, self).save(*args, **kwargs)
    
class Especialidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    coordinador = models.ForeignKey('Coordinador',on_delete=models.CASCADE, null=True)
    universidad = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Especialidad, self).save(*args, **kwargs)
    
class Universidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    coordinador = models.ForeignKey('Coordinador',on_delete=models.CASCADE, null=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.siglas = self.siglas.upper()
        self.ciudad = self.ciudad.upper()
        super(Universidad, self).save(*args, **kwargs)
    
class Sede_Adjudicacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre   
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        self.ciudad = self.ciudad.upper()
        super(Sede_Adjudicacion, self).save(*args, **kwargs)
        
class Plaza(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Plaza, self).save(*args, **kwargs)
    
class Entidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Entidad, self).save(*args, **kwargs)

class Centro_Asistencial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        super(Centro_Asistencial, self).save(*args, **kwargs)

class Tipo_profesional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Tipo_profesional, self).save(*args, **kwargs)

class Profesional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    persona = models.OneToOneField('Persona', on_delete=models.CASCADE)
    CMP = models.CharField(max_length=20)
    especialidad = models.ForeignKey('Especialidad', on_delete=models.CASCADE)
    plaza = models.ForeignKey('Plaza', on_delete=models.CASCADE)
    entidad = models.ForeignKey('Entidad', on_delete=models.CASCADE)
    centro_Asistencial = models.ForeignKey('Centro_Asistencial', on_delete=models.CASCADE)
    universidad_procedencia = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    tipo_profesional = models.ForeignKey('Tipo_profesional', on_delete=models.CASCADE)
    plan_trabajo = models.ForeignKey('Plan_trabajo', blank=True, null=True, related_name='profesionales', on_delete=models.CASCADE)  # Cambiado a ForeignKey
    fecha_inscripcion = models.DateField(auto_now_add=True)
    fecha_modificacion = models.DateField(auto_now=True)
    usuario_modificacion = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    is_postgraduado = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.persona.nombre + ' ' + self.persona.apellido

class Plan_trabajo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    acuerdo = models.ManyToManyField('Acuerdo', blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre + ' ' + self.universidad.nombre + ' ' + self.fecha_inicio.strftime('%d/%m/%Y') + ' ' + self.fecha_fin.strftime('%d/%m/%Y')
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Plan_trabajo, self).save(*args, **kwargs)
    
class Acuerdo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compromiso = models.CharField(max_length=200)
    detalle = models.CharField(max_length=200)
    sede_Adjudicacion = models.ForeignKey('Sede_Adjudicacion', on_delete=models.CASCADE)
    beneficiarios = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    valorizacion = models.FloatField()
    is_esssalud_responsable = models.BooleanField()
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.compromiso + ' ' + self.detalle + ' ' + self.sede_Adjudicacion.nombre + ' ' + self.fecha_inicio.strftime('%d/%m/%Y') + ' ' + self.fecha_fin.strftime('%d/%m/%Y')
    def save(self , *args, **kwargs):
        self.compromiso = self.compromiso.upper()
        self.detalle = self.detalle.upper()
        super(Acuerdo, self).save(*args, **kwargs)

class Curso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    postulacion = models.ManyToManyField('Postulacion', blank=True)
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE, null=True)
    modalidad = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre + ' ' + self.fecha_inicio.strftime('%d/%m/%Y') + ' ' + self.fecha_fin.strftime('%d/%m/%Y')
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.modalidad = self.modalidad.upper()
        super(Curso, self).save(*args, **kwargs)

class Postulacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profesional = models.ForeignKey('Profesional', on_delete=models.CASCADE)
    plan_trabajo = models.ForeignKey('Plan_trabajo', on_delete=models.CASCADE)
    fecha_postulacion = models.DateField()
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.profesional.persona.nombre + ' ' + self.profesional.persona.apellido + ' ' + self.plan_trabajo.nombre + ' ' + self.fecha_postulacion.strftime('%d/%m/%Y')