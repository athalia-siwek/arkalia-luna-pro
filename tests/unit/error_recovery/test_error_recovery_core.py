# 🔄 tests/unit/test_error_recovery_core.py
"""
Tests unitaires pour le module error_recovery/core.py
Arkalia-LUNA v2.8.0 - Error Recovery System
"""

from datetime import datetime
from unittest.mock import patch

import pytest

from modules.error_recovery.core import (
    ErrorRecoverySystem,
    ModuleError,
    RecoveryAction,
    RecoveryResult,
)


class TestErrorRecoverySystem:
    """Tests pour la classe principale ErrorRecoverySystem"""

    def test_error_recovery_system_initialization(self) -> None:
        """Test d'initialisation du système de récupération d'erreurs"""
        recovery_system = ErrorRecoverySystem()
        assert recovery_system is not None
        assert hasattr(recovery_system, "active_errors")
        assert hasattr(recovery_system, "recovery_history")
        assert hasattr(recovery_system, "is_running")
        assert hasattr(recovery_system, "max_retries")
        assert recovery_system.max_retries == 3

    @pytest.mark.asyncio
    async def test_error_recovery_system_register_error(self):
        """Test d'enregistrement d'erreur"""
        recovery_system = ErrorRecoverySystem()
        error = ModuleError(
            module_name="zeroia",
            error_type="connection_lost",
            error_message="Connection timeout",
            timestamp=datetime.now(),
        )

        result = await recovery_system.register_error(error)
        assert result is not None
        assert "status" in result
        assert result["status"] in ["recovery_attempted", "error_registered"]

    def test_error_recovery_system_plan_recovery_action_connection_lost(self) -> None:
        """Test de planification d'action pour erreur de connexion"""
        recovery_system = ErrorRecoverySystem()
        error = ModuleError(
            module_name="zeroia",
            error_type="connection_lost",
            error_message="Connection timeout",
            timestamp=datetime.now(),
        )

        action = recovery_system._plan_recovery_action(error)
        assert action is not None
        assert action.action_type == "reconnect"
        assert action.module_name == "zeroia"
        assert action.priority == 2

    def test_error_recovery_system_plan_recovery_action_state_corrupted(self) -> None:
        """Test de planification d'action pour état corrompu"""
        recovery_system = ErrorRecoverySystem()
        error = ModuleError(
            module_name="reflexia",
            error_type="state_corrupted",
            error_message="State file corrupted",
            timestamp=datetime.now(),
        )

        action = recovery_system._plan_recovery_action(error)
        assert action is not None
        assert action.action_type == "restore_state"
        assert action.module_name == "reflexia"
        assert action.priority == 3

    def test_error_recovery_system_plan_recovery_action_deadlock(self) -> None:
        """Test de planification d'action pour deadlock"""
        recovery_system = ErrorRecoverySystem()
        error = ModuleError(
            module_name="sandozia",
            error_type="deadlock",
            error_message="Deadlock detected",
            timestamp=datetime.now(),
        )

        action = recovery_system._plan_recovery_action(error)
        assert action is not None
        assert action.action_type == "force_restart"
        assert action.module_name == "sandozia"
        assert action.priority == 1

    def test_error_recovery_system_plan_recovery_action_max_retries(self) -> None:
        """Test de planification d'action après max retries"""
        recovery_system = ErrorRecoverySystem()
        recovery_system.active_errors["zeroia"] = [
            ModuleError(
                module_name="zeroia",
                error_type="unknown",
                error_message="Unknown error",
                timestamp=datetime.now(),
            )
            for _ in range(3)
        ]

        error = ModuleError(
            module_name="zeroia",
            error_type="unknown",
            error_message="Another error",
            timestamp=datetime.now(),
        )

        action = recovery_system._plan_recovery_action(error)
        assert action is not None
        assert action.action_type == "restart"
        assert action.priority == 3

    @pytest.mark.asyncio
    async def test_error_recovery_system_execute_recovery_reconnect(self):
        """Test d'exécution de récupération - reconnexion"""
        recovery_system = ErrorRecoverySystem()
        action = RecoveryAction(
            module_name="zeroia",
            action_type="reconnect",
            parameters={},
            timestamp=datetime.now(),
            priority=2,
        )

        with patch("asyncio.sleep"):
            result = await recovery_system.execute_recovery(action)
            assert result is not None
            assert isinstance(result, RecoveryResult)
            assert result.success is True
            assert result.action == action
            assert result.error_fixed is True
            assert result.new_state == "recovered"

    @pytest.mark.asyncio
    async def test_error_recovery_system_execute_recovery_restart(self):
        """Test d'exécution de récupération - redémarrage"""
        recovery_system = ErrorRecoverySystem()
        action = RecoveryAction(
            module_name="zeroia",
            action_type="restart",
            parameters={"clean": True},
            timestamp=datetime.now(),
            priority=3,
        )

        with patch("asyncio.sleep"):
            result = await recovery_system.execute_recovery(action)
            assert result is not None
            assert isinstance(result, RecoveryResult)
            assert result.success is True
            assert result.action == action
            assert result.error_fixed is True
            assert result.new_state == "recovered"

    @pytest.mark.asyncio
    async def test_error_recovery_system_execute_recovery_error(self):
        """Test d'exécution de récupération avec erreur"""
        recovery_system = ErrorRecoverySystem()
        action = RecoveryAction(
            module_name="zeroia",
            action_type="invalid_action",
            parameters={},
            timestamp=datetime.now(),
            priority=1,
        )

        with patch("asyncio.sleep"):
            result = await recovery_system.execute_recovery(action)
            assert result is not None
            assert isinstance(result, RecoveryResult)
            assert result.success is False
            assert result.action == action
            assert result.error_fixed is False
            assert result.new_state == "failed"


