document.addEventListener("DOMContentLoaded", function () {

    // ==============================
    // Income vs Expense Chart
    // ==============================
    const incomeExpenseCanvas = document.getElementById("incomeExpenseChart");

    if (incomeExpenseCanvas) {

        const months = JSON.parse(incomeExpenseCanvas.dataset.months);
        const incomeData = JSON.parse(incomeExpenseCanvas.dataset.income);
        const expenseData = JSON.parse(incomeExpenseCanvas.dataset.expense);

        new Chart(incomeExpenseCanvas, {
            type: "bar",
            data: {
                labels: months,
                datasets: [
                    {
                        label: "Income",
                        data: incomeData,
                        backgroundColor: "#1cc88a",
                        borderRadius: 8,
                        borderSkipped: false,
                        maxBarThickness: 40
                    },
                    {
                        label: "Expense",
                        data: expenseData,
                        backgroundColor: "#e74a3b",
                        borderRadius: 8,
                        borderSkipped: false,
                        maxBarThickness: 40
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
                plugins: {
                    legend: {
                        position: "top",
                        labels: {
                            color: "#2e384d",
                            font: {
                                size: 14,
                                weight: "600"
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: "#ffffff",
                        titleColor: "#2e384d",
                        bodyColor: "#2e384d",
                        borderColor: "#e3e6f0",
                        borderWidth: 1,
                        padding: 12
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: "#858796"
                        },
                        grid: {
                            color: "#f1f3f9"
                        }
                    },
                    x: {
                        ticks: {
                            color: "#858796"
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });

    }

    // ==============================
    // Fee Status Chart
    // ==============================
    const feeCanvas = document.getElementById("feeChart");

    if (feeCanvas) {

        const paidFees = feeCanvas.dataset.paid;
        const partialFees = feeCanvas.dataset.partial;
        const pendingFees = feeCanvas.dataset.pending;

        new Chart(feeCanvas, {
            type: "doughnut",
            data: {
                labels: ["Paid", "Partial", "Pending"],
                datasets: [{
                    data: [
                        paidFees,
                        partialFees,
                        pendingFees
                    ],
                    backgroundColor: [
                        "#1cc88a",
                        "#f6c23e",
                        "#e74a3b"
                    ],
                    hoverOffset: 8,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "70%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            padding: 20,
                            color: "#2e384d",
                            font: {
                                size: 13,
                                weight: "600"
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: "#ffffff",
                        titleColor: "#2e384d",
                        bodyColor: "#2e384d",
                        borderColor: "#e3e6f0",
                        borderWidth: 1,
                        padding: 12
                    }
                }
            }
        });

    }

});