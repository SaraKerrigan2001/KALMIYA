-- =====================================================
-- SCHEMA COMPLETO DE bd_elementos (Solo estructura)
-- PostgreSQL - Versión Final con todas las modificaciones
-- =====================================================

-- Eliminar y recrear schema
DROP SCHEMA IF EXISTS bd_elementos CASCADE;
CREATE SCHEMA bd_elementos;
SET search_path TO bd_elementos;

-- =====================================================
-- TABLAS PRINCIPALES
-- =====================================================

-- Tabla PERSONA
CREATE TABLE PERSONA (
  pers_documento BIGINT NOT NULL,
  pers_nombres VARCHAR(45) NOT NULL,
  pers_apellidos VARCHAR(45) NOT NULL,
  pers_direccion VARCHAR(45) NOT NULL,
  pers_telefono BIGINT NOT NULL,
  pers_tipodoc VARCHAR(5) NOT NULL,
  pers_password VARCHAR(45) NOT NULL,
  pers_correo VARCHAR(100) NOT NULL,
  PRIMARY KEY (pers_documento)
);

-- Tabla MARCA
CREATE TABLE MARCA (
  marc_id INT NOT NULL,
  marc_nombre TEXT NOT NULL,
  PRIMARY KEY (marc_id)
);

-- Tabla ELEMENTO (elem_placa cambiado a TEXT para códigos alfanuméricos)
CREATE TABLE ELEMENTO (
  elem_placa TEXT NOT NULL,
  elem_descripcion TEXT NOT NULL,
  elem_modelo TEXT NOT NULL,
  MARCA_marc_id INT NOT NULL,
  elem_serial TEXT NOT NULL,
  elem_fecha_compra TIMESTAMP NULL,
  elem_vida_util INT NULL,
  elem_costo BIGINT NULL,
  PRIMARY KEY (elem_placa),
  CONSTRAINT fk_ELEMENTO_MARCA
    FOREIGN KEY (MARCA_marc_id)
    REFERENCES MARCA (marc_id)
);

CREATE INDEX idx_ELEMENTO_MARCA ON ELEMENTO(MARCA_marc_id);

-- Tabla SEDE
CREATE TABLE SEDE (
  sede_id INT NOT NULL,
  sede_nombre TEXT NULL,
  PRIMARY KEY (sede_id)
);

-- Tabla SOLICITUD
CREATE TABLE SOLICITUD (
  solic_id SERIAL NOT NULL,
  solic_fecha_ini TIMESTAMP NOT NULL,
  solic_fecha_fin TIMESTAMP NULL,
  PERSONA_pers_documento BIGINT NOT NULL,
  solic_destino TEXT NOT NULL,
  solic_motivo TEXT NOT NULL,
  solic_estado TEXT NOT NULL,
  solic_observaciones TEXT NOT NULL,
  SEDE_sede_id INT NOT NULL,
  PRIMARY KEY (solic_id),
  CONSTRAINT fk_SOLICITUD_PERSONA1
    FOREIGN KEY (PERSONA_pers_documento)
    REFERENCES PERSONA (pers_documento),
  CONSTRAINT fk_SOLICITUD_SEDE1
    FOREIGN KEY (SEDE_sede_id)
    REFERENCES SEDE (sede_id)
);

CREATE INDEX idx_SOLICITUD_PERSONA ON SOLICITUD(PERSONA_pers_documento);
CREATE INDEX idx_SOLICITUD_SEDE ON SOLICITUD(SEDE_sede_id);

-- Tabla AMBIENTE
CREATE TABLE AMBIENTE (
  amb_id INT NOT NULL,
  amb_nombre TEXT NULL,
  SEDE_sede_id INT NOT NULL,
  PRIMARY KEY (amb_id),
  CONSTRAINT fk_AMBIENTE_SEDE1
    FOREIGN KEY (SEDE_sede_id)
    REFERENCES SEDE (sede_id)
);

CREATE INDEX idx_AMBIENTE_SEDE ON AMBIENTE(SEDE_sede_id);

-- Tabla ASIGNACION (ELEMENTO_elem_placa cambiado a TEXT)
CREATE TABLE ASIGNACION (
  ELEMENTO_elem_placa TEXT NOT NULL,
  AMBIENTE_amb_id INT NOT NULL,
  PERSONA_pers_documento BIGINT NOT NULL,
  asig_id SERIAL NOT NULL,
  asig_fecha_ini TIMESTAMP NOT NULL,
  disponible SMALLINT NOT NULL,
  PRIMARY KEY (asig_id),
  CONSTRAINT fk_ASIGNACION_ELEMENTO1
    FOREIGN KEY (ELEMENTO_elem_placa)
    REFERENCES ELEMENTO (elem_placa),
  CONSTRAINT fk_ASIGNACION_AMBIENTE1
    FOREIGN KEY (AMBIENTE_amb_id)
    REFERENCES AMBIENTE (amb_id),
  CONSTRAINT fk_ASIGNACION_PERSONA1
    FOREIGN KEY (PERSONA_pers_documento)
    REFERENCES PERSONA (pers_documento)
);

