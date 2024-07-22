from django.urls import path, include, re_path
from rest_framework import routers

from api.views import *

routers = routers.DefaultRouter()

routers.register(r'rol', RolViewSet)
routers.register(r'persona', PersonaViewSet)
routers.register(r'tipo-documento', TipoDocumentoViewSet)
routers.register(r'universidad', UniversidadViewSet)
routers.register(r'especialidad', EspecialidadViewSet)
routers.register(r'sede-adjudicacion', Sede_AdjudicacionViewSet)


urlpatterns = [
    path('', include(routers.urls)),
    path('signup/', SingnupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
]
