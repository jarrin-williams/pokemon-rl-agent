
import asyncio
import time

from agents.type_aware_agent import TypeAwareAgent
from agents.max_power_agent import MaxPowerAgent
from evaluation.battle_logger import save_battles

NUM_BATTLES = 100


async def main():
    
    max_agent = MaxPowerAgent(
        battle_format = "gen9randombattle",
        max_concurrent_battles = 1
    )

    type_agent = TypeAwareAgent(
        battle_format = "gen9randombattle",
        max_concurrent_battles = 1,
    )

    print(f"Starting {NUM_BATTLES} battles....")

    start = time.perf_counter()
    try:

        await type_agent.battle_against(
            max_agent,
            n_battles=NUM_BATTLES,
        )
        elapsed = time.perf_counter() - start


        csv_path = save_battles(type_agent, max_agent)

        battles = list(type_agent.battles.values())

        wins = sum(battle.won is True for battle in battles)
        losses = sum(battle.lost is True for battle in battles)
        draws = len(battles) - wins - losses

        average_turns = (
            sum(battle.turn for battle in battles) / len(battles)
            if battles else 0
        )

        print("\n--- Experiment Results ---")
        print(f"Battles: {len(battles)}")
        print(f"TypeAwareAgent wins: {wins}")
        print(f"MaxPowerAgent wins: {losses}")
        print(f"Draws or unresolved: {draws}")
        print(f"Win rate: {type_agent.win_rate:.1%}")
        print(f"Average turns: {average_turns:.2f}")
        print(f"Elapsed time: {elapsed:.2f} seconds")
        print(f"Results saved to: {csv_path}")

    finally:
        await type_agent.ps_client.stop_listening()
        await max_agent.ps_client.stop_listening()

if __name__ == "__main__":
    asyncio.run(main())