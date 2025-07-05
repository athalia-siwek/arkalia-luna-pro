#!/usr/bin/env python3
"""
🔍 CrossModuleValidator Core - Validation croisée des modules IA
Assure la cohérence entre les différents modules du système
"""

# import asyncio
# import logging
from datetime import datetime
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModuleState(BaseModel):
    """État d'un module pour validation"""

    module_name: str
    state: dict
    timestamp: datetime
    version: str
    health_score: float


class ValidationResult(BaseModel):
    """Résultat de validation croisée"""

    coherence_score: float
    conflicts: list[dict]
    recommendations: list[str]
    timestamp: datetime


class CrossModuleValidator:
    """Validateur de cohérence inter-modules"""

    def __init__(self) -> None:
        self.module_states: dict[str, ModuleState] = {}
        self.last_validation: ValidationResult | None = None
        self.is_running = False
        self.validation_threshold = 0.75

    async def register_state(self, state: ModuleState) -> dict:
        """Enregistre l'état d'un module"""
        self.module_states[state.module_name] = state
        validation = await self.validate_states()
        return {
            "status": "registered",
            "coherence_score": validation.coherence_score,
            "conflicts": len(validation.conflicts),
        }

    async def validate_states(self) -> ValidationResult:
        """Effectue une validation croisée complète"""
        conflicts: list[Any] = []
        recommendations: list[Any] = []

        # Vérification basique de cohérence
        if len(self.module_states) < 2:
            return ValidationResult(
                coherence_score=1.0,
                conflicts=[],
                recommendations=["Pas assez de modules pour validation croisée"],
                timestamp=datetime.now(),
            )

        # Détection des conflits de version
        version_groups: dict[str, Any] = {}
        for name, state in self.module_states.items():
            if state.version not in version_groups:
                version_groups[state.version] = []
            version_groups[state.version].append(name)

        if len(version_groups) > 1:
            conflicts.append({"type": "version_mismatch", "details": version_groups})
            recommendations.append("Uniformiser les versions des modules")

        # Vérification santé globale
        health_scores = [s.health_score for s in self.module_states.values()]
        avg_health = sum(health_scores) / len(health_scores)
        if avg_health < self.validation_threshold:
            conflicts.append({"type": "low_health", "score": avg_health})
            recommendations.append(f"Score santé global faible: {avg_health:.2f}")

        # Calcul score cohérence
        coherence_score = self._calculate_coherence()

        # Création résultat
        result = ValidationResult(
            coherence_score=coherence_score,
            conflicts=conflicts,
            recommendations=recommendations,
            timestamp=datetime.now(),
        )

        self.last_validation = result
        return result

    def _calculate_coherence(self) -> float:
        """Calcule le score de cohérence global"""
        if not self.module_states:
            return 0.0

        # Facteurs de cohérence
        factors = {
            "health": 0.4,  # Santé des modules
            "versions": 0.3,  # Uniformité versions
            "timestamps": 0.3,  # Fraîcheur données
        }

        # Score santé
        health_scores = [s.health_score for s in self.module_states.values()]
        health_coherence = sum(health_scores) / len(health_scores)

        # Score versions
        versions = {s.version for s in self.module_states.values()}
        version_coherence = 1.0 if len(versions) == 1 else 0.5

        # Score timestamps
        timestamps = [s.timestamp for s in self.module_states.values()]
        max_diff = max((max(timestamps) - min(timestamps)).total_seconds(), 1)
        time_coherence = 1.0 if max_diff < 60 else 0.8  # 1 minute max

        # Score final pondéré
        return (
            health_coherence * factors["health"]
            + version_coherence * factors["versions"]
            + time_coherence * factors["timestamps"]
        )

    async def run_validation_loop(self):
        """Boucle principale de validation"""
        self.is_running = True
        logger.info("🔍 Démarrage boucle de validation")

        while self.is_running:
            try:
                validation = await self.validate_states()
                logger.info(
                    f"✅ Validation: score={validation.coherence_score:.2f}, "
                    f"conflits={len(validation.conflicts)}"
                )
                await asyncio.sleep(30)  # Validation toutes les 30 secondes
            except Exception as e:
                logger.error(f"❌ Erreur validation: {e}")
                await asyncio.sleep(5)


# FastAPI app
app = FastAPI(title="CrossModuleValidator API")
validator = CrossModuleValidator()


@app.post("/register")
async def register_module_state(state: ModuleState):
    """Enregistre l'état d'un module"""
    try:
        result = await validator.register_state(state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/validate")
async def get_validation():
    """Force une validation immédiate"""
    try:
        result = await validator.validate_states()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/status")
async def get_status():
    """État du validateur"""
    return {
        "status": "running" if validator.is_running else "stopped",
        "modules_registered": len(validator.module_states),
        "last_validation": (
            validator.last_validation.dict() if validator.last_validation else None
        ),
    }


if __name__ == "__main__":
    import uvicorn

    # Démarrer la boucle de validation en arrière-plan
    asyncio.create_task(validator.run_validation_loop())
    # Lancer l'API
    uvicorn.run(app, host="0.0.0.0", port=8016)
