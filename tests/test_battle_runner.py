import unittest
from unittest.mock import AsyncMock, patch
from types import SimpleNamespace

from battle import battle_runner

class BattleRunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_battle_failure_closes_connections_and_propagates(self):
        type_agent = SimpleNamespace(
            battle_against=AsyncMock(
                side_effect=RuntimeError("Battle connection failed")
            ),
            ps_client=SimpleNamespace(
                stop_listening=AsyncMock()
            ),
        )

        max_agent = SimpleNamespace(
            ps_client=SimpleNamespace(
                stop_listening=AsyncMock()
            ),
        )

        with patch.object(battle_runner, "TypeAwareAgent", return_value=type_agent), patch.object(battle_runner, "MaxPowerAgent", return_value=max_agent):
            with self.assertRaisesRegex(RuntimeError, "Battle connection failed"):
                await battle_runner.run_battles(3)


        type_agent.ps_client.stop_listening.assert_awaited()
        max_agent.ps_client.stop_listening.assert_awaited()