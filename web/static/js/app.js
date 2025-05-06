import Alpine from "./module.esm.js";
import { app } from "./state.js";

Alpine.data("app", app);
Alpine.start();
export default app;

// import Alpine from "./module.esm.js";

// export default function app() {
//   let chart = null;

//   return {
//     initialized: false,
//     running: false,
//     house: 1,
//     counts: { 1: 0, 2: 0 },
//     trends: { dates: [], house1: [], house2: [] },
//     showSettings: false,
//     settingsDate: "",
//     settingsLoading: false,
//     polling: false,
//     socket: null,
//     reconnectTimeout: null,
//     pollingInterval: null,
//     settings: {},

//     async init() {
//       console.log("hi");
//       if (this.initialized) return;
//       this.initialized = true;
//       const [s, h, c, t] = await Promise.all([
//         this.api.get("/status"),
//         this.api.get("/current_house"),
//         this.api.get("/current_counts"),
//         this.api.get("/trends"),
//       ]);
//       await this.loadSettings();

//       this.running = s.running;
//       this.house = h.house;
//       this.counts = c;
//       this.trends = t;
//       this.buildChart();
//       try {
//         if (this.polling) {
//           this.startPolling(); // fallback if init fails
//         } else {
//           this.handleRunningChange();
//         }
//       } catch (e) {
//         console.error("init error", e);
//         this.polling = true;
//         this.startPolling(); // fallback if init fails
//       }
//     },

//     async loadSettings() {
//       console("ugh");
//       this.settingsLoading = true;
//       try {
//         const res = await fetch("/settings/get");
//         const data = await res.json();
//         this.settings = { ...this.settings, ...data };
//       } catch (e) {
//         console.error(e);
//       } finally {
//         this.settingsLoading = false;
//       }
//     },

//     handleRunningChange() {
//       if (this.running) {
//         if (this.polling) {
//           this.startPolling();
//         } else {
//           this.initWebSocket();
//         }
//       } else {
//         if (this.polling) {
//           this.stopPolling();
//         } else {
//           this.closeWebSocket();
//         }
//       }
//     },

//     initWebSocket() {
//       const wsProtocol = location.protocol === "https:" ? "wss" : "ws";
//       const wsUrl = `${wsProtocol}://${location.host}/ws/house_counts`;
//       this.socket = new WebSocket(wsUrl);

//       this.socket.onmessage = (event) => {
//         // const now = Date.now();
//         // if (now - lastUpdate < 500) return; // Only process every 500ms
//         // lastUpdate = now;

//         try {
//           const data = JSON.parse(event.data);
//           this.counts = {
//             house1: data.house1 ?? this.counts[1],
//             house2: data.house2 ?? this.counts[2],
//           };
//         } catch (e) {
//           console.error("WebSocket parse error:", e);
//         }
//       };

//       this.socket.onerror = (e) => {
//         console.warn("WebSocket error:", e);
//         this.startPolling();
//       };

//       this.socket.onclose = () => {
//         // console.warn("WebSocket closed.");
//         // if (this.running) {
//         //   this.startPolling();
//         // }
//         // this.reconnectTimeout = setTimeout(() => {
//         //   if (this.running) this.initWebSocket();
//         // }, 10000); // Retry every 10s
//       };
//     },

//     closeWebSocket() {
//       if (this.socket) {
//         this.socket.close();
//         this.socket = null;
//       }
//       if (this.reconnectTimeout) {
//         clearTimeout(this.reconnectTimeout);
//         this.reconnectTimeout = null;
//       }
//     },

//     startPolling() {
//       if (!this.pollingInterval && this.running) {
//         this.pollingInterval = setInterval(() => this.refreshCounts(), 2000);
//       }
//     },

//     stopPolling() {
//       if (this.pollingInterval) {
//         clearInterval(this.pollingInterval);
//         this.pollingInterval = null;
//       }
//     },

//     async refreshCounts() {
//       try {
//         this.counts = await this.api.get("/current_counts");
//       } catch (e) {
//         console.error("Polling error:", e);
//       }
//     },

