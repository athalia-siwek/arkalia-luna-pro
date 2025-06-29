# 📊 Tests Event Store — Arkalia-LUNA

## Objectif
Tests unitaires pour le système de stockage et d'analyse d'événements ZeroIA.

## Structure
- `test_basic.py` : Tests de base (initialisation, ajout, récupération, filtrage)
- `test_analytics.py` : Tests d'analytics et de détection d'anomalies
- `test_export.py` : Tests d'export, persistance et fonctionnalités avancées

## Exécution rapide
```bash
pytest tests/unit/zeroia/event_store/
pytest tests/unit/zeroia/event_store/test_basic.py
pytest tests/unit/zeroia/event_store/test_analytics.py
```

## Marqueurs
- `@pytest.mark.performance` : Tests de performance
- `@pytest.mark.analytics` : Tests d'analytics

## Bonnes pratiques
- Utiliser des répertoires temporaires pour les tests
- Tester la persistance et la récupération
- Valider les métriques d'analytics
- Vérifier la détection d'anomalies

## Exemple de test
```python
import pytest
from modules.zeroia.event_store import EventStore, EventType

@pytest.fixture
def temp_event_store():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield EventStore(cache_dir=f"{temp_dir}/test_events")

def test_add_event(temp_event_store):
    event_id = temp_event_store.add_event(
        EventType.DECISION_MADE,
        {"decision": "monitor", "confidence": 0.8}
    )
    assert event_id.startswith("decision_made_")
```

## Conseil
Ces tests valident la fiabilité du système de stockage d'événements critique pour le monitoring. 