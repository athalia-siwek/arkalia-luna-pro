import shutil
import subprocess

import pytest

docker_available = shutil.which("docker") is not None


def is_container_running(name: str) -> bool:
    try:
        output = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Running}}", name]
        )
        return output.strip() == b"true"
    except Exception:
        return False


@pytest.mark.skipif(not docker_available, reason="Docker not available in CI")
@pytest.mark.skipif(
    not is_container_running("zeroia"), reason="ZeroIA not running in CI"
)
def test_zeroia_docker_loop_runs():
    result = subprocess.run(
        ["docker", "logs", "zeroia"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert "ZeroIA decided:" in result.stdout
