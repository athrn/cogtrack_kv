# -*- coding: utf-8 -*-
import sqlite3
from sqlitehelper import DictHelper

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



class SqliteBackend(object):
    def __init__(self, path=None, con=None):
        if con:
            self.con = con
        else:
            self.con = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
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
            self.con.executescript(create_base_tables)
            self.con.commit()

        get_db_version = 'Select value from ProgramInfo where key="db_version"'
        (self.db_version,) = self.con.execute(get_db_version).fetchone()



if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_sqlitebackend', failfast=True, exit=False)

