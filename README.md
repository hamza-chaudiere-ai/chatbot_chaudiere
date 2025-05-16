# 🤖 Chatbot Chaudière – Générateur AMDEC & Gammes Automatisé (Projet Intelligent)

Ce projet est une plateforme web interactive destinée à automatiser le traitement des historiques de maintenance d’une chaudière industrielle.  
Elle permet actuellement de générer une AMDEC colorée et une gamme de maintenance à partir de fichiers Excel, avec pour ambition d’évoluer vers une solution intelligente enrichie par LLM et RAG.

---

## ✅ Fonctionnalités actuelles

- 📁 Import de fichier Excel contenant les historiques d’arrêts
- 🧠 Génération automatique d’un tableau AMDEC
  - Calcul de criticité : F × G × D
  - Affichage coloré selon les niveaux de criticité
- 📊 Graphique de visualisation des sous-composants critiques
- 📄 Génération de gamme de maintenance (basée sur un template Word)
- 🖼️ Logos intégrés (TAQA, AMDEC)
- Interface HTML/JS dynamique + traitement Python local

---

## 📂 Structure du projet

```
chatbot_chaudiere_nv/
│
├── index.html                  → Interface utilisateur
├── style.css                   → Feuille de style
├── script.js                   → Logique front-end
├── amdec_generator.py          → Génération automatique de l’AMDEC
├── maintenance_planner.py      → Génération des gammes de maintenance (à boucler)
├── templates/                  → Template Word utilisé pour les gammes
├── data/                       → Fichiers historiques à analyser
├── images/                     → Logos, composants
└── README.md
```

---

## ⚙️ Technologies utilisées

- **Python 3.10**
- **Pandas**, **openpyxl**, **python-docx**
- **HTML**, **CSS**, **JavaScript**
- **Chart.js** pour les graphiques de criticité
- **Jinja2** (optionnel) pour les templates Word

---

## 🎯 Objectif de professionnalisation (étape suivante)

Le projet sera amélioré pour devenir une solution intelligente, robuste et évolutive :

### 🔁 1. Automatiser la génération multi-gammes
- Boucle automatique sur chaque composant détecté dans le fichier Excel
- Génération d’une gamme personnalisée pour chaque sous-composant critique

### 🧠 2. Intégrer un moteur RAG + LLM (comme dans `chatbot_chaudiere_pdf`)
- Fournir un ensemble de documents techniques (PDF, Word, Excel, images)
- Intégrer ces documents dans une base vectorielle (ChromaDB)
- Interroger ces documents via un LLM (Claude, LLaMA3, etc.)
- Fournir des réponses contextualisées (défaut → AMDEC + gamme associée)

### 📦 3. Centraliser les modèles et templates
- Utilisation de fichiers `.docx` et `.xlsx` comme base de génération
- Système propre de templates à travers un backend Python intelligent

---

## 🧠 Objectif final

Créer un **assistant intelligent complet** capable de :

- Générer dynamiquement une AMDEC à partir d’un historique
- Générer automatiquement des gammes professionnelles (Word)
- Identifier les défaillances par composant
- Recommander des actions correctives
- Répondre aux questions des techniciens ou ingénieurs
- Fournir des plans de maintenance basés sur données et documents

---

## 🎯 Ce que Claude doit comprendre

> 🧾 **Prompt à partager avec Claude** :

```
Voici un projet d’automatisation de la maintenance chaudière.  
Il génère automatiquement une AMDEC et des gammes de maintenance à partir d’un fichier Excel, en utilisant des modèles Word prédéfinis (templates).  
Je souhaite rendre ce système plus intelligent, avec :
- une intégration des documents techniques (PDF, Excel, Word) via RAG
- un chatbot capable de répondre à des questions techniques
- la capacité de prédire des défaillances ou recommander des actions

Mon besoin est que tu comprennes toute la logique du projet actuel, les fichiers et les scripts, pour m’aider à :
1. Connecter les documents à un LLM (Claude ou autre)
2. Fournir des réponses précises et fiables aux techniciens
3. Améliorer l’automatisation et la qualité de sortie

Je te fournis le dépôt complet, les templates, les scripts Python, les documents d’entrée et les modèles visuels.
```

---

Développé par **Hamza** – PFE Maintenance TAQA / EMSI – 2025 🏭