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
    direccion = models.CharField(max_length=200, null=True)
    numero_documento = models.CharField(max_length=20, unique=True)
    tipo_documento = models.ForeignKey('TipoDocumento', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' ' + self.apellido

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        if self.direccion:
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
    is_active = models.BooleanField(default=True)
 
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

class Facultad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Facultad, self).save(*args, **kwargs)
        
class Carrera(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    facultad = models.ForeignKey('Facultad', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    
class Asignatura(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Asignatura, self).save(*args, **kwargs)

    
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

class CategoriaProfesional(models.Model):
    """
    Represents categories like Postgrado, Pregrado, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    is_postgrado = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre

    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(CategoriaProfesional, self).save(*args, **kwargs)


class GrupoProfesional(models.Model):
    """
    Represents subcategories such as 'Residentado Médico', 'Segunda Especialidad', etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    categoria_profesional = models.ForeignKey('CategoriaProfesional', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    emite_certificado = models.BooleanField(default=False)  # Certificate flag

    def __str__(self):
        return self.nombre

    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(GrupoProfesional, self).save(*args, **kwargs)
        return f'{self.nombre} {self.categoria_profesional.nombre}'


class Especialidad(models.Model):
    """
    Represents the specific specialties within each subcategory, e.g. 'Enfermería', 'Medicina', etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    grupo_profesional = models.ForeignKey('GrupoProfesional', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Especialidad, self).save(*args, **kwargs)
        return f'{self.nombre} {self.grupo_profesional.nombre}'

        
class Profesional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    persona = models.OneToOneField('Persona', on_delete=models.CASCADE)
    CMP = models.CharField(max_length=20, null=True)
    plaza = models.ForeignKey('Plaza', on_delete=models.CASCADE)
    entidad = models.ForeignKey('Entidad', on_delete=models.CASCADE)
    centro_asistencial = models.ForeignKey('Centro_Asistencial', on_delete=models.CASCADE)
    universidad_procedencia = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    
    # Relaciones con CategoriaProfesional, GrupoProfesional, y Especialidad
    categoria_profesional = models.ForeignKey('CategoriaProfesional', on_delete=models.CASCADE)  # Relación directa con CategoriaProfesional
    grupo_profesional = models.ForeignKey('GrupoProfesional', on_delete=models.CASCADE)  # Relación directa con GrupoProfesional
    especialidad = models.ForeignKey('Especialidad', on_delete=models.CASCADE)  # Relación directa con Especialidad
    is_postgrado = models.BooleanField(default=False)
    sede_adjudicacion = models.ForeignKey('Sede_Adjudicacion', on_delete=models.CASCADE, null=True, blank=True)
    plan_trabajo = models.ForeignKey('Plan_trabajo', blank=True, null=True, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField()
    fecha_fin = models.DateField()
    duracion = models.IntegerField(null=True)
    gerencia_dependencia = models.ForeignKey('Gerencia_dependencia', on_delete=models.CASCADE, null=True, blank=True)
    nivel = models.ForeignKey('Nivel', on_delete=models.CASCADE)
    usuario_modificacion = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.persona.nombre} {self.persona.apellido}'

class Campo_clinico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Campo_clinico, self).save(*args, **kwargs)

class Profesional_pregrado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    persona = models.OneToOneField('Persona', on_delete=models.CASCADE)
    
    # Relaciones con Universidad, Facultad, Carrera, y Asignatura
    universidad = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    facultad = models.ForeignKey('Facultad', on_delete=models.CASCADE)
    carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
    asignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE)
    ciclo = models.CharField(max_length=100)
    fecha_inscripcion = models.DateField()
    fecha_fin = models.DateField()
    plan_trabajo = models.ForeignKey('Plan_trabajo', on_delete=models.CASCADE)
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    campo_clinico = models.ForeignKey('Campo_clinico', on_delete=models.CASCADE)
    induccion = models.BooleanField(default=False)
    duracion = models.IntegerField(null=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.persona.nombre + ' ' + self.persona.apellido + ' ' + self.fecha_inicio.strftime('%d/%m/%Y') + ' ' + self.fecha_fin.strftime('%d/%m/%Y')
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Profesional_pregrado, self).save(*args, **kwargs)
    
class Gerencia_dependencia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Gerencia_dependencia, self).save(*args, **kwargs)

class Nivel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Nivel, self).save(*args, **kwargs)

class Plan_trabajo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey('Universidad', on_delete=models.CASCADE)
    is_postgrado = models.BooleanField(default=False)
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
    link = models.URLField(null=True)
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
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    profesion = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    regimen_laboral = models.CharField(max_length=100)
    establecimiento_RPA = models.ForeignKey('Establecimiento_RPA', on_delete=models.CASCADE)
    grupo_ocupacional = models.ForeignKey('Grupo_Ocupacional', on_delete=models.CASCADE)
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    codigo_planilla = models.CharField(max_length=100)
    area = models.CharField(max_length=100, null=True)
    fecha_postulacion = models.DateField(auto_now=True)
    asistencia = models.FloatField(null=True)
    notas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Ejemplo de campo para nota
    observaciones = models.TextField(null=True, blank=True)
    is_rejected = models.BooleanField(default=False)
    link = models.URLField(null=True)
    certificado_estado = models.BooleanField(default=False)
    estado = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre + ' ' + self.apellido + ' ' + ' ' + self.fecha_postulacion.strftime('%d/%m/%Y')
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        self.profesion = self.profesion.upper()
        self.area = self.area.upper()
        super(Postulacion, self).save(*args, **kwargs)         

class Establecimiento_RPA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Establecimiento_RPA, self).save(*args, **kwargs)

class Grupo_Ocupacional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Grupo_Ocupacional, self).save(*args, **kwargs)

class Cargo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    def save(self , *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Cargo, self).save(*args, **kwargs)

class Formulario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curso = models.OneToOneField('Curso', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    postulacion = models.ManyToManyField(Postulacion, related_name='formularios', blank=True)
    fecha_modificacion = models.DateField(auto_now=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.fecha_creacion.strftime('%d/%m/%Y') + ' ' + self.fecha_modificacion.strftime('%d/%m/%Y')