import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from agents.observation_agent import first_legal_policy, ObservationAgent

class PolicyTests(unittest.TestCase):

    def test_skips_unavailable_slot_and_chooses_first_legal(self):
        
        action_mask = [False, True, True, False]
        slot = first_legal_policy(None, action_mask)

        self.assertIs(type(slot), int)
        self.assertEqual(slot, 1)
    
    def test_return_zero_when_legal(self):

        action_mask = [True, True, False, False]
        slot = first_legal_policy(None, action_mask)

        self.assertIs(type(slot), int)
        self.assertEqual(slot, 0)
    
    def test_no_legal_moves(self):

        action_mask = [False, False, False, False]

        self.assertRaises(ValueError, first_legal_policy, None, action_mask)


class ObservationAgentTests(unittest.TestCase):

    def test_choose_move_uses_policy(self):

        move_a = SimpleNamespace(base_power=0)
        move_b = SimpleNamespace(base_power=120)
        battle = SimpleNamespace(
            active_pokemon=SimpleNamespace(current_hp_fraction=0.75),
            opponent_active_pokemon=None,
            available_moves=[move_a, move_b],
        )

        policy = Mock(return_value=1)

        agent = ObservationAgent(policy=policy, start_listening=False)
        expected_order = object()

        with patch.object(agent, "create_order", return_value=expected_order) as create_order:

            actual_order = agent.choose_move(battle)

        policy.assert_called_once()
        observation, action_mask = policy.call_args.args

        self.assertEqual(action_mask, [True, True, False, False])
        create_order.assert_called_once_with(move_b)
        self.assertIs(actual_order, expected_order)

    def test_choose_move_uses_fallback_without_calling_policy(self):
        
        battle = SimpleNamespace(available_moves=[])

        policy = Mock()
        expected_order = object()

        agent = ObservationAgent(policy=policy, start_listening=False)
        
        with patch.object(agent, "choose_random_move", return_value=expected_order) as fallback:

            actual_order = agent.choose_move(battle)
        
        fallback.assert_called_once_with(battle)
        policy.assert_not_called()
        self.assertIs(actual_order, expected_order)

    def test_choose_move_rejects_invalid_policy_slot(self):

        move_a = SimpleNamespace(base_power=0)
        move_b = SimpleNamespace(base_power=120)
        battle = SimpleNamespace(active_pokemon=SimpleNamespace(current_hp_fraction=0.75),
                                opponent_active_pokemon=None,
                                available_moves=[move_a, move_b]
            )

        policy = Mock(return_value=3)

        agent = ObservationAgent(policy=policy, start_listening=False)

        with patch.object(agent, "create_order") as create_order:
            self.assertRaises(ValueError, agent.choose_move, battle)

        create_order.assert_not_called()

    def test_choose_move_rejects_negative_indices(self):
        move_a = SimpleNamespace(base_power=0)
        move_b = SimpleNamespace(base_power=120)
        battle = SimpleNamespace(active_pokemon=SimpleNamespace(current_hp_fraction=0.75),
                                opponent_active_pokemon=None,
                                available_moves=[move_a, move_b]
            )

        policy = Mock(return_value=-1)

        agent = ObservationAgent(policy=policy, start_listening=False)

        with patch.object(agent, "create_order") as create_order:
            self.assertRaises(ValueError, agent.choose_move, battle)
            
        create_order.assert_not_called()