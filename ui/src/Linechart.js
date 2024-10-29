import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const LineChart = ({ prices }) => {
    // Prepare labels (e.g., time or index) and data for the chart
    const labels = prices.map((_, index) => index + 1); // Create labels as indices
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Last Traded Price',
                data: prices,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0, // Set tension to 0 for straight lines
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Last Traded Price Over Time',
            },
        },
    };

    return <Line data={data} options={options} />;
};

export default LineChart;