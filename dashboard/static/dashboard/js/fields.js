document.addEventListener(

    "DOMContentLoaded",

    () => {

        // =====================================
        // DATA
        // =====================================
        Chart.register(
            ChartDataLabels
        );

        const fieldLabels = JSON.parse(

            document.getElementById(
                "field-labels"
            ).textContent

        );

        const fieldValues = JSON.parse(

            document.getElementById(
                "field-values"
            ).textContent

        );

        const stackedLabels = JSON.parse(

            document.getElementById(
                "stacked-labels"
            ).textContent

        );

        const stackedDatasets = JSON.parse(

            document.getElementById(
                "stacked-datasets"
            ).textContent

        );

        const articleLabels = JSON.parse(

            document.getElementById(
                "article-labels"
            ).textContent

        );

        const articleValues = JSON.parse(

            document.getElementById(
                "article-values"
            ).textContent

        );

        const hindexLabels = JSON.parse(

            document.getElementById(
                "hindex-labels"
            ).textContent

        );

        const hindexValues = JSON.parse(

            document.getElementById(
                "hindex-values"
            ).textContent

        );


        // =====================================
        // CHART
        // =====================================

        const ctx = document.getElementById(
            "fieldPublicationChart"
        );

        createBarChart({

            canvasId: "fieldPublicationChart",
            labels: fieldLabels,
            values: fieldValues,
            label: "Số CBKH",
            horizontal: true
        });

        // =====================================
        // PIE CHART
        // =====================================

        createPieChart({

            canvasId: "fieldPieChart",
            labels: fieldLabels,
            values: fieldValues,
            minLabelPercentage:5,
            doughnut: false

        });

        // =====================================
        // STACKED DOCUMENT TYPE CHART
        // =====================================
        createStackedBarChart({

            canvasId: "documentTypeChart",
            labels: stackedLabels,
            datasets: stackedDatasets
        });

        // =====================================
        // ARTICLE PERCENTAGE CHART
        // =====================================

        createBarChart({

            canvasId: "articlePercentageChart",
            labels: articleLabels,
            values: articleValues,
            label: "% Article",
            horizontal: true,
            percentage:true,
            display_y_axis:false,
            display_legend:false
        });

        // =====================================
        // H-INDEX CHART
        // =====================================

        createBarChart({

            canvasId: "fieldHIndexChart",
            labels: hindexLabels,
            values: hindexValues,
            label: "H-index",
            horizontal: true
        });

    }

);