// Chart.js Configuration for Operations Dashboard
// Author: Gnanachandu Kalla | Arrowcosta Technology

const CHART_COLORS = {
    primary: '#4a90e2',
    secondary: '#5cb85c',
    danger: '#d9534f',
    warning: '#f0ad4e',
    info: '#5bc0de',
    lightBlue: '#64b5f6',
    purple: '#9c27b0',
    orange: '#ff9800'
};

const chartDefaults = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: '#eaeaea',
                font: {
                    size: 12
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(22, 33, 62, 0.9)',
            titleColor: '#eaeaea',
            bodyColor: '#a8a8a8',
            borderColor: '#4a90e2',
            borderWidth: 1,
            padding: 12,
            displayColors: true
        }
    },
    scales: {
        x: {
            ticks: {
                color: '#a8a8a8'
            },
            grid: {
                color: 'rgba(42, 42, 62, 0.3)'
            }
        },
        y: {
            ticks: {
                color: '#a8a8a8'
            },
            grid: {
                color: 'rgba(42, 42, 62, 0.3)'
            }
        }
    }
};

// Helper function to create gradient backgrounds
function createGradient(ctx, colorStart, colorEnd) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, colorStart);
    gradient.addColorStop(1, colorEnd);
    return gradient;
}

// Export configurations
const ChartConfig = {
    colors: CHART_COLORS,
    defaults: chartDefaults,
    createGradient: createGradient
};
