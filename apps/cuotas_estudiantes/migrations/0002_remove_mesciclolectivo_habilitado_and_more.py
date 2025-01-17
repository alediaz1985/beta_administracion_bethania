# Generated by Django 5.0.6 on 2024-12-16 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion_alumnos', '0010_alter_estudiante_sexo_estudiante'),
        ('cuotas_estudiantes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mesciclolectivo',
            name='habilitado',
        ),
        migrations.AddField(
            model_name='inscripcion',
            name='descuento',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Descuento (%)'),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='estudiante',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inscripcion', to='administracion_alumnos.estudiante'),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='fecha_inscripcion',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='pagada',
            field=models.BooleanField(default=False, verbose_name='Pagada'),
        ),
    ]
