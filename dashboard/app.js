// Operations Analytics Dashboard - Main Application Logic
// Modules M5 (Data Visualization) and M6 (Reporting Engine)
// Author: Gnanachandu Kalla | Arrowcosta Technology

// Global state
let productionData = [];
let charts = {};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async function() {
    try {
        await loadData();
        updateKPICards();
        initializeCharts();
        populateTable();
        loadInsights();
        updateTimestamp();
    } catch (error) {
        console.error('Dashboard initialization error:', error);
    }
});

// M5: Data Loading
async function loadData() {
    try {
        const response = await fetch('../data/production_records.csv');
        const csvText = await response.text();
        productionData = parseCSV(csvText);
        console.log(`Loaded ${productionData.length} production records`);
    } catch (error) {
        console.warn('Could not load production data, using sample data');
        productionData = generateSampleData();
    }
}

// Parse CSV data
function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');
    
    return lines.slice(1).map(line => {
        const values = line.split(',');
        const record = {};
        headers.forEach((header, index) => {
            record[header] = values[index];
        });
        return record;
    });
}

// Generate sample data if CSV not available
function generateSampleData() {
    const data = [];
    const lines = ['LINE-A', 'LINE-B', 'LINE-C', 'LINE-D'];
    const shifts = ['Morning', 'Afternoon', 'Night'];
    
    for (let i = 0; i < 100; i++) {
        data.push({
            Date: `2026-0${2 + Math.floor(i/30)}-${String(i % 28 + 1).padStart(2, '0')}`,
            Production_Line: lines[i % 4],
            Shift: shifts[i % 3],
            Production_Volume: 800 + Math.random() * 400,
            OEE_Percent: 60 + Math.random() * 30,
            Defect_Rate_Percent: Math.random() * 5,
            Downtime_Hours: Math.random() * 3,
            Throughput_Efficiency_Percent: 75 + Math.random() * 25
        });
    }
    return data;
}

// M5: Update KPI Cards
function updateKPICards() {
    const avgOEE = calculateAverage(productionData.map(d => parseFloat(d.OEE_Percent)));
    const avgDefectRate = calculateAverage(productionData.map(d => parseFloat(d.Defect_Rate_Percent)));
    const avgThroughput = calculateAverage(productionData.map(d => parseFloat(d.Throughput_Efficiency_Percent)));
    const totalDowntime = productionData.reduce((sum, d) => sum + parseFloat(d.Downtime_Hours), 0);
    
    document.getElementById('avgOEE').textContent = `${avgOEE.toFixed(1)}%`;
    document.getElementById('avgDefectRate').textContent = `${avgDefectRate.toFixed(2)}%`;
    document.getElementById('avgThroughput').textContent = `${avgThroughput.toFixed(1)}%`;
    document.getElementById('totalDowntime').textContent = `${totalDowntime.toFixed(0)} hrs`;
    
    // Update trends
    updateTrend('oeeTrend', avgOEE, 85);
    updateTrend('defectTrend', avgDefectRate, 2, true);
    updateTrend('throughputTrend', avgThroughput, 95);
    updateTrend('downtimeTrend', totalDowntime, 500, true);
}

function updateTrend(elementId, value, target, inverse = false) {
    const element = document.getElementById(elementId);
    const isGood = inverse ? value < target : value > target;
    const diff = Math.abs(value - target);
    
    element.textContent = `${isGood ? '↑' : '↓'} ${diff.toFixed(1)} vs target`;
    element.className = `kpi-trend ${isGood ? 'positive' : 'negative'}`;
}

// M5: Initialize Charts
function initializeCharts() {
    createOEETrendChart();
    createProductionByLineChart();
    createShiftPerformanceChart();
    createCorrelationChart();
    createDefectDistributionChart();
    createMonthlyTrendChart();
}

