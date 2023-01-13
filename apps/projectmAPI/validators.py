import hashlib
import json 
from schema import Schema, And, Or
from .global_fields import *
class GameAddValidator:

    def __init__(self, game_description) -> None:
        checksum = game_description['checksum']
        del game_description['checksum']
        self.is_valid = self.__fields_checker(game_description)
        game_description = json.dumps(game_description, separators=(',', ':'), ensure_ascii=False)
        game_description = game_description.encode('utf-8')
        
        self.is_valid = self.is_valid & (checksum == hashlib.sha256(game_description).hexdigest())

    @staticmethod
    def __fields_checker(game_description):
        schema = Schema({
            'club': {
                'id': int,
                'title': str
            },
            'players': [
                {
                    'nickname': str,
                    'role': And(str, lambda x: x in GAME_ROLES[:4]),
                    'game_number': And(int, lambda x: x > 0 and x <= 10),
                    'fouls': And(int, lambda x: x >= 0 and x <= 4),
                    'is_delete': bool,
                    'id': int,
                    'delete_reason': str,
                    'points': Or(float, int),
                    'points_description': str
                }
            ],
            'judge': {
                'id': int,
                'nickname': str
            },
            'timestamp_start': str,
            'timestamp_end': str,
            'days': {
                'night_actions': [
                    {
                        'Mafia': And(int, lambda x: x >= -1 and x <= 10),
                        'Don': And(int, lambda x: x >= -1 and x <= 10),
                        'Comissioner': And(int, lambda x: x >= -1 and x <= 10)
                    }
                ],
                'voting': [
                    {
                        'voted' :[
                            {
                                'num': int,
                                'nickname': str,
                                'id': int,
                                'hands': int
                            }
                        ],
                        'type_of_event': And(str, lambda x: x in ['Catastrophe', 'Up', 'Down']),
                        'day': int
                    }
                ]
            },
            'best_move': {
                'nickname': str,
                'id': int,
                'num': And(int, lambda x: x >= 0 and x <= 10),
                'nums': str,
            },
            'result': And(str, lambda x: x in ('Mafia', 'City', 'Draw')),
            'judge_comments': str
        })
        schema.validate(game_description)
        return schema.is_valid(game_description)


class ClubAddValidation:
    ALLOWED_FIELDS = {'title', 'country', 'city', 'address', 'description'}
    def __init__(self, data) -> None:
        self.data = data
        
    
    @property
    def is_valid(self) -> bool:
        for key in self.data.keys():
            if key not in self.ALLOWED_FIELDS:
                return False
        return True
        
        
    

