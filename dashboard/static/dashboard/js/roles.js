document.addEventListener(

    "DOMContentLoaded",

    () => {

        // =====================================
        // REGISTER
        // =====================================

        Chart.register(
            ChartDataLabels
        );

        const fieldGroupLabels = JSON.parse(

            document.getElementById(
                "field_group_labels"
            ).textContent

        );

        const firstAuthorDatasets = JSON.parse(

            document.getElementById(
                "first_author_datasets"
            ).textContent

        );

        const firstAuthorPercentageValues = JSON.parse(

            document.getElementById(
                "first_author_percentage_values"
            ).textContent

        );

        const corrAuthorDatasets = JSON.parse(

            document.getElementById(
                "corr_author_datasets"
            ).textContent

        );

        const corrAuthorPercentageValues = JSON.parse(

            document.getElementById(
                "corr_author_percentage_values"
            ).textContent

        );

        const firstAuthorCitationDatasets = JSON.parse(

            document.getElementById(
                "first_author_citation_datasets"
            ).textContent

        );

        const firstAuthorCitationPercentageField = JSON.parse(

            document.getElementById(
                "first_author_citation_percentage_field"
            ).textContent

        );

        const corrAuthorCitationDatasets = JSON.parse(

            document.getElementById(
                "corr_author_citation_datasets"
            ).textContent

        );

        const corrAuthorCitationPercentageField = JSON.parse(

            document.getElementById(
                "corr_author_citation_percentage_field"
            ).textContent

        );

        createStackedBarChart({

            canvasId: "firstAuthorFieldChart",
            labels: fieldGroupLabels,
            datasets: firstAuthorDatasets,
            minLabelValue: 10,
            hideSmallLabels: true,
            horizontal: true,
            custom_colors: [DASHBOARD_COLORS[15], DASHBOARD_COLORS[3]]
        });

        createBarChart({

            canvasId: "firstAuthorPercentageChart",
            labels: fieldGroupLabels,
            values: firstAuthorPercentageValues,
            label: "% CBKH có tác giả thứ nhất thuộc LQDTU",
            horizontal: true,
            percentage: true,
            display_y_axis: false,
            display_legend: false,
            custom_color: DASHBOARD_COLORS[15]
        });

        createStackedBarChart({

            canvasId: "correspondingAuthorFieldChart",
            labels: fieldGroupLabels,
            datasets: corrAuthorDatasets,
            minLabelValue: 10,
            hideSmallLabels: true,
            horizontal: true,
            custom_colors: [DASHBOARD_COLORS[17], DASHBOARD_COLORS[3]]
        });

        createBarChart({

            canvasId: "correspondingAuthorPercentageChart",
            labels: fieldGroupLabels,
            values: corrAuthorPercentageValues,
            label: "% CBKH có tác giả liên hệ thuộc LQDTU",
            horizontal: true,
            percentage: true,
            display_y_axis: false,
            display_legend: false,
            custom_color: DASHBOARD_COLORS[17]
        });
        
        createStackedBarChart({

            canvasId: "firstAuthorCitationByFieldChart",
            labels: fieldGroupLabels,
            datasets: firstAuthorCitationDatasets,
            minLabelValue: 10,
            hideSmallLabels: true,
            horizontal: true,
            custom_colors: [DASHBOARD_COLORS[0], DASHBOARD_COLORS[3]]
        });

        createBarChart({

            canvasId: "firstAuthorCitationPercentageByFieldChart",
            labels: fieldGroupLabels,
            values: firstAuthorCitationPercentageField,
            label: "% Trích dẫn từ CBKH có tác giả liên hệ thuộc LQDTU",
            horizontal: true,
            percentage: true,
            display_y_axis: false,
            display_legend: false,
            custom_color: DASHBOARD_COLORS[0]
        });
        createStackedBarChart({

            canvasId: "corrAuthorCitationByFieldChart",
            labels: fieldGroupLabels,
            datasets: corrAuthorCitationDatasets,
            minLabelValue: 10,
            hideSmallLabels: true,
            horizontal: true,
            custom_colors: [DASHBOARD_COLORS[14], DASHBOARD_COLORS[3]]
        });

        createBarChart({

            canvasId: "corrAuthorCitationPercentageByFieldChart",
            labels: fieldGroupLabels,
            values: corrAuthorCitationPercentageField,
            label: "% Trích dẫn từ CBKH có tác giả liên hệ thuộc LQD",
            horizontal: true,
            percentage: true,
            display_y_axis: false,
            display_legend: false,
            custom_color: DASHBOARD_COLORS[14]
        });


        



        

    }

);