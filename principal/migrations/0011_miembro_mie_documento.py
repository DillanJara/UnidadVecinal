# Generated by Django 4.0.6 on 2023-10-16 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0010_alter_miembro_mie_firma'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='mie_documento',
            field=models.ImageField(default='No hay archivo', upload_to=''),
        ),
    ]
