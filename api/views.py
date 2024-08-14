from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from api.serializers import *
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.mail import EmailMessage
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth import get_user_model
import django_filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    
class UniversidadFilter(django_filters.FilterSet):
    class Meta:
        model = Universidad
        fields = ['nombre','estado','coordinador','siglas','ciudad']

class UniversidadViewSet(viewsets.ModelViewSet):
    queryset = Universidad.objects.all().order_by('id')
    serializer_class = UniversidadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UniversidadFilter
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('nombre', openapi.IN_QUERY, description="Nombre de la universidad", type=openapi.TYPE_STRING),
        openapi.Parameter('estado', openapi.IN_QUERY, description="Estado de la universidad", type=openapi.TYPE_STRING),
        openapi.Parameter('coordinador', openapi.IN_QUERY, description="Coordinador de la universidad", type=openapi.TYPE_STRING),
        openapi.Parameter('siglas', openapi.IN_QUERY, description="Siglas de la universidad", type=openapi.TYPE_STRING),
        openapi.Parameter('ciudad', openapi.IN_QUERY, description="Ciudad de la universidad", type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class PlazaViewSet(viewsets.ModelViewSet):
    queryset = Plaza.objects.all().order_by('id')
    serializer_class = PlazaSerializer

class EntidadViewSet(viewsets.ModelViewSet):
    queryset = Entidad.objects.all().order_by('id')
    serializer_class = EntidadSerializer

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all().order_by('id')
    serializer_class = EspecialidadSerializer

class Sede_AdjudicacionViewSet(viewsets.ModelViewSet):
    queryset = Sede_Adjudicacion.objects.all().order_by('id')
    serializer_class = Sede_AdjudicacionSerializer

class CentroAsistencialViewSet(viewsets.ModelViewSet):
    queryset = Centro_Asistencial.objects.all().order_by('id')
    serializer_class = CentroAsistencialSerializer

class TipoProfesionalViewSet(viewsets.ModelViewSet):
    queryset = Tipo_profesional.objects.all().order_by('id')
    serializer_class = TipoProfesionalSerializer

class PlanTrabajoViewSet(viewsets.ModelViewSet):
    queryset = Plan_trabajo.objects.all()
    serializer_class = PlanTrabajoSerializer

class CoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Coordinador.objects.all()
    serializer_class = CoordinadorSerializer

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def partial_update(self, request, pk=None):
        usuario = self.get_queryset().filter(pk=pk).first()
        if not usuario:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer_class()(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostulacionFilter(django_filters.FilterSet):
    class Meta:
        model = Postulacion
        fields = ['profesional','plan_trabajo','fecha_postulacion','estado']
        
class PostulacionViewSet(viewsets.ModelViewSet):
    queryset = Postulacion.objects.all()
    serializer_class = PostulacionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostulacionFilter
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('profesional', openapi.IN_QUERY, description="Profesional", type=openapi.TYPE_STRING),
        openapi.Parameter('plan_trabajo', openapi.IN_QUERY, description="Plan de trabajo", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_postulacion', openapi.IN_QUERY, description="Fecha de postulación", type=openapi.TYPE_STRING),
        openapi.Parameter('estado', openapi.IN_QUERY, description="Estado", type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class CursoFilter(django_filters.FilterSet):
    class Meta:
        model = Curso
        fields = ['nombre','postulacion','profesor','fecha_inicio','fecha_fin','estado']

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CursoFilter
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('nombre', openapi.IN_QUERY, description="Nombre del curso", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_inicio', openapi.IN_QUERY, description="Fecha de inicio", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_fin', openapi.IN_QUERY, description="Fecha de fin", type=openapi.TYPE_STRING),
        openapi.Parameter('estado', openapi.IN_QUERY, description="Estado", type=openapi.TYPE_STRING),
        openapi.Parameter('profesor', openapi.IN_QUERY, description="Profesor", type=openapi.TYPE_STRING),
        openapi.Parameter('plan_trabajo', openapi.IN_QUERY, description="Plan de trabajo", type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

   
class SingnupView(APIView):
    @swagger_auto_schema(
        operation_description="Registro de usuario",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'persona': openapi.Schema(type=openapi.TYPE_OBJECT, description='Persona', properties={
                    'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la persona'),
                    'apellido': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido de la persona'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email de la persona'),
                    'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono de la persona'),
                    'direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de la persona'),
                    'numero_documento': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento de la persona'),
                    'tipo_documento': openapi.Schema(type=openapi.TYPE_STRING, description='ID del tipo de documento de la persona'),
                }),
                'rol': openapi.Schema(type=openapi.TYPE_STRING, description='ID del rol del usuario'),
            },
            required=['email', 'password', 'persona', 'rol']
        ),
        responses={
            200: openapi.Response('User registered successfully', SignupSerializer),
            400: "Invalid data",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            persona_data = request.data.get('persona')
            persona_serializer = PersonaSerializer(data=persona_data)
            if persona_serializer.is_valid():
                persona = persona_serializer.save()
                
                # Obtener la instancia de Rol usando el UUID
                rol_uuid = request.data['rol']
                rol = get_object_or_404(Rol, pk=rol_uuid)  # Asume que 'rol' es un UUID válido para un Rol existente
                
                # Crear el usuario con la instancia de Rol
                user = Usuario.objects.create(
                    email=request.data['email'],
                    password=make_password(request.data['password']),  # Hash the password
                    persona=persona,
                    rol=rol  # Asignar la instancia de Rol
                )
                
                token = Token.objects.create(user=user)
                return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(persona_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    rol_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del rol'),
            'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del rol'),
            'estado': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Estado del rol'),
        }
    )

    user_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Correo electrónico del usuario'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña encriptada del usuario'),
            'persona': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la persona asociada al usuario'),
            'rol': rol_schema,
        }
    )

    @swagger_auto_schema(
        operation_description="A custom description for this operation",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response('Successful login', user_schema),
            400: "Please provide both email and password",
            404: "User not found",
            401: "Invalid password",
        },
    )
    def post(self, request):
        User = get_user_model()
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response("Please provide both email and password.", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response("Invalid password", status=status.HTTP_401_UNAUTHORIZED)
        
        # Actualizar el campo last_login del usuario
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        print(user.last_login)
        # Check if a token already exists for the user
        token, created = Token.objects.get_or_create(user=user)
        serializer = LoginSerializer(user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserDetails(APIView):
    @swagger_auto_schema(
        operation_description="Obtener detalles del usuario",
        manual_parameters=[openapi.Parameter(
            'Authorization', openapi.IN_HEADER, description="Token de autenticación", type=openapi.TYPE_STRING)],
        responses={200: openapi.Response('User details', UsuarioSerializer)},
    )
    def get(self, request, format=None):
        user = request.user  # El usuario autenticado actualmente
        # Puedes personalizar los datos que deseas devolver
        user_data = {
            'id': user.id,
            'email': user.email,
            'is_active': user.is_active,
            'last_login': user.last_login,
            'persona': {
                'id': user.persona.id,
                'nombre': user.persona.nombre,
                'apellido': user.persona.apellido,
                'tipo_documento': user.persona.tipo_documento.nombre,
                'documento_identidad': user.persona.numero_documento,
                'direccion': user.persona.direccion,
                'telefono': user.persona.telefono,
            },
            'rol':{
                'id': user.rol.id,
                'nombre': user.rol.nombre,
                'estado': user.rol.estado
            }
        }
        return Response(user_data)
       
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    print(request.auth)
    token = request.auth
    token.delete()
    return Response("Logged out successfully", status=status.HTTP_200_OK)

class ProfesionalFilter(django_filters.FilterSet):
    class Meta:
        model = Profesional
        fields = ['persona','CMP','fecha_inscripcion','fecha_modificacion','estado','especialidad','centro_Asistencial','tipo_profesional','plaza','entidad']

class ProfesionalViewSet(viewsets.ModelViewSet):
    queryset = Profesional.objects.all()
    serializer_class = ProfesionalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfesionalFilter

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('persona', openapi.IN_QUERY, description="Persona", type=openapi.TYPE_STRING),
        openapi.Parameter('CMP', openapi.IN_QUERY, description="CMP", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_inscripcion', openapi.IN_QUERY, description="Fecha de inscripción", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_modificacion', openapi.IN_QUERY, description="Fecha de modificación", type=openapi.TYPE_STRING),
        openapi.Parameter('estado', openapi.IN_QUERY, description="Estado", type=openapi.TYPE_STRING),
        openapi.Parameter('especialidad', openapi.IN_QUERY, description="Especialidad", type=openapi.TYPE_STRING),
        openapi.Parameter('centro_Asistencial', openapi.IN_QUERY, description="Centro Asistencial", type=openapi.TYPE_STRING),
        openapi.Parameter('tipo_profesional', openapi.IN_QUERY, description="Tipo de profesional", type=openapi.TYPE_STRING),
        openapi.Parameter('plaza', openapi.IN_QUERY, description="Plaza", type=openapi.TYPE_STRING),
        openapi.Parameter('entidad', openapi.IN_QUERY, description="Entidad", type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crear un profesional junto con los datos de la persona",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'persona': openapi.Schema(type=openapi.TYPE_OBJECT, description='Datos de la persona', properties={
                    'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la persona'),
                    'apellido': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido de la persona'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email de la persona'),
                    'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono de la persona'),
                    'direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de la persona'),
                    'numero_documento': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento de la persona'),
                    'tipo_documento': openapi.Schema(type=openapi.TYPE_STRING, description='ID del tipo de documento de la persona'),
                }),
                'CMP': openapi.Schema(type=openapi.TYPE_STRING, description='CMP'),
                'fecha_inscripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Fecha de inscripción'),
                'fecha_modificacion': openapi.Schema(type=openapi.TYPE_STRING, description='Fecha de modificación'),
                'estado': openapi.Schema(type=openapi.TYPE_STRING, description='Estado'),
                'especialidad': openapi.Schema(type=openapi.TYPE_STRING, description='Especialidad'),
                'centro_Asistencial': openapi.Schema(type=openapi.TYPE_STRING, description='Centro Asistencial'),
                'tipo_profesional': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de profesional'),
                'plaza': openapi.Schema(type=openapi.TYPE_STRING, description='Plaza'),
                'entidad': openapi.Schema(type=openapi.TYPE_STRING, description='Entidad'),
                'universidad_procedencia': openapi.Schema(type=openapi.TYPE_STRING, description='Universidad de procedencia'),
                'plan_trabajo': openapi.Schema(type=openapi.TYPE_STRING, description='Plan de trabajo'),
                'usuario_modificacion': openapi.Schema(type=openapi.TYPE_STRING, description='Usuario de modificación'),
            },
            required=['persona', 'CMP', 'fecha_inscripcion', 'fecha_modificacion', 'estado', 'especialidad', 'centro_Asistencial', 'tipo_profesional', 'plaza', 'entidad']
        ),
        responses={
            201: openapi.Response('Profesional created successfully', ProfesionalSerializer),
            400: "Invalid data",
        },
    )
    def create(self, request, *args, **kwargs):
        persona_data = request.data.get('persona')
        profesional_data = request.data

        persona_serializer = PersonaSerializer(data=persona_data)
        if persona_serializer.is_valid():
            persona = persona_serializer.save()
            profesional_data['persona'] = persona.id
            profesional_serializer = ProfesionalSerializer(data=profesional_data)
            if profesional_serializer.is_valid():
                profesional_serializer.save()
                return Response(profesional_serializer.data, status=status.HTTP_201_CREATED)
            else:
                persona.delete()  # Rollback persona creation if profesional data is invalid
                return Response(profesional_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(persona_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


