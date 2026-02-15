--=========================USUARIOS=======================

CREATE TABLE Usuarios (
    -- Clave Primaria y de Identidad
    us_clave INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    
    -- Campos Comunes de Persona
    us_nombre VARCHAR(50) NOT NULL,
    us_apellidos VARCHAR(255) NOT NULL,
    us_correo VARCHAR(255) UNIQUE NOT NULL,
    us_telefono VARCHAR(10) NOT NULL,
    us_fechanac DATE NOT NULL,
    
    -- Restricciones de Dominio para Sexo
    us_sexo CHAR(1) NOT NULL DEFAULT 'N' 
        CHECK (us_sexo IN ('M', 'F', 'N')),
    
    -- Campos de Cuenta/Autenticación
    us_rol VARCHAR(20) NOT NULL DEFAULT 'Paciente' 
        CHECK (us_rol IN ('Paciente', 'Doctor', 'Admin')), 
    us_contrasena VARCHAR(255) NOT NULL
);

--=====================ESPECIALIDADES====================

CREATE TABLE Especialidades (
    es_clave INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    es_nombre VARCHAR(100) UNIQUE NOT NULL
);

--=====================DOCTORES_ESPECIALIDADES========================
-- Nombre de la tabla intermedia cambiado a plural para consistencia
CREATE TABLE Doctores_Especialidades (
    us_clave INT UNSIGNED NOT NULL, 
    es_clave INT UNSIGNED NOT NULL, 
    
    PRIMARY KEY (us_clave, es_clave),
    
    -- Definición de Restricciones de Clave Foránea
    FOREIGN KEY (us_clave) 
        REFERENCES Usuarios(us_clave) 
        ON DELETE CASCADE,
        
    FOREIGN KEY (es_clave) 
        REFERENCES Especialidades(es_clave)
        ON DELETE RESTRICT
);


--======================CONSULTAS========================

CREATE TABLE Consultas (
    co_clave INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    
    -- Campos de contenido
    co_diagnostico TEXT NOT NULL,
    co_motivo VARCHAR(255) NOT NULL,
    
    -- Restricciones de Dominio para Estado
    co_estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente'
        CHECK (co_estado IN ('Pendiente', 'Confirmada', 'Cancelada', 'Completada')),
    
    co_hora TIME NOT NULL,
    co_fecha DATE NOT NULL,
    
    -- Campo para el tipo de consulta
    co_tipo_consulta ENUM('Virtual', 'Presencial') NOT NULL DEFAULT 'Virtual',
    
    -- Claves Foráneas (referencian a Usuarios)
    paciente_clave INT UNSIGNED NOT NULL,
    doctor_clave INT UNSIGNED NOT NULL,
    
    -- Restricciones a Nivel de Tabla
    FOREIGN KEY (paciente_clave)
        REFERENCES Usuarios(us_clave),
    
    FOREIGN KEY (doctor_clave)
        REFERENCES Usuarios(us_clave)

);
