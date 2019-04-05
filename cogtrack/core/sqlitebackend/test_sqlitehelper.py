# -*- coding: utf-8 -*-
import unittest as ut
import sqlite3

from pprint import pprint

from sqlitehelper import DictHelper, list_columns

class TestDictHelper(ut.TestCase):
    def setUp(self):
        self.con = sqlite3.connect(':memory:')
        
        cur = self.con.cursor()
        cur.execute('Create Table Main (id Integer Primary Key, name Text Not Null Default "");')
        cur.execute('Insert Into Main(name) Values ("one");')
        cur.execute('Insert Into Main(name) Values ("two");')


        self.helper = DictHelper(base_name='Dict',
                                 data_type='Real',
                                 foreign_key_column='main_id',
                                 foreign_key_table='Main',
                                 )

        self.helper.create_tables(cur)
        self.con.commit()

        self.cur = self.con.cursor()



    def test10_creation(self):
        self.assertEqual([(1, 'one'), (2, 'two')], self.con.execute('Select * From Main;').fetchall())
        self.assertEqual([], self.con.execute('Select * From DictKey;').fetchall())
        self.assertEqual([], self.con.execute('Select * From Dict;').fetchall())

        a = [(i, name, type) for i,name,type,_,_,_ in list_columns(self.cur, 'DictKey')]
        e = [(0, 'id', 'Integer'),
             (1, 'name', 'Text')]
        self.assertEqual(e, a)

        a = [(i, name, type) for i,name,type,_,_,_ in list_columns(self.cur, 'Dict')]
        e = [(0, 'id', 'Integer'),
             (1, 'main_id', 'Integer'),
             (2, 'key_id', 'Integer'),
             (3, 'value', 'Real')]
        self.assertEqual(e, a)
        
        
    def test11_insert_values(self):
        self.helper.save(self.cur,
                         foreign_key=1,
                         data=dict(x=10, y=20))
        
        self.con.commit()

        a = self.con.execute('Select * From DictKey;').fetchall()
        self.assertEqual([(1, 'x'), (2, 'y')], a)
        a =  self.con.execute('Select main_id, key_id, value From Dict Order By main_id, key_id;').fetchall()
        self.assertEqual([(1, 1, 10.0), (1, 2, 20.0)], a)

    def test12_load_dict(self):
        fk = 1
        e = dict(x=10., y=20.)
        self.helper.save(self.cur,
                         foreign_key=fk,
                         data=e)
        self.con.commit()
        self.assertEqual(e, self.helper.load_dict(self.con.cursor(), fk))
        


    def test13_update_values(self):
        self.helper.save(self.cur,
                         foreign_key=1,
                         data=dict(x=10, y=20))

        self.helper.save(self.cur,
                         foreign_key=2,
                         data=dict(x=100, y=200))

        self.con.commit()
        self.assertEqual(dict(x=10, y=20), self.helper.load_dict(self.con.cursor(), 1))
        self.assertEqual(dict(x=100, y=200), self.helper.load_dict(self.con.cursor(), 2))


        self.helper.save(self.cur,
                         foreign_key=1,
                         data=dict(y=25))
        self.con.commit()

        self.assertEqual(dict(y=25), self.helper.load_dict(self.con.cursor(), 1))
        self.assertEqual(dict(x=100, y=200), self.helper.load_dict(self.con.cursor(), 2))


if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
