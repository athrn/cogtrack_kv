# -*- coding: utf-8 -*-
import unittest as ut
import sqlite3

from dateutil.parser import parse as date
from sqlitebackend import SqliteBackend, Game

class Test1_Creation(ut.TestCase):

    def test10_creation(self):
        backend = SqliteBackend(':memory:')
        backend.initialize()
        self.assertEqual("1.0", backend.db_version)

        tables = sorted(row[0] for row in backend.con.execute('Select name From sqlite_master Where type="table"'))
        e = u'Game GameSession GameSessionInfo GameSessionInfoKey GameSessionStats GameSessionStatsKey GameSettings GameSettingsKey GameType ProgramInfo'.split()
        self.assertEqual(e, tables)

    def test11_recreation(self):
        a = SqliteBackend(':memory:')
        a.initialize()
        self.assertEqual("1.0", a.db_version)
        
        b = SqliteBackend(con=a.con)
        b.initialize()
        self.assertEqual("1.0", b.db_version)

    def test21_update_types(self):
        a = SqliteBackend(':memory:')
        a.initialize()

        a.update_game_types({'type1', 'type2'})
        self.assertEqual({'type1':1, 'type2':2},  a.game_types)

        a.update_game_types({'type1', 'type2', 'type13'})
        self.assertEqual({'type1':1, 'type2':2, 'type13':3},  a.game_types)

        # Raise error if game_types are removed
        self.assertRaises(ValueError, a.update_game_types, {'type2'})





class Test2(ut.TestCase):
    def setUp(self):
        self.backend = SqliteBackend(':memory:')
        self.backend.initialize()
        self.backend.update_game_types({'nback', 'memory'})

        self.backend2 = SqliteBackend(con=self.backend.con)
        self.backend2.initialize()

    def test11_add_game(self):
        self.backend.add_game('2-back', game_type='nback', game_settings={'max_rounds':10,
                                                                          'n_back':2}) 

        a = self.backend.con.execute('Select * From Game').fetchall()
        e = [(1, '2-back', self.backend.game_types['nback'])]
        self.assertEqual(e, a)


    def test12_load_games(self):
        e = Game(id=1,
                 name=u'2-back',
                 type=u'nback',
                 # NOTE: everything stored as strings for now.
                 settings={u'max_rounds':'10',
                           u'n_back':'2'})

        self.backend.add_game(game_name=e.name,
                              game_type=e.type,
                              game_settings=e.settings)
        
        games = self.backend.load_games()
        self.assertEqual([e], games)

        e2 = Game(id=2,
                  name=u'Memory',
                  type=u'memory',
                  settings={u'x':'ex',
                            u'y':'why'})

        self.backend.add_game(game_name=e2.name,
                              game_type=e2.type,
                              game_settings=e2.settings)

        games = self.backend.load_games()
        self.assertEqual([e, e2], games)

        self.assertRaises(sqlite3.IntegrityError,
                          self.backend.add_game,
                          game_name=e2.name,
                          game_type=e2.type,
                          game_settings=e2.settings)



    def test21_save_session(self):
        self.backend.add_game(game_name='dummy',
                              game_type='nback',
                              game_settings={})

        self.assertRaises(TypeError, self.backend.save_session, game_name='error', game_session={})
        timestamp=date('2001-02-03T04:05:06.789')
        info={u'completion':u'stopped',
              u'stuff':u'bat'}
        stats={'x':1,
               'y':2.0}

        self.backend.save_session(game_name='dummy',
                                  session_info=info,
                                  session_stats=stats,
                                  timestamp=timestamp)
                                  
        a = self.backend.session_info.load_dicts(self.backend.con)
        self.assertEqual({1: info}, a)

        a = self.backend.session_stats.load_dicts(self.backend.con)
        self.assertEqual({1: stats}, a)
        
        
        
        

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
