document.addEventListener(

    "DOMContentLoaded",

    () => {

        // =====================================
        // REGISTER
        // =====================================

        Chart.register(
            ChartDataLabels
        );

        // =====================================
        // LOAD DATA
        // =====================================

        const publicationYears = JSON.parse(

            document.getElementById(
                "publication-years"
            ).textContent

        );

        const publicationCounts = JSON.parse(

            document.getElementById(
                "publication-counts"
            ).textContent

        );

        const citationCounts = JSON.parse(

            document.getElementById(
                "citation-counts"
            ).textContent

        );

        createBarChart({

            canvasId: "publicationChart",
            labels:publicationYears,
            values:publicationCounts,
            label:"Số CBKH",
            horizontal:false

        });

        createLineChart({

            canvasId:"citationChart",
            labels: publicationYears,
            values: citationCounts,
            label:"Tổng số trích dẫn",
            fill:true
        });
    }

);