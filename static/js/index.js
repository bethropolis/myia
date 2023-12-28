const theme = async (from) => {
  await ui("theme", from);
};

async function sendPostRequest(url, label, image_url, prediction = 0) {
  const data = {
    label: label,
    image_path: image_url,
    prediction: prediction
  };

  // Use axios to make a POST request with the data and headers
  await axios.post(url, { ...data }, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
    .then(response => data)
    .catch(error => {
      // Handle error
      console.error(error);
    });

}

function trigger_load() {
  htmx.trigger('#counter', 'pageLoaded');
}

function label_skip() {
  trigger_load();
}


async function label_bad(image_url, type, prediction = 0) {
  sendPostRequest(`/${type}_label`, 'bad', image_url, prediction);
  trigger_load();
}

async function label_good(image_url, type, prediction = 0) {
  sendPostRequest(`/${type}_label`, 'good', image_url, prediction);
  trigger_load();
}


function makeToast(text, duration = 3000, backgroundColor = "#ff0000") {
  Toastify({
    text: text,
    duration: duration,
    close: true,
    gravity: "top", 
    position: "center", 
    style: {
      background: backgroundColor,
    },
  }).showToast();
}

htmx.on('htmx:responseError', (evt) => {
  if (evt.detail.failed || evt.detail.xhr.status != 200) {
    // if responseText
    if (evt.detail.xhr.responseText) {
      makeToast(evt.detail.xhr.responseText);
    }
    else {
      makeToast("An error occured");
    }
  }
});
