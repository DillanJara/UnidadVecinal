# Generated by Django 4.0.6 on 2023-10-16 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0011_miembro_mie_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='espacio',
            name='esp_imagen',
            field=models.ImageField(null=True, upload_to='`media/espacio/'),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='mie_documento',
            field=models.ImageField(upload_to='media/miembro/'),
        ),
    ]
