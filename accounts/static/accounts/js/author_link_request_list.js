document.addEventListener(

    "DOMContentLoaded",

    () => {

        const selectedAll = document.getElementById("selectAllRequests");
        if (selectedAll){

            selectedAll.addEventListener(

                "change",

                function () {

                    document

                        .querySelectorAll(

                            ".request-checkbox"

                        )

                        .forEach(

                            checkbox => {

                                checkbox.checked =

                                    this.checked;

                            }

                        );

                }

            )};

        document

        .querySelectorAll(

        ".evidence-btn"

        )

        .forEach(

            button => {

                button.addEventListener(

                    "click",

                    async function () {

                        const requestId =

                            this.dataset.requestId;

                        const response = await fetch(

                            `/accounts/admin/author-link-request/${requestId}/evidence/`

                        );

                        const data =

                            await response.json();

                        let html = `

                        <table class="table table-bordered">

                            <thead>

                                <tr>

                                    <th>Tiêu đề CBKH</th>

                                    <th>Tác giả</th>

                                    <th>Năm công bố</th>

                                    <th>DOI</th>

                                </tr>

                            </thead>

                            <tbody>

                    `;

                        data.publications.forEach(

                            publication => {
                                const authorsHtml = publication.authors.replace(data.target_author, `<span class="text-success fw-bold">${data.target_author}</span>`);
                                html += `

                                <tr>

                                    <td>

                                        ${publication.title}

                                    </td>

                                    <td>

                                        ${authorsHtml}

                                    </td>

                                    <td>

                                        ${publication.year || ""}

                                    </td>

                                    <td>

                                        ${publication.doi || ""}

                                    </td>

                                </tr>

                            `;

                            }

                        );

                        html += `

                            </tbody>

                        </table>

                    `;

                        document.getElementById(

                            "evidenceContainer"

                        ).innerHTML = `

                        <div class="alert alert-info">

                            Tác giả cần xác minh:

                            <strong>

                                ${data.target_author}

                            </strong>

                        </div>

                        ${html}

                        `;

                        const modal =

                            new bootstrap.Modal(

                                document.getElementById(

                                    "evidenceModal"

                                )

                            );

                        modal.show();

                    }

                );

            }

        );

        function getCSRFToken() {

            return document

                .querySelector(

                    '[name=csrfmiddlewaretoken]'

                )

                .value;

        }

        document

            .querySelectorAll(

                ".approve-btn"

            )

            .forEach(

                button => {

                    button.addEventListener(

                        "click",

                        async function () {

                            const requestId =

                                this.dataset.requestId;

                            if (

                                !confirm(

                                    "Chấp nhận yêu cầu này?"

                                )

                            ) {

                                return;

                            }

                            const response =

                                await fetch(

                                    `/accounts/admin/author-link-request/${requestId}/approve/`,

                                    {

                                        method: "POST",

                                        headers: {

                                            "X-CSRFToken":

                                                getCSRFToken()

                                        }

                                    }

                                );

                            const data =

                                await response.json();

                            if (

                                data.success

                            ) {

                                location.reload();

                            }

                        }

                    );

                }

            );


        document

            .querySelectorAll(

                ".reject-btn"

            )

            .forEach(

                button => {

                    button.addEventListener(

                        "click",

                        async function () {

                            const requestId =

                                this.dataset.requestId;

                            if (

                                !confirm(

                                    "Từ chối yêu cầu này?"

                                )

                            ) {

                                return;

                            }

                            const response =

                                await fetch(

                                    `/accounts/admin/author-link-request/${requestId}/reject/`,

                                    {

                                        method: "POST",

                                        headers: {

                                            "X-CSRFToken":

                                                getCSRFToken()

                                        }

                                    }

                                );

                            const data =

                                await response.json();

                            if (

                                data.success

                            ) {

                                location.reload();

                            }

                        }

                    );

                }

            );


});