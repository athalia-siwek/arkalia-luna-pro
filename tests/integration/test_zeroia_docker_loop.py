import shutil
import subprocess
import time

import pytest

# Vérifie si Docker est disponible
docker_available = shutil.which("docker") is not None


# Vérifie si un conteneur spécifique est actif
def is_container_running(name: str) -> bool:
    try:
        output = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Running}}", name]
        )
        return output.strip() == b"true"
    except subprocess.CalledProcessError:
        return False


@pytest.mark.skipif(shutil.which("docker") is None, reason="Docker not installed")
@pytest.mark.skipif(not docker_available, reason="Docker not available in CI")
@pytest.mark.skipif(
    not is_container_running("zeroia"), reason="ZeroIA not running in CI"
)
def test_zeroia_docker_loop_runs():
    # Laisse le temps à ZeroIA d'émettre les logs
    time.sleep(3)

    result = subprocess.run(
        ["docker", "logs", "zeroia"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "loop started" in result.stdout.lower(), (
        "Le conteneur ZeroIA ne semble pas avoir émis de décision.\n"
        f"Logs capturés:\n{result.stdout[:500] or '[aucun log]'}"
    )