class TestModuleError:
    """Tests pour la classe ModuleError"""

    def test_module_error_creation(self) -> None:
        """Test de création d'une erreur de module"""
        error = ModuleError(
            module_name="zeroia",
            error_type="connection_lost",
            error_message="Connection timeout",
            timestamp=datetime.now(),
        )
        assert error.module_name == "zeroia"
        assert error.error_type == "connection_lost"
        assert error.error_message == "Connection timeout"
        assert error.timestamp is not None

    def test_module_error_with_optional_fields(self) -> None:
        """Test de création d'erreur avec champs optionnels"""
        error = ModuleError(
            module_name="reflexia",
            error_type="state_corrupted",
            error_message="State file corrupted",
            timestamp=datetime.now(),
            stack_trace="Traceback...",
            context={"line": 42, "function": "process_data"},
        )
        assert error.stack_trace == "Traceback..."
        assert error.context["line"] == 42
        assert error.context["function"] == "process_data"


class TestRecoveryAction:
    """Tests pour la classe RecoveryAction"""

    def test_recovery_action_creation(self) -> None:
        """Test de création d'une action de récupération"""
        action = RecoveryAction(
            module_name="zeroia",
            action_type="reconnect",
            parameters={"timeout": 30},
            timestamp=datetime.now(),
            priority=2,
        )
        assert action.module_name == "zeroia"
        assert action.action_type == "reconnect"
        assert action.parameters["timeout"] == 30
        assert action.priority == 2

    def test_recovery_action_default_priority(self) -> None:
        """Test de création d'action avec priorité par défaut"""
        action = RecoveryAction(
            module_name="reflexia",
            action_type="restart",
            parameters={},
            timestamp=datetime.now(),
        )
        assert action.priority == 1  # Valeur par défaut


class TestRecoveryResult:
    """Tests pour la classe RecoveryResult"""

    def test_recovery_result_creation(self) -> None:
        """Test de création d'un résultat de récupération"""
        action = RecoveryAction(
            module_name="zeroia",
            action_type="reconnect",
            parameters={},
            timestamp=datetime.now(),
        )

        result = RecoveryResult(
            success=True,
            action=action,
            error_fixed=True,
            new_state="recovered",
            timestamp=datetime.now(),
        )
        assert result.success is True
        assert result.action == action
        assert result.error_fixed is True
        assert result.new_state == "recovered"


class TestErrorRecoveryIntegration:
    """Tests d'intégration pour Error Recovery"""

    @pytest.mark.asyncio
    async def test_full_error_recovery_cycle(self):
        """Test du cycle complet de récupération d'erreurs"""
        recovery_system = ErrorRecoverySystem()

        # Créer une erreur
        error = ModuleError(
            module_name="zeroia",
            error_type="connection_lost",
            error_message="Connection timeout",
            timestamp=datetime.now(),
        )

        # Enregistrer l'erreur
        with patch("asyncio.sleep"):
            result = await recovery_system.register_error(error)
            assert result["status"] == "recovery_attempted"
            assert result["success"] is True
            assert result["action"] == "reconnect"

    def test_error_recovery_system_error_tracking(self) -> None:
        """Test du suivi des erreurs"""
        recovery_system = ErrorRecoverySystem()

        # Ajouter des erreurs
        error1 = ModuleError(
            module_name="zeroia",
            error_type="connection_lost",
            error_message="Connection timeout",
            timestamp=datetime.now(),
        )
        error2 = ModuleError(
            module_name="reflexia",
            error_type="state_corrupted",
            error_message="State file corrupted",
            timestamp=datetime.now(),
        )

        recovery_system.active_errors["zeroia"] = [error1]
        recovery_system.active_errors["reflexia"] = [error2]

        assert len(recovery_system.active_errors) == 2
        assert len(recovery_system.active_errors["zeroia"]) == 1
        assert len(recovery_system.active_errors["reflexia"]) == 1

    def test_error_recovery_system_history_tracking(self) -> None:
        """Test du suivi de l'historique"""
        recovery_system = ErrorRecoverySystem()

        # Ajouter des résultats
        action = RecoveryAction(
            module_name="zeroia",
            action_type="reconnect",
            parameters={},
            timestamp=datetime.now(),
        )

        result = RecoveryResult(
            success=True,
            action=action,
            error_fixed=True,
            new_state="recovered",
            timestamp=datetime.now(),
        )

        recovery_system.recovery_history.append(result)
        assert len(recovery_system.recovery_history) == 1
        assert recovery_system.recovery_history[0] == result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
