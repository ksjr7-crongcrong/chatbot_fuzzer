document.addEventListener('readystatechange', event => {

    // When HTML/DOM elements are ready:
    if (event.target.readyState === "interactive") {   //does same as:  ..addEventListener("DOMContentLoaded"..
        // alert("hi 1");
    }

    // When window loaded ( external resources are loaded too- `css`,`src`, etc...)
    if (event.target.readyState === "complete") {
        
        var bar = new ldBar(".myBar", {
            "stroke": '#cee5d5',
            "stroke-width": 10,
            "preset": "circle",
            "value": 0
        });

        check_str = document.getElementById("checkToken").value;
        check_list = check_str.split("|");
        (async function loops() {
            for (const [idx, item] of check_list.entries()) {
                const loop = await fetch("/check/" + item)
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.status == "success") {
                            bar.set(100 * (idx + 1) / check_list.length);
                            document.querySelector('div[id="result"][name$=' + item + ']').innerText = "done";
                        }
                    });
            }
            document.querySelector('div[id="goResultView"]').innerHTML = '<a href="/fuzz_done" class="btn btn-primary btn-lg" role="button">결과 확인하기</a>';
        })();   
    }
});

