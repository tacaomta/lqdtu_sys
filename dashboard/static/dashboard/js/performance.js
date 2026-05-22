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


            // =====================================
            // UPDATE LABEL
            // =====================================

            document.getElementById(

                "publicationThresholdLabel"

            ).innerText = publicationThreshold;


            // =====================================
            // FILTER AUTHORS
            // =====================================

            const authorsWithPublication =

                authorsMetrics.filter(

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

        updateAuthorPerformanceKPIs();
        

    }

);