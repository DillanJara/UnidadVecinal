# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import RegexValidator


class Actividad(models.Model):
    act_id = models.AutoField(primary_key=True)
    act_fecha = models.DateField()
    act_descripcion = models.CharField(max_length=30)
    act_cupo = models.IntegerField()
    act_imagen = models.CharField(max_length=300)
    act_cuota = models.IntegerField(blank=True, null=True)
    tipo_actividad_tip_act = models.ForeignKey('TipoActividad', on_delete=models.PROTECT, db_column='TIPO_ACTIVIDAD_tip_act_id')  # Field name made lowercase.
    administrador_adm = models.ForeignKey('Administrador', on_delete=models.PROTECT, db_column='ADMINISTRADOR_adm_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'actividad'


class Administrador(models.Model):
    adm_id = models.AutoField(primary_key=True)
    adm_nombre = models.CharField(max_length=30)
    miembro_mie_rut = models.OneToOneField('Miembro', on_delete=models.PROTECT, db_column='MIEMBRO_mie_rut')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'administrador'


class Asistencia(models.Model):
    asis_id = models.AutoField(primary_key=True)
    actividad_act = models.ForeignKey(Actividad, on_delete=models.PROTECT, db_column='ACTIVIDAD_act_id')  # Field name made lowercase.
    miembro_mie_rut = models.ForeignKey('Miembro', on_delete=models.PROTECT, db_column='MIEMBRO_mie_rut')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asistencia'


class Certificado(models.Model):
    cer_id = models.AutoField(primary_key=True)
    cer_nombre = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'certificado'


class Comuna(models.Model):
    com_id = models.AutoField(primary_key=True)
    com_nombre = models.CharField(max_length=30)
    region_reg = models.ForeignKey('Region', on_delete=models.PROTECT, db_column='REGION_reg_id')  # Field name made lowercase.

    def __str__(self) -> str:
        return self.com_nombre

    class Meta:
        managed = False
        db_table = 'comuna'


class CuotaSocial(models.Model):
    cuo_id = models.AutoField(primary_key=True)
    cuo_monto = models.IntegerField()
    cuo_fecha_pago = models.DateField()
    cuo_estado = models.CharField(max_length=30)
    miembro_mie_rut = models.ForeignKey('Miembro', on_delete=models.PROTECT, db_column='MIEMBRO_mie_rut')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cuota_social'


class Espacio(models.Model):
    esp_id = models.AutoField(primary_key=True)
    esp_nombre = models.CharField(max_length=30)
    esp_direccion = models.CharField(max_length=100)
    esp_telefono = models.CharField(max_length=12)
    junta_vecinos_jun = models.ForeignKey('JuntaVecinos', on_delete=models.PROTECT, db_column='JUNTA_VECINOS_jun_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'espacio'


class EstadoProyecto(models.Model):
    est_proy_id = models.AutoField(primary_key=True)
    est_proy_estado = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'estado_proyecto'


class FamiliarMiembro(models.Model):
    fam_mie_rut = models.IntegerField(primary_key=True)
    fam_mie_dv = models.CharField(max_length=1)
    fam_mie_nombre = models.CharField(max_length=30)
    fam_mie_ap_paterno = models.CharField(max_length=30)
    fam_mie_ap_materno = models.CharField(max_length=30)
    fam_mie_telefono_formato = RegexValidator(regex=r'^\+569\d{8}$', message='El numero debe estar en formato +56 9 1234 5678')
    fam_mie_telefono = models.CharField(validators=[fam_mie_telefono_formato], max_length=12, blank=True)
    fam_mie_parentesco = models.CharField(max_length=30)
    miembro_mie_rut = models.ForeignKey('Miembro', on_delete=models.PROTECT, db_column='MIEMBRO_mie_rut')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'familiar_miembro'


class JuntaVecinos(models.Model):
    jun_id = models.AutoField(primary_key=True)
    jun_nombre = models.CharField(max_length=50)
    jun_fecha_fundacion = models.DateField()
    jun_nombre_villa = models.CharField(max_length=30)
    jun_telefono_formato = RegexValidator(regex=r'^\+569\d{8}$', message='El numero debe estar en formato +56 9 1234 5678')
    jun_telefono = models.CharField(validators=[jun_telefono_formato], max_length=12, blank=True)
    jun_correo = models.EmailField(max_length=254)
    jun_direccion = models.CharField(max_length=100)
    jun_mision = models.CharField(max_length=300)
    comuna_com_id = models.ForeignKey(Comuna, on_delete=models.PROTECT, db_column='COMUNA_com_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'junta_vecinos'


class Miembro(models.Model):
    mie_rut = models.IntegerField(primary_key=True)
    mie_dv_formato = RegexValidator(r'^[0-9kK]$', message='Ingrese un digito verificador valido')
    mie_dv = models.CharField(validators=[mie_dv_formato], max_length=1)
    mie_nombre = models.CharField(max_length=30)
    mie_ap_paterno = models.CharField(max_length=30)
    mie_ap_materno = models.CharField(max_length=30)
    mie_fecha_nacimento = models.DateField()
    mie_telefono_formato = RegexValidator(regex=r'^\+569\d{8}$', message='El numero debe estar en formato +56 9 1234 5678')
    mie_telefono = models.CharField(validators=[mie_telefono_formato], max_length=12, blank=True)
    mie_correo = models.EmailField(max_length=254)
    mie_password = models.CharField(max_length=300)
    mie_direccion = models.CharField(max_length=100)
    junta_vecinos_jun = models.ForeignKey(JuntaVecinos, on_delete=models.PROTECT, db_column='JUNTA_VECINOS_jun_id')  # Field name made lowercase.
    mie_estado = models.CharField(max_length=30, default="Inhabilitado")

    class Meta:
        managed = False
        db_table = 'miembro'


class Noticia(models.Model):
    not_id = models.AutoField(primary_key=True)
    not_titulo = models.CharField(max_length=50)
    not_subtitulo = models.CharField(max_length=100)
    not_fecha = models.DateField()
    not_descripcion = models.CharField(max_length=300)
    not_imagen = models.CharField(max_length=300)
    actividad_act = models.ForeignKey(Actividad, on_delete=models.PROTECT, db_column='ACTIVIDAD_act_id', blank=True, null=True)  # Field name made lowercase.
    proyecto_proy = models.ForeignKey('Proyecto', on_delete=models.PROTECT, db_column='PROYECTO_proy_id', blank=True, null=True)  # Field name made lowercase.
    administrador_adm = models.ForeignKey(Administrador, on_delete=models.PROTECT, db_column='ADMINISTRADOR_adm_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'noticia'


class Proyecto(models.Model):
    proy_id = models.AutoField(primary_key=True)
    proy_nombre = models.CharField(max_length=30)
    proy_descripcion = models.CharField(max_length=300)
    proy_imagen = models.CharField(max_length=300)
    estado_proyecto_est_proy = models.ForeignKey(EstadoProyecto, on_delete=models.PROTECT, db_column='ESTADO_PROYECTO_est_proy_id')  # Field name made lowercase.
    miembro_mie_rut = models.ForeignKey(Miembro, on_delete=models.PROTECT, db_column='MIEMBRO_mie_rut')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'proyecto'


class Region(models.Model):
    reg_id = models.AutoField(primary_key=True)
    reg_nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'region'


class Reserva(models.Model):
    res_id = models.AutoField(primary_key=True)
    res_fecha_hora = models.DateTimeField()
    miembro_mie_rut = models.ForeignKey(Miembro, on_delete=models.PROTECT, db_column='MIEMBRO_mie_rut')  # Field name made lowercase.
    espacio_esp = models.ForeignKey(Espacio, on_delete=models.PROTECT, db_column='ESPACIO_esp_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reserva'


class SolicitudCertificado(models.Model):
    sol_cer_id = models.AutoField(primary_key=True)
    sol_cer_fecha = models.DateField()
    miembro_mie_rut = models.ForeignKey(Miembro, on_delete=models.PROTECT, db_column='MIEMBRO_mie_rut')  # Field name made lowercase.
    certificado_cer = models.ForeignKey(Certificado, on_delete=models.PROTECT, db_column='CERTIFICADO_cer_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'solicitud_certificado'


class TipoActividad(models.Model):
    tip_act_id = models.AutoField(primary_key=True)
    tip_act_nombre = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tipo_actividad'
