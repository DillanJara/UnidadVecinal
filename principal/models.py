from django.db import models


class Cargo(models.Model):
    car_id     = models.AutoField(primary_key=True)
    car_nombre = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.car_nombre


class Comuna(models.Model):
    com_id     = models.AutoField(primary_key=True)
    com_nombre = models.CharField(max_length=30)
    region_reg = models.ForeignKey('Region', models.CASCADE, db_column='REGION_reg_id')


class CuotaSocial(models.Model):
    cuo_id          = models.AutoField(primary_key=True)
    cuo_monto       = models.IntegerField()
    cuo_fecha_pago  = models.DateField()
    cuo_estado      = models.CharField(max_length=30)
    miembro_mie     = models.ForeignKey('Miembro', models.CASCADE, db_column='MIEMBRO_mie_rut')


class Espacio(models.Model):
    esp_id            = models.AutoField(primary_key=True)
    esp_nombre        = models.CharField(max_length=30)
    esp_direccion     = models.CharField(max_length=50)
    esp_telefono      = models.CharField(max_length=12)
    esp_imagen        = models.ImageField(upload_to="media/espacio/", null=True)
    junta_vecinos_jun = models.ForeignKey('JuntaVecinos', models.CASCADE, db_column='JUNTA_VECINOS_jun_id')


class EstadoProyecto(models.Model):
    est_proy_id     = models.AutoField(primary_key=True)
    est_proy_estado = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.est_proy_estado


class FamiliarMiembro(models.Model):
    fam_mie_rut        = models.IntegerField(primary_key=True)
    fam_mie_dv         = models.CharField(max_length=1)
    fam_mie_nombre     = models.CharField(max_length=30)
    fam_mie_ap_paterno = models.CharField(max_length=30)
    fam_mie_ap_materno = models.CharField(max_length=30)
    fam_mie_telefono   = models.CharField(max_length=12)
    fam_mie_parentesco = models.CharField(max_length=30)
    miembro_mie        = models.ForeignKey('Miembro', models.CASCADE, db_column='MIEMBRO_mie_rut')


class JuntaVecinos(models.Model):
    jun_id                   = models.AutoField(primary_key=True)
    jun_rol_municipal        = models.PositiveIntegerField()
    jun_nombre               = models.CharField(max_length=50)
    jun_fecha_fundacion      = models.DateField()
    jun_nombre_villa         = models.CharField(max_length=30)
    jun_telefono             = models.CharField(unique=True, max_length=12)
    jun_correo               = models.CharField(unique=True, max_length=254)
    jun_direccion            = models.CharField(max_length=50)
    jun_mision               = models.CharField(max_length=300, null=True)
    jun_habilitada           = models.BooleanField(default=False)
    jun_certificado_vigencia = models.ImageField(upload_to="media/juntaVecinos/", blank=True)
    jun_directiva            = models.CharField(max_length=300)
    comuna_com               = models.ForeignKey(Comuna, models.CASCADE, db_column='COMUNA_com_id')


class Miembro(models.Model):
    mie_rut              = models.IntegerField(primary_key=True,)
    mie_dv               = models.CharField(max_length=1)
    mie_nombre           = models.CharField(max_length=30)
    mie_ap_paterno       = models.CharField(max_length=30)
    mie_ap_materno       = models.CharField(max_length=30)
    mie_fecha_nacimiento = models.DateField()
    mie_telefono         = models.CharField(unique=True, max_length=12)
    mie_correo           = models.CharField(unique=True, max_length=254)
    mie_password         = models.CharField(max_length=150)
    mie_direccion        = models.CharField(max_length=50)
    mie_estado           = models.CharField(max_length=30, default="Deshabilitado")
    junta_vecinos_jun    = models.ForeignKey(JuntaVecinos, on_delete=models.CASCADE, db_column='JUNTA_VECINOS_jun_id')
    cargo_car            = models.ForeignKey(Cargo, on_delete=models.CASCADE, db_column='CARGO_car_id')
    mie_firma            = models.CharField(max_length=50000, null=True)
    mie_documento        = models.ImageField(upload_to="media/miembro/")


class Noticia(models.Model):
    not_id          = models.AutoField(primary_key=True)
    not_titulo      = models.CharField(max_length=50)
    not_subtitulo   = models.CharField(max_length=100)
    not_fecha       = models.DateField(auto_now_add=True)
    not_descripcion = models.CharField(max_length=300)
    not_imagen      = models.ImageField(upload_to="media/noticia/", null=True)
    miembro_mie     = models.ForeignKey(Miembro, models.CASCADE, db_column='MIEMBRO_mie_rut')


class Proyecto(models.Model):
    proy_id                  = models.AutoField(primary_key=True)
    proy_nombre              = models.CharField(max_length=30)
    proy_descripcion         = models.CharField(max_length=300)
    proy_imagen              = models.ImageField(upload_to="media/proyecto/")
    estado_proyecto_est_proy = models.ForeignKey(EstadoProyecto, models.CASCADE, db_column='ESTADO_PROYECTO_est_proy_id')
    miembro_mie              = models.ForeignKey(Miembro, models.CASCADE, db_column='MIEMBRO_mie_rut')


class Region(models.Model):
    reg_id     = models.AutoField(primary_key=True)
    reg_nombre = models.CharField(max_length=50)


class Reserva(models.Model):
    res_id          = models.AutoField(primary_key=True)
    res_fecha       = models.DateField()
    res_hora_inicio = models.TimeField()
    res_hora_fin    = models.TimeField()
    miembro_mie     = models.ForeignKey(Miembro, models.CASCADE, db_column='MIEMBRO_mie_rut')
    espacio_esp     = models.ForeignKey(Espacio, models.CASCADE, db_column='ESPACIO_esp_id')


class TipoActividad(models.Model):
    tip_act_id     = models.AutoField(primary_key=True)
    tip_act_nombre = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.tip_act_nombre


class Certificado(models.Model):
    cer_id     = models.AutoField(primary_key=True)
    cer_nombre = models.CharField(max_length=50, default="")


class SolicitudCertificado(models.Model):
    sol_cer_id           = models.AutoField(primary_key=True)
    sol_cer_fecha        = models.DateField(auto_now_add=True, blank=True)
    miembro_mie          = models.ForeignKey(Miembro, models.CASCADE, db_column='MIEMBRO_mie_rut')
    certificado_cer      = models.ForeignKey(Certificado, models.CASCADE, db_column='CERTIFICADO_cer_id')
    sol_cer_familiar     = models.BooleanField(default=False)
    sol_cer_rut_familiar = models.IntegerField(null=True)


class Actividad(models.Model):
    act_id                 = models.AutoField(primary_key=True)
    act_fecha              = models.DateField()
    act_descripcion        = models.CharField(max_length=30)
    act_cupo               = models.IntegerField()
    act_cuota              = models.IntegerField(default=0, null=True)
    tipo_actividad_tip_act = models.ForeignKey('TipoActividad', models.CASCADE, db_column='TIPO_ACTIVIDAD_tip_act_id')
    junta_vecinos_jun      = models.ForeignKey('JuntaVecinos', on_delete=models.CASCADE, db_column='JUNTA_VECINOS_jun_id')


class Asistencia(models.Model):
    asis_id         = models.AutoField(primary_key=True)
    asis_cantidad   = models.IntegerField(default=1)
    actividad_act   = models.ForeignKey(Actividad, models.CASCADE, db_column='ACTIVIDAD_act_id')
    miembro_mie     = models.ForeignKey('Miembro', models.CASCADE, db_column='MIEMBRO_mie_rut')