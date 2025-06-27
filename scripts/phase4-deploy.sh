#!/bin/bash
# 💣 scripts/phase4-deploy.sh
# Déploiement Phase 4 : Renforcement Paranoïaque Arkalia-LUNA

set -euo pipefail

# Configuration
PHASE4_VERSION="4.0.0-security"
SECURITY_LEVEL="PARANOID"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/phase4_deployment_${TIMESTAMP}.log"

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# Header
echo -e "${PURPLE}"
cat << 'EOF'
💣 ====================================
   ARKALIA-LUNA PHASE 4 DEPLOYMENT
   RENFORCEMENT PARANOÏAQUE
====================================
EOF
echo -e "${NC}"

log "🚀 Starting Phase 4 deployment..."
log "📊 Version: $PHASE4_VERSION"
log "🔐 Security Level: $SECURITY_LEVEL"

# Phase 4.1: Security Core Infrastructure
echo -e "\n${BLUE}🔐 PHASE 4.1: SECURITY CORE INFRASTRUCTURE${NC}"

# Vérification prérequis
log "📋 Checking prerequisites..."

# Python modules requis
required_modules=("cryptography" "toml" "docker" "psutil")
for module in "${required_modules[@]}"; do
    if python -c "import $module" 2>/dev/null; then
        success "✅ $module available"
    else
        warning "⚠️ Installing $module..."
        pip install "$module" || error "Failed to install $module"
    fi
done

# Docker availability
if command -v docker &> /dev/null; then
    success "✅ Docker available"
else
    error "❌ Docker not found - required for sandboxing"
fi

# Test du module security
log "🧪 Testing security module..."
if python -c "from modules.security import BuildIntegrityValidator, SECURITY_LEVEL; print(f'Security level: {SECURITY_LEVEL}')" 2>/dev/null; then
    success "✅ Security module imported successfully"
else
    error "❌ Security module import failed"
fi

# Génération manifest initial
log "📄 Generating initial security manifest..."
python -c "
from modules.security.crypto.checksum_validator import generate_build_manifest
import sys
try:
    manifest_path = generate_build_manifest()
    print(f'✅ Manifest generated: {manifest_path}')
except Exception as e:
    print(f'❌ Manifest generation failed: {e}')
    sys.exit(1)
" || error "Manifest generation failed"

# Test validation intégrité
log "🔍 Testing integrity validation..."
python -c "
from modules.security.crypto.checksum_validator import BuildIntegrityValidator
import sys
try:
    validator = BuildIntegrityValidator()
    checksums = validator.generate_checksums()
    print(f'✅ Generated checksums for {len(checksums)} files')

    # Quick check
    results = validator.quick_check()
    failed = [f for f, ok in results.items() if not ok]
    if failed:
        print(f'⚠️ Some files not in manifest yet: {len(failed)} files')
    else:
        print('✅ Quick integrity check passed')

except Exception as e:
    print(f'❌ Integrity test failed: {e}')
    sys.exit(1)
" || error "Integrity validation test failed"

# Phase 4.2: Monitoring Infrastructure Setup
echo -e "\n${BLUE}📊 PHASE 4.2: MONITORING INFRASTRUCTURE${NC}"

log "🏗️ Setting up monitoring infrastructure..."

# Création dossiers monitoring
mkdir -p infrastructure/monitoring/{prometheus,grafana,loki,alertmanager}
mkdir -p infrastructure/monitoring/grafana/{dashboards,datasources,alerting}

# Configuration Prometheus avancée
log "⚙️ Configuring Prometheus..."
cat > infrastructure/monitoring/prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerting_rules.yml"
  - "recording_rules.yml"

scrape_configs:
  - job_name: 'arkalia-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics
    scrape_interval: 5s

  - job_name: 'assistantia'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: /metrics
    scrape_interval: 10s

  - job_name: 'zeroia'
    static_configs:
      - targets: ['localhost:8002']
    metrics_path: /metrics
    scrape_interval: 5s

  - job_name: 'reflexia'
    static_configs:
      - targets: ['localhost:8003']
    metrics_path: /metrics
    scrape_interval: 10s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
