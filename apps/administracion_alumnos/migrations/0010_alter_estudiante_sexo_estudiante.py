# Generated by Django 5.0.6 on 2024-12-15 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion_alumnos', '0009_alter_estudiante_marca_temporal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='sexo_estudiante',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M', max_length=50),
        ),
    ]
