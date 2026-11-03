from poke_env.player import Player

class TypeAwareAgent(Player):

    def choose_move(self, battle):

        opponent = battle.opponent_active_pokemon


        if battle.available_moves and opponent:

            def score_move(move):
                
                effectiveness = opponent.damage_multiplier(move)

                score = move.base_power * effectiveness

                return score
            

            best_move = max(

                battle.available_moves,
                key=score_move

            )

            return self.create_order(best_move)
        
        return self.choose_random_move(battle)