from api.models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class GrupoOcupacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo_Ocupacional
        fields = '__all__'
        
class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'
class EstablecimientoRPASerializer(serializers.ModelSerializer):
    class Meta:
        model = Establecimiento_RPA
        fields = '__all__'        

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'

class AcuerdoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acuerdo
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    rol = RolSerializer()
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'persona', 'rol', 'is_active', 'last_login']

class UniversidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidad
        fields = '__all__'
        
class PlazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plaza
        fields = '__all__'

class EntidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        fields = '__all__'

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'
class Sede_AdjudicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede_Adjudicacion
        fields = '__all__'

class CentroAsistencialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centro_Asistencial
        fields = '__all__'

class TipoProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_profesional
        fields = '__all__'
  
class GerenDependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerencia_dependencia
        fields = '__all__'  
    
class ProfesionalSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()

    class Meta:
        model = Profesional
        fields = '__all__'

    def validate(self, data):
        fecha_fin = data.get('fecha_fin')
        fecha_inscripcion = data.get('fecha_inscripcion')
        
        if not fecha_fin or not fecha_inscripcion:
            raise serializers.ValidationError("Los campos 'fecha_fin' y 'fecha_inscripcion' son obligatorios.")
        
        if fecha_fin <= fecha_inscripcion:
            raise serializers.ValidationError("La 'fecha_fin' debe ser posterior a la 'fecha_inscripcion'.")
        
        errors = {}
        required_fields = [
            'tipo_profesional', 'especialidad', 'estado', 'is_postgraduado',
            'centro_Asistencial', 'plaza', 'grupo_profesional', 'fecha_inscripcion',
            'fecha_fin', 'nivel', 'entidad', 'plan_trabajo', 'universidad_procedencia',
            'usuario_modificacion'
        ]  
        for field in required_fields:
            if not data.get(field):
                errors[field] = 'Este campo es obligatorio.'

        if errors:
            raise serializers.ValidationError(errors)
        
        return data     
         
    def create(self, validated_data):
        persona_data = validated_data.pop('persona')
        persona = Persona.objects.create(**persona_data)
        
        fecha_fin = validated_data['fecha_fin']
        fecha_inscripcion = validated_data['fecha_inscripcion']
        duracion = (fecha_fin - fecha_inscripcion).days
        
        profesional = Profesional.objects.create(
            persona=persona,
            CMP=validated_data.get('CMP', None),
            tipo_profesional=validated_data['tipo_profesional'],
            especialidad=validated_data['especialidad'],
            estado=validated_data['estado'],
            is_postgraduado=validated_data['is_postgraduado'],
            centro_Asistencial=validated_data['centro_Asistencial'],
            plaza=validated_data['plaza'],
            grupo_profesional=validated_data['grupo_profesional'],
            fecha_inscripcion=fecha_inscripcion,
            fecha_fin=fecha_fin,
            duracion=duracion,
            sede_adjudicacion=validated_data.get('sede_adjudicacion', None),
            gerencia_dependencia=validated_data.get('gerencia_dependencia', None),
            nivel=validated_data['nivel'],
            entidad=validated_data['entidad'],
            plan_trabajo=validated_data['plan_trabajo'],
            universidad_procedencia=validated_data['universidad_procedencia'],
            usuario_modificacion=validated_data['usuario_modificacion'],
        )
        profesional.save()
        return profesional

class PlanTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan_trabajo
        fields = '__all__'
        
class CoordinadorSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Coordinador
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'
             
class FormularioCreateSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')

    class Meta:
        model = Formulario
        fields = ['id', 'fecha_inicio', 'fecha_fin', 'estado', 'curso_id']

    def validate(self, data):
        fecha_fin = data.get('fecha_fin')
        fecha_inicio = data.get('fecha_inicio')
        if not fecha_fin or not fecha_inicio:
            raise serializers.ValidationError("Los campos 'fecha_fin' y 'fecha_inicio' son obligatorios.")
        
        if fecha_fin <= fecha_inicio:
            raise serializers.ValidationError("La 'fecha_fin' debe ser posterior a la 'fecha_inicio'.")
        
        errors = {}
        required_fields = ['fecha_inicio', 'fecha_fin', 'estado', 'curso']
        
        for field in required_fields:
            if not data.get(field):
                errors[field] = 'Este campo es obligatorio.'
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return data

    def create(self, validated_data):
        curso = validated_data.pop('curso')
        formulario = Formulario.objects.create(curso=curso, **validated_data)
        return formulario
    
class PostulacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postulacion
        fields = '__all__'   
        
class FormularioSerializer(serializers.ModelSerializer):
    postulacion = PostulacionSerializer(many=True)
    curso = CursoSerializer()
    class Meta:
        model = Formulario
        fields = ['id', 'fecha_inicio', 'fecha_fin', 'estado', 'curso', 'postulacion']
        
class GrupoProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo_profesional
        fields = '__all__'

class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'

class SignupSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'password', 'persona', 'rol']

    def create(self, validated_data):
        persona_data = validated_data.pop('persona')
        persona = Persona.objects.create(**persona_data)
        usuario = Usuario.objects.create(
            email=validated_data['email'],
            persona=persona,
            rol=validated_data['rol'],
            password=make_password(validated_data['password']),

        )
        usuario.save()
        return usuario
    
class LoginSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'persona', 'rol']