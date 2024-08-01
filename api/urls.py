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
routers.register(r'centro-asistencial', CentroAsistencialViewSet)
routers.register(r'tipo-profesional', TipoProfesionalViewSet)
routers.register(r'plaza', PlazaViewSet)
routers.register(r'entidad', EntidadViewSet)
routers.register(r'profesional', ProfesionalViewSet)
routers.register(r'plan-trabajo', PlanTrabajoViewSet)
routers.register(r'coordinador', CoordinadorViewSet)
routers.register(r'curso', CursoViewSet)
routers.register(r'profesor', ProfesorViewSet)


urlpatterns = [
    path('', include(routers.urls)),
    path('signup/', SingnupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-details/', UserDetails.as_view(), name='UserDetails'),
    path('logout/', logout, name='logout'),
]
