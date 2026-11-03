import numpy as np


def encode_battle(battle):

    our_pokemon = battle.active_pokemon
    opponent = battle.opponent_active_pokemon


    our_hp = (
        our_pokemon.current_hp_fraction
        if our_pokemon is not None else 0.0
    )

    opponent_hp = (
        opponent.current_hp_fraction
        if opponent is not None else 0.0
    )

    move_powers = np.zeros(4, dtype=np.float32)

    move_effectiveness = np.zeros(4, dtype=np.float32)
    
    for i, move in enumerate(battle.available_moves[:4]):

        move_powers[i] = min(move.base_power / 200.0, 1.0)

    if opponent is not None:
        multiplier = opponent.damage_multiplier(move)
        move_effectiveness[i] = min(multiplier / 4.0, 1.0)
    
    observation = np.array(
        [
            our_hp,
            opponent_hp,
            *move_powers,
            *move_effectiveness
        ],
        dtype=np.float32
    )

    return observation