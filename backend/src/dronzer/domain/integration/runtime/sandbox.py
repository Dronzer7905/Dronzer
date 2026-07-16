import asyncio
import os
import tempfile

import structlog

logger = structlog.get_logger("dronzer.integration.runtime.sandbox")


class SandboxEngine:
    """
    Executes raw code (Python, JS, Shell) in an isolated environment.
    Prevents Agent LLMs from executing catastrophic server commands.

    In a true production environment, this should interface with Docker API
    or Firecracker microVMs. For this milestone, we provide a strict local
    subprocess fallback with timeouts.
    """

    def __init__(self, mode: str = "subprocess"):
        self.mode = mode  # 'subprocess', 'docker', 'firecracker'

    async def execute_python(
        self, code: str, timeout_seconds: int = 10
    ) -> tuple[str, str, int | None]:
        """
        Executes Python code in an isolated subprocess.
        Returns: (stdout, stderr, exit_code)
        """
        logger.debug("Executing Python code in Sandbox", mode=self.mode)

        # Create a temporary file for the script
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_path = f.name

        try:
            if self.mode == "subprocess":
                # Standard subprocess execution with timeout
                process = await asyncio.create_subprocess_exec(
                    "python",
                    temp_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(), timeout=timeout_seconds
                    )
                    return stdout.decode(), stderr.decode(), process.returncode
                except TimeoutError:
                    process.kill()
                    return "", "Execution timed out.", -1
            elif self.mode == "docker":
                # Pseudo: docker run --rm -v temp_path:/app/script.py python:3.9 python /app/script.py
                raise NotImplementedError("Docker sandbox mode requires daemon connection.")
            return "", f"Unknown mode {self.mode}", -1
        finally:
            os.remove(temp_path)

    async def execute_shell(
        self, command: str, timeout_seconds: int = 5
    ) -> tuple[str, str, int | None]:
        """
        Executes a shell command.
        WARNING: Highly dangerous if exposed to unprivileged agents.
        """
        logger.warning(f"Executing Shell command in Sandbox: {command}")

        if self.mode == "subprocess":
            process = await asyncio.create_subprocess_shell(
                command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout_seconds
                )
                return stdout.decode(), stderr.decode(), process.returncode
            except TimeoutError:
                process.kill()
                return "", "Execution timed out.", -1
        return "", f"Unknown mode {self.mode}", -1
