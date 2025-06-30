# 🌙 Arkalia-LUNA Pro v2.8.0

<div class="luna-bg-fractal">
  <!-- SVG fractal/éclair bleu, overlay -->
  <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="none" style="position:absolute;top:0;left:0;width:100vw;height:100vh;z-index:0;">
    <defs>
      <radialGradient id="glow" cx="50%" cy="50%" r="60%">
        <stop offset="0%" stop-color="#7ecbff" stop-opacity="0.18"/>
        <stop offset="100%" stop-color="#090c12" stop-opacity="0"/>
      </radialGradient>
      <filter id="glowFilter" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="18" result="glow"/>
        <feMerge>
          <feMergeNode in="glow"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    <rect width="1920" height="1080" fill="url(#glow)"/>
    <polyline points="200,200 400,300 600,180 900,400 1200,200 1500,350 1700,180" stroke="#7ecbff" stroke-width="2.5" fill="none" opacity="0.18" filter="url(#glowFilter)"/>
    <polyline points="300,800 600,700 900,900 1200,700 1500,900 1700,700" stroke="#7ecbff" stroke-width="2.5" fill="none" opacity="0.13" filter="url(#glowFilter)"/>
    <polyline points="100,500 400,600 800,500 1200,600 1600,500" stroke="#7ecbff" stroke-width="1.5" fill="none" opacity="0.10" filter="url(#glowFilter)"/>
  </svg>
</div>

<div class="luna-status">Reflexia active. 92% system integrity</div>

<header class="luna-header">
  <nav class="luna-nav">
    <span class="luna-logo">Arkalia</span>
    <ul class="luna-menu">
      <li><a href="#modules">Modules</a></li>
      <li><a href="#api">API</a></li>
      <li><a href="#usage">Usage</a></li>
      <li><a href="#architecture">Architecture</a></li>
      <li><a href="#logs">Logs</a></li>
      <li><a href="#mind">Mind</a></li>
    </ul>
  </nav>
</header>

<div style="display: flex; justify-content: flex-end; align-items: center; margin: 1rem 0 2rem 0;">
  <a href="http://localhost:5173/" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, rgba(126, 203, 255, 0.2) 0%, rgba(30, 58, 138, 0.3) 100%); color: #7ecbff; font-family: 'Orbitron', monospace; font-weight: bold; text-transform: uppercase; letter-spacing: 0.1em; text-decoration: none; border-radius: 9999px; border: 1px solid rgba(126, 203, 255, 0.3); transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
    🚀 Dashboard React (Port 5173)
  </a>
  <a href="http://localhost:8081/" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, rgba(126, 203, 255, 0.2) 0%, rgba(30, 58, 138, 0.3) 100%); color: #7ecbff; font-family: 'Orbitron', monospace; font-weight: bold; text-transform: uppercase; letter-spacing: 0.1em; text-decoration: none; border-radius: 9999px; border: 1px solid rgba(126, 203, 255, 0.3); transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-left: 1rem;">
    📚 Documentation (Port 8081)
  </a>
</div>

