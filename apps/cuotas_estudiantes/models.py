from django.db import models
from apps.administracion_alumnos.models import Estudiante  # Importa el modelo Estudiante
from django.utils.dateparse import parse_date
from django.apps import apps



from django.db import models
from django.utils.timezone import now
from django.utils import timezone

        
class CicloLectivo(models.Model):
    anio = models.PositiveIntegerField(unique=True, verbose_name="Año del Ciclo Lectivo")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    habilitado = models.BooleanField(default=False, verbose_name="Habilitado")

    def __str__(self):
        return f"Ciclo Lectivo {self.anio}"

    def esta_activo(self):
        """Verifica si el ciclo lectivo está activo según las fechas."""
        from datetime import date
        hoy = date.today()
        return self.habilitado and self.fecha_inicio <= hoy <= self.fecha_fin

class Inscripcion(models.Model):
    estudiante = models.OneToOneField(
        Estudiante,
        on_delete=models.CASCADE,
        related_name="inscripcion"
    )
    ciclo_lectivo = models.ForeignKey(
        CicloLectivo,
        on_delete=models.CASCADE,
        related_name="inscripciones"
    )
    fecha_inscripcion = models.DateField(auto_now_add=True)
    monto_inscripcion = models.DecimalField(max_digits=10, decimal_places=2)
    pagada = models.BooleanField(default=False, verbose_name="Pagada")
    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Descuento (%)"
    )

    def __str__(self):
        return f"{self.estudiante} - {self.ciclo_lectivo}"

    def monto_final(self):
        """Calcula el monto final aplicando el descuento, si existe."""
        if self.descuento:
            return self.monto_inscripcion * (1 - self.descuento / 100)
        return self.monto_inscripcion


from django.db import models
from django.apps import apps


from django.db import models
from django.apps import apps
from decimal import Decimal
from datetime import date


