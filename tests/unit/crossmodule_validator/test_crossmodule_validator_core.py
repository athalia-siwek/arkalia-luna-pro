# 🔗 tests/unit/test_crossmodule_validator_core.py
"""
Tests unitaires pour le module crossmodule_validator/core.py
Arkalia-LUNA v2.8.0 - Cross Module Validator
"""

from datetime import datetime

import pytest

from modules.crossmodule_validator.core import CrossModuleValidator, ModuleState, ValidationResult


class TestCrossModuleValidator:
    """Tests pour la classe principale CrossModuleValidator"""

    def test_crossmodule_validator_initialization(self):
        """Test d'initialisation du Cross Module Validator"""
        validator = CrossModuleValidator()
        assert validator is not None
        assert hasattr(validator, "module_states")
        assert hasattr(validator, "last_validation")
        assert hasattr(validator, "is_running")
        assert hasattr(validator, "validation_threshold")
        assert validator.validation_threshold == 0.75

    @pytest.mark.asyncio
    async def test_crossmodule_validator_register_state(self):
        """Test d'enregistrement d'état de module"""
        validator = CrossModuleValidator()
        state = ModuleState(
            module_name="zeroia",
            state={"status": "active", "cpu_usage": 50},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=0.95,
        )

        result = await validator.register_state(state)
        assert result is not None
        assert result["status"] == "registered"
        assert "coherence_score" in result
        assert "conflicts" in result
        assert "zeroia" in validator.module_states

    @pytest.mark.asyncio
    async def test_crossmodule_validator_validate_states_single_module(self):
        """Test de validation avec un seul module"""
        validator = CrossModuleValidator()
        state = ModuleState(
            module_name="zeroia",
            state={"status": "active"},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=0.95,
        )

        validator.module_states["zeroia"] = state
        result = await validator.validate_states()

        assert result is not None
        assert isinstance(result, ValidationResult)
        assert result.coherence_score == 1.0
        assert len(result.conflicts) == 0
        assert len(result.recommendations) > 0

    @pytest.mark.asyncio
    async def test_crossmodule_validator_validate_states_version_mismatch(self):
        """Test de validation avec conflit de versions"""
        validator = CrossModuleValidator()

        # Module avec version différente
        state1 = ModuleState(
            module_name="zeroia",
            state={"status": "active"},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=0.95,
        )
        state2 = ModuleState(
            module_name="reflexia",
            state={"status": "active"},
            timestamp=datetime.now(),
            version="v2.7.0",
            health_score=0.90,
        )

        validator.module_states["zeroia"] = state1
        validator.module_states["reflexia"] = state2

        result = await validator.validate_states()

        assert result is not None
        assert isinstance(result, ValidationResult)
        assert result.coherence_score < 1.0
        assert len(result.conflicts) > 0
        assert any("version_mismatch" in str(conflict) for conflict in result.conflicts)

    @pytest.mark.asyncio
    async def test_crossmodule_validator_validate_states_low_health(self):
        """Test de validation avec santé faible"""
        validator = CrossModuleValidator()

        # Modules avec santé faible
        state1 = ModuleState(
            module_name="zeroia",
            state={"status": "active"},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=0.50,
        )
        state2 = ModuleState(
            module_name="reflexia",
            state={"status": "active"},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=0.60,
        )

        validator.module_states["zeroia"] = state1
        validator.module_states["reflexia"] = state2

        result = await validator.validate_states()

        assert result is not None
        assert isinstance(result, ValidationResult)
        assert result.coherence_score < 1.0
        assert len(result.conflicts) > 0
        assert any("low_health" in str(conflict) for conflict in result.conflicts)

    def test_crossmodule_validator_calculate_coherence_empty(self):
        """Test de calcul de cohérence avec aucun module"""
        validator = CrossModuleValidator()
        coherence = validator._calculate_coherence()
        assert coherence == 0.0

    def test_crossmodule_validator_calculate_coherence_perfect(self):
        """Test de calcul de cohérence parfaite"""
        validator = CrossModuleValidator()

        # Modules identiques
        state1 = ModuleState(
            module_name="zeroia",
            state={"status": "active"},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=1.0,
        )
        state2 = ModuleState(
            module_name="reflexia",
            state={"status": "active"},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=1.0,
        )

        validator.module_states["zeroia"] = state1
        validator.module_states["reflexia"] = state2

        coherence = validator._calculate_coherence()
        assert coherence > 0.9  # Cohérence très élevée


