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
from django.contrib.auth.forms import PasswordResetForm
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

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

class GrupoOcupacionalViewSet(viewsets.ModelViewSet):
    queryset = Grupo_Ocupacional.objects.all()
    serializer_class = GrupoOcupacionalSerializer

class EstablecimientoRPAViewSet(viewsets.ModelViewSet):
    queryset = Establecimiento_RPA.objects.all()
    serializer_class = EstablecimientoRPASerializer
    
class UniversidadFilter(django_filters.FilterSet):
    class Meta:
        model = Universidad
        fields = ['nombre','estado','coordinador','siglas','ciudad']

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
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

class CategoriaProfesionalViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProfesional.objects.all()
    serializer_class = CategoriaProfesionalSerializer

class PlanTrabajoViewSet(viewsets.ModelViewSet):
    queryset = Plan_trabajo.objects.all()
    serializer_class = PlanTrabajoSerializer

class AcuerdoViewSet(viewsets.ModelViewSet):
    queryset = Acuerdo.objects.all()
    serializer_class = AcuerdoSerializer

class CoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Coordinador.objects.all()
    serializer_class = CoordinadorSerializer

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class GrupoProfesionalViewSet(viewsets.ModelViewSet):
    queryset = GrupoProfesional.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GrupoProfesionalCreateSerializer
        return GrupoProfesionalSerializer
    
class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer

class GerenciaDependenciaViewSet(viewsets.ModelViewSet):
    queryset = Gerencia_dependencia.objects.all()
    serializer_class = GerenDependenciaSerializer

