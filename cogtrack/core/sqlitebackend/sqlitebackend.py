# -*- coding: utf-8 -*-
import sqlite3
from sqlitehelper import DictHelper
import datetime

create_base_tables = '''
Create Table GameType
(
id Integer Primary Key,
name Text Not Null Unique
);

Create Table Game
(
id Integer Primary Key,
name Text Not Null Unique,
game_type_id Integer,
Constraint FK_Game_game_type_id
    Foreign Key (game_type_id)
    References GameType(id)
    On Delete Cascade
);

Create Table GameSession
(
id Integer Primary Key,
timestamp Real Timestamp Not Null,
game_id Integer Not Null,
Constraint FK_GameSession_game_id
    Foreign Key (game_id)
    References Game(id)
    On Delete Cascade
);

Create Table ProgramInfo
(
id Integer Primary Key,
key Text Not Null Unique,
value Text Not Null
);

Insert Into ProgramInfo (key, value) Values ("db_version", "1.0");

'''

# TODO: Create table DisplayName with name, display_name, sort_order, description (game_type)
# Presentation / Theme
# name - display_name & description

from collections import namedtuple

Game = namedtuple('GameDef', 'id name type settings'.split())


class SqliteBackend(object):
    def __init__(self, path=None, con=None):
        if con:
            self.con = con
        else:
            self.con = sqlite3.connect(path,
                                       detect_types=sqlite3.PARSE_DECLTYPES) # |sqlite3.PARSE_COLNAMES)
            self.con.execute('PRAGMA foreign_keys=ON')
            self.con.commit()
        
        self.game_settings = DictHelper('GameSettings',
                                        data_type='Text',
                                        foreign_key_column='game_id',
                                        foreign_key_reference='Game(id)')
        self.session_info = DictHelper('GameSessionInfo',
                                       data_type='Text',
                                       foreign_key_reference='GameSession(id)',
                                       foreign_key_column='game_session_id')
        self.session_stats = DictHelper('GameSessionStats',
                                        data_type='Real',
                                        foreign_key_reference='GameSession(id)',
                                        foreign_key_column='game_session_id')
                                        

    def initialize(self):
        db_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='ProgramInfo';"
        if not self.con.execute(db_exists).fetchall():
            cur = self.con.cursor()
            cur.executescript(create_base_tables)
            self.game_settings.create_tables(cur)
            self.session_info.create_tables(cur)
            self.session_stats.create_tables(cur)
            self.con.commit()

        self.reload()

    def reload(self):
        # TODO: Assert something relating to db_version?
        db_version_cmd = 'Select value from ProgramInfo where key="db_version"'
        (self.db_version,) = self.con.execute(db_version_cmd).fetchone()

        self.load_game_types()        
    

    def load_game_types(self):
        self.game_types = dict(self.con.execute('Select name, id From GameType'))
        return self.game_types
        

    def update_game_types(self, game_types):
        removed = set(self.game_types) - set(game_types)
        if removed:
            raise ValueError('Can not remove game types')
        
        missing = set(game_types) - set(self.game_types)
        cur = self.con.cursor()
        for game_type in missing:
            cur.execute('Insert Into GameType(name) Values (?);', [game_type])

        self.load_game_types()


    def add_game(self, game_name, game_type, game_settings):
        game_type_id = self.game_types[game_type]
        
        cur = self.con.cursor()
        cur.execute('Insert Into Game(name, game_type_id) Values (?,?);', [game_name, game_type_id])
        (game_id,) = cur.execute('Select id from Game Where name = ?;', [game_name]).fetchone()
        self.game_settings.save(cur=cur,
                                foreign_key=game_id,
                                data=game_settings
                                )
        self.con.commit()


    # def update_game(self, game_def):
    #     pass

    def load_games(self):
        cur = self.con.cursor()
        settings = self.game_settings.load_dicts(cur)

        cmd = "Select G.id, G.name, T.name From Game G Inner Join GameType T On G.game_type_id = T.id"
        rows = cur.execute(cmd)
        games = [Game(id=id, name=name, type=type_name, settings=settings[id]) for id, name, type_name in rows]
        return games
        
        

    def save_session(self,
                     game_name,
                     # TODO: Replace info with tags.
                     session_info,
                     session_stats,
                     timestamp=None):
        if not timestamp:
            timestamp=datetime.datetime.now()

        (game_id,) = self.con.execute("Select id From Game Where name = ?", [game_name]).fetchone()

        cur = self.con.cursor()
        cur.execute('Insert Into GameSession(game_id, timestamp) Values (?, ?)', [game_id, timestamp])
        (session_id,) = cur.execute('Select last_insert_rowid();').fetchone()
        self.session_info.save(cur, foreign_key=session_id, data=session_info)
        self.session_stats.save(cur, foreign_key=session_id, data=session_stats)
        self.con.commit()


if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_sqlitebackend', failfast=True, exit=False)

