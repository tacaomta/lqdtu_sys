function showToast(

    message,

    type = "info"

) {

    const container =

        document.getElementById(
            "toastContainer"
        )

    let bgClass =

        "bg-primary"

    if (type.includes("success"))
        bgClass = "bg-success"

    else if (
        type.includes("error")
    )
        bgClass = "bg-danger"

    else if (
        type.includes("warning")
    )
        bgClass = "bg-warning"

    const toastId =

        "toast-" +
        Date.now()

    const html = `

        <div

            id="${toastId}"

            class="toast align-items-center text-white ${bgClass} border-0"

            role="alert"

        >

            <div class="d-flex">

                <div class="toast-body">

                    ${message}

                </div>

                <button

                    type="button"

                    class="btn-close btn-close-white me-2 m-auto"

                    data-bs-dismiss="toast"

                ></button>

            </div>

        </div>

    `

    container.insertAdjacentHTML(

        "beforeend",

        html

    )

    const toastElement =

        document.getElementById(
            toastId
        )

    const toast =

        new bootstrap.Toast(

            toastElement,

            {
                delay: 5000
            }

        )

    toast.show()

    toastElement.addEventListener(

        "hidden.bs.toast",

        function () {

            toastElement.remove()

        }

    )

}