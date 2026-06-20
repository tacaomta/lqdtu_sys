document.addEventListener(

    "DOMContentLoaded",

    function () {
        let currentPage = 1;
        const pageSize = 20;

        async function loadAuthors(page = 1) {

            const keyword = document.getElementById("keyword").value;
            const pageSize =
                document.getElementById(
                    "pageSize"
                ).value;

            const response = await fetch(
                `/accounts/admin/authors/api/?page=${currentPage}&page_size=${pageSize}&keyword=${encodeURIComponent(keyword)}`
            );

            const data = await response.json();

            const tbody = document.getElementById("authorTableBody");
            tbody.innerHTML = "";

            data.records.forEach((author, index) => {
                const stt =

                    ((currentPage - 1) * pageSize)

                    +

                    index

                    +

                    1;
                tbody.innerHTML += `
                    <tr>
                        <td>${stt}</td>
                        <td>${author.name}</td>
                        <td>${author.university || ""}</td>
                        <td>${author.country || ""}</td>
                    </tr>
                    `;
            });

            renderSummary(data);
            renderPagination(data);
        }

        document.getElementById("keyword").addEventListener("keyup", function (e) {
            if (e.key === "Enter") {
                loadAuthors(1);
            }
        });



        function renderSummary(

            data

        ) {

            document

                .getElementById(

                    "summary"

                )

                .innerHTML =

                `Hiển thị ${data.start_index} - ${data.end_index} trên ${data.total_records} bản ghi`;

        }


        function renderPagination(

            data

        ) {


            const pagination =

                document.getElementById(

                    "pagination"

                );

            pagination.innerHTML = "";

            const currentPage =
                data.current_page;

            const totalPages =
                data.num_pages;

            if (totalPages <= 1) {

                return;

            }

            // First

            if (currentPage > 1) {

                pagination.innerHTML += `

                    <li class="page-item">

                        <button

                            class="page-link page-btn"

                            data-page="1"

                        >

                            First

                        </button>

                    </li>

                `;

            }

            // Previous

            if (data.has_previous) {

                pagination.innerHTML += `

                    <li class="page-item">

                        <button

                            class="page-link page-btn"

                            data-page="${currentPage - 1}"

                        >

                            Previous

                        </button>

                    </li>

                `;

            }

            // Page window

            const startPage =
                Math.max(
                    1,
                    currentPage - 3
                );

            const endPage =
                Math.min(
                    totalPages,
                    currentPage + 3
                );

            for (let page = startPage; page <= endPage; page++) {

                if (page === currentPage) {

                    pagination.innerHTML += `

                        <li class="page-item active">

                            <span class="page-link">

                                ${page}

                            </span>

                        </li>

                    `;

                } else {

                    pagination.innerHTML += `

                        <li class="page-item">

                            <button

                                class="page-link page-btn"

                                data-page="${page}"

                            >

                                ${page}

                            </button>

                        </li>

                    `;

                }

            }

            // Next

            if (data.has_next) {

                pagination.innerHTML += `

                    <li class="page-item">

                        <button

                            class="page-link page-btn"

                            data-page="${currentPage + 1}"

                        >

                            Next

                        </button>

                    </li>

                `;

            }

            // Last

            if (currentPage < totalPages) {

                pagination.innerHTML += `

                    <li class="page-item">

                        <button

                            class="page-link page-btn"

                            data-page="${totalPages}"

                        >

                            Last

                        </button>

                    </li>

                `;

            }

        }

        document.addEventListener(

            "click",

            function (e) {

                if (

                    e.target.classList.contains(

                        "page-btn"

                    )

                ) {
                    console.log("click");

                    currentPage = parseInt(

                        e.target.dataset.page

                    );

                    loadAuthors();

                }

            }

        );
        document
            .getElementById(
                "pageSize"
            )
            .addEventListener(

                "change",

                () => loadAuthors()

            );

        document
            .getElementById(
                "keyword"
            )
            .addEventListener(

                "keyup",

                () => loadAuthors()

            );

        loadAuthors();

    }
)