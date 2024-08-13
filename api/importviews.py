import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import TipoDocumento, Usuario, Rol, Profesor, Especialidad
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class ImportDataView(View):
    def post(self, request):
        file = request.FILES['file']
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            # Ejemplo para importar datos a TipoDocumento
            TipoDocumento.objects.create(
                nombre=row['nombre'],
                estado=row['estado']
            )

        if df.empty:
            return JsonResponse({'message': 'No se importaron datos'}, status=400)
        return JsonResponse({'message': 'Datos importados correctamente'}, status=200)