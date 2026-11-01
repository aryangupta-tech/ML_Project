
const form = document.getElementById("predictionForm");

// Connect frontend with Flask prediction API

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    for (let key in data) {
        data[key] = Number(data[key]);
    }

    const prediction = document.getElementById("prediction");
    const confidenceElement = document.getElementById("confidence");
    const status = document.getElementById("status");
    const probabilityContainer = document.getElementById("probabilities");

    // Loading state
    prediction.innerText = "Analysing...";
    confidenceElement.innerText = "Calculating confidence...";
    status.innerText = "Processing sensor readings...";

    const submitButton = form.querySelector('button[type="submit"]');

    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerText = "Analysing...";
    }

    try {

        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Prediction failed");
        }

        // Display prediction
        prediction.innerText = result.prediction;

        // Confidence calculation
        const confidence = result.confidence;

        let confidenceLabel;

        if (confidence >= 90) {
            confidenceLabel = "Very High Confidence";
        } else if (confidence >= 75) {
            confidenceLabel = "High Confidence";
        } else if (confidence >= 60) {
            confidenceLabel = "Moderate Confidence";
        } else if (confidence >= 40) {
            confidenceLabel = "Low Confidence";
        } else {
            confidenceLabel = "Very Low Confidence";
        }

        confidenceElement.innerText =
            "Confidence: " + confidence + "%";

        // Confidence label
        status.innerText =
            result.status + " | " + confidenceLabel;

        // Confidence progress bar
        const confidenceBar =
            document.getElementById("confidenceBar");

        if (confidenceBar) {
            confidenceBar.style.width =
                confidence + "%";
        }

        // Prediction timestamp
        const timestamp =
            document.getElementById("timestamp");

        if (timestamp) {
            timestamp.innerText =
                "Last analysed: " + new Date().toLocaleString();
        }

        // Display top 3 probabilities
        probabilityContainer.innerHTML =
            "<h3>Top 3 Predictions</h3>";

        const sortedProbabilities =
            Object.entries(result.probabilities)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 3);

        sortedProbabilities.forEach(([name, probability]) => {

            const p = document.createElement("p");

            p.textContent =
                name + ": " +
                (probability * 100).toFixed(2) + "%";

            probabilityContainer.appendChild(p);

        });

    } catch (error) {

        prediction.innerText = "Prediction Failed";
        confidenceElement.innerText = "";
        status.innerText = error.message;

    } finally {

        if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerText = "Predict";
        }

    }

});


// Load model evaluation metrics

async function loadMetrics() {

    try {

        const response = await fetch("/api/metrics");

        if (!response.ok) {
            throw new Error("Unable to load model metrics");
        }

        const metrics = await response.json();

        document.getElementById("accuracy").innerText =
            "Accuracy: " +
            (metrics.accuracy * 100).toFixed(2) + "%";

        document.getElementById("precision").innerText =
            "Precision: " +
            (metrics.precision * 100).toFixed(2) + "%";

        document.getElementById("recall").innerText =
            "Recall: " +
            (metrics.recall * 100).toFixed(2) + "%";

        document.getElementById("f1").innerText =
            "F1 Score: " +
            (metrics.f1_score * 100).toFixed(2) + "%";

    } catch (error) {

        console.error("Metrics loading failed:", error);

    }

}


// Reset prediction results

form.addEventListener("reset", function() {

    document.getElementById("prediction").innerText =
        "Awaiting sensor data";

    document.getElementById("confidence").innerText = "";

    document.getElementById("status").innerText = "";

    document.getElementById("probabilities").innerHTML = "";

    const confidenceBar =
        document.getElementById("confidenceBar");

    if (confidenceBar) {
        confidenceBar.style.width = "0%";
    }

    const timestamp =
        document.getElementById("timestamp");

    if (timestamp) {
        timestamp.innerText = "";
    }

});


loadMetrics();
