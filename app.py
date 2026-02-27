import streamlit as st
import os, re, glob
from datetime import datetime
from collections import defaultdict

# ─── Google Sheets (optionnel — dégradation gracieuse) ────────────────────────
try:
    import gspread
    from google.oauth2.service_account import Credentials
    _HAS_GSPREAD = True
except ImportError:
    _HAS_GSPREAD = False

_GS_SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

def _gs_configured():
    return _HAS_GSPREAD and "SHEET_ID" in st.secrets and "gcp_service_account" in st.secrets

@st.cache_resource
def _get_workbook():
    if not _gs_configured():
        return None
    try:
        creds  = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes=_GS_SCOPES)
        client = gspread.authorize(creds)
        wb     = client.open_by_key(st.secrets["SHEET_ID"])
        try:
            wb.worksheet("historique")
        except gspread.WorksheetNotFound:
            ws = wb.add_worksheet("historique", rows=5000, cols=10)
            ws.append_row(["timestamp","username","bureau","module_num","module_title","score_pct","points","badge"])
        return wb
    except Exception:
        return None

def gs_push_score(username, bureau, mod_num, mod_title, score_pct, points, badge):
    wb = _get_workbook()
    if wb is None:
        return
    try:
        ws = wb.worksheet("historique")
        ws.append_row([datetime.now().strftime("%Y-%m-%d %H:%M"),
                       username, bureau, mod_num, mod_title,
                       round(score_pct, 1), points, badge])
        gs_fetch_scores.clear()
    except Exception:
        pass

@st.cache_data(ttl=30)
def gs_fetch_scores():
    wb = _get_workbook()
    if wb is None:
        return []
    try:
        return wb.worksheet("historique").get_all_records()
    except Exception:
        return []

# ─── Scores en session (fallback sans GSheets) ────────────────────────────────
def get_all_scores():
    remote = gs_fetch_scores()
    local  = st.session_state.get("local_scores", [])
    # Merge : éviter doublons (clé = username+bureau+module_num+score_pct)
    seen = {(r["username"], r["bureau"], str(r["module_num"]), r["score_pct"]) for r in remote}
    extra = [r for r in local if (r["username"], r["bureau"], str(r["module_num"]), r["score_pct"]) not in seen]
    return remote + extra

def save_score_local(username, bureau, mod_num, mod_title, score_pct, points, badge):
    if "local_scores" not in st.session_state:
        st.session_state["local_scores"] = []
    st.session_state["local_scores"].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "username": username, "bureau": bureau,
        "module_num": mod_num, "module_title": mod_title,
        "score_pct": score_pct, "points": points, "badge": badge,
    })

# ─── Système de points & badges ───────────────────────────────────────────────
def calc_pts_badge(score_pct: float):
    if score_pct == 100: return 150, "💎 Maître"
    if score_pct >= 80:  return 100, "🏆 Expert"
    if score_pct >= 60:  return  50, "✅ Validé"
    return 10, "📖 En cours"

def get_user_stats(username, bureau, all_scores, modules):
    rows = [r for r in all_scores if r["username"] == username and r["bureau"] == bureau]
    best = {}
    for r in rows:
        mod = str(r["module_num"])
        if mod not in best or float(r["score_pct"]) > float(best[mod]["score_pct"]):
            best[mod] = r

    completed = {m for m, r in best.items() if float(r["score_pct"]) >= 60}
    total_pts  = sum(int(r["points"]) for r in best.values())

    all_nums = {m["number"] for m in modules if m["number"] != "00"}
    domain_map = defaultdict(set)
    for m in modules:
        if m["number"] != "00":
            domain_map[m["meta"].get("domaine", "")].add(m["number"])

    badges = []
    # Milestone badges
    if len(completed) >= 19:  badges.append("🎓 DAP Pro");    total_pts += 500
    if len(completed) >= 10:  badges.append("⚡ Mi-parcours")
    if len(completed) >= 5:   badges.append("🚀 Lancé")
    if len(completed) >= 1:   badges.append("🌱 Premiers pas")

    # Spécialiste par domaine
    for domain, mods in domain_map.items():
        if len(mods) >= 2 and mods <= completed:
            badges.append(f"🌟 Spécialiste {domain}")
            total_pts += 100

    # Score badges
    masters = sum(1 for r in best.values() if float(r["score_pct"]) == 100)
    experts = sum(1 for r in best.values() if float(r["score_pct"]) >= 80)
    if masters >= 5:  badges.append("💎 Maître de l'excellence")
    if experts >= 10: badges.append("🏆 Expert confirmé")

    return {
        "total_points":  total_pts,
        "completed":     completed,
        "best":          best,
        "badges":        badges,
        "n_completed":   len(completed),
        "n_total":       len(all_nums),
    }

