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