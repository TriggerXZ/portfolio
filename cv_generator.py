"""
CV de Airton Márquez Abril — Edición Editorial Minimalista (claro).
Bilingüe: genera CV-Airton-Marquez.pdf (es) y CV-Airton-Marquez-EN.pdf (en).

Estética: "quiet luxury" — serif Fraunces + sans Inter, blanco + dorado,
numeración editorial, hairlines, mucho aire. 1 página A4.
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
OUT = {
    "es": BASE / "assets" / "CV-Airton-Marquez.pdf",
    "en": BASE / "assets" / "CV-Airton-Marquez-EN.pdf",
}
AVATAR = BASE / "assets" / "avatar.jpg"

# ---------- Textos ----------
T = {
    "es": {
        "title": "CV — Airton Márquez Abril",
        "subject": "AI Developer Junior · Full-Stack Builder",
        "role": "AI DEVELOPER JUNIOR  ·  FULL-STACK BUILDER  ·  CO-FUNDADOR @ SCOOTERCOOP",
        "sec_profile": "Perfil",
        "sec_exp": "Experiencia profesional",
        "sec_edu_main": "Formación académica",
        "profile": ("Desarrollador web orientado a IA generativa y automatización inteligente. "
                    "Co-fundador y desarrollador principal de ScooterCoop, donde llevé la plataforma "
                    "completa de la idea al despliegue: arquitectura, desarrollo y operación. "
                    "Experiencia construyendo soluciones full-stack con Astro, JavaScript/TypeScript, "
                    "Python y SQL, e integrando APIs y modelos de IA (Claude, LLMs) en productos "
                    "en producción. Formación activa en N8N, Docker y cloud (Azure/GCP) para "
                    "soluciones empresariales."),
        "when_scooter": "2025 — Actual",
        "title_scooter": "Co-fundador & Desarrollador principal",
        "company_scooter": "ScooterCoop",
        "bullets_scooter": [
            "Diseño, desarrollo y despliegue de la plataforma completa: sitio web corporativo, software de gestión de alquiler y sistema de reservas en línea.",
            "Soporte técnico, mantenimiento y operación continua del servicio.",
        ],
        "when_rmg": "2022 — 2023",
        "title_rmg": "Desarrollador Full-Stack",
        "company_rmg": "RMG Insurance Service",
        "bullets_rmg": [
            "Desarrollo de componentes de interfaz (UI) responsive e interactivos para el sitio web corporativo.",
            "Elaboración de reportes y soporte a la base de datos.",
        ],
        "edu1_when": "2022 — 2023",
        "edu1_title": "Técnico en Programación Web",
        "edu1_inst": "Universidad del Litoral",
        "edu1_desc": "HTML, CSS, JavaScript, SQL (MySQL), desarrollo full-stack, patrones de diseño responsive.",
        "edu2_when": "2017",
        "edu2_title": "Bachiller",
        "edu2_inst": "Colegio Nuestra Señora del Rosario",
        "side_edu": "Educación",
        "side_tech": "Habilidades técnicas",
        "skills": [
            ("IA & Datos", ["Claude (Code, Skills, Hooks)", "LLMs · RAG · Prompt Eng.", "SQL · MySQL · PostgreSQL"]),
            ("Web & Full-Stack", ["Astro · i18n", "JavaScript · TypeScript", "HTML · CSS · Responsive", "REST APIs · JSON"]),
            ("Automatización", ["Bash scripting", "Python", "GitHub Actions"]),
            ("Deploy & Tools", ["Git · GitHub", "Netlify · Vercel · Render", "VS Code"]),
        ],
        "side_soft": "Habilidades blandas",
        "soft": ["Pensamiento crítico", "Comunicación efectiva", "Negociación",
                 "Adaptabilidad al cambio", "Orientación a resultados"],
        "side_langs": "Idiomas",
        "langs": [("Español", "Nativo"), ("Inglés", "Intermedio (B1/B2)")],
        "footer1": "Airton Márquez Abril  ·  AI Developer Junior  ·  Barranquilla, Colombia",
    },
    "en": {
        "title": "CV — Airton Márquez Abril",
        "subject": "AI Developer Junior · Full-Stack Builder",
        "role": "AI DEVELOPER JUNIOR  ·  FULL-STACK BUILDER  ·  CO-FOUNDER @ SCOOTERCOOP",
        "sec_profile": "Profile",
        "sec_exp": "Professional Experience",
        "sec_edu_main": "Academic Background",
        "profile": ("Web developer focused on generative AI and intelligent automation. "
                    "Co-founder and lead developer at ScooterCoop, where I took the platform "
                    "end-to-end from idea to deployment: architecture, development, and operations. "
                    "Experience building full-stack solutions with Astro, JavaScript/TypeScript, "
                    "Python, and SQL, and integrating APIs and AI models (Claude, LLMs) into "
                    "production products. Actively training in N8N, Docker, and cloud (Azure/GCP) "
                    "for enterprise solutions."),
        "when_scooter": "2025 — Present",
        "title_scooter": "Co-founder & Lead Developer",
        "company_scooter": "ScooterCoop",
        "bullets_scooter": [
            "Design, development, and deployment of the full platform: corporate website, rental management software, and online booking system.",
            "Technical support, maintenance, and continuous service operation.",
        ],
        "when_rmg": "2022 — 2023",
        "title_rmg": "Full-Stack Developer",
        "company_rmg": "RMG Insurance Service",
        "bullets_rmg": [
            "Development of responsive, interactive UI components for the corporate website.",
            "Report generation and database support.",
        ],
        "edu1_when": "2022 — 2023",
        "edu1_title": "Web Development Technician",
        "edu1_inst": "Universidad del Litoral",
        "edu1_desc": "HTML, CSS, JavaScript, SQL (MySQL), full-stack development, responsive design patterns.",
        "edu2_when": "2017",
        "edu2_title": "High School Diploma",
        "edu2_inst": "Colegio Nuestra Señora del Rosario",
        "side_edu": "Education",
        "side_tech": "Technical Skills",
        "skills": [
            ("AI & Data", ["Claude (Code, Skills, Hooks)", "LLMs · RAG · Prompt Engineering", "SQL · MySQL · PostgreSQL"]),
            ("Web & Full-Stack", ["Astro · i18n", "JavaScript · TypeScript", "HTML · CSS · Responsive", "REST APIs · JSON"]),
            ("Automation", ["Bash scripting", "Python", "GitHub Actions"]),
            ("Deploy & Tools", ["Git · GitHub", "Netlify · Vercel · Render", "VS Code"]),
        ],
        "side_soft": "Soft Skills",
        "soft": ["Critical thinking", "Effective communication", "Negotiation",
                 "Adaptability", "Results-oriented"],
        "side_langs": "Languages",
        "langs": [("Spanish", "Native"), ("English", "Intermediate (B1/B2)")],
        "footer1": "Airton Márquez Abril  ·  AI Developer Junior  ·  Barranquilla, Colombia",
    },
}

# ---------- Paleta editorial claro ----------
PAPER      = colors.HexColor("#ffffff")
INK        = colors.HexColor("#161616")
BODY       = colors.HexColor("#3d3d3d")
MUTED      = colors.HexColor("#8a8a8a")
FAINT      = colors.HexColor("#c9c9c9")
HAIRLINE   = colors.HexColor("#e8e6e0")
GOLD       = colors.HexColor("#a87f08")
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
ML = 22 * mm
MR = 22 * mm
MT = 40 * mm
MB = 30 * mm
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
    c.setFillColor(MUTED)
    c.setFont("Inter-500", 8.2)
    c.drawRightString(x + max_w, y + 2, when)
    c.setFillColor(INK)
    c.setFont("Inter-600", 11)
    c.drawString(x, y, title)
    y -= 5.2 * mm
    c.setFillColor(GOLD)
    c.setFont("Inter-600", 8)
    c.drawString(x, y, company.upper())
    y -= 4.6 * mm
    # bullets — un punto por ITEM lógico, continuaciones con indentación colgante
    for ln in lines:
        chunks = wrap(ln, "Inter-400", 9.0, max_w - 5 * mm)
        first = True
        for chunk in chunks:
            if first:
                c.setFillColor(GOLD)
                c.circle(x + 1.3 * mm, y + 1.2, 0.9, fill=1, stroke=0)
                first = False
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


def main(lang):
    t = T[lang]
    out_path = OUT[lang]
    c = canvas.Canvas(str(out_path), pagesize=A4)
    c.setTitle(t["title"])
    c.setAuthor("Airton Márquez Abril")
    c.setSubject(t["subject"])
    c.setCreator("Portfolio Airton Marquez")

    # fondo
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ================= HEADER =================
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(1.2)
    c.line(ML, H - 22 * mm, W - MR, H - 22 * mm)

    # nombre
    c.setFillColor(INK)
    c.setFont("Fraunces-600", 27)
    c.drawString(ML, H - 33 * mm, "Airton Márquez Abril")

    # rol
    c.setFillColor(GOLD)
    c.setFont("Inter-700", 8.2)
    c.drawString(ML, H - 40 * mm, t["role"])

    # contacto (2 filas)
    contact1 = "Barranquilla, CO   ·   kaminatrigger@gmail.com   ·   github.com/TriggerXZ"
    contact2 = "linkedin.com/in/airton-márquez-abril"
    c.setFillColor(MUTED)
    c.setFont("Inter-400", 8.6)
    c.drawString(ML, H - 45.5 * mm, contact1)
    c.drawString(ML + 3 * mm, H - 49 * mm, contact2)

    # avatar circular derecha — 31.2mm diámetro (15.6mm radio)
    draw_avatar(c, W - MR - 17 * mm, H - 42 * mm, 15.6 * mm)

    # ================= COLUMNA PRINCIPAL =================
    y = H - 45.5 * mm - 14 * mm
    x = MAIN_X

    # ---- 01 · Perfil / Profile ----
    y = section_head(c, x, y, "01", t["sec_profile"], MAIN_W)
    y = para(c, x, y - 4 * mm, t["profile"], first_y=y - 4 * mm)
    y -= 8 * mm

    # ---- 02 · Experiencia / Professional Experience ----
    y = section_head(c, x, y, "02", t["sec_exp"], MAIN_W)
    y -= 3 * mm
    y = job_entry(c, x, y - 5 * mm, t["when_scooter"], t["title_scooter"],
        t["company_scooter"], t["bullets_scooter"], MAIN_W)
    y -= 2 * mm
    y = job_entry(c, x, y - 4 * mm, t["when_rmg"], t["title_rmg"],
        t["company_rmg"], t["bullets_rmg"], MAIN_W)
    y -= 7 * mm

    # ---- 03 · Formación / Academic Background ----
    y = section_head(c, x, y, "03", t["sec_edu_main"], MAIN_W)
    y -= 4 * mm
    c.setFillColor(MUTED)
    c.setFont("Inter-500", 8.2)
    c.drawRightString(x + MAIN_W, y, t["edu1_when"])
    c.setFillColor(INK)
    c.setFont("Inter-600", 11)
    c.drawString(x, y, t["edu1_title"])
    y -= 5 * mm
    c.setFillColor(GOLD)
    c.setFont("Inter-600", 8)
    c.drawString(x, y, t["edu1_inst"].upper())
    y -= 4.6 * mm
    y = para(c, x, y, t["edu1_desc"], size=9.0, leading=12.8, max_w=MAIN_W)
    y -= 3 * mm
    c.setFillColor(MUTED)
    c.setFont("Inter-500", 8.2)
    c.drawRightString(x + MAIN_W, y, t["edu2_when"])
    c.setFillColor(INK)
    c.setFont("Inter-600", 11)
    c.drawString(x, y, t["edu2_title"])
    y -= 5 * mm
    c.setFillColor(GOLD)
    c.setFont("Inter-600", 8)
    c.drawString(x, y, t["edu2_inst"].upper())

    # ================= SIDEBAR =================
    sx = SIDEBAR_X
    sy = H - 45.5 * mm - 14 * mm

    # línea vertical separadora
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.6)
    c.line(SIDEBAR_X - GUTTER / 2, sy, SIDEBAR_X - GUTTER / 2, MB + 14 * mm)

    # ---- Educación / Education ----
    c.setFillColor(INK)
    c.setFont("Inter-700", 8.5)
    c.drawString(sx, sy, t["side_edu"].upper())
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(0.8)
    c.line(sx, sy - 3.5, sx + SIDEBAR_W, sy - 3.5)
    sy -= 8 * mm

    for when, title, inst in [
        (t["edu1_when"], t["edu1_title"], t["edu1_inst"]),
        (t["edu2_when"], t["edu2_title"], t["edu2_inst"]),
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

    # ---- Habilidades técnicas / Technical Skills ----
    c.setFillColor(INK)
    c.setFont("Inter-700", 8.5)
    c.drawString(sx, sy, t["side_tech"].upper())
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(0.8)
    c.line(sx, sy - 3.5, sx + SIDEBAR_W, sy - 3.5)
    sy -= 8 * mm

    for cat, items in t["skills"]:
        c.setFillColor(GOLD)
        c.setFont("Inter-600", 8)
        c.drawString(sx, sy, cat.upper())
        sy -= 4.2 * mm
        for it in items:
            sy = skill_item(c, sx, sy, it)
        sy -= 1.6 * mm

    sy -= 1 * mm

    # ---- Habilidades blandas / Soft Skills ----
    c.setFillColor(INK)
    c.setFont("Inter-700", 8.5)
    c.drawString(sx, sy, t["side_soft"].upper())
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(0.8)
    c.line(sx, sy - 3.5, sx + SIDEBAR_W, sy - 3.5)
    sy -= 8 * mm

    for s in t["soft"]:
        sy = skill_item(c, sx, sy, s)
    sy -= 2 * mm

    # ---- Idiomas / Languages ----
    c.setFillColor(INK)
    c.setFont("Inter-700", 8.5)
    c.drawString(sx, sy, t["side_langs"].upper())
    c.setStrokeColor(GOLD_SOFT)
    c.setLineWidth(0.8)
    c.line(sx, sy - 3.5, sx + SIDEBAR_W, sy - 3.5)
    sy -= 8 * mm

    for name, lvl in t["langs"]:
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
    c.drawCentredString(W / 2, MB - 12 * mm, t["footer1"])
    c.setFillColor(GOLD)
    c.setFont("Inter-600", 7.6)
    c.drawCentredString(W / 2, MB - 17 * mm, "Portfolio: triggerxz.github.io/portfolio")

    c.showPage()
    c.save()
    print(f"PDF saved: {out_path}  ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    for lang in ("es", "en"):
        main(lang)
