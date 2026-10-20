# ✨ Horóscopo Mensual (Streamlit)

App para generar el horóscopo de un mes completo: 12 signos × todos los días × 4 categorías
(Hoy, Amor, Riqueza, Bienestar).

- **Sin repetir**: ninguna *oración* se repite dentro del mes, entre signos, ni con lo ya guardado en la base de datos. Dentro de un texto tampoco se repiten ideas ni palabras clave.
- **Voz de astrólogo**: 2 o 3 oraciones que fluyen como un solo pensamiento (situación, esfuerzo y luz), con influencia de los astros o un consejo ocasional. Tono positivo.
- **Excel**: mismo formato del archivo de referencia (hoja `HORO`: SIGNO, CATEGORIA, PRONOSTICO, FECHA), nombre `Horoscopo_OCT_2026-V2.xlsx`.
- **Versiones**: cada generación del mismo mes crea una versión nueva; se pueden eliminar.
- **Base de datos SQLite** con fecha de creación y tilde de *Publicado* por versión.

## Ejecutar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Desplegar en Streamlit Community Cloud

1. Sube el repo a GitHub y crea la app apuntando a `app.py`.
2. Ojo: el disco de Streamlit Cloud es efímero; la base SQLite (`data/horoscopo.db`) se pierde al reiniciar
   la app. Descarga los Excel que necesites. Variable `HOROSCOPO_DB` permite cambiar la ruta.

## Ampliar variedad

Las piezas de redacción viven en `content.py` (situaciones, esfuerzos, resultados, astros, consejos y conectores). Más piezas = más meses sin agotar combinaciones (hoy ~40 meses de historial).
Tests: `python -m pytest tests`.