//     // ── Controls ────────────────────────────────────────────────
//     async start() {
//       if (this.running) return;
//       await this.api.post("/start", {
//         house_number: this.house,
//         config: this.settings,
//       });
//       this.running = true;
//       this.handleRunningChange();
//     },
//     async stop() {
//       if (!this.running) return;
//       await this.api.post("/stop", { house_number: this.house });
//       this.running = false;
//       this.handleRunningChange();
//       await this.postAction();
//     },
//     async selectHouse() {
//       await this.api.post("/select_house", { house: this.house });
//       await this.postAction();
//     },
//     async postAction() {
//       await this.refreshCounts();
//       this.trends = await this.api.get("/trends");
//       this.updateChart();
//     },
//     // ── Chart.js ────────────────────────────────────────────────
//     getPercentageChanges(data) {
//       const changes = [];
//       for (let i = 0; i < data.length; i++) {
//         if (i === 0) {
//           changes.push(null); // no previous day
//         } else {
//           const prev = data[i - 1];
//           const curr = data[i];
//           if (prev === 0) {
//             changes.push(null); // avoid division by zero
//           } else {
//             const pct = ((curr - prev) / prev) * 100;
//             changes.push(pct.toFixed(1) + "%");
//           }
//         }
//       }
//       return changes;
//     },
//     buildChart() {
//       const house1Changes = this.getPercentageChanges(this.trends.house1);
//       const house2Changes = this.getPercentageChanges(this.trends.house2);

//       const ctx = document.getElementById("trendChart").getContext("2d");

//       chart = new Chart(ctx, {
//         type: "bar",
//         data: {
//           labels: this.trends.dates,
//           datasets: [
//             {
//               label: "House 1",
//               data: this.trends.house1,
//               backgroundColor: "rgba(59, 130, 246, 0.7)",
//               percentageLabels: house1Changes,
//             },
//             {
//               label: "House 2",
//               data: this.trends.house2,
//               backgroundColor: "rgba(34, 197, 94, 0.7)",
//               percentageLabels: house2Changes,
//             },
//           ],
//         },
//         options: {
//           responsive: true,
//           maintainAspectRatio: false,
//           plugins: {
//             datalabels: false, // disable if you're using chartjs-plugin-datalabels
//             tooltip: {
//               callbacks: {
//                 afterLabel: function (context) {
//                   const change =
//                     context.dataset.percentageLabels?.[context.dataIndex];
//                   return change ? `Change: ${change}` : null;
//                 },
//               },
//             },
//           },
//           scales: {
//             y: { beginAtZero: true },
//             x: { stacked: false },
//           },
//         },
//         plugins: [
//           {
//             id: "percentageLabelPlugin",
//             afterDatasetsDraw(chart, args, options) {
//               const { ctx } = chart;
//               chart.data.datasets.forEach((dataset, datasetIndex) => {
//                 const meta = chart.getDatasetMeta(datasetIndex);

//                 // 🔵 Skip hidden datasets
//                 if (!chart.isDatasetVisible(datasetIndex)) return;

//                 meta.data.forEach((bar, index) => {
//                   const pct = dataset.percentageLabels?.[index];
//                   if (!pct) return;

//                   ctx.fillStyle = "#111";
//                   ctx.font = "12px sans-serif";
//                   ctx.textAlign = "center";
//                   ctx.fillText(pct, bar.x, bar.y - 6);
//                 });
//               });
//             },
//           },
//         ],
//       });
//     },

//     updateChart() {
//       if (!chart) return;
//       chart.data.labels = this.trends.dates;
//       chart.data.datasets[0].data = this.trends.house1;
//       chart.data.datasets[1].data = this.trends.house2;

//       const house1Changes = this.getPercentageChanges(this.trends.house1);
//       const house2Changes = this.getPercentageChanges(this.trends.house2);

//       chart.data.datasets[0].percentageLabels = house1Changes;
//       chart.data.datasets[1].percentageLabels = house2Changes;
//       chart.update();
//     },

