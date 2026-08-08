-- =====================================================
-- BASE DE DATOS COMPLETA: bd_elementos
-- PostgreSQL - Estructura + Datos de Prueba
-- Versión Final con todas las modificaciones aplicadas
-- =====================================================

-- Eliminar y recrear schema
DROP SCHEMA IF EXISTS bd_elementos CASCADE;
CREATE SCHEMA bd_elementos;
SET search_path TO bd_elementos;

-- =====================================================
-- CREAR TODAS LAS TABLAS
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

-- Tabla ELEMENTO (elem_placa como TEXT)
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

-- Tabla ASIGNACION
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

-- Tabla ESTADOxELEMENTO
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
-- INSERTAR DATOS DE PRUEBA
-- =====================================================

-- Insertar Sedes
INSERT INTO SEDE (sede_id, sede_nombre) VALUES
(1, 'Sede Principal'),
(2, 'Sede Norte');

-- Insertar Ambientes
INSERT INTO AMBIENTE (amb_id, amb_nombre, SEDE_sede_id) VALUES
(1, 'Almacén Principal', 1),
(2, 'Aula 201', 1),
(3, 'Oficina Instructores', 1),
(4, 'Laboratorio Sistemas', 1);

-- Insertar Roles
INSERT INTO ROL (rol_id, rol_nombre) VALUES
(1, 'Administrador'),
(2, 'Coordinador'),
(3, 'Instructor'),
(4, 'Almacenista');

-- Insertar Personas (Cuentadantes)
INSERT INTO PERSONA (pers_documento, pers_nombres, pers_apellidos, pers_direccion, pers_telefono, pers_tipodoc, pers_password, pers_correo) VALUES
(12345678, 'María', 'González', 'Coordinación', 3001234567, 'CC', '123456', 'maria.gonzalez@sena.edu.co'),
(87654321, 'Carlos', 'Rodríguez', 'Sistemas', 3007654321, 'CC', '123456', 'carlos.rodriguez@sena.edu.co'),
(11223344, 'Ana', 'Martínez', 'Diseño', 3009876543, 'CC', '123456', 'ana.martinez@sena.edu.co'),
(55667788, 'Luis', 'Pérez', 'Logística', 3005554321, 'CC', '123456', 'luis.perez@sena.edu.co');

-- Asignar Roles a Personas
INSERT INTO ROL_PERSONA (ROL_rol_id, PERSONA_pers_documento, SEDE_sede_id) VALUES
(2, 12345678, 1),  -- María González - Coordinador
(3, 87654321, 1),  -- Carlos Rodríguez - Instructor
(3, 11223344, 1),  -- Ana Martínez - Instructor
(2, 55667788, 1);  -- Luis Pérez - Coordinador

-- Insertar Marcas
INSERT INTO MARCA (marc_id, marc_nombre) VALUES
(1, 'Computadores'),
(2, 'Impresoras'),
(3, 'Proyectores'),
(4, 'Tablets'),
(5, 'Monitores'),
(6, 'Equipos de Red'),
(7, 'Periféricos');

-- Insertar Elementos (Bienes) con códigos alfanuméricos
INSERT INTO ELEMENTO (elem_placa, elem_descripcion, elem_modelo, MARCA_marc_id, elem_serial, elem_fecha_compra, elem_vida_util, elem_costo) VALUES
('HP-2024-001', 'Computador HP EliteBook 840', 'EliteBook 840 G8', 1, 'SN001HP2024', '2024-01-15', 5, 2500000),
('EPSON-2023-045', 'Proyector EPSON PowerLite', 'PowerLite X49', 3, 'SN045EPSON', '2023-08-20', 5, 1800000),
('CANON-2024-012', 'Impresora Canon ImageClass', 'ImageClass MF445dw', 2, 'SN012CANON', '2024-02-10', 5, 800000),
('DELL-2024-015', 'Monitor DELL UltraSharp 27"', 'U2720Q', 5, 'SN015DELL', '2024-03-05', 5, 1200000),
('LOGITECH-2024-020', 'Teclado y Mouse Logitech MK850', 'MK850', 7, 'SN020LOGI', '2024-03-10', 3, 250000),
('CISCO-2024-008', 'Router Cisco RV340', 'RV340', 6, 'SN008CISCO', '2024-02-20', 5, 1500000),
('LENOVO-2024-003', 'Tablet Lenovo Tab M10', 'Tab M10 Plus', 4, 'SN003LENOVO', '2024-01-25', 3, 800000),
('HP-2023-089', 'Laptop HP Pavilion 15', 'Pavilion 15-eh1xxx', 1, 'SN089HP', '2023-11-10', 5, 2200000);

-- Insertar Asignaciones
INSERT INTO ASIGNACION (ELEMENTO_elem_placa, AMBIENTE_amb_id, PERSONA_pers_documento, asig_fecha_ini, disponible) VALUES
('EPSON-2023-045', 2, 12345678, '2024-10-15 10:30:00', 0),
('HP-2023-089', 3, 87654321, '2024-09-20 14:15:00', 0);

-- Insertar Estados de Elementos
INSERT INTO ESTADOxELEMENTO (ELEMENTO_elem_placa, est_elem_id, estado, est_fecha_registro) VALUES
('HP-2024-001', 'EST001', 'Disponible', '2024-01-15'),
('EPSON-2023-045', 'EST002', 'Asignado', '2024-10-15'),
('CANON-2024-012', 'EST003', 'Disponible', '2024-02-10'),
('DELL-2024-015', 'EST004', 'Disponible', '2024-03-05'),
('LOGITECH-2024-020', 'EST005', 'Disponible', '2024-03-10'),
('CISCO-2024-008', 'EST006', 'Disponible', '2024-02-20'),
('LENOVO-2024-003', 'EST007', 'Disponible', '2024-01-25'),
('HP-2023-089', 'EST008', 'Asignado', '2024-09-20');

-- =====================================================
-- VERIFICACIÓN
-- =====================================================

SELECT '✅ Base de datos bd_elementos creada exitosamente!' as resultado;
SELECT 'Personas: ' || COUNT(*) as conteo FROM persona;
SELECT 'Elementos: ' || COUNT(*) as conteo FROM elemento;
SELECT 'Asignaciones: ' || COUNT(*) as conteo FROM asignacion;
SELECT 'Roles asignados: ' || COUNT(*) as conteo FROM rol_persona;
