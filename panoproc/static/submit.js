const submit = document.getElementById('submit');

submit.addEventListener('click', () => {
  const data = {};

  for (const [k, v] of Object.entries(elems)) {
    let propValue = v.innerText;
    if (['N/A', ''].includes(propValue)) {
      propValue = null;
    }
    data[k] = propValue;
  }
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
