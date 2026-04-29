# DataCollect CM — INF232 EC2

Application de **collecte et d'analyse descriptive des données** développée en Python (Flask).

## 3 Domaines actifs

| Domaine | Variables clés |
|---------|----------------|
| 🏥 **Santé & Épidémiologie** | Âge, poids, taille, tension, glycémie, antécédents |
| 🌾 **Agriculture & Environnement** | Culture, superficie, rendement, type sol, engrais |
| 🎓 **Éducation & Performance** | Notes, niveau, heures d'étude, accès internet |

## Fonctionnalités

- ✅ Formulaires de saisie structurés par domaine
- ✅ Validation des données côté client et serveur
- ✅ Statistiques descriptives : moyenne, médiane, écart-type, min, max, Q1, Q3
- ✅ Distributions des variables catégorielles
- ✅ Tableau des données brutes
- ✅ Export CSV pour analyses avancées (régression, classification)
- ✅ Interface responsive et moderne

## Lancer en local

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

---

## 🚀 Déploiement sur Render (étapes détaillées)

### Étape 1 — Préparer GitHub
1. Créez un compte sur [github.com](https://github.com)
2. Créez un nouveau dépôt public : `datacollect-cm`
3. Uploadez tous les fichiers du projet :
   ```bash
   git init
   git add .
   git commit -m "Initial commit — DataCollect CM"
   git remote add origin https://github.com/VOTRE_USERNAME/datacollect-cm.git
   git push -u origin main
   ```

### Étape 2 — Créer un compte Render
1. Allez sur [render.com](https://render.com)
2. Cliquez **Get Started for Free**
3. Inscrivez-vous avec votre email ou GitHub

### Étape 3 — Créer un nouveau Web Service
1. Dans le dashboard Render, cliquez **New +** → **Web Service**
2. Choisissez **Connect a repository**
3. Sélectionnez votre dépôt `datacollect-cm`
4. Configurez :
   - **Name** : `datacollect-cm`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`
   - **Plan** : Free

### Étape 4 — Déployer
1. Cliquez **Create Web Service**
2. Render va automatiquement :
   - Installer les dépendances (`Flask`, `gunicorn`)
   - Lancer l'application
3. Attendez 2-3 minutes que le build se termine
4. Votre URL sera : `https://datacollect-cm.onrender.com`

### Étape 5 — Persistance des données (optionnel)
> Sur le plan gratuit de Render, le disque est éphémère (données perdues au redémarrage).
> Pour persister les données, ajoutez un **Disk** dans Render :
> - Settings → Disks → Add Disk
> - Mount Path : `/app/data`
> - Size : 1 GB (gratuit)

### Structure des fichiers à uploader sur GitHub
```
datacollect-cm/
├── app.py              # Application Flask principale
├── requirements.txt    # Dépendances Python
├── Procfile            # Commande de démarrage (Heroku/Render)
├── render.yaml         # Config automatique Render
├── templates/
│   ├── base.html       # Template de base
│   ├── index.html      # Page d'accueil
│   ├── collect.html    # Formulaire de collecte
│   └── analyse.html    # Page d'analyses
└── data/               # Données JSON (créé automatiquement)
```

---

## Technologies utilisées

- **Backend** : Python 3.11 + Flask 3.0
- **Serveur WSGI** : Gunicorn
- **Stockage** : JSON (fichiers locaux)
- **Frontend** : HTML5 + CSS3 + JavaScript vanilla
- **Déploiement** : Render.com

## Lien vers l'application (après déploiement)

```
https://datacollect-cm.onrender.com
```
