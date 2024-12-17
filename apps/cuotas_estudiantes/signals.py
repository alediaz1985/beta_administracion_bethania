from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CicloLectivo, MesCicloLectivo

@receiver(post_save, sender=CicloLectivo)
def crear_meses_ciclo(sender, instance, created, **kwargs):
    if created:
        meses = [
            "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        for mes in meses:
            MesCicloLectivo.objects.create(ciclo_lectivo=instance, nombre=mes)
