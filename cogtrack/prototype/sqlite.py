from pprint import pprint

def create_dict_tables(base_name,
                       data_type,
                       foreign_key_column,
                       foreign_key_table,
                       key_suffix='Key',
                       value_suffix=''):
    key_table = '{base_name}{key_suffix}'.format(**locals())
    value_table = '{base_name}{value_suffix}'.format(**locals())

    create_key_table = """
Create Table {key_table}
(
id Integer Primary Key,
name Text Not Null Unique
);""".format(**locals())

    create_value_table = '''
Create Table {value_table}
(
id Integer Primary Key,
{foreign_key_column} Integer References {foreign_key_table}(id),
key_id Integer References {key_table}(id),
"value" {data_type} Not Null
);'''.format(**locals())

    return [create_key_table, create_value_table]
    

def create_game_table():
    cmd = '''
Create Table Game
(
id Integer Primary Key,
name Text Not Null Unique,
"type" Text Not Null
);'''

    return [cmd]


def create_game_session_tables():
    cmd = '''
Create Table GameSession
(
id Integer Primary Key,
"timestamp" Real Timestamp Not Null,
game_id Integer References Game(id)
);'''

    info = create_dict_tables('GameSessionInfo',
                              data_type='Text',
                              foreign_key_table='GameSession',
                              foreign_key_column='game_session_id')

    stats = create_dict_tables('GameSessionStats',
                               data_type='Real',
                               foreign_key_table='GameSession',
                               foreign_key_column='game_session_id')

    return [cmd] + info + stats
    

    


# Presentation / Theme
# name - display_name & description

# def create_program_info():
#     cmd = '''
# Create Table ProgramInfo
# (
# id Integer Primary Key,
# key Text Not Null Unique,
# "value" Text Not Null
# );'''

#     insert = 'Insert Into ProgramInfo (key,value) Values ("database_version", "1");'

#     return [cmd, insert]

import sqlite3

def create_tables():
    cmds = []
    cmds += create_game_table()
    cmds += create_dict_tables('GameSettings',
                               data_type='text',
                               foreign_key_table='Game',
                               foreign_key_column='game_id')

    cmds += create_game_session_tables()


    # Auto detect dates etc.
    # https://www.pythoncentral.io/advanced-sqlite-usage-in-python/
    # db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    for cmd in cmds:
        print(cmd)
        cur.execute(cmd)
    con.commit()
    con.close()
    
    


if __name__ == "__main__":
    create_tables()
