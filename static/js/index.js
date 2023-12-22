const theme = async (from) => {
  await ui("theme", from);
};

async function sendPostRequest(url, label, image_url) {
  const data = {
    label: label,
    image_path: image_url
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


async function label_bad(image_url, type) {
  sendPostRequest(`/${type}_label`, 'bad', image_url);
  trigger_load();
}

async function label_good(image_url, type) {
  sendPostRequest(`/${type}_label`, 'good', image_url);
  trigger_load();
}

document.addEventListener("DOMContentLoaded", function (event) {
  htmx.trigger('#counter', 'pageLoaded');
}
);