CREATE INDEX idx_ASIGNACION_AMBIENTE ON ASIGNACION(AMBIENTE_amb_id);
CREATE INDEX idx_ASIGNACION_PERSONA ON ASIGNACION(PERSONA_pers_documento);

-- Tabla ROL
CREATE TABLE ROL (
  rol_id INT NOT NULL,
  rol_nombre TEXT NULL,
  PRIMARY KEY (rol_id)
);

-- Tabla ROL_PERSONA
CREATE TABLE ROL_PERSONA (
  ROL_rol_id INT NOT NULL,
  PERSONA_pers_documento BIGINT NOT NULL,
  SEDE_sede_id INT NOT NULL,
  PRIMARY KEY (ROL_rol_id, PERSONA_pers_documento),
  CONSTRAINT fk_ROL_PERSONA_ROL1
    FOREIGN KEY (ROL_rol_id)
    REFERENCES ROL (rol_id),
  CONSTRAINT fk_ROL_PERSONA_PERSONA1
    FOREIGN KEY (PERSONA_pers_documento)
    REFERENCES PERSONA (pers_documento),
  CONSTRAINT fk_ROL_PERSONA_SEDE1
    FOREIGN KEY (SEDE_sede_id)
    REFERENCES SEDE (sede_id)
);

CREATE INDEX idx_ROL_PERSONA_PERSONA ON ROL_PERSONA(PERSONA_pers_documento);
CREATE INDEX idx_ROL_PERSONA_SEDE ON ROL_PERSONA(SEDE_sede_id);

-- Tabla DETALLE_SOLICITUD
CREATE TABLE DETALLE_SOLICITUD (
  detsolic_id SERIAL NOT NULL,
  SOLICITUD_solic_id INT NOT NULL,
  ASIGNACION_asig_id INT NOT NULL,
  PRIMARY KEY (detsolic_id, SOLICITUD_solic_id),
  CONSTRAINT fk_DETALLE_SOLICITUD_SOLICITUD1
    FOREIGN KEY (SOLICITUD_solic_id)
    REFERENCES SOLICITUD (solic_id),
  CONSTRAINT fk_DETALLE_SOLICITUD_ASIGNACION1
    FOREIGN KEY (ASIGNACION_asig_id)
    REFERENCES ASIGNACION (asig_id)
);

CREATE INDEX idx_DETALLE_SOLICITUD_SOLICITUD ON DETALLE_SOLICITUD(SOLICITUD_solic_id);
CREATE INDEX idx_DETALLE_SOLICITUD_ASIGNACION ON DETALLE_SOLICITUD(ASIGNACION_asig_id);

-- Tabla ESTADOxELEMENTO (ELEMENTO_elem_placa cambiado a TEXT)
CREATE TABLE ESTADOxELEMENTO (
  ELEMENTO_elem_placa TEXT NOT NULL,
  est_elem_id TEXT NOT NULL,
  estado TEXT NOT NULL,
  est_fecha_registro TIMESTAMP NULL,
  PRIMARY KEY (est_elem_id),
  CONSTRAINT fk_ESTADOxELEMENTO_ELEMENTO1
    FOREIGN KEY (ELEMENTO_elem_placa)
    REFERENCES ELEMENTO (elem_placa)
);

CREATE INDEX idx_ESTADOxELEMENTO_ELEMENTO ON ESTADOxELEMENTO(ELEMENTO_elem_placa);

-- Tabla FIRMA_SOLICITUD
CREATE TABLE FIRMA_SOLICITUD (
  SOLICITUD_solic_id INT NOT NULL,
  firm_id TEXT NULL,
  ROL_PERSONA_ROL_rol_id INT NOT NULL,
  ROL_PERSONA_PERSONA_pers_documento BIGINT NOT NULL,
  firm_firmado SMALLINT NOT NULL,
  firm_observacion TEXT NOT NULL,
  firm_fecha_firmado TIMESTAMP NULL,
  CONSTRAINT fk_FIRMA_SOLICITUD_SOLICITUD1
    FOREIGN KEY (SOLICITUD_solic_id)
    REFERENCES SOLICITUD (solic_id),
  CONSTRAINT fk_FIRMA_SOLICITUD_ROL_PERSONA1
    FOREIGN KEY (ROL_PERSONA_ROL_rol_id, ROL_PERSONA_PERSONA_pers_documento)
    REFERENCES ROL_PERSONA (ROL_rol_id, PERSONA_pers_documento)
);

CREATE INDEX idx_FIRMA_SOLICITUD_SOLICITUD ON FIRMA_SOLICITUD(SOLICITUD_solic_id);
CREATE INDEX idx_FIRMA_SOLICITUD_ROL_PERSONA ON FIRMA_SOLICITUD(ROL_PERSONA_ROL_rol_id, ROL_PERSONA_PERSONA_pers_documento);

-- =====================================================
-- FIN DEL SCHEMA
-- =====================================================

SELECT 'Schema bd_elementos creado exitosamente!' as mensaje;