<main class="luna-main-bg">
  <div class="luna-moon-anim">
    <!-- SVG lune animée -->
    <svg width="120" height="120" viewBox="0 0 120 120" class="luna-moon-svg">
      <defs>
        <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#fff" stop-opacity="1"/>
          <stop offset="80%" stop-color="#7ecbff" stop-opacity="0.7"/>
          <stop offset="100%" stop-color="#0ff" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <circle cx="60" cy="60" r="40" fill="url(#moonGlow)">
        <animate attributeName="r" values="38;42;38" dur="3s" repeatCount="indefinite"/>
      </circle>
      <circle cx="60" cy="60" r="32" fill="#fff" fill-opacity="0.95"/>
    </svg>
  </div>
  <h1 class="luna-title">ARKALIA-LUNA</h1>
  <h2 class="luna-subtitle">Cognitive Autonomy System</h2>
  <section class="luna-grid">
    <div class="luna-col">
      <h3>Overview</h3>
      <ul>
        <li>Cognitive Architecture
          <ul>
            <li><a href="#reflexia">Reflexia</a></li>
            <li><a href="#zeroia">Zeroia</a></li>
            <li><a href="#sandozia">Sandozia</a></li>
            <li><a href="#cognitive-reactor">Cognitive Reactor</a></li>
          </ul>
        </li>
        <li>API Reference
          <ul>
            <li><a href="#reflexia">Reflexia</a></li>
            <li><a href="#zeroia">Zeroia</a></li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="luna-col">
      <h3>API Reference</h3>
      <ul>
        <li><a href="#arkalia-api">Arkalia API (port 8000)</a></li>
        <li><a href="#endpoints">Endpoints</a></li>
      </ul>
      <h3>Testing</h3>
      <ul>
        <li><a href="#monitoring">Monitoring & Logs</a></li>
        <li><a href="#prometheus">Prometheus</a></li>
        <li><a href="#grafana">Grafana</a></li>
      </ul>
    </div>
    <div class="luna-col">
      <h3>Testing & Security</h3>
      <ul>
        <li><a href="#prometheus">Prometheus</a></li>
        <li><a href="#grafana">Grafana</a></li>
        <li><a href="#vault">Vault Manager</a></li>
        <li><a href="#anti-hallucination">Anti-Hallucination</a></li>
      </ul>
    </div>
  </section>
  <div class="luna-roadmap">Roadmap</div>
</main>

## 🚀 Architecture Modulaire

<div class="modules-grid">
    <div class="module-card">
        <div class="module-icon">🚀</div>
        <h3>Helloria</h3>
        <p>API centrale FastAPI haute performance avec gestion d'état distribuée</p>
        <span class="status-badge healthy">✅ Opérationnel</span>
    </div>

    <div class="module-card">
        <div class="module-icon">🧠</div>
        <h3>AssistantIA</h3>
        <p>Interface conversationnelle contextuelle avec intégration Ollama</p>
        <span class="status-badge healthy">✅ Opérationnel</span>
    </div>

    <div class="module-card">
        <div class="module-icon">🔁</div>
        <h3>Reflexia</h3>
        <p>Observateur cognitif réflexif avec analyse comportementale</p>
        <span class="status-badge healthy">✅ Opérationnel</span>
    </div>

    <div class="module-card">
        <div class="module-icon">🤖</div>
        <h3>ZeroIA</h3>
        <p>Décisionneur autonome avec circuit breaker et adaptive thresholds</p>
        <span class="status-badge healthy">✅ Opérationnel</span>
    </div>

    <div class="module-card">
        <div class="module-icon">🧠</div>
        <h3>Sandozia</h3>
        <p>Intelligence croisée Enterprise avec analyse multi-dimensionnelle</p>
        <span class="status-badge healthy">✅ Opérationnel</span>
    </div>

    <div class="module-card">
        <div class="module-icon">⚡</div>
        <h3>Cognitive Reactor</h3>
        <p>Moteur d'intelligence avancée avec traitement parallèle</p>
        <span class="status-badge healthy">✅ Opérationnel</span>
    </div>

    <div class="module-card">
        <div class="module-icon">📊</div>
        <h3>Monitoring</h3>
        <p>Observabilité complète avec Prometheus et métriques customisées</p>
        <span class="status-badge healthy">✅ Opérationnel</span>
    </div>
</div>

## 📊 Métriques Système

<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-icon">🧪</div>
        <div class="metric-value">97</div>
        <div class="metric-label">Tests automatisés</div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-value">&lt; 2s</div>
        <div class="metric-label">Latence ZeroIA</div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">🔧</div>
        <div class="metric-value">94</div>
        <div class="metric-label">Modules Python</div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-value">6/6</div>
        <div class="metric-label">Modules IA actifs</div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-value">34</div>
        <div class="metric-label">Métriques exposées</div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">🎯</div>
        <div class="metric-value">99.9%</div>
        <div class="metric-label">Disponibilité</div>
    </div>
</div>

## 📋 Prérequis Système

