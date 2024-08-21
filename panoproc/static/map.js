const map = new Mazemap.Map({
  // container id specified in the HTML
  container: 'map',
  campuses: 111,
  // initial position in lngLat format
  center: { lng: 151.23140898946815, lat: -33.91702431505671 },
  // initial zoom
  zoom: 10,
  zLevel: 0,
  maxBounds: [
    [151.217893555, -33.9242064802],
    [151.244924424, -33.9126716815],
  ],
});

// Add zoom and rotation controls to the map.
map.addControl(new Mazemap.mapboxgl.NavigationControl());

map.on('load', () => {
  map.highlighter = new Mazemap.Highlighter(map, {
    showOutline: true,
    showFill: true,
    outlineColor: Mazemap.Util.Colors.MazeColors.MazeBlue,
    fillColor: Mazemap.Util.Colors.MazeColors.MazeBlue,
  });
  map.on('click', onMapClick);
});

let mazeMarker;

const onMapClick = (e) => {
  clearPoiMarker();

  const lngLat = e.lngLat;
  const zLevel = map.zLevel;
  Mazemap.Data.getPoiAt(lngLat, zLevel)
    .then((poi) => {
      processPoiData(poi, lngLat);
      placePoiMarker(poi);
    })
    .catch(() => false);
};

const setDefaults = () => {
  Object.keys(elems).forEach((key) => {
    elems[key].innerText = 'N/A';
  });
};

const processPoiData = (poi, clickLngLat = null) => {
  document.getElementById('submit').removeAttribute('disabled');
  if (!poi) {
    setDefaults();
    if (!clickLngLat) return;
    elems['latitude'].innerText = clickLngLat.lat;
    elems['longitude'].innerText = clickLngLat.lng;
    return;
  }
  const props = poi.properties;

  console.log(props);

  elems['latitude'].innerText = props.point.coordinates[0];
  elems['longitude'].innerText = props.point.coordinates[1];
  elems['title'].innerText = props.title;
  elems['building'].innerText = props.buildingName;
  elems['floor'].innerText = props.floorName;
};

const clearPoiMarker = (poi) => {
  if (mazeMarker) {
    mazeMarker.remove();
  }
  map.highlighter.clear();
};

const placePoiMarker = (poi) => {
  const lngLat = Mazemap.Util.getPoiLngLat(poi);

  mazeMarker = new Mazemap.MazeMarker({
    color: '#ff00cc',
    innerCircle: true,
    innerCircleColor: '#FFF',
    size: 34,
    innerCircleScale: 0.5,
    zLevel: poi.properties.zLevel,
  })
    .setLngLat(lngLat)
    .addTo(map);

  // If we have a polygon, use the default 'highlight' function to draw a marked outline around the POI.
  if (poi.geometry.type === 'Polygon') {
    map.highlighter.highlight(poi);
  }
  map.flyTo({ center: lngLat, zoom: 19, speed: 0.5 });
};
