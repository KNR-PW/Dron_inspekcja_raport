// JS do pobierania i wypełniania danych raportu z Flask API

async function loadReport() {
    const response = await fetch('/api/report');
    const data = await response.json();

    document.querySelector("#team-name").textContent = data.team;
    document.querySelector("#team-email").textContent = data.email;
    document.querySelector("#pilot-name").textContent = data.pilot;
    document.querySelector("#pilot-phone").textContent = data.phone;
    document.querySelector("#mission-time").textContent = data.mission_time;
    document.querySelector("#mission-no").textContent = data.mission_no;
    document.querySelector("#duration").textContent = data.duration;
    document.querySelector("#battery-before").textContent = data.battery_before;
    document.querySelector("#battery-after").textContent = data.battery_after;
    document.querySelector("#kp-index").textContent = data.kp_index;

    // Zmiany w infrastrukturze
    const infraTable = document.querySelector("#infra-changes tbody");
    infraTable.innerHTML = "";
    data.infrastructure_changes.forEach((row, idx) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${idx + 1}</td>
            <td>${row.category}</td>
            <td>${row.detection_time}</td>
            <td>${row.location}</td>
            <td><img src="${row.image}" alt="Zmiana"></td>
            <td>${row.jury}</td>
        `;
        infraTable.appendChild(tr);
    });

    // Sytuacje nadzwyczajne
    const incidentsTable = document.querySelector("#incidents tbody");
    incidentsTable.innerHTML = "";
    data.incidents.forEach((row, idx) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${idx + 1}</td>
            <td>${row.event}</td>
            <td>${row.time}</td>
            <td>${row.location}</td>
            <td><img src="${row.image}" alt="Incydent"></td>
            <td>${row.notified}</td>
            <td>${row.jury}</td>
        `;
        incidentsTable.appendChild(tr);
    });
}

document.addEventListener("DOMContentLoaded", loadReport);