import unittest
from types import SimpleNamespace
import numpy as np

from environment import observation_encoder

class EncoderTests(unittest.TestCase):
    
    def test_empty_move_list(self):
        battle = SimpleNamespace(active_pokemon=SimpleNamespace(current_hp_fraction=0.5),
                                    opponent_active_pokemon=SimpleNamespace(current_hp_fraction=0.8),
                                    available_moves=[])
        observation = observation_encoder.encode_battle(battle)
        expected = [0.5, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        np.testing.assert_allclose(observation, expected)

    def test_two_moves_aligned_correctly(self):
        move_a = SimpleNamespace(base_power=80)
        move_b = SimpleNamespace(base_power=120)
        battle = SimpleNamespace(active_pokemon=SimpleNamespace(current_hp_fraction=0.5),
                                    opponent_active_pokemon=SimpleNamespace(current_hp_fraction=0.8, damage_multiplier=lambda move: 2.0 if move is move_a else 0.5),
                                    available_moves=[move_a, move_b])
        observation = observation_encoder.encode_battle(battle)
        expected = [0.5, 0.8, 0.4, 0.6, 0.0, 0.0, 0.5, 0.125, 0.0, 0.0]
        np.testing.assert_allclose(observation, expected)