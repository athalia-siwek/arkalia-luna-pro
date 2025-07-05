"""Module de métriques Prometheus pour Arkalia-LUNA"""

<<<<<<< HEAD
from core.ark_logger import ark_logger
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
=======
from typing import Optional
>>>>>>> dev-migration

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram


class ArkaliaMetrics:
    """Classe de gestion des métriques Prometheus"""

    def __init__(self, registry: CollectorRegistry | None = None) -> None:
        # Utiliser le registre fourni ou créer un nouveau
        self._registry = registry or CollectorRegistry()

        # Métriques système
        self.arkalia_system_uptime = Gauge(
            "arkalia_system_uptime",
            "Temps d'activité du système en secondes",
            registry=self._registry,
        )

        self.arkalia_cpu_usage = Gauge(
            "arkalia_cpu_usage", "Utilisation CPU en pourcentage", registry=self._registry
        )

        self.arkalia_memory_usage = Gauge(
            "arkalia_memory_usage", "Utilisation mémoire en bytes", registry=self._registry
        )

        # Métriques des modules
        self.arkalia_modules_status = Gauge(
            "arkalia_modules_status",
            "Statut des modules (1=actif, 0=inactif)",
            ["module_name"],
            registry=self._registry,
        )

        # Métriques des requêtes
        self.arkalia_requests_total = Counter(
            "arkalia_requests_total",
            "Nombre total de requêtes",
            ["method", "endpoint", "status"],
            registry=self._registry,
        )

        self.arkalia_request_duration = Histogram(
            "arkalia_request_duration",
            "Durée des requêtes en secondes",
            ["method", "endpoint"],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
            registry=self._registry,
        )

<<<<<<< HEAD
        # === MÉTRIQUES INFO ===
        self.system_info = Info("arkalia_system_info", "Informations système Arkalia")

        # Variables internes
        self.start_time = time.time()
        self.last_reflexia_status = None

        # Initialisation des infos système
        self._update_system_info()

    def _update_system_info(self):
        """Met à jour les informations système"""
        try:
            # Cache TOML Enhanced - 94.8% performance boost
            from modules.utils_enhanced.cache_enhanced import load_toml_cached

            version_info = load_toml_cached("version.toml")
            current_version = version_info.get("current_version", "unknown")
        except Exception:
            current_version = "unknown"

        self.system_info.info(
            {
                "version": current_version,
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "modules": "zeroia,reflexia,assistantia,helloria",
                "security_features": "io_safe,prompt_validation,docker_hardening",
            }
        )

    # === COLLECTEURS ZEROIA ===

    def record_zeroia_decision(self, decision: str, confidence: float):
        """Enregistre une décision ZeroIA"""
        # Classifie le niveau de confiance
        if confidence >= 0.8:
            confidence_level = "high"
        elif confidence >= 0.5:
            confidence_level = "medium"
        else:
            confidence_level = "low"

        self.zeroia_decisions.labels(
            decision_type=decision, confidence_level=confidence_level
        ).inc()

        self.zeroia_confidence.set(confidence)

    def record_zeroia_loop_duration(self, duration: float):
        """Enregistre la durée d'un loop ZeroIA"""
        self.zeroia_loop_duration.observe(duration)

    def record_zeroia_contradiction(self):
        """Enregistre une contradiction ZeroIA"""
        self.zeroia_contradictions.inc()

    def update_zeroia_state_health(self, is_healthy: bool):
        """Met à jour l'état de santé des fichiers ZeroIA"""
        self.zeroia_state_health.set(1 if is_healthy else 0)

    # === COLLECTEURS REFLEXIA ===

    def update_reflexia_metrics(self, cpu: float, ram: float, latency: float):
        """Met à jour les métriques ReflexIA"""
        self.reflexia_cpu_usage.set(cpu)
        self.reflexia_ram_usage.set(ram)
        self.reflexia_latency.set(latency)
        self.reflexia_monitoring_cycles.inc()

    def record_reflexia_status_change(self, from_status: str, to_status: str):
        """Enregistre un changement de statut ReflexIA"""
        if from_status != to_status:
            self.reflexia_status_changes.labels(from_status=from_status, to_status=to_status).inc()

        self.last_reflexia_status = to_status

    # === COLLECTEURS ASSISTANTIA ===

    def record_assistantia_prompt(self, status: str, security_level: str):
        """Enregistre un prompt traité par AssistantIA"""
        self.assistantia_prompts_processed.labels(
            status=status, security_level=security_level
        ).inc()

    def record_assistantia_security_block(self, reason: str, pattern_type: str):
        """Enregistre un blocage sécurité AssistantIA"""
        self.assistantia_security_blocks.labels(
            block_reason=reason, pattern_type=pattern_type
        ).inc()

    def record_assistantia_response_time(self, duration: float):
        """Enregistre le temps de réponse AssistantIA"""
        self.assistantia_response_time.observe(duration)

    def record_assistantia_rate_limit(self):
        """Enregistre un rate limit AssistantIA"""
        self.assistantia_rate_limits.inc()

    # === COLLECTEURS GLOBAUX ===

    def record_file_operation(self, operation: str, file_type: str, status: str):
        """Enregistre une opération de fichier"""
        self.file_operations.labels(operation=operation, file_type=file_type, status=status).inc()

    def record_api_request(self, endpoint: str, method: str, status_code: int):
        """Enregistre une requête API"""
        self.api_requests.labels(
            endpoint=endpoint, method=method, status_code=str(status_code)
        ).inc()

    def record_error(self, module: str, error_type: str, severity: str):
        """Enregistre une erreur système"""
        self.error_count.labels(module=module, error_type=error_type, severity=severity).inc()

    def update_system_uptime(self):
        """Met à jour le temps de fonctionnement"""
        uptime = time.time() - self.start_time
        self.arkalia_system_uptime.set(uptime)


