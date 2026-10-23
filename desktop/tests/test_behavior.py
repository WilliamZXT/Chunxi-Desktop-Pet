import copy
import json
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from chunxi.config import load_config
from chunxi.state_machine import PetStateMachine, State


class BehaviorTests(unittest.TestCase):
    def make(self, **overrides):
        config = load_config()["behavior"]
        config.update(overrides)
        return PetStateMachine(config, 0.0, random.Random(23))

    def test_rest_then_sleep_and_slow_wake(self):
        pet = self.make()
        pet.tick(pet.loaf_after+0.01)
        self.assertEqual(pet.state, State.LOAF)
        pet.tick(pet.sleep_after+0.01)
        self.assertEqual(pet.state, State.SLEEPING)
        now = pet.sleep_after+1
        pet.activity(now)
        self.assertEqual(pet.state, State.WAKING)
        pet.activity(now+0.2)  # Continuous movement must not restart waking forever.
        pet.tick(now+1.6)
        self.assertEqual(pet.state, State.SITTING)
        self.assertGreater(pet.next_blink, now+1.6)

    def test_input_prevents_unwanted_sleep(self):
        pet = self.make()
        for now in range(1, 2000):
            pet.activity(now)
            pet.tick(now)
            self.assertEqual(pet.state, State.SITTING)

    def test_click_probability_and_cooldown(self):
        pet = self.make(click_probability=1)
        self.assertTrue(pet.click(1))
        first_deadline = pet.next_click
        self.assertFalse(pet.click(1.1))
        self.assertEqual(first_deadline, pet.next_click)
        pet = self.make(click_probability=0)
        self.assertFalse(pet.click(1))
        self.assertGreater(pet.next_click, 1)

    def test_probability_is_not_always_response(self):
        pet = self.make()
        answers = []
        for n in range(100):
            pet.action = None
            answers.append(pet.click(n*100))
        self.assertTrue(any(answers))
        self.assertFalse(all(answers))

    def test_nearby_cursor_does_not_spin_head(self):
        pet = self.make(look_probability=1)
        pet.next_look = 0
        pet.proximity(1, True, 4)
        self.assertEqual(pet.action, "look")
        self.assertEqual(pet.look_direction, 4)
        for now in (2, 3, 4):
            pet.proximity(now, True, 12)
            self.assertEqual(pet.look_direction, 4)
        pet.proximity(5, False, 0)
        pet.proximity(6, True, 12)
        self.assertEqual(pet.look_direction, 4)  # Cooldown still applies.

    def test_drag_never_causes_sleep(self):
        pet = self.make()
        pet.drag_start(1)
        pet.tick(1000)
        self.assertEqual(pet.state, State.DRAGGING)
        self.assertEqual(pet.clip_key, "neutral")
        pet.drag_end(1001)
        self.assertEqual(pet.state, State.SITTING)
        self.assertIsNone(pet.action)

    def test_sleep_does_not_wave_on_waking_click(self):
        pet = self.make(click_probability=1)
        pet.tick(1000)
        self.assertFalse(pet.click(1001))
        self.assertEqual(pet.state, State.WAKING)

    def test_randomized_blink_and_ear_intervals(self):
        pet = self.make()
        blinks, ears = [], []
        for i in range(1, 36000):
            now = i*0.1
            pet.activity(now)
            previous = pet.action
            pet.tick(now)
            if pet.action != previous:
                if pet.action == "blink": blinks.append(now)
                elif pet.action == "ear": ears.append(now)
        self.assertGreater(len(blinks), 90)
        self.assertGreater(len(ears), 15)
        self.assertLess(len(ears), len(blinks))
        gaps = [round(b-a, 1) for a, b in zip(blinks, blinks[1:])]
        self.assertGreater(len(set(gaps)), 10)
        self.assertGreaterEqual(min(gaps), 12)

    def test_pause_resume_resets_idle(self):
        pet = self.make()
        pet.set_paused(True, 1)
        pet.tick(10000)
        self.assertEqual(pet.state, State.SITTING)
        pet.set_paused(False, 10001)
        pet.tick(10002)
        self.assertEqual(pet.state, State.SITTING)

    def test_bad_config_rejected(self):
        from chunxi.config import validate_config
        data = load_config()
        data['behavior']['sleep_after_seconds'] = [1, 2]
        with self.assertRaises(ValueError):
            validate_config(data)

    def test_repeated_click_feedback_can_be_skipped_without_other_cooldowns(self):
        from unittest.mock import patch
        pet = self.make(click_probability=1)
        pet._last_click_action = 'blink'
        before = (pet.next_blink, pet.next_ear, pet.next_look)
        with patch.object(pet.rng, 'choice', return_value='blink'), patch.object(pet.rng, 'random', return_value=0):
            self.assertFalse(pet.click(1))
        self.assertGreater(pet.next_click, 1)
        self.assertEqual((pet.next_blink, pet.next_ear, pet.next_look), before)
        self.assertIsNone(pet.action)

    def test_resume_reschedules_all_cooldowns(self):
        pet = self.make()
        pet.set_paused(True, 1)
        pet.set_paused(False, 10000)
        self.assertTrue(all(deadline > 10000 for deadline in (pet.next_blink, pet.next_ear, pet.next_look, pet.next_click)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
