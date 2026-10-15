# ✨ Horóscopo Mensual (Streamlit)

App para generar el horóscopo de un mes completo: 12 signos × todos los días × 4 categorías
(Hoy, Amor, Riqueza, Bienestar).

- **Textos únicos**: ningún pronóstico se repite dentro del mes, entre signos, ni con lo ya guardado en la base de datos.
- **Tono positivo**: cada texto plantea una situación, un esfuerzo/dificultad y cierra con luz.
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

Los fragmentos viven en `content.py`. Más frases = más meses sin agotar combinaciones.
Tests: `python -m pytest tests`.
