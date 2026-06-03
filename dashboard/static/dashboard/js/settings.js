const SUPPORT_SUBFIELD_GROUPS = [

    "Electrical and Electronic Engineering"

];

document.addEventListener(

    "DOMContentLoaded",

    () => {
        document

            .querySelectorAll(

                ".edit-field-group-btn"

            )

            .forEach(btn => {

                btn.addEventListener(

                    "click",

                    async function () {

                        const groupName =

                            this.dataset.group;
                        
                        if (

                            SUPPORT_SUBFIELD_GROUPS.includes(
                                groupName
                            )

                        ) {

                            document.getElementById("subfieldContainer").classList.remove("d-none");

                        }
                        else {

                            document.getElementById("subfieldContainer").classList.add("d-none");

                        }

                        const response =

                            await fetch(

                                `/settings/field-group/detail/${encodeURIComponent(groupName)}/`

                            );

                        const data =

                            await response.json();

                        document

                            .getElementById(
                                "groupName"
                            )

                            .value =

                            data.group;

                        document

                            .getElementById(
                                "fieldGroupModalTitle"
                            )

                            .innerText =

                            data.group;

                        buildTomSelect(

                            "fieldSelect",

                            data.all_fields,

                            data.fields

                        );

                        buildTomSelect(

                            "subfieldSelect",

                            data.all_subfields,

                            data.subfields

                        );

                        const modal =

                            new bootstrap.Modal(

                                document.getElementById(

                                    "fieldGroupModal"

                                )

                            );

                        modal.show();

                    }

                );

            });

        

        function buildTomSelect(

            elementId,

            options,

            selectedValues

        ) {

            const select =

                document.getElementById(

                    elementId

                );
            if (

                select.tomselect

            ) {

                select.tomselect.destroy();

            }

            select.innerHTML = "";

            options.forEach(value => {

                const option =

                    document.createElement(

                        "option"

                    );

                option.value = value;

                option.textContent = value;

                option.selected =

                    selectedValues.includes(

                        value

                    );

                select.appendChild(option);

            });

            new TomSelect(

                select,

                {

                    plugins: [

                        "remove_button"

                    ]

                }

            );

        }

        document

            .getElementById(

                "saveFieldGroupBtn"

            )

            .addEventListener(

                "click",

                async function () {

                    try {

                        const payload = {

                            group:

                                document.getElementById(

                                    "groupName"

                                ).value,

                            fields:

                                document.getElementById(

                                    "fieldSelect"

                                )

                                    .tomselect

                                    .getValue(),

                            subfields:

                                document.getElementById(

                                    "subfieldSelect"

                                )

                                    .tomselect

                                    .getValue()

                        };

                        const response =

                            await fetch(

                                "/settings/field-group/save/",

                                {

                                    method: "POST",

                                    headers: {

                                        "Content-Type":

                                            "application/json",

                                        "X-CSRFToken":

                                            getCSRFToken()

                                    },

                                    body:

                                        JSON.stringify(

                                            payload

                                        )

                                }

                            );

                        const result =

                            await response.json();

                        if (

                            result.success

                        ) {

                            location.reload();

                        }
                        else{
                            if (result.duplicates!="")
                            {
                                alert(

                                    result.message +

                                    "\n\n" +

                                    result.duplicates.join("\n")

                                );
                            }
                            else{
                                alert(result.message);
                            }
                            
                        }

                    }

                    catch (error) {

                        console.error(error);

                    }

                }

            );
        
        function getCSRFToken() {

            return document

                .querySelector(

                    'meta[name="csrf-token"]'

                )

                .getAttribute(

                    'content'

                );

        }



    }
);