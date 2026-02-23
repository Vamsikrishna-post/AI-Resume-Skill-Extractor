const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('resume-input');
const analyzeBtn = document.getElementById('analyze-btn');
const resultsSection = document.getElementById('results');
const loader = document.getElementById('loader');

let selectedFile = null;
let chartInstance = null;

dropZone.onclick = () => fileInput.click();

fileInput.onchange = (e) => {
    selectedFile = e.target.files[0];
    dropZone.querySelector('p').innerText = `Selected: ${selectedFile.name}`;
};

dropZone.ondragover = (e) => {
    e.preventDefault();
    dropZone.style.background = "rgba(99, 102, 241, 0.2)";
};

dropZone.ondragleave = () => {
    dropZone.style.background = "transparent";
};

dropZone.ondrop = (e) => {
    e.preventDefault();
    selectedFile = e.dataTransfer.files[0];
    dropZone.querySelector('p').innerText = `Selected: ${selectedFile.name}`;
};

analyzeBtn.onclick = async () => {
    if (!selectedFile) {
        alert("Please select a file first.");
        return;
    }

    loader.style.display = 'block';
    analyzeBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }
        renderResults(data);
    } catch (error) {
        console.error("Error analyzing resume:", error);
        alert("An error occurred during analysis.");
    } finally {
        loader.style.display = 'none';
        analyzeBtn.disabled = false;
    }
};

function renderResults(data) {
    resultsSection.style.display = 'grid';

    // AI Summary
    document.getElementById('ai-summary').innerText = data.ai_summary;

    // Skills
    const skillsContainer = document.getElementById('skills-container');
    skillsContainer.innerHTML = '';

    for (const [category, skills] of Object.entries(data.skills)) {
        const group = document.createElement('div');
        group.className = 'category-group';
        group.innerHTML = `
            <div class="category-title">${category}</div>
            <div class="skills-list">
                ${skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
            </div>
        `;
        skillsContainer.appendChild(group);
    }

    // Keywords
    const keywordsContainer = document.getElementById('keywords-container');
    keywordsContainer.innerHTML = data.keywords.map(k => `<span class="skill-tag" style="border-color: var(--accent); background: rgba(34, 211, 238, 0.1);">${k}</span>`).join('');

    // Chart
    renderChart(data.frequency);

    window.scrollTo({ top: resultsSection.offsetTop - 50, behavior: 'smooth' });
}

function renderChart(frequency) {
    const ctx = document.getElementById('frequencyChart').getContext('2d');

    if (chartInstance) chartInstance.destroy();

    const labels = Object.keys(frequency);
    const counts = Object.values(frequency);

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mention Frequency',
                data: counts,
                backgroundColor: 'rgba(99, 102, 241, 0.6)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}