def compute_leaderboard(all_scores, modules):
    user_rows = defaultdict(list)
    for r in all_scores:
        user_rows[(r["username"], r["bureau"])].append(r)

    all_nums   = {m["number"] for m in modules if m["number"] != "00"}
    domain_map = defaultdict(set)
    for m in modules:
        if m["number"] != "00":
            domain_map[m["meta"].get("domaine", "")].add(m["number"])

    individual   = []
    bureau_pts   = defaultdict(int)

    for (uname, ubur), rows in user_rows.items():
        best = {}
        for r in rows:
            mod = str(r["module_num"])
            if mod not in best or float(r["score_pct"]) > float(best[mod]["score_pct"]):
                best[mod] = r
        pts       = sum(int(r["points"]) for r in best.values())
        completed = {m for m, r in best.items() if float(r["score_pct"]) >= 60}
        if completed >= all_nums: pts += 500
        for mods in domain_map.values():
            if len(mods) >= 2 and mods <= completed: pts += 100
        individual.append({"name": uname, "bureau": ubur, "points": pts, "modules": len(completed)})
        bureau_pts[ubur] += pts

    individual.sort(key=lambda x: x["points"], reverse=True)
    bureau_ranking = sorted(bureau_pts.items(), key=lambda x: x[1], reverse=True)
    return individual, bureau_ranking

# ─── Configuration ────────────────────────────────────────────────────────────
st.set_page_config(page_title="DAP Academy", page_icon="🎓",
                   layout="wide", initial_sidebar_state="expanded")

MODULES_DIR = "modules"
VIDEO_FILES = {str(i).zfill(2): f"videos/DAPModule{str(i).zfill(2)}.mp4" for i in range(1, 20)}

BUREAUX = [
    "Bruxelles", "Rhode-Saint-Genèse", "Manage", "Charleroi",
    "Leuze", "Ladeuze", "Mons", "Ath", "Enghien", "Alost", "Liège", "Eupen",
]

DOMAIN_COLORS = {
    "Assurances":          "badge-blue",
    "Outils Digitaux":     "badge-green",
    "Réglementation":      "badge-orange",
    "IT":                  "badge-orange",
    "Produits d'assurance":"badge-blue",
}

