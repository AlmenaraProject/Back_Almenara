# Generated by Django 4.2.4 on 2024-07-24 16:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_especialidad_coordinador'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinador',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('documento', models.CharField(max_length=250, null=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='especialidad',
            name='coordinador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.coordinador'),
        ),
        migrations.AlterField(
            model_name='universidad',
            name='coordinador_general',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.coordinador'),
        ),
    ]