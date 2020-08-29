import re
text1 = '"Python", "PHP", "Java"'
print(re.findall(r'"(.*?)"', text1))

# \\(?!.*\\)(.*?)(?=)\;
text2 = """
DROP DATABASE IF EXISTS mydatabase;
CREATE DATABASE mydatabase;
USE mydatabase;
CREATE TABLE Persons (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255)
);
CREATE TABLE mydb (
"index" INT(8),
  "id_evento_caso" INT(8),
  "sexo" VARCHAR(255),
  "edad" FLOAT,
  "edad_a�os_meses" VARCHAR(255),
  "residencia_pais_nombre" VARCHAR(255),
  "residencia_provincia_nombre" VARCHAR(255),
  "residencia_departamento_nombre" VARCHAR(255),
  "carga_provincia_nombre" VARCHAR(255),
  "fecha_inicio_sintomas" VARCHAR(255),
  "fecha_apertura" VARCHAR(255),
  "sepi_apertura" INT(8),
  "fecha_internacion" VARCHAR(255),
  "cuidado_intensivo" VARCHAR(255),
  "fecha_cui_intensivo" VARCHAR(255),
  "fallecido" VARCHAR(255),
  "fecha_fallecimiento" VARCHAR(255),
  "asistencia_respiratoria_mecanica" VARCHAR(255),
  "carga_provincia_id" INT(8),
  "origen_financiamiento" VARCHAR(255),
  "clasificacion" VARCHAR(255),
  "clasificacion_resumen" VARCHAR(255),
  "residencia_provincia_id" INT(8),
  "fecha_diagnostico" VARCHAR(255),
  "residencia_departamento_id" INT(8),
  "ultima_actualizacion" VARCHAR(255)
);
"""
print(re.findall(r'CREATE TABLE mydb ([.*?]);', text2))