st.markdown("""
<style>
  .main-header{background:linear-gradient(135deg,#2A4B62 0%,#37A1D7 100%);
    color:white;padding:30px;border-radius:12px;margin-bottom:20px;text-align:center;}
  .badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:.75em;font-weight:700;margin:2px;}
  .badge-blue  {background:#e3f2fd;color:#1565c0;}
  .badge-green {background:#e8f5e9;color:#2e7d32;}
  .badge-orange{background:#fff3e0;color:#e65100;}
  .stProgress>div>div{background-color:#37A1D7;}

  /* Login */
  .login-card{max-width:480px;margin:60px auto;background:white;border-radius:16px;
    padding:40px;box-shadow:0 8px 32px rgba(42,75,98,.12);}
  .login-title{font-size:1.8em;font-weight:800;color:#2A4B62;text-align:center;margin-bottom:6px;}
  .login-sub  {text-align:center;color:#666;margin-bottom:28px;}

  /* Stat cards */
  .stat-grid{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:18px;}
  .stat-card{flex:1;min-width:120px;background:white;border-radius:10px;padding:18px 14px;
    text-align:center;border:1px solid #e0e7ef;box-shadow:0 2px 8px rgba(0,0,0,.04);}
  .stat-num  {font-size:2.2em;font-weight:800;color:#2A4B62;line-height:1;}
  .stat-label{font-size:.8em;color:#888;margin-top:4px;}

  /* Badges display */
  .badge-lg{display:inline-block;padding:6px 16px;border-radius:20px;margin:4px;
    font-size:.9em;font-weight:700;background:#EFF6FB;color:#2A4B62;border:1px solid #D6EAF5;}

  /* Module cards */
  .mod-done{border-left:4px solid #34A853!important;}
  .mod-todo{border-left:4px solid #DDD!important;opacity:.9;}

  /* Leaderboard */
  .lb-row{padding:10px 16px;border-radius:8px;margin:3px 0;display:flex;align-items:center;gap:10px;}
  .lb-1{background:linear-gradient(90deg,#FFFBEA,#FFF);border-left:4px solid #FFD700;}
  .lb-2{background:linear-gradient(90deg,#F8F8F8,#FFF);border-left:4px solid #C0C0C0;}
  .lb-3{background:linear-gradient(90deg,#FFF4EE,#FFF);border-left:4px solid #CD7F32;}
  .lb-n{background:#FAFAFA;border-left:4px solid #E0E7EF;}
  .lb-rank{font-size:1.3em;font-weight:800;width:36px;text-align:center;}
  .lb-name{flex:1;font-weight:600;}
  .lb-pts {font-weight:800;color:#2A4B62;}
  .lb-mod {font-size:.8em;color:#888;}
  .demo-banner{background:#FFF8E1;border:1px solid #FFD54F;border-radius:8px;
    padding:10px 16px;margin-bottom:16px;font-size:.9em;color:#795548;}
</style>
""", unsafe_allow_html=True)

# ─── Chargement modules ───────────────────────────────────────────────────────
@st.cache_data
def load_modules():
    files = sorted(glob.glob(f"{MODULES_DIR}/[0-9]*.md"))
    modules = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        lines = content.split("\n")
        title = lines[0].replace("#", "").strip() if lines else os.path.basename(f)
        meta  = {}
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
        modules.append({"filename": os.path.basename(f), "path": f,
                         "title": title, "content": content, "number": num, "meta": meta})
    return modules

# ─── Parsing quiz ─────────────────────────────────────────────────────────────
def parse_quiz(content):
    quiz_section = re.search(r"## Quiz de validation.*?(?=\n---|\Z)", content, re.DOTALL)
    if not quiz_section:
        return []
    questions = []
    for block in re.split(r"\*\*Q\d+\.\*\*\s*", quiz_section.group(0))[1:]:
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        options, correct = [], None
        for line in lines[1:]:
            m = re.match(r"[-–]\s*([a-d])\)\s*(.*?)(\s*✅)?\s*$", line)
            if m:
                letter, text, tick = m.group(1), m.group(2).strip(), bool(m.group(3))
                options.append({"letter": letter, "text": text, "correct": tick})
                if tick: correct = letter
        if options and correct:
            questions.append({"question": lines[0], "options": options, "correct": correct})
    return questions

def content_without_quiz(content):
    idx = content.find("## Quiz de validation")
    return content[:idx] if idx > 0 else content

