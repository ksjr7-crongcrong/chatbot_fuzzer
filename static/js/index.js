bulmaToast.setDefaults({
    duration: 1000,
    position: "top-right",
    closeOnClick: true,
});

function errorToast(msg = "Error occured.") {
    bulmaToast.toast({
        message: msg,
        type: "is-danger",
        dismissible: true,
        pauseOnHover: true,
        animate: { in: "fadeIn", out: "fadeOut" },
    });
}

function warningToast(msg = "Warn") {
    bulmaToast.toast({
        message: msg,
        type: "is-warning",
        dismissible: true,
        pauseOnHover: true,
        animate: { in: "fadeIn", out: "fadeOut" },
    });
}

function successToast() {
    bulmaToast.toast({
        message: "Success",
        type: "is-success",
        dismissible: true,
        pauseOnHover: true,
        animate: { in: "fadeIn", out: "fadeOut" },
    });
}
function apiValidCheck() {
    let api_url = document.getElementsByName("api_url")[0].value;
    const data = { api_url: api_url };
    fetch("/api_valid_check", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status == "success") {
                url_checked = true;
                successToast();
            } else {
                url_checked = false;
                errorToast();
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function requireCheck() {
    let api_url = document.getElementsByName("api_url")[0].value;
    if (api_url == "") {
        warningToast("URL 주소를 입력해주세요.");
        return false;
    }
    if (url_checked == false) {
        warningToast("URL 주소를 확인해주세요.");
        return false;
    }
    let choice_count = document.querySelectorAll(
        'input[name="category"]:checked'
    ).length;
    if (choice_count == 0) {
        warningToast("카테고리를 하나 이상 확인해주세요.");
        return false;
    }
    return true;
}

let url_checked = false;