//     // ── API Helpers ─────────────────────────────────────────────
//     api: {
//       async get(path) {
//         const res = await fetch(path);
//         if (!res.ok) throw new Error(`GET ${path} ${res.status}`);
//         return res.json();
//       },
//       async post(path, body = null) {
//         const opts = { method: "POST" };
//         if (body && typeof body === "object") {
//           opts.headers = { "Content-Type": "application/json" };
//           opts.body = JSON.stringify(body);
//         }
//         const res = await fetch(path, opts);
//         if (!res.ok) {
//           const text = await res.text();
//           console.error(`POST ${path} failed:`, text);
//           throw new Error(`POST ${path} ${res.status}`);
//         }
//         return res.json();
//       },
//       async put(path, body = null) {
//         const opts = { method: "PUT" };
//         if (body && typeof body === "object") {
//           opts.headers = { "Content-Type": "application/json" };
//           opts.body = JSON.stringify(body);
//         }
//         const res = await fetch(path, opts);
//         if (!res.ok) {
//           const text = await res.text();
//           console.error(`PUT ${path} failed:`, text);
//           throw new Error(`PUT ${path} ${res.status}`);
//         }
//         return res.json();
//       },
//     },

//     // ── Settings Actions ───────────────────────────────────────

//     // async get_settings() {
//     //   const res = await fetch("/api/settings");
//     //   return await res.json();
//     // },
//     // async save_settings(settings) {
//     //   const res = await fetch("/settings/update", {
//     //     method: "PUT",
//     //     headers: { "Content-Type": "application/json" },
//     //     body: JSON.stringify(settings),
//     //   });
//     //   if (res.ok) {
//     //     alert("Settings saved successfully");
//     //   } else {
//     //     alert("Error saving settings");
//     //   }
//     // },

//     async saveSettings() {
//       this.saving = true;
//       // Example: send `this.videoInput`, `this.displayUI`, ... to server
//       await this.api
//         .put("/settings/update", this.settings)
//         .then(() => {
//           this.saving = false;
//           alert("Settings saved successfully");
//           this.showSettings = false;
//         })
//         .catch(() => {
//           this.saving = false;
//           alert("Failed to save settings");
//         });
//     },

//     async deleteAll() {
//       if (!confirm("Delete ALL rows?")) return;
//       this.settingsLoading = true;
//       try {
//         const { deleted } = await this.api.post("/settings/delete_all");
//         alert(`Deleted ${deleted} rows.`);
//       } catch {
//         alert("Failed to delete all rows.");
//       } finally {
//         this.settingsLoading = false;
//       }
//     },
//     async deleteByDate() {
//       if (!this.settingsDate) return;
//       if (!confirm(`Delete rows on ${this.settingsDate}?`)) return;
//       this.settingsLoading = true;
//       try {
//         const { deleted } = await this.api.post("/settings/delete_date", {
//           date: this.settingsDate,
//         });
//         alert(`Deleted ${deleted} rows for ${this.settingsDate}.`);
//       } catch {
//         alert("Failed to delete by date.");
//       } finally {
//         this.settingsLoading = false;
//       }
//     },
//     async clearRedis() {
//       if (!confirm("Clear all Redis keys?")) return;
//       this.settingsLoading = true;
//       try {
//         const { deleted_keys } = await this.api.post("/settings/clear_redis");
//         alert(`Cleared ${deleted_keys} keys.`);
//       } catch {
//         alert("Failed to clear Redis keys.");
//       } finally {
//         this.settingsLoading = false;
//       }
//     },
//     async exportCsv() {
//       if (!confirm("export to csv and email?")) return;
//       this.settingsLoading = true;
//       try {
//         const { exported_csv } = await this.api.post("/settings/export_csv", {
//           date: this.settingsDate,
//           password: this.setting.email_password,
//         });
//       } catch {
//         alert("Failed to export csv.");
//       } finally {
//         this.settingsLoading = false;
//       }
//     },
//   };
// }

// Alpine.data("app", app);
// Alpine.start();