# ─── Page : Login ─────────────────────────────────────────────────────────────
def page_login():
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;padding-top:40px;">
      <div class="login-card">
        <div class="login-title">🎓 DAP Academy</div>
        <div class="login-sub">Plan de Formation 2026 · Identifie-toi pour suivre ta progression</div>
      </div>
    </div>""", unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        with st.container(border=True):
            st.markdown("### Bienvenue !")
            name   = st.text_input("Ton prénom", placeholder="Ex : Sophie", max_chars=40)
            bureau = st.selectbox("Ton bureau", ["— Choisir —"] + BUREAUX)
            st.markdown("")
            if st.button("Commencer la formation →", type="primary", use_container_width=True):
                if not name.strip():
                    st.error("Entre ton prénom pour continuer.")
                elif bureau == "— Choisir —":
                    st.error("Sélectionne ton bureau.")
                else:
                    st.session_state["user"] = {"name": name.strip(), "bureau": bureau}
                    st.session_state["page"] = "home"
                    st.rerun()
            if not _gs_configured():
                st.markdown("""<div class="demo-banner">
                    ℹ️ <strong>Mode démo</strong> — les scores sont sauvegardés localement
                    (session uniquement). Configure Google Sheets pour la persistance.
                </div>""", unsafe_allow_html=True)

# ─── Page : Accueil ───────────────────────────────────────────────────────────
def page_home(modules, user_stats):
    n_done  = user_stats["n_completed"]
    n_total = user_stats["n_total"]
    pts     = user_stats["total_points"]
    user    = st.session_state["user"]

    st.markdown(f"""
    <div class="main-header">
      <h1>🎓 DAP Academy</h1>
      <p style="font-size:1.1em;margin:0 0 8px;">
        Plan Global de Formation 2026 · 19 modules · 46h · Conformité FSMA
      </p>
      <p style="margin:0;font-size:1em;opacity:.85;">
        Bonjour <strong>{user['name']}</strong> · {user['bureau']} ·
        <strong>{n_done}/{n_total}</strong> modules · <strong>{pts} pts</strong>
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Barre de progression globale
    if n_done > 0:
        st.progress(n_done / n_total, text=f"{n_done}/{n_total} modules complétés ({int(n_done/n_total*100)}%)")
    else:
        st.progress(0.0, text="0/19 modules — commence dès maintenant !")

    # Badges rapides
    if user_stats["badges"]:
        badges_html = " ".join(f'<span class="badge-lg">{b}</span>' for b in user_stats["badges"])
        st.markdown(badges_html, unsafe_allow_html=True)
        st.markdown("")

    st.markdown("### 📚 Modules disponibles")
    completed = user_stats["completed"]

    cols = st.columns(3)
    for i, mod in enumerate(modules):
        if mod["number"] == "00":
            continue
        meta         = mod["meta"]
        domain_badge = DOMAIN_COLORS.get(meta.get("domaine", ""), "badge-blue")
        is_done      = mod["number"] in completed
        best         = user_stats["best"].get(mod["number"])
        card_class   = "mod-done" if is_done else "mod-todo"
        status_icon  = "✅" if is_done else "⏳"
        score_txt    = f" · {best['badge']} ({best['score_pct']:.0f}%)" if best else ""

        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(
                    f'<div class="{card_class}" style="padding-left:8px;">'
                    f'<strong>{status_icon} {mod["title"]}</strong>'
                    f'<br><small style="color:#666;">{score_txt}</small>'
                    f'</div>',
                    unsafe_allow_html=True)
                st.markdown(
                    f'<span class="badge {domain_badge}">{meta.get("domaine","")}</span> '
                    f'<span class="badge badge-green">⏱ {meta.get("duree","")}</span> '
                    f'<span class="badge badge-orange">📅 {meta.get("mois","")}</span>',
                    unsafe_allow_html=True)
                if st.button("Accéder →", key=f"home_btn_{mod['number']}", use_container_width=True):
                    st.session_state["page"] = mod["number"]
                    st.rerun()

