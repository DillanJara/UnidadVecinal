# Generated by Django 4.0.6 on 2023-10-06 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_alter_proyecto_proy_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='espacio',
            name='esp_imagen',
            field=models.ImageField(null=True, upload_to='media/espacio/'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='not_imagen',
            field=models.ImageField(upload_to='media/noticia/'),
        ),
    ]
