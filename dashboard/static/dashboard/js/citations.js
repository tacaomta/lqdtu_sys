document.addEventListener(

    "DOMContentLoaded",

    () => {

        // =====================================
        // REGISTER
        // =====================================

        Chart.register(
            ChartDataLabels
        );

        const citationYears = JSON.parse(

            document.getElementById(
                "citation-years"
            ).textContent

        );

        const citationValues = JSON.parse(

            document.getElementById(
                "citation-values"
            ).textContent

        );

        const fieldGroupLabels = JSON.parse(

            document.getElementById(
                "field-group-labels"
            ).textContent

        );

        const stackedDatasets = JSON.parse(

            document.getElementById(
                "stacked-datasets"
            ).textContent

        );

        const citation_group_labels = JSON.parse(

            document.getElementById(
                "citation_group_labels"
            ).textContent

        );

        const citation_group_values = JSON.parse(

            document.getElementById(
                "citation_group_values"
            ).textContent

        );

        const citationSumDatasets = JSON.parse(

            document.getElementById(
                "citation-sum-datasets"
            ).textContent

        );

        const treemapLabels = JSON.parse(

            document.getElementById(
                "treemap-labels"
            ).textContent

        );

        const treemapValues = JSON.parse(

            document.getElementById(
                "treemap-values"
            ).textContent

        );

        const treemapData = treemapLabels.map(

            (label, index) => ({

                field: label,

                value: treemapValues[index]

            })

        );

        const documentTypeDatasets = JSON.parse(

            document.getElementById(
                "document_type_datasets"
            ).textContent

        );

        const articlePercentageValues = JSON.parse(

            document.getElementById(
                "article_percentage_values"
            ).textContent

        );

        const citationByDocumentTypeLabel = JSON.parse(

            document.getElementById(
                "document_type_pie_labels"
            ).textContent

        );

        const citationByDocumentTypeValue = JSON.parse(

            document.getElementById(
                "document_type_pie_values"
            ).textContent

        );



        function buildRollingDataset(

            years,
            values,
            windowSize

        ) {

            // ==========================
            // RAW
            // ==========================

            if (windowSize === 1) {

                return {

                    labels: years,

                    data: values

                };

            }

            // ==========================
            // ROLLING
            // ==========================

            const labels = [];

            const data = [];

            for (

                let i = 0;

                i <= values.length - windowSize;

                i++

            ) {

                let sum = 0;

                for (

                    let j = i;

                    j < i + windowSize;

                    j++

                ) {

                    sum += values[j];

                }

                labels.push(

                    `${years[i]}-${years[i + windowSize - 1]}`

                );

                data.push(sum);

            }

            return {

                labels,
                data

            };

        }

        const ctx = document.getElementById(
            "citationTrendChart"
        );

        let currentWindow = 1;

        let rollingDataset = buildRollingDataset(

            citationYears,
            citationValues,
            currentWindow

        );

        const citationChart = new Chart(

            ctx,

            {

                type: "bar",

                data: {

                    labels: rollingDataset.labels,

                    datasets: [{

                        label: "Trích dẫn",

                        data: rollingDataset.data,

                        borderRadius: 3,
                        borderWidth: 1

                    }]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false

                }

            }

        );

        const slider = document.getElementById(
            "windowSizeSlider"
        );

        const valueText = document.getElementById(
            "windowSizeValue"
        );
        slider.addEventListener(

            "input",

            function () {

                const windowSize = parseInt(
                    this.value
                );

                valueText.innerText =
                    windowSize;

                // ==========================
                // BUILD ROLLING
                // ==========================

                const rolling = buildRollingDataset(

                    citationYears,
                    citationValues,
                    windowSize

                );

                // ==========================
                // UPDATE LABELS + DATA
                // ==========================

                citationChart.data.labels =
                    rolling.labels;

                citationChart.data.datasets[0].data =
                    rolling.data;
                citationChart.data.datasets[0].label =
                    windowSize === 1
                        ? "Trích dẫn"
                        : `Trích dẫn - Cửa sổ trượt ${windowSize} năm`

                // ==========================
                // CHANGE CHART TYPE
                // ==========================

                if (windowSize === 1) {

                    citationChart.config.type =
                        "bar";

                    citationChart.data.datasets[0].tension =
                        0;

                    citationChart.data.datasets[0].fill =
                        false;

                }

                else {

                    citationChart.config.type =
                        "line";

                    citationChart.data.datasets[0].tension =
                        0.3;

                    citationChart.data.datasets[0].fill =
                        true;

                }

                // ==========================
                // UPDATE
                // ==========================

                citationChart.update();

            }

        );

        createStackedBarChart({

            canvasId: "citationFieldStackedChart",
            labels: fieldGroupLabels,
            datasets: stackedDatasets,
            minLabelValue:10,
            hideSmallLabels:true,
            horizontal:true

        });

        // =====================================
        // PIE CHART
        // =====================================
        createPieChart({

            canvasId: "citationGroupPieChart",
            labels: citation_group_labels,
            values: citation_group_values,
            minLabelPercentage: 5,
            doughnut: false

        });

        createStackedBarChart({

            canvasId: "citationContributionChart",
            labels: fieldGroupLabels,
            datasets: citationSumDatasets,
            minLabelValue: 10,
            hideSmallLabels: true,
            horizontal: true

        });

        createPieChart({

            canvasId: "citationContributionPieChart",
            labels: treemapLabels,
            values: treemapValues,
            minLabelPercentage:5,
            doughnut:true

        }); 

        createStackedBarChart({

            canvasId: "documentCitationChart",
            labels: fieldGroupLabels,
            datasets: documentTypeDatasets,
            minLabelValue: 100,
            hideSmallLabels: true,
            horizontal: true

        });

        createBarChart({

            canvasId: "articleCitationPercentageInField",
            labels: fieldGroupLabels,
            values: articlePercentageValues,
            label: "% trích dẫn từ Article",
            horizontal: true,
            percentage:true,
            display_y_axis: false,
            display_legend:false
        });

        createPieChart({

            canvasId: "percentageCitationByDocumentType",
            labels: citationByDocumentTypeLabel,
            values: citationByDocumentTypeValue,
            minLabelPercentage: 5,
            doughnut: true

        }); 
        
    }

);