# ─── Page : Module ────────────────────────────────────────────────────────────
def page_module(module, user_stats):
    user = st.session_state["user"]
    if st.button("← Retour aux modules"):
        st.session_state["page"] = "home"
        st.rerun()

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
            opts   = [f"{o['letter']}) {o['text']}" for o in q["options"]]
            chosen = st.radio("", opts, key=f"{qkey}_q{i}", label_visibility="collapsed")
            answers[i] = chosen[0] if chosen else None
            st.markdown("")
        submitted = st.form_submit_button("✅ Valider le quiz", type="primary", use_container_width=True)

    if submitted:
        score = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["correct"])
        pct   = (score / len(questions)) * 100
        pts, badge = calc_pts_badge(pct)
        st.session_state[f"{qkey}_score"] = (score, len(questions), pct, answers, pts, badge)

        # Sauvegarde
        gs_push_score(user["name"], user["bureau"], module["number"],
                      module["title"], pct, pts, badge)
        save_score_local(user["name"], user["bureau"], module["number"],
                         module["title"], pct, pts, badge)

    if st.session_state[f"{qkey}_score"]:
        score, total, pct, saved_answers, pts, badge = st.session_state[f"{qkey}_score"]
        st.markdown("---")
        if pct >= 80:
            st.success(f"🏆 Excellent ! **{score}/{total}** — {pct:.0f}% — **+{pts} pts** · {badge}")
        elif pct >= 60:
            st.warning(f"👍 Bien ! **{score}/{total}** — {pct:.0f}% — **+{pts} pts** · {badge}")
        else:
            st.error(f"📖 **{score}/{total}** — {pct:.0f}% · {badge} — Relisez le module avant de recommencer")

        with st.expander("📋 Voir les réponses correctes"):
            for i, q in enumerate(questions):
                correct_opt = next((o for o in q["options"] if o["correct"]), None)
                icon = "✅" if saved_answers.get(i) == q["correct"] else "❌"
                st.markdown(f"{icon} **Q{i+1}.** Bonne réponse : **{q['correct']}) {correct_opt['text'] if correct_opt else ''}**")

# ─── Page : Dashboard ─────────────────────────────────────────────────────────
def page_dashboard(modules, user_stats):
    user = st.session_state["user"]
    n    = user_stats["n_completed"]
    pts  = user_stats["total_points"]
    best = user_stats["best"]

    st.markdown(f"## 📊 Mon Dashboard — {user['name']} · {user['bureau']}")

    # Stats cards
    pct_done = int(n / user_stats["n_total"] * 100) if user_stats["n_total"] else 0
    avg_score = (sum(float(r["score_pct"]) for r in best.values()) / len(best)) if best else 0
    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-num">{pts}</div>
        <div class="stat-label">Points totaux</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{n}</div>
        <div class="stat-label">Modules complétés</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{pct_done}%</div>
        <div class="stat-label">Progression</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{avg_score:.0f}%</div>
        <div class="stat-label">Score moyen</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Progression globale
    st.progress(n / user_stats["n_total"] if user_stats["n_total"] else 0,
                text=f"{n}/{user_stats['n_total']} modules validés")

    # Badges
    st.markdown("### 🏅 Mes badges")
    if user_stats["badges"]:
        html_b = " ".join(f'<span class="badge-lg">{b}</span>' for b in user_stats["badges"])
        st.markdown(html_b, unsafe_allow_html=True)
    else:
        st.info("Valide ton premier quiz pour débloquer tes premiers badges !")

    # Progression par domaine
    st.markdown("### 📚 Progression par domaine")
    domain_map = defaultdict(list)
    for mod in modules:
        if mod["number"] != "00":
            domain_map[mod["meta"].get("domaine", "Autre")].append(mod["number"])

    for domain, mods in sorted(domain_map.items()):
        done  = len([m for m in mods if m in user_stats["completed"]])
        total = len(mods)
        color = {"Produits d'assurance": "#2A4B62", "Réglementation": "#C2410C",
                 "Outils Digitaux": "#1D6B2F", "IT": "#9B1C1C"}.get(domain, "#37A1D7")
        st.markdown(f"**{domain}** — {done}/{total}")
        st.progress(done / total if total else 0)

    # Détail par module
    if best:
        st.markdown("### 🗒️ Détail des modules")
        rows = []
        for mod in modules:
            if mod["number"] == "00": continue
            r = best.get(mod["number"])
            if r:
                rows.append(f"| {mod['number']} | {mod['title'].split('—')[-1].strip()[:40]} "
                            f"| {r['badge']} | {float(r['score_pct']):.0f}% | {r['points']} pts |")
        if rows:
            st.markdown("| # | Module | Badge | Score | Points |\n|---|---|---|---|---|\n" + "\n".join(rows))

