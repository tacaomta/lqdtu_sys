document.addEventListener(

    "DOMContentLoaded",

    () => {

        // =====================================
        // DATA
        // =====================================
        Chart.register(
            ChartDataLabels
        );

        const field_collaboration_labels = JSON.parse(

            document.getElementById(
                "field_collaboration_labels"
            ).textContent

        );
        const field_collaboration_datasets = JSON.parse(

            document.getElementById(
                "field_collaboration_datasets"
            ).textContent

        );
        const field_hindex_datasets = JSON.parse(

            document.getElementById(
                "field_hindex_datasets"
            ).textContent

        );

        createStackedBarChart({

            canvasId:
                "fieldCollaborationChart",

            labels:
                field_collaboration_labels,

            datasets:
                field_collaboration_datasets,

            horizontal: true,

            custom_colors: [DASHBOARD_COLORS[0], DASHBOARD_COLORS[21]]

        });

        createClusteredBarChart({

            canvasId:
                "fieldHindexChart",

            labels:
                field_collaboration_labels,

            datasets:
                field_hindex_datasets,

            horizontal: true,

            custom_colors: [DASHBOARD_COLORS[0], DASHBOARD_COLORS[21]]

        });

        const domestic_international_datasets = JSON.parse(

            document.getElementById(
                "domestic_international_datasets"
            ).textContent

        );
        const domestic_international_hindex_datasets = JSON.parse(

            document.getElementById(
                "domestic_international_hindex_datasets"
            ).textContent

        );

        createStackedBarChart({

            canvasId:
                "domesticInternationalChart",

            labels:
                field_collaboration_labels,

            datasets:
                domestic_international_datasets,

            horizontal: true,
            custom_colors: [DASHBOARD_COLORS[3], DASHBOARD_COLORS[17]]

        });

        createClusteredBarChart({

            canvasId:
                "domesticInternationalHindexChart",

            labels:
                field_collaboration_labels,

            datasets:
                domestic_international_hindex_datasets,

            horizontal: true,
            custom_colors: [DASHBOARD_COLORS[3], DASHBOARD_COLORS[17]]

        });

        const domesticUniversityRanking = JSON.parse(

            document.getElementById(
                "domestic_university_ranking"
            ).textContent

        );
        const internationalUniversityRanking = JSON.parse(

            document.getElementById(
                "international_university_ranking"
            ).textContent

        );
        const countryRanking = JSON.parse(

            document.getElementById(
                "country_ranking"
            ).textContent

        );

        function renderRankingTable({

            tableId,
            data,
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

                    <td>${index + 1}</td>

                    <td>${row.name}</td>

                    <td>${row.count}</td>

                </tr>

            `;

                }

            );
        }

        function renderRankingChart({

            canvasId,
            data,
            topN

        }) {

            const existingChart = Chart.getChart(canvasId);
            if (existingChart){
                existingChart.destroy();
            }

            const labels = data

                .slice(0, topN)

                .map(item => item.name);


            const values = data

                .slice(0, topN)

                .map(item => item.count);

            createBarChart({

                canvasId: canvasId,
                labels: labels,
                values: values,
                label: "CBKH",
                display_legend: false,
                horizontal: true
            });            
        }

        function updateCollaborationRankings() {

            const topN = parseInt(

                document.getElementById(
                    "topNSlider"
                ).value

            );


            document.getElementById(

                "topNLabel"

            ).innerText = topN;


            // =====================================
            // TABLES
            // =====================================

            renderRankingTable({

                tableId:
                    "domesticUniversityTable",

                data:
                    domesticUniversityRanking,

                topN

            });


            renderRankingTable({

                tableId:
                    "internationalUniversityTable",

                data:
                    internationalUniversityRanking,

                topN

            });


            renderRankingTable({

                tableId:
                    "countryTable",

                data:
                    countryRanking,

                topN

            });
            // =====================================
            // CHARTS
            // =====================================

            renderRankingChart({

                canvasId:
                    "domesticUniversityChart",

                data:
                    domesticUniversityRanking,

                topN

            });


            renderRankingChart({

                canvasId:
                    "internationalUniversityChart",

                data:
                    internationalUniversityRanking,

                topN

            });


            renderRankingChart({

                canvasId:
                    "countryChart",

                data:
                    countryRanking,

                topN

            });
        }

        function toggleRankingView() {

            const chartView = document.getElementById(

                "chartViewSwitch"

            ).checked;


            const tablesContainer = document.getElementById(

                "rankingTablesContainer"

            );


            const chartsContainer = document.getElementById(

                "rankingChartsContainer"

            );


            if (chartView) {

                tablesContainer.classList.add(
                    "d-none"
                );

                chartsContainer.classList.remove(
                    "d-none"
                );

            }

            else {

                tablesContainer.classList.remove(
                    "d-none"
                );

                chartsContainer.classList.add(
                    "d-none"
                );

            }
        }

        window.addEventListener(

            "DOMContentLoaded",

            function () {

                updateCollaborationRankings();


                document.getElementById(

                    "topNSlider"

                ).addEventListener(

                    "input",

                    updateCollaborationRankings

                );


                document.getElementById(

                    "chartViewSwitch"

                ).addEventListener(

                    "change",

                    toggleRankingView

                );

            }

        );

        const domesticNetworkNodes =

            JSON.parse(

                document.getElementById(

                    "domestic_network_nodes"

                ).textContent

            );


        const domesticNetworkEdges =

            JSON.parse(

                document.getElementById(

                    "domestic_network_edges"

                ).textContent

            );
        let domesticNetworkCy = null;

        function renderDomesticNetwork(

            threshold = 5

        ) {


            // =====================================
            // DESTROY OLD
            // =====================================

            if (domesticNetworkCy) {

                domesticNetworkCy.destroy();

            }


            // =====================================
            // FILTER EDGES
            // =====================================

            const filteredEdges = domesticNetworkEdges.filter(

                edge =>

                    edge.data.weight >= threshold

            );


            // =====================================
            // GET CONNECTED NODES
            // =====================================

            const connectedNodeIds = new Set();


            filteredEdges.forEach(edge => {

                connectedNodeIds.add(

                    edge.data.source

                );

                connectedNodeIds.add(

                    edge.data.target

                );

            });


            // =====================================
            // FILTER NODES
            // =====================================

            const filteredNodes = domesticNetworkNodes.filter(

                node =>

                    connectedNodeIds.has(

                        node.data.id

                    )

            );


            // =====================================
            // CREATE CY
            // =====================================

            domesticNetworkCy = cytoscape({

                container:

                    document.getElementById(

                        "domesticCollaborationNetwork"

                    ),

                elements: [

                    ...filteredNodes,

                    ...filteredEdges

                ],

                style: [
                    
                    {

                        selector: "node",

                        style: {

                            "background-color": "#1e7eb9",

                            "label": "data(label)",

                            "width": "data(size)",

                            "height": "data(size)",

                            "font-size": 24,

                            "text-wrap": "wrap",

                            "text-max-width": 100,

                            "text-valign": "bottom",

                            "text-margin-y": 10

                        }

                    },
                    {

                        selector: 'node[is_lqdtu = 1]',

                        style: {

                            "background-color": "#d62728",

                            "border-width": 1,

                            "border-color": "#222",
                            "text-valign": "center",
                            "text-margin-y": 0

                        }

                    },

                    {

                        selector: "edge",

                        style: {

                            "width":

                                "mapData(weight, 1, 50, 1, 10)",

                            "line-color": "#999",

                            "curve-style": "bezier",

                            "opacity": 0.8,

                            "label": "data(weight)",

                            "font-size": 24,

                            "text-background-color": "#f8f6f6",

                            "text-background-opacity": 1,

                            "text-background-padding": 2

                        }

                    }

                ],

                layout: {

                    name: "cose",

                    animate: true,

                    idealEdgeLength: 120,

                    nodeRepulsion: 500000

                }

            });

        }

        document.getElementById(

            "networkThresholdSlider"

        ).addEventListener(

            "input",

            function() {

                const threshold = Number(

                    this.value

                );


                document.getElementById(

                    "networkThresholdLabel"

                ).innerText = threshold;


                renderDomesticNetwork(

                    threshold

                );

            }

        );


        renderDomesticNetwork(30);

        ///Mạng lưới quốc tế


        const internationalNetworkNodes =

            JSON.parse(

                document.getElementById(

                    "internaltional_network_nodes"

                ).textContent

            );


        const internationalNetworkEdges =

            JSON.parse(

                document.getElementById(

                    "internaltional_network_edges"

                ).textContent

            );
        let internationalNetworkCy = null;

        function renderInternationalNetwork(

            threshold = 30

        ) {


            // =====================================
            // DESTROY OLD
            // =====================================

            if (internationalNetworkCy) {

                internationalNetworkCy.destroy();

            }


            // =====================================
            // FILTER EDGES
            // =====================================

            const filteredEdges = internationalNetworkEdges.filter(

                edge =>

                    edge.data.weight >= threshold

            );


            // =====================================
            // GET CONNECTED NODES
            // =====================================

            const connectedNodeIds = new Set();


            filteredEdges.forEach(edge => {

                connectedNodeIds.add(

                    edge.data.source

                );

                connectedNodeIds.add(

                    edge.data.target

                );

            });


            // =====================================
            // FILTER NODES
            // =====================================

            const filteredNodes = internationalNetworkNodes.filter(

                node =>

                    connectedNodeIds.has(

                        node.data.id

                    )

            );


            // =====================================
            // CREATE CY
            // =====================================

            internationalNetworkCy = cytoscape({

                container:

                    document.getElementById(

                        "internaltionalCollaborationNetwork"

                    ),

                elements: [

                    ...filteredNodes,

                    ...filteredEdges

                ],

                style: [

                    {

                        selector: "node",

                        style: {

                            "background-color": "#198f8f",

                            "label": "data(label)",

                            "width": "data(size)",

                            "height": "data(size)",

                            "font-size": 24,

                            "text-wrap": "wrap",

                            "text-max-width": 100,

                            "text-valign": "bottom",

                            "text-margin-y": 10

                        }

                    },

                    {

                        selector: 'node[is_lqdtu = 1]',

                        style: {

                            "background-color": "#d62728",

                            "border-width": 1,

                            "border-color": "#222",
                            "text-valign": "center",
                            "text-margin-y": 0

                        }

                    },

                    {

                        selector: "edge",

                        style: {

                            "width":

                                "mapData(weight, 1, 50, 1, 10)",

                            "line-color": "#999",

                            "curve-style": "bezier",

                            "opacity": 0.8,

                            "label": "data(weight)",

                            "font-size": 24,

                            "text-background-color": "#f8f6f6",

                            "text-background-opacity": 1,

                            "text-background-padding": 2

                        }

                    }

                ],

                layout: {

                    name: "cose",

                    animate: true,

                    idealEdgeLength: 120,

                    nodeRepulsion: 500000

                }

            });

        }

        document.getElementById(

            "networkThresholdSlider2"

        ).addEventListener(

            "input",

            function () {

                const threshold = Number(

                    this.value

                );


                document.getElementById(

                    "networkThresholdLabel2"

                ).innerText = threshold;


                renderInternationalNetwork(

                    threshold

                );

            }

        );

        renderInternationalNetwork(30);



        




    }

);