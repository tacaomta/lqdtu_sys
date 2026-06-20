document.addEventListener(

    "DOMContentLoaded",

    function () {
        let currentPage = 1;
        const pageSize = 20;

        async function loadUniversities(page = 1) {

            const keyword = document.getElementById("keyword").value;
            const pageSize = document.getElementById("pageSize").value;
            const response = await fetch(`/accounts/admin/universities/api/?page=${currentPage}&page_size=${pageSize}&keyword=${encodeURIComponent(keyword)}`);
            const data = await response.json();

            const tbody = document.getElementById("universityTableBody");
            tbody.innerHTML = "";

            data.records.forEach((u, index) => {
                const stt = ((currentPage - 1) * pageSize) + index + 1;

                tbody.innerHTML += `
                    <tr>
                        <td class="text-center">${stt}</td>
                        <td>${u.name}</td>
                        <td>${u.country}</td>
                        <td class="text-center">${u.author_count}</td>
                    </tr>
                    `;
            });

            renderSummary(data);
            renderPagination(data);
        }

        document.getElementById("keyword").addEventListener("keyup", function(e) {
            if (e.key === "Enter") loadUniversities();
        });

        document.addEventListener(

            "click",

            function (e) {

                if (

                    e.target.classList.contains(

                        "page-btn"

                    )

                ) {

                    currentPage = parseInt(

                        e.target.dataset.page

                    );

                    loadUniversities();

                }

            }

        );

        document
            .getElementById(
                "pageSize"
            )
            .addEventListener(

                "change",

                () => loadUniversities()

            );

        document
            .getElementById(
                "keyword"
            )
            .addEventListener(

                "keyup",

                () => loadUniversities()

            );

        loadUniversities();
    }
);