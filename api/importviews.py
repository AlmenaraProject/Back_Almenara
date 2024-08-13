from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .models import Profesional, TipoDocumento

@method_decorator(csrf_exempt, name='dispatch')
class ImportProfesionalView(View):
    def post(self, request):
        file = request.FILES['file']
        df = pd.read_excel(file)

        if df.empty:
            return JsonResponse({'message': 'No se importaron datos'}, status=400)

        for index, row in df.iterrows():
            tipo_documento = get_object_or_404(TipoDocumento, nombre=row['tipo_documento_nombre'])
            Profesional.objects.create(
                nombre=row['nombre'],
                apellido=row['apellido'],
                tipo_documento=tipo_documento,
                numero_documento=row['numero_documento'],
                correo=row['correo'],
                telefono=row['telefono'],
                estado=row['estado']
            )

        return JsonResponse({'message': 'Datos importados correctamente'}, status=200)