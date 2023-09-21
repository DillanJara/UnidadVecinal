-- Generado por Oracle SQL Developer Data Modeler 19.4.0.350.1424
--   en:        2023-09-20 17:36:28 CLST
--   sitio:      Oracle Database 11g
--   tipo:      Oracle Database 11g



-- Generado por Oracle SQL Developer Data Modeler 19.4.0.350.1424
--   en:        2023-09-20 17:36:28 CLST
--   sitio:      Oracle Database 11g
--   tipo:      Oracle Database 11g



CREATE TABLE actividad (
    act_id                     INTEGER NOT NULL,
    act_fecha                  DATE NOT NULL,
    act_descripcion            VARCHAR2(30) NOT NULL,
    act_cupo                   INTEGER NOT NULL,
    act_imagen                 VARCHAR2(300) NOT NULL,
    act_cuota                  INTEGER,
    tipo_actividad_tip_act_id  INTEGER NOT NULL,
    administrador_adm_id       INTEGER NOT NULL
);

ALTER TABLE actividad ADD CONSTRAINT actividad_pk PRIMARY KEY ( act_id );

CREATE TABLE administrador (
    adm_id           INTEGER NOT NULL,
    adm_nombre       VARCHAR2(30) NOT NULL,
    miembro_mie_rut  INTEGER NOT NULL
);

CREATE UNIQUE INDEX administrador__idx ON
    administrador (
        miembro_mie_rut
    ASC );

ALTER TABLE administrador ADD CONSTRAINT administrador_pk PRIMARY KEY ( adm_id );

CREATE TABLE asistencia (
    asis_id           INTEGER NOT NULL,
    actividad_act_id  INTEGER NOT NULL,
    miembro_mie_rut   INTEGER NOT NULL
);

ALTER TABLE asistencia ADD CONSTRAINT asistencia_pk PRIMARY KEY ( asis_id );

CREATE TABLE certificado (
    cer_id      INTEGER NOT NULL,
    cer_nombre  INTEGER NOT NULL
);

ALTER TABLE certificado ADD CONSTRAINT certificado_pk PRIMARY KEY ( cer_id );

CREATE TABLE comuna (
    com_id         INTEGER NOT NULL,
    com_nombre     VARCHAR2(30) NOT NULL,
    region_reg_id  INTEGER NOT NULL
);

ALTER TABLE comuna ADD CONSTRAINT comuna_pk PRIMARY KEY ( com_id );

CREATE TABLE cuota_social (
    cuo_id           INTEGER NOT NULL,
    cuo_monto        INTEGER NOT NULL,
    cuo_fecha_pago   DATE NOT NULL,
    cuo_estado       VARCHAR2(30) NOT NULL,
    miembro_mie_rut  INTEGER NOT NULL
);

ALTER TABLE cuota_social ADD CONSTRAINT cuota_social_pk PRIMARY KEY ( cuo_id );

CREATE TABLE espacio (
    esp_id                INTEGER NOT NULL,
    esp_nombre            VARCHAR2(30) NOT NULL,
    esp_direccion         VARCHAR2(50) NOT NULL,
    esp_telefono          VARCHAR2(12) NOT NULL,
    junta_vecinos_jun_id  INTEGER NOT NULL
);

ALTER TABLE espacio ADD CONSTRAINT espacio_pk PRIMARY KEY ( esp_id );

CREATE TABLE estado_proyecto (
    est_proy_id      INTEGER NOT NULL,
    est_proy_estado  VARCHAR2(30) NOT NULL
);

ALTER TABLE estado_proyecto ADD CONSTRAINT estado_proyecto_pk PRIMARY KEY ( est_proy_id );

CREATE TABLE familiar_miembro (
    fam_mie_rut      INTEGER NOT NULL,
    mie_dv           CHAR 
--  WARNING: CHAR size not specified 
     NOT NULL,
    mie_nombre       VARCHAR2(30) NOT NULL,
    mie_ap_paterno   VARCHAR2(30) NOT NULL,
    mie_ap_materno   VARCHAR2(30) NOT NULL,
    mie_telefono     VARCHAR2(12) NOT NULL,
    parentesco       VARCHAR2(30) NOT NULL,
    miembro_mie_rut  INTEGER NOT NULL
);

ALTER TABLE familiar_miembro ADD CONSTRAINT familiar_miembro_pk PRIMARY KEY ( fam_mie_rut );

