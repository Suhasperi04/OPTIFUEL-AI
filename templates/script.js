// Loader Animation
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelector('.loader-container').style.opacity = '0';
        setTimeout(() => {
            document.querySelector('.loader-container').style.display = 'none';
            document.querySelector('.dashboard').classList.remove('hidden');
        }, 500);
    }, 2000);
});

// Chart Initialization
const initializeCharts = () => {
    // Fuel Consumption Chart
    const fuelCtx = document.getElementById('fuelChart').getContext('2d');
    new Chart(fuelCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Fuel Consumption (gallons)',
                data: [12000, 11500, 11000, 10800, 10200, 9800],
                borderColor: '#2196f3',
                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });

    // Route Efficiency Chart
    const routeCtx = document.getElementById('routeChart').getContext('2d');
    new Chart(routeCtx, {
        type: 'bar',
        data: {
            labels: ['Route A', 'Route B', 'Route C', 'Route D', 'Route E'],
            datasets: [{
                label: 'Efficiency Score',
                data: [85, 92, 78, 95, 88],
                backgroundColor: [
                    'rgba(33, 150, 243, 0.8)',
                    'rgba(76, 175, 80, 0.8)',
                    'rgba(255, 152, 0, 0.8)',
                    'rgba(156, 39, 176, 0.8)',
                    'rgba(233, 30, 99, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
};

// Initialize charts when dashboard is visible
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        initializeCharts();
    }, 2500);
});

// Navigation Functionality
document.querySelectorAll('.nav-links li').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelectorAll('.nav-links li').forEach(li => li.classList.remove('active'));
        item.classList.add('active');
    });
}); 