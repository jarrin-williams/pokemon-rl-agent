
import asyncio
import argparse

from battle.battle_runner import run_battles

NUM_BATTLES = 100

def positive_int(value):

    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Battle count must be a positive integer."
        )
    if number <= 0:
        raise argparse.ArgumentTypeError(
            "Battle count must be greater than zero."
        )
    return number

def parse_args():

    parser = argparse.ArgumentParser(description="Run a Pokemon battle experiment")
    
    parser.add_argument(
        "--num-battles",
        type=positive_int,
        default=NUM_BATTLES,
        help="Number of battles to run (default: %(default)s).",
    )
    parser.add_argument(
        "--agent",
        choices=["type-aware", "max-power", "observation"],
        default="type-aware",
        help="Agent type to use (default: %(default)s)."
    )

    return parser.parse_args()


async def main(num_battles=None, agent_type="type-aware"):

    if num_battles is None:
        num_battles = NUM_BATTLES
    await run_battles(num_battles, agent_type=agent_type)

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.num_battles, agent_type=args.agent))