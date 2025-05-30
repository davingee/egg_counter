import { api } from "./api.js";
import { buildChart } from "./chart.js";

export function app() {
  let chart = null;
  let sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);

  return {
    initialized: false,
    running: false,
    house: 1,
    counts: { 1: 0, 2: 0 },
    trends: { dates: [], house1: [], house2: [] },
    showSettings: false,
    showOptions: false,
    settingsDate: "",
    settingsLoading: false,
    exportDate: sevenDaysAgo.toISOString().slice(0, 10),
    settingsDate: sevenDaysAgo.toISOString().slice(0, 10),
    polling: false,
    socket: null,
    reconnectTimeout: null,
    pollingInterval: null,
    settings: {},
    api,

    async init() {
      if (this.initialized) return;
      this.initialized = true;
      const [s, h, c, t] = await Promise.all([
        this.api.get("/status"),
        this.api.get("/current_house"),
        this.api.get("/current_counts"),
        this.api.get("/trends"),
      ]);
      await this.loadSettings();
      this.running = s.running;
      this.house = h.house;
      this.counts = c;
      this.trends = t;
      this.buildChart();
      this.handleRunningChange();
    },

    async loadSettings() {
      this.settingsLoading = true;
      try {
        const res = await this.api.get("/settings/get");
        this.settings = { ...this.settings, ...res };
      } catch (e) {
        console.error(e);
      } finally {
        this.settingsLoading = false;
      }
    },

    handleRunningChange() {
      if (this.running) {
        this.initWebSocket();
      } else {
        this.closeWebSocket();
      }
    },

    initWebSocket() {
      const wsProtocol = location.protocol === "https:" ? "wss" : "ws";
      const wsUrl = `${wsProtocol}://${location.host}/ws/house_counts`;
      this.socket = new WebSocket(wsUrl);
      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.counts = {
            house1: data.house1 ?? this.counts[1],
            house2: data.house2 ?? this.counts[2],
          };
        } catch (e) {
          console.error("WebSocket parse error:", e);
        }
      };
      this.socket.onerror = () => this.startPolling();
      this.socket.onclose = () => {};
    },

    closeWebSocket() {
      if (this.socket) this.socket.close();
      this.socket = null;
    },

    startPolling() {
      if (!this.pollingInterval && this.running) {
        this.pollingInterval = setInterval(() => this.refreshCounts(), 2000);
      }
    },

    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
        this.pollingInterval = null;
      }
    },

    async refreshCounts() {
      try {
        this.counts = await this.api.get("/current_counts");
      } catch (e) {
        console.error("Polling error:", e);
      }
    },

    async start() {
      if (this.running) return;
      await this.api.post("/start", {
        house_number: this.house,
        config: this.settings,
      });
      this.running = true;
      this.handleRunningChange();
    },

    async stop() {
      if (!this.running) return;
      await this.api.post("/stop", { house_number: this.house });
      this.running = false;
      this.handleRunningChange();
      await this.postAction();
    },

    async selectHouse() {
      await this.api.post("/select_house", {
        house_number: this.house,
        config: this.settings,
      });
      await this.postAction();
    },

    async postAction() {
      await this.refreshCounts();
      this.trends = await this.api.get("/trends");
      this.updateChart();
    },

    buildChart() {
      const ctx = document.getElementById("trendChart").getContext("2d");
      chart = buildChart(ctx, this.trends);
    },

    updateChart() {
      if (!chart) return;
      chart.data.labels = this.trends.dates;
      chart.data.datasets[0].data = this.trends.house1;
      chart.data.datasets[1].data = this.trends.house2;
      chart.update();
    },

    async saveSettings() {
      this.saving = true;
      await this.api
        .put("/settings/update", this.settings)
        .then(() => {
          this.saving = false;
          alert("Settings saved successfully");
          this.showSettings = false;
        })
        .catch(() => {
          this.saving = false;
          alert("Failed to save settings");
        });
    },
    async deleteAll() {
      if (!confirm("Delete ALL rows?")) return;
      this.settingsLoading = true;
      try {
        const { deleted } = await this.api.post("/settings/delete_all");
        alert(`Deleted ${deleted} rows.`);
      } catch {
        alert("Failed to delete all rows.");
      } finally {
        this.settingsLoading = false;
      }
    },
    async deleteByDate() {
      if (!this.settingsDate) return;
      if (!confirm(`Delete rows on ${this.settingsDate}?`)) return;
      this.settingsLoading = true;
      try {
        const { deleted } = await this.api.post("/settings/delete_date", {
          date: this.settingsDate,
        });
        alert(`Deleted ${deleted} rows for ${this.settingsDate}.`);
      } catch {
        alert("Failed to delete by date.");
      } finally {
        this.settingsLoading = false;
      }
    },
    async clearRedis() {
      if (!confirm("Clear all Redis keys?")) return;
      this.settingsLoading = true;
      try {
        const { deleted_keys } = await this.api.post("/settings/clear_redis");
        alert(`Cleared ${deleted_keys} keys.`);
      } catch {
        alert("Failed to clear Redis keys.");
      } finally {
        this.settingsLoading = false;
      }
    },
    async exportCsv() {
      if (!this.exportDate) return;
      if (!confirm("export to csv and email?")) return;
      this.settingsLoading = true;
      try {
        const { exported_csv } = await this.api.post("/settings/export_csv", {
          date: this.exportDate,
          password: this.settings.email_password,
        });
      } catch {
        alert("Failed to export csv.");
      } finally {
        this.settingsLoading = false;
      }
    },
  };
}
