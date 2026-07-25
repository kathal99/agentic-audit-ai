import docker
import time
from docker.errors import DockerException, APIError, ContainerError
from .config import CANARY_FILES, CANARY_CONTENT, DOCKER_IMAGE, SANDBOX_TIMEOUT, SANDBOX_MEMORY, SANDBOX_CPUS, MAX_LOG_LINES

class SandboxEngine:
    def __init__(self):
        self.client = docker.from_env()

    def create_container(self):
        try:
            container = self.client.containers.run(
                DOCKER_IMAGE,
                command="sleep 3600",
                detach=True,
                tty=True,
                stdin_open=True,
                network_disabled=True,
                mem_limit=SANDBOX_MEMORY,
                nano_cpus=int(SANDBOX_CPUS * 1e9),
                security_opt=["no-new-privileges"],
                cap_drop=["ALL"],
                labels={"ai_fight_club": "sandbox"},
            )
            self._seed_canaries(container)
            return container
        except (DockerException, APIError) as exc:
            raise RuntimeError(f"Sandbox creation failed: {exc}")

    def _seed_canaries(self, container):
        for path, content in CANARY_CONTENT.items():
            container.exec_run(["sh", "-c", f"mkdir -p $(dirname {path}) && cat > {path} <<'EOF'\n{content}EOF"], demux=True)

    def execute(self, container, command: str):
        try:
            result = container.exec_run(["sh", "-c", command], demux=True, stdout=True, stderr=True, timeout=SANDBOX_TIMEOUT)
            stdout = result.output[0].decode("utf-8", errors="replace") if result.output and result.output[0] else ""
            stderr = result.output[1].decode("utf-8", errors="replace") if result.output and result.output[1] else ""
            return stdout, stderr, result.exit_code
        except ContainerError as exc:
            return exc.stdout.decode("utf-8", errors="replace"), exc.stderr.decode("utf-8", errors="replace"), exc.exit_status
        except (DockerException, APIError) as exc:
            return "", f"Docker execution failed: {exc}", 1

    def cleanup(self, container):
        try:
            container.remove(force=True)
        except Exception:
            pass

    @staticmethod
    def trim_output(output: str, limit: int = MAX_LOG_LINES) -> str:
        lines = output.strip().splitlines()
        if len(lines) <= limit:
            return output.strip()
        return "\n".join(lines[:limit]) + "\n[...output truncated...]"