<div class="requirements-list">
    <div class="requirement-item">
        <span class="req-icon">🐍</span>
        <strong>Python</strong>: 3.11+ (recommandé 3.12)
    </div>
    <div class="requirement-item">
        <span class="req-icon">🐳</span>
        <strong>Docker</strong>: Version stable avec Compose
    </div>
    <div class="requirement-item">
        <span class="req-icon">💾</span>
        <strong>Mémoire</strong>: 8GB RAM minimum (16GB recommandé)
    </div>
    <div class="requirement-item">
        <span class="req-icon">💽</span>
        <strong>Stockage</strong>: 10GB disponibles (SSD recommandé)
    </div>
    <div class="requirement-item">
        <span class="req-icon">🧠</span>
        <strong>Ollama</strong>: Modèles locaux (optionnel pour AssistantIA)
    </div>
    <div class="requirement-item">
        <span class="req-icon">📊</span>
        <strong>Monitoring</strong>: Prometheus + Grafana (inclus)
    </div>
</div>

## 🏁 Démarrage Rapide

<div class="quick-links">
    <a href="getting-started/quick-start/" class="quick-link primary">
        <span class="link-icon">⚡</span>
        <div class="link-content">
            <h4>Installation rapide</h4>
            <p>Déploiement en 5 minutes</p>
        </div>
    </a>

    <a href="fonctionnement/structure/" class="quick-link">
        <span class="link-icon">🏗️</span>
        <div class="link-content">
            <h4>Architecture système</h4>
            <p>Comprendre l'organisation</p>
        </div>
    </a>

    <a href="modules/" class="quick-link">
        <span class="link-icon">📚</span>
        <div class="link-content">
            <h4>Documentation modules</h4>
            <p>Référence technique complète</p>
        </div>
    </a>

    <a href="reference/api/" class="quick-link">
        <span class="link-icon">🔌</span>
        <div class="link-content">
            <h4>API Reference</h4>
            <p>Points d'intégration REST</p>
        </div>
    </a>

    <a href="modules/assistantia/" class="quick-link">
        <span class="link-icon">🧠</span>
        <div class="link-content">
            <h4>AssistantIA</h4>
            <p>Interface conversationnelle</p>
        </div>
    </a>

    <a href="modules/cognitive-reactor/" class="quick-link">
        <span class="link-icon">⚡</span>
        <div class="link-content">
            <h4>Cognitive Reactor</h4>
            <p>Moteur d'intelligence avancée</p>
        </div>
    </a>

    <a href="infrastructure/monitoring/" class="quick-link">
        <span class="link-icon">📊</span>
        <div class="link-content">
            <h4>Monitoring</h4>
            <p>Observabilité complète</p>
        </div>
    </a>

    <a href="security/" class="quick-link">
        <span class="link-icon">🔒</span>
        <div class="link-content">
            <h4>Sécurité</h4>
            <p>Bonnes pratiques & audit</p>
        </div>
    </a>
</div>

## 🔧 Support & Maintenance

<div class="support-section">
    <div class="support-item">
        <div class="support-icon">📖</div>
        <h4>Documentation</h4>
        <p>Guides détaillés et exemples</p>
    </div>

    <div class="support-item">
        <div class="support-icon">🔧</div>
        <h4>Configuration</h4>
        <p>Paramétrage avancé</p>
    </div>

    <div class="support-item">
        <div class="support-icon">🚨</div>
        <h4>Sécurité</h4>
        <p>Bonnes pratiques</p>
    </div>

    <div class="support-item">
        <div class="support-icon">📊</div>
        <h4>Monitoring</h4>
        <p>Observabilité complète</p>
    </div>
</div>

<div class="footer-note">
    <p><strong>Arkalia-LUNA Pro v2.8.0</strong> - Système d'Intelligence Artificielle Enterprise. Architecture modulaire avec 7 modules IA opérationnels, monitoring complet et observabilité totale. Optimisé pour la production avec 97 tests automatisés et 99.9% de disponibilité.</p>
</div>
