"""Pure, monotonic-time FSM. No Qt, OS calls or artwork mutation here."""
from __future__ import annotations

import logging
import random
from enum import Enum

log = logging.getLogger(__name__)


class State(str, Enum):
    SITTING = "sitting"
    LOAF = "loaf"
    SLEEPING = "sleeping"
    WAKING = "waking"
    DRAGGING = "dragging"


class PetStateMachine:
    def __init__(self, behavior: dict, now: float, rng: random.Random | None = None):
        self.config = behavior
        self.rng = rng or random.Random()
        self.state = State.SITTING
        self.state_since = self.last_activity = now
        self.action: str | None = None
        self.action_until = now
        self.look_direction = 0
        self.paused = False
        self.frequency_multiplier = 1.0
        self.frequency = 'normal'
        self._near = False
        self._sample_rest_thresholds()
        self.next_blink = now + self._delay("blink_interval_seconds")
        self.next_ear = now + self._delay("ear_interval_seconds")
        self.next_look = now + self._delay("look_cooldown_seconds")
        self.next_click = now
        self._last_click_action = None

    def _delay(self, key: str) -> float:
        value = self.rng.uniform(*self.config[key])
        if key in ("blink_interval_seconds", "ear_interval_seconds", "look_cooldown_seconds", "click_cooldown_seconds"):
            value *= self.frequency_multiplier
        return value

    def set_frequency(self, frequency: str, now: float):
        self.frequency = frequency
        self.frequency_multiplier = {"quiet": 1.5, "normal": 1.0, "more": 0.8}[frequency]
        self.next_blink = now+self._delay("blink_interval_seconds")
        self.next_ear = now+self._delay("ear_interval_seconds")
        self.next_look = now+self._delay("look_cooldown_seconds")
        self.next_click = max(self.next_click, now+self._delay("click_cooldown_seconds"))

    def _sample_rest_thresholds(self):
        self.loaf_after = self._delay("loaf_after_seconds")
        self.sleep_after = self._delay("sleep_after_seconds")

    def _state(self, state: State, now: float):
        if state != self.state:
            log.info("state %s -> %s", self.state.value, state.value)
            self.state, self.state_since = state, now
            self.action = None

    def _start_action(self, action: str, now: float, duration: float):
        self.action, self.action_until = action, now + duration
        log.info("action %s", action)

    def activity(self, now: float):
        self.last_activity = now
        if not self.paused and self.state in (State.LOAF, State.SLEEPING):
            self._state(State.WAKING, now)
            self._sample_rest_thresholds()

    def click(self, now: float) -> bool:
        was_resting = self.state in (State.LOAF, State.SLEEPING, State.WAKING)
        self.activity(now)
        if self.paused or was_resting or self.state != State.SITTING or self.action or now < self.next_click:
            return False
        # Even a non-response consumes the opportunity, preventing click-spam farming.
        self.next_click = now + self._delay("click_cooldown_seconds")
        if self.rng.random() >= self.config["click_probability"]:
            return False
        action = self.rng.choice(("wave", "blink", "blink"))
        # Skip some repeated click responses instead of adding more movement.
        # A skipped response still consumes only the click's own cooldown.
        if action == self._last_click_action and self.rng.random() < 0.5:
            return False
        self._last_click_action = action
        self._start_action(action, now, 1.8 if action == "wave" else 1.15)
        if action == 'blink':
            self.next_blink = now + self._delay('blink_interval_seconds')
        return True

    def proximity(self, now: float, near: bool, direction: int):
        entered = near and not self._near
        self._near = near
        if not entered or self.paused or self.state != State.SITTING or self.action or now < self.next_look:
            return
        self.next_look = now + self._delay("look_cooldown_seconds")
        if self.rng.random() < self.config["look_probability"]:
            self.look_direction = direction % 16
            self._start_action("look", now, self.rng.uniform(1.4, 2.4))

    def drag_start(self, now: float):
        self.last_activity = now
        self._state(State.DRAGGING, now)

    def drag_end(self, now: float):
        self.last_activity = now
        self._state(State.SITTING, now)
        self.next_blink = now + self._delay("blink_interval_seconds")

    def set_paused(self, value: bool, now: float):
        self.paused = value
        self.action = None
        if not value:
            self.last_activity = now
            self._state(State.SITTING, now)
            self.set_frequency(self.frequency, now)

    def tick(self, now: float):
        if self.paused or self.state == State.DRAGGING:
            return
        if self.action and now >= self.action_until:
            self.action = None
        if self.state == State.WAKING:
            if now - self.state_since >= self.config["wake_seconds"]:
                self._state(State.SITTING, now)
                self.last_activity = now
                self.next_blink = now + self._delay("blink_interval_seconds")
                self.next_ear = now + self._delay("ear_interval_seconds")
            return
        idle = now - self.last_activity
        if idle >= self.sleep_after:
            self._state(State.SLEEPING, now)
        elif idle >= self.loaf_after:
            self._state(State.LOAF, now)
        if self.state not in (State.SITTING, State.LOAF) or self.action:
            return
        if now >= self.next_blink:
            if self.state == State.SITTING:
                self._start_action("blink", now, 1.15)
            self.next_blink = now + self._delay("blink_interval_seconds")
        elif now >= self.next_ear:
            if self.state == State.SITTING:
                self._start_action("ear", now, 0.95)
            self.next_ear = now + self._delay("ear_interval_seconds")

    @property
    def clip_key(self) -> str:
        if self.state == State.DRAGGING:
            return "neutral"
        return self.action or {
            State.SITTING: "breathing", State.LOAF: "loaf",
            State.SLEEPING: "sleep", State.WAKING: "wake",
        }[self.state]
