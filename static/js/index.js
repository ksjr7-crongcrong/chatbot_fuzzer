bulmaToast.setDefaults({
    duration: 1000,
    position: 'top-right',
    closeOnClick: true,
})

function errorToast() {
    bulmaToast.toast({
      message: 'Error occured.',
      type: 'is-danger',
      dismissible: true,
      pauseOnHover: true,
      animate: { in: 'fadeIn', out: 'fadeOut' },
    })
}

function successToast() {
    bulmaToast.toast({
      message: 'Success',
      type: 'is-success',
      dismissible: true,
      pauseOnHover: true,
      animate: { in: 'fadeIn', out: 'fadeOut' },
    })
}
function apiValidCheck() {
    let api_url=document.getElementById("api_url").value;
    const data = { api_url: api_url };
    fetch('/api_valid_check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then(response => response.json())
      .then(data => {
        if (data.status == "success") {
          successToast();
        } else {
          errorToast();
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
}