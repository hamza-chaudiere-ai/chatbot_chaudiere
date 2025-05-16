# 🤖 Chatbot Chaudière – Générateur AMDEC Automatisé

Ce projet représente une interface intelligente pour l’analyse de la maintenance préventive d’une chaudière industrielle.  
Il permet d'importer un fichier Excel historique, de générer automatiquement une AMDEC, de visualiser les criticités, et de proposer des actions correctives à travers une interface web interactive.

---

## 🎯 Objectif du projet

- Automatiser la génération de l’AMDEC à partir de l’historique d’arrêts
- Calculer la criticité (C = F × G × D)
- Proposer des actions correctives par sous-composant critique
- Visualiser les résultats sous forme de tableau dynamique et de graphiques
- Simplifier le travail du service maintenance avec un outil intégré

---

## ⚙️ Fonctionnalités principales

- 📁 **Import Excel** : Fichier historique structuré avec arrêts par composant
- 🧠 **Génération automatique de l’AMDEC** via analyse Python
- 📊 **Calcul des facteurs** : Fréquence (F), Gravité (G), Détectabilité (D)
- 🎯 **Affichage coloré** selon la criticité :
  - Rouge : C ≥ 40
  - Orange : 20 ≤ C < 40
  - Gris : C < 20 (masqué ou désactivé)
- 📈 **Graphique de statistiques** : Nombre de sous-composants par niveau de criticité
- 📄 **Téléchargement de l'AMDEC** : Exportable (Excel ou PDF à intégrer)
- 🖼️ Logos TAQA Maroc + AMDEC

---

## 🧪 Technologies utilisées

- **Python 3.10** : Traitement logique
- **Pandas, openpyxl** : Lecture/traitement Excel
- **python-docx (optionnel)** : Génération Word des gammes
- **HTML, CSS, JavaScript** : Interface utilisateur
- **Chart.js** : Visualisation graphique
- **Flask (ou autre)** : Back-end pour test local (si activé)

---

## 📂 Arborescence type

```
chatbot_chaudiere_nv/
│
├── index.html              # Page principale
├── style.css               # Design moderne et responsive
├── script.js               # Logique dynamique + affichage graphique
├── amdec_generator.py      # Script d’analyse AMDEC depuis Excel
├── uploads/                # Dossier pour fichiers Excel importés
├── images/                 # Logos, composants
└── README.md
```

---

## 📎 Exemple de fichier attendu (Excel)

Le fichier doit contenir :
- Composant / Sous-composant
- Mode de défaillance
- Cause, Effet
- Fréquence, Gravité, Détectabilité (ou automatiquement détectés)

---

## 🔗 Démo (optionnel si hébergé)

[https://hamza-chaudiere-ai.github.io/chatbot_chaudiere_nv](https://hamza-chaudiere-ai.github.io/chatbot_chaudiere_nv)

---

Développé par **Hamza**  
Projet PFE Maintenance 2025 – TAQA / EMSI 🏭