document.addEventListener(

    "DOMContentLoaded",

    function () {

        let currentPage = 1;

        async function loadLogs() {

            page = currentPage;

            const keyword =
                document.getElementById(
                    "keyword"
                ).value;

            const startDate =
                document.getElementById(
                    "startDate"
                ).value;

            const endDate =
                document.getElementById(
                    "endDate"
                ).value;

            const pageSize =
                document.getElementById(
                    "pageSize"
                ).value;
            const response =
                await fetch(

                    `/accounts/admin/login-logs/api/?page=${page}&page_size=${pageSize}&keyword=${encodeURIComponent(keyword)}&start_date=${startDate}&end_date=${endDate}`

                );

            const data =
                await response.json();
            const tbody =
                document.getElementById(
                    "loginLogTableBody"
                );

            tbody.innerHTML = "";
            data.records.forEach(
                log => {

                    tbody.innerHTML += `

                <tr>

                    <td>${log.username}</td>

                    <td>${log.fullname}</td>

                    <td>${log.login_time}</td>

                    <td>

                        ${log.logout_time
                            ?
                            log.logout_time
                            :
                            '<span class="badge bg-success">Online</span>'
                        }

                    </td>

                    <td>${log.ip_address}</td>

                    <td>

                        ${log.user_agent}

                    </td>
                    <td class="text-end">
                        <button class="btn btn-outline-danger btn-sm delete-log-btn" data-id="${log.id }">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>

                </tr>

            `

                }
            )
            renderSummary(data);
            renderPagination(data);
        }

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

                    currentPage = parseInt(

                        e.target.dataset.page

                    );

                    loadLogs();

                }

            }

        );

        document
            .getElementById(
                "keyword"
            )
            .addEventListener(

                "keyup",

                () => loadLogs()

            );
        
        document
            .getElementById(
                "startDate"
            )
            .addEventListener(

                "change",

                () => loadLogs()

            );
        document
            .getElementById(
                "endDate"
            )
            .addEventListener(

                "change",

                () => loadLogs()

            );
        document
            .getElementById(
                "pageSize"
            )
            .addEventListener(

                "change",

                () => loadLogs()

            );
        
        loadLogs();



        function getCSRFToken() {

            const cookie = document.cookie
                .split("; ")
                .find(
                    row =>
                        row.startsWith(
                            "csrftoken="
                        )
                );

            return cookie
                ? cookie.split("=")[1]
                : "";

        }

        
        document.addEventListener(

            "click",

            async function (e) {

                const btn = e.target.closest(
                    ".delete-log-btn"
                )

                if (!btn) {

                    return

                }

                if (

                    !confirm(
                        "Xóa log này?"
                    )

                ) {

                    return

                }

                const logId =
                    btn.dataset.id

                try {

                    const response =
                        await fetch(

                            `/accounts/admin/login-logs/${logId}/delete/`,

                            {
                                method: "POST",

                                headers: {

                                    "X-CSRFToken":
                                        getCSRFToken()

                                }

                            }

                        )

                    const data =
                        await response.json()

                    if (data.success) {

                        loadLogs(currentPage)

                    }

                }

                catch (error) {

                    console.error(error)

                }

            }

        )


        const clearBtn =
            document.getElementById(
                "clearLogsBtn"
            )

        if (clearBtn) {

            clearBtn.addEventListener(

                "click",

                async function () {

                    if (

                        !confirm(
                            "Xóa toàn bộ log?"
                        )

                    ) {

                        return

                    }

                    const response =
                        await fetch(

                            "/accounts/admin/login-logs/clear/",

                            {
                                method: "POST",

                                headers: {
                                    "X-CSRFToken":
                                        getCSRFToken()
                                }
                            }

                        )

                    const data =
                        await response.json()

                    if (
                        data.success
                    ) {

                        location.reload()

                    }

                }

            )

        }

    }

)