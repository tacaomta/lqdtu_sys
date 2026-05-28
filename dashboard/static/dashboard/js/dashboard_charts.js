window.DashboardCharts = {

    createBarChart,
    createStackedBarChart,
    createPieChart,
    createLineChart,
    createAreaChart,
    createDualAxisChart
};

const DEFAULT_PLUGIN_OPTIONS = {

    legend: {

        position: "bottom"

    },

    datalabels: {

        color: "#fff",

        font: {

            weight: "bold",

            size: 11

        }

    }

};

// ============================================
// CLUSTERED BAR CHART
// ============================================

function createClusteredBarChart({

    canvasId,
    labels,
    datasets,

    horizontal = true,

    custom_colors = [],

    display_legend = true,

    display_label = true,

    minLabelValue = 0

}) {

    const ctx = document.getElementById(

        canvasId

    );


    // ========================================
    // COLORS
    // ========================================

    const chartColors =

        custom_colors.length > 0

        ? custom_colors

        : DASHBOARD_COLORS;


    // ========================================
    // DATASETS
    // ========================================

    const processedDatasets = datasets.map(

        (dataset, index) => ({

            ...dataset,

            backgroundColor:

                dataset.backgroundColor ||

                chartColors[
                    index % chartColors.length
                ],

            borderColor:

                dataset.borderColor ||

                chartColors[
                    index % chartColors.length
                ],

            borderWidth: 1,
            borderRadius: 3

        })

    );


    // ========================================
    // CHART
    // ========================================

    return new Chart(

        ctx,

        {

            type: "bar",

            data: {

                labels,

                datasets:
                    processedDatasets

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                indexAxis:

                    horizontal ? "y" : "x",

                scales: {

                    x: {

                        beginAtZero: true,

                        stacked: false

                    },

                    y: {

                        stacked: false

                    }

                },

                plugins: {

                    legend: {

                        display:
                            display_legend,

                        position: "bottom"

                    },

                    tooltip: {

                        enabled: true

                    },

                    datalabels: {

                        display:
                            display_label,

                        anchor: "end",

                        align:

                            horizontal

                            ? "right"

                            : "top",

                        formatter: function(value) {

                            if (

                                value < minLabelValue

                            ) {

                                return "";

                            }

                            return value;

                        }

                    }

                }

            },

        }

    );

}


