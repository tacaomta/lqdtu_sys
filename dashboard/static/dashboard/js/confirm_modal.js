function showConfirm(

    message

) {

    return new Promise(

        (resolve) => {

            const modalEl =

                document.getElementById(
                    "confirmModal"
                )

            const modal =

                new bootstrap.Modal(
                    modalEl
                )

            document.getElementById(
                "confirmMessage"
            ).textContent = message

            const okBtn =

                document.getElementById(
                    "confirmOkBtn"
                )

            const newBtn =
                okBtn.cloneNode(true)

            okBtn.parentNode.replaceChild(
                newBtn,
                okBtn
            )

            newBtn.addEventListener(

                "click",

                function () {

                    modal.hide()

                    resolve(true)

                }

            )

            modalEl.addEventListener(

                "hidden.bs.modal",

                function handler() {

                    modalEl.removeEventListener(

                        "hidden.bs.modal",

                        handler

                    )

                    resolve(false)

                },

                { once: true }

            )

            modal.show()

        }

    )

}