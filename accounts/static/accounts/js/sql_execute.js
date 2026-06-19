document.addEventListener(

    "DOMContentLoaded",

    function () {

        const executeBtn = document.getElementById(
            "executeSqlBtn"
        );

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

        const input_sql = document.getElementById("sqlText");
        input_sql.addEventListener("input", function()
        {
            document.getElementById(
                "sqlResult"
            ).innerHTML = '';
        });

        executeBtn.addEventListener(

            "click",

            async function () {

                const sql = document
                    .getElementById(
                        "sqlText"
                    )
                    .value
                    .trim();

                const confirmed = document
                    .getElementById(
                        "confirmSql"
                    )
                    .checked;

                if (!confirmed) {

                    showToast("Vui lòng xác nhận trước khi thực thi", 'error');

                    return;
                }

                if (!sql) {
                    showToast("SQL không được để trống.", 'error');

                    return;
                }

                const formData = new FormData();

                formData.append(
                    "sql",
                    sql
                );

                try {

                    const response = await fetch(

                        "/accounts/admin/sql-execute/run/",

                        {
                            method: "POST",

                            headers: {
                                "X-CSRFToken":
                                    getCSRFToken()
                            },

                            body: formData
                        }

                    );

                    const data =
                        await response.json();

                    const resultDiv =
                        document.getElementById(
                            "sqlResult"
                        );

                    if (data.success) {

                        resultDiv.innerHTML = `

                            <div class="alert alert-success">

                                ${data.message}

                            </div>

                        `;
                        //document.getElementById("sqlText").value = '';
                        document.getElementById("confirmSql").checked = false;
                    }
                    else {

                        resultDiv.innerHTML = `

                            <div class="alert alert-danger">

                                ${data.message}

                            </div>

                        `;
                    }

                }
                catch (error) {

                    document.getElementById(
                        "sqlResult"
                    ).innerHTML = `

                        <div class="alert alert-danger">

                            Không thể kết nối tới server

                        </div>

                    `;
                    showToast('Không thể kết nối tới server', 'error');

                    console.error(error);

                }

            }

        )

    }

)