# ─── Page : Classement ────────────────────────────────────────────────────────
def page_leaderboard(modules):
    st.markdown("## 🏆 Classement DAP Academy")
    all_scores = get_all_scores()
    if not all_scores:
        st.info("Pas encore de scores enregistrés. Sois le premier à passer un quiz !")
        return

    individual, bureau_ranking = compute_leaderboard(all_scores, modules)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 👤 Top individuel")
        medals = ["🥇", "🥈", "🥉"]
        for i, entry in enumerate(individual[:15]):
            cls     = f"lb-{i+1}" if i < 3 else "lb-n"
            medal   = medals[i] if i < 3 else str(i + 1)
            is_me   = (entry["name"] == st.session_state["user"]["name"]
                       and entry["bureau"] == st.session_state["user"]["bureau"])
            me_tag  = " ← toi" if is_me else ""
            st.markdown(
                f'<div class="lb-row {cls}">'
                f'  <span class="lb-rank">{medal}</span>'
                f'  <span class="lb-name">{entry["name"]}<small style="color:#999;"> · {entry["bureau"]}{me_tag}</small></span>'
                f'  <span class="lb-mod">{entry["modules"]} mod.</span>'
                f'  <span class="lb-pts">{entry["points"]} pts</span>'
                f'</div>',
                unsafe_allow_html=True)

    with col2:
        st.markdown("### 🏢 Classement par bureau")
        bureau_medals = ["🥇", "🥈", "🥉"]
        for i, (bur, pts) in enumerate(bureau_ranking):
            cls   = f"lb-{i+1}" if i < 3 else "lb-n"
            medal = bureau_medals[i] if i < 3 else str(i + 1)
            is_me = bur == st.session_state["user"]["bureau"]
            me_tag = " ← ton bureau" if is_me else ""
            st.markdown(
                f'<div class="lb-row {cls}">'
                f'  <span class="lb-rank">{medal}</span>'
                f'  <span class="lb-name">{bur}{me_tag}</span>'
                f'  <span class="lb-pts">{pts} pts</span>'
                f'</div>',
                unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
def sidebar(modules, user_stats):
    user = st.session_state.get("user", {})
    with st.sidebar:
        st.markdown("## 🎓 DAP Academy")
        if user:
            pts = user_stats["total_points"]
            n   = user_stats["n_completed"]
            st.markdown(f"**{user['name']}** · {user['bureau']}")
            st.markdown(f"⭐ **{pts} pts** · {n}/19 modules")
            st.progress(n / 19)
        st.markdown("---")

        if st.button("🏠 Accueil", use_container_width=True):
            st.session_state["page"] = "home"; st.rerun()
        if st.button("📊 Mon Dashboard", use_container_width=True):
            st.session_state["page"] = "dashboard"; st.rerun()
        if st.button("🏆 Classement", use_container_width=True):
            st.session_state["page"] = "leaderboard"; st.rerun()

        st.markdown("---")
        st.markdown("**Modules**")
        completed = user_stats["completed"]
        for mod in modules:
            if mod["number"] == "00": continue
            icon  = "✅" if mod["number"] in completed else "⬜"
            label = f"{icon} {mod['number']} · {mod['title'].split('—')[-1].strip()[:28]}"
            if st.button(label, key=f"sb_{mod['number']}", use_container_width=True):
                st.session_state["page"] = mod["number"]; st.rerun()

        st.markdown("---")
        if st.button("🚪 Se déconnecter", use_container_width=True):
            for key in ["user", "page"]:
                st.session_state.pop(key, None)
            st.rerun()
        st.caption("46h · 19 modules · FSMA ✅")

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    # Login requis
    if "user" not in st.session_state:
        page_login()
        return

    modules    = load_modules()
    all_scores = get_all_scores()
    user       = st.session_state["user"]
    user_stats = get_user_stats(user["name"], user["bureau"], all_scores, modules)

    sidebar(modules, user_stats)

    page = st.session_state["page"]
    if page == "home":
        page_home(modules, user_stats)
    elif page == "dashboard":
        page_dashboard(modules, user_stats)
    elif page == "leaderboard":
        page_leaderboard(modules)
    else:
        mod = next((m for m in modules if m["number"] == page), None)
        if mod:
            page_module(mod, user_stats)
        else:
            st.error("Module introuvable.")
            st.session_state["page"] = "home"
            st.rerun()

if __name__ == "__main__":
    main()
