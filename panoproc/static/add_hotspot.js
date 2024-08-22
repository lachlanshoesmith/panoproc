const addHotspot = document.getElementById('add-hotspot');
const hotspotsBody = document.getElementById('hotspots-body');

const hotspotDataElems = {
  title: document.getElementById('hotspot_filename'),
  pitch: document.getElementById('pitch'),
  yaw: document.getElementById('yaw'),
  targetPitch: document.getElementById('centre-pitch'),
  targetYaw: document.getElementById('centre-yaw'),
  hfov: document.getElementById('hfov'),
};

const createHotspot = (hotspot) => {
  const tr = document.createElement('tr');
  for (const [k, v] of Object.entries(hotspot)) {
    const td = document.createElement('td');
    td.classList.add(k);
    td.innerText = v;
    tr.appendChild(td);
  }
  return tr;
};

addHotspot.addEventListener('click', () => {
  const hotspot = {};

  for (const [k, v] of Object.entries(hotspotDataElems)) {
    let propValue;
    if (k == 'title') {
      propValue = v.value;
    } else {
      propValue = v.innerText;
    }

    if (['N/A', ''].includes(propValue)) {
      alert('Please fill in ' + k);
      return;
    }
    hotspot[k] = propValue;
  }
  hotspotsBody.appendChild(createHotspot(hotspot));
});
