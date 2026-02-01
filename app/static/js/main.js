document.addEventListener('DOMContentLoaded', () => {
    const networkCtx = document.getElementById('networkChart').getContext('2d');
    
    // Initialize Chart
    const networkChart = new Chart(networkCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Latency (ms)',
                data: [],
                borderColor: '#f0cb35',
                backgroundColor: 'rgba(240, 203, 53, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { display: false } }
            },
            plugins: { legend: { display: false } }
        }
    });

    function updateDashboard() {
        fetch('/api/status')
            .then(res => res.json())
            .then(data => {
                // Update Network
                document.getElementById('network-latency').textContent = `${data.network.latency} ms`;
                
                const now = new Date().toLocaleTimeString();
                networkChart.data.labels.push(now);
                networkChart.data.datasets[0].data.push(data.network.latency);
                
                if (networkChart.data.labels.length > 20) {
                    networkChart.data.labels.shift();
                    networkChart.data.datasets[0].data.shift();
                }
                networkChart.update();

                // Update ATMs
                const atmList = document.getElementById('atm-list');
                atmList.innerHTML = '';
                data.atms.forEach(atm => {
                    const statusClass = atm.status === 'ONLINE' ? 'status-online' : 'status-offline';
                    atmList.innerHTML += `
                        <div class="atm-item">
                            <div class="atm-info">
                                <h4>${atm.location}</h4>
                                <p style="font-size: 0.8rem; color: #94a3b8">Cash Level: ${atm.cash_level}%</p>
                            </div>
                            <span class="status-indicator ${statusClass}">${atm.status}</span>
                        </div>
                    `;
                });

                // Update Alerts
                const alertList = document.getElementById('alert-list');
                alertList.innerHTML = '';
                if (data.alerts.length === 0) {
                    alertList.innerHTML = '<div class="loading">No active alerts</div>';
                } else {
                    data.alerts.forEach(alert => {
                        const sevClass = alert.severity === 'HIGH' ? 'severity-high' : '';
                        alertList.innerHTML += `
                            <div class="alert-item ${sevClass}">
                                <strong style="color: ${alert.severity === 'CRITICAL' ? '#ef4444' : '#f59e0b'}">${alert.severity}</strong>: 
                                <span>${alert.message}</span>
                                <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 4px;">${alert.time}</div>
                            </div>
                        `;
                    });
                }
            })
            .catch(err => console.error('Error fetching status:', err));
    }

    // Update every 5 seconds
    setInterval(updateDashboard, 5000);
    updateDashboard(); // Initial call
});
