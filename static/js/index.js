function sendPostRequest(label, image_url) {
  const url = '/label';
  const data = {
    label: label,
    image_path: image_url
  };

  // Use axios to make a POST request with the data and headers
  axios.post(url, { ...data }, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
    .then(response => {
      // Handle success
      console.log(response.data);
    })
    .catch(error => {
      // Handle error
      console.error(error);
    });

}


function label_bad(image_url) {
  sendPostRequest('bad', image_url);
}

function label_good(image_url) {
  sendPostRequest('good', image_url);
}