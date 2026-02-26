# Module 17 — Cybersécurité
**Domaine :** IT · **Durée :** 4h · **Format :** À distance · **Public :** Tous · **Mois :** Novembre 2026

---

## Objectifs pédagogiques

1. Identifier les principales cybermenaces auxquelles un courtier d'assurance est exposé
2. Reconnaître les tentatives de phishing et d'ingénierie sociale
3. Appliquer les bonnes pratiques de sécurité informatique au quotidien
4. Connaître la procédure d'incident de sécurité chez DAP
5. Comprendre les obligations légales en matière de cybersécurité (RGPD, NIS2)

---

## Contenu pédagogique

### 1. Le paysage des cybermenaces pour un courtier d'assurance

Les courtiers d'assurance sont des cibles privilégiées pour les cybercriminels car :
- Ils détiennent des **données personnelles et financières sensibles** (clients, polices, RIB)
- Ils sont souvent des **PME** avec des moyens IT limités
- Ils servent de **passerelle** vers les grandes compagnies d'assurance

**Statistiques clés :**
- 1 PME belge sur 2 a été victime d'une cyberattaque en 2024
- 60 % des cyberattaques sur les PME passent par le **phishing**
- Le coût moyen d'une cyberattaque sur une PME : **50 000 à 200 000 €**

### 2. Les principales menaces

#### Phishing
Email frauduleux imitant une source de confiance (compagnie d'assurance, banque, FSMA...) pour obtenir des identifiants ou faire cliquer sur un lien malveillant.

**Signes d'un email de phishing :**
- Adresse expéditeur suspecte (ex. : ag-insurance@gmail.com au lieu de @aginsurance.be)
- Urgence artificielle ("Votre compte sera bloqué dans 24h")
- Lien qui ne correspond pas au domaine officiel (survoler sans cliquer)
- Fautes d'orthographe, mise en forme inhabituelle
- Demande de données personnelles ou de mot de passe

#### Ransomware
Logiciel malveillant qui chiffre les fichiers de l'entreprise et exige une rançon pour les déverrouiller. Souvent introduit via un email de phishing ou un accès distant non sécurisé.

**Conséquences :** perte totale des données BRIO, polices, sinistres si pas de sauvegarde.

#### Arnaque au président (BEC — Business Email Compromise)
Le cybercriminel usurpe l'identité d'un dirigeant (Diego de Lichtervelde) et demande par email un virement urgent à un employé du service financier.

**Règle DAP :** tout virement demandé par email sans processus habituel = **vérifier par téléphone sur un numéro connu**, jamais répondre directement à l'email.

#### Vol de données
Exfiltration de la base clients DAP (noms, contrats, IBAN, données de santé) revendue sur des forums criminels.

### 3. Les bonnes pratiques au quotidien

#### Mots de passe
- Longueur minimum : **12 caractères**
- Combinaison : majuscules + minuscules + chiffres + caractères spéciaux
- Un mot de passe unique par service
- Utiliser un **gestionnaire de mots de passe** (Bitwarden, 1Password)
- **Ne jamais** partager son mot de passe, même à l'IT DAP

#### Authentification à deux facteurs (2FA)
Activer systématiquement sur :
- Messagerie professionnelle (Microsoft 365)
- BRIO
- Accès VPN DAP
- Toute application contenant des données clients

#### Navigation sécurisée
- Vérifier le cadenas HTTPS avant de saisir des informations
- Ne pas utiliser les réseaux WiFi publics pour travailler (café, gare)
- Si WiFi public nécessaire → utiliser le VPN DAP
- Ne pas cliquer sur des liens dans des emails non sollicités

#### Postes de travail
- Verrouiller son écran dès qu'on s'éloigne (Windows+L)
- Ne pas brancher de clé USB inconnue
- Signaler immédiatement tout comportement inhabituel du PC
- Mises à jour → toujours accepter (ne pas reporter indéfiniment)

#### Données clients
- Ne jamais envoyer de données sensibles par email non chiffré
- Ne pas stocker de données clients sur des supports personnels
- Utiliser uniquement les outils approuvés par DAP (BRIO, Teams, OneDrive DAP)

### 4. Reconnaître et réagir face au phishing

**Procédure si vous recevez un email suspect :**
1. Ne pas cliquer sur les liens
2. Ne pas ouvrir les pièces jointes
3. Vérifier l'adresse email de l'expéditeur
4. Signaler à l'IT DAP (Objet : [PHISHING SUSPECTÉ])
5. Supprimer l'email

**Si vous avez cliqué par erreur :**
1. Déconnecter immédiatement l'ordinateur du réseau (câble ethernet à débrancher / WiFi à couper)
2. Appeler immédiatement l'IT DAP
3. Ne pas éteindre l'ordinateur (les logs sont nécessaires)
4. Ne pas accéder à d'autres systèmes depuis cet ordinateur

### 5. Obligations légales

#### RGPD
Toute violation de données doit être notifiée à l'APD dans les **72 heures** (voir Module 13). Une cyberattaque ayant exposé des données clients est une violation de données.

#### Directive NIS2 (Network and Information Security)
Applicable depuis octobre 2024 aux entreprises de taille intermédiaire dans certains secteurs. DAP doit :
- Disposer d'une politique de sécurité documentée
- Mettre en place des procédures de gestion des incidents
- Former les collaborateurs à la cybersécurité (ce module !)
- Notifier les incidents significatifs au CCN (Centre for Cybersecurity Belgium)

---

## Points clés à retenir

1. 60 % des attaques commencent par un email de phishing — apprendre à les reconnaître est la défense n°1
2. Mot de passe fort + 2FA = barrière efficace contre la grande majorité des intrusions
3. Arnaque au président : tout virement urgent demandé par email = vérifier par téléphone
4. Si vous avez cliqué sur un lien suspect → déconnectez du réseau immédiatement, appelez l'IT
5. NIS2 et RGPD imposent des obligations de sécurité documentées — ce n'est pas optionnel

---

## Exercice pratique

Analyser les 3 emails fictifs suivants et identifier pour chacun :
- S'agit-il d'un phishing ? Pourquoi ?
- Quels signaux d'alerte repérez-vous ?
- Que faites-vous ?

*(Emails fictifs fournis par le formateur pendant la session)*

---

## Quiz de validation (5 questions)

**Q1.** Le principal vecteur de cyberattaque sur les PME est :
- a) Les clés USB infectées
- b) Les réseaux WiFi publics
- c) Les emails de phishing ✅
- d) Les mises à jour logicielles

