import './public/leaflet.css'
import './public/leaflet.js'
import './public/style.css'

import scaphImg from './public/Scaphandrier_s.png'
import workerImg from './public/w.png'
import workerSImg from './public/wshade.png'

fetch('https://filedn.nsix.fr/data/scaphdata.json')
.then(resp => resp.json())
.then(json => {
  let map = L.map('map').setView([46.71, 1.08], 6);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  let scaphIcon = L.icon({
    iconUrl: scaphImg,
    // shadowUrl: 'public/wshade.png',

    iconSize:     [40, 54], // size of the icon
    // shadowSize:   [70, 40], // size of the shadow
    iconAnchor:   [20, 56], // point of the icon which will correspond to marker's location
    // shadowAnchor: [16, 40],  // the same for the shadow
    popupAnchor:  [2, -20] // point from which the popup should open relative to the iconAnchor
  });

  let workerIcon = L.icon({
    iconUrl: workerImg,
    shadowUrl: workerSImg,

    iconSize:     [32, 42], // size of the icon
    shadowSize:   [70, 40], // size of the shadow
    iconAnchor:   [16, 40], // point of the icon which will correspond to marker's location
    shadowAnchor: [16, 40],  // the same for the shadow
    popupAnchor:  [0, -40] // point from which the popup should open relative to the iconAnchor
  });

  let g = []
  for (let elt of json.entreprises) {
    let mark = L.marker([elt.loc.lat, elt.loc.lon]);
    let popup = `<b><a href="${elt.url}">${elt.name}</a></b><p>${elt.loc.name}</p>`
    if(elt.logo) {
      popup += `<img src="${elt.logo}" alt="logo">`
    }
    mark.bindPopup(popup);
    g.push(mark);
  }
  let entreprises = L.layerGroup(g).addTo(map);

  g = []
  for (let elt of json.interim) {
    let mark = L.marker([elt.loc.lat, elt.loc.lon], {icon: workerIcon});
    let popup = `<b><a href="${elt.url}">${elt.name}</a></b><p>${elt.loc.name}</p>`
    if(elt.logo) {
      popup += `<img src="${elt.logo}" alt="logo">`
    }
    mark.bindPopup(popup);
    g.push(mark);
  }
  let interim = L.layerGroup(g).addTo(map);

  g = []
  for (let elt of json.formation) {
    let mark = L.marker([elt.loc.lat, elt.loc.lon], {icon: scaphIcon});
    let popup = `<b><a href="${elt.url}">${elt.name}</a></b><p>${elt.loc.name}</p>`
    if(elt.logo) {
      popup += `<img src="${elt.logo}" alt="logo">`
    }
    mark.bindPopup(popup);
    g.push(mark);
  }
  let formations = L.layerGroup(g);

  let overlayMaps = {
    "Entreprises": entreprises,
    "Interim": interim,
    "Formations": formations
  };

  let layerControl = L.control.layers({}, overlayMaps).addTo(map);
});
