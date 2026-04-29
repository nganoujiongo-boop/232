from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import csv
import io
from datetime import datetime
import statistics
import math

app = Flask(__name__)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

DOMAINS = {
    "sante": {
        "label": "Santé & Épidémiologie",
        "icon": "🏥",
        "color": "#e74c3c",
        "fields": [
            {"name": "age", "label": "Âge (années)", "type": "number", "required": True},
            {"name": "sexe", "label": "Sexe", "type": "select", "options": ["Masculin", "Féminin"], "required": True},
            {"name": "poids", "label": "Poids (kg)", "type": "number", "required": True},
            {"name": "taille", "label": "Taille (cm)", "type": "number", "required": True},
            {"name": "tension_sys", "label": "Tension systolique (mmHg)", "type": "number", "required": True},
            {"name": "tension_dia", "label": "Tension diastolique (mmHg)", "type": "number", "required": True},
            {"name": "glycemie", "label": "Glycémie (g/L)", "type": "number", "required": False},
            {"name": "region", "label": "Région", "type": "select", "options": ["Centre", "Littoral", "Ouest", "Nord", "Sud", "Est", "Adamaoua", "Nord-Ouest", "Sud-Ouest", "Extrême-Nord"], "required": True},
            {"name": "antecedents", "label": "Antécédents médicaux", "type": "select", "options": ["Aucun", "Diabète", "Hypertension", "Cardiopathie", "Autre"], "required": True},
        ]
    },
    "agriculture": {
        "label": "Agriculture & Environnement",
        "icon": "🌾",
        "color": "#27ae60",
        "fields": [
            {"name": "culture", "label": "Type de culture", "type": "select", "options": ["Maïs", "Cacao", "Café", "Manioc", "Plantain", "Riz", "Sorgho", "Mil", "Coton"], "required": True},
            {"name": "superficie", "label": "Superficie (hectares)", "type": "number", "required": True},
            {"name": "rendement", "label": "Rendement (tonnes/ha)", "type": "number", "required": True},
            {"name": "pluviometrie", "label": "Pluviométrie (mm/an)", "type": "number", "required": False},
            {"name": "type_sol", "label": "Type de sol", "type": "select", "options": ["Argileux", "Sableux", "Limoneux", "Latéritique", "Volcanique"], "required": True},
            {"name": "engrais", "label": "Utilisation engrais", "type": "select", "options": ["Oui - Chimique", "Oui - Organique", "Non"], "required": True},
            {"name": "region", "label": "Région", "type": "select", "options": ["Centre", "Littoral", "Ouest", "Nord", "Sud", "Est", "Adamaoua", "Nord-Ouest", "Sud-Ouest", "Extrême-Nord"], "required": True},
            {"name": "annee", "label": "Année de production", "type": "number", "required": True},
        ]
    },
    "education": {
        "label": "Éducation & Performance",
        "icon": "🎓",
        "color": "#2980b9",
        "fields": [
            {"name": "niveau", "label": "Niveau scolaire", "type": "select", "options": ["Primaire", "Collège", "Lycée", "Licence", "Master", "Doctorat"], "required": True},
            {"name": "age_etudiant", "label": "Âge de l'étudiant", "type": "number", "required": True},
            {"name": "sexe", "label": "Sexe", "type": "select", "options": ["Masculin", "Féminin"], "required": True},
            {"name": "note_maths", "label": "Note Mathématiques (/20)", "type": "number", "required": True},
            {"name": "note_francais", "label": "Note Français (/20)", "type": "number", "required": True},
            {"name": "note_sciences", "label": "Note Sciences (/20)", "type": "number", "required": True},
            {"name": "heures_etude", "label": "Heures d'étude/semaine", "type": "number", "required": True},
            {"name": "acces_internet", "label": "Accès Internet", "type": "select", "options": ["Oui", "Non"], "required": True},
            {"name": "region", "label": "Région", "type": "select", "options": ["Centre", "Littoral", "Ouest", "Nord", "Sud", "Est", "Adamaoua", "Nord-Ouest", "Sud-Ouest", "Extrême-Nord"], "required": True},
        ]
    }
}

