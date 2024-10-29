import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const ArrayVisualizer = ({ array1, array2 }) => {
    // Function to calculate frequencies
    const calculateFrequencies = (array) => {
        return array.reduce((acc, value) => {
            const parsedValue = parseFloat(value);  // Parse value as float
            acc[parsedValue] = (acc[parsedValue] || 0) + 1;
            return acc;
        }, {});
    };

    const freq1 = calculateFrequencies(array1);
    const freq2 = calculateFrequencies(array2);

    // Combine unique keys from both frequency objects
    const allLabels = [...new Set([...Object.keys(freq1), ...Object.keys(freq2)])].sort((a, b) => parseFloat(a) - parseFloat(b));

    // Prepare data for the chart based on frequency
    const data1 = allLabels.map(label => freq1[label] || 0);
    const data2 = allLabels.map(label => freq2[label] || 0);

    const chartData = {
        labels: allLabels.map(label => parseFloat(label).toFixed(2)), // Format labels to 2 decimal points
        datasets: [
            {
                label: 'Array 1',
                data: data1,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
            {
                label: 'Array 2',
                data: data2,
                backgroundColor: 'rgba(255, 99, 132, 0.6)',
            },
        ],
    };

    const options = {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
            },
        },
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Comparison of Two Sorted Arrays by Frequency',
            },
        },
    };

    return (
        <div style={styles.container}>
            <div style={styles.chartContainer}>
                <h3>Bar Chart Visualization</h3>
                <Bar data={chartData} options={options} />
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '20px',
        border: '1px solid #ccc',
        borderRadius: '5px',
        maxWidth: '800px',
        margin: '0 auto',
    },
    chartContainer: {
        marginTop: '20px',
        width: '100%',
    },
};

export default ArrayVisualizer;