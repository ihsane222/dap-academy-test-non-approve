#!/usr/bin/env python3
"""
DAP Academy — Génération des fiches imprimables
Génère un fichier HTML par module dans le dossier printable/
Usage : python generate_printable.py
        python generate_printable.py --with-quiz   (pour inclure le quiz)
"""

import os
import re
import glob
import sys
import html

# ─── Configuration ─────────────────────────────────────────────────────────────
MODULES_DIR = "modules"
OUTPUT_DIR  = "printable"
WITH_QUIZ   = "--with-quiz" in sys.argv

# ─── Palette DAP ──────────────────────────────────────────────────────────────
DOMAIN_STYLES = {
    "assurances":     {"bg": "#EFF6FB", "primary": "#2A4B62", "accent": "#37A1D7", "light": "#D6EAF5"},
    "digital":        {"bg": "#EFF8F0", "primary": "#1D6B2F", "accent": "#34A853", "light": "#C8EDCF"},
    "reglementation": {"bg": "#FFF7ED", "primary": "#C2410C", "accent": "#F97316", "light": "#FFEDD5"},
    "it":             {"bg": "#FFF1F2", "primary": "#9B1C1C", "accent": "#EF4444", "light": "#FECACA"},
    "produits":       {"bg": "#F5F0FF", "primary": "#5B21B6", "accent": "#8B5CF6", "light": "#DDD6FE"},
}

def get_domain_style(domaine: str) -> dict:
    d = domaine.lower()
    if "digital" in d or "outil" in d:  return DOMAIN_STYLES["digital"]
    if "règle" in d or "regle" in d or "rgpd" in d or "aml" in d: return DOMAIN_STYLES["reglementation"]
    if "produit" in d:                  return DOMAIN_STYLES["produits"]
    if d == "it" or d.startswith("it ") or " it" in d or "cyber" in d: return DOMAIN_STYLES["it"]
    return DOMAIN_STYLES["assurances"]

# ─── Parsing markdown ──────────────────────────────────────────────────────────
def parse_module(content: str):
    lines = content.split("\n")
    title = lines[0].replace("#", "").strip() if lines else ""

    meta = {}
    if len(lines) > 1:
        raw = lines[1]
        for key, pattern in [
            ("domaine", r"\*\*Domaine\s*:\*\*\s*([^·]+)"),
            ("duree",   r"\*\*Dur[eé]e\s*:\*\*\s*([^·]+)"),
            ("format",  r"\*\*Format\s*:\*\*\s*([^·]+)"),
            ("public",  r"\*\*Public\s*:\*\*\s*([^·]+)"),
            ("mois",    r"\*\*Mois\s*:\*\*\s*([^·\n]+)"),
        ]:
            m = re.search(pattern, raw)
            meta[key] = m.group(1).strip() if m else ""

    # Contenu sans le quiz (par défaut)
    quiz_idx = content.find("## Quiz de validation")
    body_raw = content[:quiz_idx].strip() if (not WITH_QUIZ and quiz_idx > 0) else content
    # Retirer les 2 premières lignes (titre + meta déjà traités)
    body_lines = body_raw.split("\n")[2:]
    body = "\n".join(body_lines).strip()

    quiz_raw = ""
    if WITH_QUIZ and quiz_idx > 0:
        quiz_raw = content[quiz_idx:]

    return title, meta, body, quiz_raw


