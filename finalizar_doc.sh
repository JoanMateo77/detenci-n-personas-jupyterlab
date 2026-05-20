#!/bin/bash
# Pipeline de finalización del documento del laboratorio.
# 1. Regenera el Word desde el script principal
# 2. Inserta las 11 imágenes capturadas / procesadas
# 3. Reemplaza el placeholder de Fig 10 por tabla con datos reales

set -e
cd "$(dirname "$0")"

PY=/opt/anaconda3/envs/quiz/bin/python

echo ">> 1) Regenerando documento base..."
$PY generar_word_lab18.py

echo ""
echo ">> 2) Insertando capturas del notebook profesional + mejora propia..."
$PY insertar_imagen.py 9  40.png
$PY insertar_imagen.py 11 frame_representativo.png
$PY insertar_imagen.py 12 heatmap_zonas.png
$PY insertar_imagen.py 13 dwell_time_top10.png

echo ""
echo ">> 3) Reemplazando Figura 10 por tabla nativa con datos reales..."
$PY reemplazar_figura10_por_tabla.py

echo ""
echo ">> ✓ Documento final listo:"
ls -la LAB_18_ABRIL_Joan_Mateo.docx
