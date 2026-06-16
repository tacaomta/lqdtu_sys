document.addEventListener(

    "DOMContentLoaded",

    () => {

        function getCSRFToken() {

            let cookieValue = null;

            const cookies = document.cookie.split(";");

            for (let cookie of cookies) {

                cookie = cookie.trim();

                if (

                    cookie.startsWith(

                        "csrftoken="

                    )

                ) {

                    cookieValue = decodeURIComponent(

                        cookie.substring(

                            "csrftoken=".length

                        )

                    );

                    break;

                }

            }

            return cookieValue;

        }


        document.addEventListener(

            "click",

            async function (e) {

                const btn =

                    e.target.closest(

                        ".toggle-user-btn"

                    );

                if (!btn) {

                    return;

                }

                const userId = btn.dataset.userId;

                const confirmed = confirm(

                    "Xác nhận thay đổi trạng thái tài khoản?"

                );

                if (!confirmed) {

                    return;

                }

                try {

                    const response = await fetch(

                        `/accounts/admin/users/${userId}/toggle-status/`,

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

                    if (!data.success) {

                        alert(

                            data.message

                        );

                        return;

                    }

                    const badge =

                        document.getElementById(

                            `status-${userId}`

                        );

                    if (data.is_active) {

                        badge.innerHTML =

                            `<span class="badge bg-success">

                        Active

                    </span>`;

                        btn.innerText =

                            "Block";

                        btn.classList.remove(

                            "btn-outline-success"

                        );

                        btn.classList.add(

                            "btn-outline-danger"

                        );

                    } else {

                        badge.innerHTML =

                            `<span class="badge bg-danger">

                        Blocked

                    </span>`;

                        btn.innerText =

                            "Unblock";

                        btn.classList.remove(

                            "btn-outline-danger"

                        );

                        btn.classList.add(

                            "btn-outline-success"

                        );

                    }

                }

                catch (error) {

                    console.error(

                        error

                    );

                }

            }

        );


    }
);