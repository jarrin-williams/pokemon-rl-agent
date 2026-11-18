from poke_env.player import Player
from environment.observation_encoder import encode_battle

def first_legal_policy(observation, action_mask):
    for i, is_legal in enumerate(action_mask):
        if is_legal:
            return i
    raise ValueError("No legal actions available.")

class ObservationAgent(Player):

    def __init__(self, policy, **player_options):
        self.policy = policy
        super().__init__(**player_options)

        

    def choose_move(self, battle):
        
        moves = battle.available_moves[:4]
        
        if not moves:
            return self.choose_random_move(battle)
        
        observation = encode_battle(battle)
        action_mask = [index < len(moves) for index in range(4)]
        slot = self.policy(observation, action_mask)

        if not (0 <= slot < len(moves)):
            raise ValueError(f"Invalid move slot: {slot}. Must be between 0 and {len(moves) - 1}.")
        
        return self.create_order(moves[slot])