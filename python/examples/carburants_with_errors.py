"""Teste la détection d’erreurs dans la construction de la spec (sources qui n’existe pas, coquile dans une clé…)."""
from pathlib import Path

from cartospec import Channel, Encoding, Layer, MapSpec, Popup

ROOT = Path(__file__).resolve().parents[2]

spec = (
    MapSpec(view={"center": (5.72, 45.19), "zoom": 9})
    .add_source("stations", url="/data/carburants_38.geojson")
    .add_layer(
        Layer(
            id="stations",
            data="stations",
            encoding=Encoding(color=Channel(value="#d62728"), size=Channel(value=5)),
            popup=Popup(title="ville", fields=["adresse", "gazole_prix", "sp95_prix", "e10_prix"]),
        )
    )
)

#MapSpec(view={"center": (5, 45)}).add_layer(Layer(id="x", data="nope"))

Layer(id="x", data="s", clor="red")

spec.save(ROOT / "ts" / "public" / "specs" / "carburants.json")
(ROOT / "schema" / "mapspec.schema.json").write_text(MapSpec.json_schema(), encoding="utf-8")
print(spec.to_json())