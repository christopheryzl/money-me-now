async function loadDashboard() {
  const response = await fetch("./data/latest.json");
  if (!response.ok) {
    throw new Error("Run `export-dashboard` before opening the dashboard.");
  }
  return response.json();
}

function colorForSignal(signal) {
  if (signal === "BUY") return "#108a5d";
  if (signal === "SELL") return "#c24141";
  return "#65717c";
}

function renderSummary(data) {
  const summary = document.getElementById("summary");
  const signal = document.getElementById("globalSignal");
  const score = document.getElementById("globalScore");

  summary.textContent = `${data.symbol} · ${data.period} · ${data.candles.length} daily bars`;
  signal.textContent = data.ensemble.signal;
  signal.style.color = colorForSignal(data.ensemble.signal);
  score.textContent = data.ensemble.score.toFixed(2);
  score.style.color = colorForSignal(data.ensemble.signal);
}

function renderChart(data) {
  const container = document.getElementById("chart");
  const chart = LightweightCharts.createChart(container, {
    layout: {
      background: { color: "#ffffff" },
      textColor: "#1f2933",
    },
    grid: {
      vertLines: { color: "#eef0ea" },
      horzLines: { color: "#eef0ea" },
    },
    rightPriceScale: { borderColor: "#d8ddd2" },
    timeScale: { borderColor: "#d8ddd2" },
  });

  const candles = chart.addCandlestickSeries({
    upColor: "#108a5d",
    downColor: "#c24141",
    borderVisible: false,
    wickUpColor: "#108a5d",
    wickDownColor: "#c24141",
  });
  candles.setData(data.candles);
  candles.setMarkers(data.markers);

  const fast = chart.addLineSeries({ color: "#2563eb", lineWidth: 2, title: "Fast SMA" });
  fast.setData(data.overlays.sma_fast);

  const slow = chart.addLineSeries({ color: "#7c3aed", lineWidth: 2, title: "Slow SMA" });
  slow.setData(data.overlays.sma_slow);

  chart.timeScale().fitContent();
  window.addEventListener("resize", () => {
    chart.applyOptions({ width: container.clientWidth, height: container.clientHeight });
  });
}

function renderVotes(data) {
  const root = document.getElementById("votes");
  root.replaceChildren(
    ...data.ensemble.votes.map((vote) => {
      const item = document.createElement("article");
      item.className = "vote";
      item.innerHTML = `
        <header>
          <h3>${vote.strategy}</h3>
          <span class="badge ${vote.signal.toLowerCase()}">${vote.signal}</span>
        </header>
        <div class="metrics">
          <div class="metric"><span>Weight</span><strong>${vote.weight.toFixed(2)}</strong></div>
          <div class="metric"><span>Confidence</span><strong>${vote.confidence.toFixed(2)}</strong></div>
          <div class="metric"><span>Contribution</span><strong>${vote.contribution.toFixed(2)}</strong></div>
        </div>
        <p class="reason">${vote.reason}</p>
      `;
      return item;
    }),
  );
}

loadDashboard()
  .then((data) => {
    renderSummary(data);
    renderChart(data);
    renderVotes(data);
  })
  .catch((error) => {
    document.getElementById("summary").textContent = error.message;
  });
