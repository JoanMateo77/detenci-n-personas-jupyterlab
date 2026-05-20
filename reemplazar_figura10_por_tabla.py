"""
Reemplaza el placeholder de la Figura 10 (resumen profesional) por una tabla
nativa de Word con los datos reales extraídos del CSV profesional.
"""
import json
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CARPETA = Path("/Users/dev/Downloads/BASESDEDATOS2/laboratorio18abrilsegundo")
DOC = CARPETA / "LAB_18_ABRIL_Joan_Mateo.docx"
RESUMEN = json.loads((CARPETA / "resumen_pro.json").read_text())

UAO_RED = "A81223"
UAO_GRAY = RGBColor(60, 60, 60)
UAO_BLACK = RGBColor(20, 20, 20)
HEADER_BG = "780C19"
ROW_ALT = "F4F4F4"


def shade(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)


doc = Document(str(DOC))
body = doc.element.body

# Buscamos la tabla placeholder previa al texto "Figura 10."
target = "Figura 10."
children = list(body.iterchildren())
target_idx = None
for i, el in enumerate(children):
    if el.tag.endswith('}p') and target in (el.text or ''):
        target_idx = i
        break

if target_idx is None:
    raise RuntimeError("No se encontró el caption de Figura 10.")

# Encontrar la tabla previa (placeholder)
placeholder_tbl_el = None
for back in range(target_idx - 1, -1, -1):
    if children[back].tag.endswith('}tbl'):
        placeholder_tbl_el = children[back]
        break
if placeholder_tbl_el is None:
    raise RuntimeError("No se encontró tabla placeholder antes de Figura 10.")

# Obtener objeto python-docx
placeholder_tbl = None
for t in doc.tables:
    if t._tbl is placeholder_tbl_el:
        placeholder_tbl = t
        break

# Vaciar y reconstruir la tabla con 2 columnas y header
celda = placeholder_tbl.cell(0, 0)
celda.text = ""

# Crear una tabla nueva con los datos del resumen y meterla DENTRO de la celda
filas = [
    ("Frames procesados",            f"{RESUMEN['frames_procesados']:,}"),
    ("Detecciones totales",          f"{RESUMEN['detecciones_totales']:,}"),
    ("FPS promedio",                 f"{RESUMEN['fps_promedio']:.2f}"),
    ("Latencia media de inferencia", f"{RESUMEN['tiempo_inferencia_promedio_ms']:.2f} ms"),
    ("Personas promedio por frame",  f"{RESUMEN['personas_promedio_por_frame']:.2f}"),
    ("Confianza promedio",           f"{RESUMEN['confianza_promedio']:.4f}"),
    ("Conteo de entradas (cruces ↓)", f"{RESUMEN['entrada_total']}"),
    ("Conteo de salidas (cruces ↑)",  f"{RESUMEN['salida_total']}"),
    ("Identificadores únicos (tracking)", f"{RESUMEN['ids_unicos_tracking']}"),
    ("ID con mayor permanencia",     f"ID {RESUMEN['id_mayor_permanencia']}"),
    ("Permanencia máxima registrada", f"{RESUMEN['dwell_max_segundos']:.2f} s"),
]

# Tabla anidada dentro de la celda
tabla_int = celda.add_table(rows=len(filas) + 1, cols=2)
tabla_int.autofit = False
tabla_int.columns[0].width = Inches(3.5)
tabla_int.columns[1].width = Inches(2.0)

# Header
hdr = tabla_int.rows[0].cells
hdr[0].text = ""
hdr[1].text = ""
for j, txt in enumerate(["Métrica", "Valor"]):
    c = hdr[j]
    shade(c, HEADER_BG)
    c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(txt)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)

# Cuerpo
for i, (metrica, valor) in enumerate(filas, start=1):
    row_cells = tabla_int.rows[i].cells
    row_cells[0].text = ""
    row_cells[1].text = ""
    if i % 2 == 0:
        shade(row_cells[0], ROW_ALT)
        shade(row_cells[1], ROW_ALT)
    # métrica
    p0 = row_cells[0].paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r0 = p0.add_run(metrica)
    r0.font.name = "Calibri"
    r0.font.size = Pt(10)
    r0.font.color.rgb = UAO_GRAY
    # valor
    p1 = row_cells[1].paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p1.add_run(valor)
    r1.font.name = "Calibri"
    r1.font.size = Pt(11)
    r1.bold = True
    r1.font.color.rgb = UAO_BLACK

# Quitar el borde rojo del placeholder externo (para que no se vea doble borde)
tcPr = placeholder_tbl.cell(0, 0)._tc.get_or_add_tcPr()
tcBorders = tcPr.find(qn('w:tcBorders'))
if tcBorders is not None:
    tcPr.remove(tcBorders)

# Reemplazar el texto del caption "Figura 10. ..." para reflejar que ahora es tabla
cap_el = children[target_idx]
# Limpiar
for r in list(cap_el):
    cap_el.remove(r)
# Reescribir caption
p_obj = None
for p in doc.paragraphs:
    if p._p is cap_el:
        p_obj = p
        break
if p_obj is not None:
    p_obj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_obj.add_run("Tabla 1. ")
    r1.bold = True
    r1.font.size = Pt(10)
    r1.font.color.rgb = UAO_BLACK
    r2 = p_obj.add_run("Resumen estadístico de la sesión del notebook profesional "
                       "(datos extraídos del CSV generado).")
    r2.italic = True
    r2.font.size = Pt(10)
    r2.font.color.rgb = UAO_GRAY

doc.save(str(DOC))
print("✓ Figura 10 reemplazada por tabla nativa con datos reales del profesional.")
