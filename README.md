# cartospec

Projet expérimental/test de **grammaire de visualisation cartographique** : décrire une carte de façon déclarative en Python, l'exporter en JSON, et l'afficher dans le navigateur avec [MapLibre GL JS](https://maplibre.org/).

```
API Python  ──►  spec JSON  ──►  compilateur TypeScript  ──►  carte MapLibre
(décrit)         (contrat)        (traduit en style)          (affiche)
```

L'approche s'inspire de [Vega-Lite](https://vega.github.io/vega-lite/) : la spec décrit la carto que l’onveut obtenir (des points de couleur, de forme de tailles différentes en fonction de la valeur d’un champ/feature, un popup au clic, etc.), le « compilateur » (renderer) traduit comment le dessiner avec MapLibre. 

Les specs carte JSON garantissent un lien agnostgique entre les deux : Python ne sait pas qu’on va utiliser MapLibre, le fichier JSON pourrait être traduit dans d’autres framework (to do : Leaflet), à l’autre bout TypeScript ne sais pas « d’où vient » le JSON. 

> **Statut : expérimental.** Ceci est un test pour expérimenter dans le cadre d’un projet plous ambitieux de toolbox pour des projets associatifs (to be announced). Sur ce dépôt la grammaire évolue étape par étape et n'est pas stable.

## Exemple

```python
from cartospec import Channel, Encoding, Layer, MapSpec, Popup

spec = (
    MapSpec(view={"center": (5.72, 45.19), "zoom": 9})
    .add_source("stations", url="/data/carburants_38.geojson")
    .add_layer(
        Layer(
            id="stations",
            data="stations",
            encoding=Encoding(color=Channel(value="#d62728"), size=Channel(value=5)),
            popup=Popup(title="ville", fields=["adresse", "gazole_prix", "sp95_prix"]),
        )
    )
)
spec.save("ts/public/specs/carburants.json")
```

## Structure

```text
.
├── data/
│   ├── raw/                     # données brutes téléchargées
│   └── prepare_carburants.py    # télécharge et preprocess le GeoJSON d'exemple
├── schema/
│   └── mapspec.schema.json      # JSON Schema de la spec, généré par Python
├── python/
│   ├── pyproject.toml
│   ├── cartospec/               # grammaire de spécification de la carte (modèles Pydantic)
│   └── examples/                # exemples de scripts qui construisent des specs cartes JSON
└── ts/                          # frontend pour tester la génération MapLibre (Vite + TypeScript + MapLibre)
    ├── public/
    │   ├── data/                # GeoJSON traités
    │   └── specs/               # specs cartes JSON produites par Python
    └── src/
        ├── types.ts             # la spec en TypeScript
        ├── render.ts            # le « compilateur » spec → MapLibre
        └── main.ts              # charge une spec et l'affiche
```

## Installation

Prérequis : Python 3.10+ et Node.js 20.19+ ou 22.12+.

```bash
# « Back » (API génération specs carte JSON, Python)
python3 -m venv .venv
source .venv/bin/activate
pip install -e python/

# « Front » (affichage carte depuis specs carte JSON, TS + MapLibre)
cd ts
npm install
cd ..
```

## Utilisation

```bash
# 1. Préparer les données (télécharge le jeu national au premier lancement)
python data/prepare_carburants.py

# 2. Générer la spec et le schéma
python python/examples/carburants.py

# 3. Lancer le serveur de développement
cd ts
npm run dev
```

Ouvrir l'adresse affichée (par défaut <http://localhost:5173>). Le paramètre d'URL `?spec=<nom>` choisit la spec chargée depuis `ts/public/specs/<nom>.json`.

Après une modification côté Python, relancer le script d'exemple puis recharger la page.

Pour la version de production :

```bash
cd ts
npm run build     # vérifie les types puis produit ts/dist/
npm run preview
```

## TO DO

- [x] **1** : chaîne complète, une couche de points à style fixe, popup au clic
- [ ] **2** : encodages liés aux données (`field` + `scale` → expressions MapLibre)
- [ ] **3** : plusieurs couches, formes et symboles
- [ ] **4** : filtres interactifs par catégorie
- [ ] **5** : agrégation par distance (clustering) selon le zoom
- [ ] **6** : sources liées (lieux + mesures successives) et résumés statistiques

Outillage envisagé : génération de `types.ts` depuis le JSON Schema, validation de la spec à l'exécution, puis une interface graphique d'édition de la spec.

## Données, sources, etc.

- Données d'exemple : [Prix des carburants en France, flux instantané v2](https://www.data.gouv.fr/datasets/6407d088d4e23dc662022e2c), DGCCRF, sous [Licence Ouverte 2.0](https://github.com/etalab/licence-ouverte/blob/master/LO.md).
- Fonds de carte : [OpenFreeMap](https://openfreemap.org/), données © contributeurs [OpenStreetMap](https://www.openstreetmap.org/copyright).

## Licence

À définir. Non pertinent pour un projet expérimental/test
