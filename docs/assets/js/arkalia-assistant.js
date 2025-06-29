/* ================================
   🤖 ARKALIA ASSISTANT OPTIMISÉ
   Léger & Efficace + Interactions Modernes
   ================================ */

const ArkaliaAssistant = {
    version: '3.2-enhanced',

    // 🚀 Initialisation simple
    init() {
        try {
            this.setupSmoothScroll();
            this.setupImageFallback();
            this.setupInteractiveElements();
            this.setupChatButton();
            this.setupParallaxEffects();
            console.log('🌙 Arkalia Assistant ready');
        } catch (error) {
            console.warn('Assistant init failed:', error);
        }
    },

    // 📜 Smooth scroll pour les ancres
    setupSmoothScroll() {
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href^="#"]');
            if (link) {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    },

    // 🖼️ Gestion erreurs images (simple)
    setupImageFallback() {
        document.addEventListener('error', (e) => {
            if (e.target.tagName === 'IMG') {
                e.target.style.display = 'none';
            }
        }, true);
    },

    // ✨ Interactions pour les nouveaux éléments
    setupInteractiveElements() {
        // Animation d'apparition pour les cards au scroll
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.animation = 'slideInUp 0.6s ease forwards';
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            // Observer les cards et sections
            document.querySelectorAll('.module-card, .quick-link, .support-item').forEach(card => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                observer.observe(card);
            });
        }

        // Effet de parallaxe subtil pour la hero section
        this.setupHeroParallax();

        // Click feedback pour les module cards
        document.addEventListener('click', (e) => {
            const card = e.target.closest('.module-card');
            if (card) {
                card.style.transform = 'translateY(-4px) scale(0.98)';
                setTimeout(() => {
                    card.style.transform = '';
                }, 150);
            }
        });
    },

    // 🌟 Effet parallaxe pour la hero section
    setupHeroParallax() {
        const hero = document.querySelector('.hero-section');
        if (!hero) return;

        let ticking = false;

        const updateParallax = () => {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;

            hero.style.transform = `translateY(${parallax}px)`;
            ticking = false;
        };

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        });
    },

    // 🎭 Effets parallaxe subtils
    setupParallaxEffects() {
        const elements = document.querySelectorAll('.module-card, .quick-link');

        let ticking = false;

        const handleScroll = () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    const scrolled = window.pageYOffset;

                    elements.forEach((el, index) => {
                        const speed = 0.02 + (index * 0.005);
                        const yPos = -(scrolled * speed);
                        el.style.transform = `translateY(${yPos}px)`;
                    });

                    ticking = false;
                });
                ticking = true;
            }
        };

        // Seulement si pas de préférence pour réduire les mouvements
        if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            window.addEventListener('scroll', handleScroll);
        }
    },

    // 💬 Bouton chat amélioré
    setupChatButton() {
        const button = document.createElement('button');
        button.innerHTML = '🌙 Assistant';
        button.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            transition: all 0.3s ease;
            z-index: 9999;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        `;

        // Animation d'entrée
        button.style.transform = 'translateY(100px)';
        setTimeout(() => {
            button.style.transform = 'translateY(0)';
        }, 1000);

        button.onmouseover = () => {
            button.style.transform = 'translateY(-3px) scale(1.05)';
            button.style.boxShadow = '0 6px 25px rgba(99, 102, 241, 0.4)';
        };
        button.onmouseout = () => {
            button.style.transform = 'translateY(0) scale(1)';
            button.style.boxShadow = '0 4px 15px rgba(99, 102, 241, 0.3)';
        };
        button.onclick = () => this.showChatModal();

        document.body.appendChild(button);
    },

    // 🎭 Modal chat amélioré
    showChatModal() {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: fadeIn 0.3s ease;
        `;

        modal.innerHTML = `
            <div style="
                background: white;
                border-radius: 20px;
                padding: 2rem;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 20px 50px rgba(0,0,0,0.3);
                animation: slideInScale 0.3s ease;
                border: 1px solid rgba(99, 102, 241, 0.1);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h3 style="margin: 0; color: #1f2937; font-size: 1.5rem;">🌙 Assistant Arkalia</h3>
                    <button onclick="this.closest('.modal').remove()" style="
                        background: none;
                        border: none;
                        font-size: 28px;
                        cursor: pointer;
                        color: #6b7280;
                        padding: 5px;
                        border-radius: 50%;
                        transition: all 0.2s ease;
                    " onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='none'">×</button>
                </div>
                <div style="color: #6b7280; line-height: 1.6;">
                    <div style="
                        background: linear-gradient(135deg, #6366f1, #8b5cf6);
                        color: white;
                        padding: 1rem;
                        border-radius: 12px;
                        margin-bottom: 1rem;
                    ">
                        <p style="margin: 0; color: white;"><strong>🤖 Salut !</strong> Je suis l'assistant IA d'Arkalia-LUNA.</p>
                    </div>
                    <p><strong>📚 Navigation rapide :</strong></p>
                    <div style="display: grid; gap: 0.5rem; margin-top: 1rem;">
                        <a href="quick-start.md" style="
                            display: flex;
                            align-items: center;
                            gap: 0.5rem;
                            padding: 0.75rem;
                            background: #f9fafb;
                            border-radius: 8px;
                            text-decoration: none;
                            color: #1f2937;
                            transition: all 0.2s ease;
                        " onmouseover="this.style.background='#f3f4f6'; this.style.transform='translateX(4px)'" onmouseout="this.style.background='#f9fafb'; this.style.transform='translateX(0)'">
                            <span>⚡</span> Documentation complète
                        </a>
                        <a href="modules.md" style="
                            display: flex;
                            align-items: center;
                            gap: 0.5rem;
                            padding: 0.75rem;
                            background: #f9fafb;
                            border-radius: 8px;
                            text-decoration: none;
                            color: #1f2937;
                            transition: all 0.2s ease;
                        " onmouseover="this.style.background='#f3f4f6'; this.style.transform='translateX(4px)'" onmouseout="this.style.background='#f9fafb'; this.style.transform='translateX(0)'">
                            <span>📚</span> Modules système
                        </a>
                        <a href="api.md" style="
                            display: flex;
                            align-items: center;
                            gap: 0.5rem;
                            padding: 0.75rem;
                            background: #f9fafb;
                            border-radius: 8px;
                            text-decoration: none;
                            color: #1f2937;
                            transition: all 0.2s ease;
                        " onmouseover="this.style.background='#f3f4f6'; this.style.transform='translateX(4px)'" onmouseout="this.style.background='#f9fafb'; this.style.transform='translateX(0)'">
                            <span>🔌</span> API Reference
                        </a>
                    </div>
                </div>
            </div>
        `;

        modal.className = 'modal';
        modal.onclick = (e) => {
            if (e.target === modal) modal.remove();
        };

        document.body.appendChild(modal);
    }
};

// Ajout des styles d'animation
const styles = document.createElement('style');
styles.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInScale {
        from { 
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        to { 
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(styles);

// 🌙 Auto-initialisation quand la page est prête
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ArkaliaAssistant.init());
} else {
    ArkaliaAssistant.init();
}
