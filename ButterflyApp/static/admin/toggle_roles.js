document.addEventListener("DOMContentLoaded", function () {
    function setupToggle(checkbox1, checkbox2) {
        checkbox1.addEventListener("change", function () {
            if (checkbox1.checked) {
                checkbox2.checked = false;  // Uncheck the other option
            }
        });
        checkbox2.addEventListener("change", function () {
            if (checkbox2.checked) {
                checkbox1.checked = false;  // Uncheck the other option
            }
        });
    }

    let isExpert = document.querySelector("#id_is_expert");
    let isResearcher = document.querySelector("#id_is_researcher");

    if (isExpert && isResearcher) {
        setupToggle(isExpert, isResearcher);
    }
});
