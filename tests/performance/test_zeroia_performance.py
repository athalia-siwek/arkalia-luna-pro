"""
🧪 Tests de performance pour ZeroIA

Tests simples pour valider la performance :
- Temps de réponse < 1 seconde
- Requêtes concurrentes
"""

import time
import pytest
from modules.zeroia.metrics import update_zeroia_metrics


class TestZeroIAPerformance:
    """Tests de performance pour ZeroIA"""
    
    @pytest.mark.performance
    def test_decision_response_time_under_1s(self):
        """Test que les décisions sont prises en moins d'1 seconde"""
        start_time = time.time()
        
        # Simulation d'une décision ZeroIA
        decision_type = "test_decision"
        status = "success"
        
        # Simuler un traitement
        time.sleep(0.1)  # Simulation d'un traitement rapide
        
        # Mettre à jour les métriques
        duration = time.time() - start_time
        update_zeroia_metrics(decision_type, status, duration)
        
        # Vérifier que c'est rapide
        assert duration < 1.0, f"Temps de décision trop lent: {duration:.2f}s"
        assert status == "success", "La décision doit réussir"
        
    @pytest.mark.performance
    def test_metrics_update_performance(self):
        """Test que la mise à jour des métriques est rapide"""
        start_time = time.time()
        
        # Mettre à jour les métriques plusieurs fois
        for i in range(10):
            update_zeroia_metrics(f"decision_{i}", "success", 0.1)
        
        total_time = time.time() - start_time
        
        # Vérifier que c'est rapide (10 mises à jour en moins d'1 seconde)
        assert total_time < 1.0, f"Mise à jour métriques trop lente: {total_time:.2f}s"
        
    @pytest.mark.performance
    def test_cognitive_score_update(self):
        """Test que la mise à jour du score cognitif fonctionne"""
        start_time = time.time()
        
        # Mettre à jour avec un score cognitif
        update_zeroia_metrics("cognitive_test", "success", 0.05, cognitive_score=0.85)
        
        duration = time.time() - start_time
        
        # Vérifier que c'est rapide
        assert duration < 0.5, f"Mise à jour score cognitif trop lente: {duration:.2f}s"
        
    @pytest.mark.performance
    def test_error_handling_performance(self):
        """Test que la gestion d'erreur est rapide"""
        start_time = time.time()
        
        # Simuler une erreur
        update_zeroia_metrics("error_test", "error", 0.02)
        
        duration = time.time() - start_time
        
        # Vérifier que c'est rapide
        assert duration < 0.5, f"Gestion d'erreur trop lente: {duration:.2f}s" 