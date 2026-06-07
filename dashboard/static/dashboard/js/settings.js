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


        const applyBtn = document.getElementById("apply-config-btn");
        if (applyBtn)
        {

            applyBtn.addEventListener(

                "click",

                async function () {

                    if (

                        !confirm(

                            "Áp dụng cấu hình mới?"

                        )

                    ) {

                        return;

                    }

                    const response =

                        await fetch(

                            "/settings/apply-config/",

                            {

                                method: "POST",

                                headers: {

                                    "X-CSRFToken":

                                        getCSRFToken()

                                }

                            }

                        );

                    const result =

                        await response.json();

                    if (

                        result.success

                    ) {

                        location.reload();
                        alert(

                            `Đã cập nhật ${result.updated}/${result.total} CBKH`

                        );

                    }

                }

        )};
        
        const histogram_labels = JSON.parse(

            document.getElementById(
                "histogram_labels"
            ).textContent

        );

        const histogram_values = JSON.parse(

            document.getElementById(
                "histogram_values"
            ).textContent

        );


        createBarChart({

            canvasId: "citationHistogramChartSetting",
            labels: histogram_labels,
            values: histogram_values,
            label: "Số CBKH",
            horizontal: false,
            custom_color: DASHBOARD_COLORS[0]
        });


        document

            .getElementById(

                "add-citation-group-row"

            )

            .addEventListener(

                "click",

                function () {

                    const tbody =

                        document.querySelector(

                            "#citation-group-table tbody"

                        );

                    tbody.insertAdjacentHTML(

                        "beforeend",

                        `
            <tr>
                <td> </td>
                <td> </td>

                <td>

                    <input
                        type="number"
                        class="form-control citation-min"
                    >

                </td>

                <td>

                    <input
                        type="number"
                        class="form-control citation-max"
                    >

                </td>

                <td>

                    <button
                        class="btn btn-danger btn-sm delete-row"
                    >

                        <i class="bi bi-trash"></i>

                    </button>

                </td>

            </tr>
            `

                    );

                }

            );

        document

            .addEventListener(

                "click",

                function (e) {

                    if (

                        e.target.closest(

                            ".delete-row"

                        )

                    ) {

                        e.target

                            .closest("tr")

                            .remove();

                    }

                }

            );

        document

            .getElementById(
                "save-citation-group-btn"
            )

            .addEventListener(

                "click",

                async function () {

                    const rows = document.querySelectorAll(

                        "#citation-group-table tbody tr"

                    );

                    const groups = [];

                    rows.forEach(row => {

                        const minInput = row.querySelector(

                            ".citation-min"

                        );

                        const maxInput = row.querySelector(

                            ".citation-max"

                        );

                        const minValue = parseInt(

                            minInput.value

                        );

                        const maxValue = maxInput.value.trim()

                            ? parseInt(

                                maxInput.value

                            )

                            : null;

                        groups.push({

                            min: minValue,

                            max: maxValue

                        });

                    });
                    console.log(groups);

                    const response = await fetch(

                        "/settings/citation-group/save/",

                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json",

                                "X-CSRFToken":
                                    getCSRFToken()

                            },

                            body: JSON.stringify({

                                groups: groups

                            })

                        }

                    );

                    const result = await response.json();
                    if (

                        result.success

                    ) {

                        location.reload();

                    }
                    else {
                        alert(result.message);

                    }

                }

            );



    }
);