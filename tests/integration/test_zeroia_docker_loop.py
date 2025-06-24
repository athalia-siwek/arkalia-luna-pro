import subprocess


def test_zeroia_docker_loop_runs():
    result = subprocess.run(
        ["docker", "logs", "zeroia"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert "ZeroIA decided:" in result.stdout
