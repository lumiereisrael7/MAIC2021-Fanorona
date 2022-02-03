from faronona.faronona_player import FarononaPlayer
from faronona.faronona_rules import FarononaRules
from faronona.faronona_action import FarononaAction
from faronona.faronona_action import FarononaActionType
from math import infinity
import random
import json


class AI(FarononaPlayer):

    name = "Honorat"

    def __init__(self, color):
        super(AI, self).__init__(self.name, color)
        self.position = color.value

    def minimax(self, state, deep, player):
        
        if player == self.position:
            best = [None, -infinity]

        else:
            best = [None, +infinity]

        if deep == 0 or (FarononaRules.get_player_action(state, player) is not None and len(FarononaRules.get_player_action(state, player) == 0)):
            score = evaluate(state)
            return [None, score]

        for actionDict in FarononaRules.get_player_action(state, player):
            at, to = actionDict['action']['at'], actionDict['action']['t0']
            if (FarononaRules.is_win_approach_move(at, to, state, self.position) is not None) and (FarononaRules.is_win_remote_move(at, to, state, self.position) is not None) and len(FarononaRules.is_win_approach_move(at, to, state, self.position)) != 0 and len(FarononaRules.is_win_remote_move(at, to, state, self.position)) != 0:
                # between win approach and win remoate, check which can let me gain the more adverse pieces
                st = ''
                if len(FarononaRules.is_win_approach_move(at, to, state, self.position)) < len(FarononaRules.is_win_remote_move(at, to, state, self.position)):
                    st = 'REMOTE'
                
                else:
                    st = 'APPROACH'

                action = FarononaAction(
                        action_type=FarononaActionType.MOVE, win_by=st, at=at, to=to)
                
                if FarononaRules.act(state, action, player):
                    score = minimax(state, deep -1, -player)
                    undo =  FarononaActio(
                            action_type=FarononaActionType.MOVE, win_by=st, at=to, to=at)
                    FarononaRules.act(state, undo, player)
                    
                    score[0] = action                    

        if player == self.position:
            if score[1] > best[1]:
                best = score
            
        else:
            if score[1] < best[1]
                best = score

        return best
    
    
    
    def play(self, state, remain_time):
        nb_pion = state.get_player_info(color)['on_board']
        if(nb_pion == 22): 
            #Retrieve a random action
            action = FarononaRules.random_play(state, self.position)
            #Extract departure and arrival of the piece
            actionDict = action.get_action_as_dict()
            at = actionDict['action']['at']
            to = actionDict['action']['to']
            #check if it is a win move both for approach and remote
            if (FarononaRules.is_win_approach_move(at, to, state, self.position) is not None) and (FarononaRules.is_win_remote_move(at, to, state, self.position) is not None) and len(FarononaRules.is_win_approach_move(at, to, state, self.position)) != 0 and len(FarononaRules.is_win_remote_move(at, to, state, self.position)) != 0:
                # between win approach and win remoate, check which can let me gain the more adverse pieces
                if len(FarononaRules.is_win_approach_move(at, to, state, self.position)) < len(FarononaRules.is_win_remote_move(at, to, state, self.position)):
                    action = FarononaAction(
                        action_type=FarononaActionType.MOVE, win_by='REMOTE', at=at, to=to)
                else:
                    action = FarononaAction(
                        action_type=FarononaActionType.MOVE, win_by='APPROACH', at=at, to=to)
            return action
        else:
            action = minimax(state, deep, self.position)
            return action
            
