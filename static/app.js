const $ = (selector) => document.querySelector(selector);

let latest = null;

const text = (tag, value, className) => {
  const element = document.createElement(tag);
  element.textContent = String(value);

  if (className) {
    element.className = className;
  }

  return element;
};

function render(data) {
  latest = data;

  const output = $("#result");
  output.replaceChildren();

  if (data.notice) {
    output.append(text("p", data.notice));
  }

  if (data.metrics) {
    const metrics = text("div", "", "metrics");

    Object.entries(data.metrics).forEach(([key, value]) => {
      const card = text("div", "", "metric");

      card.append(
        text("small", key),
        text("strong", value)
      );

      metrics.append(card);
    });

    output.append(metrics);
  }

  if (data.bars) {
    const panel = text("section", "", "panel");

    panel.append(
      text("h2", data.chart_title || "Comparison")
    );

    const maxValue = Math.max(
      1,
      ...data.bars.map((item) => Math.abs(item.value))
    );

    data.bars.forEach((item) => {
      const row = text("div", "", "bar");
      const bar = document.createElement("i");

      bar.style.width =
        (100 * Math.abs(item.value)) / maxValue + "%";

      row.append(
        text("span", item.label),
        bar,
        text(
          "span",
          Number(item.value).toLocaleString(undefined, {
            maximumFractionDigits: 2,
          })
        )
      );

      panel.append(row);
    });

    output.append(panel);
  }

  if (data.rows) {
    const panel = text("section", "", "panel");

    panel.append(
      text("h2", data.table_title || "Results")
    );

    if (!data.rows.length) {
      panel.append(
        text("p", "No results match these filters.")
      );
    } else {
      const wrapper = text("div", "", "scroll");
      const table = document.createElement("table");
      const header = document.createElement("tr");
      const keys = Object.keys(data.rows[0]);

      keys.forEach((key) => {
        header.append(text("th", key));
      });

      table.append(header);

      data.rows.slice(0, 250).forEach((row) => {
        const tableRow = document.createElement("tr");

        keys.forEach((key) => {
          const value =
            typeof row[key] === "object"
              ? JSON.stringify(row[key])
              : row[key];

          tableRow.append(text("td", value));
        });

        table.append(tableRow);
      });

      wrapper.append(table);
      panel.append(wrapper);

      if (data.rows.length > 250) {
        panel.append(
          text(
            "p",
            "Showing first 250 rows; export includes all rows."
          )
        );
      }
    }

    output.append(panel);
  }

  if (data.answer) {
    const panel = text("section", "", "panel");

    panel.append(
      text("h2", "Answer"),
      text("pre", data.answer)
    );

    output.append(panel);
  }

  if (data.details) {
    const details = document.createElement("details");

    details.append(
      text("summary", "Method and full results"),
      text("pre", JSON.stringify(data.details, null, 2))
    );

    output.append(details);
  }
}

async function run(event) {
  if (event) {
    event.preventDefault();
  }

  const button = $("#run");
  button.disabled = true;

  $("#status").textContent = "Running…";
  $("#status").className = "";

  try {
    const params = Object.fromEntries(
      new FormData($("#controls"))
    );

    const response = await fetch("/api/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Portfolio-Request": "1",
      },
      body: JSON.stringify(params),
    });

    const data = await response.json();

    if (!response.ok) {
      throw Error(data.error || "Request failed");
    }

    render(data);

    $("#status").textContent = "Updated successfully";
  } catch (error) {
    $("#status").textContent =
      error.message +
      (latest
        ? " · Previous successful results remain below."
        : "");

    $("#status").className = "error";
  } finally {
    button.disabled = false;
  }
}

$("#controls").addEventListener("submit", run);

$("#export").onclick = () => {
  if (!latest) {
    return;
  }

  const anchor = document.createElement("a");

  const url = URL.createObjectURL(
    new Blob([JSON.stringify(latest, null, 2)], {
      type: "application/json",
    })
  );

  anchor.href = url;
  anchor.download = "results.json";
  anchor.click();

  URL.revokeObjectURL(url);
};

run();
