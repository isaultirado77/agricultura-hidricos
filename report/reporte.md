# Agricultura y Agua en Sonora: un vistazo a más de dos décadas de datos
Cuando se habla de agricultura en Sonora, casi siempre pensamos en trigo, maíz, uva, espárrago o papa. Pero detrás de esos cultivos hay algo igual de importante: el agua. En un estado donde el clima es seco por naturaleza, entender cómo cambian los cultivos y cómo cambia el agua no es un lujo técnico, es una necesidad básica.

En este análisis exploré datos agrícolas de 1999 a 2021 y datos de almacenamiento de presas desde 1999. El objetivo no era construir un modelo complejo, sino algo mucho más sencillo (y a veces más valioso): **mirar los datos  y entender la historia que cuentan**.

---
## ¿Cómo ha evolucionado la superficie sembrada y cosechada?

![Superficie Sembrada vs Cosechada 1999-2021](../plots/superficie_sembrada_cosechada.png)
La superficie sembrada y cosechada es el pulso de la actividad agrícola. Representa cuánto se planea sembrar y cuánto se logra cosechar realmente. En Sonora, ambas variables muestran un comportamiento estable a lo largo del tiempo, pero con ciclos muy marcados.

Entre 1999 y 2021, la superficie sembrada creció suavemente, alcanzando su punto más alto alrededor de 2016. Después vino un descenso importante en 2020, uno de los años más secos recientes. Lo interesante es que la superficie cosechada sigue prácticamente el mismo patrón: cuando la siembra sube, la cosecha también; cuando cae, ambas caen.

Hay años donde la diferencia entre sembrado y cosechado se abre más de lo normal, como en 2004 y 2011. Ambos coinciden con periodos secos donde la disponibilidad de agua fue limitada. Aun así, en la mayoría de los años la brecha es pequeña, lo que sugiere que Sonora mantiene tasas bajas de pérdida total de superficie.

La evolución no es caótica. Por el contrario, sigue una lógica muy simple: **años húmedos &rarr; expansión agrícola**, **años secos &rarr; contracción**.

---
## ¿Qué cultivos son los más importantes?

![Comparación de Superficie, Producción y Valor por Cultivo (Top 10)](../plots/top_cultivos.png)

Los cultivos pueden analizarse desde varias dimensiones: cuánto se siembra, cuánto se produce y cuánto valor económico generan. Al comparar estas tres ventanas para los 10 cultivos más importantes del estado, aparece una imagen muy clara.

El **trigo** domina por superficie y producción. Es con diferencia el cultivo más amplio del estado. Pero cuando miramos el valor económico, pierde ese liderazgo. En esta dimensión, cultivos como la **uva**, el **espárrago** y la **papa** se vuelven protagonistas. Son cultivos con menos superficie, pero con un valor por hectárea mucho mayor, impulsados por mercados de exportación.
La **alfalfa**, por su parte, ocupa un papel equilibrado: superficie considerable, producción constante y un valor económico importante, clave para la actividad ganadera.

Este contraste revela la estructura dual de la agricultura sonorense:
**grandes extensiones dedicadas a cultivos extensivos**, y **bloques compactos de cultivos intensivos con altísima rentabilidad**.
---
## ¿Qué cultivos han crecido y cuáles han disminuido?

Para ver qué cultivos están creciendo de verdad, tomé la superficie sembrada en 1999 y la comparé con 2021. Las diferencias son fuertes y reveladoras.
![Cambio porcentual 1999–2021 en superficie sembrada (Top 10)](../plots/cambio_sup_sembrada.png)

### Cultivos en declive

* **Algodón (-93%)**: casi desaparece del paisaje agrícola.
* **Cártamo (-85%)**: cae de manera sostenida desde finales de los 90.
* **Uva (-27%)**: aunque genera un gran valor económico, se siembra menos que antes.

Sorgo y garbanzo también presentan descensos, aunque más moderados.

### Cultivos en crecimiento

* **Espárrago (+191%)** y **papa (+176%)** son los grandes ganadores. Cultivos de exportación, altamente rentables, que han expandido su presencia.
* **Alfalfa (+52%)** también crece de manera estable.
* **Trigo (+16%)** y **maíz (+9%)** muestran un crecimiento moderado pero sostenido en el tiempo.

La conclusión es clara:
**la agricultura sonorense ha estado en transformación**, alejándose de algunos cultivos tradicionales y moviéndose hacia productos de mayor valor.
## ¿Y qué pasa con el agua?
![Disponibilidad de agua vs Superficie sembrada](../plots/disponibilidad_agua_sup_sembrada.png)

El sistema hídrico de Sonora es el reflejo más puro del clima en el estado. Desde 1999, el almacenamiento en presas ha mostrado ciclos intensos de altibajos: años húmedos, años secos, recuperaciones, caídas abruptas.

Los periodos secos más fuertes en el registro reciente —2002 a 2004 y 2019 a 2021— se ven clarísimos tanto en los datos de agua como en la superficie agrícola. Lo interesante es que **cuando se desploma el almacenamiento en presas, se desploma también la superficie sembrada**, y cuando el agua se recupera, la agricultura vuelve a expandirse.

No hace falta un modelo complicado para ver la relación: la agricultura de Sonora y el agua caminan juntas.

La disponibilidad de agua no solo influye en cuánto se siembra, sino también en **qué cultivos crecen o retroceden**. Los cultivos de alto valor que requieren manejo más preciso parecen adaptarse mejor; los extensivos, como algodón y cártamo, no tanto.
---
## Conclusiones

* La actividad agrícola de Sonora se mantiene estable a largo plazo, pero reacciona rápidamente a los ciclos de agua.
* El trigo manda en superficie y producción, pero cultivos como uva, espárrago y papa dominan el valor económico.
* Algunos cultivos tradicionales retroceden, mientras que los cultivos hortícolas de exportación crecen con fuerza.
* La disponibilidad de agua es un factor determinante: cuando baja el nivel en presas, baja la superficie sembrada; cuando se recupera, la actividad agrícola también lo hace.
* En conjunto, los datos muestran una agricultura que se adapta, se ajusta y responde a las condiciones hídricas del estado.