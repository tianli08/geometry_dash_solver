import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path

from pynput.keyboard import Controller, Key

from gameDetection import GameDetection


@dataclass
class TrainerConfig:
    profile_path: Path = Path("timing_profile.json")
    attempts: int = 50
    max_attempt_seconds: float = 60.0
    lead_time_before_death: float = 0.12
    nudge_seconds: float = 0.012
    append_window_seconds: float = 0.18
    poll_seconds: float = 0.005
    restart_threshold: float = 0.70


class TimingTrainer:
    def __init__(self, config: TrainerConfig) -> None:
        self.config = config
        self.detector = GameDetection()
        self.keyboard = Controller()
        self.jump_times: list[float] = []

    def load_profile(self) -> None:
        if not self.config.profile_path.exists():
            return
        raw = json.loads(self.config.profile_path.read_text())
        loaded = raw.get("jump_times_seconds", [])
        self.jump_times = sorted(float(v) for v in loaded if float(v) >= 0.0)
        print(f"loaded_profile jumps={len(self.jump_times)}", flush=True)

    def save_profile(self, best_survival: float, attempts_done: int) -> None:
        payload = {
            "jump_times_seconds": [round(v, 4) for v in self.jump_times],
            "best_survival_seconds": round(best_survival, 4),
            "attempts_done": attempts_done,
            "updated_at_epoch": time.time(),
        }
        self.config.profile_path.write_text(json.dumps(payload, indent=2))
        print(f"saved_profile path={self.config.profile_path}", flush=True)

    def wait_for_game(self) -> None:
        print("waiting_for_geometry_dash...", flush=True)
        while not GameDetection.is_geometry_dash_running():
            time.sleep(0.5)
        print("game_detected", flush=True)

    def _tap_jump(self) -> None:
        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)

    def run_attempt(self) -> float:
        jump_idx = 0
        death_time = self.config.max_attempt_seconds
        start = time.monotonic()

        while True:
            now = time.monotonic()
            elapsed = now - start
            if elapsed >= self.config.max_attempt_seconds:
                break

            while jump_idx < len(self.jump_times) and elapsed >= self.jump_times[jump_idx]:
                self._tap_jump()
                jump_idx += 1

            frame = self.detector.capture_frame()
            restart_match = self.detector.detect_restart_button(
                frame_bgr=frame,
                threshold=self.config.restart_threshold,
            )
            if restart_match.found and elapsed > 0.5:
                death_time = elapsed
                break

            time.sleep(self.config.poll_seconds)

        restarted = self.detector.click_restart_if_visible(
            timeout_seconds=2.0,
            threshold=self.config.restart_threshold,
        )
        if not restarted:
            self._tap_jump()
        time.sleep(0.35)
        return death_time

    def _adjust_schedule(self, death_time: float) -> None:
        if not self.jump_times:
            self.jump_times = [max(0.08, death_time - self.config.lead_time_before_death)]
            return

        nearest_before = -1
        for i, jump_time in enumerate(self.jump_times):
            if jump_time <= death_time:
                nearest_before = i
            else:
                break

        if nearest_before < 0:
            self.jump_times.insert(0, max(0.05, death_time - self.config.lead_time_before_death))
            return

        dt = death_time - self.jump_times[nearest_before]
        if dt > self.config.append_window_seconds:
            self.jump_times.append(max(0.08, death_time - self.config.lead_time_before_death))
        else:
            self.jump_times[nearest_before] = max(
                0.05,
                self.jump_times[nearest_before] - self.config.nudge_seconds,
            )

        self.jump_times = sorted(set(round(v, 4) for v in self.jump_times))

    def train(self) -> None:
        self.wait_for_game()
        self.load_profile()
        best_survival = 0.0

        print("training_started press Ctrl+C to stop", flush=True)
        for attempt in range(1, self.config.attempts + 1):
            death_time = self.run_attempt()
            improved = death_time > best_survival
            if improved:
                best_survival = death_time
            self._adjust_schedule(death_time)

            print(
                f"attempt={attempt} death_time={death_time:.3f}s "
                f"best={best_survival:.3f}s jumps={len(self.jump_times)}",
                flush=True,
            )
            self.save_profile(best_survival=best_survival, attempts_done=attempt)

    def replay_once(self) -> None:
        self.wait_for_game()
        self.load_profile()
        if not self.jump_times:
            print("profile_empty: run train mode first", flush=True)
            return

        print("replay_starts_in=3", flush=True)
        time.sleep(3.0)
        start = time.monotonic()
        for jump_time in self.jump_times:
            while (time.monotonic() - start) < jump_time:
                time.sleep(0.001)
            self._tap_jump()
        print("replay_complete", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Geometry Dash timing trainer/replayer")
    parser.add_argument("--mode", choices=["train", "replay"], default="train")
    parser.add_argument("--attempts", type=int, default=50)
    parser.add_argument("--profile", type=str, default="timing_profile.json")
    parser.add_argument("--max-attempt-seconds", type=float, default=60.0)
    parser.add_argument("--restart-threshold", type=float, default=0.70)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = TrainerConfig(
        profile_path=Path(args.profile),
        attempts=max(1, int(args.attempts)),
        max_attempt_seconds=max(5.0, float(args.max_attempt_seconds)),
        restart_threshold=min(0.99, max(0.1, float(args.restart_threshold))),
    )
    trainer = TimingTrainer(config)
    if args.mode == "train":
        trainer.train()
    else:
        trainer.replay_once()


if __name__ == "__main__":
    main()