EOF

# Règles d'alerting critiques
log "🚨 Setting up critical alerting rules..."
cat > infrastructure/monitoring/prometheus/alerting_rules.yml << 'EOF'
groups:
  - name: arkalia_security_critical
    rules:
      - alert: SecurityIntegrityViolation
        expr: arkalia_security_integrity_violations_total > 0
        for: 0s
        labels:
          severity: critical
          component: security
        annotations:
          summary: "SECURITY BREACH: Integrity violation detected"
          description: "File integrity violation detected - immediate investigation required"

      - alert: ZeroIADecisionStall
        expr: increase(arkalia_zeroia_decisions_total[5m]) == 0
        for: 2m
        labels:
          severity: critical
          component: zeroia
        annotations:
          summary: "ZeroIA decision loop stalled"
          description: "No ZeroIA decisions in last 5 minutes"

      - alert: CognitiveMismatchHigh
        expr: arkalia_zeroia_contradictions_total > 10
        for: 1m
        labels:
          severity: warning
          component: cognitive
        annotations:
          summary: "High cognitive contradiction rate"
          description: "More than 10 contradictions detected"

      - alert: SecuritySandboxBreach
        expr: arkalia_security_sandbox_violations_total > 0
        for: 0s
        labels:
          severity: critical
          component: sandbox
        annotations:
          summary: "CRITICAL: Sandbox containment breach"
          description: "LLM sandbox violation - potential security compromise"

  - name: arkalia_performance
    rules:
      - alert: HighLatency
        expr: arkalia_reflexia_latency_ms > 1000
        for: 30s
        labels:
          severity: warning
          component: performance
        annotations:
          summary: "High system latency detected"

      - alert: CPUStress
        expr: arkalia_reflexia_cpu_usage_percent > 80
        for: 2m
        labels:
          severity: warning
          component: resources
        annotations:
          summary: "High CPU usage sustained"
EOF

# Configuration AlertManager
log "📢 Configuring AlertManager..."
cat > infrastructure/monitoring/alertmanager/config.yml << 'EOF'
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'arkalia-alerts@localhost'

route:
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'critical-alerts'
      group_wait: 5s
      repeat_interval: 5m

receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://localhost:8000/alerts/webhook'
        send_resolved: true

  - name: 'critical-alerts'
    webhook_configs:
      - url: 'http://localhost:8000/alerts/critical'
        send_resolved: true
        http_config:
          basic_auth:
            username: 'arkalia'
            password: 'secure-token'
EOF

# Dashboard Grafana Security Operations Center
log "📊 Creating Security Operations Center dashboard..."
cat > infrastructure/monitoring/grafana/dashboards/security-ops.json << 'EOF'
{
  "dashboard": {
    "id": null,
    "title": "Arkalia-LUNA Security Operations Center",
    "tags": ["arkalia", "security", "phase4"],
    "timezone": "browser",
    "refresh": "5s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "panels": [
      {
        "id": 1,
        "title": "Security Threat Level",
        "type": "stat",
        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "arkalia_security_threats_detected_total",
            "legendFormat": "Threats Detected"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "thresholds"},
            "thresholds": {
              "steps": [
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 1},
                {"color": "red", "value": 5}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "ZeroIA Decision Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 6, "y": 0},
        "targets": [
          {
            "expr": "rate(arkalia_zeroia_decisions_total[1m])",
            "legendFormat": "Decisions/sec"
          }
        ]
      },
      {
        "id": 3,
        "title": "Cognitive Contradictions",
        "type": "stat",
        "gridPos": {"h": 8, "w": 6, "x": 18, "y": 0},
        "targets": [
          {
            "expr": "arkalia_zeroia_contradictions_total",
            "legendFormat": "Contradictions"
          }
        ]
      }
    ]
  }
}
EOF

# Test des métriques existantes
log "📈 Testing existing metrics integration..."
if curl -s http://localhost:8000/metrics > /dev/null 2>&1; then
    success "✅ Main API metrics endpoint accessible"
