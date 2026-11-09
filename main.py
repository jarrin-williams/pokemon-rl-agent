
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
    return parser.parse_args()


async def main(num_battles=None):
    if num_battles is None:
        num_battles = NUM_BATTLES
    await run_battles(num_battles)

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.num_battles))