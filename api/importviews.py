from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
import pandas as pd
from .models import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthenticationFailed('Authorization header missing')
    
    token_key = auth_header.split(' ')[1]
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        raise AuthenticationFailed('Invalid token')

@method_decorator(csrf_exempt, name='dispatch')
class ImportProfesionalView(View):
    @swagger_auto_schema(
        operation_description='Importar profesionales desde un archivo excel',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='Archivo excel con los datos de los profesionales')
            }
        ),
        responses={200: 'Datos importados correctamente', 400: 'Errores encontrados'}
    )
    def post(self, request):
        try:
            usuario_modificacion = get_user_from_token(request)
        except AuthenticationFailed as e:
            return JsonResponse({'message': str(e)}, status=401)

        file = request.FILES['file']
        df = pd.read_excel(file)

        if df.empty:
            return JsonResponse({'message': 'No se importaron datos'}, status=400)

        errores = []
        datos_validos = []

        for index, row in df.iterrows():
            try:
                tipo_documento = get_object_or_404(TipoDocumento, nombre=row['TIPO_DOCUMENTO'])
                especialidad = get_object_or_404(Especialidad, nombre=row['ESPECIALIDAD'])
                plaza = get_object_or_404(Plaza, nombre=row['PLAZA'])
                entidad = get_object_or_404(Entidad, nombre=row['ENTIDAD'])
                centro_asistencial = get_object_or_404(Centro_Asistencial, nombre=row['CENTRO_ASISTENCIAL'])
                universidad = get_object_or_404(Universidad, nombre=row['UNIVERSIDAD'])
                plan_trabajo = get_object_or_404(Plan_trabajo, nombre=row['PLAN_TRABAJO'])
                nivel = get_object_or_404(Nivel, nombre=row['NIVEL'])

                # Obtener el grupo profesional desde la especialidad
                grupo_profesional = especialidad.grupo_profesional

                # Verificar que el grupo profesional coincide con el proporcionado en el archivo
                if grupo_profesional.nombre != row['GRUPO_PROFESIONAL']:
                    raise ValueError(f"El grupo profesional {grupo_profesional.nombre} no coincide con el proporcionado {row['GRUPO_PROFESIONAL']}")

                # Obtener la categoría profesional desde el grupo profesional
                categoria_profesional = grupo_profesional.categoria_profesional

                # Verificar que la categoría profesional coincide con la proporcionada en el archivo
                if categoria_profesional.nombre != row['CATEGORIA']:
                    raise ValueError(f"La categoría profesional {categoria_profesional.nombre} no coincide con la proporcionada {row['CATEGORIA']}")

                is_postgrado = categoria_profesional.is_postgrado
                  
                datos_validos.append({
                    'persona': {
                        'nombre': row['NOMBRE'],
                        'apellido': row['APELLIDO'],
                        'email': row['EMAIL'], 
                        'telefono': row['TELEFONO'],
                        'direccion': row['DIRECCION'],
                        'numero_documento': row['NUMERO_DOCUMENTO'],
                        'tipo_documento': tipo_documento
                    },
                    'profesional': {
                        'CMP': row['CMP'],
                        'plaza': plaza,
                        'entidad': entidad,
                        'fecha_inscripcion': row['FECHA_INSCRIPCION'],
                        'fecha_fin': row['FECHA_FIN'], 
                        'centro_asistencial': centro_asistencial,
                        'universidad_procedencia': universidad,
                        'categoria_profesional': categoria_profesional,
                        'grupo_profesional': grupo_profesional,
                        'especialidad': especialidad,
                        'plan_trabajo': plan_trabajo,
                        'nivel': nivel,
                        'usuario_modificacion': usuario_modificacion,
                        'is_postgrado': is_postgrado
                    }
                })
            except Exception as e:
                errores.append(f"Error en la fila {index + 2}: {str(e)}")

        if errores:
            return JsonResponse({'message': 'Errores encontrados', 'errores': errores}, status=400)

        for datos in datos_validos:
            with transaction.atomic():
                try:
                    # Verificar si la persona ya existe
                    persona = Persona.objects.filter(numero_documento=datos['persona']['numero_documento']).first()
                    if not persona:
                        persona = Persona.objects.create(**datos['persona'])
                    else:
                        # Si la persona ya existe, verificar si el profesional ya existe
                        profesional = Profesional.objects.filter(persona=persona, CMP=datos['profesional']['CMP']).first()
                        if profesional:
                            raise ValueError(f"Documento: {datos['persona']['numero_documento']} ya existente")

                    # Crear el profesional si no existe
                    Profesional.objects.create(persona=persona, **datos['profesional'])
                except Exception as e:
                    errores.append(f"Error al crear profesional para la persona con documento {datos['persona']['numero_documento']}: {str(e)}")

        if errores:
            return JsonResponse({'message': 'Errores encontrados', 'errores': errores}, status=400)

        return JsonResponse({'message': 'Datos importados correctamente'}, status=200)