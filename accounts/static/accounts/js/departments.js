document.addEventListener(

    "DOMContentLoaded",

    function () {

        function getCSRFToken() {

            return document.cookie
                .split("; ")
                .find(
                    row =>
                        row.startsWith(
                            "csrftoken="
                        )
                )
                ?.split("=")[1]

        }

        const saveBtn =
        document.getElementById(
        "saveDepartmentBtn"
        );

        const createUrl = saveBtn.dataset.url;


        document
            .querySelectorAll(
                ".edit-department-btn"
            )
            .forEach(btn => {

                btn.addEventListener(
                    "click",
                    function () {

                        document.getElementById(
                            "departmentId"
                        ).value = this.dataset.id

                        document.getElementById(
                            "departmentName"
                        ).value = this.dataset.name

                        document.querySelector(
                            "#createDepartmentModal .modal-title"
                        ).innerText =
                            "Cập nhật Department"

                        const modal =
                            new bootstrap.Modal(
                                document.getElementById(
                                    "createDepartmentModal"
                                )
                            )

                        modal.show()

                    }
                )

            });

        saveBtn
            .addEventListener(
                "click",
                async function () {

                    const departmentId =
                        document.getElementById(
                            "departmentId"
                        ).value;

                    const name =
                        document.getElementById(
                            "departmentName"
                        ).value.trim();

                    const formData =
                        new FormData();

                    formData.append(
                        "name",
                        name
                    );

                    let url="";

                    if (departmentId) {

                        url =
                            `/accounts/admin/departments/${departmentId}/update/`;

                    } else {

                        url = createUrl;

                    }

                    const response =
                        await fetch(
                            url,
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

                    if (!data.success) {
                        showToast(data.message, 'error');

                        return;

                    }

                    location.reload();

                }
            );

        document
            .getElementById(
                "btn-create-department"
            )
            .addEventListener(
                "click",
                function () {

                    document.getElementById(
                        "departmentId"
                    ).value = ""

                    document.getElementById(
                        "departmentName"
                    ).value = ""

                    document.querySelector(
                        "#createDepartmentModal .modal-title"
                    ).innerText =
                        "Tạo Department"

                }
            );

        document
            .querySelectorAll(
                ".delete-department-btn"
            )
            .forEach(btn => {

                btn.addEventListener(
                    "click",
                    async function () {

                        const departmentId = this.dataset.id;

                        const departmentName = this.dataset.name;

                        const confirmed = await showConfirm(`Bạn có chắc muốn xóa Department "${departmentName}"?`);

                        if (!confirmed) {
                            return;
                        }

                        const response =
                            await fetch(
                                `/accounts/admin/departments/${departmentId}/delete/`,
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
                            showToast(data.message, 'error');
                            return;

                        }
                        else{
                            showToast("Xóa department thành công", 'success');
                        }

                        location.reload();

                    }
                )

            });
    }

)