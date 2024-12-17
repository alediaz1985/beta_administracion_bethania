from django.apps import AppConfig

class CuotasEstudiantesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cuotas_estudiantes'

    def ready(self):
        import apps.cuotas_estudiantes.signals  # Importa el archivo de señales