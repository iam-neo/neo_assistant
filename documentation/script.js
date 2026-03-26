/**
 * Neo Assistant Documentation Logic
 * Handles dynamic timeline rendering and docs scrollspy navigation
 */

const updatesData = [
    {
        version: "v1.2.0",
        date: "March 2026",
        title: "Phase 3: Deep LLM Intent Fallback",
        description: "Integrated a quantized Mistral local LLM via Ollama to handle complex reasoning entirely offline when rule-based engines fail.",
        features: [
            "Created utils/llm.py to interface locally with Ollama without external dependencies.",
            "Wired a fallback in the intent parser, preventing command failure on complex input.",
            "Prepared a strict system prompt to correctly parse unstructured English/Nepali sentences.",
            "Preserved performance and stability by keeping it localized."
        ]
    },
    {
        version: "v1.1.0",
        date: "March 2026",
        title: "NLP & Nepali Localization Integration",
        description: "Replaced the rigid exact-match parser with a smart pipeline.",
        features: [
            "Introduced spaCy en_core_web_sm for dynamic tokenization.",
            "Added comprehensive support for Romanized & Devanagari Nepali words.",
            "Implemented smart stop-word filtering for English & Nepali.",
            "Preserved 100% backward compatibility."
        ]
    },
    {
        version: "v1.0.0",
        date: "March 2026",
        title: "Initial Launch: Neo Assistant Core",
        description: "The initial offline-first, rule-based local AI assistant architecture.",
        features: [
            "Built modular command system separating system actions.",
            "Added 'open_app', 'open_website', and 'create_folder'.",
            "Set up apps.json configuration mapping."
        ]
    }
];

// --- Timeline Render Logic ---
function renderUpdates() {
    const container = document.getElementById('updates-container');
    if (!container) return;

    container.innerHTML = '';
    updatesData.forEach((update, index) => {
        const card = document.createElement('div');
        card.className = `update-card`;

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

// --- Scrollspy & Reveal Animations ---
function setupObservers() {
    // 1. Reveal sections on scroll
    const sections = document.querySelectorAll('.doc-section');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });

    sections.forEach(sec => revealObserver.observe(sec));

    // 2. Sidebar Active Link Highlighting
    const navLinks = document.querySelectorAll('.toc a');
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, { threshold: 0.5 }); // Trigger when section is 50% in view

    sections.forEach(sec => scrollObserver.observe(sec));
}

// Lifecycle Init
document.addEventListener('DOMContentLoaded', () => {
    renderUpdates();
    setTimeout(() => {
        setupObservers();
    }, 100);
});