CREATE TABLE junta_vecinos (
    jun_id               INTEGER NOT NULL,
    jun_nombre           VARCHAR2(50) NOT NULL,
    jun_fecha_fundacion  DATE NOT NULL,
    jun_nombre_villa     VARCHAR2(30) NOT NULL,
    jun_telefono         VARCHAR2(12) NOT NULL,
    jun_correo           VARCHAR2(50) NOT NULL,
    jun_direccion        VARCHAR2(50) NOT NULL,
    jun_mision           VARCHAR2(300) NOT NULL,
    comuna_com_id        INTEGER NOT NULL
);

ALTER TABLE junta_vecinos ADD CONSTRAINT junta_vecinos_pk PRIMARY KEY ( jun_id );

ALTER TABLE junta_vecinos ADD CONSTRAINT junta_vecinos_jun_telefono_un UNIQUE ( jun_telefono );

ALTER TABLE junta_vecinos ADD CONSTRAINT junta_vecinos_jun_correo_un UNIQUE ( jun_correo );

CREATE TABLE miembro (
    mie_rut               INTEGER NOT NULL,
    mie_dv                VARCHAR2(1) NOT NULL,
    mie_nombre            VARCHAR2(30) NOT NULL,
    mie_ap_paterno        VARCHAR2(30) NOT NULL,
    mie_ap_materno        VARCHAR2(30) NOT NULL,
    mie_fecha_nacimento   DATE NOT NULL,
    mie_telefono          VARCHAR2(12) NOT NULL,
    mie_correo            VARCHAR2(50) NOT NULL,
    mie_password          VARCHAR2(50) NOT NULL,
    mie_direccion         VARCHAR2(30) NOT NULL,
    junta_vecinos_jun_id  INTEGER NOT NULL,
    mie_estado            VARCHAR2(30) NOT NULL
);

ALTER TABLE miembro ADD CONSTRAINT miembro_pk PRIMARY KEY ( mie_rut );

ALTER TABLE miembro ADD CONSTRAINT miembro_mie_telefono_un UNIQUE ( mie_telefono );

ALTER TABLE miembro ADD CONSTRAINT miembro_mie_correo_un UNIQUE ( mie_correo );

CREATE TABLE noticia (
    not_id                INTEGER NOT NULL,
    not_titulo            VARCHAR2(50) NOT NULL,
    not_subtitulo         VARCHAR2(100) NOT NULL,
    not_fecha             DATE NOT NULL,
    not_descripcion       VARCHAR2(300) NOT NULL,
    not_imagen            VARCHAR2(300) NOT NULL,
    actividad_act_id      INTEGER,
    proyecto_proy_id      INTEGER,
    administrador_adm_id  INTEGER NOT NULL
);

ALTER TABLE noticia
    ADD CONSTRAINT arc_2 CHECK ( ( ( proyecto_proy_id IS NOT NULL )
                                   AND ( actividad_act_id IS NULL ) )
                                 OR ( ( actividad_act_id IS NOT NULL )
                                      AND ( proyecto_proy_id IS NULL ) )
                                 OR ( ( proyecto_proy_id IS NULL )
                                      AND ( actividad_act_id IS NULL ) ) );

ALTER TABLE noticia ADD CONSTRAINT noticia_pk PRIMARY KEY ( not_id );

CREATE TABLE proyecto (
    proy_id                      INTEGER NOT NULL,
    proy_nombre                  VARCHAR2(30) NOT NULL,
    proy_descripcion             VARCHAR2(300) NOT NULL,
    proy_imagen                  VARCHAR2(300) NOT NULL,
    estado_proyecto_est_proy_id  INTEGER NOT NULL,
    miembro_mie_rut              INTEGER NOT NULL
);

ALTER TABLE proyecto ADD CONSTRAINT proyecto_pk PRIMARY KEY ( proy_id );

CREATE TABLE region (
    reg_id      INTEGER NOT NULL,
    reg_nombre  VARCHAR2(50) NOT NULL
);

ALTER TABLE region ADD CONSTRAINT region_pk PRIMARY KEY ( reg_id );

CREATE TABLE reserva (
    res_id           INTEGER NOT NULL,
    res_fecha_hora   DATE NOT NULL,
    miembro_mie_rut  INTEGER NOT NULL,
    espacio_esp_id   INTEGER NOT NULL
);

ALTER TABLE reserva ADD CONSTRAINT reserva_pk PRIMARY KEY ( res_id );

CREATE TABLE solicitud_certificado (
    sol_cer_id          INTEGER NOT NULL,
    sol_cer_fecha       DATE NOT NULL,
    miembro_mie_rut     INTEGER NOT NULL,
    certificado_cer_id  INTEGER NOT NULL
);

