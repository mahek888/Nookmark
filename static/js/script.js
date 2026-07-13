

const searchInput = document.getElementById("searchInput");
const filter = document.getElementById("typeFilter");
const cards = document.querySelectorAll(".resource-card");

console.log(searchInput);
console.log(filter);
console.log(cards.length);

function updateResources() {

    const query = searchInput.value.toLowerCase();
    const selectedType = filter.value;

    cards.forEach(card => {

        const title = card.dataset.title;
        const type = card.dataset.type;

        const matchesSearch = title.includes(query);
        const matchesType =
            selectedType === "all" || type === selectedType;

        card.style.display =
            (matchesSearch && matchesType) ? "flex" : "none";
    });
}

searchInput.addEventListener("input", updateResources);
filter.addEventListener("change", updateResources);

new Chart(

    document.getElementById("resourceChart"),

    {

        type:"pie",

        data:{

            labels:Object.keys(resourceTypes),

            datasets:[{

                data:Object.values(resourceTypes)

            }]

        }

    }

);

new Chart(

    document.getElementById("statusChart"),

    {

        type:"doughnut",

        data:{

            labels:["Completed","In Progress","Saved"],

            datasets: [{

            label: "Resources",

            data: [
                statusData.completed,
                statusData.in_progress,
                statusData.saved
            ],

            backgroundColor: [
                "#00ff5eff",   // Completed (green)
                "#ebff6aff",   // In Progress (amber)
                "#2081ffe8"    // Saved (blue)
            ],

            borderColor: "#1b2235",

            borderWidth: 2

        }]

        }

    }

);

new Chart(

    document.getElementById("priorityChart"),

    {

        type:"bar",

        data:{

            labels:["High","Medium","Low"],

            datasets: [{
                label: "Resources",
                data: [
                    priorityData.high,
                    priorityData.medium,
                    priorityData.low
                ]
            }]

        }

    }

);