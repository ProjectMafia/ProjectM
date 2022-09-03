import hashlib 
from jsonschema import validate
import json
from schema import Schema, And, Use, Optional, SchemaError
from .global_fields import *
class GameAddValidator:

    def __init__(self, game_description) -> None:
        checksum = game_description['checksum']
        del game_description['checksum']
        self.is_valid = self.__fields_checker(game_description)
        
        game_description = str(game_description).encode('utf-8')
        print(hashlib.sha256(game_description).hexdigest())
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
                    'fouls': And(int, lambda x: x >= 0 and x <= 4),
                    'is_delete': bool,
                    'id': int,
                    'delete_reason': str,
                    'points': float,
                    'points_description': str
                }
            ],
            'judge': {
                'nickname': str,
                'id': int
            },
            'timestamp_start': str,
            'timestamp_end': str,
            'days': {
                'night_actions': [
                    {
                        'Mafia': And(int, lambda x: x >= 0 and x <= 10),
                        'Don': And(int, lambda x: x >= 0 and x <= 10),
                        'Comissioner': And(int, lambda x: x >= 0 and x <= 10)
                    }
                ],
                'voting': [
                    [
                        {
                            'voted' :[
                                {
                                    'num': int,
                                    'nickname': str,
                                    'id': int,
                                    'hands': int
                                }
                            ],
                            'type_of_event': And(str, lambda x: x in ['catastrophe', 'up', 'seat'])
                        }
                    ]
                ]
            },
            'best_move': {
                'nickname': str,
                'id': int,
                'num': And(int, lambda x: x >= 0 and x <= 10),
                'nums': [
                    And(int, lambda x: x >= 0 and x <= 10)
                ]
            },
            'result': And(str, lambda x: x in ('Mafia', 'City', 'Draw')),
            'judge_comments': str
        })
        return schema.is_valid(game_description)


