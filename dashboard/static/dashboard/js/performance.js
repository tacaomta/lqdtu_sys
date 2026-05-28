document.addEventListener(

    "DOMContentLoaded",

    () => {

        // =====================================
        // REGISTER
        // =====================================

        Chart.register(
            ChartDataLabels
        );

        const authorsMetrics = JSON.parse(

            document.getElementById(
                "authors_with_N_publications"
            ).textContent

        );

        function updateAuthorPerformanceKPIs() {

            // =====================================
            // GET THRESHOLD
            // =====================================

            const publicationThreshold = parseInt(

                document.getElementById(

                    "publicationThreshold"

                ).value

            );

            const lqdtuOnly = document.getElementById("publicationLQDTUOnly").checked;


            // =====================================
            // UPDATE LABEL
            // =====================================

            document.getElementById(

                "publicationThresholdLabel"

            ).innerText = lqdtuOnly ? `${publicationThreshold} (Chỉ tính LQDTU)` : publicationThreshold;

            let filteredAuthors = authorsMetrics;

            if (lqdtuOnly) { filteredAuthors = filteredAuthors.filter(x => x.is_lqdtu); }


            // =====================================
            // FILTER AUTHORS
            // =====================================

            const authorsWithPublication =

                filteredAuthors.filter(

                    x =>

                        x.publication_count

                        >=

                        publicationThreshold

                ).length;


            // =====================================
            // UPDATE CARD
            // =====================================

            document.getElementById(

                "authorsWithPublicationValue"

            ).innerText =

                authorsWithPublication;

        }


        // =========================================
        // SLIDER EVENT
        // =========================================

        document.getElementById(

            "publicationThreshold"

        ).addEventListener(

            "input",

            updateAuthorPerformanceKPIs

        );

        function updateHindexThresholdKPI() {
            const hindexThreshold = parseInt(document.getElementById("hindexThreshold").value);

            const lqdtuOnly = document.getElementById("hindexLQDTUOnly").checked;

            document.getElementById("hindexThresholdLabel").innerText = lqdtuOnly ? `${hindexThreshold} (Chỉ tính LQDTU)` : hindexThreshold;; 

            let filteredAuthors = authorsMetrics;

            if (lqdtuOnly) { filteredAuthors = filteredAuthors.filter(x => x.is_lqdtu); }

            const authorsWithHindex = filteredAuthors.filter( x => x.h_index >= hindexThreshold ).length; 

            document.getElementById("authorsWithHindexValue").innerText = authorsWithHindex;; 
        }

        


        // =========================================
        // EVENTS
        // =========================================

        document.getElementById(

            "publicationThreshold"

        ).addEventListener(

            "input",

            updateAuthorPerformanceKPIs

        );


        document.getElementById(

            "hindexThreshold"

        ).addEventListener(

            "input",

            updateHindexThresholdKPI

        );

        document.getElementById(

            "publicationLQDTUOnly"

        ).addEventListener(

            "input",

            updateAuthorPerformanceKPIs

        );

        document.getElementById(

            "hindexLQDTUOnly"

        ).addEventListener(

            "input",

            updateHindexThresholdKPI

        );


        // =========================================
        // INITIAL RENDER
        // =========================================

        updateAuthorPerformanceKPIs();
        updateHindexThresholdKPI();

        // =========================================
        // DATA
        // ========================================


        const publicationBins = JSON.parse(

            document.getElementById(
                "publication_bins"
            ).textContent

        );

        const publicationBinCounts = JSON.parse(

            document.getElementById(
                "publication_bin_counts"
            ).textContent

        );

        const citationBins = JSON.parse(

            document.getElementById(
                "citation_bins"
            ).textContent

        );

        const citationBinCounts = JSON.parse(

            document.getElementById(
                "citation_bin_counts"
            ).textContent

        );
        // =========================================
        // PUBLICATION HISTOGRAM
        // =========================================

        createBarChart({

            canvasId: "publicationHistogramChart",
            labels: publicationBins,
            values: publicationBinCounts,
            label:"Số tác giả",
            horizontal:false,
            custom_color: DASHBOARD_COLORS[0]
        });

        createBarChart({

            canvasId: "citationHistogramChart",
            labels: citationBins,
            values: citationBinCounts,
            label: "Số tác giả",
            horizontal: false,
            custom_color: DASHBOARD_COLORS[0]
        });

        // =========================================
        // DATA
        // =========================================
        const fieldAuthorTables = JSON.parse(

            document.getElementById(
                "field_author_tables"
            ).textContent

        );

        // =========================================
        // RENDER TABLE
        // =========================================

        function renderTable({

            tableId,
            data,
            metricKey,
            topN

        }) {

            const tbody = document.getElementById(

                tableId

            );


            tbody.innerHTML = "";


            data.slice(0, topN).forEach(

                (row, index) => {

                    tbody.innerHTML += `

                    <tr>

                            <td>

                                ${index + 1}

                            </td>

                            <td>

                                ${row.author_name}

                            </td>

                            <td>

                                ${row[metricKey]}

                            </td>

                        </tr>

                    `;

                }

            );

        }

        function updateRankingTables() {

            const topN = parseInt(

                document.getElementById(

                    "topNSlider"

                ).value

            );

            document.getElementById(

                "topNLabel"

            ).innerText = topN;


            const fieldGroup =

                document.getElementById(

                    "fieldGroupSelect"

                ).value;


            const tables =

                fieldAuthorTables[fieldGroup];


            renderTable({

                tableId:
                    "publicationTable",

                data:
                    tables.publication,

                metricKey:
                    "publication_count",

                topN

            });


            renderTable({

                tableId:
                    "citationTable",

                data:
                    tables.citation,

                metricKey:
                    "citation_count",

                topN

            });


            renderTable({

                tableId:
                    "hindexTable",

                data:
                    tables.hindex,

                metricKey:
                    "h_index",

                topN

            });

        }

        document.getElementById(

            "topNSlider"

        ).addEventListener(

            "input",

            updateRankingTables

        );


        document.getElementById(

            "fieldGroupSelect"

        ).addEventListener(

            "change",

            updateRankingTables

        );

        updateRankingTables();

    }

);