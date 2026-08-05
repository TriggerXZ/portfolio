"""
Genera el CV PDF de Airton Márquez Abril.

Estructura minimalista (mercado colombiano, 1 página A4):

  ┌──────────────────┬───────────────────────────┐
  │ EDUCACIÓN        │ PERFIL                    │
  │ (sidebar)        │ (columna principal, arriba)│
  │                  │                           │
  │ HABILIDADES      │ EXPERIENCIA PROFESIONAL   │
  │ TÉCNICAS         │                           │
  │                  │ FORMACIÓN ACADÉMICA       │
  │ IDIOMAS          │                           │
  │                  │                           │
  └──────────────────┴───────────────────────────┘

Fuera (van en el portfolio):
  - Proyectos destacados
  - Formación continua
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pathlib import Path

OUT = Path(r"D:\Programacion\portfolio\assets\CV-Airton-Marquez.pdf")
AVATAR = Path(r"D:\Programacion\portfolio\assets\avatar.jpg")

# Paleta
BG          = colors.HexColor("#0a0a0a")
BG_LIGHT    = colors.HexColor("#141414")
LINE        = colors.HexColor("#262626")
GOLD        = colors.HexColor("#f0b90b")
GOLD_DARK   = colors.HexColor("#c99a06")
TEXT        = colors.HexColor("#f5f5f5")
TEXT_2      = colors.HexColor("#a3a3a3")
TEXT_3      = colors.HexColor("#737373")

W, H = A4
SIDE_W = 62 * mm    # sidebar
PAD = 8 * mm
HEADER_H = 48 * mm


def draw_avatar(c, cx, cy, diameter):
    if not AVATAR.exists():
        c.circle(cx, cy, diameter / 2, fill=1, stroke=0)
        return
    img = ImageReader(str(AVATAR))
    iw, ih = img.getSize()
    c.saveState()
    p = c.beginPath()
    p.circle(cx, cy, diameter / 2)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(img,
                cx - diameter / 2, cy - diameter / 2,
                width=diameter, height=diameter,
                mask='auto')
    c.restoreState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.circle(cx, cy, diameter / 2, fill=0, stroke=1)


def section_title(c, x, y, text, width):
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y, text.upper())
    c.setStrokeColor(LINE)
    c.setLineWidth(0.4)
    c.line(x, y - 2, x + width, y - 2)


def text_block(c, x, y, lines, leading=10.5, font="Helvetica", size=8.5, color=TEXT_2, max_w=None):
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

    # === HEADER ===
    c.setFillColor(BG_LIGHT)
    c.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(0, H - HEADER_H, W, H - HEADER_H)

    # Avatar
    avatar_d = 32 * mm
    avatar_cx = 20 * mm
    avatar_cy = H - HEADER_H / 2
    draw_avatar(c, avatar_cx, avatar_cy, avatar_d)

    # Name + role
    tx = 20 * mm + avatar_d / 2 + 8 * mm
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(tx, H - 20 * mm, "AIRTON MÁRQUEZ ABRIL")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(tx, H - 28 * mm, "AI Developer Junior  ·  Full-Stack Builder  ·  Co-fundador @ ScooterCoop")

    # Contact chips
    cy = H - 36 * mm
    contact_items = [
        ("B",  "Barranquilla, CO"),
        ("@",  "kaminatrigger@gmail.com"),
        ("G",  "github.com/TriggerXZ"),
        ("in", "linkedin.com/in/airton-márquez-abril"),
    ]
    x = tx
    for icon, text in contact_items:
        c.setFillColor(BG)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.4)
        chip_w = 4.5 * mm + c.stringWidth(text, "Helvetica", 8) + 3 * mm
        c.roundRect(x, cy - 3.5 * mm, chip_w, 6.5 * mm, 1.5 * mm, fill=1, stroke=1)
        c.setFillColor(GOLD)
        c.circle(x + 2.7 * mm, cy, 1.2 * mm, fill=1, stroke=0)
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 8)
        c.drawString(x + 4.5 * mm, cy - 1.3 * mm, text)
        x += chip_w + 2 * mm

    # === SIDEBAR (left) ===
    side_x = PAD
    side_w = SIDE_W - PAD
    y_side = H - HEADER_H - 10 * mm

    # Educación
    section_title(c, side_x, y_side, "Educación", side_w)
    y_side -= 8 * mm

    edu = [
        ("2022 — 2023", "Técnico en Programación Web", "Universidad del Litoral"),
        ("2017",        "Bachiller",                   "Colegio Nuestra Señora del Rosario"),
    ]
    for when, title, inst in edu:
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(side_x, y_side, when)
        y_side -= 3.8 * mm
        c.setFillColor(TEXT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(side_x, y_side, title)
        y_side -= 3.6 * mm
        c.setFillColor(TEXT_3)
        c.setFont("Helvetica", 8)
        c.drawString(side_x, y_side, inst)
        y_side -= 5.5 * mm

    y_side -= 2 * mm

    # Habilidades técnicas
    section_title(c, side_x, y_side, "Habilidades técnicas", side_w)
    y_side -= 7 * mm

    tech_skills = [
        ("IA & Datos",       ["Claude (Code, Skills, Hooks)", "LLMs · RAG · Prompt Eng.", "SQL · MySQL · PostgreSQL"]),
        ("Web & Full-Stack", ["Astro · i18n", "JavaScript · TypeScript", "HTML · CSS · Responsive", "REST APIs · JSON"]),
        ("Automatización",   ["Bash scripting", "Python", "GitHub Actions"]),
        ("Deploy & Tools",   ["Git · GitHub", "Netlify · Vercel · Render", "VS Code"]),
    ]
    for cat, items in tech_skills:
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(side_x, y_side, cat)
        y_side -= 4 * mm
        for it in items:
            c.setFillColor(GOLD)
            c.circle(side_x + 1.2 * mm, y_side + 0.8 * mm, 0.5 * mm, fill=1, stroke=0)
            c.setFillColor(TEXT)
            c.setFont("Helvetica", 8)
            c.drawString(side_x + 4 * mm, y_side, it)
            y_side -= 3.6 * mm
        y_side -= 1.2 * mm

    y_side -= 1 * mm

    # Habilidades blandas (compactas)
    section_title(c, side_x, y_side, "Habilidades blandas", side_w)
    y_side -= 7 * mm
    soft = ["Pensamiento crítico", "Comunicación efectiva", "Negociación", "Adaptabilidad al cambio", "Orientación a resultados"]
    for s in soft:
        c.setFillColor(GOLD)
        c.circle(side_x + 1.2 * mm, y_side + 0.8 * mm, 0.5 * mm, fill=1, stroke=0)
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 8)
        c.drawString(side_x + 4 * mm, y_side, s)
        y_side -= 3.6 * mm
    y_side -= 3 * mm

    # Idiomas
    section_title(c, side_x, y_side, "Idiomas", side_w)
    y_side -= 7 * mm
    langs = [("Español", "Nativo", 1.0), ("Inglés", "Intermedio (B1/B2)", 0.65)]
    for name, lvl, pct in langs:
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 8)
        c.drawString(side_x, y_side, name)
        c.setFillColor(TEXT_2)
        c.setFont("Helvetica", 7.5)
        c.drawRightString(side_x + side_w, y_side, lvl)
        y_side -= 3 * mm
        c.setFillColor(LINE)
        c.roundRect(side_x, y_side, side_w, 1.2 * mm, 0.6 * mm, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(side_x, y_side, side_w * pct, 1.2 * mm, 0.6 * mm, fill=1, stroke=0)
        y_side -= 5 * mm

    # === MAIN COLUMN (right) ===
    main_x = SIDE_W + PAD / 2
    main_w = W - main_x - PAD
    y_main = H - HEADER_H - 10 * mm

    # Perfil (arriba del main)
    section_title(c, main_x, y_main, "Perfil", main_w)
    y_main -= 8 * mm
    y_main = text_block(c, main_x, y_main,
        "Desarrollador con base práctica en IA generativa, LLMs y automatización. "
        "Co-fundador de ScooterCoop, donde llevo producto desde cero. "
        "Stack principal: Astro, JavaScript/TypeScript, Python, Bash, SQL. "
        "En proceso activo de formación en N8N, Docker y cloud (Azure/GCP) para "
        "cerrar el stack completo de soluciones empresariales.",
        leading=11, size=9, color=TEXT, max_w=main_w)
    y_main -= 5 * mm

    # Experiencia profesional
    section_title(c, main_x, y_main, "Experiencia profesional", main_w)
    y_main -= 8 * mm

    # --- ScooterCoop ---
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(main_x, y_main, "2025 — Actual")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(main_x + main_w, y_main, "Co-fundador & Desarrollador principal")
    y_main -= 5 * mm
    c.setFillColor(GOLD_DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(main_x, y_main, "ScooterCoop  ·  Alquiler de scooters eléctricos, Malecón del Río (BAQ)")
    y_main -= 5 * mm
    y_main = text_block(c, main_x, y_main,
        "Producto desde cero: sitio web, sistema de reservas, marca y operación. "
        "Stack: Astro, JavaScript, Netlify, WhatsApp API. Resultados en producción: "
        "1,240+ rutas, 2,340 reseñas verificadas, rating 4.8/5.",
        leading=11, size=8.5, color=TEXT_2, max_w=main_w)
    y_main -= 3 * mm

    # --- RMG ---
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(main_x, y_main, "2022 — 2023")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(main_x + main_w, y_main, "Desarrollador Full-Stack")
    y_main -= 5 * mm
    c.setFillColor(GOLD_DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(main_x, y_main, "RMG Insurance Service  ·  Sector seguros")
    y_main -= 5 * mm
    y_main = text_block(c, main_x, y_main,
        "Creación de componentes UI para el sitio web (diseño responsive, "
        "interactividad), envío de reportes periódicos y soporte a base de datos.",
        leading=11, size=8.5, color=TEXT_2, max_w=main_w)
    y_main -= 4 * mm

    # Formación académica (en main)
    section_title(c, main_x, y_main, "Formación académica", main_w)
    y_main -= 8 * mm

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(main_x, y_main, "2022 — 2023")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(main_x + 22 * mm, y_main, "Técnico en Programación Web")
    y_main -= 5 * mm
    c.setFillColor(GOLD_DARK)
    c.setFont("Helvetica", 9)
    c.drawString(main_x, y_main, "Universidad del Litoral")
    y_main -= 5 * mm
    y_main = text_block(c, main_x, y_main,
        "HTML, CSS, JavaScript, SQL (MySQL), desarrollo full-stack, "
        "patrones de diseño responsive.",
        leading=10.5, size=8.5, color=TEXT_2, max_w=main_w)
    y_main -= 2 * mm

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(main_x, y_main, "2017")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(main_x + 22 * mm, y_main, "Bachiller")
    y_main -= 5 * mm
    c.setFillColor(GOLD_DARK)
    c.setFont("Helvetica", 9)
    c.drawString(main_x, y_main, "Colegio Nuestra Señora del Rosario")
    y_main -= 6 * mm

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
