import streamlit as st
import os
import re
import glob

# ─── Configuration ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DAP Academy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white; padding: 30px; border-radius: 12px;
        margin-bottom: 20px; text-align: center;
    }
    .module-card {
        background: #f8f9fa; border-radius: 8px;
        padding: 15px; margin: 8px 0;
        border-left: 4px solid #1a1a2e;
        cursor: pointer;
    }
    .badge {
        display: inline-block; padding: 2px 8px;
        border-radius: 12px; font-size: 0.75em;
        font-weight: bold; margin: 2px;
    }
    .badge-blue   { background:#e3f2fd; color:#1565c0; }
    .badge-green  { background:#e8f5e9; color:#2e7d32; }
    .badge-orange { background:#fff3e0; color:#e65100; }
    .stProgress > div > div { background-color: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

MODULES_DIR = "modules"

DOMAIN_COLORS = {
    "Assurances": "badge-blue",
    "Outils Digitaux": "badge-green",
    "Réglementation": "badge-orange",
    "IT": "badge-orange",
    "Produits d'assurance": "badge-blue",
}

# ─── Chargement des modules ───────────────────────────────────────────────────
@st.cache_data
def load_modules():
    files = sorted(glob.glob(f"{MODULES_DIR}/[0-9]*.md"))
    modules = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        lines = content.split("\n")
        title = lines[0].replace("#", "").strip() if lines else os.path.basename(f)

        # Parse metadata from line 2 (ex: **Domaine :** Assurances · **Durée :** 4h ...)
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

        num = os.path.basename(f).split("_")[0]
        modules.append({
            "filename": os.path.basename(f),
            "path": f,
            "title": title,
            "content": content,
            "number": num,
            "meta": meta,
        })
    return modules


# ─── Parsing quiz ─────────────────────────────────────────────────────────────
def parse_quiz(content):
    quiz_section = re.search(r"## Quiz de validation.*?(?=\n---|\Z)", content, re.DOTALL)
    if not quiz_section:
        return []
    quiz_text = quiz_section.group(0)
    questions = []
    q_blocks = re.split(r"\*\*Q\d+\.\*\*\s*", quiz_text)[1:]
    for block in q_blocks:
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        question_text = lines[0]
        options, correct = [], None
        for line in lines[1:]:
            m = re.match(r"[-–]\s*([a-d])\)\s*(.*?)(\s*✅)?\s*$", line)
            if m:
                letter, text, tick = m.group(1), m.group(2).strip(), bool(m.group(3))
                options.append({"letter": letter, "text": text, "correct": tick})
                if tick:
                    correct = letter
        if options and correct:
            questions.append({"question": question_text, "options": options, "correct": correct})
    return questions


def content_without_quiz(content):
    idx = content.find("## Quiz de validation")
    return content[:idx] if idx > 0 else content


# ─── Page : Accueil ───────────────────────────────────────────────────────────
def page_home(modules):
    st.markdown("""
    <div class="main-header">
        <h1>🎓 DAP Academy</h1>
        <p style="font-size:1.1em; margin:0;">Plan Global de Formation 2026 · 19 modules · 46h · Conformité FSMA</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📚 Modules disponibles")
    cols = st.columns(3)
    for i, mod in enumerate(modules):
        if mod["number"] == "00":
            continue
        meta = mod["meta"]
        domain_badge = DOMAIN_COLORS.get(meta.get("domaine", ""), "badge-blue")
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"**{mod['title']}**")
                st.markdown(
                    f'<span class="badge {domain_badge}">{meta.get("domaine","")}</span> '
                    f'<span class="badge badge-green">⏱ {meta.get("duree","")}</span> '
                    f'<span class="badge badge-orange">📅 {meta.get("mois","")}</span>',
                    unsafe_allow_html=True
                )
                if st.button("Accéder →", key=f"home_btn_{mod['number']}", use_container_width=True):
                    st.session_state["page"] = mod["number"]
                    st.rerun()


# Mapping module number → fichier vidéo local
VIDEO_FILES = {
    "01": "videos/DAPModule01.mp4",
}

# ─── Page : Module ────────────────────────────────────────────────────────────
def page_module(module):
    if st.button("← Retour aux modules"):
        st.session_state["page"] = "home"
        st.rerun()

    # Lecteur vidéo si une animation existe pour ce module
    video_path = VIDEO_FILES.get(module["number"])
    if video_path and os.path.exists(video_path):
        st.markdown("### 🎬 Animation du module")
        st.video(video_path)
        st.markdown("---")

    st.markdown(content_without_quiz(module["content"]))

    st.markdown("---")
    st.markdown("## 🎯 Quiz de validation")

    questions = parse_quiz(module["content"])
    if not questions:
        st.info("Pas de quiz pour ce module.")
        return

    qkey = f"quiz_{module['number']}"
    if f"{qkey}_score" not in st.session_state:
        st.session_state[f"{qkey}_score"] = None

    with st.form(f"form_{module['number']}"):
        answers = {}
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}.** {q['question']}")
            opts = [f"{o['letter']}) {o['text']}" for o in q["options"]]
            chosen = st.radio("", opts, key=f"{qkey}_q{i}", label_visibility="collapsed")
            answers[i] = chosen[0] if chosen else None
            st.markdown("")

        submitted = st.form_submit_button("✅ Valider le quiz", type="primary", use_container_width=True)

    if submitted:
        score = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["correct"])
        pct = (score / len(questions)) * 100
        st.session_state[f"{qkey}_score"] = (score, len(questions), pct, answers)

    if st.session_state[f"{qkey}_score"]:
        score, total, pct, saved_answers = st.session_state[f"{qkey}_score"]
        st.markdown("---")
        if pct >= 80:
            st.success(f"🏆 Excellent ! **{score}/{total}** — {pct:.0f}% — Module validé !")
        elif pct >= 60:
            st.warning(f"👍 Bien ! **{score}/{total}** — {pct:.0f}% — Quelques points à revoir")
        else:
            st.error(f"📖 **{score}/{total}** — {pct:.0f}% — Relisez le module avant de recommencer")

        with st.expander("📋 Voir les réponses correctes"):
            for i, q in enumerate(questions):
                correct_opt = next((o for o in q["options"] if o["correct"]), None)
                user = saved_answers.get(i)
                icon = "✅" if user == q["correct"] else "❌"
                st.markdown(f"{icon} **Q{i+1}.** Bonne réponse : **{q['correct']}) {correct_opt['text'] if correct_opt else ''}**")


# ─── Sidebar ──────────────────────────────────────────────────────────────────
def sidebar(modules):
    with st.sidebar:
        st.markdown("## 🎓 DAP Academy")
        st.markdown("---")
        if st.button("🏠 Accueil", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()
        st.markdown("---")
        st.markdown("**Modules**")
        for mod in modules:
            if mod["number"] == "00":
                continue
            label = f"{mod['number']} · {mod['title'].split('—')[-1].strip()[:35]}"
            if st.button(label, key=f"sb_{mod['number']}", use_container_width=True):
                st.session_state["page"] = mod["number"]
                st.rerun()
        st.markdown("---")
        st.caption("46h · 19 modules · FSMA ✅")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    modules = load_modules()
    sidebar(modules)

    page = st.session_state["page"]
    if page == "home":
        page_home(modules)
    else:
        mod = next((m for m in modules if m["number"] == page), None)
        if mod:
            page_module(mod)
        else:
            st.error("Module introuvable.")
            st.session_state["page"] = "home"
            st.rerun()


if __name__ == "__main__":
    main()
