# Generated by Django 2.1.1 on 2018-10-09 13:03

import apps.persona.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to=apps.persona.models.url_upload_to)),
            ],
            options={
                'verbose_name': 'Imágen',
                'verbose_name_plural': 'Imágenes',
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellido', models.CharField(max_length=200)),
                ('nombre', models.CharField(max_length=200)),
                ('cuil', models.CharField(max_length=15)),
                ('dni', models.CharField(max_length=10)),
                ('legajo', models.IntegerField()),
            ],
            options={
                'ordering': ('apellido', 'nombre'),
            },
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('nombre_seccion', models.CharField(max_length=100)),
                ('orden', models.IntegerField()),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seccion_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seccion_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sección',
                'verbose_name_plural': 'Secciones',
                'ordering': ('orden',),
            },
        ),
        migrations.AddField(
            model_name='imagen',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.Persona'),
        ),
        migrations.AddField(
            model_name='imagen',
            name='seccion',
            field=models.ForeignKey(on_delete=models.SET(apps.persona.models.default_seccion), to='persona.Seccion'),
        ),
    ]