class ArkaliaMetricsCollector:
    """Collecteur automatique de métriques depuis les fichiers état"""

    def __init__(self, metrics: ArkaliaMetrics) -> None:
        self.metrics = metrics
        self.state_paths = {
            "zeroia_state": Path("modules/zeroia/state/zeroia_state.toml"),
            "reflexia_state": Path("state/reflexia_state.toml"),
            "global_context": Path("state/global_context.toml"),
            "zeroia_dashboard": Path("state/zeroia_dashboard.json"),
        }

    def collect_all_metrics(self):
        """Collecte toutes les métriques disponibles"""
        self.collect_zeroia_metrics()
        self.collect_reflexia_metrics()
        self.collect_system_metrics()

    def collect_zeroia_metrics(self):
        """Collecte les métriques ZeroIA depuis les fichiers état"""
        try:
            # Dashboard ZeroIA
            dashboard_path = self.state_paths["zeroia_dashboard"]
            if dashboard_path.exists():
                with open(dashboard_path) as f:
                    dashboard = json.load(f)

                # Dernière décision
                last_decision = dashboard.get("last_decision", "unknown")
                confidence = dashboard.get("confidence", 0.0)
                if last_decision != "unknown":
                    self.metrics.record_zeroia_decision(last_decision, confidence)

            # État TOML ZeroIA
            state_path = self.state_paths["zeroia_state"]
            if state_path.exists():
                try:
                    state_data = toml.load(state_path)
                    self.metrics.update_zeroia_state_health(True)

                    # Informations de décision
                    decision_info = state_data.get("decision", {})
                    if decision_info:
                        decision = decision_info.get("last_decision", "unknown")
                        confidence = decision_info.get("confidence_score", 0.0)
                        if decision != "unknown":
                            self.metrics.record_zeroia_decision(decision, confidence)

                except (toml.TomlDecodeError, Exception):
                    self.metrics.update_zeroia_state_health(False)
                    self.metrics.record_error("zeroia", "state_corruption", "high")

        except Exception:
            self.metrics.record_error("zeroia", "metrics_collection", "medium")

    def collect_reflexia_metrics(self):
        """Collecte les métriques ReflexIA"""
        try:
            state_path = self.state_paths["reflexia_state"]
            if state_path.exists():
                state_data = toml.load(state_path)

                # Métriques système
                metrics_data = state_data.get("metrics", {})
                if metrics_data:
                    cpu = metrics_data.get("cpu", 0.0)
                    ram = metrics_data.get("ram", 0.0)
                    latency = metrics_data.get("latency", 0.0)

                    self.metrics.update_reflexia_metrics(cpu, ram, latency)

                # Statut
                status = state_data.get("status", "unknown")
                if self.metrics.last_reflexia_status:
                    self.metrics.record_reflexia_status_change(
                        self.metrics.last_reflexia_status, status
                    )
                self.metrics.last_reflexia_status = status

        except Exception:
            self.metrics.record_error("reflexia", "metrics_collection", "medium")

    def collect_system_metrics(self):
        """Collecte les métriques système globales"""
        # Uptime
        self.metrics.update_system_uptime()

        # Vérification santé fichiers critiques
        critical_files = [
            "utils/io_safe.py",
            "modules/assistantia/security/prompt_validator.py",
            "modules/zeroia/reason_loop.py",
            "modules/reflexia/core.py",
        ]

        for file_path in critical_files:
            path = Path(file_path)
            if path.exists() and path.stat().st_size > 100:
                self.metrics.record_file_operation("health_check", "critical", "success")
            else:
                self.metrics.record_file_operation("health_check", "critical", "failure")
                self.metrics.record_error("system", "missing_critical_file", "critical")


