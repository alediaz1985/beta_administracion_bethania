# Generated by Django 5.0.6 on 2024-12-12 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion_alumnos', '0006_alter_estudiante_sexo_estudiante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='autoriza_imagen',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='foto_estudiante',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