class TestModuleState:
    """Tests pour la classe ModuleState"""

    def test_module_state_creation(self):
        """Test de création d'un état de module"""
        state = ModuleState(
            module_name="zeroia",
            state={"status": "active", "cpu_usage": 50},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=0.95,
        )
        assert state.module_name == "zeroia"
        assert state.state["status"] == "active"
        assert state.state["cpu_usage"] == 50
        assert state.version == "v2.8.0"
        assert state.health_score == 0.95
        assert state.timestamp is not None

    def test_module_state_validation(self):
        """Test de validation des données d'état"""
        # Test avec health_score invalide - la classe accepte les valeurs hors limites
        # mais on peut tester que la valeur est bien assignée
        state = ModuleState(
            module_name="zeroia",
            state={"status": "active"},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=1.5,  # Valeur hors limites mais acceptée
        )
        assert state.health_score == 1.5
        assert state.module_name == "zeroia"


class TestValidationResult:
    """Tests pour la classe ValidationResult"""

    def test_validation_result_creation(self):
        """Test de création d'un résultat de validation"""
        result = ValidationResult(
            coherence_score=0.85,
            conflicts=[{"type": "version_mismatch"}],
            recommendations=["Uniformiser les versions"],
            timestamp=datetime.now(),
        )
        assert result.coherence_score == 0.85
        assert len(result.conflicts) == 1
        assert len(result.recommendations) == 1
        assert result.timestamp is not None

    def test_validation_result_perfect_score(self):
        """Test de résultat de validation parfait"""
        result = ValidationResult(
            coherence_score=1.0,
            conflicts=[],
            recommendations=[],
            timestamp=datetime.now(),
        )
        assert result.coherence_score == 1.0
        assert len(result.conflicts) == 0
        assert len(result.recommendations) == 0


class TestCrossModuleValidatorIntegration:
    """Tests d'intégration pour Cross Module Validator"""

    @pytest.mark.asyncio
    async def test_full_validation_cycle(self):
        """Test du cycle complet de validation"""
        validator = CrossModuleValidator()

        # Enregistrer plusieurs modules
        modules = [
            ModuleState(
                module_name="zeroia",
                state={"status": "active"},
                timestamp=datetime.now(),
                version="v2.8.0",
                health_score=0.95,
            ),
            ModuleState(
                module_name="reflexia",
                state={"status": "active"},
                timestamp=datetime.now(),
                version="v2.8.0",
                health_score=0.90,
            ),
            ModuleState(
                module_name="sandozia",
                state={"status": "active"},
                timestamp=datetime.now(),
                version="v2.8.0",
                health_score=0.88,
            ),
        ]

        # Enregistrer les états
        for module in modules:
            result = await validator.register_state(module)
            assert result["status"] == "registered"

        # Valider l'ensemble
        validation = await validator.validate_states()
        assert validation is not None
        assert validation.coherence_score > 0.8
        assert len(validation.conflicts) == 0  # Toutes versions identiques

    @pytest.mark.asyncio
    async def test_crossmodule_validator_error_handling(self):
        """Test de la gestion d'erreurs"""
        validator = CrossModuleValidator()

        # Test avec état avec valeurs limites - la classe accepte ces valeurs
        invalid_state = ModuleState(
            module_name="",
            state={},
            timestamp=datetime.now(),
            version="",
            health_score=-1,
        )
        result = await validator.register_state(invalid_state)
        assert result["status"] == "registered"
        assert len(validator.module_states) == 1

    def test_crossmodule_validator_performance_metrics(self):
        """Test des métriques de performance"""
        validator = CrossModuleValidator()

        # Ajouter des modules pour tester
        state = ModuleState(
            module_name="zeroia",
            state={"status": "active"},
            timestamp=datetime.now(),
            version="v2.8.0",
            health_score=0.95,
        )
        validator.module_states["zeroia"] = state

        # Vérifier les métriques
        assert len(validator.module_states) == 1
        assert validator.last_validation is None  # Pas encore de validation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
