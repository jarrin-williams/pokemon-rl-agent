
import asyncio

from battle.battle_runner import run_battles

NUM_BATTLES = 100

async def main():
    await run_battles(NUM_BATTLES)

if __name__ == "__main__":
    asyncio.run(main())