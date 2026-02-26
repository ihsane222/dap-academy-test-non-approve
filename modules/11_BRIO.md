# Module 11 — BRIO : Pratiques d'Encodage
**Domaine :** Outils Digitaux · **Durée :** 4h · **Format :** À distance · **Public :** Tous · **Mois :** Juin 2026

---

## Objectifs pédagogiques

1. Maîtriser les standards d'encodage DAP dans BRIO
2. Créer et gérer les fiches clients avec toutes les informations requises
3. Encoder correctement les polices, avenants et sinistres
4. Utiliser les fonctionnalités de reporting de BRIO
5. Adopter des pratiques uniformes garantissant la qualité des données

---

## Contenu pédagogique

### 1. Présentation de BRIO

**BRIO** est la plateforme de gestion de courtage utilisée par DAP. Elle centralise :
- La gestion des clients (personnes physiques et morales)
- La gestion des polices d'assurance (toutes branches)
- Le suivi des sinistres
- La comptabilité des primes
- Le reporting réglementaire (FSMA)

L'objectif de cette formation est **l'harmonisation des pratiques** — une même information encodée de la même façon par tous les DAPiens garantit la qualité des données et facilite le travail en équipe.

### 2. Standards d'encodage des clients

#### Personnes physiques
| Champ | Standard DAP | Exemple |
|---|---|---|
| Nom | MAJUSCULES | DUPONT |
| Prénom | Première lettre majuscule | Jean-Marie |
| Date de naissance | JJ/MM/AAAA | 15/03/1978 |
| N° national | Format BRIO automatique | — |
| Adresse | Rue + numéro + boîte | Rue de la Loi 16 bte 3 |
| Code postal | 4 chiffres | 1000 |
| Commune | Majuscules | BRUXELLES |
| Téléphone | 0032 + numéro sans 0 | 0032 474 12 34 56 |
| Email | Minuscules | jean.dupont@email.be |

#### Personnes morales
| Champ | Standard DAP |
|---|---|
| Raison sociale | Exactement comme au BCE |
| Forme juridique | Abréviations standard (SRL, SA, ASBL) |
| N° BCE | Format BE XXXX.XXX.XXX |
| Contact principal | Toujours renseigner le nom + fonction |

### 3. Encodage des polices

**Champs obligatoires pour toute police :**
- Compagnie d'assurance
- N° de police (tel que mentionné sur le document compagnie)
- Branche (code BRIO standardisé)
- Date de prise d'effet
- Date d'échéance
- Prime annuelle TVAC
- Fréquence de paiement
- Mode de paiement (domiciliation / virement)
- Courtier responsable

**Règles d'encodage spécifiques :**
- Ne jamais encoder la prime HTVA — toujours TVAC
- La date d'échéance = date à laquelle la résiliation doit être envoyée si nécessaire
- Toujours uploader le document police en PDF dans la GED (Gestion Électronique des Documents)
- Ajouter une note dans le dossier pour tout élément particulier (franchise spéciale, exclusion négociée...)

### 4. Encodage des avenants

Un avenant modifie une police existante. Il faut :
1. Trouver la police concernée dans BRIO
2. Créer un nouvel avenant (pas modifier la police d'origine)
3. Mentionner le N° d'avenant de la compagnie
4. Indiquer la date d'effet de la modification
5. Mettre à jour la prime si elle change
6. Uploader l'avenant en PDF

**Types d'avenants fréquents :**
- Changement d'adresse
- Ajout/suppression d'un véhicule
- Modification de capital garanti
- Changement de bénéficiaire (assurance vie)

### 5. Encodage des sinistres

**Délai d'encodage :** dès réception de la déclaration du client (même jour si possible).

**Champs obligatoires :**
- Date du sinistre
- Date de déclaration au courtier
- Description succincte (50-100 mots)
- Police concernée
- Compagnie notifiée (Oui/Non + date notification)
- N° de sinistre compagnie (à compléter dès réception)
- Statut (Ouvert / En cours / Clôturé)
- Montant estimé (si connu)

**Règle des 3 jours :** la compagnie doit être notifiée dans les 3 jours ouvrables suivant la déclaration du client (délai légal pour la plupart des polices).

### 6. Reporting dans BRIO

**Rapports utiles à maîtriser :**
- Liste des polices à échéance sur les 60 prochains jours
- Portefeuille par compagnie
- Sinistres ouverts > 3 mois
- Rapport annuel pour la FSMA (registre des formations PCP)

**Exporter vers Excel :** tous les rapports BRIO peuvent être exportés en `.xlsx` pour analyse complémentaire.

### 7. Erreurs fréquentes à éviter

| Erreur | Conséquence | Bonne pratique |
|---|---|---|
| Police encodée en HTVA | Écart comptable | Toujours TVAC |
| Date d'échéance incorrecte | Absence d'alerte renouvellement | Vérifier sur le document compagnie |
| PDF non uploadé | Dossier incomplet | Upload immédiat après réception |
| Client dupliqué | Dossier fragmenté | Chercher avant de créer |
| Sinistre non encodé | Suivi impossible | Encoder le jour de réception |

---

## Points clés à retenir

1. BRIO est la mémoire de DAP — une information mal encodée = information perdue
2. Toujours en TVAC, toujours le PDF uploadé, toujours le sinistre encodé le jour J
3. Ne jamais créer un nouveau client sans avoir vérifié s'il existe déjà
4. Les avenants se créent en complément de la police — jamais en modifiant la police d'origine
5. Les 3 jours pour notifier la compagnie d'un sinistre sont un délai légal, pas une recommandation

---

## Quiz de validation (5 questions)

**Q1.** Les primes doivent être encodées dans BRIO :
- a) HTVA pour faciliter les comparaisons
- b) TVAC ✅
- c) Au choix du courtier
- d) HTVA pour les professionnels, TVAC pour les particuliers

**Q2.** Quand un client déclare un sinistre, le délai pour notifier la compagnie est de :
- a) 24h
- b) 3 jours ouvrables ✅
- c) 7 jours
- d) 15 jours

**Q3.** Une modification de capital sur une police existante doit être encodée comme :
- a) Une modification directe de la police
- b) Un avenant ✅
- c) Une nouvelle police
- d) Une note dans le dossier client

**Q4.** Avant de créer une nouvelle fiche client dans BRIO, il faut :
- a) Obtenir l'accord du responsable
- b) Vérifier que le client n'existe pas déjà ✅
- c) Encoder d'abord la police
- d) Attendre d'avoir tous les documents

**Q5.** Le délai recommandé pour encoder un sinistre déclaré par un client est :
- a) Dans les 3 jours
- b) Dans la semaine
- c) Le jour même de réception ✅
- d) Après clôture du sinistre

---

## Ressources complémentaires

- Manuel utilisateur BRIO (version DAP — interne)
- Studio BRIO : modules e-learning (accès via portail BRIO)
- Support BRIO : helpdesk@brio.be
