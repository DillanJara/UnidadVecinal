-- Generado por Oracle SQL Developer Data Modeler 19.4.0.350.1424
--   en:        2023-09-20 18:03:16 CLST
--   sitio:      SQL Server 2012
--   tipo:      SQL Server 2012



CREATE TABLE ACTIVIDAD 
    (
     act_id INTEGER NOT NULL , 
     act_fecha DATE NOT NULL , 
     act_descripcion VARCHAR (30) NOT NULL , 
     act_cupo INTEGER NOT NULL , 
     act_imagen VARCHAR (300) NOT NULL , 
     act_cuota INTEGER , 
     TIPO_ACTIVIDAD_tip_act_id INTEGER NOT NULL , 
     ADMINISTRADOR_adm_id INTEGER NOT NULL 
    )
GO;

ALTER TABLE ACTIVIDAD ADD CONSTRAINT ACTIVIDAD_PK PRIMARY KEY CLUSTERED (act_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE ADMINISTRADOR 
    (
     adm_id INTEGER NOT NULL , 
     adm_nombre VARCHAR (30) NOT NULL , 
     MIEMBRO_mie_rut INTEGER NOT NULL 
    )
GO; 

    


CREATE UNIQUE NONCLUSTERED INDEX 
    ADMINISTRADOR__IDX ON ADMINISTRADOR 
    ( 
     MIEMBRO_mie_rut 
    ) 
GO;

ALTER TABLE ADMINISTRADOR ADD CONSTRAINT ADMINISTRADOR_PK PRIMARY KEY CLUSTERED (adm_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE ASISTENCIA 
    (
     asis_id INTEGER NOT NULL , 
     ACTIVIDAD_act_id INTEGER NOT NULL , 
     MIEMBRO_mie_rut INTEGER NOT NULL 
    )
GO;

ALTER TABLE ASISTENCIA ADD CONSTRAINT ASISTENCIA_PK PRIMARY KEY CLUSTERED (asis_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE CERTIFICADO 
    (
     cer_id INTEGER NOT NULL , 
     cer_nombre INTEGER NOT NULL 
    )
GO;

ALTER TABLE CERTIFICADO ADD CONSTRAINT CERTIFICADO_PK PRIMARY KEY CLUSTERED (cer_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE COMUNA 
    (
     com_id INTEGER NOT NULL , 
     com_nombre VARCHAR (30) NOT NULL , 
     REGION_reg_id INTEGER NOT NULL 
    )
GO;

ALTER TABLE COMUNA ADD CONSTRAINT COMUNA_PK PRIMARY KEY CLUSTERED (com_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE CUOTA_SOCIAL 
    (
     cuo_id INTEGER NOT NULL , 
     cuo_monto INTEGER NOT NULL , 
     cuo_fecha_paGO; DATE NOT NULL , 
     cuo_estado VARCHAR (30) NOT NULL , 
     MIEMBRO_mie_rut INTEGER NOT NULL 
    )
GO;

ALTER TABLE CUOTA_SOCIAL ADD CONSTRAINT CUOTA_SOCIAL_PK PRIMARY KEY CLUSTERED (cuo_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE ESPACIO 
    (
     esp_id INTEGER NOT NULL , 
     esp_nombre VARCHAR (30) NOT NULL , 
     esp_direccion VARCHAR (50) NOT NULL , 
     esp_telefono VARCHAR (12) NOT NULL , 
     JUNTA_VECINOS_jun_id INTEGER NOT NULL 
    )
GO;

ALTER TABLE ESPACIO ADD CONSTRAINT ESPACIO_PK PRIMARY KEY CLUSTERED (esp_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE ESTADO_PROYECTO 
    (
     est_proy_id INTEGER NOT NULL , 
     est_proy_estado VARCHAR (30) NOT NULL 
    )
GO;

ALTER TABLE ESTADO_PROYECTO ADD CONSTRAINT ESTADO_PROYECTO_PK PRIMARY KEY CLUSTERED (est_proy_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE FAMILIAR_MIEMBRO 
    (
     fam_mie_rut INTEGER NOT NULL , 
     mie_dv CHAR NOT NULL , 
     mie_nombre VARCHAR (30) NOT NULL , 
     mie_ap_paterno VARCHAR (30) NOT NULL , 
     mie_ap_materno VARCHAR (30) NOT NULL , 
     mie_telefono VARCHAR (12) NOT NULL , 
     parentesco VARCHAR (30) NOT NULL , 
     MIEMBRO_mie_rut INTEGER NOT NULL 
    )
GO;

ALTER TABLE FAMILIAR_MIEMBRO ADD CONSTRAINT FAMILIAR_MIEMBRO_PK PRIMARY KEY CLUSTERED (fam_mie_rut)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE JUNTA_VECINOS 
    (
     jun_id INTEGER NOT NULL , 
     jun_nombre VARCHAR (50) NOT NULL , 
     jun_fecha_fundacion DATE NOT NULL , 
     jun_nombre_villa VARCHAR (30) NOT NULL , 
     jun_telefono VARCHAR (12) NOT NULL , 
     jun_correo VARCHAR (50) NOT NULL , 
     jun_direccion VARCHAR (50) NOT NULL , 
     jun_mision VARCHAR (300) NOT NULL , 
     COMUNA_com_id INTEGER NOT NULL 
    )
GO;

ALTER TABLE JUNTA_VECINOS ADD CONSTRAINT JUNTA_VECINOS_PK PRIMARY KEY CLUSTERED (jun_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;
ALTER TABLE JUNTA_VECINOS ADD CONSTRAINT JUNTA_VECINOS_jun_telefono_UN UNIQUE NONCLUSTERED (jun_telefono)
GO;
ALTER TABLE JUNTA_VECINOS ADD CONSTRAINT JUNTA_VECINOS_jun_correo_UN UNIQUE NONCLUSTERED (jun_correo)
GO;

CREATE TABLE MIEMBRO 
    (
     mie_rut INTEGER NOT NULL , 
     mie_dv CHAR (1) NOT NULL , 
     mie_nombre VARCHAR (30) NOT NULL , 
     mie_ap_paterno VARCHAR (30) NOT NULL , 
     mie_ap_materno VARCHAR (30) NOT NULL , 
     mie_fecha_nacimento DATE NOT NULL , 
     mie_telefono VARCHAR (12) NOT NULL , 
     mie_correo VARCHAR (50) NOT NULL , 
     mie_password VARCHAR (50) NOT NULL , 
     mie_direccion VARCHAR (30) NOT NULL , 
     JUNTA_VECINOS_jun_id INTEGER NOT NULL , 
     mie_estado VARCHAR (30) NOT NULL 
    )
GO;

ALTER TABLE MIEMBRO ADD CONSTRAINT MIEMBRO_PK PRIMARY KEY CLUSTERED (mie_rut)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;
ALTER TABLE MIEMBRO ADD CONSTRAINT MIEMBRO_mie_telefono_UN UNIQUE NONCLUSTERED (mie_telefono)
GO;
ALTER TABLE MIEMBRO ADD CONSTRAINT MIEMBRO_mie_correo_UN UNIQUE NONCLUSTERED (mie_correo)
GO;

CREATE TABLE NOTICIA 
    (
     not_id INTEGER NOT NULL , 
     not_titulo VARCHAR (50) NOT NULL , 
     not_subtitulo VARCHAR (100) NOT NULL , 
     not_fecha DATE NOT NULL , 
     not_descripcion VARCHAR (300) NOT NULL , 
     not_imagen VARCHAR (300) NOT NULL , 
     ACTIVIDAD_act_id INTEGER , 
     PROYECTO_proy_id INTEGER , 
     ADMINISTRADOR_adm_id INTEGER NOT NULL 
    )
GO; 
ALTER TABLE NOTICIA 
    ADD CONSTRAINT Arc_2 CHECK ( 
        (  (PROYECTO_proy_id IS NOT NULL) AND 
         (ACTIVIDAD_act_id IS NULL) ) OR 
        (  (ACTIVIDAD_act_id IS NOT NULL) AND 
         (PROYECTO_proy_id IS NULL) ) OR  
        (  (PROYECTO_proy_id IS NULL)  AND 
         (ACTIVIDAD_act_id IS NULL) )  ) 
;

ALTER TABLE NOTICIA ADD CONSTRAINT NOTICIA_PK PRIMARY KEY CLUSTERED (not_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE PROYECTO 
    (
     proy_id INTEGER NOT NULL , 
     proy_nombre VARCHAR (30) NOT NULL , 
     proy_descripcion VARCHAR (300) NOT NULL , 
     proy_imagen VARCHAR (300) NOT NULL , 
     ESTADO_PROYECTO_est_proy_id INTEGER NOT NULL , 
     MIEMBRO_mie_rut INTEGER NOT NULL 
    )
GO;

ALTER TABLE PROYECTO ADD CONSTRAINT PROYECTO_PK PRIMARY KEY CLUSTERED (proy_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE REGION 
    (
     reg_id INTEGER NOT NULL , 
     reg_nombre VARCHAR (50) NOT NULL 
    )
GO;

ALTER TABLE REGION ADD CONSTRAINT REGION_PK PRIMARY KEY CLUSTERED (reg_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE RESERVA 
    (
     res_id INTEGER NOT NULL , 
     res_fecha_hora DATETIME NOT NULL , 
     MIEMBRO_mie_rut INTEGER NOT NULL , 
     ESPACIO_esp_id INTEGER NOT NULL 
    )
GO;

ALTER TABLE RESERVA ADD CONSTRAINT RESERVA_PK PRIMARY KEY CLUSTERED (res_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE SOLICITUD_CERTIFICADO 
    (
     sol_cer_id INTEGER NOT NULL , 
     sol_cer_fecha DATE NOT NULL , 
     MIEMBRO_mie_rut INTEGER NOT NULL , 
     CERTIFICADO_cer_id INTEGER NOT NULL 
    )
GO;

ALTER TABLE SOLICITUD_CERTIFICADO ADD CONSTRAINT SOLICITUD_CERTIFICADO_PK PRIMARY KEY CLUSTERED (sol_cer_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

CREATE TABLE TIPO_ACTIVIDAD 
    (
     tip_act_id INTEGER NOT NULL , 
     tip_act_nombre VARCHAR (30) NOT NULL 
    )
GO;

ALTER TABLE TIPO_ACTIVIDAD ADD CONSTRAINT TIPO_ACTIVIDAD_PK PRIMARY KEY CLUSTERED (tip_act_id)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO;

ALTER TABLE ACTIVIDAD 
    ADD CONSTRAINT ACTIVIDAD_ADMINISTRADOR_FK FOREIGN KEY 
    ( 
     ADMINISTRADOR_adm_id
    ) 
    REFERENCES ADMINISTRADOR 
    ( 
     adm_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE ACTIVIDAD 
    ADD CONSTRAINT ACTIVIDAD_TIPO_ACTIVIDAD_FK FOREIGN KEY 
    ( 
     TIPO_ACTIVIDAD_tip_act_id
    ) 
    REFERENCES TIPO_ACTIVIDAD 
    ( 
     tip_act_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE ADMINISTRADOR 
    ADD CONSTRAINT ADMINISTRADOR_MIEMBRO_FK FOREIGN KEY 
    ( 
     MIEMBRO_mie_rut
    ) 
    REFERENCES MIEMBRO 
    ( 
     mie_rut 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE ASISTENCIA 
    ADD CONSTRAINT ASISTENCIA_ACTIVIDAD_FK FOREIGN KEY 
    ( 
     ACTIVIDAD_act_id
    ) 
    REFERENCES ACTIVIDAD 
    ( 
     act_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE ASISTENCIA 
    ADD CONSTRAINT ASISTENCIA_MIEMBRO_FK FOREIGN KEY 
    ( 
     MIEMBRO_mie_rut
    ) 
    REFERENCES MIEMBRO 
    ( 
     mie_rut 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE COMUNA 
    ADD CONSTRAINT COMUNA_REGION_FK FOREIGN KEY 
    ( 
     REGION_reg_id
    ) 
    REFERENCES REGION 
    ( 
     reg_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE CUOTA_SOCIAL 
    ADD CONSTRAINT CUOTA_SOCIAL_MIEMBRO_FK FOREIGN KEY 
    ( 
     MIEMBRO_mie_rut
    ) 
    REFERENCES MIEMBRO 
    ( 
     mie_rut 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE ESPACIO 
    ADD CONSTRAINT ESPACIO_JUNTA_VECINOS_FK FOREIGN KEY 
    ( 
     JUNTA_VECINOS_jun_id
    ) 
    REFERENCES JUNTA_VECINOS 
    ( 
     jun_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE FAMILIAR_MIEMBRO 
    ADD CONSTRAINT FAMILIAR_MIEMBRO_MIEMBRO_FK FOREIGN KEY 
    ( 
     MIEMBRO_mie_rut
    ) 
    REFERENCES MIEMBRO 
    ( 
     mie_rut 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE JUNTA_VECINOS 
    ADD CONSTRAINT JUNTA_VECINOS_COMUNA_FK FOREIGN KEY 
    ( 
     COMUNA_com_id
    ) 
    REFERENCES COMUNA 
    ( 
     com_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE MIEMBRO 
    ADD CONSTRAINT MIEMBRO_JUNTA_VECINOS_FK FOREIGN KEY 
    ( 
     JUNTA_VECINOS_jun_id
    ) 
    REFERENCES JUNTA_VECINOS 
    ( 
     jun_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE NOTICIA 
    ADD CONSTRAINT NOTICIA_ACTIVIDAD_FK FOREIGN KEY 
    ( 
     ACTIVIDAD_act_id
    ) 
    REFERENCES ACTIVIDAD 
    ( 
     act_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE NOTICIA 
    ADD CONSTRAINT NOTICIA_ADMINISTRADOR_FK FOREIGN KEY 
    ( 
     ADMINISTRADOR_adm_id
    ) 
    REFERENCES ADMINISTRADOR 
    ( 
     adm_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE NOTICIA 
    ADD CONSTRAINT NOTICIA_PROYECTO_FK FOREIGN KEY 
    ( 
     PROYECTO_proy_id
    ) 
    REFERENCES PROYECTO 
    ( 
     proy_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE PROYECTO 
    ADD CONSTRAINT PROYECTO_ESTADO_PROYECTO_FK FOREIGN KEY 
    ( 
     ESTADO_PROYECTO_est_proy_id
    ) 
    REFERENCES ESTADO_PROYECTO 
    ( 
     est_proy_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE PROYECTO 
    ADD CONSTRAINT PROYECTO_MIEMBRO_FK FOREIGN KEY 
    ( 
     MIEMBRO_mie_rut
    ) 
    REFERENCES MIEMBRO 
    ( 
     mie_rut 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE RESERVA 
    ADD CONSTRAINT RESERVA_ESPACIO_FK FOREIGN KEY 
    ( 
     ESPACIO_esp_id
    ) 
    REFERENCES ESPACIO 
    ( 
     esp_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE RESERVA 
    ADD CONSTRAINT RESERVA_MIEMBRO_FK FOREIGN KEY 
    ( 
     MIEMBRO_mie_rut
    ) 
    REFERENCES MIEMBRO 
    ( 
     mie_rut 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE SOLICITUD_CERTIFICADO 
    ADD CONSTRAINT SOLICITUD_CERTIFICADO_CERTIFICADO_FK FOREIGN KEY 
    ( 
     CERTIFICADO_cer_id
    ) 
    REFERENCES CERTIFICADO 
    ( 
     cer_id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;

ALTER TABLE SOLICITUD_CERTIFICADO 
    ADD CONSTRAINT SOLICITUD_CERTIFICADO_MIEMBRO_FK FOREIGN KEY 
    ( 
     MIEMBRO_mie_rut
    ) 
    REFERENCES MIEMBRO 
    ( 
     mie_rut 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO;



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
-- CREATE DATABASE                          0
-- CREATE DEFAULT                           0
-- CREATE INDEX ON VIEW                     0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE ROLE                              0
-- CREATE RULE                              0
-- CREATE SCHEMA                            0
-- CREATE SEQUENCE                          0
-- CREATE PARTITION FUNCTION                0
-- CREATE PARTITION SCHEME                  0
-- 
-- DROP DATABASE                            0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
