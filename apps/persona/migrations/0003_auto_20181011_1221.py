# Generated by Django 2.1.1 on 2018-10-11 15:21

import apps.persona.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20181011_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagen',
            name='fecha_subida',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imagen',
            name='persona',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='persona.Persona'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imagen',
            name='seccion',
            field=models.ForeignKey(default=1, on_delete=models.SET(apps.persona.models.default_seccion), to='persona.Seccion'),
            preserve_default=False,
        ),
    ]
