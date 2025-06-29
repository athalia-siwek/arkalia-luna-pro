/* ================================
   🤖 ARKALIA ASSISTANT v3.0-phase1
   Performance & UX Optimisées
   ================================ */

// 🚀 Configuration et optimisations
const ArkaliaAssistant = {
    version: '3.0-phase1',
    initialized: false,

    // 🎯 Initialisation sécurisée
    init() {
        if (this.initialized) return;

        try {
            // Performance observer pour tracking
            this.setupPerformanceTracking();

            // Lazy loading pour les images
            this.setupLazyLoading();

            // Interactions améliorées
            this.setupInteractions();

            // Assistant chat intégré
            this.setupChatAssistant();

            this.initialized = true;
            console.log('🌙 Arkalia Assistant initialized successfully');
        } catch (error) {
            console.warn('🚨 Arkalia Assistant initialization failed:', error);
        }
    },

    // 📊 Performance Tracking
    setupPerformanceTracking() {
        if ('performance' in window) {
            // Mesure du temps de chargement
            window.addEventListener('load', () => {
                const loadTime = performance.now();
                if (loadTime > 3000) {
                    console.warn('⚠️ Page load time slow:', loadTime + 'ms');
                }
            });
        }
    },

    // 🖼️ Lazy Loading Optimisé
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.classList.remove('lazy');
                            imageObserver.unobserve(img);
                        }
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    },

    // 🎨 Interactions Améliorées
    setupInteractions() {
        // Smooth scroll pour les ancres
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Effets hover améliorés
        this.setupHoverEffects();

        // Gestion des erreurs d'images
        this.setupImageErrorHandling();
    },

    // ✨ Effets Hover Optimisés
    setupHoverEffects() {
        const buttons = document.querySelectorAll('.md-button, .arkalia-box');

        buttons.forEach(button => {
            button.addEventListener('mouseenter', (e) => {
                e.target.style.transform = 'translateY(-2px) scale(1.02)';
                e.target.style.boxShadow = '0 8px 25px rgba(99, 102, 241, 0.2)';
            });

            button.addEventListener('mouseleave', (e) => {
                e.target.style.transform = '';
                e.target.style.boxShadow = '';
            });
        });
    },

    // 🖼️ Gestion Erreurs Images
    setupImageErrorHandling() {
        document.querySelectorAll('img').forEach(img => {
            img.addEventListener('error', (e) => {
                // Placeholder SVG en cas d'erreur
                e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjNjM2NmYxIi8+Cjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+QXJrYWxpYTwvdGV4dD4KPHN2Zz4=';
                e.target.alt = 'Arkalia-LUNA Logo';
                console.warn('🖼️ Image failed to load:', e.target.src);
            });
        });
    },

    // 💬 Chat Assistant Intégré (Mode Démo)
    setupChatAssistant() {
        const chatButton = this.createChatButton();
        document.body.appendChild(chatButton);
    },

    // 🎯 Créer Bouton Chat Moderne
    createChatButton() {
        const button = document.createElement('button');
        button.className = 'arkalia-chat-button';
        button.innerHTML = '🌙 Assistant Arkalia';

        // Styles inline pour éviter les conflits CSS
        Object.assign(button.style, {
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            backgroundColor: '#6366f1',
            color: 'white',
            border: 'none',
            borderRadius: '50px',
            padding: '12px 20px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            boxShadow: '0 4px 15px rgba(99, 102, 241, 0.3)',
            transition: 'all 0.3s ease',
            zIndex: '9999'
        });

        button.addEventListener('click', () => this.openChatModal());

        return button;
    },

    // 🎭 Modal Chat Moderne
    openChatModal() {
        const modal = document.createElement('div');
        modal.className = 'arkalia-chat-modal';
        modal.innerHTML = `
            <div class="arkalia-chat-content">
                <div class="arkalia-chat-header">
                    <h3>🌙 Assistant Arkalia-LUNA</h3>
                    <button class="arkalia-close-btn">×</button>
                </div>
                <div class="arkalia-chat-body">
                    <div class="arkalia-chat-messages">
                        <div class="arkalia-message arkalia-bot">
                            <strong>🤖 Arkalia:</strong> Salut ! Je suis l'assistant IA d'Arkalia-LUNA. Comment puis-je t'aider ?
                        </div>
                        <div class="arkalia-message arkalia-bot">
                            <strong>📚 Suggestions:</strong>
                            <ul>
                                <li>• Explique-moi les modules</li>
                                <li>• Comment démarrer Arkalia ?</li>
                                <li>• Quelle est l'architecture ?</li>
                            </ul>
                        </div>
                    </div>
                    <div class="arkalia-chat-input">
                        <input type="text" placeholder="Tape ta question..." />
                        <button>Envoyer</button>
                    </div>
                </div>
            </div>
        `;

        // Styles pour éviter les conflits
        this.applyChatStyles(modal);

        document.body.appendChild(modal);

        // Événements
        modal.querySelector('.arkalia-close-btn').addEventListener('click', () => {
            modal.remove();
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });

        // Focus sur l'input
        modal.querySelector('input').focus();
    },

    // 🎨 Styles Chat Modal
    applyChatStyles(modal) {
        Object.assign(modal.style, {
            position: 'fixed',
            top: '0',
            left: '0',
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: '10000'
        });

        const content = modal.querySelector('.arkalia-chat-content');
        Object.assign(content.style, {
            backgroundColor: 'white',
            borderRadius: '16px',
            width: '90%',
            maxWidth: '500px',
            maxHeight: '600px',
            overflow: 'hidden',
            boxShadow: '0 20px 40px rgba(0, 0, 0, 0.2)'
        });
    }
};

// 🚀 Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    ArkaliaAssistant.init();
});

// 🌐 Gestion PWA (Progressive Web App)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('🔧 Service Worker registered');
            })
            .catch(error => {
                console.log('🚨 Service Worker registration failed');
            });
    });
}
