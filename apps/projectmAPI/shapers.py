from .global_fields import *


class UserInClubStatShaper:

    def __init__(self, user_dict:dict) -> None:
        
        self.data = {
            'mafia': {}, 
            'don': {}, 
            'civilian': {}, 
            'comissioner': {},
            'total': {}
        }
        for field in user_dict.keys():
            self.data[GAME_ROLES_DICT[field[-3:]].lower()].update({field[:-4]: user_dict[field]})


class GameStatShaper:

    def __init__(self, game_dict:dict) -> None:
        self.data = game_dict[0]
        players = []
        for i in range(len(self.data['players'])):
            players.append({
                'id': self.data['ids'][i],
                'nickname': self.data['players'][i],
                'role': self.data['roles'][i]
            })
        del self.data['players'], self.data['ids'], self.data['roles']
        print(self.data)
        self.data = self.data | {'players': players}