document.addEventListener(

    "DOMContentLoaded",

    () => {

        // ============================================
        // ELEMENTS
        // ============================================

        const transformBtn = document.getElementById(
            "transform-btn"
        );

        const progressSection = document.getElementById(
            "progress-section"
        );

        const progressBar = document.getElementById(
            "transform-progress"
        );

        const logBox = document.getElementById(
            "transform-log"
        );

        const forceRebuild = document.getElementById(
            "forceRebuild"
        );

        const totalRawEl = document.getElementById(
        "total-raw"
        );

        const processedRawEl = document.getElementById(
        "processed-raw"
        );

        const pendingRawEl = document.getElementById(
        "pending-raw"
        );

        const totalFactEl = document.getElementById(
        "total-fact"
        );

        const insertedEl = document.getElementById(
            "inserted-count"
        );

        const updatedEl = document.getElementById(
            "updated-count"
        );




        // ============================================
        // NO BUTTON
        // ============================================

        if (!transformBtn) return;

        // ============================================
        // APPEND LOG
        // ============================================

        function appendLog(message) {

            const now = new Date();

            const timestamp = now.toLocaleTimeString();

            logBox.innerHTML +=

                `[${ timestamp }] ${ message } \n`;

            logBox.scrollTop = logBox.scrollHeight;

        }

        // ============================================
        // UPDATE PROGRESS
        // ============================================

        function updateProgress(percent) {

            progressBar.style.width =
                `${ percent }% `;

            progressBar.innerText =
                `${ percent }% `;

        }

        // ============================================
        // SIMULATE STEPS
        // ============================================

        async function simulateSteps() {

            const steps = [

                {
                    percent: 10,
                    message:
                        "Đang tải dữ liệu thô..."
                },

                {
                    percent: 20,
                    message:
                        "Đang tính toán nhóm trích dẫn..."
                },

                {
                    percent: 30,
                    message:
                        "Đang thực hiện việc phân nhóm chuyên ngành..."
                },

                {
                    percent: 40,
                    message:
                        "Đang tính toán chỉ số hợp tác nghiên cứu..."
                },

                {
                    percent: 55,
                    message:
                        "Đang xây dựng bảng dữ liệu thông tin CBKH đã được chuẩn hóa..."
                },
                {
                    percent: 65,
                    message:
                        "Đang xây dựng bảng dữ liệu thông tin quốc gia..."
                },
                {
                    percent: 75,
                    message:
                        "Đang xây dựng bảng dữ liệu thông tin trường đại học..."
                },
                {
                    percent: 85,
                    message:
                        "Đang xây dựng bảng dữ liệu thông tin tác giả..."
                }

            ];

            for (const step of steps) {

                updateProgress(
                    step.percent
                );

                appendLog(
                    step.message
                );

                await new Promise(resolve =>

                    setTimeout(
                        resolve,
                        1200
                    )

                );

            }

        }

        // ============================================
        // CLICK EVENT
        // ============================================

        transformBtn.addEventListener(

            "click",

            async () => {

                // ====================================
                // INIT UI
                // ====================================

                transformBtn.disabled = true;

                progressSection.style.display =
                    "block";

                logBox.innerHTML = "";

                updateProgress(0);

                appendLog(
                    "Bắt đầu quá trình chuyển đổi, chuẩn hóa dữ liệu..."
                );

                // ====================================
                // SIMULATE ETL STEPS
                // ====================================

                await simulateSteps();

                // ====================================
                // CSRF
                // ====================================

                const csrfToken = document.querySelector(
                    "[name=csrfmiddlewaretoken]"
                ).value;

                // ====================================
                // API CALL
                // ====================================

                try {

                    const response = await fetch(

                        "/api/transform/",

                        {

                            method: "POST",

                            headers: {

                                "X-CSRFToken":
                                    csrfToken,

                                "Content-Type":
                                    "application/x-www-form-urlencoded"

                            },

                            body: new URLSearchParams({

                                force_rebuild:
                                    forceRebuild.checked

                            })

                        }

                    );

                    const data =
                        await response.json();

                    // ================================
                    // SUCCESS
                    // ================================

                    if (data.success) {

                        updateProgress(100);

                        appendLog(
                            "Quá trình chuẩn hóa, chuyển đổi dữ liệu hoàn thành."
                        );

                        appendLog(

                            `Thực hiện chuẩn hóa ${ data.processed_count } bản ghi.`

                        );

                        // ========================================
                        // UPDATE DASHBOARD STATS
                        // ========================================

                        if (

                            totalRawEl &&
                            processedRawEl &&
                            pendingRawEl &&
                            totalFactEl

                        ) {

                            // ==========================================
                            // REFRESH DASHBOARD STATE
                            // ==========================================

                            totalRawEl.innerText = (
                                data.total_raw
                            );

                            processedRawEl.innerText = (
                                data.processed_raw
                            );

                            pendingRawEl.innerText = (
                                data.pending_raw
                            );

                            totalFactEl.innerText = (
                                data.total_fact
                            );

                        }

                        // ==============================================
                        // UPDATE INSERTED / UPDATED
                        // ==============================================

                        if (insertedEl) {

                            insertedEl.innerText = (
                                data.inserted_count
                            );

                        }

                        if (updatedEl) {

                            updatedEl.innerText = (
                                data.updated_count
                            );

                        }

                    }


                    // ================================
                    // FAILED
                    // ================================

                    else {

                        appendLog(
                            "Transformation failed."
                        );

                        appendLog(
                            data.message
                        );

                    }

                }

                catch (error) {

                    appendLog(
                        "Unexpected error occurred."
                    );

                    appendLog(
                        error
                    );

                }

                progressBar.classList.remove("progress-bar-animated"); 
                progressBar.classList.remove("progress-bar-striped"); 
                progressBar.classList.add("bg-success");
                // ====================================
                // FINISH UI
                // ====================================

                setTimeout(() => {

                    const progressWrapper = document.querySelector(
                        ".progress"
                    );

                    if (progressWrapper) {

                        progressWrapper.style.display =
                            "none";

                    }

                }, 1000);

                // ====================================
                // ENABLE BUTTON
                // ====================================

                transformBtn.disabled = false;


            }

        );

    }

);