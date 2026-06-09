document.addEventListener(

    "DOMContentLoaded",

    () => {
        const authorSelect = new TomSelect(

        "#authorSelect",

        {

            valueField: "id",

        labelField: "text",

        searchField: "text",

        load(query, callback) {

            fetch(

                `/accounts/api/authors/search/?q=${query}`

            )

                .then(

                    r => r.json()

                )

                .then(

                    data => callback(

                        data.results

                    )

                );

            }

        }

        );


        const publicationSelect = new TomSelect(

                "#publicationSelect",

                {

                    valueField: "id",

                labelField: "text",

                searchField: [

                "title",

                "authors",

                "text"

                ],

                plugins: [

                "remove_button"

                ],

                maxItems: 3,

                load(query, callback) {

                if (!query.length) {

                    return callback();

                }

                fetch(

                `/accounts/api/publications/search/?q=${encodeURIComponent(query)}`

                )

                .then(

                    response => response.json()

                )

                .then(

                    data => callback(

                data.results

                )

                )

                .catch(

                    () => callback()

                );

            },

                render: {

                    option: function(item, escape) {

                    return `

                <div class="py-2">

                    <div class="fw-semibold">

                        ${escape(item.title)}

                    </div>

                    <div class="small text-muted">

                        ${escape(item.authors)}

                    </div>

                    <div class="small text-secondary">

                        Year: ${escape(String(item.year || ""))}

                    </div>

                </div>

                `;
                },

                item: function(item, escape) {

                    return `

                <div>

                    ${escape(item.title)}

                </div>

                    `;
                }

            }

        });

        function getCSRFToken() {

            return document

                .querySelector(

                    'meta[name="csrf-token"]'

                )

                .getAttribute(

                    'content'

                );

        }


        document

            .getElementById(

                "submitLinkRequestBtn"

            )

            .addEventListener(

                "click",

                async function () {

                    const authorId =

                        authorSelect.getValue();

                    const publicationIds =

                        publicationSelect.getValue();

                    if (!authorId) {

                        alert(

                            "Vui lòng chọn tác giả."

                        );

                        return;
                    }

                    if (

                        !publicationIds ||

                        publicationIds.length === 0

                    ) {

                        alert(

                            "Vui lòng chọn ít nhất một công bố minh chứng."

                        );

                        return;
                    }

                    try {

                        const response = await fetch(

                            "/accounts/api/author-link/create/",

                            {

                                method: "POST",

                                headers: {

                                    "Content-Type":

                                        "application/json",

                                    "X-CSRFToken":

                                        getCSRFToken()

                                },

                                body: JSON.stringify({

                                    author_id:

                                        authorId,

                                    publication_ids:

                                        publicationIds

                                })

                            }

                        );

                        const data =

                            await response.json();

                        if (

                            data.success

                        ) {

                            alert(

                                "Gửi yêu cầu thành công."

                            );

                            location.reload();

                        }

                        else {

                            alert(

                                data.message ||

                                "Có lỗi xảy ra."

                            );

                        }

                    }

                    catch (error) {

                        console.error(

                            error

                        );

                        alert(

                            "Không thể gửi yêu cầu."

                        );

                    }

                }

            );

        document

            .querySelectorAll(

                ".cancel-request-btn"

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

                                    "Bạn có chắc muốn hủy yêu cầu này?"

                                )

                            ) {

                                return;

                            }

                            const response =

                                await fetch(

                                    `/accounts/author-link-request/${requestId}/cancel/`,

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

                            else {

                                alert(

                                    data.message

                                );

                            }

                        }

                    );

                }

            );

    }
);