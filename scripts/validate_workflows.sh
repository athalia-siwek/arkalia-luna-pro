#!/bin/bash

# 🚀 Script de Validation Complète - Arkalia-LUNA Pro
# Valide tous les composants critiques de la CI/CD

set -e

echo "🌕 Validation Complète Arkalia-LUNA Pro"
echo "========================================"

# === 1. VALIDATION WORKFLOWS GITHUB ACTIONS ===
echo ""
echo "🔍 Validation des workflows GitHub Actions..."

WORKFLOWS=(
    ".github/workflows/ci.yml"
    ".github/workflows/deployment.yml"
    ".github/workflows/e2e-tests.yml"
    ".github/workflows/performance-tests.yml"
    ".github/workflows/documentation.yml"
)

for workflow in "${WORKFLOWS[@]}"; do
    if [ -f "$workflow" ]; then
        echo "✅ $workflow trouvé"
        # Validation YAML basique si actionlint n'est pas disponible
        if command -v actionlint > /dev/null 2>&1; then
            if actionlint "$workflow" > /dev/null 2>&1; then
                echo "✅ $workflow valide (actionlint)"
            else
                echo "❌ $workflow invalide (actionlint)"
                exit 1
            fi
        else
            # Validation YAML basique avec python
            if python3 -c "import yaml; yaml.safe_load(open('$workflow'))" > /dev/null 2>&1; then
                echo "✅ $workflow valide (YAML basique)"
            else
                echo "❌ $workflow invalide (YAML basique)"
                exit 1
            fi
        fi
    else
        echo "❌ $workflow manquant"
        exit 1
    fi
done

# === 2. VALIDATION DOCKERFILES ===
echo ""
echo "🔍 Validation des Dockerfiles critiques..."

DOCKERFILES=(
    "Dockerfile"
    "Dockerfile-reflexia"
    "Dockerfile.zeroia"
    "Dockerfile.assistantia"
    "Dockerfile.sandozia"
    "Dockerfile.generative-ai"
    "Dockerfile.cognitive-reactor"
    "Dockerfile.master"
)

for dockerfile in "${DOCKERFILES[@]}"; do
    if [ -f "$dockerfile" ]; then
        echo "✅ $dockerfile trouvé"
        # Validation basique (vérification que le fichier existe et contient FROM et CMD/ENTRYPOINT)
        echo "🔍 Validation basique pour $dockerfile..."
        if grep -q "FROM" "$dockerfile" && grep -q -E "(CMD|ENTRYPOINT)" "$dockerfile"; then
            echo "✅ $dockerfile valide (structure basique)"
        else
            echo "❌ $dockerfile invalide (structure basique)"
            exit 1
        fi
    else
        echo "❌ $dockerfile manquant"
        exit 1
    fi
done

# === 3. VALIDATION DOCKER-COMPOSE ===
echo ""
echo "🔍 Validation des fichiers docker-compose..."

COMPOSE_FILES=(
    "docker-compose.yml"
    "docker-compose.prod.yml"
    "docker-compose.master.yml"
)

for compose_file in "${COMPOSE_FILES[@]}"; do
    if [ -f "$compose_file" ]; then
        echo "✅ $compose_file trouvé"
        if python3 -c "import yaml; yaml.safe_load(open('$compose_file'))" > /dev/null 2>&1; then
            echo "✅ $compose_file valide (YAML)"
        else
            echo "❌ $compose_file invalide (YAML)"
            exit 1
        fi
    else
        echo "❌ $compose_file manquant"
        exit 1
    fi
done

# === 4. VALIDATION MKDOCS ===
echo ""
echo "🔍 Validation de la configuration MkDocs..."
if [ -f "mkdocs.yml" ]; then
    echo "✅ mkdocs.yml trouvé"
    if mkdocs build --strict > /dev/null 2>&1; then
        echo "✅ mkdocs.yml valide"
    else
        echo "❌ mkdocs.yml invalide - Vérification des erreurs..."
        mkdocs build --strict 2>&1 | head -20
        exit 1
    fi
else
    echo "❌ mkdocs.yml manquant"
    exit 1
fi

# === 5. VALIDATION SCRIPTS CRITIQUES ===
echo ""
echo "🔍 Validation des scripts critiques..."

SCRIPTS=(
    "scripts/ark-docker-dev.sh"
    "scripts/ark-performance-benchmark.py"
    "ark-test-full.sh"
    "ark-start.sh"
    "ark-fix-all.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "✅ $script trouvé"
        if [ -x "$script" ]; then
            echo "✅ $script exécutable"
        else
            echo "⚠️  $script non exécutable"
        fi
    else
        echo "❌ $script manquant"
        exit 1
    fi
done

# === 6. VALIDATION PYTHON ===
echo ""
echo "🔍 Validation de la configuration Python..."

PYTHON_FILES=(
    "pyproject.toml"
    "requirements.txt"
    "pytest.ini"
    "pytest-integration.ini"
)

for py_file in "${PYTHON_FILES[@]}"; do
    if [ -f "$py_file" ]; then
        echo "✅ $py_file trouvé"
    else
        echo "❌ $py_file manquant"
        exit 1
    fi
done

# === 7. VALIDATION YAML ===
echo ""
echo "🔍 Validation de la syntaxe YAML..."

YAML_FILES=(
    "mkdocs.yml"
    ".yamllint"
    "codecov.yml"
    ".pre-commit-config.yaml"
)

for yaml_file in "${YAML_FILES[@]}"; do
    if [ -f "$yaml_file" ]; then
        echo "✅ $yaml_file trouvé"
        if python -c "import yaml; yaml.safe_load(open('$yaml_file'))" > /dev/null 2>&1; then
            echo "✅ $yaml_file syntaxe valide"
        else
            echo "❌ $yaml_file syntaxe invalide"
            exit 1
        fi
    else
        echo "❌ $yaml_file manquant"
        exit 1
    fi
done

# === 8. VALIDATION FINALE ===
echo ""
echo "🎉 VALIDATION COMPLÈTE RÉUSSIE !"
echo "================================"
echo "✅ Tous les workflows GitHub Actions sont valides"
echo "✅ Tous les Dockerfiles critiques sont présents et valides"
echo "✅ Tous les fichiers docker-compose sont valides"
echo "✅ La configuration MkDocs est valide"
echo "✅ Tous les scripts critiques sont présents"
echo "✅ Toutes les configurations Python sont présentes"
echo "✅ Tous les fichiers YAML ont une syntaxe valide"
echo ""
echo "🚀 Le projet Arkalia-LUNA Pro est prêt pour la production !"
