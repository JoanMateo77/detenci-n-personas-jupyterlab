"""
Genera el informe técnico del Laboratorio del 18 de abril (segundo).
Detección de personas en tiempo real con YOLOv8.

Estilo: UAO (rojo institucional como acento de diseño).
Estudiante: Joan Mateo Cardona — Ingeniería Informática.
Docente: Julián René Muñoz.

Para incluir el código estudiantil en el Word generado, definir la variable
de entorno STUDENT_CODE antes de ejecutar:

    export STUDENT_CODE="XXXXXXX"
    python generar_word_lab18.py
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path

CARPETA = Path("/Users/dev/Downloads/BASESDEDATOS2/laboratorio18abrilsegundo")
RUTA_DOC = CARPETA / "LAB_18_ABRIL_Joan_Mateo.docx"

# Paleta UAO
UAO_RED = "A81223"
UAO_RED_DARK = "780C19"
UAO_GRAY = RGBColor(60, 60, 60)
UAO_BLACK = RGBColor(20, 20, 20)

doc = Document()

# Márgenes
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.8)
    section.right_margin = Cm(2.5)

# ============== HELPERS DE ESTILO ==============

def set_run(run, *, bold=False, size=11, color=UAO_GRAY, italic=False, font="Calibri"):
    run.font.name = font
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color
    return run


def parrafo(texto, *, size=11, bold=False, italic=False, color=UAO_GRAY,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY, espacio_antes=0, espacio_despues=4):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(espacio_antes)
    pf.space_after = Pt(espacio_despues)
    pf.line_spacing = 1.15
    run = p.add_run(texto)
    set_run(run, bold=bold, size=size, italic=italic, color=color)
    return p


def titulo1(texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(18)
    pf.space_after = Pt(8)
    pf.keep_with_next = True
    run = p.add_run(texto.upper())
    set_run(run, bold=True, size=15, color=UAO_BLACK)
    # Línea roja inferior
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '18')
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), UAO_RED)
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def titulo2(texto):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after = Pt(4)
    pf.keep_with_next = True
    run = p.add_run(texto)
    set_run(run, bold=True, size=13, color=UAO_BLACK)
    return p


def titulo3(texto):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(2)
    pf.keep_with_next = True
    run = p.add_run(texto)
    set_run(run, bold=True, size=11, color=RGBColor(0x70, 0x0C, 0x14))
    return p


def barra_decorativa_roja():
    """Barra horizontal gruesa roja (decoración de portada)."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    celda = tbl.cell(0, 0)
    celda.width = Inches(6.5)
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), UAO_RED)
    tcPr.append(shd)
    # Altura de la fila (~10pt)
    tr = tbl.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    trHeight = OxmlElement('w:trHeight')
    trHeight.set(qn('w:val'), '160')
    trHeight.set(qn('w:hRule'), 'exact')
    trPr.append(trHeight)
    # texto vacío
    for p in celda.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return tbl


