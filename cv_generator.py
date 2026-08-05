"""
Genera el CV PDF de Airton Márquez Abril.
Estructura: 1 página (A4), estilo sobrio profesional colombiano,
acorde a los requisitos de la convocatoria AOS SAS (Desarrollo IA Junior).

Layout:
  ┌──────────────────────────────────────────────┐
  │ [Foto circular]  AIRTON MÁRQUEZ ABRIL        │
  │                  AI Developer Junior · BAQ   │
  │                  contacto · links            │
  ├──────────────┬───────────────────────────────┤
  │ PERFIL       │ EXPERIENCIA PROFESIONAL       │
  │              │   - Co-fundador ScooterCoop    │
  │ HABILIDADES  │   - Dev Full-Stack RMG         │
  │ TÉCNICAS     │                                │
  │              │ FORMACIÓN                      │
  │ HABILIDADES  │                                │
  │ BLANDAS      │ PROYECTOS DESTACADOS           │
  │              │                                │
  │ IDIOMAS      │ PORTAFOLIO WEB                 │
  └──────────────┴───────────────────────────────┘
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pathlib import Path

OUT = Path(r"D:\Programacion\portfolio\assets\CV-Airton-Marquez.pdf")
AVATAR = Path(r"D:\Programacion\portfolio\assets\avatar.jpg")

# Paleta — dark + gold (consistente con portfolio)
BG          = colors.HexColor("#0a0a0a")
BG_LIGHT    = colors.HexColor("#141414")
LINE        = colors.HexColor("#262626")
GOLD        = colors.HexColor("#f0b90b")
GOLD_DARK   = colors.HexColor("#c99a06")
TEXT        = colors.HexColor("#f5f5f5")
TEXT_2      = colors.HexColor("#a3a3a3")
TEXT_3      = colors.HexColor("#737373")
WHITE       = colors.white
GREEN       = colors.HexColor("#00c853")

# A4
W, H = A4
LEFT_MARGIN = 0
TOP_MARGIN  = 0
SIDE_W      = 70 * mm      # columna izquierda
PAD         = 8 * mm


def draw_avatar(c, cx, cy, diameter):
    """Dibuja el avatar recortado en círculo."""
    if not AVATAR.exists():
        c.circle(cx, cy, diameter / 2, fill=1, stroke=0)
        return
    img = ImageReader(str(AVATAR))
    iw, ih = img.getSize()
    # Crop centrado
    side = min(iw, ih)
    x0 = (iw - side) / 2
    y0 = (ih - side) / 2
    # drawImage con mask circular (path)
    c.saveState()
    p = c.beginPath()
    p.circle(cx, cy, diameter / 2)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(img,
                cx - diameter / 2, cy - diameter / 2,
                width=diameter, height=diameter,
                mask='auto')
    c.restoreState()
    # Border gold
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.circle(cx, cy, diameter / 2, fill=0, stroke=1)


def section_title(c, x, y, text):
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y, text.upper())
    c.setStrokeColor(LINE)
    c.setLineWidth(0.4)
    c.line(x, y - 2, x + 62 * mm, y - 2)


def text_block(c, x, y, lines, leading=10.5, font="Helvetica", size=8.5, color=TEXT_2, max_w=None):
    """Imprime un bloque de texto. lines puede ser str o list."""
    c.setFillColor(color)
    c.setFont(font, size)
    if isinstance(lines, str):
        lines = [lines]
    for line in lines:
        if max_w:
            from reportlab.lib.utils import simpleSplit
            chunks = simpleSplit(line, font, size, max_w)
            for ch in chunks:
                c.drawString(x, y, ch)
                y -= leading
        else:
            c.drawString(x, y, line)
            y -= leading
    return y


def main():
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("CV — Airton Márquez Abril")
    c.setAuthor("Airton Márquez Abril")
    c.setSubject("AI Developer Junior · Full-Stack Builder")
    c.setCreator("Portfolio Airton Marquez")

    # === Background ===
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # === HEADER (full-width, dark gold band) ===
    header_h = 50 * mm
    c.setFillColor(BG_LIGHT)
    c.rect(0, H - header_h, W, header_h, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(0, H - header_h, W, H - header_h)

    # Avatar circular a la izquierda
    avatar_d = 34 * mm
    avatar_cx = 22 * mm
    avatar_cy = H - header_h / 2
    draw_avatar(c, avatar_cx, avatar_cy, avatar_d)

    # Name + role (al lado del avatar)
    tx = 22 * mm + avatar_d / 2 + 8 * mm
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(tx, H - 22 * mm, "AIRTON MÁRQUEZ ABRIL")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(tx, H - 30 * mm, "AI Developer Junior  ·  Full-Stack Builder  ·  Co-fundador @ ScooterCoop")

    # Línea de contacto (debajo del nombre, con íconos simples)
    cy = H - 38 * mm
    contact_items = [
        ("B", "Barranquilla, CO"),
        ("@", "kaminatrigger@gmail.com"),
        ("G", "github.com/TriggerXZ"),
        ("in", "linkedin.com/in/airton-márquez-abril"),
    ]
    x = tx
    for icon, text in contact_items:
        # chip-style con icono en gold
        c.setFillColor(BG)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.4)
        chip_w = 4.5 * mm + c.stringWidth(text, "Helvetica", 8) + 3 * mm
        c.roundRect(x, cy - 3.5 * mm, chip_w, 6.5 * mm, 1.5 * mm, fill=1, stroke=1)
        # icon dot
        c.setFillColor(GOLD)
        c.circle(x + 2.7 * mm, cy, 1.2 * mm, fill=1, stroke=0)
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 8)
        c.drawString(x + 4.5 * mm, cy - 1.3 * mm, text)
        x += chip_w + 2 * mm

    # === LEFT COLUMN ===
    left_x = PAD
    left_w = SIDE_W - PAD
    y_left = H - header_h - 10 * mm

    # Perfil
    section_title(c, left_x, y_left, "Perfil")
    y_left -= 8 * mm
    y_left = text_block(c, left_x, y_left,
        "Desarrollador con base práctica en IA generativa, LLMs y automatización. "
        "Co-fundador de ScooterCoop, donde llevo producto desde cero. "
        "Stack: Astro, JavaScript/TypeScript, Python, Bash, SQL. "
        "En proceso activo de formación en N8N, Docker y cloud (Azure/GCP).",
        leading=10.5, font="Helvetica", size=8.5, color=TEXT_2, max_w=left_w)
    y_left -= 4 * mm

    # Habilidades técnicas
    section_title(c, left_x, y_left, "Habilidades técnicas")
    y_left -= 7 * mm
    tech_skills = [
        ("IA & Datos",     ["Claude (Code, Skills, Hooks)", "LLMs · RAG · Prompt Eng.", "OpenAI · Gemini APIs", "SQL · MySQL · PostgreSQL"]),
        ("Web & Full-Stack", ["Astro · i18n", "JavaScript · TypeScript", "HTML · CSS · Responsive", "REST APIs · JSON"]),
        ("Automatización", ["Bash scripting", "Python", "N8N (en formación)", "GitHub Actions"]),
        ("Deploy & Tools",  ["Git · GitHub", "Netlify · Vercel · Render", "VS Code", "Docker (en formación)"]),
    ]
    for cat, items in tech_skills:
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left_x, y_left, cat)
        y_left -= 4.5 * mm
        for it in items:
            c.setFillColor(GOLD)
            c.circle(left_x + 1.2 * mm, y_left + 0.8 * mm, 0.5 * mm, fill=1, stroke=0)
            c.setFillColor(TEXT)
            c.setFont("Helvetica", 8)
            c.drawString(left_x + 4 * mm, y_left, it)
            y_left -= 3.6 * mm
        y_left -= 1.5 * mm

    # Habilidades blandas
    section_title(c, left_x, y_left, "Habilidades blandas")
    y_left -= 7 * mm
    soft = [
        "Pensamiento crítico",
        "Comunicación efectiva",
        "Negociación",
        "Adaptabilidad al cambio",
        "Orientación a resultados",
    ]
    for s in soft:
        c.setFillColor(GOLD)
        c.circle(left_x + 1.2 * mm, y_left + 0.8 * mm, 0.5 * mm, fill=1, stroke=0)
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 8)
        c.drawString(left_x + 4 * mm, y_left, s)
        y_left -= 3.8 * mm
    y_left -= 3 * mm

    # Idiomas
    section_title(c, left_x, y_left, "Idiomas")
    y_left -= 7 * mm
    langs = [("Español", "Nativo", 1.0), ("Inglés", "Intermedio (B1/B2)", 0.65)]
    for name, lvl, pct in langs:
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 8)
        c.drawString(left_x, y_left, name)
        c.setFillColor(TEXT_2)
        c.setFont("Helvetica", 7.5)
        c.drawRightString(left_x + left_w, y_left, lvl)
        # progress bar
        y_left -= 3 * mm
        bar_w = left_w
        c.setFillColor(LINE)
        c.roundRect(left_x, y_left, bar_w, 1.2 * mm, 0.6 * mm, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(left_x, y_left, bar_w * pct, 1.2 * mm, 0.6 * mm, fill=1, stroke=0)
        y_left -= 5 * mm

    # === RIGHT COLUMN ===
    right_x = SIDE_W + PAD / 2
    right_w = W - right_x - PAD
    y_right = H - header_h - 10 * mm

    # Experiencia
    section_title(c, right_x, y_right, "Experiencia profesional")
    y_right -= 8 * mm

    # --- ScooterCoop ---
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(right_x, y_right, "2025 — Actual")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawRightString(right_x + right_w, y_right, "Co-fundador & Desarrollador principal")
    y_right -= 5 * mm
    c.setFillColor(GOLD_DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(right_x, y_right, "ScooterCoop  ·  Alquiler de scooters eléctricos, Malecón del Río (BAQ)")
    y_right -= 5 * mm
    y_right = text_block(c, right_x, y_right,
        "Producto desde cero: sitio web, sistema de reservas, marca y operación. "
        "Stack: Astro, JavaScript, Netlify, WhatsApp API. Resultados en producción: "
        "1,240+ rutas, 2,340 reseñas verificadas, rating 4.8/5.",
        leading=10.5, size=8.5, color=TEXT_2, max_w=right_w)
    y_right -= 3 * mm

    # --- RMG ---
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(right_x, y_right, "2022 — 2023")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawRightString(right_x + right_w, y_right, "Desarrollador Full-Stack")
    y_right -= 5 * mm
    c.setFillColor(GOLD_DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(right_x, y_right, "RMG Insurance Service  ·  Sector seguros")
    y_right -= 5 * mm
    y_right = text_block(c, right_x, y_right,
        "Creación de componentes UI para el sitio web (diseño responsive, "
        "interactividad), envío de reportes periódicos y soporte a base de datos.",
        leading=10.5, size=8.5, color=TEXT_2, max_w=right_w)
    y_right -= 4 * mm

    # Formación
    section_title(c, right_x, y_right, "Formación académica")
    y_right -= 8 * mm

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(right_x, y_right, "2022 — 2023")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(right_x + 22 * mm, y_right, "Técnico en Programación Web")
    y_right -= 4.5 * mm
    c.setFillColor(GOLD_DARK)
    c.setFont("Helvetica", 8.5)
    c.drawString(right_x, y_right, "Universidad del Litoral")
    y_right -= 4.5 * mm
    y_right = text_block(c, right_x, y_right,
        "HTML, CSS, JavaScript, SQL (MySQL), desarrollo full-stack, "
        "patrones de diseño responsive.",
        leading=10, size=8, color=TEXT_2, max_w=right_w)
    y_right -= 2 * mm

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(right_x, y_right, "2017")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(right_x + 22 * mm, y_right, "Bachiller")
    y_right -= 4.5 * mm
    c.setFillColor(GOLD_DARK)
    c.setFont("Helvetica", 8.5)
    c.drawString(right_x, y_right, "Colegio Nuestra Señora del Rosario")
    y_right -= 6 * mm

    # Formación continua
    section_title(c, right_x, y_right, "Formación continua (en curso)")
    y_right -= 7 * mm
    courses = [
        "LLMs, agentes IA y prompt engineering (práctica en producción)",
        "Cloud: Azure Fundamentals & Google Cloud Platform",
        "Docker y orquestación de contenedores",
        "N8N — automatización de flujos no-code/low-code",
    ]
    for it in courses:
        c.setFillColor(GOLD)
        c.circle(right_x + 1.2 * mm, y_right + 0.8 * mm, 0.5 * mm, fill=1, stroke=0)
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 8)
        c.drawString(right_x + 4 * mm, y_right, it)
        y_right -= 3.8 * mm
    y_right -= 3 * mm

    # Proyectos destacados
    section_title(c, right_x, y_right, "Proyectos destacados")
    y_right -= 7 * mm
    projects = [
        ("block-destructive-commands",
         "Hook de seguridad para Claude Code — 22/22 tests pasan. MIT-licensed.",
         "github.com/TriggerXZ/block-destructive-commands"),
        ("generate-changelog",
         "Auto-generador de CHANGELOG.md desde git history. Zero deps.",
         "github.com/TriggerXZ/generate-changelog"),
        ("ScooterCoop",
         "Plataforma de alquiler de scooters · 1,240+ riders · rating 4.8/5",
         "scootercoop.netlify.app"),
        ("Versio",
         "Comparador de documentos · procesamiento 100% local",
         "verzi.netlify.app"),
    ]
    for name, desc, url in projects:
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(right_x, y_right, name)
        c.setFillColor(TEXT_2)
        c.setFont("Helvetica", 7.5)
        c.drawRightString(right_x + right_w, y_right, "↗")
        y_right -= 3.6 * mm
        c.setFillColor(TEXT_2)
        c.setFont("Helvetica", 7.5)
        c.drawString(right_x, y_right, desc)
        y_right -= 3.2 * mm
        c.setFillColor(TEXT_3)
        c.setFont("Helvetica", 7)
        c.drawString(right_x, y_right, url)
        y_right -= 4.2 * mm

    # === FOOTER ===
    c.setFillColor(BG_LIGHT)
    c.rect(0, 0, W, 10 * mm, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.4)
    c.line(0, 10 * mm, W, 10 * mm)
    c.setFillColor(TEXT_3)
    c.setFont("Helvetica", 7)
    c.drawString(PAD, 4 * mm, "Airton Márquez Abril  ·  AI Developer Junior  ·  Barranquilla, Colombia")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7)
    c.drawRightString(W - PAD, 4 * mm, "Portfolio: triggerxz.github.io/portfolio")

    c.showPage()
    c.save()
    print(f"PDF saved: {OUT}  ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
