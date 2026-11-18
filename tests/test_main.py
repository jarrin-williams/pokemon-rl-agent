import unittest
from unittest.mock import AsyncMock, patch

import main


class MainTests(unittest.IsolatedAsyncioTestCase):

    async def test_main_awaits_runner_with_configured_count(self):
        with patch.object(main, "NUM_BATTLES", 7):
            with patch.object(main, "run_battles", new_callable=AsyncMock) as runner:
                await main.main()
                runner.assert_awaited_once_with(7, agent_type="type-aware")

    async def test_main_uses_explicit_battle_count(self):
        with patch.object(main, "run_battles", new_callable=AsyncMock) as runner:
            await main.main(3, agent_type="type-aware")

        runner.assert_awaited_once_with(3, agent_type="type-aware")
    
    async def test_main_forwards_correct_agent_to_runner(self):
        with patch.object(main, "run_battles", new_callable=AsyncMock) as runner:
            await main.main(3, agent_type="observation")
        
        runner.assert_awaited_once_with(3, agent_type="observation")

class PositiveIntTests(unittest.TestCase):
    
    def test_accepts_positive_integers(self):
        self.assertEqual(main.positive_int("20"), 20)
    def test_rejects_non_integers(self):
        with self.assertRaises(main.argparse.ArgumentTypeError):
            main.positive_int("hell0")
    def test_rejects_zero(self):
        with self.assertRaises(main.argparse.ArgumentTypeError):
            main.positive_int("0")
    def test_rejects_negative_integers(self):
        with self.assertRaises(main.argparse.ArgumentTypeError):
            main.positive_int("-3")