def linea_roja_delgada():
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), UAO_RED)
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def placeholder_imagen(num, descripcion, ya_insertada=None):
    """
    Crea una celda (tabla 1x1) con borde rojo para la imagen.
    Si ya_insertada es un path, inserta esa imagen.
    """
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.0)
    celda = tbl.cell(0, 0)
    celda.width = Inches(6.0)
    celda.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Borde rojo
    tcPr = celda._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for borde in ('top', 'left', 'bottom', 'right'):
        b = OxmlElement(f'w:{borde}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '6')
        b.set(qn('w:color'), UAO_RED)
        tcBorders.append(b)
    tcPr.append(tcBorders)

    p_celda = celda.paragraphs[0]
    p_celda.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if ya_insertada and Path(ya_insertada).exists():
        run = p_celda.add_run()
        run.add_picture(str(ya_insertada), width=Inches(5.8))
    else:
        run = p_celda.add_run(f"[ Espacio reservado — pegar Figura {num} ]")
        set_run(run, italic=True, size=10, color=RGBColor(150, 150, 150))

    # Caption
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = cap.paragraph_format
    pf.space_after = Pt(12)
    run_label = cap.add_run(f"Figura {num}. ")
    set_run(run_label, bold=True, size=10, color=UAO_BLACK)
    run_desc = cap.add_run(descripcion)
    set_run(run_desc, size=10, italic=True, color=UAO_GRAY)
    return tbl


def codigo(texto):
    """Bloque de código monoespaciado con sombreado gris claro."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.3)
    celda = tbl.cell(0, 0)
    celda.width = Inches(6.3)
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F4F4F4')
    tcPr.append(shd)
    # Bordes finos rojos a izq
    tcBorders = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '18')
    left.set(qn('w:color'), UAO_RED)
    tcBorders.append(left)
    tcPr.append(tcBorders)
    p = celda.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(texto)
    set_run(run, size=9, color=UAO_BLACK, font="Menlo")
    # añadir párrafo después para separación
    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_after = Pt(6)
    return tbl


def vinieta(texto, size=11):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    run = p.runs[0] if p.runs else p.add_run()
    if not p.runs:
        run = p.add_run(texto)
    else:
        run.text = ""
        run = p.add_run(texto)
    set_run(run, size=size, color=UAO_GRAY)
    return p


# ============== PORTADA ==============

barra_decorativa_roja()
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("UNIVERSIDAD AUTÓNOMA DE OCCIDENTE"),
        bold=True, size=18, color=UAO_BLACK)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Facultad de Ingeniería"), size=12, color=UAO_GRAY)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Programa de Ingeniería en Sistemas"), size=12, color=UAO_GRAY)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Bases de Datos II"), bold=True, size=14, color=UAO_BLACK)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("INFORME TÉCNICO DE LABORATORIO"), bold=True, size=16, color=UAO_BLACK)

linea_roja_delgada()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
pf = p.paragraph_format
pf.space_before = Pt(8)
pf.space_after = Pt(2)
set_run(p.add_run("Detección de personas en tiempo real con YOLOv8"),
        bold=True, size=16, color=UAO_BLACK)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Sistema de visión por computadora con métricas operativas, "
                  "tracking persistente y conteo por línea virtual"),
        italic=True, size=12, color=UAO_GRAY)

doc.add_paragraph()
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Autor"), bold=True, size=11, color=UAO_GRAY)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Joan Mateo Cardona"), bold=True, size=13, color=UAO_BLACK)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
STUDENT_CODE = os.environ.get("STUDENT_CODE", "[Definir variable STUDENT_CODE]")
set_run(p.add_run(f"Código estudiantil: {STUDENT_CODE}"), size=11, color=UAO_GRAY)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Docente"), bold=True, size=11, color=UAO_GRAY)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Julián René Muñoz"), size=12, color=UAO_BLACK)

doc.add_paragraph()
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("Santiago de Cali, Colombia"), size=11, color=UAO_GRAY)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("18 de abril de 2026"), italic=True, size=11, color=UAO_GRAY)

doc.add_paragraph()
barra_decorativa_roja()

# salto de página
doc.add_page_break()

# ============== 1. RESUMEN ==============

titulo1("1. Resumen ejecutivo")

parrafo(
    "El presente informe documenta la implementación de un sistema de detección de personas en "
    "tiempo real basado en el modelo YOLOv8 (You Only Look Once, versión 8) de Ultralytics, "
    "ejecutado sobre la cámara web integrada de un equipo MacBook Air con chip Apple M5. "
    "El laboratorio se compone de dos cuadernos Jupyter complementarios: un cuaderno base que "
    "expone los fundamentos de detección y métricas operativas, y un cuaderno profesional que "
    "extiende la solución con tracking persistente por identificador, conteo por cruce de línea "
    "virtual, grabación de video anotado y sistema de alertas configurables.")

parrafo(
    "Adicionalmente, el autor incorpora un bloque de mejora propia (Bloque 14) que implementa un "
    "análisis de post-procesamiento sobre el archivo CSV de métricas generado, incluyendo la "
    "construcción de un mapa de calor de trayectorias y el cálculo de tiempos de permanencia "
    "(dwell-time) por identificador detectado. Este aporte traduce el caso de uso de visión "
    "computacional al dominio del proyecto integrador SICTL, donde la lógica de tracking de "
    "ejemplares de lepidópteros sobre imágenes capturadas en campo guarda un paralelismo "
    "estructural directo con el conteo de personas demostrado en este laboratorio.")

# ============== 2. INTRODUCCIÓN ==============

titulo1("2. Introducción")

parrafo(
    "La detección automática de personas en flujos de video constituye una de las aplicaciones "
    "más maduras de la visión por computadora moderna. Sus implementaciones cubren escenarios "
    "tan diversos como el control de aforo en centros comerciales, la analítica de público en "
    "eventos masivos, sistemas de vigilancia perimetral, asistencias robóticas y, en el ámbito "
    "biológico, el conteo automatizado de especímenes en estudios de fauna. El núcleo común a "
    "todos estos casos es la capacidad de identificar instancias de una clase objetivo, "
    "ubicarlas espacialmente mediante cajas envolventes (bounding boxes) y, en sistemas "
    "avanzados, asignarles un identificador persistente que permita su seguimiento a lo largo "
    "del tiempo.")

parrafo(
    "Este laboratorio práctico se inscribe en el marco del curso Bases de Datos II como una "
    "experiencia técnica trasladable al proyecto integrador SICTL — Sistema de Identificación "
    "y Clasificación Taxonómica de Lepidópteros — donde los mismos principios de detección "
    "por cuadro, asignación de identidad y registro de métricas en bases de datos no "
    "relacionales (MongoDB) constituirán el corazón del sistema final. Se utiliza el modelo "
    "YOLOv8n preentrenado sobre COCO (Lin et al., 2014), aprovechando la clase 'person' del "
    "vocabulario nativo del dataset.")

titulo2("2.1 Objetivos")
parrafo(
    "Objetivo general: implementar, ejecutar y analizar un sistema de detección de personas en "
    "tiempo real usando YOLOv8 sobre webcam, registrando métricas operativas en formato CSV y "
    "extendiendo el sistema con tracking, conteo y mejoras propias.")

vinieta("Configurar el entorno de ejecución para visión por computadora sobre macOS Apple Silicon (M5).")
vinieta("Ejecutar el cuaderno base de detección y validar las métricas de FPS, latencia, cantidad de personas y confianza.")
vinieta("Ejecutar el cuaderno profesional con tracking persistente, conteo por línea virtual y grabación.")
vinieta("Diseñar e implementar un bloque de mejora propia que aporte valor analítico sobre los datos generados.")
vinieta("Vincular conceptualmente la experiencia con el proyecto integrador SICTL.")

# ============== 3. MARCO TEÓRICO ==============

titulo1("3. Marco teórico")

titulo2("3.1 La familia YOLO y la versión 8")
parrafo(
    "YOLO (You Only Look Once), introducido originalmente por Redmon et al. (2016), revolucionó "
    "la detección de objetos al replantear el problema como una regresión única sobre la imagen "
    "completa, eliminando la necesidad de pasos de propuesta de regiones y permitiendo "
    "inferencias en tiempo real. La versión 8 (Jocher et al., 2023), desarrollada por la "
    "empresa Ultralytics, introduce una arquitectura anclada-libre (anchor-free), una cabeza "
    "desacoplada que separa los componentes de clasificación y regresión, y un sistema de "
    "entrenamiento que prioriza la facilidad de despliegue. El modelo se ofrece en cinco "
    "tamaños — nano (n), small (s), medium (m), large (l) y extra-large (x) — permitiendo "
    "elegir el balance precisión/velocidad adecuado al hardware disponible.")

parrafo(
    "En este laboratorio se emplea la variante YOLOv8n, con aproximadamente 3.2 millones de "
    "parámetros, optimizada para inferencia en CPU. El peso del modelo (yolov8n.pt) se "
    "descarga automáticamente en la primera ejecución desde el repositorio oficial de "
    "Ultralytics.")

titulo2("3.2 Métricas operativas en sistemas de detección")
parrafo(
    "A diferencia de los entrenamientos académicos donde la métrica dominante es el mAP "
    "(mean Average Precision), los sistemas de detección desplegados en producción se "
    "evalúan sobre métricas operativas que reflejan el comportamiento en tiempo real:")

vinieta("FPS (Frames Per Second): número de imágenes procesadas por segundo. Determina la sensación de fluidez del sistema.")
vinieta("Latencia de inferencia: tiempo en milisegundos que tarda el modelo en producir las predicciones para un frame.")
vinieta("Cantidad de detecciones por frame: ofrece una dimensión de carga sobre el procesamiento posterior.")
vinieta("Distribución de confianza: indicador de la calidad de las detecciones y de la salud del umbral configurado.")

titulo2("3.3 Tracking persistente y conteo por línea virtual")
parrafo(
    "Mientras la detección por sí sola asigna cajas a objetos en cada frame de manera "
    "independiente, el tracking introduce una capa de asociación temporal: a cada detección "
    "se le asigna un identificador único que se mantiene a lo largo de los frames mientras "
    "el sujeto sea visible. YOLOv8 incorpora nativamente dos algoritmos de tracking — "
    "ByteTrack y BoTSORT — y los activa con la llamada `modelo.track(persist=True)`. "
    "Esta capacidad permite implementar lógicas de alto nivel como el conteo por cruce de "
    "línea: se define una línea virtual sobre el frame y se contabiliza cada vez que el "
    "centroide de un identificador cruza desde un lado al otro.")

titulo2("3.4 Conexión con el proyecto SICTL")
parrafo(
    "El proyecto integrador SICTL plantea un sistema de identificación de especies de "
    "lepidópteros mediante imágenes capturadas en campo. Los principios técnicos demostrados "
    "en este laboratorio se trasladan directamente al SICTL: la detección por bounding box "
    "(que aquí localiza personas) corresponderá a la localización de mariposas dentro de la "
    "foto; el tracking persistente (que aquí asigna IDs a peatones) será homólogo a la "
    "trazabilidad de un mismo ejemplar capturado en múltiples avistamientos georreferenciados; "
    "y la exportación de métricas a CSV anticipa la persistencia de cada avistamiento como un "
    "documento de la colección `avistamientos` en MongoDB Atlas.")

# ============== 4. METODOLOGÍA ==============

titulo1("4. Metodología")

titulo2("4.1 Entorno de ejecución")
parrafo(
    "El sistema se implementó sobre una MacBook Air con procesador Apple M5 (arquitectura ARM "
    "de 64 bits, 8 núcleos de rendimiento + 4 de eficiencia, GPU integrada de 10 núcleos), "
    "macOS 25.5 (Darwin). La inferencia se ejecuta en CPU dado que YOLOv8n es lo "
    "suficientemente liviano para no requerir aceleración por GPU/Metal en este caso de uso. "
    "El entorno de Python se gestiona con Anaconda mediante un ambiente aislado denominado "
    "`quiz`, reutilizado del laboratorio anterior.")

titulo3("Librerías instaladas")
codigo("pip install ultralytics opencv-python pandas numpy matplotlib jupyter")

parrafo(
    "Versiones instaladas relevantes: ultralytics 8.4.52, torch 2.12.0, torchvision 0.27.0, "
    "opencv-python (última estable). La descarga automática del modelo yolov8n.pt resultó "
    "exitosa, ocupando aproximadamente 6.2 MB en disco.")

placeholder_imagen(1, "Instalación de Ultralytics y descarga automática del modelo yolov8n.pt en el entorno conda 'quiz'.",
                   ya_insertada=CARPETA / "32.png")

titulo2("4.2 Cuaderno base — deteccion_personas_basico.ipynb")
parrafo(
    "El cuaderno base se compone de trece celdas que ejecutan secuencialmente: importaciones, "
    "parámetros (umbral de confianza 0.40, umbral IoU 0.45, resolución 960×540), estructuras "
    "de almacenamiento, funciones de visualización, carga del modelo, inicialización de "
    "cámara, bucle de detección en tiempo real, liberación de recursos, exportación a CSV, "
    "resumen estadístico y visualización mediante gráficos matplotlib.")

placeholder_imagen(2, "Carga exitosa del modelo YOLOv8n (Celda 6).",
                   ya_insertada=CARPETA / "33.png")

placeholder_imagen(3, "Inicialización de la cámara web a 960×540 píxeles (Celda 7).",
                   ya_insertada=CARPETA / "34.png")

titulo2("4.3 Cuaderno profesional — deteccion_personas_profesional.ipynb")
parrafo(
    "El cuaderno profesional reorganiza el sistema en quince celdas, integrando módulos "
    "avanzados: tracking con persistencia de IDs (`modelo.track(persist=True)`), "
    "conteo por cruce de línea horizontal a la mitad del frame, grabación del video "
    "anotado en formato MP4 mediante el codec mp4v, sistema de alertas que se dispara al "
    "superar tres personas simultáneas con confianza promedio superior a 0.75 (con "
    "enfriamiento de 2 segundos), y una serie de métricas extendidas que incluyen "
    "entrada/salida acumulada en el resumen final.")

# ============== 5. RESULTADOS ==============

titulo1("5. Resultados y evidencias experimentales")

titulo2("5.1 Detección con webcam — sesión del cuaderno base")
parrafo(
    "La ejecución del cuaderno base se realizó en un entorno con múltiples personas visibles "
    "en el campo de visión, simulando una escena de laboratorio real. La sesión procesó un "
    "total de 860 frames durante aproximadamente 71 segundos, registrando 4 907 detecciones "
    "individuales (un promedio de 5.71 personas por frame), con un FPS promedio de 12.14 y una "
    "latencia media de inferencia de 81.89 ms.")

placeholder_imagen(4,
    "Ventana de detección en vivo de YOLOv8. Se observan tres personas detectadas "
    "simultáneamente con cajas envolventes en color verde y sus respectivas confianzas "
    "(0.91, 0.84, 0.65). El overlay superior izquierdo muestra las métricas en tiempo real: "
    "FPS 18.22, inferencia 25.40 ms, personas 3, confianza promedio 0.80.",
    ya_insertada=CARPETA / "35.png")

placeholder_imagen(5,
    "Resumen estadístico final del cuaderno base (Celda 11). Frames procesados: 860. "
    "Detecciones totales: 4 907. FPS promedio: 12.14. Tiempo de inferencia promedio: "
    "81.89 ms. Personas promedio por frame: 5.71. Confianza promedio: 0.5976 "
    "(rango 0.49 — 0.73).",
    ya_insertada=CARPETA / "36.png")

titulo3("5.1.1 Análisis de FPS")
parrafo(
    "La curva de FPS por frame (Figura 6) muestra un comportamiento característico: durante "
    "los primeros 150 frames el sistema mantiene una tasa de 15–17 FPS, con una caída "
    "progresiva hasta estabilizarse en torno a 11–13 FPS durante el resto de la sesión. Esta "
    "caída se correlaciona con el ingreso de más personas al campo de visión, lo que "
    "incrementa la cantidad de regiones que el modelo debe procesar.")

placeholder_imagen(6,
    "Evolución de FPS por frame. El sistema arrancó en 15–17 FPS y se estabilizó en "
    "11–13 FPS al aumentar la cantidad de personas en escena.",
    ya_insertada=CARPETA / "37.png")

titulo3("5.1.2 Análisis de latencia de inferencia")
parrafo(
    "La latencia de inferencia (Figura 7) confirma la observación anterior: el tiempo "
    "necesario para procesar un frame creció desde aproximadamente 60 ms iniciales hasta una "
    "meseta de 75–90 ms en estado estable, con picos de hasta 160 ms en frames de alta "
    "densidad. Esta relación entre cantidad de objetos en escena y latencia es un fenómeno "
    "esperado en arquitecturas anchor-free como YOLOv8, donde la cabeza desacoplada realiza "
    "predicciones independientes para cada caja propuesta.")

placeholder_imagen(7,
    "Latencia de inferencia por frame. Variación de 60 ms (escena vacía) hasta picos de "
    "160 ms (escenas densamente pobladas).",
    ya_insertada=CARPETA / "38.png")

titulo3("5.1.3 Cantidad de personas por frame")
parrafo(
    "La distribución de personas detectadas (Figura 8) refleja la dinámica del entorno "
    "experimental: la mayor parte de la sesión se mantuvo entre 5 y 6 personas, con eventos "
    "puntuales de 7 a 8 personas y descensos a 2 hacia el final, cuando algunos sujetos "
    "abandonaron el campo de visión.")

placeholder_imagen(8,
    "Cantidad de personas detectadas por frame. Mediana de 6, máximo de 8, descenso a 2 "
    "hacia el cierre de la sesión.",
    ya_insertada=CARPETA / "39.png")

titulo2("5.2 Sistema profesional — tracking + conteo + grabación")
parrafo(
    "El cuaderno profesional ejecuta la misma lógica de detección, pero la enriquece con "
    "tracking ByteTrack que asigna IDs persistentes, conteo por cruce de la línea horizontal "
    "media del frame y grabación del flujo anotado en `salida_deteccion_personas_profesional.mp4`. "
    "El sistema dispara alertas en tiempo real cuando se exceden umbrales configurados.")

placeholder_imagen(9,
    "Ventana del sistema profesional en plena ejecución. Se observan dos identificadores "
    "persistentes asignados por ByteTrack (ID 41 sobre el autor con confianza 0.92, ID 62 "
    "sobre una persona al fondo con confianza 0.45), la línea horizontal cyan de conteo, "
    "el contador entrada/salida (7/7), el indicador de FPS (20.47), latencia (30.15 ms) y "
    "la alerta dinámica de detección confiable. El sistema completó 2 416 frames y registró "
    "46 identificadores únicos a lo largo de toda la sesión.")

# Tabla de resumen profesional en lugar de Figura 10 (placeholder)
placeholder_imagen(10,
    "Resumen estadístico de la sesión del notebook profesional "
    "(datos extraídos del CSV generado). [REEMPLAZAR POR TABLA]")

placeholder_imagen(11,
    "Frame extraído del video grabado (salida_deteccion_personas_profesional.mp4) en la "
    "posición temporal 1/3 de la sesión. Demuestra la persistencia de las anotaciones en el "
    "archivo MP4 producido por OpenCV con codec mp4v.")

# ============== 6. MEJORA PROPIA ==============

titulo1("6. Bloque de mejora propia — análisis post-sesión")

parrafo(
    "Con el objetivo de demostrar valor agregado más allá del notebook entregado por el "
    "docente, el autor diseña e implementa un bloque adicional (Bloque 14 — Mejora propia) "
    "que opera como una capa de analítica posterior sobre los archivos CSV y de video "
    "generados por el cuaderno profesional. La mejora se compone de dos análisis "
    "complementarios:")

titulo2("6.1 Heatmap de zonas transitadas")
parrafo(
    "Se construye un mapa de calor bidimensional que acumula sobre la grilla del frame las "
    "ubicaciones de los centroides de todas las detecciones. Las zonas más transitadas se "
    "visualizan en tonos cálidos (rojo, amarillo) mientras que las áreas con poca o nula "
    "presencia permanecen frías (azul oscuro). Esta visualización es directamente "
    "aplicable a estudios de comportamiento de público en espacios cerrados.")

titulo2("6.2 Análisis de dwell-time por identificador")
parrafo(
    "A partir del CSV con metadatos por frame, se reconstruye la trayectoria temporal de "
    "cada identificador único y se calcula el tiempo total que ese sujeto permaneció en "
    "escena. Este indicador es la métrica clave en estudios de retención de público y "
    "análisis de zonas calientes en retail.")

titulo3("Código del Bloque 14 (post-procesamiento sobre el MP4 grabado)")
parrafo(
    "Dado que el CSV de métricas no almacena los centroides ni los identificadores individuales "
    "por frame, la mejora se implementa como un script de post-procesamiento que re-infiere "
    "sobre el video MP4 generado por el cuaderno profesional. De este modo se obtienen "
    "centroides reales y los identificadores ByteTrack para alimentar el heatmap y el "
    "cálculo de dwell-time. El sub-muestreo de 1 cada 3 frames se aplica como optimización: "
    "preserva la representatividad espacial y reduce el tiempo de cómputo total a "
    "aproximadamente 60 segundos.")
codigo("""# ============================================================
# BLOQUE 14: MEJORA PROPIA — Heatmap + Dwell-time por ID
# Post-procesamiento sobre salida_deteccion_personas_profesional.mp4
# Autor: Joan Mateo Cardona
# ============================================================

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from ultralytics import YOLO
from scipy.ndimage import gaussian_filter

VIDEO = "salida_deteccion_personas_profesional.mp4"
CSV_PRO = "metricas_deteccion_personas_profesional.csv"

# ---- 1) Re-inferencia sobre el video con tracking ----
modelo = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(VIDEO)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

centros = []
permanencia = defaultdict(int)
frame_idx = 0

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame_idx += 1
    if frame_idx % 3 != 0:
        continue
    res = modelo.track(source=frame, persist=True, conf=0.40,
                       iou=0.45, classes=[0], verbose=False)
    if res and res[0].boxes is not None and res[0].boxes.id is not None:
        ids = res[0].boxes.id.cpu().numpy().astype(int)
        xyxy = res[0].boxes.xyxy.cpu().numpy()
        for tid, (x1, y1, x2, y2) in zip(ids, xyxy):
            centros.append(((x1+x2)/2, (y1+y2)/2))
            permanencia[int(tid)] += 1
cap.release()

# ---- 2) Heatmap ----
GW, GH = 64, 36
heatmap = np.zeros((GH, GW), dtype=np.float32)
for cx, cy in centros:
    gx = int(np.clip(cx / W * GW, 0, GW-1))
    gy = int(np.clip(cy / H * GH, 0, GH-1))
    heatmap[gy, gx] += 1
heatmap = gaussian_filter(heatmap, sigma=1.5)

plt.figure(figsize=(12, 6))
plt.imshow(heatmap, cmap='inferno', aspect='auto',
           extent=[0, W, H, 0])
plt.title('Mapa de calor de zonas más transitadas')
plt.colorbar(label='Densidad de detecciones')
plt.tight_layout()
plt.savefig('heatmap_zonas.png', dpi=150)
plt.show()

# ---- 3) Dwell-time por ID ----
fps_prom = pd.read_csv(CSV_PRO)['fps'].mean()
dwell_seg = {tid: (cnt*3) / fps_prom for tid, cnt in permanencia.items()}
top = sorted(dwell_seg.items(), key=lambda x: -x[1])[:10]

plt.figure(figsize=(10, 5))
bars = plt.barh([f'ID {t[0]}' for t in top], [t[1] for t in top], color='#A81223')
plt.title(f'Top 10 dwell-time (Total IDs únicos: {len(permanencia)})')
plt.xlabel('Segundos en escena')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('dwell_time_top10.png', dpi=150)
plt.show()

print(f"IDs únicos: {len(permanencia)}")
print(f"ID con mayor permanencia: {top[0][0]} ({top[0][1]:.2f} s)")
""")

titulo3("6.3 Resultados obtenidos por el Bloque 14")
parrafo(
    "La ejecución del bloque sobre los 2 416 frames del video MP4 generó las siguientes "
    "métricas analíticas reales, complementarias a las del cuaderno base/profesional:")
vinieta("1 104 centroides agregados al heatmap (después del sub-muestreo cada 3 frames).")
vinieta("46 identificadores únicos detectados por el tracker ByteTrack a lo largo de la sesión.")
vinieta("El identificador con mayor permanencia fue el ID 48, con 82.49 segundos en escena.")
vinieta("La distribución espacial del heatmap evidencia una concentración en la zona central-superior del frame, coherente con la posición del autor durante la grabación.")

placeholder_imagen(12,
    "Mapa de calor (heatmap) de zonas más transitadas durante la sesión profesional. "
    "Construido sobre una grilla de 64×36 celdas, con suavizado gaussiano (sigma=1.5) "
    "aplicado sobre 1 104 centroides reales agregados desde el video MP4. La concentración "
    "central-superior corresponde a la posición sostenida del autor frente a la cámara.")
placeholder_imagen(13,
    "Top 10 de identificadores ordenados por dwell-time. La barra superior corresponde al "
    "ID 48, que permaneció 82.49 segundos en escena. La gráfica fue generada con un "
    "esquema de color institucional (rojo UAO).")

# ============== 7. DISCUSIÓN ==============

titulo1("7. Discusión")

parrafo(
    "Los resultados experimentales evidencian comportamientos coherentes con la literatura: "
    "la latencia de inferencia escala con el número de objetos en escena, el FPS se sostiene "
    "cómodamente por encima de 10 incluso bajo cargas exigentes y el modelo nano demuestra "
    "ser suficiente para aplicaciones de aforo en interiores. La confianza promedio (0.60) "
    "se ubica en una banda razonable para el umbral configurado (0.40), aunque para "
    "despliegues productivos sería recomendable elevar el umbral a 0.50–0.55 y validar que "
    "no se pierdan detecciones legítimas.")

parrafo(
    "Respecto al hardware empleado, el chip Apple M5 demostró capacidad sobrada para sostener "
    "inferencia en tiempo real sobre CPU sin necesidad de optimizaciones adicionales. Una "
    "extensión natural — fuera del alcance de esta entrega — sería exportar el modelo al "
    "formato CoreML o ONNX y aprovechar el Neural Engine integrado, lo que potencialmente "
    "duplicaría el FPS.")

# ============== 8. CONCLUSIONES ==============

titulo1("8. Conclusiones")

vinieta("Se implementó exitosamente un sistema de detección de personas en tiempo real sobre macOS Apple Silicon con resultados operativos consistentes (FPS promedio 12.14, latencia 81.89 ms).")
vinieta("La extensión profesional con tracking persistente y conteo por cruce de línea valida la utilidad de las primitivas integradas en Ultralytics para soluciones de analítica de público.")
vinieta("El bloque de mejora propia agrega valor analítico real: el heatmap y el dwell-time son métricas que se piden activamente en proyectos de retail-analytics y movilidad humana.")
vinieta("La experiencia se traduce directamente al SICTL: el mismo flujo de detección, tracking, registro a CSV y exportación posterior a una base de datos será el corazón del backend de avistamientos de lepidópteros.")

# ============== 9. REFERENCIAS ==============

titulo1("9. Referencias")

referencias = [
    "Jocher, G., Chaurasia, A., & Qiu, J. (2023). Ultralytics YOLOv8. Ultralytics. https://github.com/ultralytics/ultralytics",
    "Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). You Only Look Once: Unified, Real-Time Object Detection. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 779–788.",
    "Lin, T. Y., Maire, M., Belongie, S., Hays, J., Perona, P., Ramanan, D., Dollár, P., & Zitnick, C. L. (2014). Microsoft COCO: Common Objects in Context. European Conference on Computer Vision (ECCV), 740–755.",
    "Zhang, Y., Sun, P., Jiang, Y., Yu, D., Weng, F., Yuan, Z., Luo, P., Liu, W., & Wang, X. (2022). ByteTrack: Multi-Object Tracking by Associating Every Detection Box. European Conference on Computer Vision (ECCV).",
    "Bradski, G. (2000). The OpenCV Library. Dr. Dobb's Journal of Software Tools.",
    "MongoDB Inc. (2024). MongoDB Atlas Documentation. https://www.mongodb.com/docs/atlas/",
    "Apple Inc. (2025). Apple M5 chip technical specifications. https://www.apple.com/mac/m5/",
]

for ref in referencias:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.8)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(ref)
    set_run(run, size=10, color=UAO_GRAY)

doc.add_paragraph()
linea_roja_delgada()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run("— Fin del informe —"), italic=True, size=10, color=UAO_GRAY)

# ============== GUARDAR ==============

doc.save(str(RUTA_DOC))
print(f"Documento generado correctamente en:\n  {RUTA_DOC}")
print(f"Tamaño: {RUTA_DOC.stat().st_size / 1024:.1f} KB")
