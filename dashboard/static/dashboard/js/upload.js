document.addEventListener(

    "DOMContentLoaded",

    () => {

        // =================================================
        // FORM
        // =================================================

        const form = document.getElementById(
            "upload-form"
        );

        if (!form) return;

        // =================================================
        // BUTTON
        // =================================================

        const uploadBtn = document.getElementById(
            "upload-btn"
        );

        // =================================================
        // PROGRESS UI
        // =================================================

        const progressCard = document.getElementById(
            "etl-progress-card"
        );

        const progressBar = document.getElementById(
            "etl-progress-bar"
        );

        const statusText = document.getElementById(
            "etl-status"
        );

        const summaryCard = document.getElementById("summary-card");

        const previewCard = document.getElementById("previewCard");

        const etl_log = document.getElementById("etl-log");

        const next_step = document.getElementById("next-step");

        // =================================================
        // STEPS
        // =================================================

        const stepRead = document.getElementById(
            "step-read"
        );

        const stepClean = document.getElementById(
            "step-clean"
        );

        const stepEnrich = document.getElementById(
            "step-enrich"
        );

        const stepSave = document.getElementById(
            "step-save"
        );
        const errorDiv = document.getElementById(
            "upload-error"
        );


        // =================================================
        // UPDATE PROGRESS
        // =================================================

        function updateProgress(percent) {

            progressBar.style.width =
                `${ percent }% `;

            progressBar.innerText =
                `${ percent }% `;

        }

        // =================================================
        // RESET STEPS
        // =================================================

        function resetSteps() {

            [

                stepRead,
                stepClean,
                stepEnrich,
                stepSave

            ].forEach(step => {

                step.classList.remove(
                    "active"
                );

                step.classList.remove(
                    "completed"
                );

            });

        }

        // =================================================
        // POLLING
        // =================================================

        function pollProgress(batchId) {

            const interval = setInterval(

                async () => {

                    try {

                        const response = await fetch(

                            `/api/import-progress/${batchId}/`

                        );

const data =
    await response.json();

// =====================================
// INVALID
// =====================================

if (!data.success) {

    clearInterval(interval);
    showToast(data.message, 'error');
    return;

}

// =====================================
// PERCENT
// =====================================

const percent =
    data.percent || 0;

updateProgress(percent);

// =====================================
// STATUS TEXT
// =====================================
if (data.step ==="Lấy thông tin ngành, chuyên ngành")
{
    statusText.innerHTML = `

                                <div>

                                    <strong>
                                        ${data.step}
                                    </strong>

                                </div>

                                <div class="mt-1 text-muted">

                                    ${data.current} / ${data.total}

                                </div>

                            `;
}
else
{
    statusText.innerHTML = ` <strong>${data.step}</strong> `;
}

// =====================================
// STEP MAPPING
// =====================================

resetSteps();

const stepName = (

    data.step || ""

).toLowerCase();

// =====================================
// STEP 1
// =====================================

if (

    stepName.includes("đọc") ||
    stepName.includes("Đọc") ||
    stepName.includes("read")

) {

    stepRead.classList.add(
        "active"
    );

}

// =====================================
// STEP 2
// =====================================

else if (

    stepName.includes("tiền xử lý") ||
    stepName.includes("Xử lý") ||
    stepName.includes("chuẩn hóa") ||
    stepName.includes("preprocess")

) {

    stepRead.classList.add(
        "completed"
    );

    stepClean.classList.add(
        "active"
    );

}

// =====================================
// STEP 3
// =====================================

else if (

    stepName.includes("openalex") ||
    stepName.includes("enrich") ||
    stepName.includes("field") ||
    stepName.includes("ngành") ||
    stepName.includes("chuyên ngành") ||
    stepName.includes("subfield")

) {

    stepRead.classList.add(
        "completed"
    );

    stepClean.classList.add(
        "completed"
    );

    stepEnrich.classList.add(
        "active"
    );

}

// =====================================
// STEP 4
// =====================================

else if (

    stepName.includes("Lưu") ||
    stepName.includes("save") ||
    stepName.includes("database") ||
    stepName.includes("insert")||
    data.status === "COMPLETED"

) {

    stepRead.classList.add(
        "completed"
    );

    stepClean.classList.add(
        "completed"
    );

    stepEnrich.classList.add(
        "completed"
    );

    stepSave.classList.add(
        "active"
    );

}

// =====================================
// COMPLETED
// =====================================

if (

    data.status === "COMPLETED"

) {

    clearInterval(interval);

    // ===============================
    // FINAL BAR
    // ===============================

    progressBar.style.width =
        "100%";

    progressBar.innerText =
        "100%";

    progressBar.classList.remove(
        "progress-bar-animated"
    );

    progressBar.classList.add(
        "bg-success"
    );

    // ===============================
    // STATUS
    // ===============================

    statusText.innerHTML = `

                                <strong>
                                    Upload hoàn tất
                                </strong>

                            `;

    // ===============================
    // COMPLETE ALL
    // ===============================

    [

        stepRead,
        stepClean,
        stepEnrich,
        stepSave

    ].forEach(step => {

        step.classList.remove(
            "active"
        );

        step.classList.add(
            "completed"
        );

    });

    // ===============================
    // ENABLE BUTTON
    // ===============================

    uploadBtn.disabled = false;

    uploadBtn.innerHTML = `

                                <i class="bi bi-upload"></i>

                                Tải & Xử lý

                            `;

    // ===============================
    // RELOAD PAGE
    // ===============================

    setTimeout(() => {

        const card = document.getElementById("etl-progress-card"); 
        if (card) { card.classList.add("d-none"); }

        window.location.reload();

    }, 1500);

}

                    }

                    catch (error) {

    console.error(error);

    clearInterval(interval);

    statusText.innerHTML = `

                            <span class="text-danger">

                                Không thể lấy trạng thái tiến trình.

                            </span>

                        `;

    uploadBtn.disabled = false;

    uploadBtn.innerHTML = `

                            <i class="bi bi-upload"></i>

                            Tải & Xử lý

                        `;

}

                },

1000

            );

        }

// =================================================
// SUBMIT
// =================================================

form.addEventListener(

    "submit",

    async (e) => {

        e.preventDefault();

        // =========================================
        // INIT UI
        // =========================================

        uploadBtn.disabled = true;

        uploadBtn.innerHTML = `

                    <span class="spinner-border spinner-border-sm"></span>

                    Đang xử lý...

                `;

        progressCard.classList.remove("d-none");

        if (summaryCard){
            summaryCard.classList.add("d-none");
            previewCard.classList.add("d-none");
            etl_log.classList.add("d-none");
            next_step.classList.add("d-none");
        } 

        updateProgress(0);

        statusText.innerHTML = `

                    <strong>
                        Khởi tạo upload batch...
                    </strong>

                `;

        // =========================================
        // RESET PROGRESS STYLE
        // =========================================

        progressBar.classList.remove(
            "bg-success"
        );

        progressBar.classList.add(
            "progress-bar-striped"
        );

        progressBar.classList.add(
            "progress-bar-animated"
        );

        // =========================================
        // FORM DATA
        // =========================================

        const formData =
            new FormData(form);

        try {

            const response = await fetch(

                form.action,

                {

                    method: "POST",

                    body: formData

                }

            );

            const data =
                await response.json();

            //console.log(data);

            // =====================================
            // FAILED
            // =====================================

            if (!data.success) {
                /// Có thể sửa chỗ này nếu không hiển thị lỗi đối với mỗi step upload
                if (data.message=="Lỗi định dạng file")
                {
                    document
                        .getElementById(
                            "etl-progress-card"
                        )
                        .classList.add("d-none");
                    errorDiv.innerText = "Định dạng file upload không đúng. Hệ thống chỉ hỗ trợ file csv, excel."
                    errorDiv.style.display = "block";
                    
                }

                statusText.innerHTML = `

                            <span class="text-danger">

                                ${data.message}

                            </span>

                        `;

                uploadBtn.disabled = false;

                uploadBtn.innerHTML = `

                            <i class="bi bi-upload"></i>

                            Tải & Xử lý

                        `;

                return;

            }

            // =====================================
            // START POLLING
            // =====================================

            pollProgress(
                data.batch_id
            );

        }

        catch (error) {

            console.error(error);

            statusText.innerHTML = `

                        <span class="text-danger">

                            Upload thất bại.

                        </span>

                    `;

            uploadBtn.disabled = false;

            uploadBtn.innerHTML = `

                        <i class="bi bi-upload"></i>

                        Tải & Xử lý

                    `;

        }

    }

);

    }

);