def get_data_file(domain):
    return os.path.join(DATA_DIR, f"{domain}.json")

def load_data(domain):
    f = get_data_file(domain)
    if os.path.exists(f):
        with open(f, "r", encoding="utf-8") as fp:
            return json.load(fp)
    return []

def save_data(domain, records):
    with open(get_data_file(domain), "w", encoding="utf-8") as fp:
        json.dump(records, fp, ensure_ascii=False, indent=2)

def compute_stats(values):
    values = [v for v in values if v is not None]
    if not values:
        return {}
    n = len(values)
    mean = sum(values) / n
    sorted_v = sorted(values)
    median = sorted_v[n // 2] if n % 2 else (sorted_v[n//2 - 1] + sorted_v[n//2]) / 2
    variance = sum((x - mean)**2 for x in values) / n if n > 1 else 0
    std = math.sqrt(variance)
    return {
        "n": n, "mean": round(mean, 2), "median": round(median, 2),
        "std": round(std, 2), "min": round(min(values), 2),
        "max": round(max(values), 2),
        "q1": round(sorted_v[n//4], 2),
        "q3": round(sorted_v[3*n//4], 2)
    }

@app.route("/")
def index():
    stats = {}
    for d in DOMAINS:
        records = load_data(d)
        stats[d] = len(records)
    return render_template("index.html", domains=DOMAINS, stats=stats)

@app.route("/collect/<domain>")
def collect(domain):
    if domain not in DOMAINS:
        return "Domaine introuvable", 404
    return render_template("collect.html", domain=domain, info=DOMAINS[domain])

@app.route("/api/submit/<domain>", methods=["POST"])
def submit(domain):
    if domain not in DOMAINS:
        return jsonify({"error": "Domaine introuvable"}), 404
    data = request.get_json()
    records = load_data(domain)
    data["_id"] = len(records) + 1
    data["_timestamp"] = datetime.now().isoformat()
    records.append(data)
    save_data(domain, records)
    return jsonify({"success": True, "total": len(records)})

@app.route("/analyse/<domain>")
def analyse(domain):
    if domain not in DOMAINS:
        return "Domaine introuvable", 404
    records = load_data(domain)
    fields = DOMAINS[domain]["fields"]
    
    numeric_stats = {}
    categorical_counts = {}
    
    for field in fields:
        fname = field["name"]
        if field["type"] == "number":
            vals = []
            for r in records:
                try:
                    vals.append(float(r.get(fname, 0)))
                except:
                    pass
            numeric_stats[fname] = {"label": field["label"], "stats": compute_stats(vals)}
        elif field["type"] == "select":
            counts = {}
            for r in records:
                v = r.get(fname, "N/A")
                counts[v] = counts.get(v, 0) + 1
            categorical_counts[fname] = {"label": field["label"], "counts": counts}
    
    return render_template("analyse.html",
        domain=domain, info=DOMAINS[domain],
        records=records,
        numeric_stats=numeric_stats,
        categorical_counts=categorical_counts,
        total=len(records)
    )

@app.route("/api/export/<domain>")
def export_csv(domain):
    if domain not in DOMAINS:
        return "Domaine introuvable", 404
    records = load_data(domain)
    if not records:
        return "Aucune donnée", 404
    
    output = io.StringIO()
    fields = [f["name"] for f in DOMAINS[domain]["fields"]] + ["_id", "_timestamp"]
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(records)
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"donnees_{domain}_{datetime.now().strftime('%Y%m%d')}.csv"
    )

@app.route("/api/data/<domain>")
def get_all_data(domain):
    return jsonify(load_data(domain))

@app.route("/api/delete/<domain>/<int:record_id>", methods=["DELETE"])
def delete_record(domain, record_id):
    records = load_data(domain)
    records = [r for r in records if r.get("_id") != record_id]
    save_data(domain, records)
    return jsonify({"success": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
