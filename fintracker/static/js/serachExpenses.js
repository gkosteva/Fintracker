const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const tableApp = document.querySelector(".app-table");
tableOutput.style.display = "none";
tableApp.style.display = "block";
const paginationContainer = document.querySelector(".pagination-container");
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tbody.innerHTML = "";
        fetch("/search-expenses", {
            body: JSON.stringify({searchText: searchValue}),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                tableApp.style.display = "none";
                tableOutput.style.display = "block";

                console.log("data.length", data.length);

                if (data.length === 0) {
                    noResults.style.display = "block";
                    tableOutput.style.display = "none";
                } else {
                    noResults.style.display = "none";
                    data.forEach((item) => {
                        tbody.innerHTML += `
                          <tr>
                           <td>${item.amount}</td>
                          <td>${item.category}</td>
                           <td>${item.description}</td>
                          <td>${item.date}</td>
                           </tr>`;
                    });
                }
            });
    } else {
        tableOutput.style.display = "none";
        tableApp.style.display = "block";
        paginationContainer.style.display = "block";
    }
});