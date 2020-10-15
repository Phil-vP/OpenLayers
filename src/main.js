import 'ol/ol.css';
import Map from 'ol/Map';
import OSM from 'ol/source/OSM';
import TileLayer from 'ol/layer/Tile';
import View from 'ol/View';
import { fromLonLat, toLonLat } from 'ol/proj';

const munich_LonLat = [11.581981, 48.135125];
const munich_mercator = fromLonLat(munich_LonLat);

var map = new Map({
  layers: [
    new TileLayer({
      source: new OSM(),
    }) ],
  target: 'map',
  view: new View({
    center: [0, 0],
    zoom: 2,
  }),
});

document.getElementById('zoom-out').onclick = function () {
  var view = map.getView();
  var zoom = view.getZoom();
  view.setZoom(zoom - 1);
};

document.getElementById('zoom-in').onclick = function () {
  var view = map.getView();
  var zoom = view.getZoom();
  view.setZoom(zoom + 1);
};

document.getElementById('center-map').onclick = function () {
  var view = map.getView();
  var center_coo = [0,0];
  view.setCenter(center_coo);
}

document.getElementById('print-center').onclick = function () {
  var bottom_text = document.getElementById('text_below_map');
  var view = map.getView();
  var center_coo = view.getCenter();
  var center_coo_LonLat = toLonLat(center_coo);
  bottom_text.innerHTML = "Center is " + center_coo_LonLat;
}

document.getElementById('center_munich').onclick = function () {
  var view = map.getView();
  view.setCenter(munich_mercator);
  var bottom_text = document.getElementById('text_below_map');
  bottom_text.innerHTML = "Center set to " + munich_LonLat;
}