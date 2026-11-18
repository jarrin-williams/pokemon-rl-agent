import time
from uuid import uuid4

from agents.observation_agent import ObservationAgent, first_legal_policy
from agents.type_aware_agent import TypeAwareAgent
from agents.max_power_agent import MaxPowerAgent
from evaluation.battle_logger import save_battles, save_experiment_metadata


async def run_battles(num_battles, agent_type="type-aware"):

    if agent_type not in ("type-aware", "max-power", "observation"):
        raise ValueError(f"{agent_type} is not a valid agent type. Must be one of: 'type-aware', 'max-power', 'observation'.")
    
    
    battle_format = "gen9randombattle"
    policy_name = None

    if agent_type == "max-power":
        agent = MaxPowerAgent(
            battle_format=battle_format,
            max_concurrent_battles=1
        )
    elif agent_type == "observation":
        agent = ObservationAgent(
            battle_format=battle_format,
            max_concurrent_battles=1,
            policy=first_legal_policy
        )
        policy_name = first_legal_policy.__name__
    elif agent_type == "type-aware":
        agent = TypeAwareAgent(
            battle_format=battle_format,
            max_concurrent_battles=1,
        )

    max_agent = MaxPowerAgent(
        battle_format=battle_format,
        max_concurrent_battles=1
    )
    agent_name = type(agent).__name__
    opponent_name = type(max_agent).__name__

    print(f"Starting {num_battles} battles....")

    start = time.perf_counter()
    try:

        await agent.battle_against(
            max_agent,
            n_battles=num_battles,
        )
        elapsed = time.perf_counter() - start


        experiment_id = str(uuid4())
        filename = f"battles_{experiment_id}.csv"
        csv_path = save_battles(agent, max_agent, filename=filename)
        metadata = {
            "experiment_id": experiment_id,
            "battle_format": battle_format,
            "num_battles_requested": num_battles,
            "agent": agent_name,
            "opponent": opponent_name,
            "policy": policy_name
        }
        metadata_path = save_experiment_metadata(csv_path, metadata)

        battles = list(agent.battles.values())

        wins = sum(battle.won is True for battle in battles)
        losses = sum(battle.lost is True for battle in battles)
        draws = len(battles) - wins - losses

        average_turns = (
            sum(battle.turn for battle in battles) / len(battles)
            if battles else 0
        )

        print("\n--- Experiment Results ---")
        print(f"Battles: {len(battles)}")
        print(f"{agent_name} wins: {wins}")
        print(f"{opponent_name} wins: {losses}")
        print(f"Draws or unresolved: {draws}")
        print(f"Win rate: {agent.win_rate:.1%}")
        print(f"Average turns: {average_turns:.2f}")
        print(f"Elapsed time: {elapsed:.2f} seconds")
        print(f"Results saved to: {csv_path}")
        print(f"Run settings saved to : {metadata_path}")

    finally:
        await agent.ps_client.stop_listening()
        await max_agent.ps_client.stop_listening()