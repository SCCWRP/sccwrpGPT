let currentPage = 1;
let rowsToShow = 10; // Default rows to show
let totalRows = 0;
let totalPages = 0;





document.getElementById("prev-page").addEventListener('click', function (e) {
    e.preventDefault();
    if (currentPage > 1) {
        changePage(currentPage - 1);
    }
});

document.getElementById("next-page").addEventListener('click', function (e) {
    e.preventDefault();
    if (currentPage < totalPages) {
        changePage(currentPage + 1);
    }
});

function changePage(page) {
    currentPage = page;
    updateTableRows();
}




function generatePagination() {
    let paginationNav = document.getElementById("pagination-nav");

    // Keeping the prev and next button, and removing all in-between
    while (paginationNav.children.length > 2) {
        paginationNav.removeChild(paginationNav.children[1]);
    }

    for (let i = 1; i <= totalPages; i++) {
        let li = document.createElement("li");
        li.className = i === currentPage ? "page-item active" : "page-item";
        li.innerHTML = `<a class="page-link page-link-numbered" href="#" data-page-number="${i}">${i}</a>`;
        paginationNav.insertBefore(li, document.getElementById("next-page"));
    }


    Array.from(document.querySelectorAll("a.page-link.page-link-numbered")).forEach(a => {
        a.addEventListener('click', function(e){
            e.preventDefault();
            changePage(this.dataset.pageNumber)
        })
    })

    // Handle 'Previous' and 'Next' button states
    document.getElementById('prev-page').classList = currentPage === 1 ? "page-item disabled" : "page-item";
    document.getElementById('next-page').classList = currentPage === totalPages ? "page-item disabled" : "page-item";
}

function updateTableRows() {
    let table = document.getElementById("data-table");
    let allRows = table.getElementsByTagName("tr");
    totalRows = allRows.length - 1; // Exclude header row
    totalPages = Math.ceil(totalRows / rowsToShow);
    
    currentPage = Math.min(totalPages, currentPage);
    console.log('totalPages')
    console.log(totalPages)
    console.log('totalRows')
    console.log(totalRows)
    console.log('currentPage')
    console.log(currentPage)

    for (let i = 1; i <= totalRows; i++) {
        if (i > (currentPage - 1) * rowsToShow && i <= currentPage * rowsToShow) {
            allRows[i].style.display = "";
        } else {
            allRows[i].style.display = "none";
        }
    }

    generatePagination();
}


// execute upon creation of the table
export function addPagination() {
    updateTableRows();

    // Below code is for adding a select dropdown to change the amount of rows to show
    document.getElementById("pagination").value = rowsToShow; // Set the default rows to show on load
    
    document.getElementById("pagination").addEventListener('change', function (e) {
        rowsToShow = Number(this.value);
        updateTableRows();
    })
}


export function createTableFromJSON(jsonDataString) {
    const jsonData = JSON.parse(jsonDataString)
    if (jsonData.length === 0) {
        return '<p>No records found.</p>';
    }

    let totalRows = jsonData.length;
    let totalPages = Math.ceil(totalRows / rowsToShow);

    var table = '<table class="table table-bordered" id="data-table"><thead><tr>';
    // Add headers
    Object.keys(jsonData[0]).forEach(key => {
        table += `<th>${key}</th>`;
    });
    table += '</tr></thead><tbody>';

    // Add rows
    jsonData.forEach((record, index) => {
        let displayStyle = (index >= (currentPage - 1) * rowsToShow && index < currentPage * rowsToShow) ? '' : 'none';
        table += `<tr style="display: ${displayStyle}">`;
        Object.values(record).forEach(value => {
            table += `<td>${value}</td>`;
        });
        table += '</tr>';
    });

    table += '</tbody></table>';
    return table;
}