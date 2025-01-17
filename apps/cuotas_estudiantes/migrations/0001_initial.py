# Generated by Django 5.0.6 on 2024-12-16 13:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administracion_alumnos', '0010_alter_estudiante_sexo_estudiante'),
    ]

    operations = [
        migrations.CreateModel(
            name='CicloLectivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.PositiveIntegerField(unique=True, verbose_name='Año del Ciclo Lectivo')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de Inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de Fin')),
                ('habilitado', models.BooleanField(default=False, verbose_name='Habilitado')),
            ],
        ),
        migrations.CreateModel(
            name='NivelEducativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nivel Educativo')),
            ],
        ),
        migrations.CreateModel(
            name='AlumnoBeca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('porcentaje_beca', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Porcentaje de Beca')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='becas', to='administracion_alumnos.estudiante')),
                ('ciclo_lectivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='becas', to='cuotas_estudiantes.ciclolectivo')),
            ],
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateField(default=django.utils.timezone.now)),
                ('monto_inscripcion', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pagada', models.BooleanField(default=False)),
                ('ciclo_lectivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='cuotas_estudiantes.ciclolectivo')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='administracion_alumnos.estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='MesCicloLectivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('habilitado', models.BooleanField(default=True)),
                ('ciclo_lectivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meses', to='cuotas_estudiantes.ciclolectivo')),
            ],
        ),
        migrations.CreateModel(
            name='Cuota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_base', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto Base')),
                ('monto_final', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Monto Final (Con Interés o Beca)')),
                ('fecha_pago', models.DateField(blank=True, null=True, verbose_name='Fecha de Pago')),
                ('pagada', models.BooleanField(default=False, verbose_name='Pagada')),
                ('fuera_de_termino', models.BooleanField(default=False, verbose_name='Fuera de Término')),
                ('interes_por_mora', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Interés por Mora (%)')),
                ('total_a_pagar', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total a Pagar')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuotas', to='administracion_alumnos.estudiante')),
                ('mes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuotas', to='cuotas_estudiantes.mesciclolectivo')),
            ],
        ),
        migrations.CreateModel(
            name='MontosCicloLectivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_inscripcion', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto Inscripción')),
                ('monto_cuota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto Cuota')),
                ('descuento_anticipado', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Descuento por Pago Anticipado (%)')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('activo', models.BooleanField(default=True, verbose_name='Monto Vigente')),
                ('ciclo_lectivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='montos', to='cuotas_estudiantes.ciclolectivo')),
                ('nivel_educativo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='montos', to='cuotas_estudiantes.niveleducativo')),
            ],
        ),
        migrations.CreateModel(
            name='Preinscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_preinscripcion', models.DateField(auto_now_add=True)),
                ('estudiante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preinscripcion', to='administracion_alumnos.estudiante')),
                ('nivel_educativo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuotas_estudiantes.niveleducativo')),
            ],
        ),
        migrations.AddConstraint(
            model_name='montosciclolectivo',
            constraint=models.UniqueConstraint(condition=models.Q(('activo', True)), fields=('ciclo_lectivo', 'nivel_educativo'), name='unique_active_monto'),
        ),
    ]
