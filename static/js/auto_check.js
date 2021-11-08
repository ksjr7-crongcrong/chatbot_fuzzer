document.addEventListener('readystatechange', event => {

    // When HTML/DOM elements are ready:
    if (event.target.readyState === "interactive") {   //does same as:  ..addEventListener("DOMContentLoaded"..
        // alert("hi 1");
    }

    // When window loaded ( external resources are loaded too- `css`,`src`, etc...)
    if (event.target.readyState === "complete") {
        check_str = document.getElementById("checkToken").value;
        check_list = check_str.split("|");
        (async function loops() {
            for (const [idx, item] of check_list.entries()) {
                const loop = await fetch("/check/" + item)
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.status == "success") {
                            document.querySelector('div[id="result"][name$=' + item + ']').innerText = "done";
                        }
                    });
            }
        })();
    }
});