class PrometheusServer:
    """Serveur HTTP Prometheus pour exposition des métriques"""

    def __init__(self, port: int = 8001, host: str = "localhost") -> None:
        self.port = port
        self.host = host
        self.metrics = ArkaliaMetrics()
        self.collector = ArkaliaMetricsCollector(self.metrics)
        self.server_started = False

    def start_server(self):
        """Démarre le serveur de métriques Prometheus"""
        if not self.server_started:
            start_http_server(self.port, addr=self.host)
            self.server_started = True
            ark_logger.info(f"🔥 Serveur métriques Prometheus démarré sur {self.host}:{self.port}", extra={"module": "monitoring"})
            ark_logger.info(f"📊 Métriques disponibles: http://{self.host}:{self.port}/metrics", extra={"module": "monitoring"})

    def collect_and_expose(self):
        """Collecte les métriques et les expose"""
        if not self.server_started:
            self.start_server()

        # Collecte périodique
        self.collector.collect_all_metrics()

        return {
            "status": "active",
            "metrics_endpoint": f"http://{self.host}:{self.port}/metrics",
            "last_collection": datetime.now().isoformat(),
        }


# === UTILITAIRES D'INTÉGRATION ===


def get_metrics_summary() -> dict[str, str | int | float]:
    """Retourne un résumé des métriques pour API REST"""
    global prometheus_server
    if prometheus_server is None:
        prometheus_server = get_prometheus_server()
    metrics_instance = prometheus_server.metrics

    summary = {
        "timestamp": datetime.now().isoformat(),
        "zeroia": {},
        "reflexia": {},
        "system": {},
    }

    try:
        # ZeroIA
        dashboard_path = Path("state/zeroia_dashboard.json")
        if dashboard_path.exists():
            with open(dashboard_path) as f:
                dashboard = json.load(f)
            summary["zeroia"] = {
                "last_decision": dashboard.get("last_decision", "unknown"),
                "confidence": dashboard.get("confidence", 0.0),
                "active": dashboard.get("reasoning_loop_active", False),
            }

        # ReflexIA
        reflexia_path = Path("state/reflexia_state.toml")
        if reflexia_path.exists():
            reflexia_data = toml.load(reflexia_path)
            summary["reflexia"] = reflexia_data.get("metrics", {})

        # Système
        summary["system"] = {
            "uptime_hours": (time.time() - metrics_instance.start_time) / 3600,
            "critical_files_ok": all(
                Path(f).exists()
                for f in [
                    "utils/io_safe.py",
                    "modules/assistantia/security/prompt_validator.py",
                ]
            ),
        }

    except Exception as e:
        summary["error"] = str(e)

    return summary


# === INSTANCE GLOBALE ===
prometheus_server = None


def get_prometheus_server() -> PrometheusServer:
    """Retourne l'instance globale du serveur Prometheus"""
    global prometheus_server
    if prometheus_server is None:
        prometheus_server = PrometheusServer()
    return prometheus_server


def initialize_metrics() -> PrometheusServer:
    """Initialise le système de métriques Arkalia"""
    server = get_prometheus_server()
    server.start_server()
    ark_logger.info("📊 Système de métriques Arkalia-LUNA initialisé", extra={"module": "monitoring"})
    return server


if __name__ == "__main__":
    # Test standalone
    ark_logger.info("🔥 Test serveur métriques Prometheus Arkalia-LUNA", extra={"module": "monitoring"})

    server = PrometheusServer(port=8001)
    server.start_server()

    # Collecte de test
    metrics = server.metrics
    metrics.record_zeroia_decision("monitor", 0.75)
    metrics.update_reflexia_metrics(65.0, 45.0, 150.0)
    metrics.record_assistantia_prompt("processed", "medium")

    ark_logger.info("✅ Métriques de test enregistrées", extra={"module": "monitoring"})
    ark_logger.info("🌐 Accès: http://localhost:8001/metrics", extra={"module": "monitoring"})

    try:
        # Collecte continue (pour test)
        while True:
            server.collect_and_expose()
            ark_logger.info(f"📊 Collecte effectuée: {datetime.now(, extra={"module": "monitoring"})}")
            time.sleep(30)  # Collecte toutes les 30 secondes
    except KeyboardInterrupt:
        ark_logger.info("🛑 Arrêt du serveur de métriques", extra={"module": "monitoring"})
=======
    def get_registry(self) -> CollectorRegistry:
        """Retourne le registre de métriques"""
        return self._registry
>>>>>>> dev-migration