function createOEETrendChart() {
    const ctx = document.getElementById('oeeTrendChart').getContext('2d');
    const dates = [...new Set(productionData.map(d => d.Date))].sort().slice(0, 30);
    const oeeByDate = dates.map(date => {
        const records = productionData.filter(d => d.Date === date);
        return calculateAverage(records.map(r => parseFloat(r.OEE_Percent)));
    });
    
    charts.oeeTrend = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates.map(d => d.substring(5)),
            datasets: [{
                label: 'OEE %',
                data: oeeByDate,
                borderColor: ChartConfig.colors.primary,
                backgroundColor: 'rgba(74, 144, 226, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            ...ChartConfig.defaults,
            plugins: {
                ...ChartConfig.defaults.plugins,
                title: {
                    display: false
                }
            }
        }
    });
}

function createProductionByLineChart() {
    const ctx = document.getElementById('productionByLineChart').getContext('2d');
    const lines = ['LINE-A', 'LINE-B', 'LINE-C', 'LINE-D'];
    const productionByLine = lines.map(line => {
        const records = productionData.filter(d => d.Production_Line === line);
        return records.reduce((sum, r) => sum + parseFloat(r.Production_Volume), 0);
    });
    
    charts.productionByLine = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: lines,
            datasets: [{
                label: 'Total Production',
                data: productionByLine,
                backgroundColor: [
                    ChartConfig.colors.primary,
                    ChartConfig.colors.secondary,
                    ChartConfig.colors.info,
                    ChartConfig.colors.purple
                ]
            }]
        },
        options: ChartConfig.defaults
    });
}

function createShiftPerformanceChart() {
    const ctx = document.getElementById('shiftPerformanceChart').getContext('2d');
    const shifts = ['Morning', 'Afternoon', 'Night'];
    const oeeByShift = shifts.map(shift => {
        const records = productionData.filter(d => d.Shift === shift);
        return calculateAverage(records.map(r => parseFloat(r.OEE_Percent)));
    });
    
    charts.shiftPerformance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: shifts,
            datasets: [{
                label: 'Average OEE %',
                data: oeeByShift,
                backgroundColor: 'rgba(74, 144, 226, 0.2)',
                borderColor: ChartConfig.colors.primary,
                borderWidth: 2
            }]
        },
        options: {
            ...ChartConfig.defaults,
            scales: {
                r: {
                    ticks: {
                        color: '#a8a8a8'
                    },
                    grid: {
                        color: 'rgba(42, 42, 62, 0.3)'
                    }
                }
            }
        }
    });
}

function createCorrelationChart() {
    const ctx = document.getElementById('correlationChart').getContext('2d');
    const scatterData = productionData.slice(0, 200).map(d => ({
        x: parseFloat(d.Downtime_Hours),
        y: parseFloat(d.Defect_Rate_Percent)
    }));
    
    charts.correlation = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Downtime vs Defects',
                data: scatterData,
                backgroundColor: ChartConfig.colors.danger
            }]
        },
        options: {
            ...ChartConfig.defaults,
            scales: {
                x: {
                    ...ChartConfig.defaults.scales.x,
                    title: {
                        display: true,
                        text: 'Downtime (hours)',
                        color: '#eaeaea'
                    }
                },
                y: {
                    ...ChartConfig.defaults.scales.y,
                    title: {
                        display: true,
                        text: 'Defect Rate (%)',
                        color: '#eaeaea'
                    }
                }
            }
        }
    });
}

function createDefectDistributionChart() {
    const ctx = document.getElementById('defectDistributionChart').getContext('2d');
    const defectRates = productionData.map(d => parseFloat(d.Defect_Rate_Percent));
    const bins = [0, 1, 2, 3, 4, 5];
    const distribution = bins.slice(0, -1).map((bin, i) => {
        return defectRates.filter(rate => rate >= bin && rate < bins[i + 1]).length;
    });
    
    charts.defectDistribution = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: bins.slice(0, -1).map((b, i) => `${b}-${bins[i+1]}%`),
            datasets: [{
                label: 'Frequency',
                data: distribution,
                backgroundColor: ChartConfig.colors.warning
            }]
        },
        options: ChartConfig.defaults
    });
}

