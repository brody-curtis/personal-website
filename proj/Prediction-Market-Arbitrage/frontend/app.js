const refreshBtn = document.getElementById("refreshBtn");
const refreshLabel = document.getElementById("refreshLabel");
const syncDot = document.getElementById("syncDot");
const syncLabel = document.getElementById("syncLabel");
const ticketList = document.getElementById("ticketList");
const emptyState = document.getElementById("emptyState");
const ticketTemplate = document.getElementById("ticketTemplate");

function formatRelativeTime(isoString) {
  if (!isoString) return "Not synced yet";
  const then = new Date(isoString);
  const diffSec = Math.round((Date.now() - then.getTime()) / 1000);
  if (diffSec < 5) return "Synced just now";
  if (diffSec < 60) return `Synced ${diffSec}s ago`;
  const diffMin = Math.round(diffSec / 60);
  if (diffMin < 60) return `Synced ${diffMin}m ago`;
  const diffHr = Math.round(diffMin / 60);
  return `Synced ${diffHr}h ago (${then.toLocaleString()})`;
}

function formatDeadline(isoString) {
  if (!isoString) return { text: "No end date", cls: "" };
  const end = new Date(isoString);
  const diffMs = end.getTime() - Date.now();
  const diffHrs = diffMs / (1000 * 60 * 60);

  const dateText = end.toLocaleString(undefined, {
    month: "short", day: "numeric", hour: "numeric", minute: "2-digit",
  });

  if (diffMs < 0) return { text: `Ended ${dateText}`, cls: "soon" };
  if (diffHrs < 48) return { text: `Ends ${dateText}`, cls: "soon" };
  if (diffHrs < 24 * 7) return { text: `Ends ${dateText}`, cls: "near" };
  return { text: `Ends ${dateText}`, cls: "" };
}

function renderLeg(legEl, platform, question, action, url) {
  legEl.querySelector(".leg-platform").textContent = platform;
  legEl.querySelector(".leg-question").textContent = question;

  const isLiteralYesNo = ["yes", "no"].includes(action.outcome_label.toLowerCase());
  const sideEl = legEl.querySelector(".leg-action__side");
  const outcomeEl = legEl.querySelector(".leg-action__outcome");

  if (isLiteralYesNo) {
    // A genuine Yes/No question: "Yes" / "No" IS the outcome, so show one badge.
    sideEl.textContent = action.outcome_label.toUpperCase();
    sideEl.classList.add(action.outcome_label === "Yes" ? "side-yes" : "side-no");
    outcomeEl.textContent = "";
  } else {
    // A named-outcome market (e.g. Portugal vs Spain): the underlying
    // Yes/No slot is just bookkeeping and can point either way, so
    // showing it would be actively misleading (a bet that wins if
    // Spain wins could be internally labeled "No"). Show only what
    // to actually buy.
    sideEl.textContent = "BUY";
    sideEl.classList.add("side-yes");
    outcomeEl.textContent = action.outcome_label;
  }

  legEl.querySelector(".leg-price").textContent = `$${action.price.toFixed(2)}`;

  const linkEl = legEl.querySelector(".leg-link");
  if (url) {
    linkEl.href = url;
  } else {
    linkEl.style.display = "none";
  }
}

function renderTicket(opp) {
  const node = ticketTemplate.content.cloneNode(true);

  node.querySelector(".ticket__roi").textContent = `${opp.roi_pct.toFixed(2)}%`;

  const deadline = formatDeadline(opp.end_date);
  const deadlineEl = node.querySelector(".ticket__deadline");
  deadlineEl.textContent = deadline.text;
  if (deadline.cls) deadlineEl.classList.add(deadline.cls);

  renderLeg(
    node.querySelector(".ticket__leg--a"),
    opp.platform_a, opp.question_a, opp.action_a, opp.url_a
  );
  renderLeg(
    node.querySelector(".ticket__leg--b"),
    opp.platform_b, opp.question_b, opp.action_b, opp.url_b
  );

  node.querySelector(".ticket__cost").textContent =
    `Cost to hedge: $${opp.best_cost.toFixed(2)} → pays $1.00`;

  const alignEl = node.querySelector(".ticket__align");
  alignEl.classList.add(opp.side_alignment === "flipped" ? "flipped" : "aligned");

  return node;
}

function render(opportunities) {
  ticketList.innerHTML = "";
  if (!opportunities || opportunities.length === 0) {
    emptyState.style.display = "block";
    emptyState.querySelector("p").innerHTML =
      "Scan ran, but nothing cleared the ROI bar right now. Try again in a bit &mdash; books shift constantly.";
    return;
  }
  emptyState.style.display = "none";
  const frag = document.createDocumentFragment();
  opportunities.forEach((opp) => frag.appendChild(renderTicket(opp)));
  ticketList.appendChild(frag);
}

async function runScan() {
  refreshBtn.disabled = true;
  refreshBtn.classList.add("spinning");
  refreshLabel.textContent = "Scanning…";
  syncDot.className = "sync-dot scanning";
  syncLabel.textContent = "Pulling live books from all three platforms…";

  try {
    const res = await fetch("/api/arbs");
    const data = await res.json();

    if (data.error) {
      syncDot.className = "sync-dot error";
      syncLabel.textContent = `Scan failed: ${data.error}`;
    } else {
      syncDot.className = "sync-dot live";
      window.__lastRun = data.last_run;
      syncLabel.textContent = formatRelativeTime(data.last_run);
    }
    render(data.opportunities);
  } catch (err) {
    syncDot.className = "sync-dot error";
    syncLabel.textContent = `Couldn't reach the backend: ${err.message}`;
  } finally {
    refreshBtn.disabled = false;
    refreshBtn.classList.remove("spinning");
    refreshLabel.textContent = "Run scan";
  }
}

refreshBtn.addEventListener("click", runScan);

// Keep the "Synced Xm ago" label fresh without re-fetching.
setInterval(() => {
  if (window.__lastRun) {
    syncLabel.textContent = formatRelativeTime(window.__lastRun);
  }
}, 15000);
