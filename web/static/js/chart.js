// import Chart from '/static/js/chart.umd.min.js';

export function buildChart(ctx, trends) {
  const getChanges = (data) =>
    data.map((v, i, a) =>
      i === 0 || a[i - 1] === 0
        ? null
        : (((v - a[i - 1]) / a[i - 1]) * 100).toFixed(1) + "%"
    );

  return new Chart(ctx, {
    type: "bar",
    data: {
      labels: trends.dates,
      datasets: [
        {
          label: "House 1",
          data: trends.house1,
          backgroundColor: "rgba(59, 130, 246, 0.7)",
          percentageLabels: getChanges(trends.house1),
        },
        {
          label: "House 2",
          data: trends.house2,
          backgroundColor: "rgba(34, 197, 94, 0.7)",
          percentageLabels: getChanges(trends.house2),
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            afterLabel: (ctx) =>
              ctx.dataset.percentageLabels?.[ctx.dataIndex]
                ? `Change: ${ctx.dataset.percentageLabels[ctx.dataIndex]}`
                : null,
          },
        },
      },
      scales: {
        y: { beginAtZero: true },
        x: { stacked: false },
      },
    },
    plugins: [
      {
        id: "percentageLabelPlugin",
        afterDatasetsDraw(chart, args, options) {
          const { ctx } = chart;
          chart.data.datasets.forEach((dataset, datasetIndex) => {
            const meta = chart.getDatasetMeta(datasetIndex);
            if (!chart.isDatasetVisible(datasetIndex)) return;
            meta.data.forEach((bar, index) => {
              const pct = dataset.percentageLabels?.[index];
              if (!pct) return;
              ctx.fillStyle = "#111";
              ctx.font = "12px sans-serif";
              ctx.textAlign = "center";
              ctx.fillText(pct, bar.x, bar.y - 6);
            });
          });
        },
      },
    ],
  });
}
