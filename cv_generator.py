"""
CV de Airton Márquez Abril — Edición Editorial Minimalista (claro).

Estética: "quiet luxury" — serif Fraunces + sans Inter, blanco + dorado,
numeración editorial, hairlines, mucho aire. 1 página A4.

  ┌───────────────────────────────────────────────────────┐
  │  AIRTON MÁRQUEZ ABRIL                    (foto ○)      │
  │  AI DEVELOPER JUNIOR · FULL-STACK BUILDER              │
  │  barranquilla · email · github · linkedin             │
  ├──────────────────────────────┬────────────────────────┤
  │  01 · PERFIL                 │  EDUCACIÓN             │
  │                              │  HABILIDADES TÉCNICAS  │
  │  02 · EXPERIENCIA            │  HABILIDADES BLANDAS   │
  │                              │  IDIOMAS               │
  │  03 · FORMACIÓN              │                        │
  ├──────────────────────────────┴────────────────────────┤
  │ footer                                                    │
  └───────────────────────────────────────────────────────┘
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader, simpleSplit
from pathlib import Path

BASE = Path(r"D:\Programacion\portfolio")
FONT_DIR = BASE / "assets" / "fonts"
OUT = BASE / "assets" / "CV-Airton-Marquez.pdf"
AVATAR = BASE / "assets" / "avatar.jpg"

# ---------- Paleta editorial claro ----------
PAPER      = colors.HexColor("#ffffff")
INK        = colors.HexColor("#161616")   # texto principal
BODY       = colors.HexColor("#3d3d3d")   # cuerpo
MUTED      = colors.HexColor("#8a8a8a")   # secundario
FAINT      = colors.HexColor("#c9c9c9")   # terciario
HAIRLINE   = colors.HexColor("#e8e6e0")   # líneas
GOLD       = colors.HexColor("#a87f08")   # dorado oscuro (legible en blanco)
GOLD_SOFT  = colors.HexColor("#d4a307")

W, H = A4

# ---------- Fuentes ----------
pdfmetrics.registerFont(TTFont("Fraunces-500", str(FONT_DIR / "Fraunces-500.ttf")))
pdfmetrics.registerFont(TTFont("Fraunces-600", str(FONT_DIR / "Fraunces-600.ttf")))
pdfmetrics.registerFont(TTFont("Inter-400", str(FONT_DIR / "Inter-400.ttf")))
pdfmetrics.registerFont(TTFont("Inter-500", str(FONT_DIR / "Inter-500.ttf")))
pdfmetrics.registerFont(TTFont("Inter-600", str(FONT_DIR / "Inter-600.ttf")))
pdfmetrics.registerFont(TTFont("Inter-700", str(FONT_DIR / "Inter-700.ttf")))

# ---------- Layout ----------
ML = 22 * mm          # margen izquierdo
MR = 22 * mm          # margen derecho
MT = 40 * mm          # margen superior
MB = 30 * mm          # margen inferior
CONTENT_W = W - ML - MR
MAIN_X = ML
SIDEBAR_W = 58 * mm
SIDEBAR_X = W - MR - SIDEBAR_W
GUTTER = 12 * mm
MAIN_W = SIDEBAR_X - GUTTER - MAIN_X


def wrap(text, font, size, max_w):
    return simpleSplit(text, font, size, max_w)


def draw_avatar(c, cx, cy, r):
    if not AVATAR.exists():
        return
    img = ImageReader(str(AVATAR))
    iw, ih = img.getSize()
    c.saveState()
    p = c.beginPath()
    p.circle(cx, cy, r)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(img, cx - r, cy - r, width=2 * r, height=2 * r, mask="auto")
    c.restoreState()
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(1.0)
    c.circle(cx, cy, r, fill=0, stroke=1)


def section_head(c, x, y, num, label, width, rules=True):
    """Título de sección editorial: número serif dorado + label mayúsculas + hairline."""
    c.setFillColor(GOLD)
    c.setFont("Fraunces-500", 12)
    c.drawString(x, y, num)
    c.setFillColor(INK)
    c.setFont("Inter-700", 8.5)
    c.drawString(x + 9 * mm, y + 1.5, label.upper())
    if rules:
        c.setStrokeColor(HAIRLINE)
        c.setLineWidth(0.6)
        c.line(x, y - 4, x + width, y - 4)
    return y - 9 * mm


def para(c, x, y, text, font="Inter-400", size=9.2, leading=13.5, color=BODY, max_w=MAIN_W, first_y=None):
    lines = wrap(text, font, size, max_w)
    yy = first_y if first_y is not None else y
    for ln in lines:
        c.setFillColor(color)
        c.setFont(font, size)
        c.drawString(x, yy, ln)
        yy -= leading
    return yy


def job_entry(c, x, y, when, title, company, lines, max_w):
    """Entrada de experiencia: fecha derecha, título, empresa dorada, bullets."""
    # fecha derecha
    c.setFillColor(MUTED)
    c.setFont("Inter-500", 8.2)
    c.drawRightString(x + max_w, y + 2, when)
    # título
    c.setFillColor(INK)
    c.setFont("Inter-600", 11)
    c.drawString(x, y, title)
    y -= 5.2 * mm
    # empresa
    c.setFillColor(GOLD)
    c.setFont("Inter-600", 8)
    c.drawString(x, y, company.upper())
    y -= 4.6 * mm
    # bullets
    for ln in lines:
        for chunk in wrap(ln, "Inter-400", 9.0, max_w - 5 * mm):
            # bullet dorado
            c.setFillColor(GOLD)
            c.circle(x + 1.3 * mm, y + 1.2, 0.9, fill=1, stroke=0)
            c.setFillColor(BODY)
            c.setFont("Inter-400", 9.0)
            c.drawString(x + 3.4 * mm, y, chunk)
            y -= 12.8
    return y - 3 * mm


def skill_item(c, x, y, label, indent=0):
    c.setFillColor(GOLD)
    c.circle(x + 1.3 * mm + indent, y + 1.1, 0.8, fill=1, stroke=0)
    c.setFillColor(BODY)
    c.setFont("Inter-400", 8.6)
    c.drawString(x + 3.6 * mm + indent, y, label)
    return y - 4.6 * mm


def main():
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("CV — Airton Márquez Abril")
    c.setAuthor("Airton Márquez Abril")
    c.setSubject("AI Developer Junior · Full-Stack Builder")
    c.setCreator("Portfolio Airton Marquez")

    # fondo
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ================= HEADER =================
    # hairline superior fina dorada
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(1.2)
    c.line(ML, H - 22 * mm, W - MR, H - 22 * mm)

    # nombre — Fraunces grande
    c.setFillColor(INK)
    c.setFont("Fraunces-600", 27)
    c.drawString(ML, H - 33 * mm, "Airton Márquez Abril")

    # rol — Inter 700 espaciado dorado
    c.setFillColor(GOLD)
    c.setFont("Inter-700", 8.2)
    c.drawString(ML, H - 40 * mm, "AI DEVELOPER JUNIOR  ·  FULL-STACK BUILDER  ·  CO-FUNDADOR @ SCOOTERCOOP")

    # contacto — línea gris con separadores (2 filas si hace falta)
    contact1 = "Barranquilla, CO   ·   kaminatrigger@gmail.com   ·   github.com/TriggerXZ"
    contact2 = "linkedin.com/in/airton-márquez-abril"
    c.setFillColor(MUTED)
    c.setFont("Inter-400", 8.6)
    c.drawString(ML, H - 45.5 * mm, contact1)
    c.drawString(ML + 3 * mm, H - 49 * mm, contact2)

    # avatar circular derecha
    draw_avatar(c, W - MR - 10 * mm, H - 32 * mm, 8.5 * mm)

    # ================= COLUMNA PRINCIPAL =================
    y = H - 45.5 * mm - 14 * mm
    x = MAIN_X

    # ---- 01 · Perfil ----
    y = section_head(c, x, y, "01", "Perfil", MAIN_W)
    y = para(c, x, y - 4 * mm,
        "Desarrollador con base práctica en IA generativa, LLMs y automatización. "
        "Co-fundador de ScooterCoop, donde llevo producto desde cero. "
        "Stack principal: Astro, JavaScript/TypeScript, Python, Bash, SQL. "
        "En proceso activo de formación en N8N, Docker y cloud (Azure/GCP) para "
        "cerrar el stack completo de soluciones empresariales.",
        first_y=y - 4 * mm)
    y -= 8 * mm

    # ---- 02 · Experiencia profesional ----
    y = section_head(c, x, y, "02", "Experiencia profesional", MAIN_W)
    y -= 3 * mm
    y = job_entry(c, x, y - 5 * mm, "2025 — Actual", "Co-fundador & Desarrollador principal",
        "ScooterCoop",
        ["Página web, software de alquiler y sistema de reservas.",
         "Soporte y operación del servicio."],
        MAIN_W)
    y -= 2 * mm
    y = job_entry(c, x, y - 4 * mm, "2022 — 2023", "Desarrollador Full-Stack",
        "RMG Insurance Service",
        ["Componentes UI para el sitio web (responsive, interactividad).",
         "Reportes y soporte a base de datos."],
        MAIN_W)
    y -= 7 * mm

    # ---- 03 · Formación académica ----
    y = section_head(c, x, y, "03", "Formación académica", MAIN_W)
    y -= 4 * mm
    # entrada formación
    c.setFillColor(MUTED)
    c.setFont("Inter-500", 8.2)
    c.drawRightString(x + MAIN_W, y, "2022 — 2023")
    c.setFillColor(INK)
    c.setFont("Inter-600", 11)
    c.drawString(x, y, "Técnico en Programación Web")
    y -= 5 * mm
    c.setFillColor(GOLD)
    c.setFont("Inter-600", 8)
    c.drawString(x, y, "UNIVERSIDAD DEL LITORAL")
    y -= 4.6 * mm
    y = para(c, x, y, "HTML, CSS, JavaScript, SQL (MySQL), desarrollo full-stack, patrones de diseño responsive.", size=9.0, leading=12.8, max_w=MAIN_W)
    y -= 3 * mm
    c.setFillColor(MUTED)
    c.setFont("Inter-500", 8.2)
    c.drawRightString(x + MAIN_W, y, "2017")
    c.setFillColor(INK)
    c.setFont("Inter-600", 11)
    c.drawString(x, y, "Bachiller")
    y -= 5 * mm
    c.setFillColor(GOLD)
    c.setFont("Inter-600", 8)
    c.drawString(x, y, "COLEGIO NUESTRA SEÑORA DEL ROSARIO")

    # ================= SIDEBAR =================
    sx = SIDEBAR_X
    sy = H - 45.5 * mm - 14 * mm

    # línea vertical separadora
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.6)
    c.line(SIDEBAR_X - GUTTER / 2, sy, SIDEBAR_X - GUTTER / 2, MB + 14 * mm)

    # ---- Educación ----
    c.setFillColor(INK)
    c.setFont("Inter-700", 8.5)
    c.drawString(sx, sy, "EDUCACIÓN")
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(0.8)
    c.line(sx, sy - 3.5, sx + SIDEBAR_W, sy - 3.5)
    sy -= 8 * mm

    for when, title, inst in [
        ("2022 — 2023", "Técnico en Programación Web", "Universidad del Litoral"),
        ("2017", "Bachiller", "Colegio Nuestra Señora del Rosario"),
    ]:
        c.setFillColor(GOLD)
        c.setFont("Inter-600", 7.8)
        c.drawString(sx, sy, when)
        sy -= 3.8 * mm
        c.setFillColor(INK)
        c.setFont("Inter-600", 9.6)
        c.drawString(sx, sy, title)
        sy -= 3.6 * mm
        c.setFillColor(MUTED)
        c.setFont("Inter-400", 8.2)
        c.drawString(sx, sy, inst)
        sy -= 6 * mm

    sy -= 2 * mm

    # ---- Habilidades técnicas ----
    c.setFillColor(INK)
    c.setFont("Inter-700", 8.5)
    c.drawString(sx, sy, "HABILIDADES TÉCNICAS")
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(0.8)
    c.line(sx, sy - 3.5, sx + SIDEBAR_W, sy - 3.5)
    sy -= 8 * mm

    skills = [
        ("IA & Datos", ["Claude (Code, Skills, Hooks)", "LLMs · RAG · Prompt Eng.", "SQL · MySQL · PostgreSQL"]),
        ("Web & Full-Stack", ["Astro · i18n", "JavaScript · TypeScript", "HTML · CSS · Responsive", "REST APIs · JSON"]),
        ("Automatización", ["Bash scripting", "Python", "GitHub Actions"]),
        ("Deploy & Tools", ["Git · GitHub", "Netlify · Vercel · Render", "VS Code"]),
    ]
    for cat, items in skills:
        c.setFillColor(GOLD)
        c.setFont("Inter-600", 8)
        c.drawString(sx, sy, cat.upper())
        sy -= 4.2 * mm
        for it in items:
            sy = skill_item(c, sx, sy, it)
        sy -= 1.6 * mm

    sy -= 1 * mm

    # ---- Habilidades blandas ----
    c.setFillColor(INK)
    c.setFont("Inter-700", 8.5)
    c.drawString(sx, sy, "HABILIDADES BLANDAS")
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(0.8)
    c.line(sx, sy - 3.5, sx + SIDEBAR_W, sy - 3.5)
    sy -= 8 * mm

    for s in ["Pensamiento crítico", "Comunicación efectiva", "Negociación",
              "Adaptabilidad al cambio", "Orientación a resultados"]:
        sy = skill_item(c, sx, sy, s)
    sy -= 2 * mm

    # ---- Idiomas ----
    c.setFillColor(INK)
    c.setFont("Inter-700", 8.5)
    c.drawString(sx, sy, "IDIOMAS")
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(0.8)
    c.line(sx, sy - 3.5, sx + SIDEBAR_W, sy - 3.5)
    sy -= 8 * mm

    for name, lvl in [("Español", "Nativo"), ("Inglés", "Intermedio (B1/B2)")]:
        c.setFillColor(INK)
        c.setFont("Inter-600", 9.2)
        c.drawString(sx, sy, name)
        c.setFillColor(MUTED)
        c.setFont("Inter-400", 8.2)
        c.drawRightString(sx + SIDEBAR_W, sy, lvl)
        sy -= 5 * mm

    # ================= FOOTER =================
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.6)
    c.line(ML, MB - 6 * mm, W - MR, MB - 6 * mm)
    c.setFillColor(MUTED)
    c.setFont("Inter-400", 7.6)
    c.drawCentredString(W / 2, MB - 12 * mm,
        "Airton Márquez Abril  ·  AI Developer Junior  ·  Barranquilla, Colombia")
    c.setFillColor(GOLD)
    c.setFont("Inter-600", 7.6)
    c.drawCentredString(W / 2, MB - 17 * mm, "Portfolio: triggerxz.github.io/portfolio")

    c.showPage()
    c.save()
    print(f"PDF saved: {OUT}  ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
