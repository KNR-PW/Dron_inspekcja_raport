async function loadReport() {
    console.log("JS inspection-report.js loaded!");
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
            <td><img src="/uploads/${row.image}" alt="Zmiana"></td>
            <td>${row.jury}</td>
        `;
        infraTable.appendChild(tr);
    });

     const employeesTable = document.querySelector("#employees tbody");
    employeesTable.innerHTML = "";
    if (Array.isArray(data.employees)) {
        data.employees.forEach((row, idx) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${idx + 1}</td>
                <td>${row.present}</td>
                <td>${row.bhp}</td>
                <td>${row.location}</td>
                <td>${row.location_changed}</td>
                <td><img src="/uploads/${row.image}" alt="Pracownik"></td>
                <td>${row.jury}</td>
            `;
            employeesTable.appendChild(tr);
        });
    }

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
            <td><img src="/uploads/${row.image}" alt="Incydent"></td>
            <td>${row.notified}</td>
            <td>${row.jury}</td>
        `;
        incidentsTable.appendChild(tr);
    });

    // Kody ArUco
    const arucoTable = document.querySelector("#arucos tbody");
    arucoTable.innerHTML = "";
    data.arucos.forEach((row, idx) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${idx + 1}</td>
            <td>${row.content}</td>
            <td>${row.location}</td>
            <td>${row.location_changed}</td>
            <td>${row.content_changed}</td>
            <td><img src="/uploads/${row.image}" alt="Aruco" style="max-width:52px;"></td>
            <td>${row.jury}</td>
        `;
        arucoTable.appendChild(tr);
    });

    // Mapa infrastruktury
    const mapImg = document.querySelector("#infra-map");
    if (data.infra_map) {
        // If only filename is stored, use /uploads/; if full path, extract filename
        let mapFile = data.infra_map.split("/").pop();
        mapImg.src = `/uploads/${mapFile}`;
    } else {
        mapImg.src = "/uploads/mapa.jpg";
    }

    // Informacje końcowe
    const finalInfoTable = document.querySelector("#final-info tbody");
    finalInfoTable.innerHTML = "";
    data.final_info.forEach(row => {
        const tr = document.createElement("tr");
        let rowClass = row.class ? row.class : "";
        tr.className = rowClass;
        tr.innerHTML = `
            <td>${row.desc}</td>
            <td>${row.points || ""}</td>
        `;
        finalInfoTable.appendChild(tr);
    });
}
async function clearReport() {
    const confirmClear = confirm("Czy na pewno chcesz usunąć zapisany raport?");
    if (!confirmClear) return;

    const response = await fetch('/api/report/delete', { method: 'DELETE' });
    if (response.ok) {
        alert("Raport został usunięty.");
        clearReportFromUI();
    } else {
        alert("Nie udało się usunąć raportu. "+response.statusText);
    }
}

function clearReportFromUI() {
    const clear = sel => document.querySelector(sel).textContent = "";
    clear("#team-name");
    clear("#team-email");
    clear("#pilot-name");
    clear("#pilot-phone");
    clear("#mission-time");
    clear("#mission-no");
    clear("#duration");
    clear("#battery-before");
    clear("#battery-after");
    clear("#kp-index");

    document.querySelector("#infra-changes tbody").innerHTML = "";
    document.querySelector("#incidents tbody").innerHTML = "";
    document.querySelector("#arucos tbody").innerHTML = "";
    document.querySelector("#infra-map").src = "/uploads/mapa.jpg";
    document.querySelector("#final-info tbody").innerHTML = "";
}

// document.addEventListener("DOMContentLoaded", loadReport);
document.addEventListener("DOMContentLoaded", () => {
    loadReport(); // initial load
    setInterval(loadReport, 1000); // reload every 1 seconds
});