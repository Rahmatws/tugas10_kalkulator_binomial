document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const inputs = document.querySelectorAll("input");

    inputs.forEach(input => {
        input.addEventListener("input", function() {
            if (parseFloat(input.value) < 0) {
                alert("Values must be positive!");
                input.value = '';
            }
        });
    });

    form.addEventListener("submit", function(event) {
        const p = parseFloat(document.getElementById("p").value);
        if (p > 1 || p < 0) {
            alert("Probability (p) must be between 0 and 1!");
            event.preventDefault();
        }
    });
});
