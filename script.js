
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector('form[action="/predict"]');
    const fileInput = document.querySelector('input[name="file"]');
    const submitButton = document.querySelector('button[type="submit"]');

    if (!form || !fileInput || !submitButton) {
        console.error("Upload form not found!");
        return;
    }

    // CSV File Validation
    fileInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) return;

        if (!file.name.toLowerCase().endsWith(".csv")) {
            alert("Please select a CSV file only!");
            this.value = "";
            return;
        }

        alert("CSV file selected successfully!");
    });

    // Form Submit
    form.addEventListener("submit", function (event) {

        const file = fileInput.files[0];

        if (!file) {
            event.preventDefault();
            alert("Please select a CSV file first!");
            return;
        }

        if (!file.name.toLowerCase().endsWith(".csv")) {
            event.preventDefault();
            alert("Only CSV files are allowed!");
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Analyzing Transactions...";

    });
// Transaction Analysis Chart
const chartCanvas = document.getElementById("fraudChart");

if (chartCanvas) {

    const genuineText = document.querySelector(".cards .card:nth-child(2) h1");
    const fraudText = document.querySelector(".cards .card:nth-child(3) h1");

    const genuine = parseInt(genuineText.textContent.replace(/,/g, "")) || 0;
    const fraud = parseInt(fraudText.textContent.replace(/,/g, "")) || 0;

    chartCanvas.width = 420;
    chartCanvas.height = 280;

    const ctx = chartCanvas.getContext("2d");
    const total = genuine + fraud;

    if (total > 0) {
        let startAngle = -Math.PI / 2;

        const data = [
            { value: genuine, color: "#16a34a", label: "Genuine" },
            { value: fraud, color: "#dc2626", label: "Fraud" }
        ];

        data.forEach(item => {
            const slice = (item.value / total) * Math.PI * 2;

            ctx.beginPath();
            ctx.moveTo(140, 130);
            ctx.arc(140, 130, 100, startAngle, startAngle + slice);
            ctx.closePath();
            ctx.fillStyle = item.color;
            ctx.fill();

            startAngle += slice;
        });

        data.forEach((item, i) => {
            ctx.fillStyle = item.color;
            ctx.fillRect(270, 95 + i * 45, 18, 18);

            ctx.fillStyle = "#111827";
            ctx.font = "15px Arial";
            ctx.fillText(
                item.label + ": " + item.value,
                298,
                109 + i * 45
            );
        });
    }
}
});
