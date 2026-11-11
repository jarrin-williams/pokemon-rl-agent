import unittest
from unittest.mock import AsyncMock, patch
from types import SimpleNamespace

from battle import battle_runner

class BattleRunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_success_saves_results_and_closes_connections(self):
        battle = SimpleNamespace(won=True, lost=False, turn=12)
        type_agent = SimpleNamespace(battle_against=AsyncMock(),
                                      battles={"battle-test-1": battle},
                                      win_rate=1.0,
                                      ps_client=SimpleNamespace(stop_listening=AsyncMock())
)
        max_agent = SimpleNamespace(ps_client=SimpleNamespace(stop_listening=AsyncMock()))
        with patch.object(
            battle_runner, "TypeAwareAgent", return_value=type_agent
            ), patch.object(
                battle_runner, "MaxPowerAgent", return_value=max_agent
                ), patch.object(
                    battle_runner, "uuid4", return_value="test-run-id"
                    ), patch.object(
                    battle_runner, "save_battles", return_value="results/battles_test-run-id.csv"
                        ) as save, patch.object(
                            battle_runner, "save_experiment_metadata", return_value="results/battles_test-run-id.json",
                        ) as save_metadata:
            await battle_runner.run_battles(1)

        type_agent.battle_against.assert_awaited_once_with(
            max_agent, n_battles=1
        )

        save.assert_called_once_with(type_agent, max_agent, filename="battles_test-run-id.csv")
        save_metadata.assert_called_once_with(
            "results/battles_test-run-id.csv",
            {
                "experiment_id": "test-run-id",
                "battle_format": "gen9randombattle",
                "num_battles_requested": 1,
            }
        )

        type_agent.ps_client.stop_listening.assert_awaited_once()
        max_agent.ps_client.stop_listening.assert_awaited_once()

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