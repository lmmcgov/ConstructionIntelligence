"""
Gemini CLI execution wrapper.
"""

from __future__ import annotations

import subprocess


class GeminiCLIRunner:
    """
    Executes Gemini CLI prompts and returns responses.
    """

    def __init__(
        self,
        command: str = "gemini",
        timeout: int = 120,
    ) -> None:
        """
        Initialize Gemini CLI runner.

        Parameters
        ----------
        command:
            Gemini executable name or path.

        timeout:
            Maximum execution time in seconds.
        """

        self.command = command
        self.timeout = timeout

    def run(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to Gemini CLI.

        Returns
        -------
        str
            Raw Gemini response output.

        Raises
        ------
        RuntimeError
            If Gemini CLI execution fails.
        """

        try:
            result = subprocess.run(
                [
                    self.command,
                    prompt,
                ],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=True,
            )

        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                "Gemini CLI timed out."
            ) from exc

        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                "Gemini CLI failed.\n"
                f"stderr:\n{exc.stderr}"
            ) from exc

        return result.stdout