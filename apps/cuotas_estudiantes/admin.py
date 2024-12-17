from django.contrib import admin
from .models import CicloLectivo, MesCicloLectivo, Preinscripcion

@admin.register(CicloLectivo)
class CicloLectivoAdmin(admin.ModelAdmin):
    list_display = ('anio', 'fecha_inicio', 'fecha_fin', 'habilitado')
    search_fields = ('anio',)

@admin.register(MesCicloLectivo)
class MesCicloLectivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciclo_lectivo')
    list_filter = ('ciclo_lectivo',)

@admin.register(Preinscripcion)
class PreinscripcionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'nivel_educativo', 'fecha_preinscripcion')
    search_fields = ('estudiante__cuil_estudiante', 'nivel_educativo__nombre')
