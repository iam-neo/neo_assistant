/**
 * Neo Assistant Documentation Logic
 * Central array managing all future updates seamlessly
 */

const updatesData = [
    {
        version: "v1.1.0",
        date: "March 2026",
        title: "NLP & Nepali Localization Integration",
        description: "Replaced the rigid exact-match parser with a smart, lightweight Natural Language Processing pipeline using spaCy.",
        features: [
            "Introduced spaCy en_core_web_sm for dynamic tokenization and verb extraction.",
            "Added comprehensive support for Romanized & Devanagari Nepali words (e.g., 'खोल', 'khola', 'banao').",
            "Implemented smart stop-word filtering for English & Nepali ('the', 'please', 'ma', 'ko').",
            "Preserved 100% backward compatibility with legacy exact-match commands.",
            "Added requirements.txt for simple dependency management."
        ]
    },
    {
        version: "v1.0.0",
        date: "March 2026",
        title: "Initial Launch: Neo Assistant Core",
        description: "The initial offline-first, rule-based local AI assistant architecture was established. Designed to be lightweight without relying on heavy AI models.",
        features: [
            "Created the core interactive loop in main.py.",
            "Built modular command system separating system actions into commands/ directory.",
            "Added 'open_app' module capable of launching native Windows desktop applications.",
            "Added 'open_website' module mapping domains directly into the default browser.",
            "Added 'create_folder' module for quick filesystem directory creation.",
            "Set up apps.json configuration to map conversational names to system executables."
        ]
    }
];

// Target DOM Element
const container = document.getElementById('updates-container');

// Render Function: Maps JSON data to HTML Nodes
function renderUpdates() {
    container.innerHTML = '';

    updatesData.forEach((update, index) => {
        const card = document.createElement('div');
        card.className = `update-card`;

        // Stagger animation timing slightly based on index
        card.style.transitionDelay = `${index * 0.1}s`;

        card.innerHTML = `
            <div class="card-header">
                <span class="version-badge">${update.version}</span>
                <span class="update-date">${update.date}</span>
            </div>
            <h3 class="update-title">${update.title}</h3>
            <p class="update-description">${update.description}</p>
            <ul class="feature-list">
                ${update.features.map(f => `<li>${f}</li>`).join('')}
            </ul>
        `;

        container.appendChild(card);
    });
}

// Interactivity: Smooth Reveal Animations on scroll
function setupIntersectionObserver() {
    const cards = document.querySelectorAll('.update-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal');
                // Drop observation after it has loaded to prevent re-animating repeatedly
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,    // Trigger when 10% is visible
        rootMargin: "0px 0px -50px 0px" // Trigger slightly before crossing the bottom screen edge
    });

    cards.forEach(card => observer.observe(card));
}

// Lifecycle Init
document.addEventListener('DOMContentLoaded', () => {
    renderUpdates();

    // Slight timeout allows DOM to fully paint before attaching animations
    setTimeout(() => {
        setupIntersectionObserver();
    }, 50);
});
