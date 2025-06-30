/**
 * 🌙 Arkalia-LUNA Enhancements v2.8.0
 * Améliorations JavaScript pour l'expérience utilisateur
 */

(function() {
    'use strict';

    // ================================
    // CONFIGURATION
    // ================================
    const CONFIG = {
        animationDuration: 300,
        scrollOffset: 100,
        themeKey: 'arkalia-theme',
        reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches
    };

    // ================================
    // UTILITAIRES
    // ================================
    const utils = {
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        throttle(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },

        isElementInViewport(el) {
            const rect = el.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        },

        smoothScrollTo(element, offset = 0) {
            if (CONFIG.reducedMotion) {
                element.scrollIntoView();
                return;
            }

            const targetPosition = element.offsetTop - offset;
            const startPosition = window.pageYOffset;
            const distance = targetPosition - startPosition;
            const duration = 800;
            let start = null;

            function animation(currentTime) {
                if (start === null) start = currentTime;
                const timeElapsed = currentTime - start;
                const run = ease(timeElapsed, startPosition, distance, duration);
                window.scrollTo(0, run);
                if (timeElapsed < duration) requestAnimationFrame(animation);
            }

            function ease(t, b, c, d) {
                t /= d / 2;
                if (t < 1) return c / 2 * t * t + b;
                t--;
                return -c / 2 * (t * (t - 2) - 1) + b;
            }

            requestAnimationFrame(animation);
        }
    };

    // ================================
    // GESTIONNAIRE DE THÈME
    // ================================
    class ThemeManager {
        constructor() {
            this.currentTheme = this.getStoredTheme() || this.getSystemTheme();
            this.init();
        }

        getSystemTheme() {
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'slate' : 'default';
        }

        getStoredTheme() {
            return localStorage.getItem(CONFIG.themeKey);
        }

        setTheme(theme) {
            this.currentTheme = theme;
            document.documentElement.setAttribute('data-md-color-scheme', theme);
            localStorage.setItem(CONFIG.themeKey, theme);
            this.updateThemeIcon(theme);
        }

        updateThemeIcon(theme) {
            const themeToggle = document.querySelector('[data-md-color-scheme-toggle]');
            if (themeToggle) {
                const icon = themeToggle.querySelector('svg');
                if (icon) {
                    icon.innerHTML = theme === 'slate' ?
                        '<path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>' :
                        '<path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>';
                }
            }
        }

        init() {
            this.setTheme(this.currentTheme);

            // Écouter les changements de préférence système
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (!this.getStoredTheme()) {
                    this.setTheme(e.matches ? 'slate' : 'default');
                }
            });
        }
    }

    // ================================
    // ANIMATIONS D'ENTRÉE
    // ================================
    class EntranceAnimations {
        constructor() {
            this.animatedElements = [];
            this.init();
        }

        init() {
            this.observeElements();
            this.animateOnLoad();
        }

        observeElements() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '50px'
            });

            // Observer les éléments à animer
            document.querySelectorAll('.module-card, .quick-link, .requirement-item, .support-item').forEach(el => {
                el.classList.add('animate-ready');
                observer.observe(el);
            });
        }

        animateOnLoad() {
            if (CONFIG.reducedMotion) return;

            // Animation de la hero section
            const hero = document.querySelector('.hero-section');
            if (hero) {
                setTimeout(() => {
                    hero.classList.add('hero-animate');
                }, 100);
            }

            // Animation des titres
            document.querySelectorAll('h1, h2, h3').forEach((title, index) => {
                setTimeout(() => {
                    title.classList.add('title-animate');
                }, 200 + (index * 50));
            });
        }
    }

    // ================================
    // NAVIGATION AMÉLIORÉE
    // ================================
    class EnhancedNavigation {
        constructor() {
            this.currentSection = null;
            this.init();
        }

        init() {
            this.setupScrollSpy();
            this.setupSmoothScroll();
            this.setupMobileMenu();
        }

        setupScrollSpy() {
            const sections = document.querySelectorAll('h1[id], h2[id], h3[id]');
            const navLinks = document.querySelectorAll('.md-nav__link[href^="#"]');

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const id = entry.target.getAttribute('id');
                        this.updateActiveNavLink(id);
                    }
                });
            }, {
                threshold: 0.5,
                rootMargin: `-${CONFIG.scrollOffset}px 0px -50% 0px`
            });

            sections.forEach(section => observer.observe(section));
        }

        updateActiveNavLink(activeId) {
            document.querySelectorAll('.md-nav__link').forEach(link => {
                link.classList.remove('md-nav__link--active');
            });

            const activeLink = document.querySelector(`.md-nav__link[href="#${activeId}"]`);
            if (activeLink) {
                activeLink.classList.add('md-nav__link--active');
            }
        }

        setupSmoothScroll() {
            document.querySelectorAll('a[href^="#"]').forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('href').substring(1);
                    const targetElement = document.getElementById(targetId);

                    if (targetElement) {
                        utils.smoothScrollTo(targetElement, CONFIG.scrollOffset);
                    }
                });
            });
        }

        setupMobileMenu() {
            const menuToggle = document.querySelector('.md-nav__toggle');
            const nav = document.querySelector('.md-nav');

            if (menuToggle && nav) {
                menuToggle.addEventListener('click', () => {
                    nav.classList.toggle('md-nav--open');
                });

                // Fermer le menu en cliquant à l'extérieur
                document.addEventListener('click', (e) => {
                    if (!nav.contains(e.target) && !menuToggle.contains(e.target)) {
                        nav.classList.remove('md-nav--open');
                    }
                });
            }
        }
    }

    // ================================
    // INTERACTIONS AVANCÉES
    // ================================
    class AdvancedInteractions {
        constructor() {
            this.init();
        }

        init() {
            this.setupHoverEffects();
            this.setupCopyButtons();
            this.setupProgressIndicator();
            this.setupSearchEnhancement();
        }

        setupHoverEffects() {
            // Effet de parallaxe sur les cartes
            document.querySelectorAll('.module-card, .quick-link').forEach(card => {
                card.addEventListener('mousemove', utils.throttle((e) => {
                    if (CONFIG.reducedMotion) return;

                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;

                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;

                    const rotateX = (y - centerY) / 10;
                    const rotateY = (centerX - x) / 10;

                    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
                }, 16));

                card.addEventListener('mouseleave', () => {
                    card.style.transform = '';
                });
            });
        }

        setupCopyButtons() {
            // Ajouter des boutons de copie aux blocs de code
            document.querySelectorAll('pre code').forEach(block => {
                const button = document.createElement('button');
                button.className = 'copy-button';
                button.innerHTML = '📋';
                button.title = 'Copier le code';

                button.addEventListener('click', () => {
                    navigator.clipboard.writeText(block.textContent).then(() => {
                        button.innerHTML = '✅';
                        button.style.background = 'var(--luna-success)';
                        setTimeout(() => {
                            button.innerHTML = '📋';
                            button.style.background = '';
                        }, 2000);
                    });
                });

                block.parentElement.style.position = 'relative';
                block.parentElement.appendChild(button);
            });
        }

        setupProgressIndicator() {
            const progressBar = document.createElement('div');
            progressBar.className = 'reading-progress';
            document.body.appendChild(progressBar);

            window.addEventListener('scroll', utils.throttle(() => {
                const scrollTop = window.pageYOffset;
                const docHeight = document.documentElement.scrollHeight - window.innerHeight;
                const scrollPercent = (scrollTop / docHeight) * 100;

                progressBar.style.width = `${scrollPercent}%`;
            }, 16));
        }

        setupSearchEnhancement() {
            const searchInput = document.querySelector('.md-search__input');
            if (searchInput) {
                searchInput.addEventListener('input', utils.debounce((e) => {
                    const query = e.target.value.toLowerCase();
                    this.highlightSearchTerms(query);
                }, 300));
            }
        }

        highlightSearchTerms(query) {
            if (!query) {
                document.querySelectorAll('.search-highlight').forEach(el => {
                    el.classList.remove('search-highlight');
                });
                return;
            }

            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null,
                false
            );

            const textNodes = [];
            let node;
            while (node = walker.nextNode()) {
                if (node.textContent.toLowerCase().includes(query)) {
                    textNodes.push(node);
                }
            }

            textNodes.forEach(textNode => {
                const parent = textNode.parentNode;
                if (parent.classList.contains('search-highlight')) return;

                const regex = new RegExp(`(${query})`, 'gi');
                const highlighted = textNode.textContent.replace(regex, '<mark class="search-highlight">$1</mark>');

                if (highlighted !== textNode.textContent) {
                    const span = document.createElement('span');
                    span.innerHTML = highlighted;
                    textNode.parentNode.replaceChild(span, textNode);
                }
            });
        }
    }

    // ================================
    // PERFORMANCE ET OPTIMISATION
    // ================================
    class PerformanceOptimizer {
        constructor() {
            this.init();
        }

        init() {
            this.setupLazyLoading();
            this.setupImageOptimization();
            this.setupResourceHints();
        }

        setupLazyLoading() {
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.src;
                            img.classList.remove('lazy');
                            imageObserver.unobserve(img);
                        }
                    });
                });

                document.querySelectorAll('img[data-src]').forEach(img => {
                    imageObserver.observe(img);
                });
            }
        }

        setupImageOptimization() {
            // Optimiser les images SVG
            document.querySelectorAll('img[src$=".svg"]').forEach(img => {
                img.addEventListener('load', () => {
                    img.style.opacity = '1';
                });
            });
        }

        setupResourceHints() {
            // Ajouter des preload pour les ressources critiques
            const criticalResources = [
                '/assets/arkalia-luna-theme.css',
                '/assets/logo.svg'
            ];

            criticalResources.forEach(resource => {
                const link = document.createElement('link');
                link.rel = 'preload';
                link.href = resource;
                link.as = resource.endsWith('.css') ? 'style' : 'image';
                document.head.appendChild(link);
            });
        }
    }

    // ================================
    // ANALYTICS ET MÉTRIQUES
    // ================================
    class Analytics {
        constructor() {
            this.init();
        }

        init() {
            this.trackPageViews();
            this.trackUserInteractions();
            this.trackPerformance();
        }

        trackPageViews() {
            // Envoyer une vue de page
            this.sendEvent('page_view', {
                page: window.location.pathname,
                title: document.title
            });
        }

        trackUserInteractions() {
            // Tracker les clics sur les liens importants
            document.querySelectorAll('.quick-link, .module-card').forEach(element => {
                element.addEventListener('click', () => {
                    this.sendEvent('link_click', {
                        element: element.className,
                        text: element.textContent.trim().substring(0, 50)
                    });
                });
            });
        }

        trackPerformance() {
            // Mesurer les métriques de performance
            window.addEventListener('load', () => {
                if ('performance' in window) {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    this.sendEvent('performance', {
                        loadTime: perfData.loadEventEnd - perfData.loadEventStart,
                        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart
                    });
                }
            });
        }

        sendEvent(eventName, data) {
            // Envoyer les événements (peut être connecté à Google Analytics ou autre)
            console.log('Analytics Event:', eventName, data);

            // Exemple d'envoi à Google Analytics 4
            if (typeof gtag !== 'undefined') {
                gtag('event', eventName, data);
            }
        }
    }

    // ================================
    // INITIALISATION
    // ================================
    class ArkaliaEnhancements {
        constructor() {
            this.modules = [];
            this.init();
        }

        init() {
            // Attendre que le DOM soit prêt
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.start());
            } else {
                this.start();
            }
        }

        start() {
            console.log('🌙 Arkalia-LUNA Enhancements v2.8.0 - Initialisation...');

            // Initialiser tous les modules
            this.modules = [
                new ThemeManager(),
                new EntranceAnimations(),
                new EnhancedNavigation(),
                new AdvancedInteractions(),
                new PerformanceOptimizer(),
                new Analytics()
            ];

            // Ajouter les styles CSS pour les animations
            this.injectStyles();

            console.log('✅ Arkalia-LUNA Enhancements initialisés avec succès');
        }

        injectStyles() {
            const styles = `
                /* Animations d'entrée */
                .animate-ready {
                    opacity: 0;
                    transform: translateY(30px);
                    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .animate-in {
                    opacity: 1;
                    transform: translateY(0);
                }

                /* Animation de la hero section */
                .hero-section {
                    opacity: 0;
                    transform: scale(0.95);
                    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .hero-animate {
                    opacity: 1;
                    transform: scale(1);
                }

                /* Animation des titres */
                h1, h2, h3 {
                    opacity: 0;
                    transform: translateX(-20px);
                    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .title-animate {
                    opacity: 1;
                    transform: translateX(0);
                }

                /* Barre de progression de lecture */
                .reading-progress {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 0;
                    height: 3px;
                    background: var(--luna-gradient);
                    z-index: 9999;
                    transition: width 0.1s ease;
                }

                /* Bouton de copie */
                .copy-button {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: var(--luna-surface);
                    border: 1px solid var(--luna-border);
                    border-radius: 4px;
                    padding: 5px 8px;
                    cursor: pointer;
                    font-size: 14px;
                    transition: all 0.2s ease;
                    z-index: 10;
                }

                .copy-button:hover {
                    background: var(--luna-primary);
                    color: white;
                }

                /* Mise en surbrillance de recherche */
                .search-highlight {
                    background: var(--luna-warning);
                    color: white;
                    padding: 2px 4px;
                    border-radius: 3px;
                }

                /* Images lazy loading */
                img.lazy {
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }

                /* Responsive pour les animations */
                @media (prefers-reduced-motion: reduce) {
                    .animate-ready,
                    .hero-section,
                    h1, h2, h3 {
                        opacity: 1;
                        transform: none;
                        transition: none;
                    }
                }
            `;

            const styleSheet = document.createElement('style');
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        }
    }

    // Démarrer les améliorations
    new ArkaliaEnhancements();

})();
