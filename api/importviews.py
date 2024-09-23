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
                tipo_documento = get_object_or_404(TipoDocumento, nombre=row['TIPO_DOCUMENTO_NOMBRE'])
                especialidad = get_object_or_404(Especialidad, nombre=row['ESPECIALIDAD_NOMBRE'])
                plaza = get_object_or_404(Plaza, nombre=row['PLAZA_NOMBRE'])
                entidad = get_object_or_404(Entidad, nombre=row['ENTIDAD_NOMBRE'])
                centro_asistencial = get_object_or_404(Centro_Asistencial, nombre=row['CENTRO_ASISTENCIAL_NOMBRE'])
                universidad = get_object_or_404(Universidad, nombre=row['UNIVERSIDAD_NOMBRE'])
                categoria_profesional = get_object_or_404(CategoriaProfesional, nombre=row['CATEGORIA_PROFESIONAL_NOMBRE'])
                plan_trabajo = get_object_or_404(Plan_trabajo, nombre=row['PLAN_TRABAJO_NOMBRE'])
                grupo_profesional = get_object_or_404(GrupoProfesional, nombre=row['GRUPO_PROFESIONAL_NOMBRE'])
                nivel = get_object_or_404(Nivel, nombre=row['NIVEL_NOMBRE'])
                
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
                        'centro_Asistencial': centro_asistencial,
                        'universidad_procedencia': universidad,
                        'categoria_profesional': categoria_profesional,
                        'grupo_profesional': grupo_profesional,
                        'especialidad': especialidad,
                        'plan_trabajo': plan_trabajo,
                        'nivel': nivel,
                        'usuario_modificacion': usuario_modificacion,
                        'is_postgraduado': row['IS_POSTGRADUADO'],
                        'estado': row['ESTADO']
                    }
                })
            except Exception as e:
                errores.append(f"Error en la fila {index + 2}: {str(e)}")

        if errores:
            return JsonResponse({'message': 'Errores encontrados', 'errores': errores}, status=400)

        for datos in datos_validos:
            persona = Persona.objects.create(**datos['persona'])
            Profesional.objects.create(persona=persona, **datos['profesional'])

        return JsonResponse({'message': 'Datos importados correctamente'}, status=200)