ALTER TABLE solicitud_certificado ADD CONSTRAINT solicitud_certificado_pk PRIMARY KEY ( sol_cer_id );

CREATE TABLE tipo_actividad (
    tip_act_id      INTEGER NOT NULL,
    tip_act_nombre  VARCHAR2(30) NOT NULL
);

ALTER TABLE tipo_actividad ADD CONSTRAINT tipo_actividad_pk PRIMARY KEY ( tip_act_id );

ALTER TABLE actividad
    ADD CONSTRAINT actividad_administrador_fk FOREIGN KEY ( administrador_adm_id )
        REFERENCES administrador ( adm_id );

ALTER TABLE actividad
    ADD CONSTRAINT actividad_tipo_actividad_fk FOREIGN KEY ( tipo_actividad_tip_act_id )
        REFERENCES tipo_actividad ( tip_act_id );

ALTER TABLE administrador
    ADD CONSTRAINT administrador_miembro_fk FOREIGN KEY ( miembro_mie_rut )
        REFERENCES miembro ( mie_rut );

ALTER TABLE asistencia
    ADD CONSTRAINT asistencia_actividad_fk FOREIGN KEY ( actividad_act_id )
        REFERENCES actividad ( act_id );

ALTER TABLE asistencia
    ADD CONSTRAINT asistencia_miembro_fk FOREIGN KEY ( miembro_mie_rut )
        REFERENCES miembro ( mie_rut );

ALTER TABLE comuna
    ADD CONSTRAINT comuna_region_fk FOREIGN KEY ( region_reg_id )
        REFERENCES region ( reg_id );

ALTER TABLE cuota_social
    ADD CONSTRAINT cuota_social_miembro_fk FOREIGN KEY ( miembro_mie_rut )
        REFERENCES miembro ( mie_rut );

ALTER TABLE espacio
    ADD CONSTRAINT espacio_junta_vecinos_fk FOREIGN KEY ( junta_vecinos_jun_id )
        REFERENCES junta_vecinos ( jun_id );

ALTER TABLE familiar_miembro
    ADD CONSTRAINT familiar_miembro_miembro_fk FOREIGN KEY ( miembro_mie_rut )
        REFERENCES miembro ( mie_rut );

ALTER TABLE junta_vecinos
    ADD CONSTRAINT junta_vecinos_comuna_fk FOREIGN KEY ( comuna_com_id )
        REFERENCES comuna ( com_id );

ALTER TABLE miembro
    ADD CONSTRAINT miembro_junta_vecinos_fk FOREIGN KEY ( junta_vecinos_jun_id )
        REFERENCES junta_vecinos ( jun_id );

ALTER TABLE noticia
    ADD CONSTRAINT noticia_actividad_fk FOREIGN KEY ( actividad_act_id )
        REFERENCES actividad ( act_id );

ALTER TABLE noticia
    ADD CONSTRAINT noticia_administrador_fk FOREIGN KEY ( administrador_adm_id )
        REFERENCES administrador ( adm_id );

ALTER TABLE noticia
    ADD CONSTRAINT noticia_proyecto_fk FOREIGN KEY ( proyecto_proy_id )
        REFERENCES proyecto ( proy_id );

ALTER TABLE proyecto
    ADD CONSTRAINT proyecto_estado_proyecto_fk FOREIGN KEY ( estado_proyecto_est_proy_id )
        REFERENCES estado_proyecto ( est_proy_id );

ALTER TABLE proyecto
    ADD CONSTRAINT proyecto_miembro_fk FOREIGN KEY ( miembro_mie_rut )
        REFERENCES miembro ( mie_rut );

ALTER TABLE reserva
    ADD CONSTRAINT reserva_espacio_fk FOREIGN KEY ( espacio_esp_id )
        REFERENCES espacio ( esp_id );

ALTER TABLE reserva
    ADD CONSTRAINT reserva_miembro_fk FOREIGN KEY ( miembro_mie_rut )
        REFERENCES miembro ( mie_rut );

ALTER TABLE solicitud_certificado
    ADD CONSTRAINT solicitud_cer_certificado_fk FOREIGN KEY ( certificado_cer_id )
        REFERENCES certificado ( cer_id );

ALTER TABLE solicitud_certificado
    ADD CONSTRAINT solicitud_cer_miembro_fk FOREIGN KEY ( miembro_mie_rut )
        REFERENCES miembro ( mie_rut );



-- Informe de Resumen de Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            17
-- CREATE INDEX                             1
-- ALTER TABLE                             42
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 1



-- Informe de Resumen de Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            17
-- CREATE INDEX                             1
-- ALTER TABLE                             42
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 1
