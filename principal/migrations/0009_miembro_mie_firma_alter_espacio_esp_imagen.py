# Generated by Django 4.0.6 on 2023-10-13 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0008_espacio_esp_imagen_alter_noticia_not_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='mie_firma',
            field=models.ImageField(null=True, upload_to='firmaPresidente/'),
        ),
        migrations.AlterField(
            model_name='espacio',
            name='esp_imagen',
            field=models.ImageField(null=True, upload_to='espacio/'),
        ),
    ]
