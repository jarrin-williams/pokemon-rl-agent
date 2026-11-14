import argparse
import csv
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Read a saved battle run.")
    parser.add_argument("csv_path", type=Path, help="Path to a battle results csv")
    args = parser.parse_args()
    with args.csv_path.open(encoding="utf-8", newline="") as file:
        battles = list(csv.DictReader(file))

    count = len(battles)
    if count == 0:
        print("No battle records found")
        return

    wins = sum(battle["won"] == "True" for battle in battles)
    win_rate = wins / count
    average_turns = sum(int(battle["turns"]) for battle in battles) / count

    print(f"Total Battles: {count}")
    print(f"Win Rate: {win_rate:.1%}")
    print(f"Average Turns: {average_turns:.2f}")

if __name__ == "__main__":
    main()