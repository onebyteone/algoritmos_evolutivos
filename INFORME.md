# Informe Final

## Objetivo del proyecto
El propósito de esta práctica fue implementar y comparar tres representaciones cromosómicas en un algoritmo genético para distribuir equitativamente a **39 alumnos** en **tres exámenes** (A, B y C). Cada grupo debía contener exactamente 13 estudiantes y el reparto debía minimizar las diferencias de rendimiento académico entre los exámenes.

## Datos utilizados
La información de los estudiantes se encuentra en `notas_1u.csv`, la cual contiene las columnas `Alumno`, `Nota` y `Tipo_Examen`. Las notas están en la escala de 0 a 20.

## Representaciones implementadas
- **Binaria** (`representacion_binaria.py`): cromosoma de 117 bits, tres para cada alumno. Solo un bit se activa para indicar el examen asignado.
- **Real** (`representacion_real.py`): cromosoma de 117 valores reales normalizados en cada tripleta de genes. Los pesos determinan la probabilidad de asignación a cada examen.
- **Permutacional** (`representacion_permutacional.py`): cromosoma que es una permutación de los índices de los alumnos. Los primeros 13 elementos corresponden al examen A, los siguientes 13 al B y el resto al C.

## Resultados principales
El archivo `analisis.txt` resume la actividad comparativa entre las representaciones. Los hallazgos más destacados fueron los siguientes:

- **Representación binaria**: no logró mantener 13 estudiantes por examen y su fitness se quedó en `-1000` por violar la restricción. La desviación estándar entre promedios de notas fue cercana a `0.30`.
- **Representación real**: alcanzó 13 alumnos por grupo con una desviación estándar aproximada de `0.036`. Su fitness mejoró hasta `-1.0911` y se estabilizó después de la generación 30.
- **Representación permutacional**: también obtuvo 13 estudiantes por grupo y la misma desviación de `0.036`. Su fitness inicial fue `0.1187` y llegó rápidamente a `0.2637` en solo 10 generaciones.

En la comparación general, la representación permutacional fue la que **convergió más rápido**, mientras que la representación real obtuvo resultados muy similares pero requirió más generaciones. La representación binaria fue la menos eficiente debido a las restricciones de tamaño de grupo.

## Conclusiones
Las pruebas muestran que, para este problema de asignación equilibrada de estudiantes, las representaciones real y permutacional son adecuadas, con una ligera ventaja para la permutacional en velocidad de convergencia. La representación binaria, aunque sencilla, no maneja bien las restricciones estrictas. En general, la elección de la representación cromosómica tiene un gran impacto en el rendimiento del algoritmo genético y debe seleccionarse según la naturaleza del problema.
