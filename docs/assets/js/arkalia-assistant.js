/* ================================
   🤖 ARKALIA ASSISTANT OPTIMISÉ
   Léger & Efficace
   ================================ */

const ArkaliaAssistant = {
    version: '3.1-optimized',

    // 🚀 Initialisation simple
    init() {
        try {
            this.setupSmoothScroll();
            this.setupImageFallback();
            this.setupChatButton();
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

    // 💬 Bouton chat simple et efficace
    setupChatButton() {
        const button = document.createElement('button');
        button.innerHTML = '🌙 Assistant';
        button.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 50px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            transition: transform 0.2s ease;
            z-index: 9999;
        `;

        button.onmouseover = () => button.style.transform = 'translateY(-2px)';
        button.onmouseout = () => button.style.transform = '';
        button.onclick = () => this.showChatModal();

        document.body.appendChild(button);
    },

    // 🎭 Modal chat simple
    showChatModal() {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;

        modal.innerHTML = `
            <div style="
                background: white;
                border-radius: 12px;
                padding: 2rem;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 20px 50px rgba(0,0,0,0.3);
            ">
                <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0; color: #1f2937;">🌙 Assistant Arkalia</h3>
                    <button onclick="this.closest('.modal').remove()" style="
                        background: none;
                        border: none;
                        font-size: 24px;
                        cursor: pointer;
                        margin-left: auto;
                    ">×</button>
                </div>
                <div style="color: #6b7280; line-height: 1.6;">
                    <p><strong>🤖 Salut !</strong> Je suis l'assistant IA d'Arkalia-LUNA.</p>
                    <p><strong>📚 Tu peux :</strong></p>
                    <ul>
                        <li>• Consulter la <a href="quick-start.md" style="color: #6366f1;">documentation</a></li>
                        <li>• Voir les <a href="modules.md" style="color: #6366f1;">modules</a></li>
                        <li>• Lire l'<a href="fonctionnement/structure.md" style="color: #6366f1;">architecture</a></li>
                        <li>• Accéder à l'<a href="api.md" style="color: #6366f1;">API</a></li>
                    </ul>
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

// 🌙 Auto-initialisation quand la page est prête
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ArkaliaAssistant.init());
} else {
    ArkaliaAssistant.init();
}
