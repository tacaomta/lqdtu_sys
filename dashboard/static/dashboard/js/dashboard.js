document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const filterPanel = document.getElementById("filterPanel");
    const overlay = document.getElementById("mobileOverlay");

    const sidebarBtn = document.getElementById("sidebarToggle");
    const filterBtn = document.getElementById("filterToggle");
    const icon = document.getElementById("filterToggleIcon");

    const tooltipList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );

    tooltipList.map(function (el) {
        return new bootstrap.Tooltip(el);
    });

    function handleResponsive() {

        if (window.innerWidth < 992) {

            sidebar.classList.add("mobile-hidden");

            if (filterPanel) {
                filterPanel.classList.add("hide");
            }

        } else {

            sidebar.classList.remove("mobile-hidden");

            overlay.classList.remove("active");
        }
    }

    handleResponsive();

    window.addEventListener(
        "resize",
        handleResponsive
    );

    sidebarBtn.addEventListener("click", function () {

        if (window.innerWidth < 992) {

            sidebar.classList.toggle("mobile-hidden");

            overlay.classList.toggle("active");

        } else {

            sidebar.classList.toggle("collapsed");

        }

    });

    if (filterBtn) {

        filterBtn.addEventListener("click", function () {

            if (window.innerWidth < 992) {

                filterPanel.classList.toggle("hide");

                overlay.classList.toggle("active");

            } else {

                filterPanel.classList.toggle("hide");

            }
            

            if (filterPanel.classList.contains("hide")) {

                icon.classList.remove(
                    "bi-chevron-right"
                );

                icon.classList.add(
                    "bi-chevron-left"
                );

            } else {

                icon.classList.remove(
                    "bi-chevron-left"
                );

                icon.classList.add(
                    "bi-chevron-right"
                );

            }

        });

    }

    overlay.addEventListener("click", function () {

        sidebar.classList.add("mobile-hidden");

        if (filterPanel) {
            filterPanel.classList.add("hide");
        }

        overlay.classList.remove("active");

    });

});