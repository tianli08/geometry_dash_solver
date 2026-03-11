from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time

import cv2
import numpy as np
import pyautogui


@dataclass
class RestartMatch:
    found: bool
    confidence: float
    center: tuple[int, int] | None


class GameDetection:
    def __init__(self) -> None:
        self.restart_templates = self._load_templates(
            ("./images/restart.png", "./images/restart2.png")
        )

    @staticmethod
    def _load_templates(paths: tuple[str, ...]) -> list[np.ndarray]:
        templates: list[np.ndarray] = []
        for path_str in paths:
            template = cv2.imread(str(Path(path_str)), cv2.IMREAD_GRAYSCALE)
            if template is not None:
                templates.append(template)
        return templates

    @staticmethod
    def is_geometry_dash_running() -> bool:
        result = subprocess.run(
            ["pgrep", "-if", "Geometry Dash"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0 and bool(result.stdout.strip())

    @staticmethod
    def capture_frame() -> np.ndarray:
        screenshot = pyautogui.screenshot()
        frame_rgb = np.array(screenshot)
        return cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    def detect_restart_button(self, frame_bgr: np.ndarray, threshold: float = 0.70) -> RestartMatch:
        if not self.restart_templates:
            return RestartMatch(False, 0.0, None)

        frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        best = RestartMatch(False, 0.0, None)
        for template in self.restart_templates:
            if template.shape[0] > frame_gray.shape[0] or template.shape[1] > frame_gray.shape[1]:
                continue
            result = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val < threshold or max_val <= best.confidence:
                continue
            h, w = template.shape[:2]
            center = (int(max_loc[0] + w / 2), int(max_loc[1] + h / 2))
            best = RestartMatch(True, float(max_val), center)
        return best

    def click_restart_if_visible(self, timeout_seconds: float = 2.0, threshold: float = 0.70) -> bool:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            frame = self.capture_frame()
            match = self.detect_restart_button(frame, threshold=threshold)
            if match.found and match.center:
                pyautogui.click(match.center[0], match.center[1])
                return True
            time.sleep(0.06)
        return False
