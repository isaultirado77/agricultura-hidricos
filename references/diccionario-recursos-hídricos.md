# **Diccionario de Datos – Recursos Hídricos de Sonora**

**Fuente oficial:** Gobierno del Estado de Sonora – Datos Abiertos
**URL:** [https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos](https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos)
**Fecha de descarga:** noviembre 2024
**Estado:** Procesado y documentado
**Archivos originales:** 1941–2024

---

# 1. **Descripción general del dataset**

El conjunto *Recursos Hídricos de Sonora* contiene información histórica del **nivel de almacenamiento en presas del estado de Sonora**, con registros que abarcan más de 80 años (1941–2024).

Está dividido en archivos por década y complementado con un catálogo estatal de presas.

El conjunto incluye:

### **Datos principales (almacenamiento histórico):**

```
hidrico_sonora_1941-1949.xlsx  
hidrico_sonora_1950-1959.xlsx  
hidrico_sonora_1970-1979.xlsx  
hidrico_sonora_1980-1989.xlsx  
hidrico_sonora_1990-1999.xlsx  
hidrico_sonora_2000-2009.xlsx  
hidrico_sonora_2010-2019.xlsx  
hidrico_sonora_2020-actualidad2024.xlsx
```

> *Nota:* Falta la década 1960–1969 por un error en la plataforma de Datos Abiertos.

### **Metadatos adicionales:**

```
catalogo.xlsx  
diccionario_hidrica_sonora.csv
```

---

# 2. **Estructura del dataset original**

Los archivos por década contienen una tabla muy simple, sin encabezados formales, con 3 columnas:

1. Clave de la presa
2. Fecha del registro
3. Nivel de almacenamiento ($\text{hm}^3$)

El diccionario de datos del gobierno incluye sólo estas tres variables; no proporciona información adicional sobre las presas.

### **Columnas originales (reconocidas manualmente):**

| Columna original        | Tipo             | Descripción                                    |
| ----------------------- | ---------------- | ---------------------------------------------- |
| `Clave`                 | Texto            | Clave identificadora de la presa               |
| `Fecha`                 | Fecha            | Fecha del registro                             |
| `Almacenamiento (hmÂ3)` | Numérico (float) | Nivel de almacenamiento en hectómetros cúbicos |

El caracter `Â` en la unidad es un error típico de codificación en la plataforma.

---

# 3. **Catálogo de presas**

El archivo `catalogo.xlsx`, hoja `Catálogo_estatal`, contiene **información estructural de cada presa**, como:

* Nombre de la presa
* Clave
* Corriente (río)
* Capacidad máxima
* Ubicación administrativa

Sin embargo, el catálogo **no tiene diccionario de datos**, por lo que los nombres se interpretaron directamente.

Las hojas:

* `Municipios`
* `Regiones`

son idénticas a las del catálogo agrícola y no aportan valor adicional para este análisis.

---

# 4. **Calidad del dato – Archivos RAW**

### Problemas detectados

* **Falta la década 1960–1969**: no pudo ser descargada por error en el portal.
* **Errores de codificación** en la columna *Almacenamiento (hmÂ3)*.
* **Formato inconsistente de fechas** entre archivos.
* **Claves de presas con mayúsculas/minúsculas mixtas**.
* Algunos archivos presentan filas vacías al final.

### Columnas repetidas o redundantes

Los archivos por década siempre contienen la misma estructura básica.

---

# 5. **Transformaciones aplicadas**

Transformación en dos módulos:

---

## **5.1. Transformación del catálogo de presas**

(archivo: `presas_processed.csv`)

```python
def transform_presas_data(): 
    catalogo_path = hidricos_dir / "catalogo.xlsx"
    presas = pd.read_excel(catalogo_path, sheet_name='Catálogo_estatal')

    presas = normalize_str(presas)

    file_path = hidricos_processed_dir / "presas_processed.csv"
    presas.to_csv(file_path)
```

### Transformaciones realizadas:

* **Normalización de textos** (`normalize_str`):

  * Minúsculas
  * Remoción de acentos
  * Reemplazo de espacios múltiples
  * Recorte de espacios
* Se mantuvieron todas las columnas del catálogo.

---

## **5.2. Transformación de datos históricos**

(archivo: `hidricos_processed.csv`)

```python
dfs = list(pd.read_excel(path, sheet_name='Hoja1') for path in data_paths)
hidricos = pd.concat(dfs)
hidricos.columns = ['clave', 'fecha', 'almacenamiento_hm3']
hidricos['clave'] = hidricos.clave.str.lower()
```

### Transformaciones realizadas:

* **Concatenación de todos los archivos por década**.
* **Asignación explícita de nombres de columnas** al no existir encabezado formal.
* **Normalización de la clave**: conversión a minúsculas.
* **Corrección de la unidad de almacenamiento**: renombrada a `almacenamiento_hm3`.

---

# 6. **Estructura final del dataset procesado**

---

## **6.1. Datos históricos (hidricos_processed.csv)**

| Variable             | Tipo     | Descripción                                         |
| -------------------- | -------- | --------------------------------------------------- |
| `clave`              | string   | Clave única de la presa (normalizada en minúsculas) |
| `fecha`              | datetime | Fecha del registro de almacenamiento                |
| `almacenamiento_hm3` | float    | Nivel de almacenamiento en hectómetros cúbicos      |

---

## **6.2. Catálogo de presas (presas_processed.csv)**

Depende del catálogo pero típicamente incluye:

* `clave`
* `nombre_presa`
* `corriente`
* `capacidad_maxima_hm3`
* `municipio`
* `region_hidrologica`
* etc.

(Los nombres exactos se mantienen de la hoja original, sólo normalizados.)

---

# 7. **Limitaciones del dataset**

* **Hueco temporal importante** en la década **1960–1969**.
* **Errores de codificación** en unidades.
* Los archivos **no especifican zona horaria** ni hora de medición.
* No existen metadatos para columnas del catálogo de presas.
* No se incluye información sobre volúmenes muertos, límites operativos o normas de extracción.
* Datos dependen de procesos administrativos de medición, pudiendo presentar retrasos o inconsistencias.

---

# 8. **Archivos finales generados**

* `data/processed/presas_processed.csv`
* `data/processed/hidricos_processed.csv`