class FormularioViewSet(viewsets.ModelViewSet):
    queryset = Formulario.objects.all()
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('nombre', openapi.IN_QUERY, description="Nombre del formulario", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_creacion', openapi.IN_QUERY, description="Fecha de creación", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_modificacion', openapi.IN_QUERY, description="Fecha de modificación", type=openapi.TYPE_STRING),
        openapi.Parameter('estado', openapi.IN_QUERY, description="Estado del formulario", type=openapi.TYPE_STRING),
        openapi.Parameter('curso', openapi.IN_QUERY, description="Curso", type=openapi.TYPE_STRING),
    ])    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FormularioCreateSerializer
        return FormularioSerializer
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('nombre', openapi.IN_QUERY, description="Nombre del formulario", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_creacion', openapi.IN_QUERY, description="Fecha de creación", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_modificacion', openapi.IN_QUERY, description="Fecha de modificación", type=openapi.TYPE_STRING),
        openapi.Parameter('estado', openapi.IN_QUERY, description="Estado del formulario", type=openapi.TYPE_STRING),
        openapi.Parameter('curso_id', openapi.IN_QUERY, description="Curso", type=openapi.TYPE_STRING),
    ])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='by-curso')
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('curso_id', openapi.IN_QUERY, description="ID del curso", type=openapi.TYPE_INTEGER)
    ])
    def list_by_curso(self, request):
        curso_id = request.query_params.get('curso_id')
        if not curso_id:
            return Response({"detail": "curso_id es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        formularios = self.queryset.filter(curso_id=curso_id)
        page = self.paginate_queryset(formularios)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(formularios, many=True)
        return Response(serializer.data)
    
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
        fields = ['fecha_postulacion','estado']
        
class PostulacionViewSet(viewsets.ModelViewSet):
    queryset = Postulacion.objects.all()
    serializer_class = PostulacionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostulacionFilter
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('profesional', openapi.IN_QUERY, description="Profesional", type=openapi.TYPE_STRING),
        openapi.Parameter('fecha_postulacion', openapi.IN_QUERY, description="Fecha de postulación", type=openapi.TYPE_STRING),
        openapi.Parameter('estado', openapi.IN_QUERY, description="Estado", type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'], url_path='enviar-postulacion')
    @swagger_auto_schema(
        operation_description="Agregar postulaciones a un formulario",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'formulario_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID del formulario'),
                'postulacion': openapi.Schema(type=openapi.TYPE_OBJECT, description='Datos de la postulación', properties={
                    'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del postulante'),
                    'apellido': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del postulante'),
                    'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del postulante'),
                    'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono del postulante'),
                    'profesion': openapi.Schema(type=openapi.TYPE_STRING, description='Profesión del postulante'),
                    'establecimiento_RPA': openapi.Schema(type=openapi.TYPE_STRING, description='Establecimiento RPA del postulante'),
                    'grupo_ocupacional': openapi.Schema(type=openapi.TYPE_STRING, description='Grupo ocupacional del postulante'),
                    'regimen_laboral': openapi.Schema(type=openapi.TYPE_STRING, description='Regimen laboral del postulante'),
                    'cargo': openapi.Schema(type=openapi.TYPE_STRING, description='Cargo del postulante'),
                    'codigo_planilla': openapi.Schema(type=openapi.TYPE_STRING, description='Código de planilla del postulante'),
                    'tipo_documento': openapi.Schema(type=openapi.TYPE_STRING, description='ID del tipo de documento del postulante'),
                    'documento': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento del postulante')
                }),
            },
            required=['formulario_id', 'postulacion']
        ),
        responses={200: "Postulacion added successfully", 400: "Invalid data"},
    )
    def enviar_postulacion(self, request, *args, **kwargs):
        formulario_id = request.data.get('formulario_id')
        postulacion_data = request.data.get('postulacion')
        
        if not formulario_id or not postulacion_data:
            return Response({"error": "Formulario ID and Postulacion data are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            formulario = Formulario.objects.get(id=formulario_id)
        except Formulario.DoesNotExist:
            return Response({"error": "Formulario not found"}, status=status.HTTP_404_NOT_FOUND)

        documento_identidad = postulacion_data.get('documento')
        if formulario.postulacion.filter(documento=documento_identidad).exists():
            return Response({"error": "Ya existe una postulación con el mismo documento de identidad en este formulario."}, status=status.HTTP_400_BAD_REQUEST)

        postulacion_serializer = PostulacionSerializer(data=postulacion_data)
        if postulacion_serializer.is_valid():
            postulacion = postulacion_serializer.save()
            formulario.postulacion.add(postulacion)
            formulario.save()
            # Informar que fue agregado en un email
            context = {
                'nombre_completo': postulacion.nombre + ' ' + postulacion.apellido,
                'correo': postulacion.correo, 
                'curso': formulario.curso.nombre
            }
            email_body = render_to_string('register/sendform_email.html', context)
            email = EmailMessage(
                'Postulación agregada',
                email_body,
                'testalmenara@gmail.com',
                [postulacion.correo],
            )
            email.content_subtype = 'html'
            email.send()
            return Response({"message": "Postulacion added successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(postulacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'], url_path='rechazar-postulacion')
    @swagger_auto_schema(
        operation_description="Rechazar postulaciones",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_curso': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='ID del curso'
                ),
                'postulaciones': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    additional_properties=openapi.Schema(type=openapi.TYPE_STRING),
                    description='Diccionario de IDs de postulaciones y sus observaciones'
                ),
            },
            required=['id_curso', 'postulaciones']
        ),
        responses={
            200: openapi.Response(description="Postulaciones rejected successfully"),
            400: openapi.Response(description="Invalid data"),
            404: openapi.Response(description="Postulacion or Curso not found"),
        },
    )
    def rechazar_postulacion(self, request, *args, **kwargs):
        id_curso = request.data.get('id_curso')
        postulaciones_data = request.data.get('postulaciones', {})

        if id_curso is None:
            return Response({"error": "id_curso is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(postulaciones_data, dict):
            return Response({"error": "postulaciones must be a dictionary"}, status=status.HTTP_400_BAD_REQUEST)
        ids_postulacion = list(postulaciones_data.keys())

        try:
            postulaciones = Postulacion.objects.filter(id__in=ids_postulacion)
        except Postulacion.DoesNotExist:
            return Response({"error": "Postulacion not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            curso = Curso.objects.get(id=id_curso)
        except Curso.DoesNotExist:
            return Response({"error": "Curso not found"}, status=status.HTTP_404_NOT_FOUND)

        # Informar que fue rechazado en un email
        for postulacion in postulaciones:
            observacion = postulaciones_data.get(str(postulacion.id), "No se proporcionó un motivo de rechazo.")
            context = {
                'nombre': postulacion.nombre,
                'apellido': postulacion.apellido,
                'correo': postulacion.correo,
                'curso': curso.nombre,
                'observacion': observacion
            }
            email_body = render_to_string('register/reject_email.html', context)
            email = EmailMessage(
                'Rechazo de postulación',
                email_body,
                'testalmenara@gmail.com',
                [postulacion.correo],
            )
            email.content_subtype = 'html'
            email.send()

        postulaciones.update(is_rejected=True)
        for postulacion in postulaciones:
            postulacion.observaciones = postulaciones_data.get(str(postulacion.id), "No se proporcionó un motivo de rechazo.")
            postulacion.save()
            curso.postulacion.add(*postulaciones)
            curso.save()
        return Response({"message": "Postulaciones rejected successfully"}, status=status.HTTP_200_OK)

     
    @action(detail=False, methods=['post'], url_path='aceptar-postulacion')
    @swagger_auto_schema(
        operation_description="Migrar postulaciones a un curso",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_curso': openapi.Schema(type=openapi.TYPE_STRING, description='ID del curso'),
                'ids_postulacion': openapi.Schema(type=openapi.TYPE_ARRAY, 
                                                  items=openapi.Schema(type=openapi.TYPE_STRING),
                                                  description='IDs de las postulaciones'),
            },
            required=['id_curso', 'ids_postulacion']
        ),
        responses={200: "Postulaciones migrated successfully", 400: "Invalid data"},
    )
    def aceptar_postulacion(self, request, *args, **kwargs):
        id_curso = request.data.get('id_curso')
        ids_postulacion = request.data.get('ids_postulacion')

        if id_curso is None or ids_postulacion is None:
            return Response({"error": "id_curso and ids_postulacion are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            curso = Curso.objects.get(id=id_curso)
        except Curso.DoesNotExist:
            return Response({"error": "Curso not found"}, status=status.HTTP_404_NOT_FOUND)

        postulaciones = Postulacion.objects.filter(id__in=ids_postulacion)
        if not postulaciones.exists():
            return Response({"error": "No valid postulaciones found"}, status=status.HTTP_404_NOT_FOUND)
        
        postulaciones.update(estado=True)
        postulaciones.update(is_rejected=False)
        curso.postulacion.add(*postulaciones)
        curso.save()
        
        #Informar que fue aceptado en un email
        for postulacion in postulaciones:
            context = {'curso': curso.nombre, 
                       'fecha_inicio': curso.fecha_inicio, 
                       'fecha_fin': curso.fecha_fin, 
                       'correo': postulacion.correo, 
                       'nombre_completo': postulacion.nombre + ' ' + postulacion.apellido}
            email_body = render_to_string('register/course_confirmation_email.html', context)
            email = EmailMessage(
                'Confirmación de postulación',
                email_body,
                'testalmenara@gmail.com',
                [postulacion.correo],
            )
            email.content_subtype = 'html'
            email.send()

        return Response({"message": "Postulaciones migrated successfully"}, status=status.HTTP_200_OK)     

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
                # Renderizar la plantilla de correo electrónico con el contexto
                context = {'email': user.email}
                email_body = render_to_string(
                    'register/confirmation_email.html', context)

                # Enviar correo de confirmación
                email = EmailMessage(
                    'Confirmación de registro',
                    email_body,
                    'testalmenara@gmail.com',
                    [user.email],
                )
                email.content_subtype = 'html'  # Establecer el contenido como HTML
                email.send()
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
        fields = [
            'persona', 'CMP', 'plaza', 'entidad', 'centro_asistencial', 'universidad_procedencia',
            'categoria_profesional', 'grupo_profesional', 'especialidad', 'is_postgrado', 'sede_adjudicacion',
            'plan_trabajo', 'fecha_inscripcion', 'fecha_fin', 'duracion', 'gerencia_dependencia', 'nivel', 'estado'
        ]

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
                'persona': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='Datos de la persona',
                    properties={
                        'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la persona'),
                        'apellido': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido de la persona'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email de la persona'),
                        'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono de la persona'),
                        'direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de la persona'),
                        'numero_documento': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento de la persona'),
                        'tipo_documento': openapi.Schema(type=openapi.TYPE_STRING, description='ID del tipo de documento de la persona'),
                    },
                    required=['nombre', 'apellido', 'email', 'telefono', 'numero_documento', 'tipo_documento']
                ),
                'CMP': openapi.Schema(type=openapi.TYPE_STRING, description='Código CMP del profesional'),
                'fecha_inscripcion': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de inscripción'),
                'fecha_modificacion': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de modificación'),
                'estado': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Estado del profesional'),
                'centro_asistencial': openapi.Schema(type=openapi.TYPE_STRING, description='ID del Centro Asistencial donde labora'),
                'categoria_profesional': openapi.Schema(type=openapi.TYPE_STRING, description='ID del Tipo de profesional (CategoriaProfesional)'),
                'grupo_profesional': openapi.Schema(type=openapi.TYPE_STRING, description='ID del Grupo Profesional'),
                'especialidad': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la Especialidad del profesional'),
                'plaza': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la Plaza'),
                'entidad': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la Entidad a la que pertenece'),
                'fecha_fin': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de fin de contrato o trabajo'),
                'duracion': openapi.Schema(type=openapi.TYPE_INTEGER, description='Duración en meses'),
                'is_postgrado': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si el profesional es postgrado'),
                'sede_adjudicacion': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la Sede de adjudicación'),
                'gerencia_dependencia': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la Gerencia o dependencia del profesional'),
                'universidad_procedencia': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la Universidad de procedencia'),
                'plan_trabajo': openapi.Schema(type=openapi.TYPE_STRING, description='ID del Plan de trabajo asignado'),
                'usuario_modificacion': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario que realizó la última modificación'),
                'nivel': openapi.Schema(type=openapi.TYPE_STRING, description='ID del Nivel del profesional'),
            },
            required=[
                'persona', 'CMP', 'fecha_inscripcion', 'fecha_modificacion', 'estado', 'centro_asistencial',
                'categoria_profesional', 'grupo_profesional', 'especialidad', 'plaza', 'entidad', 'universidad_procedencia',
                'plan_trabajo', 'usuario_modificacion', 'is_postgrado', 'nivel'
            ],
        ),
        responses={
            201: openapi.Response('Profesional creado exitosamente', ProfesionalSerializer),
            400: "Datos inválidos",
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = ProfesionalSerializer(data=request.data)
        if serializer.is_valid():
            profesional = serializer.save()
            return Response({
                "message": "Profesional creado exitosamente",
                "data": ProfesionalSerializer(profesional).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Error en la validación de los datos",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetView(APIView):
    @swagger_auto_schema(
        operation_description="Enviar correo electrónico de restablecimiento de contraseña",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            },
            required=['email']
        ),
        responses={
            200: "Password reset email sent.",
            400: "Invalid data",
        },
    )
    def post(self, request):
        form = PasswordResetForm(request.data)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'from_email': 'testalmenara@gmail.com',
                'request': request,
                'html_email_template_name': 'recover/password_reset_email.html',
                'extra_email_context': {'host': request.get_host()}
            }
            form.save(**opts)
            return Response("Password reset email sent.", status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

