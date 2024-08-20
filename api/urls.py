from django.urls import path, include, re_path
from rest_framework import routers
from django.contrib.auth import views as auth_views
from api.views import *
from api.importviews import *
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
routers.register(r'postulacion', PostulacionViewSet)
routers.register(r'usuario', UsuarioViewSet)
routers.register(r'grupo-profesional', GrupoProfesionalViewSet)
routers.register(r'nivel', NivelViewSet)
routers.register(r'gerencia-dependencia', GerenciaDependenciaViewSet)
routers.register(r'formulario', FormularioViewSet)


urlpatterns = [
    path('', include(routers.urls)),
    path('aceptar-postulacion/', AceptarPostulacion.as_view(), name='AceptarPostulacion'),
    path('rechazar-postulacion/', RechazarPostulacion.as_view(), name='RechazarPostulacion'),
    path('signup/', SingnupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-details/', UserDetails.as_view(), name='UserDetails'),
    path('logout/', logout, name='logout'),
    path('import-profesional/', ImportProfesionalView.as_view(), name='import'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='recover/password_reset_form.html'), name='password_reset_confirm'),
]