function createBarChart({

    canvasId,
    labels,
    values,
    label = "",
    horizontal = false,
    multiColor = false,
    percentage = false,
    display_y_axis = true,
    display_legend = true,
    custom_color = ""
}) {

    return new Chart(

        document.getElementById(
            canvasId
        ),

        {

            type: "bar",

            data: {

                labels,

                datasets: [{

                    label,

                    data: values,

                    borderRadius: 3,

                    borderWidth: 1,

                    borderColor: DASHBOARD_COLORS[10],

                    backgroundColor:
                        multiColor?

                            DASHBOARD_COLORS.slice(
                                0,
                                labels.length
                            )
                            : custom_color == "" ? DASHBOARD_COLORS[0] : custom_color
                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                indexAxis:

                    horizontal
                        ? "y"
                        : "x",
                scales: {

                    x: {

                        min: 0,

                        max: percentage?100:undefined

                    },
                    y:
                    {
                        display: display_y_axis
                    }
                },

                plugins: {

                    legend: {

                        display: display_legend

                    },

                    datalabels: {

                        display: true,

                        anchor: "end",

                        align: horizontal? "right":"top",

                        font: {

                            weight: "bold"

                        },

                        formatter: (

                            value

                        ) => {

                            return percentage ? value + "%" : value;

                        }

                    }

                }            
            }

        }

    );

}

function createStackedBarChart({

    canvasId,
    labels,
    datasets,
    minLabelValue = 10,
    hideSmallLabels = true,
    horizontal = true,
    custom_colors = []

}) {

    if (window[canvasId + "_chart"])
        { 
            window[canvasId + "_chart"].destroy(); 
        }

    datasets.forEach(

        (dataset, index) => {

            dataset.backgroundColor = custom_colors.length==0?

                DASHBOARD_COLORS[

                    index %
                    DASHBOARD_COLORS.length

                ] 
                : 
                custom_colors[

                    index %
                    custom_colors.length
                ]

        }

    );
    window[canvasId + "_chart"] = new Chart(

        document.getElementById(
            canvasId
        ),

        {

            type: "bar",

            data: {

                labels,
                datasets

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                indexAxis:

                    horizontal
                        ? "y"
                        : "x",

                scales: {

                    x: {

                        stacked: true

                    },

                    y: {

                        stacked: true

                    }

                },

                plugins: {

                    ...DEFAULT_PLUGIN_OPTIONS,

                    datalabels: {

                        color: "#fff",

                        formatter: function(value) {

                            if (

                                hideSmallLabels &&

                                value < minLabelValue

                            ) {

                                return "";

                            }

                            return value;

                        }

                    }

                }

            }

        }

    );

}

function createPieChart({

    canvasId,
    labels,
    values,
    minLabelPercentage = 5,
    doughnut = false

}) {

    return new Chart(

        document.getElementById(
            canvasId
        ),

        {

            type:

                doughnut
                    ? "doughnut"
                    : "pie",

            data: {

                labels,

                datasets: [{

                    data: values,

                    backgroundColor:

                        DASHBOARD_COLORS.slice(
                            0,
                            labels.length
                        ),

                    borderWidth: 1,

                    borderColor: "#fff"

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout:

                    doughnut
                        ? "45%"
                        : 0,

                plugins: {

                    ...DEFAULT_PLUGIN_OPTIONS,

                    datalabels: {

                        color: "#fff",

                        formatter:

                            (value, ctx) => {

                                const data =
                                    ctx.chart.data
                                    .datasets[0]
                                    .data;

                                const total =
                                    data.reduce(
                                        (a, b) => a + b,
                                        0
                                    );
                                
                                    const percentage = value*100/total;
                                    if (percentage<minLabelPercentage)
                                        return null;

                                return percentage.toFixed(1) + "%";

                            }

                    },
                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                const label =
                                    context.label;

                                const value =
                                    context.raw;

                                const data =
                                    context.dataset.data;

                                const total =
                                    data.reduce(

                                        (a, b) => a + b,
                                        0

                                    );

                                const percentage = (

                                    value / total * 100

                                ).toFixed(1);

                                return (

                                    `${label}: ` +
                                    `${value.toLocaleString()} ` +
                                    `(${percentage} %)`

                                );
                            }

                        }

                    }

                }

            },

            plugins: [

                ChartDataLabels

            ]

        }

    );

}

// =====================================================
// LINE CHART
// =====================================================

function createLineChart({

    canvasId,
    labels,
    values,
    label = "",
    fill = false

}) {

    return new Chart(

        document.getElementById(
            canvasId
        ),

        {

            type: "line",

            data: {

                labels,

                datasets: [{

                    label,

                    data: values,

                    borderColor:

                        DASHBOARD_COLORS[0],

                    backgroundColor:

                        DASHBOARD_COLORS[0],

                    tension: 0.3,

                    fill

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom"

                    },

                    datalabels: {

                        anchor: "end",

                        align: "top",

                        font: {

                            weight: "bold"

                        }

                    }

                }

            },

            plugins: [

                ChartDataLabels

            ]

        }

    );

}


// =====================================================
// AREA CHART
// =====================================================

function createAreaChart({

    canvasId,
    labels,
    values,
    label = ""

}) {

    return new Chart(

        document.getElementById(
            canvasId
        ),

        {

            type: "line",

            data: {

                labels,

                datasets: [{

                    label,

                    data: values,

                    borderColor:

                        DASHBOARD_COLORS[0],

                    backgroundColor:

                        DASHBOARD_COLORS[0],

                    tension: 0.3,

                    fill: true

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom"

                    },

                    datalabels: {

                        anchor: "end",

                        align: "top",

                        font: {

                            weight: "bold"

                        }

                    }

                }

            },

            plugins: [

                ChartDataLabels

            ]

        }

    );

}


// =====================================================
// DUAL AXIS CHART
// =====================================================

function createDualAxisChart({

    canvasId,
    labels,

    leftLabel,
    leftValues,

    rightLabel,
    rightValues,

    leftType = "bar",
    rightType = "line"

}) {

    return new Chart(

        document.getElementById(
            canvasId
        ),

        {

            data: {

                labels,

                datasets: [

                    {

                        type: leftType,

                        label: leftLabel,

                        data: leftValues,

                        backgroundColor:

                            DASHBOARD_COLORS[0],

                        borderColor:

                            DASHBOARD_COLORS[0],

                        yAxisID: "y"

                    },

                    {

                        type: rightType,

                        label: rightLabel,

                        data: rightValues,

                        backgroundColor:

                            DASHBOARD_COLORS[1],

                        borderColor:

                            DASHBOARD_COLORS[1],

                        tension: 0.3,

                        yAxisID: "y1"

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                interaction: {

                    mode: "index",

                    intersect: false

                },

                scales: {

                    y: {

                        type: "linear",

                        position: "left"

                    },

                    y1: {

                        type: "linear",

                        position: "right",

                        grid: {

                            drawOnChartArea: false

                        }

                    }

                },

                plugins: {

                    legend: {

                        position: "bottom"

                    },

                    datalabels: {

                        display: false

                    }

                }

            }

        }

    );

}