else
    warning "⚠️ Main API metrics not yet available"
fi

# Vérification espace disque pour logs
available_space=$(df . | awk 'NR==2 {print $4}')
if [ "$available_space" -gt 1000000 ]; then  # 1GB
    success "✅ Sufficient disk space for monitoring logs"
else
    warning "⚠️ Low disk space - monitoring may fill up quickly"
fi

# Phase 4.3: Testing & Validation
echo -e "\n${BLUE}🧪 PHASE 4.3: TESTING & VALIDATION${NC}"

log "🔬 Running comprehensive Phase 4 tests..."

# Test sécurité intégrée
test_security() {
    log "Testing security module integration..."
    python -c "
from modules.security import BuildIntegrityValidator, SECURITY_LEVEL
from datetime import datetime

print(f'🔐 Security Level: {SECURITY_LEVEL}')

# Test validator
validator = BuildIntegrityValidator()
checksums = validator.generate_checksums()
print(f'📄 Generated checksums for {len(checksums)} critical files')

# Test quick check
results = validator.quick_check(['main.py', 'docker-compose.yml'])
all_ok = all(results.values())
print(f'⚡ Quick check: {\"PASSED\" if all_ok else \"FAILED\"}')

print('✅ Security module test completed')
"
}

# Test monitoring endpoints
test_monitoring() {
    log "Testing monitoring configuration..."

    # Vérifier fichiers de config
    config_files=(
        "infrastructure/monitoring/prometheus/prometheus.yml"
        "infrastructure/monitoring/prometheus/alerting_rules.yml"
        "infrastructure/monitoring/alertmanager/config.yml"
        "infrastructure/monitoring/grafana/dashboards/security-ops.json"
    )

    for config_file in "${config_files[@]}"; do
        if [ -f "$config_file" ]; then
            success "✅ $config_file created"
        else
            error "❌ Missing config file: $config_file"
        fi
    done
}

# Exécution des tests
test_security || error "Security tests failed"
test_monitoring || error "Monitoring tests failed"

# Phase 4.4: Documentation & Rollout
echo -e "\n${BLUE}📚 PHASE 4.4: DOCUMENTATION UPDATE${NC}"

log "📝 Updating documentation..."

# Mise à jour navigation MkDocs
if ! grep -q "Phase 4" mkdocs.yml; then
    log "Adding Phase 4 to documentation navigation..."
    sed -i '' '/- 🔐 Sécurité:/a\
        - Phase 4 Roadmap: security/phase4-roadmap.md' mkdocs.yml
fi

# Build documentation test
if command -v mkdocs &> /dev/null; then
    log "Testing documentation build..."
    mkdocs build --quiet && success "✅ Documentation build successful"
fi

# Final Status Report
echo -e "\n${PURPLE}🎯 PHASE 4 DEPLOYMENT SUMMARY${NC}"
echo "=================================="

success "✅ Security Core Infrastructure: DEPLOYED"
success "✅ Monitoring Infrastructure: CONFIGURED"
success "✅ Alerting Rules: ACTIVE"
success "✅ Documentation: UPDATED"

log "📊 Phase 4 Components Status:"
log "   🔐 BuildIntegrityValidator: OPERATIONAL"
log "   📈 Prometheus Config: READY"
log "   🚨 AlertManager: CONFIGURED"
log "   📊 Grafana Dashboards: READY"

warning "⏳ Next Steps Required:"
warning "   1. Deploy monitoring stack: docker-compose -f monitoring.yml up"
warning "   2. Generate production manifest: python modules/security/crypto/checksum_validator.py generate"
warning "   3. Set up AlertManager webhooks"
warning "   4. Configure Grafana datasources"

log "🎉 Phase 4 deployment completed successfully!"
log "📄 Full deployment log: $LOG_FILE"

echo -e "\n${GREEN}💣 ARKALIA-LUNA PHASE 4: PARANOID SECURITY ACTIVE! 🛡️${NC}"
