# -*- coding: utf-8 -*-
import logging

def list_columns(cur, table):
    return cur.execute('PRAGMA table_info({});'.format(table)).fetchall()

class DictHelper(object):
    """ Create tables for storing dicts with auto-adding of new keys """
    
    def __init__(self,
                 base_name,
                 data_type,
                 foreign_key_column,
                 foreign_key_reference,
                 key_suffix='Key',
                 value_suffix=''):        
        self.data_type = data_type
        self.key_table = '{base_name}{key_suffix}'.format(**locals())
        self.value_table = '{base_name}{value_suffix}'.format(**locals())
        self.foreign_key_column = foreign_key_column
        self.foreign_key_reference = foreign_key_reference

        self.keys = {}


    def create_tables(self, cur):
        create_key_table = """
Create Table {self.key_table}
(
id Integer Primary Key,
name Text Not Null Unique
);""".format(self=self)

        cur.execute(create_key_table)

        create_value_table = '''
Create Table {self.value_table}
(
id Integer Primary Key,
{self.foreign_key_column} Integer,
key_id Integer,
value {self.data_type} Not Null,
Constraint FK_{self.value_table}_{self.foreign_key_column}
  Foreign Key ({self.foreign_key_column})
  References {self.foreign_key_reference}
  On Delete Cascade,
Constraint FK_{self.value_table}_key_id
  Foreign Key (key_id)
  References {self.key_table}(id)
  On Delete Cascade
);'''.format(self=self)

        cur.execute(create_value_table)

    def initialize(self, cur):
        if not self.keys:
            self.load_keys(cur)

    def load_keys(self, cur):
        keys = cur.execute('Select name, id from {self.key_table};'.format(self=self)).fetchall()
        self.keys = dict(keys)
        # self.id2key = dict([id, name] for name,id in keys)
        return self.keys

    def update_keys(self, cur, keys):
        self.initialize(cur)
        
        missing_keys = set(keys) - set(self.keys)
        for key in sorted(missing_keys):
            cmd = 'Insert Into {self.key_table}(name) Values (?);'.format(self=self)
            cur.execute(cmd, [key])

        self.load_keys(cur)

    def load_dict(self, cur, foreign_key):
        """ Load single dictionary """
        self.initialize(cur)
        
        load_dict_cmd = """
Select K.name, V.value
From {self.value_table} as V
Inner Join {self.key_table} As K
    On V.key_id = K.id
Where {self.foreign_key_column} = ?""".format(self=self)

        return dict(cur.execute(load_dict_cmd, [foreign_key]).fetchall())

    def load_dicts(self, cur):
        """ Load all dictionaries """
        self.initialize(cur)
        
        load_dict_cmd = """
Select V.{self.foreign_key_column}, K.name, V.value
From {self.value_table} as V
Inner Join {self.key_table} As K
    On V.key_id = K.id""".format(self=self)

        dicts = {}
        for fk, key, value in cur.execute(load_dict_cmd):
            if fk not in dicts:
                dicts[fk] = {}
            dicts[fk][key]=value

        return dicts
            
    def save(self, cur, foreign_key, data):
        self.initialize(cur)
        
        self.update_keys(cur, data.keys())

        delete_values_cmd = 'Delete From {self.value_table} Where {self.foreign_key_column} = ?;'.format(self=self)
        cur.execute(delete_values_cmd, [foreign_key])

        insert_values_cmd = 'Insert Into {self.value_table}({self.foreign_key_column}, key_id, value) Values (?, ?, ?);'.format(self=self)
        for (key,value) in data.items():
            cur.execute(insert_values_cmd, [foreign_key, self.keys[key], value])

            
        

    


if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_sqlitehelper', failfast=True, exit=False)

