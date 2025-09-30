/*
 * JavaScript for the "Anjo Projects" Website
 * This file handles all interactive functionality.
 */

// Start a timer as soon as the JavaScript file loads.
const startTime = new Date();

// This function is an example of how you can add interactivity.
function setRiskProfile(profile) {
    alert("You selected the " + profile + " risk profile.");
}

// === Main script execution after the page is loaded ===
document.addEventListener("DOMContentLoaded", function () {
    
    // --- Logic for the Portfolio Builder (Quiz) page ---
    const form = document.getElementById("risk-form");
    if (form) { 
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            let riskScore = 0;
            const questions = form.querySelectorAll(".question");
            questions.forEach((question) => {
                const selectedAnswer = question.querySelector("input:checked");
                if (selectedAnswer) {
                    riskScore += parseInt(selectedAnswer.value);
                }
            });

            const endTime = new Date();
            const timeTakenInSeconds = (endTime - startTime) / 1000;

            fetch("http://127.0.0.1:5000/submit", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    score: riskScore,
                    time_taken: timeTakenInSeconds
                }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Server responded with an error!");
                }
                return response.json();
            })
            .then(data => {
                localStorage.setItem("portfolioData", JSON.stringify(data));
                window.location.href = "results.html";
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Failed to connect to the server. Make sure Flask is running!");
            });
        });
    }

    // === NEW & UPDATED Logic for the Results Page Dashboard ===
    const dashboardContainer = document.querySelector('.dashboard-container');
    if (dashboardContainer) {
        const portfolioDataString = localStorage.getItem("portfolioData");

        if (portfolioDataString) {
            const data = JSON.parse(portfolioDataString);
            
            // 1. Populate Key Statistics Boxes
            document.getElementById('score-value').textContent = data.score;
            document.getElementById('return-value').textContent = data.expected_return;
            document.getElementById('std-dev-value').textContent = data.standard_deviation;

            // 2. Populate the Allocations Table
            const tableBody = document.querySelector("#allocations-table tbody");
            data.assets.forEach(asset => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${asset.name}</td>
                    <td>${asset.allocation}</td>
                `;
                tableBody.appendChild(row);
            });

            // 3. Create the Pie Chart using Chart.js
            const ctx = document.getElementById('allocationChart').getContext('2d');
            
            const labels = data.assets.map(asset => asset.name);
            const allocations = data.assets.map(asset => parseFloat(asset.allocation.replace('%', '')));

            const backgroundColors = labels.map(() => 
                `rgba(${Math.floor(Math.random() * 200)}, ${Math.floor(Math.random() * 200)}, ${Math.floor(Math.random() * 200)}, 0.7)`
            );

            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Asset Allocation',
                        data: allocations,
                        backgroundColor: backgroundColors,
                        borderColor: '#fff',
                        borderWidth: 1.5
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        }
                    }
                }
            });

        } else {
            dashboardContainer.innerHTML = "<h1>No data found. Please complete the risk profile quiz first.</h1>";
        }
    }
});