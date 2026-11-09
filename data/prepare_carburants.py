"""Télécharge les stations-service et produit un GeoJSON allégé pour l'Isère."""
import json
import urllib.request
from pathlib import Path
import gzip

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "carburants_france.geojson"
OUT = ROOT / "ts" / "public" / "data" / "carburants_38.geojson"
URL = (
    "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
    "prix-des-carburants-en-france-flux-instantane-v2/exports/geojson"
)

# Champs conservés : à ajuster après l'inspection ci-dessous
KEEP = ["id", "adresse", "ville", "cp",
        "gazole_prix", "sp95_prix", "sp98_prix", "e10_prix", "e85_prix"]

def load_json(path: Path) -> dict:
    """Lit un fichier JSON, compressé en gzip ou non."""
    data = path.read_bytes()
    if data[:2] == b"\x1f\x8b":          # signature d'un fichier gzip
        data = gzip.decompress(data)
    return json.loads(data.decode("utf-8"))

def main() -> None:
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        print("Téléchargement…")
        urllib.request.urlretrieve(URL, RAW)

    fc = load_json(RAW)
    features = fc["features"]
    print(f"{len(features)} stations en France")
    print("Champs disponibles :", sorted(features[0]["properties"]))

    isere = [
        f for f in features
        if f.get("geometry") and str(f["properties"].get("cp", "")).startswith("38")
    ]
    for f in isere:
        f["properties"] = {k: f["properties"].get(k) for k in KEEP}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps({"type": "FeatureCollection", "features": isere}, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"{len(isere)} stations écrites dans {OUT}")


if __name__ == "__main__":
    main()