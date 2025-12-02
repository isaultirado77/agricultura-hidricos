# **Diccionario de Datos — Agricultura Sonora (1999–2022)**

## **1. Identificación del Conjunto de Datos**

**Fuente:** Gobierno del Estado de Sonora — Datos Abiertos
**URL:** [https://datos.sonora.gob.mx/dataset/Agricultura%20Sonora](https://datos.sonora.gob.mx/dataset/Agricultura%20Sonora)
**Años cubiertos:** 1999–2022
**Formato original:** Archivos **XLSX** por año
**Archivos adicionales:**

* `catalogo.xlsx` (múltiples tablas auxiliares)
* `diccionario_agricultura_sonora.csv`

El catálogo no aportó información útil para el análisis y se omitió.
El diccionario oficial se integró parcialmente en este documento.

---

# **2. Estado Original del Dataset**

El conjunto original consiste en **24 archivos Excel** (uno por año) con estructura uniforme:

```
agricultura-sonora-1999.xlsx
agricultura-sonora-2000.xlsx
…
agricultura_sonora_-2022.xlsx
```

Cada archivo contiene una sola hoja: **Hoja1**.

Los datos incluyen información de:

* Superficie sembrada / cosechada / siniestrada
* Producción total y rendimiento
* Valores económicos
* Identificación de municipios, distritos DDR, ciclos y cultivos

### Problemas detectados:

* Inconsistencias en mayúsculas/minúsculas
* Variaciones en nombres de columnas
* Presencia de prefijo `"ddr "` en la columna del distrito
* Formatos mixtos (numéricos ↔ texto) en claves
* Archivos con nombres no homogéneos (ej. `agricultura_sonora_-2022.xlsx`)

---

# **3. Transformación Aplicada**

La función usada fue:

```python
dfs = list(pd.read_excel(path, sheet_name='Hoja1') for path in data_paths)
agriculutra = pd.concat(dfs)
agriculutra = normalize_str(agriculutra)
agriculutra = agriculutra.rename(columns=AGR_COLUMNS_MAP)
agriculutra['distrito_ddr'] = agriculutra['distrito_ddr'].str.replace('ddr ', '')
```

### **Transformaciones realizadas:**

### 1. Lectura y unión

* Se leyeron todos los archivos `agricultura-sonora-*.xlsx`.
* Se concatenaron en un solo DataFrame.

### 2. Normalización de strings

* Se aplicó `normalize_str()` a:

  * nombres de columnas
  * valores tipo string
* Efectos:

  * Eliminación de tildes
  * Conversión a minúsculas
  * Reemplazo de espacios→underscore
  * Limpieza general de caracteres especiales

### 3. Renombrado de columnas

Usando `AGR_COLUMNS_MAP`, las columnas fueron estandarizadas a nombres consistentes en snake_case.
(Ej.: `ANO` : `ano`, `PRODTON` : `produccion_ton`).

### 4. Limpieza de columna `distrito_ddr`

* Se removió el prefijo `"ddr "` para dejar solo el número del distrito.

### 5. Exportación

* Se generó `data/processed/agricultura/agricultura_processed.csv`.

---

# **4. Diccionario de Datos (Posterior a Transformación)**

| Columna                          | Tipo  | Descripción                                                 |
| -------------------------------- | ----- | ----------------------------------------------------------- |
| **ano**                          | str   | Año del registro.                                           |
| **cierre_o_avance**              | int   | Indica si el registro es cierre o avance del año.           |
| **ciclo**                        | int   | 1=Otoño–Invierno, 2=Primavera–Verano, 3=Perennes.           |
| **distrito_ddr**                 | str   | Clave del Distrito de Desarrollo Rural (sin prefijo "ddr"). |
| **nombre_distrito_ddr**          | str   | Nombre del DDR.                                             |
| **municipio_cve**                | str   | Clave del municipio.                                        |
| **municipio_nombre**             | str   | Nombre del municipio.                                       |
| **mes_cve**                      | str   | Clave del mes.                                              |
| **mes_nombre**                   | str   | Nombre del mes.                                             |
| **cultivo_cve**                  | str   | Clave del cultivo.                                          |
| **cultivo_nombre**               | str   | Nombre del cultivo.                                         |
| **variedad_cve**                 | str   | Clave de la variedad.                                       |
| **variedad_nombre**              | str   | Nombre de la variedad.                                      |
| **sup_sembrada_ha**              | float | Hectáreas sembradas.                                        |
| **sup_cosechada_ha**             | float | Hectáreas cosechadas.                                       |
| **sup_siniestrada_ha**           | float | Hectáreas siniestradas.                                     |
| **produccion_ton**               | float | Toneladas producidas.                                       |
| **rendimiento_ton_ha**           | float | Producción/ha.                                              |
| **precio_mr_pesos_ton**          | float | Precio Medio Rural.                                         |
| **valor_produccion_miles_pesos** | float | Valor total de la producción.                               |

---

# **5. Notas y Decisiones Metodológicas**

* El catálogo incluido en la descarga contiene claves y catálogos relacionados, pero no aportó valor adicional: **se omitió**.
* Se confió en el diccionario de datos oficial para interpretar las variables.
* Las claves permanecen como strings, porque existen inconsistencias numéricas (ej. ceros a la izquierda).
* No se realizó validación geográfica cruzada (municipios/DDR), aunque podría hacerse en futuras mejoras.
* No se agregaron columnas derivadas aún (como "producción por municipio”, "intensidad de cultivo", etc.).

---

# **6. Archivo Final**

**`data/processed/agricultura/agricultura_processed.csv`**
Incluye todos los años integrados y estandarizados.
