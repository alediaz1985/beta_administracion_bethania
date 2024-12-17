from django.urls import path
from . import views

app_name = 'cuotas_estudiantes'

urlpatterns = [
    path('admin-panel/', views.panel_administracion, name='panel_administracion'),
    path('cuotas/', views.listar_cuotas, name='listar_cuotas'),
    path('cuotas/registrar/<int:estudiante_id>/', views.registrar_cuota, name='registrar_cuota'),
    path('cuotas/registrar_pago/<int:cuota_id>/', views.registrar_pago_cuota, name='registrar_pago_cuota'),
    path('ciclos/', views.listar_ciclos, name='listar_ciclos'),
    path('ciclos/registrar/', views.registrar_ciclo_lectivo, name='registrar_ciclo_lectivo'),
    path('ciclos/habilitar/<int:ciclo_id>/', views.habilitar_ciclo, name='habilitar_ciclo'),
    path('montos/', views.listar_montos, name='listar_montos'),
    path('montos/registrar/', views.registrar_montos, name='registrar_montos'),
    path('montos/cambiar-estado/<int:monto_id>/', views.cambiar_estado_monto, name='cambiar_estado_monto'),
    path('niveles/', views.listar_niveles, name='listar_niveles'),
    path('niveles/registrar/', views.registrar_nivel_educativo, name='registrar_nivel_educativo'),
    path("preinscripciones/", views.listar_preinscripciones, name="listar_preinscripciones"),
    path("preinscripciones/registrar/", views.registrar_preinscripcion, name="registrar_preinscripcion"),
    path('inscripciones/', views.listar_preinscripciones_para_inscripcion, name='listar_preinscripciones_para_inscripcion'),
    path('inscripciones/<int:preinscripcion_id>/inscribir/', views.inscribir_estudiante, name='inscribir_estudiante'),
    path('inscripciones/listar/', views.listar_inscripciones, name='listar_inscripciones'),
    path('estado_deuda/<int:estudiante_id>/', views.estado_deuda_por_ciclo, name='estado_deuda_por_ciclo'),
    path('estado_deuda/', views.listado_estado_deuda, name='listado_estado_deuda'),
    path('pagar_inscripcion/', views.pagar_inscripcion, name='pagar_inscripcion'),
    path('pagar_cuotas/', views.pagar_cuotas, name='pagar_cuotas'),
]
