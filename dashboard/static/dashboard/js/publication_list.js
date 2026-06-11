document.addEventListener(

    "DOMContentLoaded",

    async function(){        

        function renderTable(

            publications

        ) {

            const tbody =

                document.getElementById(

                    "publication-table-body"

                );

            tbody.innerHTML = "";

            publications.forEach(

                publication => {

                    type = "";
                    if (publication.document_type == "Article") {
                        type += '<span class="badge bg-primary">';
                    }
                    else if (publication.document_type == "Conference paper"){
                        type += '<span class="badge bg-success">';
                    }
                    else if (publication.document_type == "Review")
                    {
                        type += '<span class="badge bg-warning text-dark">';
                    }
                    else{
                        type += '<span class="badge bg-secondary">';
                    }
                    type += publication.document_type +'</span>';

                    tbody.innerHTML += `

                <tr>

                    <td>${publication.year}</td>

                    <td>${type}</td>

                    <td>
                        ${publication.doi ?

                        `<a href="https://doi.org/${publication.doi}" target="_blank">${publication.title}</a>`

                            :

                            "-"

                        }
                    </td>

                    <td>${publication.authors}</td>

                    <td>${publication.citation}</td>

                    <td>${publication.journal}</td>

                </tr>

            `;

                }

            );

        }

        function renderSummary(

            data

        ) {

            document

                .getElementById(

                    "publication-summary"

                )

                .innerHTML =

                `Hiển thị ${data.start_index} - ${data.end_index} trên ${data.total_count} CBKH`;

        }


        function renderPagination(

            data

        ) {

            const pagination =

                document.getElementById(

                    "publication-pagination"

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


        let currentPage = 1;

        let currentKeyword = "";

        let currentPageSize = 10;

        let searchTimeout = null;
        let currentYear = "";

        let currentDocumentType = "";

        async function loadPublications() {

            const response = await fetch(

                `/api/publications/?page=${currentPage}` +

                `&page_size=${currentPageSize}` +

                `&keyword=${encodeURIComponent(currentKeyword)}` +

                `&year=${encodeURIComponent(currentYear)}` +

                `&document_type=${encodeURIComponent(currentDocumentType)}`

            );

            const data = await response.json();

            renderTable(

                data.records

            );

            renderPagination(

                data

            );

            renderSummary(

                data

            );

        }

        async function loadFilterOptions() {

            const response = await fetch(

                "/publications/filter-options/"

            );

            const data = await response.json();

            const yearSelect =

                document.getElementById(

                    "year-filter"

                );

            data.years.forEach(

                year => {

                    yearSelect.innerHTML +=

                        `<option value="${year}">${year}</option>`;

                }

            );

            const typeSelect =

                document.getElementById(

                    "document-type-filter"

                );

            data.document_types.forEach(

                type => {

                    typeSelect.innerHTML +=

                        `<option value="${type}">${type}</option>`;

                }

            );

        }

        // Tìm kiếm
        document

            .getElementById(

                "publication-search"

            )

            .addEventListener(

                "keyup",

                function () {

                    clearTimeout(

                        searchTimeout

                    );

                    searchTimeout = setTimeout(

                        () => {

                            currentKeyword =

                                this.value;

                            currentPage = 1;

                            loadPublications();

                        },

                        500

                    );

                }

            );

        // Thay đổi kích thước trang
        document

            .getElementById(

                "page-size"

            )

            .addEventListener(

                "change",

                function () {

                    currentPageSize =

                        parseInt(

                            this.value

                        );

                    currentPage = 1;

                    loadPublications();

                }

            );

        // GotoPage
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

                    loadPublications();

                }

            }

        );

        // Lọc theo năm
        document

            .getElementById(

                "year-filter"

            )

            .addEventListener(

                "change",

                function () {

                    currentYear =

                        this.value;

                    currentPage = 1;

                    loadPublications();

                }

            );

        // Lọc theo thể loại
        document

            .getElementById(

                "document-type-filter"

            )

            .addEventListener(

                "change",

                function () {

                    currentDocumentType =

                        this.value;

                    currentPage = 1;

                    loadPublications();

                }

            );

        await loadFilterOptions();
        await loadPublications();
    });