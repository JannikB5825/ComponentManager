
function handleFileSelect(event) {
    const files = event.target.files;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                const contents = e.target.result;
                const rows = contents.split("\n");

                for (let j = 1; j < rows.length; j++) {
                    const columns = parseCSVRow(rows[j]);

                    if (columns.length >= 8) {
                        const firstColumn = columns[0];
                        const eighthColumn = columns[7];
                        // Make an API call for each row here
                        addComponent(firstColumn, eighthColumn);
                    }
                }
            };

            reader.readAsText(file);
        }
    }
}

function parseCSVRow(row) {
    const separator = ",";
    const quote = '"';
    const columns = [];

    let inQuotes = false;
    let column = "";

    for (let i = 0; i < row.length; i++) {
        const char = row.charAt(i);

        if (char === quote) {
            inQuotes = !inQuotes;
        } else if (char === separator && !inQuotes) {
            columns.push(column.trim());
            column = "";
        } else {
            column += char;
        }
    }

    columns.push(column.trim());

    return columns;
}

function addComponent(firstColumn, eighthColumn) {
    // Replace this with your actual API endpoint and data handling logic
    const url = "/api/addComp";
    const data = {
        cNumber: firstColumn,
        inventory: eighthColumn,
    };

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (response.ok) {
                console.log("API call successful");
            } else {
                console.error("API call failed");
            }
        })
        .catch((error) => {
            console.error("Error occurred during API call:", error);
        });
}

async function createTable(apiResponse) {
    const tableContainer = document.getElementById("content-table");
    const table = document.createElement("table");

    // Create table header
    const headerRow = document.createElement("tr");
    const headerCells = [
        "Key",
        "Name",
        "Category",
        "Price",
        "Inventory",
        "Package",
        "Image",
        "Parameters",
    ];
    headerCells.forEach((cellText) => {
        const cell = document.createElement("th");
        cell.textContent = cellText;
        headerRow.appendChild(cell);
    });
    table.appendChild(headerRow);

    // Create table rows
    for (const key in apiResponse) {
        if (apiResponse.hasOwnProperty(key)) {
            const data = apiResponse[key];
            const row = document.createElement("tr");

            // Create table cells
            const keyCell = document.createElement("td");
            const link = document.createElement("a");
            link.href = "https://www.lcsc.com/product-detail/" + key + ".html";
            link.textContent = key;
            keyCell.appendChild(link);
            row.appendChild(keyCell);

            const nameCell = document.createElement("td");
            nameCell.textContent = data.name;
            row.appendChild(nameCell);

            const categoryCell = document.createElement("td");
            categoryCell.textContent = data.category;
            row.appendChild(categoryCell);

            const priceCell = document.createElement("td");
            priceCell.textContent = data.price;
            row.appendChild(priceCell);

            const inventoryCell = document.createElement("td");
            inventoryCell.textContent = data.inventory;
            row.appendChild(inventoryCell);

            const packageCell = document.createElement("td");
            packageCell.textContent = data.package;
            row.appendChild(packageCell);

            const imageCell = document.createElement("td");
            const image = document.createElement("img");
            imageCell.className = "image-cell";
            image.src = data.image;
            imageCell.appendChild(image);
            row.appendChild(imageCell);

            const parametersCell = document.createElement("td");
            parametersCell.className = "parameters-cell";
            parametersCell.innerHTML = `
          <span>${data.parameters.length} Parameters</span>
          <div class="tooltip">${getParameterTooltip(data.parameters)}</div>
        `;
            row.appendChild(parametersCell);

            table.appendChild(row);
        }
    }

    // Append table to the container
    tableContainer.appendChild(table);
}

// Function to generate the tooltip content for parameters
function getParameterTooltip(parameters) {
    return parameters.map((param) => param.join(": ")).join("<br>");
}

async function loadComps() {
    const response = await fetch("/api/allComps");
    const apiResponse = await response.json();
    await createTable(apiResponse);
    const tooltipCells = document.querySelectorAll(".parameters-cell");
  tooltipCells.forEach((cell) => {
    const span = cell.querySelector("span");
    const tooltip = cell.querySelector("div");

    cell.addEventListener("mouseenter", () => {
        span.classList.add("tooltip");
    });

    cell.addEventListener("mouseleave", () => {
        span.classList.remove("tooltip");
    });

    cell.addEventListener("mouseenter", () => {
        tooltip.classList.remove("tooltip");
    });

    cell.addEventListener("mouseleave", () => {
        tooltip.classList.add("tooltip");
    });
  });
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("input", () => {
        console.log("test");
        const searchQuery = searchInput.value.trim().toLowerCase();
        const rows = document.querySelectorAll("#content-table table tr");
        var first = true;
        rows.forEach((row) => {
            if (first) {
                first = false;
                return;
            }
            const keyCell = row.querySelector("td:first-child");
            const nameCell = row.querySelector("td:nth-child(2)");
            const categoryCell = row.querySelector("td:nth-child(3)");
            const parametersCell = row.querySelector("td:nth-child(8) div");

            const keyText = keyCell.textContent.toLowerCase();
            const nameText = nameCell.textContent.toLowerCase();
            const categoryText = categoryCell.textContent.toLowerCase();
            const parametersText = parametersCell.textContent.toLowerCase();

            if (
                keyText.includes(searchQuery) ||
                nameText.includes(searchQuery) ||
                categoryText.includes(searchQuery) ||
                parametersText.includes(searchQuery)
            ) {
                row.style.display = "table-row";
            } else {
                row.style.display = "none";
            }
        });
    });
}

loadComps();