# 🌙 Arkalia-LUNA Pro - Interface React

Interface moderne React avec Tailwind CSS pour le système IA Arkalia-LUNA Pro.

## 🚀 Installation

```bash
# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev

# Construire pour la production
npm run build

# Prévisualiser la build
npm run preview
```

## 🛠️ Technologies

- **React 18** - Interface utilisateur
- **Tailwind CSS** - Styling utilitaire
- **Vite** - Build tool rapide
- **React Router** - Navigation
- **Framer Motion** - Animations
- **Lucide React** - Icônes

## 📁 Structure

```
├── components/
│   └── ArkaliaLunaHomepage.jsx    # Page d'accueil principale
├── src/
│   ├── App.jsx                    # Composant principal
│   ├── main.jsx                   # Point d'entrée
│   └── index.css                  # Styles globaux
├── tailwind.config.js             # Configuration Tailwind
├── vite.config.js                 # Configuration Vite
├── package.json                   # Dépendances
└── index.html                     # Template HTML
```

## 🎨 Design System

### Couleurs

- `arkalia-black`: `#090c12` - Fond principal
- `neural-blue`: `#7ecbff` - Bleu neural
- `neural-cyan`: `#0ff` - Cyan cybernétique
- `slate-200`: `#e2e8f0` - Texte principal

### Polices

- **Orbitron** - Titres et navigation
- **Inter** - Texte principal
- **JetBrains Mono** - Code

### Animations

- `luna-glow` - Glow de la lune
- `lightning-pulse` - Éclairs du fond
- `moon-pulse` - Pulsation de la lune
- `neural-flicker` - Flicker neural

## 🔧 Configuration

### Tailwind CSS

Le fichier `tailwind.config.js` contient :

- Palette de couleurs personnalisée
- Animations CSS personnalisées
- Polices Google Fonts
- Utilitaires personnalisés

### Vite

Configuration optimisée pour :

- Hot reload rapide
- Build optimisé
- Alias de chemins
- PostCSS avec Tailwind

## 📱 Responsive

L'interface s'adapte automatiquement :

- **Desktop** : Grille 3 colonnes
- **Tablet** : Grille 2 colonnes
- **Mobile** : Grille 1 colonne

## 🎯 Fonctionnalités

### Page d'accueil

- ✅ Fond fractal animé
- ✅ Lune centrale pulsante
- ✅ Navigation horizontale
- ✅ Status bar système
- ✅ Grille de liens 3 colonnes
- ✅ Typographie premium
- ✅ Micro-interactions

### Animations

- ✅ Éclairs mouvants
- ✅ Glow bleu sur hover
- ✅ Transitions fluides
- ✅ Pulsations neurales

## 🚀 Déploiement

### Build de production

```bash
npm run build
```

### Serveur statique

```bash
npm run preview
```

### Docker (optionnel)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🔗 Intégration

L'interface React peut être intégrée avec :

- L'API FastAPI existante
- Le système de monitoring
- Les modules Arkalia
- La documentation MkDocs

## 📝 Scripts disponibles

- `npm run dev` - Serveur de développement
- `npm run build` - Build de production
- `npm run preview` - Prévisualisation
- `npm run lint` - Linting ESLint
- `npm run format` - Formatage Prettier

## 🎨 Personnalisation

### Ajouter une nouvelle page

1. Créer un composant dans `components/`
2. Ajouter la route dans `src/App.jsx`
3. Styliser avec les classes Tailwind

### Modifier les couleurs

Éditer `tailwind.config.js` dans la section `colors`

### Ajouter des animations

Définir dans `tailwind.config.js` sous `keyframes`

## 🔮 Roadmap

- [ ] Intégration API temps réel
- [ ] Dashboard interactif
- [ ] Thème sombre/clair
- [ ] Animations avancées
- [ ] PWA support
- [ ] Tests unitaires
- [ ] Documentation interactive

---

**Arkalia-LUNA Pro** - Système IA Cognitif Ultra-Protection
