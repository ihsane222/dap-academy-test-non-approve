# Module 07 — Excel : Maîtrise pour la Gestion Client
**Domaine :** Outils Digitaux · **Durée :** 2h · **Format :** À distance · **Public :** Tous · **Mois :** Avril 2026

---

## Objectifs pédagogiques

1. Maîtriser les fonctions Excel essentielles pour le reporting client
2. Construire un tableau de suivi de portefeuille clients
3. Utiliser les tableaux croisés dynamiques pour analyser un portefeuille
4. Automatiser des tâches répétitives avec des formules avancées
5. Mettre en forme des données pour une présentation professionnelle

---

## Contenu pédagogique

### 1. Fonctions essentielles pour un courtier

#### Fonctions de recherche
| Fonction | Usage | Exemple |
|---|---|---|
| `RECHERCHEV` | Trouver une valeur dans un tableau | Retrouver la prime d'un client par son N° de police |
| `RECHERCHEX` | Version améliorée de RECHERCHEV | Recherche dans les deux sens |
| `INDEX/EQUIV` | Recherche flexible | Croiser N° client + type de police |

#### Fonctions conditionnelles
| Fonction | Usage |
|---|---|
| `SI` | Si prime > 500 € alors "VIP" sinon "Standard" |
| `SI.ENS` | Plusieurs conditions simultanées |
| `NB.SI` | Compter les clients d'un secteur donné |
| `SOMME.SI` | Totaliser les primes d'un type de produit |

#### Fonctions de date
| Fonction | Usage |
|---|---|
| `AUJOURDHUI()` | Date du jour (pour alertes d'échéances) |
| `DATEDIF` | Calculer l'ancienneté d'un contrat |
| `NB.JOURS.OUVRES` | Délais de traitement |

### 2. Construire un tableau de suivi de portefeuille

**Structure recommandée :**

| Colonne | Contenu |
|---|---|
| A | N° client |
| B | Nom / Raison sociale |
| C | Type de produit |
| D | Compagnie |
| E | N° de police |
| F | Prime annuelle (€) |
| G | Date d'échéance |
| H | Jours restants (=G2-AUJOURDHUI()) |
| I | Statut (formule : Rouge/Orange/Vert) |
| J | Courtier responsable |

**Mise en forme conditionnelle pour les échéances :**
- Rouge : échéance < 30 jours
- Orange : échéance entre 30 et 60 jours
- Vert : échéance > 60 jours

### 3. Tableaux croisés dynamiques (TCD)

Les TCD permettent d'analyser un portefeuille en quelques clics.

**Exemples d'analyses utiles :**
- Volume de primes par compagnie
- Nombre de contrats par type de produit
- CA par courtier responsable
- Répartition des échéances par mois

**Étapes pour créer un TCD :**
1. Sélectionner le tableau de données
2. Insertion → Tableau croisé dynamique
3. Glisser les champs dans les zones (Lignes, Colonnes, Valeurs)
4. Filtrer et trier selon les besoins

### 4. Formules utiles pour le reporting

```
// Alerte échéance (colonne H)
=G2-AUJOURDHUI()

// Statut coloré (colonne I)
=SI(H2<30;"URGENT";SI(H2<60;"À surveiller";"OK"))

// Total primes par compagnie
=SOMME.SI($D:$D;"AG Insurance";$F:$F)

// Taux de renouvellement
=NB.SI(I:I;"Renouvelé")/NBVAL(A:A)-1
```

### 5. Bonnes pratiques

- Toujours **geler la première ligne** (Affichage → Figer les volets)
- Utiliser des **tableaux structurés** (Ctrl+T) pour des formules qui s'étendent automatiquement
- Nommer ses plages (Formules → Gestionnaire de noms) pour des formules lisibles
- **Protéger les feuilles** en lecture seule pour les rapports partagés
- Sauvegarder en `.xlsx` et non `.xls` (format obsolète)

---

## Points clés à retenir

1. RECHERCHEV et SOMME.SI sont les deux fonctions les plus utiles au quotidien
2. La mise en forme conditionnelle transforme un tableau en outil de pilotage visuel
3. Les TCD remplacent des dizaines de formules manuelles pour les analyses
4. Toujours utiliser des tableaux structurés pour faciliter les mises à jour
5. La colonne "Jours restants" avec AUJOURDHUI() est la base de tout suivi d'échéances

---

## Exercice pratique

Télécharger le fichier `Exercice_Excel_DAP.xlsx` (disponible sur Teams/BRIO) et réaliser les tâches suivantes :
1. Créer une colonne "Jours avant échéance" automatique
2. Ajouter une mise en forme conditionnelle (rouge/orange/vert)
3. Créer un TCD montrant le total des primes par compagnie
4. Filtrer pour n'afficher que les contrats qui arrivent à échéance dans les 60 prochains jours

---

## Quiz de validation (5 questions)

**Q1.** Quelle fonction permet de calculer automatiquement le nombre de jours avant une échéance ?
- a) `=DATEDIF()`
- b) `=G2-AUJOURDHUI()` ✅
- c) `=NB.JOURS.OUVRES()`
- d) `=MAINTENANT()`

**Q2.** Un tableau croisé dynamique sert à :
- a) Créer des graphiques automatiquement
- b) Analyser et synthétiser de grandes quantités de données ✅
- c) Partager un fichier avec plusieurs utilisateurs
- d) Protéger les données sensibles

**Q3.** La fonction SOMME.SI permet de :
- a) Additionner toutes les cellules d'une colonne
- b) Additionner uniquement les cellules qui respectent un critère ✅
- c) Vérifier si une somme est correcte
- d) Calculer une somme si une condition est vraie ou fausse

**Q4.** "Geler les volets" dans Excel permet de :
- a) Protéger le fichier par mot de passe
- b) Maintenir visible la première ligne lors du défilement ✅
- c) Bloquer les modifications sur certaines cellules
- d) Figer les valeurs calculées par des formules

**Q5.** Le format de fichier recommandé pour les fichiers Excel modernes est :
- a) .xls
- b) .csv
- c) .xlsx ✅
- d) .ods

---

## Ressources complémentaires

- Fichier modèle : Tableau de suivi portefeuille DAP (Teams)
- Tutoriels Microsoft : support.microsoft.com/excel
- Formation complémentaire : Excel avancé (Macros VBA) — à la demande
