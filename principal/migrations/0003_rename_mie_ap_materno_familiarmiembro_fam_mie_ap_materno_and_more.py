# Generated by Django 4.0.6 on 2023-09-29 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_rename_mie_fecha_nacimento_miembro_mie_fecha_nacimiento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='familiarmiembro',
            old_name='mie_ap_materno',
            new_name='fam_mie_ap_materno',
        ),
        migrations.RenameField(
            model_name='familiarmiembro',
            old_name='mie_ap_paterno',
            new_name='fam_mie_ap_paterno',
        ),
        migrations.RenameField(
            model_name='familiarmiembro',
            old_name='mie_dv',
            new_name='fam_mie_dv',
        ),
        migrations.RenameField(
            model_name='familiarmiembro',
            old_name='mie_nombre',
            new_name='fam_mie_nombre',
        ),
        migrations.RenameField(
            model_name='familiarmiembro',
            old_name='parentesco',
            new_name='fam_mie_parentesco',
        ),
        migrations.RenameField(
            model_name='familiarmiembro',
            old_name='mie_telefono',
            new_name='fam_mie_telefono',
        ),
    ]
