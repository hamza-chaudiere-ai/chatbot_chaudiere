# 🤖 Chatbot Chaudière – Générateur AMDEC & Gammes Automatisé (Projet Intelligent)

Ce projet représente une solution semi-automatisée de maintenance préventive d’une chaudière industrielle.  
Il offre une interface web pour importer un fichier Excel historique, générer dynamiquement une AMDEC colorée, produire des gammes de maintenance personnalisées à partir de templates, et visualiser les criticités sous forme de graphique.

---

## ✅ Fonctionnalités actuelles

- 📁 Import de fichiers Excel avec historiques d’arrêts
- 🧠 Génération automatique d’un tableau AMDEC (F, G, D, C)
- 📄 Création d’une gamme de maintenance basée sur des **templates Word**
- 🎯 Criticité calculée automatiquement avec **mise en couleur dynamique**
- 📊 Affichage d’un **graphe de criticité**
- 🖼️ Intégration de logos (TAQA, AMDEC)
- Interface HTML + JS fluide et interactive

---

## ⚙️ Technologies utilisées

- **Python 3.10** (Pandas, openpyxl, python-docx)
- **HTML / CSS / JavaScript** pour l’interface
- **Chart.js** pour les graphiques dynamiques
- **Jinja2 / Templates personnalisés** pour la génération de documents

---

## 📂 Arborescence du projet

```
chatbot_chaudiere_nv/
│
├── index.html
├── style.css
├── script.js
├── amdec_generator.py
├── maintenance_planner.py
├── templates/                # Templates Word (gammes)
├── data/                     # Historiques Excel
├── images/                   # Logos, composants
└── README.md
```

---

## 🚀 Objectif de professionnalisation

Le projet évolue vers une solution complète **assistée par intelligence artificielle**, intégrant :

### 🧱 1. Utilisation systématique de templates
- Formatage professionnel des gammes selon un modèle Word standardisé
- Génération automatique multi-gammes (1 gamme par composant)

### 🔗 2. Connexion à un moteur **RAG + LLM**
- Base documentaire (PDF, Word, Excel, images)
- Intégration dans un moteur vectoriel (ex : ChromaDB)
- Utilisation d’un modèle LLM (Claude ou LLaMA3) pour répondre à :
  - "Quel est le défaut probable ?"
  - "Donne-moi la gamme de l’économiseur HT"
  - "Quelle action corrective appliquer au percement ?"

### 🧠 3. Objectif final : assistant Claude

Le projet sera connecté à Claude pour :
- Générer automatiquement AMDEC + gamme
- Répondre à des questions techniques à partir des documents
- Recommander des plans d’action contextualisés
- Récupérer les templates et les fichiers associés à chaque réponse

---

## 📌 Livrables attendus pour Claude

- `README.md` explicatif clair
- `amdec_generator.py`, `maintenance_planner.py`
- Templates `.docx`, fichiers Excel test
- Dossier `/images`, `/data`, `/templates`
- JSONL ou base vectorielle pour assistant Claude

---

Développé par **Hamza** – PFE Maintenance TAQA / EMSI – 2025 🏭