class Cuota(models.Model):
    estudiante = models.ForeignKey(
        "administracion_alumnos.Estudiante",
        on_delete=models.CASCADE,
        related_name="cuotas"
    )
    mes = models.ForeignKey(
        "cuotas_estudiantes.MesCicloLectivo",
        on_delete=models.CASCADE,
        related_name="cuotas"
    )
    monto_base = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Monto Base"
    )
    monto_final = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Monto Final (Con Beca)"
    )
    fecha_pago = models.DateField(
        null=True, blank=True, verbose_name="Fecha de Pago"
    )
    pagada = models.BooleanField(default=False, verbose_name="Pagada")
    fuera_de_termino = models.BooleanField(default=False, verbose_name="Fuera de Término")
    interes_por_mora = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0, verbose_name="Interés por Mora (%)"
    )
    total_a_pagar = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Total a Pagar"
    )

    def calcular_monto_con_beca(self):
        """
        Aplica el porcentaje de beca al monto base, si el estudiante tiene una beca.
        """
        AlumnoBeca = apps.get_model("cuotas_estudiantes", "AlumnoBeca")
        try:
            # Busca si el estudiante tiene una beca asociada al ciclo lectivo
            beca = AlumnoBeca.objects.get(
                estudiante=self.estudiante,
                ciclo_lectivo=self.mes.ciclo_lectivo
            )
            return self.monto_base * (1 - Decimal(beca.porcentaje_beca) / 100)
        except AlumnoBeca.DoesNotExist:
            # Si no hay beca, retorna el monto base
            return self.monto_base

    def calcular_total(self):
        """
        Calcula el total a pagar aplicando el interés por mora si está fuera de término.
        """
        monto_con_beca = self.calcular_monto_con_beca()

        # Si la cuota está fuera de término, aplica interés por mora
        if self.fuera_de_termino:
            self.total_a_pagar = monto_con_beca + (monto_con_beca * (self.interes_por_mora / 100))
        else:
            self.total_a_pagar = monto_con_beca

        return self.total_a_pagar

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para calcular los valores automáticamente antes de guardar.
        """
        # Determina si la cuota está fuera de término (después del día 10 del mes actual)
        hoy = date.today()
        if not self.pagada and hoy.day > 10:
            self.fuera_de_termino = True
            self.interes_por_mora = Decimal('10.0')  # 10% de interés por mora
        else:
            self.fuera_de_termino = False
            self.interes_por_mora = Decimal('0.0')

        # Calcula el monto final aplicando la beca y el total a pagar
        self.monto_final = self.calcular_monto_con_beca()
        self.calcular_total()

        # Guarda el objeto en la base de datos
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cuota - {self.estudiante} - {self.mes.nombre} ({self.mes.ciclo_lectivo.anio})"


    
class NivelEducativo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nivel Educativo")

    def __str__(self):
        return self.nombre


from django.utils import timezone

class MontosCicloLectivo(models.Model):
    ciclo_lectivo = models.ForeignKey(
        CicloLectivo, 
        on_delete=models.CASCADE, 
        related_name="montos"
    )
    nivel_educativo = models.ForeignKey(
        NivelEducativo, 
        on_delete=models.CASCADE, 
        related_name="montos"
    )
    monto_inscripcion = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Inscripción")
    monto_cuota = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Cuota")
    descuento_anticipado = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="Descuento por Pago Anticipado (%)", 
        default=0
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    activo = models.BooleanField(default=True, verbose_name="Monto Vigente")

    def save(self, *args, **kwargs):
        """
        Antes de guardar, desactiva otros montos activos del mismo ciclo lectivo y nivel educativo.
        """
        if self.activo:
            # Desactivar otros montos activos para el mismo ciclo lectivo y nivel educativo
            MontosCicloLectivo.objects.filter(
                ciclo_lectivo=self.ciclo_lectivo,
                nivel_educativo=self.nivel_educativo,
                activo=True
            ).exclude(id=self.id).update(activo=False)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ciclo_lectivo', 'nivel_educativo'],
                condition=models.Q(activo=True),
                name='unique_active_monto'
            )
        ]

    def __str__(self):
        return f"{self.nivel_educativo} - {self.ciclo_lectivo} - {'Activo' if self.activo else 'Inactivo'}"


from django.db import models
from apps.administracion_alumnos.models import Estudiante  # Importa el modelo Estudiante
from .models import NivelEducativo  # Importa el modelo NivelEducativo si está en la misma aplicación


class Preinscripcion(models.Model):
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, related_name="preinscripciones"
    )
    nivel_educativo = models.ForeignKey(
        NivelEducativo, on_delete=models.CASCADE
    )
    ciclo_lectivo = models.ForeignKey(
        CicloLectivo, on_delete=models.CASCADE
    )
    fecha_preinscripcion = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("estudiante", "ciclo_lectivo")  # Restricción de unicidad
        verbose_name = "Preinscripción"
        verbose_name_plural = "Preinscripciones"

    def __str__(self):
        return f"{self.estudiante} - {self.ciclo_lectivo.anio}"

    
from apps.administracion_alumnos.models import Estudiante

class AlumnoBeca(models.Model):
    estudiante = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE, 
        related_name="becas"
    )
    ciclo_lectivo = models.ForeignKey(
        CicloLectivo, 
        on_delete=models.CASCADE, 
        related_name="becas"
    )
    porcentaje_beca = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Porcentaje de Beca")

    def __str__(self):
        return f"{self.estudiante} - {self.ciclo_lectivo} - {self.porcentaje_beca}% Beca"


from django.db import models

class MesCicloLectivo(models.Model):
    ciclo_lectivo = models.ForeignKey(
        CicloLectivo,
        on_delete=models.CASCADE,
        related_name="meses"
    )
    nombre = models.CharField(max_length=20)  # Enero, Febrero, etc.

    def __str__(self):
        return f"{self.nombre} - {self.ciclo_lectivo.anio}"

    
