

async function submitApp() {
    const appName = document.getElementById("name").value;
    const appAddress = document.getElementById("address").value;

    const response = await fetch('/api/submitApp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({name: appName, address: appAddress})
    });
    const data = await response.json();
    alert(JSON.stringify(data));
}

async function checkStatus() {
    const appId = document.getElementById("check-id").value;

    try {
        const response = await fetch(`/api/checkStatus/${appId}`);
        const data = await response.json();

        const output = document.getElementById("status-output");

        if (data.status === "success") {
            output.innerHTML = `
                <strong>Application ID:</strong> ${data._id}<br>
                <strong>Status:</strong> ${data.application_status}<br>
                <strong>Notes:</strong> ${data.notes.join(", ") || "None"}
            `;
        } else {
            output.innerHTML = `<span style="color:red;">${data.message}</span>`;
        }
    } catch (error) {
        document.getElementById("status-output").innerHTML =
            `<span style="color:red;">An error occurred while checking status.</span>`;
    }
}

async function updateStatus() {
    const appId = document.getElementById("app-id").value;
    const newStatus = document.getElementById("new-status").value;
    const note = document.getElementById("status-note").value;

    const payload = {
        _id: appId,
        status: newStatus
    };

    if (note.trim() !== "") {
        payload.note = note;
    }

    const response = await fetch('/api/update_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const data = await response.json();
    alert(JSON.stringify(data));
}






async function addSubphase() {
    
    const appId = document.getElementById("app-idb").value;
    const subphaseName = document.getElementById("subphase-name").value;

    const response = await fetch('/api/add_subphase', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            _id: appId,
            subphase_name: subphaseName
        })
    });

    const data = await response.json();
    alert(data.status || data.error);
}

async function addTask() {
    const appId = document.getElementById("app-idb").value;
    const subphaseName = document.getElementById("subphase-name").value;
    const taskName = document.getElementById("task-name").value;

    const response = await fetch('/api/add_task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            _id: appId,
            subphase_name: subphaseName,
            task_name: taskName
        })
    });

    const data = await response.json();
    alert(data.status || data.error);
}

async function updateTaskStatus() {
    const appId = document.getElementById("app-idb").value;
    const subphaseName = document.getElementById("subphase-name").value;
    const taskName = document.getElementById("task-name").value;
    const status = document.getElementById("status").value;
    const message = document.getElementById("message").value;
    const response = await fetch('/api/update_task_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            _id: appId,
            subphase_name: subphaseName,
            task_name: taskName,
            status: status,
            message: message
        })
    });

    const data = await response.json();
    alert(data.status || data.error);
}
