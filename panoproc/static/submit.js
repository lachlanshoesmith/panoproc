const submit = document.getElementById('submit');

submit.addEventListener('click', () => {
  const basicMetadata = {};

  for (const [k, v] of Object.entries(elems)) {
    let propValue = v.innerText;
    if (['N/A', ''].includes(propValue)) {
      propValue = null;
    }
    basicMetadata[k] = propValue;
  }

  const hotspotsBody = document.getElementById('hotspots-body');
  const hotspots = [];
  for (const tr of hotspotsBody.children) {
    const hotspot = {};
    for (const td of tr.children) {
      const property = td.classList[0];
      const val = td.innerText;
      if (!isNaN(val)) {
        hotspot[property] = Number(val);
      } else {
        hotspot[property] = val;
      }
    }
    hotspot.sceneId = hotspot.title;
    hotspot.type = 'scene';
    hotspots.push(hotspot);
  }

  const data = {
    ...basicMetadata,
    panorama: document.getElementById('filename').innerText,
    type: 'equirectangular',
    // TODO: allow these values to be based on current perspective
    // in the editor
    hfov: 0,
    pitch: 0,
    yaw: 0,
    hotspots: hotspots,
  };

  fetch('/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then(() => location.reload())
    .catch((e) => console.error(e));
});
