# Generated by Django 4.0.6 on 2023-10-30 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0019_remove_miembro_mie_estado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='mie_estado',
            field=models.CharField(default='Deshabilitado', max_length=30),
        ),
    ]