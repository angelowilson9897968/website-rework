/*
 * JavaScript for the "Anjo Projects" Website
 * This file handles all interactive functionality.
 */

// This function is an example of how you can add interactivity.
function setRiskProfile(profile) {
    alert("You selected the " + profile + " risk profile.");
}

// === Main script execution after the page is loaded ===
document.addEventListener("DOMContentLoaded", function () {
    
    // --- Logic for the Portfolio Builder (Quiz) page ---
    const form = document.getElementById("risk-form");
    if (form) { 
        const questions = form.querySelectorAll(".question");

        // --- NEW: LOGIC TO SAVE AND LOAD ANSWERS ---

        // Function to load answers from Local Storage when the page opens
        const loadAnswers = () => {
            const savedAnswers = JSON.parse(localStorage.getItem('quizAnswers'));
            if (savedAnswers) {
                // Loop through each saved answer
                Object.keys(savedAnswers).forEach(questionName => {
                    const value = savedAnswers[questionName];
                    // Find the radio button that matches the saved answer and check it
                    const radioToSelect = form.querySelector(`input[name="${questionName}"][value="${value}"]`);
                    if (radioToSelect) {
                        radioToSelect.checked = true;
                    }
                });
            }
        };

        // Function to save all current answers to Local Storage
        const saveAnswers = () => {
            const currentAnswers = {};
            questions.forEach(question => {
                const selectedAnswer = question.querySelector('input:checked');
                if (selectedAnswer) {
                    currentAnswers[selectedAnswer.name] = selectedAnswer.value;
                }
            });
            localStorage.setItem('quizAnswers', JSON.stringify(currentAnswers));
        };

        // Add an event listener to every radio button. When one is clicked, save all answers.
        form.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', saveAnswers);
        });

        // Load any existing answers as soon as the page loads
        loadAnswers();

        // --- END OF NEW LOGIC ---

        const startTime = new Date();

        form.addEventListener("submit", function (event) {
            event.preventDefault();

            let riskScore = 0;
            questions.forEach((question) => {
                const selectedAnswer = question.querySelector("input:checked");
                if (selectedAnswer) {
                    riskScore += parseInt(selectedAnswer.value);
                }
            });

            const endTime = new Date();
            const timeTakenInSeconds = (endTime - startTime) / 1000;
            
            // Clear the saved answers after successful submission
            localStorage.removeItem('quizAnswers');

            // --- THIS IS THE UPDATED PART ---
            fetch("https://website-rework-3.onrender.com/submit", {
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
                alert("Failed to connect to the server. Please try again later.");
            });
        });
    }

    // === Logic for the Results Page Dashboard ===
    const dashboardContainer = document.querySelector('.dashboard-container');
    if (dashboardContainer) {
        // ... (The rest of your results page logic remains the same)
        const portfolioDataString = localStorage.getItem("portfolioData");

        if (portfolioDataString) {
            const data = JSON.parse(portfolioDataString);
            
            document.getElementById('score-value').textContent = data.score;
            document.getElementById('return-value').textContent = data.expected_return;
            document.getElementById('std-dev-value').textContent = data.standard_deviation;

            const tableBody = document.querySelector("#allocations-table tbody");
            data.assets.forEach(asset => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${asset.name}</td>
                    <td>${asset.allocation}</td>
                `;
                tableBody.appendChild(row);
            });

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