def md_to_html(text: str) -> str:
    """Conversion Markdown → HTML sans dépendance externe."""
    lines = text.split("\n")
    html_parts = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Tables markdown
        if "|" in line and i + 1 < len(lines) and re.match(r"^\|[-| :]+\|$", lines[i+1].strip()):
            table_lines = [line]
            j = i + 2
            while j < len(lines) and "|" in lines[j]:
                table_lines.append(lines[j])
                j += 1
            html_parts.append(render_table(table_lines))
            i = j
            continue

        # Séparateurs
        if re.match(r"^---+$", line.strip()):
            html_parts.append("<hr>")
            i += 1
            continue

        # Titres
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            content_h = inline_md(m.group(2))
            html_parts.append(f"<h{level}>{content_h}</h{level}>")
            i += 1
            continue

        # Listes numérotées
        if re.match(r"^\d+\.\s", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i]):
                cleaned = re.sub(r"^\d+\.\s", "", lines[i])
                items.append("<li>" + inline_md(cleaned) + "</li>")
                i += 1
            html_parts.append("<ol>" + "".join(items) + "</ol>")
            continue

        # Listes à puces
        if re.match(r"^[-*]\s", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s", lines[i]):
                cleaned = re.sub(r"^[-*]\s", "", lines[i])
                items.append("<li>" + inline_md(cleaned) + "</li>")
                i += 1
            html_parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        # Paragraphe normal (ignorer les lignes vides)
        if line.strip():
            html_parts.append(f"<p>{inline_md(line)}</p>")
        else:
            pass  # espace vide → pas de balise

        i += 1

    return "\n".join(html_parts)


def render_table(table_lines: list) -> str:
    rows = []
    for idx, raw in enumerate(table_lines):
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if idx == 0:
            row = "<tr>" + "".join(f"<th>{inline_md(c)}</th>" for c in cells) + "</tr>"
        elif re.match(r"^[-| :]+$", raw.strip()):
            continue
        else:
            row = "<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in cells) + "</tr>"
        rows.append(row)
    return "<table>" + "".join(rows) + "</table>"


def inline_md(text: str) -> str:
    """Convertit la mise en forme inline : gras, italique, code, ✅."""
    # Échapper HTML d'abord, puis remettre les balises
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*",     r"<em>\1</em>",         text)
    text = re.sub(r"`(.+?)`",       r"<code>\1</code>",      text)
    text = text.replace("✅", '<span class="check">✅</span>')
    return text


# ─── Génération HTML ───────────────────────────────────────────────────────────
def generate_html(num: str, title: str, meta: dict, body_html: str, quiz_html: str) -> str:
    style = get_domain_style(meta.get("domaine", ""))
    primary = style["primary"]
    accent  = style["accent"]
    bg      = style["bg"]
    light   = style["light"]

    duree  = meta.get("duree", "")
    format_= meta.get("format", "")
    public = meta.get("public", "")
    mois   = meta.get("mois", "")

    badges = "".join([
        f'<span class="badge" style="background:{light};color:{primary}">📚 {meta.get("domaine","")}</span>' if meta.get("domaine") else "",
        f'<span class="badge" style="background:#e8f5e9;color:#1B5E20">⏱ {duree}</span>'  if duree  else "",
        f'<span class="badge" style="background:#EFF6FB;color:#1565C0">📋 {format_}</span>' if format_ else "",
        f'<span class="badge" style="background:#FFF8E1;color:#E65100">👥 {public}</span>'  if public else "",
        f'<span class="badge" style="background:#F3E5F5;color:#4A148C">📅 {mois}</span>'    if mois   else "",
    ])

    quiz_section = f"""
    <div class="quiz-section">
        <h2>Quiz de validation</h2>
        {quiz_html}
    </div>""" if quiz_html else ""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DAP Academy — {title}</title>
<style>
  /* ── Reset & Base ── */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Segoe UI', Calibri, 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.65;
    color: #1a1a1a;
    background: white;
    padding: 0;
  }}

  /* ── En-tête ── */
  .header {{
    background: linear-gradient(135deg, {primary} 0%, {accent} 100%);
    color: white;
    padding: 28px 40px 22px;
    position: relative;
  }}
  .header-num {{
    font-size: 9pt;
    opacity: 0.7;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}
  .header-title {{
    font-size: 20pt;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 14px;
  }}
  .badges {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 8.5pt;
    font-weight: 600;
  }}
  .header-logo {{
    position: absolute;
    top: 24px; right: 40px;
    font-size: 22pt;
    font-weight: 800;
    opacity: 0.18;
    letter-spacing: -1px;
  }}

  /* ── Contenu ── */
  .content {{
    padding: 30px 40px 40px;
    max-width: 900px;
    margin: 0 auto;
  }}

  h2 {{
    font-size: 13pt;
    font-weight: 700;
    color: {primary};
    border-bottom: 2px solid {accent};
    padding-bottom: 5px;
    margin: 26px 0 12px;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 11.5pt;
    font-weight: 700;
    color: {primary};
    margin: 18px 0 8px;
    page-break-after: avoid;
  }}
  h4 {{
    font-size: 10.5pt;
    font-weight: 700;
    color: #444;
    margin: 12px 0 6px;
    page-break-after: avoid;
  }}
  p {{ margin: 0 0 8px; }}

  ul, ol {{
    margin: 6px 0 10px 22px;
    padding: 0;
  }}
  li {{ margin-bottom: 3px; }}

  strong {{ color: {primary}; font-weight: 700; }}
  em {{ font-style: italic; color: #444; }}
  code {{
    background: #f0f4f8;
    border: 1px solid #d0d8e4;
    border-radius: 3px;
    padding: 1px 5px;
    font-family: 'Courier New', monospace;
    font-size: 9.5pt;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e0e7ef;
    margin: 18px 0;
  }}

  /* ── Tableaux ── */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px;
    font-size: 10pt;
    page-break-inside: avoid;
  }}
  th {{
    background: {primary};
    color: white;
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 9.5pt;
  }}
  td {{
    padding: 7px 12px;
    border-bottom: 1px solid #e8eef4;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{ background: {bg}; }}
  tr:hover td {{ background: {light}; }}

  /* ── Quiz ── */
  .quiz-section {{
    background: {bg};
    border-left: 4px solid {accent};
    border-radius: 6px;
    padding: 20px 24px;
    margin-top: 28px;
    page-break-inside: avoid;
  }}
  .quiz-section h2 {{
    border-bottom-color: {light};
    margin-top: 0;
  }}
  .check {{ color: #16a34a; }}

  /* ── Pied de page ── */
  .footer {{
    text-align: center;
    font-size: 8pt;
    color: #999;
    border-top: 1px solid #eee;
    padding: 12px 40px;
    margin-top: 20px;
  }}

  /* ── Impression ── */
  @media print {{
    @page {{
      size: A4;
      margin: 0;
    }}
    body {{ background: white; }}
    .header {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    th {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    tr:nth-child(even) td {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .quiz-section {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    h2, h3, h4 {{ page-break-after: avoid; }}
    table {{ page-break-inside: avoid; }}
    .no-print {{ display: none; }}
  }}
</style>
</head>
<body>

<!-- Bouton imprimer (masqué à l'impression) -->
<div class="no-print" style="background:#f8f9fa;padding:10px 40px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #ddd;">
  <button onclick="window.print()" style="background:{accent};color:white;border:none;padding:8px 20px;border-radius:6px;font-size:10pt;cursor:pointer;font-weight:600;">
    🖨️ Imprimer / Exporter en PDF
  </button>
  <span style="color:#666;font-size:9pt;">Astuce : dans la boîte de dialogue d'impression, choisissez "Enregistrer en PDF" pour obtenir un PDF.</span>
</div>

<!-- En-tête -->
<div class="header">
  <div class="header-logo">DAP</div>
  <div class="header-num">Module {num} · DAP Academy 2026</div>
  <div class="header-title">{html.escape(title)}</div>
  <div class="badges">{badges}</div>
</div>

<!-- Contenu principal -->
<div class="content">
  {body_html}
  {quiz_section}
</div>

<!-- Pied de page -->
<div class="footer">
  DAP Academy 2026 · Plan Global de Formation · 19 modules · 46h · Conformité FSMA<br>
  Ce document est à usage interne exclusif — DAP sa, Boulevard du Souverain 280, 1160 Bruxelles
</div>

</body>
</html>"""


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = sorted(glob.glob(f"{MODULES_DIR}/[0-9]*.md"))
    count = 0

    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as fp:
            content = fp.read()

        num = os.path.basename(filepath).split("_")[0]
        if num == "00":
            continue

        title, meta, body, quiz_raw = parse_module(content)
        body_html = md_to_html(body)
        quiz_html = md_to_html(quiz_raw) if quiz_raw else ""

        html_content = generate_html(num, title, meta, body_html, quiz_html)

        out_name = os.path.basename(filepath).replace(".md", ".html")
        out_path = os.path.join(OUTPUT_DIR, out_name)

        with open(out_path, "w", encoding="utf-8") as fp:
            fp.write(html_content)

        print(f"  ✅ Module {num} → {out_path}")
        count += 1

    print(f"\n🎉 {count} fiches générées dans le dossier '{OUTPUT_DIR}/'")
    print("   Ouvrez chaque fichier HTML dans votre navigateur,")
    print("   puis Ctrl+P → 'Enregistrer en PDF' pour exporter en PDF.")

    if not WITH_QUIZ:
        print("\n   ℹ️  Quiz non inclus. Ajoutez --with-quiz pour l'inclure.")


if __name__ == "__main__":
    main()
