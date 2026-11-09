"""Grammaire carto, v0.1 : spec décrite via Pydantic."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Strict(BaseModel):
    """Refus clefs inconnues"""
    model_config = ConfigDict(extra="forbid")


class Channel(Strict):
    """Un seul canal visuel. 1 valeur fixe pr le moment. Plus tard : un champ + une échelle, etc."""
    value: str | float | None = None


class Encoding(Strict):
    color: Channel | None = None
    size: Channel | None = None
    opacity: Channel | None = None


class Popup(Strict):
    title: str | None = None            # champ affiché en titre
    fields: list[str] = Field(min_length=1)


class Layer(Strict):
    id: str
    data: str                           # nom d'une source déclarée dans MapSpec.data
    mark: Literal["point"] = "point"
    encoding: Encoding = Field(default_factory=Encoding)
    popup: Popup | None = None


class Source(Strict):
    type: Literal["geojson"] = "geojson"
    url: str


class View(Strict):
    center: tuple[float, float]         # [longitude, latitude]
    zoom: float = 5
    basemap: Literal["positron", "liberty", "bright"] = "positron"


class MapSpec(Strict):
    version: Literal["0.1"] = "0.1"
    view: View
    data: dict[str, Source] = {}
    layers: list[Layer] = []

    @model_validator(mode="after")
    def check_references(self) -> MapSpec:
        for layer in self.layers:
            if layer.data not in self.data:
                raise ValueError(f"La couche '{layer.id}' référence une source inconnue : '{layer.data}'")
        return self

    # --- chaque méthode renvoie une NOUVELLE spec validée ---
    def add_source(self, name: str, url: str) -> MapSpec:
        return self._with(data={**self.data, name: Source(url=url)})

    def add_layer(self, layer: Layer) -> MapSpec:
        return self._with(layers=[*self.layers, layer])

    def _with(self, **changes) -> MapSpec:
        # model_validate relance toute la validation, y compris check_references
        return MapSpec.model_validate({**self.model_dump(), **changes})

    # --- export ---
    def to_json(self) -> str:
        return self.model_dump_json(indent=2, exclude_none=True)

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def json_schema(cls) -> str:
        return json.dumps(cls.model_json_schema(), indent=2, ensure_ascii=False)