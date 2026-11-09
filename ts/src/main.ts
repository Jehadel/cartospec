import "maplibre-gl/dist/maplibre-gl.css";
import "./style.css";
import * as maplibregl from "maplibre-gl";
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?url";

maplibregl.setWorkerUrl(workerUrl);

const map = new maplibregl.Map({
  container: "map",                                         // id de la <div>
  style: "https://tiles.openfreemap.org/styles/positron",
  center: [5.72, 45.19],                                    // [longitude, latitude]
  zoom: 9,
});
map.addControl(new maplibregl.NavigationControl());         // boutons zoom / rotation