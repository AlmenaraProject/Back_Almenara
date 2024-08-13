import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import TipoDocumento, Usuario, Rol, Profesor, Especialidad

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

        return JsonResponse({'message': 'Data imported successfully'}, status=200)