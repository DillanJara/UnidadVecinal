# Generated by Django 4.0.6 on 2023-11-23 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0024_asistencia_asis_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='junta_vecinos_jun',
            field=models.ForeignKey(db_column='JUNTA_VECINOS_jun_id', on_delete=django.db.models.deletion.CASCADE, to='principal.juntavecinos'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='tipo_actividad_tip_act',
            field=models.ForeignKey(db_column='TIPO_ACTIVIDAD_tip_act_id', on_delete=django.db.models.deletion.CASCADE, to='principal.tipoactividad'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='actividad_act',
            field=models.ForeignKey(db_column='ACTIVIDAD_act_id', on_delete=django.db.models.deletion.CASCADE, to='principal.actividad'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='miembro_mie',
            field=models.ForeignKey(db_column='MIEMBRO_mie_rut', on_delete=django.db.models.deletion.CASCADE, to='principal.miembro'),
        ),
        migrations.AlterField(
            model_name='comuna',
            name='region_reg',
            field=models.ForeignKey(db_column='REGION_reg_id', on_delete=django.db.models.deletion.CASCADE, to='principal.region'),
        ),
        migrations.AlterField(
            model_name='cuotasocial',
            name='miembro_mie',
            field=models.ForeignKey(db_column='MIEMBRO_mie_rut', on_delete=django.db.models.deletion.CASCADE, to='principal.miembro'),
        ),
        migrations.AlterField(
            model_name='espacio',
            name='junta_vecinos_jun',
            field=models.ForeignKey(db_column='JUNTA_VECINOS_jun_id', on_delete=django.db.models.deletion.CASCADE, to='principal.juntavecinos'),
        ),
        migrations.AlterField(
            model_name='familiarmiembro',
            name='miembro_mie',
            field=models.ForeignKey(db_column='MIEMBRO_mie_rut', on_delete=django.db.models.deletion.CASCADE, to='principal.miembro'),
        ),
        migrations.AlterField(
            model_name='juntavecinos',
            name='comuna_com',
            field=models.ForeignKey(db_column='COMUNA_com_id', on_delete=django.db.models.deletion.CASCADE, to='principal.comuna'),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='cargo_car',
            field=models.ForeignKey(db_column='CARGO_car_id', on_delete=django.db.models.deletion.CASCADE, to='principal.cargo'),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='junta_vecinos_jun',
            field=models.ForeignKey(db_column='JUNTA_VECINOS_jun_id', on_delete=django.db.models.deletion.CASCADE, to='principal.juntavecinos'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='miembro_mie',
            field=models.ForeignKey(db_column='MIEMBRO_mie_rut', on_delete=django.db.models.deletion.CASCADE, to='principal.miembro'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='estado_proyecto_est_proy',
            field=models.ForeignKey(db_column='ESTADO_PROYECTO_est_proy_id', on_delete=django.db.models.deletion.CASCADE, to='principal.estadoproyecto'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='miembro_mie',
            field=models.ForeignKey(db_column='MIEMBRO_mie_rut', on_delete=django.db.models.deletion.CASCADE, to='principal.miembro'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='espacio_esp',
            field=models.ForeignKey(db_column='ESPACIO_esp_id', on_delete=django.db.models.deletion.CASCADE, to='principal.espacio'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='miembro_mie',
            field=models.ForeignKey(db_column='MIEMBRO_mie_rut', on_delete=django.db.models.deletion.CASCADE, to='principal.miembro'),
        ),
        migrations.AlterField(
            model_name='solicitudcertificado',
            name='certificado_cer',
            field=models.ForeignKey(db_column='CERTIFICADO_cer_id', on_delete=django.db.models.deletion.CASCADE, to='principal.certificado'),
        ),
        migrations.AlterField(
            model_name='solicitudcertificado',
            name='miembro_mie',
            field=models.ForeignKey(db_column='MIEMBRO_mie_rut', on_delete=django.db.models.deletion.CASCADE, to='principal.miembro'),
        ),
    ]
