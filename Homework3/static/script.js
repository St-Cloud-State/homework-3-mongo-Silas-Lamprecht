

async function submitApp() {
    appName = document.getElementById("name").value;
    address = document.getElementById("address").value;

    await fetch('/api/submitApp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({name: appName, address})
    });
    
}