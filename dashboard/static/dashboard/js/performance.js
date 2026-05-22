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

        

    }

);