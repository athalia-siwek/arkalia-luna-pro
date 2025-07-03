# 📦 Makefile Arkalia IA Devstation

.PHONY: all test format bump patch minor major zeroia

all: test

test:
	bash ./ark-test-full.sh

format:
	black .
	ruff check . --fix

bump:
	bumpver update

patch:
	bumpver update --patch

minor:
	bumpver update --minor

major:
	bumpver update --major

zeroia:
	@echo "🔁 [Make] ZeroIA full check"
	@docker ps -a | grep zeroia
	@docker inspect zeroia --format="Status: {{.State.Status}} | Restarting: {{.State.Restarting}}"
	@docker logs zeroia --tail 30
	@ruff modules/zeroia/ --fix
	@black modules/zeroia/
	@pytest tests/unit/test_state_writer.py
	@ls -lh modules/zeroia/state/zeroia_state.toml
	@ls -lh state/zeroia_dashboard.json
	@echo "✅ [Make] Fin ZeroIA full check"
