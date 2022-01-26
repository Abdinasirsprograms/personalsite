window.onload = (event) => {
    let connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    let loader = document.querySelector('#loaderContainer');
    // delay to make sure loading screen shows up first if load time is quick
    // else the assumption is you've properly already noticed it
    if (connection) {
        if (connection.downlink >= 1.5) {
            setTimeout(function() {
                loader.classList.add("hidden");
            }, 850);
        }
        else{
            loader.classList.add("hidden");
        };
    };
    loader.addEventListener("animationend", function() {
    loader.parentNode.removeChild(loader);
    });
};

