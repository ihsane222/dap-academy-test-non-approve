# Configuration Google Sheets — DAP Academy

## Pourquoi Google Sheets ?
Les scores, badges et classements de tous les DAPiens sont stockés dans une Google Sheet.
Sans cette configuration, l'app fonctionne quand même (mode démo, scores non persistants).

---

## Étapes (15 minutes)

### 1. Créer le projet Google Cloud

1. Va sur [console.cloud.google.com](https://console.cloud.google.com)
2. Crée un nouveau projet : **"dap-academy"**
3. Dans la barre de recherche, cherche **"Google Sheets API"** → Activer
4. Cherche aussi **"Google Drive API"** → Activer

### 2. Créer un compte de service

1. Menu gauche → **"IAM et administration"** → **"Comptes de service"**
2. Cliquer **"Créer un compte de service"**
   - Nom : `dap-academy-scores`
   - Rôle : **Éditeur**
3. Une fois créé, clique sur le compte → onglet **"Clés"**
4. **"Ajouter une clé"** → **"JSON"** → télécharger le fichier

### 3. Créer la Google Sheet

1. Va sur [sheets.google.com](https://sheets.google.com)
2. Crée une nouvelle feuille : **"DAP Academy — Scores"**
3. Copie l'ID depuis l'URL :
   `https://docs.google.com/spreadsheets/d/**TON_SHEET_ID**/edit`
4. Partage la feuille avec l'email du compte de service
   (ex : `dap-academy-scores@dap-academy.iam.gserviceaccount.com`)
   → Rôle : **Éditeur**

### 4. Configurer les secrets localement

1. Copie `.streamlit/secrets.toml.template` en `.streamlit/secrets.toml`
2. Remplis :
   - `SHEET_ID` = l'ID copié à l'étape 3
   - `[gcp_service_account]` = le contenu du JSON téléchargé à l'étape 2
3. Ajoute `secrets.toml` dans `.gitignore` (ne jamais pusher ce fichier !)

### 5. Configurer Streamlit Cloud

1. Va sur [share.streamlit.io](https://share.streamlit.io)
2. Sélectionne ton app → **"Settings"** → **"Secrets"**
3. Colle exactement le contenu de ton `secrets.toml`
4. Sauvegarde → l'app redémarre automatiquement

---

## Structure de la Google Sheet créée automatiquement

L'app crée la feuille **"historique"** avec ces colonnes :

| timestamp | username | bureau | module_num | module_title | score_pct | points | badge |
|---|---|---|---|---|---|---|---|
| 2026-02-27 10:30 | Sophie | Bruxelles | 01 | Module 01 — ... | 80.0 | 100 | 🏆 Expert |

---

## En cas de problème

- L'app affiche une bannière **"Mode démo"** si Google Sheets n'est pas configuré
- Les scores sont quand même stockés en session (perdus au refresh)
- Vérifie que le compte de service a bien accès à la feuille (Éditeur)
- Vérifie que les APIs Sheets et Drive sont bien activées

---

## Structure des points (rappel)

| Action | Points | Badge |
|---|---|---|
| Quiz < 60% | +10 pts | 📖 En cours |
| Quiz ≥ 60% | +50 pts | ✅ Validé |
| Quiz ≥ 80% | +100 pts | 🏆 Expert |
| Quiz 100% | +150 pts | 💎 Maître |
| Tous les modules d'un domaine | +100 pts bonus | 🌟 Spécialiste |
| 19/19 modules complétés | +500 pts bonus | 🎓 DAP Pro |