function createMonthlyTrendChart() {
    const ctx = document.getElementById('monthlyTrendChart').getContext('2d');
    const months = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];
    const productionByMonth = months.map((month, idx) => {
        const monthNum = String(idx + 2).padStart(2, '0');
        const records = productionData.filter(d => d.Date.includes(`-${monthNum}-`));
        return records.reduce((sum, r) => sum + parseFloat(r.Production_Volume), 0);
    });
    
    charts.monthlyTrend = new Chart(ctx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'Monthly Production',
                data: productionByMonth,
                borderColor: ChartConfig.colors.secondary,
                backgroundColor: 'rgba(92, 184, 92, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: ChartConfig.defaults
    });
}

// M5: Populate Performance Table
function populateTable() {
    const tbody = document.querySelector('#performanceTable tbody');
    const lines = ['LINE-A', 'LINE-B', 'LINE-C', 'LINE-D'];
    
    lines.forEach(line => {
        const records = productionData.filter(d => d.Production_Line === line);
        const totalProduction = records.reduce((sum, r) => sum + parseFloat(r.Production_Volume), 0);
        const avgOEE = calculateAverage(records.map(r => parseFloat(r.OEE_Percent)));
        const avgDefectRate = calculateAverage(records.map(r => parseFloat(r.Defect_Rate_Percent)));
        const totalDowntime = records.reduce((sum, r) => sum + parseFloat(r.Downtime_Hours), 0);
        
        let status = 'excellent';
        if (avgOEE < 70) status = 'needs-improvement';
        else if (avgOEE < 80) status = 'good';
        if (avgDefectRate > 3) status = 'critical';
        
        const row = `
            <tr>
                <td><strong>${line}</strong></td>
                <td>${totalProduction.toLocaleString()}</td>
                <td>${avgOEE.toFixed(1)}%</td>
                <td>${avgDefectRate.toFixed(2)}%</td>
                <td>${totalDowntime.toFixed(1)}</td>
                <td><span class="status-badge ${status}">${status.replace('-', ' ').toUpperCase()}</span></td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

// M7: Load Insights
function loadInsights() {
    const container = document.getElementById('insightsContainer');
    const insights = generateInsights();
    
    insights.forEach(insight => {
        const card = `
            <div class="insight-card ${insight.severity.toLowerCase()}-priority">
                <div class="insight-header">
                    <span class="insight-category">${insight.category}</span>
                    <span class="insight-severity ${insight.severity}">${insight.severity}</span>
                </div>
                <div class="insight-text">${insight.text}</div>
                <div class="insight-recommendation">💡 ${insight.recommendation}</div>
            </div>
        `;
        container.innerHTML += card;
    });
}

function generateInsights() {
    const avgOEE = calculateAverage(productionData.map(d => parseFloat(d.OEE_Percent)));
    const avgDefectRate = calculateAverage(productionData.map(d => parseFloat(d.Defect_Rate_Percent)));
    
    const insights = [
        {
            category: 'Performance',
            severity: avgOEE < 75 ? 'HIGH' : 'MEDIUM',
            text: `Overall Equipment Effectiveness is ${avgOEE.toFixed(1)}%, ${avgOEE < 85 ? 'below' : 'meeting'} the target of 85%.`,
            recommendation: avgOEE < 85 ? 'Focus on reducing downtime and improving maintenance schedules.' : 'Maintain current performance levels.'
        },
        {
            category: 'Quality',
            severity: avgDefectRate > 2 ? 'HIGH' : 'LOW',
            text: `Defect rate is ${avgDefectRate.toFixed(2)}%, ${avgDefectRate > 2 ? 'exceeding' : 'within'} acceptable limits.`,
            recommendation: avgDefectRate > 2 ? 'Implement quality control checkpoints and operator training.' : 'Continue quality monitoring.'
        },
        {
            category: 'Operations',
            severity: 'MEDIUM',
            text: 'Night shift consistently shows higher variability in production metrics.',
            recommendation: 'Review night shift staffing and implement standardized operating procedures.'
        }
    ];
    
    return insights;
}

// Utility functions
function calculateAverage(arr) {
    return arr.reduce((sum, val) => sum + val, 0) / arr.length;
}

function updateTimestamp() {
    const now = new Date();
    document.getElementById('lastUpdate').textContent = now.toLocaleString();
}

console.log('Operations Dashboard initialized successfully');
