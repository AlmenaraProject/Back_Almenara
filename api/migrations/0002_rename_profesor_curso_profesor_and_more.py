# Generated by Django 4.2.4 on 2024-08-01 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='curso',
            old_name='Profesor',
            new_name='profesor',
        ),
        migrations.RenameField(
            model_name='especialidad',
            old_name='Coordinador',
            new_name='coordinador',
        ),
        migrations.RenameField(
            model_name='plan_trabajo',
            old_name='Universidad',
            new_name='universidad',
        ),
        migrations.RenameField(
            model_name='profesional',
            old_name='Usuario_modificacion',
            new_name='usuario_modificacion',
        ),
        migrations.RenameField(
            model_name='universidad',
            old_name='Coordinador',
            new_name='coordinador',
        ),
    ]