import 'ol/ol.css';
import Map from 'ol/Map';
import OSM from 'ol/source/OSM';
import View from 'ol/View';
import GeoJSON from 'ol/format/GeoJSON';
import {Draw, Modify, Select, Snap} from 'ol/interaction';
import {Circle as CircleStyle, Fill, Icon, Stroke, Style} from 'ol/style';
import {Vector as VectorSource} from 'ol/source';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';
import milsymbol from 'milsymbol';


import { fromLonLat, toLonLat } from 'ol/proj';

const munich_LonLat = [11.57549, 48.13743];
const munich_mercator = fromLonLat(munich_LonLat);
const ratio = window.devicePixelRatio || 1;

const sidcs = {
  'radar' : "SFGPESR-----",
  'launcher' : "SFGPUCDHP---",
  'laser' : "SFGPEXL-----",
  'toc' : "SFGPUUSO----"
}


var source = new VectorSource();
var vector = new VectorLayer({
  source: source
});

function getStyle(style_val){
  var ms = new milsymbol.Symbol(sidcs[style_val]);
  var mycanvas = ms.setOptions({ size: 20 * ratio}).asCanvas();
  
  var st = new Style({
    image: new Icon(({
      scale: 1 / ratio,
      imgSize: [Math.floor(ms.getSize().width), Math.floor(ms.getSize().height)],
      img: (mycanvas)
    }))
  });

  return st;
}


var map = new Map({
  layers: [
    new TileLayer({
      source: new OSM(),
    }), vector ],
  target: 'map',
  view: new View({
    //center: [0, 0],
    center: munich_mercator,
    zoom: 8,
  }),
});





var draw, snap, modify, click; // global so we can remove them later
var typeSelect = document.getElementById('object_placement');
var featureID = 0;
var allFeatures = {};

function addInteraction() {
  var value = typeSelect.value;
  if (value === 'move'){
    snap = new Snap({source: source});
    map.addInteraction(snap);
    modify = new Modify({source: source});
    map.addInteraction(modify);

  }
  else if(value === 'delete'){
    snap = new Snap({source: source});
    map.addInteraction(snap);
    click = new Select();
    map.addInteraction(click);
    click.getFeatures().on('add', function(event) {
      selectedID = event.element.getProperties().id;
      
      currentFeatures = source.getFeatures();

      if(currentFeatures != null && currentFeatures.length > 0){
        for (x in currentFeatures){
          var properties = currentFeatures[x].getProperties();

          var id = properties.id;
            if (id == selectedID) {
              source.removeFeature(currentFeatures[x]);
              delete allFeatures[id];
              break;
            }
        }
      }
      console.log(allFeatures);

      
      text = "Removed " + selectedID + "<br>";
      text = "All Features:<br>";
      /*for (f in source.getFeatures()){
        text += allFeatures[f].toString() + "<br>";
        //text += toLonLat(f.getGeometry().getCoordinates()) + "<br>";
      }*/
      text += allFeatures + "<br>";
    })
  }
  else if(value === 'details'){
    panel = document.getElementById('detailPanel');
    panel.style.visibility='visible';
    snap = new Snap({source: source});
    map.addInteraction(snap);
    click = new Select({style: null});
    map.addInteraction(click);
    click.getFeatures().on('add', function(event) {
      featureObject = event.element
      console.log(featureObject);
      properties = featureObject.getProperties();
      console.log(properties);

      inner = "<table>"
        for(p in properties){
          if(p !== 'geometry'){
            inner += "<tr><td>" + p + "</td><td>" + properties[p] + "</td></tr>";
          }
          console.log(p + ": " + properties[p])
        }
      inner += "</table>"
      panel.innerHTML = inner;
    })
  }
  else if (value !== 'none') {
    draw = new Draw({
      source: source,
      type: 'Point',
    });
    draw.on('drawend', function (event) {
      var feature = event.feature;
      feature.setStyle(getStyle(value));
      feature.setProperties({
        'id': featureID,
        'sidc': sidcs[value],
        'classification': "friendly",
        'identification': document.getElementById('object_placement').options[typeSelect.selectedIndex].text
      });
      
      allFeatures[featureID] = feature;
      geo = feature.getGeometry();
      console.log(allFeatures);
      console.log(source.getFeatures());
      featureID = featureID + 1;
    })
    map.addInteraction(draw);
  }
}

/**
 * Handle change event.
 */
typeSelect.onchange = function () {
  document.getElementById('detailPanel').style.visibility='hidden';
  map.removeInteraction(draw);
  map.removeInteraction(snap);
  map.removeInteraction(modify);
  map.removeInteraction(click);
  addInteraction();
};

addInteraction();

document.getElementById('zoom_out').onclick = function () {
  var view = map.getView();
  var zoom = view.getZoom();
  view.setZoom(zoom - 1);
};

document.getElementById('zoom_in').onclick = function () {
  var view = map.getView();
  var zoom = view.getZoom();
  view.setZoom(zoom + 1);
};

document.getElementById('center_map').onclick = function () {
  var view = map.getView();
  var center_coo = [0,0];
  view.setCenter(center_coo);
}

document.getElementById('print_center').onclick = function () {
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

document.getElementById('display_tracks').onclick = function () {
  'use strict';

  const fs = require('fs');
  global.Buffer = global.Buffer || require("buffer").Buffer;

  let rawdata = fs.readFileSync('test1.json');
  let testJSON = JSON.parse(rawdata);

  var gs = new GeoJSON();

  var features = gs.readFeatures(testJSON);
}

document.getElementById('print_features').onclick = function () {
  text = "All Features:<br>";
  text += source.getFeatures() + "<br>";
  document.getElementById('text_below_map').innerHTML = text;
}

document.getElementById('parse_geojson').onclick = function () {
  var gs = new GeoJSON();
  // document.getElementById('json').textContent = gs.writeFeatures(source.getFeatures());
  console.log(gs.writeFeatures(source.getFeatures()));
}