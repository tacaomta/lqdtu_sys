document.addEventListener(

    "DOMContentLoaded",

    function () {
        document.querySelectorAll(".view-batch-btn").forEach(btn => {

            btn.addEventListener("click", function () {

                document.getElementById("m_filename").textContent = this.dataset.filename;
                document.getElementById("m_source").textContent = this.dataset.source;
                document.getElementById("m_filesize").textContent = this.dataset.filesize;
                let status = '';
                if (this.dataset.status == "COMPLETED")
                {
                    status += `<span class="badge bg-success">${this.dataset.status}</span>`;
                }
                else if (this.dataset.status == "PROCESSING")
                {
                    status += `<span class="badge bg-warning text-dark">${this.dataset.status}</span>`;
                }
                else if (this.dataset.status == "FAILED")
                {
                    status += `<span class="badge bg-danger">${this.dataset.status}</span>`;
                }
                else{
                    status += `<span class="badge bg-secondary">PENDING</span>`;
                }
                document.getElementById("m_status").innerHTML = status;

                document.getElementById("m_uploaded").textContent = this.dataset.uploaded;
                document.getElementById("m_started").textContent = this.dataset.started;
                document.getElementById("m_finished").textContent = this.dataset.finished;

                document.getElementById("m_total").textContent = this.dataset.total;
                document.getElementById("m_inserted").textContent = this.dataset.inserted;
                document.getElementById("m_updated").textContent = this.dataset.updated;

                document.getElementById("m_existing_doi").textContent = this.dataset.existing;
                document.getElementById("m_new_doi").textContent = this.dataset.newdoi;
                document.getElementById("m_missing_doi").textContent = this.dataset.missingdoi;
                document.getElementById("m_duplicated").textContent = this.dataset.duplicated;
                document.getElementById("m_enriched_success").textContent = this.dataset.enrichedsuccess;
                document.getElementById("m_enriched_failed").textContent = this.dataset.enrichedfailed;

                document.getElementById("m_log").value = this.dataset.log;

            });

        });
    }
)