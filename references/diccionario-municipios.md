# **Diccionario de Datos – Municipios de Sonora (Geometrías)**

**Fuente oficial:** INEGI – Marco Geoestadístico
**URL:** [https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/794551132173/26_sonora.zip](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/794551132173/26_sonora.zip)

**Fecha de descarga:** noviembre 2024
**Estado:** Procesado y documentado
**Uso:** Mapas coropléticos, uniones geoespaciales y análisis territorial

---

# 1. **Descripción general del dataset**

Este conjunto contiene la geometría oficial de los **municipios del estado de Sonora**, según el Marco Geoestadístico del INEGI. Se descargaron múltiples shapefiles que representan diferentes capas geográficas (localidades, regiones, ejes, límites, etc.)

De acuerdo con el catálogo (`contenido.pdf`), el archivo específico que contiene las **geometrías municipales** es:

```
26mun.shp
```

Solo este archivo se utiliza en el proyecto.

---

# 2. **Archivos originales descargados**

El directorio incluye múltiples shapefiles con diferentes capas temáticas:

```
26a.shp  
26ar.shp  
26cd.shp  
26e.shp  
26ent.shp  
26fm.shp  
26l.shp  
26lpr.shp  
26m.shp  
26mun.shp   (archivo relevante)
26pe.shp  
26pem.shp  
26sia.shp  
26sil.shp  
26sip.shp  
26ti.shp  
```

Aunque muchos contienen geometría, *solo `26mun.shp` contiene la capa de municipios*, según el catálogo.

---

# 3. **Estructura del dataset original**

El shapefile `26mun.shp` contiene aproximadamente:

* Geometría poligonal de cada municipio
* Identificadores administrativos
* Nombres oficiales de municipio y estado
* Clave del municipio y la entidad

### **Columnas típicas de shapefile (originales):**

| Columna    | Tipo    | Descripción                                  |
| ---------- | ------- | -------------------------------------------- |
| `CVE_ENT`  | string  | Clave de la entidad federativa (Sonora = 26) |
| `CVE_MUN`  | string  | Clave numérica del municipio                 |
| `NOMGEO`   | string  | Nombre del municipio                         |
| `geometry` | Polygon | Polígono del municipio                       |

*Los nombres exactos pueden variar ligeramente según versión del MGE.*

---

# 4. **Catálogo y metadatos**

El archivo:

```
catalogos/contenido.pdf
```

indica:

* Definición de cada capa
* Propósito cartográfico
* Claves de entidad y municipio
* Fuentes de construcción del Marco Geoestadístico

No incluye un diccionario detallado por campo, como suele pasar con shapefiles.

---

# 5. **Calidad del dato – Archivos RAW**

### Problemas detectados

* Nombres de municipios en **mayúsculas** y con acentos (normalización requerida)
* Columna `CVE_ENT` siempre tiene valor 26 (redundante)
* Encoding estándar, sin problemas de lectura
* Estructura limpia y consistente

### Elementos omitidos

Aunque se descargaron múltiples capas geográficas, solo se usó la capa municipal (`26mun.shp`), por ser la relevante para análisis estadístico y mapas coropléticos.

---

# 6. **Transformaciones aplicadas**

```python
gdf.columns = gdf.columns.str.lower()
gdf['nomgeo'] = gdf['nomgeo'].str.lower()
gdf = gdf.drop(columns='cve_ent')
```

### Transformaciones realizadas:

* **Conversión a minúsculas** de nombres de columnas
* Normalización de `nomgeo`:

  * todo en minúsculas
  * remoción de acentos (si aplica)
  * limpieza de espacios
* Eliminación de la columna `cve_ent` (redundante, siempre 26)
* Exportación a GeoJSON para mayor compatibilidad

---

# 7. **Estructura final del dataset procesado**

Archivo generado:

```
data/processed/geodata/mpios_processed.geojson
```

### **Columnas finales:**

| Variable   | Tipo    | Descripción                                              |
| ---------- | ------- | -------------------------------------------------------- |
| `cve_mun`  | string  | Clave del municipio de Sonora                            |
| `nomgeo`   | string  | Nombre oficial del municipio (normalizado en minúsculas) |
| `geometry` | Polygon | Polígono con los límites municipales                     |

(Otras columnas del shapefile se mantienen según versión pero sin modificaciones.)

---

# 8. **Archivos finales generados**

* `data/processed/mpios_processed.geojson`