**Q2.** Si vous recevez un email de votre "directeur" demandant un virement urgent, vous devez :
- a) Exécuter immédiatement — c'est le directeur
- b) Vérifier par email en répondant directement
- c) Vérifier par téléphone sur un numéro connu de lui ✅
- d) Ignorer l'email

**Q3.** Si vous avez cliqué sur un lien de phishing, la première action est :
- a) Éteindre immédiatement l'ordinateur
- b) Changer tous vos mots de passe
- c) Déconnecter l'ordinateur du réseau et appeler l'IT DAP ✅
- d) Scanner l'ordinateur avec un antivirus

**Q4.** L'authentification à deux facteurs (2FA) protège contre :
- a) Les virus et malwares
- b) L'accès non autorisé même si le mot de passe est compromis ✅
- c) Les emails de phishing
- d) La perte de données

**Q5.** La directive NIS2 impose notamment :
- a) L'utilisation obligatoire d'un VPN
- b) La notification des incidents de sécurité significatifs aux autorités compétentes ✅
- c) L'interdiction du télétravail pour les données sensibles
- d) L'utilisation exclusive de logiciels open source

---

## Ressources complémentaires

- CCN (Centre for Cybersecurity Belgium) : ccb.belgium.be
- Signalement phishing belge : safeonweb.be
- IT DAP : [contact helpdesk interne]
- Gestionnaire de mots de passe recommandé : Bitwarden (version entreprise)
