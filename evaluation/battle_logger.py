import csv
import json
from datetime import datetime
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

def save_battles(agent, opponent, filename=None) :
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"battles_{timestamp}.csv"
    
    file_path = RESULTS_DIR / filename

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "battle_id",
            "agent",
            "opponent",
            "won",
            "lost",
            "turns"
        ])

        for battle_id, battle in agent.battles.items():
            writer.writerow([
                battle_id,
                type(agent).__name__,
                type(opponent).__name__,
                battle.won,
                battle.lost,
                battle.turn
            ])
    return file_path

def save_experiment_metadata(csv_path, metadata):
    metadata_path = Path(csv_path).with_suffix(".json")
    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata,file, indent=2)
        return metadata_path