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
    class Meta:
        model = Usuario
        fields = 'id', 'email', 'persona', 'rol', 'estado', 'last_login'

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
    class Meta:
        model = Profesional
        fields = '__all__'

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
