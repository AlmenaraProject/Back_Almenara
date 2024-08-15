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

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    rol = RolSerializer()

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'persona', 'rol', 'estado', 'last_login']

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
    
class ProfesionalSerializer(serializers.ModelSerializer):
    persona = serializers.PrimaryKeyRelatedField(queryset=Persona.objects.all())
    plaza = serializers.PrimaryKeyRelatedField(queryset=Plaza.objects.all())
    entidad = serializers.PrimaryKeyRelatedField(queryset=Entidad.objects.all())
    centro_asistencial = serializers.PrimaryKeyRelatedField(queryset=Centro_Asistencial.objects.all())
    universidad_procedencia = serializers.PrimaryKeyRelatedField(queryset=Universidad.objects.all())
    tipo_profesional = serializers.PrimaryKeyRelatedField(queryset=Tipo_profesional.objects.all())
    grupo_profesional = serializers.PrimaryKeyRelatedField(queryset=Grupo_profesional.objects.all())
    especialidad = serializers.PrimaryKeyRelatedField(queryset=Especialidad.objects.all())
    plan_trabajo = serializers.PrimaryKeyRelatedField(queryset=Plan_trabajo.objects.all())
    nivel = serializers.PrimaryKeyRelatedField(queryset=Nivel.objects.all())
    
    class Meta:
        model = Profesional
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['persona'] = PersonaSerializer(instance.persona).data
        representation['plaza'] = PlazaSerializer(instance.plaza).data
        representation['entidad'] = EntidadSerializer(instance.entidad).data
        representation['centro_asistencial'] = CentroAsistencialSerializer(instance.centro_asistencial).data
        representation['universidad_procedencia'] = UniversidadSerializer(instance.universidad).data
        representation['tipo_profesional'] = TipoProfesionalSerializer(instance.tipo_profesional).data
        representation['grupo_profesional'] = GrupoProfesionalSerializer(instance.grupo_profesional).data
        representation['especialidad'] = EspecialidadSerializer(instance.especialidad).data
        representation['plan_trabajo'] = PlanTrabajoSerializer(instance.plan_trabajo).data
        representation['nivel'] = NivelSerializer(instance.nivel).data
        
        return representation

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
        
class PostulacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postulacion
        fields = '__all__'

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
