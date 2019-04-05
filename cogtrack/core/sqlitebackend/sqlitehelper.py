# -*- coding: utf-8 -*-

def list_columns(cur, table):
    return cur.execute('PRAGMA table_info({});'.format(table)).fetchall()

class DictHelper(object):
    def __init__(self,
                 base_name,
                 data_type,
                 foreign_key_column,
                 foreign_key_table,
                 key_suffix='Key',
                 value_suffix=''):        
        self.key_table = '{base_name}{key_suffix}'.format(**locals())
        self.value_table = '{base_name}{value_suffix}'.format(**locals())
        self.foreign_key_column = foreign_key_column
        self.foreign_key_table = foreign_key_table

        self.create_key_table = """
Create Table {self.key_table}
(
id Integer Primary Key,
name Text Not Null Unique
);""".format(**locals())

        self.create_value_table = '''
Create Table {self.value_table}
(
id Integer Primary Key,
{foreign_key_column} Integer, -- References {foreign_key_table}(id),
key_id Integer, -- References {self.key_table}(id),
value {data_type} Not Null,
Constraint FK_{base_name}_{foreign_key_column}
  Foreign Key ({foreign_key_column})
  References {foreign_key_table}(foreign_key_column)
  On Delete Cascade,
Constraint FK_{base_name}_key
  Foreign Key (key_id)
  References {self.key_table}(id)
  On Delete Cascade
);'''.format(**locals())

        self._init_commands()

        self.keys = {}


    def _init_commands(self):
        self.delete_values_cmd = 'Delete From {self.value_table} Where {self.foreign_key_column} = ?;'.format(self=self)

        self.insert_values_cmd = 'Insert Into {self.value_table}({self.foreign_key_column}, key_id, value) Values (?, ?, ?);'.format(self=self)

        self.load_dict_cmd = """
Select keys.name, V.value
From {self.value_table} as V
Inner Join {self.key_table} As keys
    On V.key_id = keys.id
Where {self.foreign_key_column} = ?;""".format(self=self)


    def create_tables(self, cur):
        cur.execute(self.create_key_table)
        cur.execute(self.create_value_table)

    def update(self, cur):
        self.load_keys()
        # self.load_values()

    def load_keys(self, cur):
        keys = cur.execute('Select name, id from {self.key_table};'.format(self=self)).fetchall()
        self.keys = dict(keys)
        return self.keys

    def update_keys(self, cur, keys):
        missing_keys = set(keys) - set(self.keys)
        for key in sorted(missing_keys):
            cmd = 'Insert Into {self.key_table}(name) Values (?);'.format(self=self)
            cur.execute(cmd, [key])

        self.load_keys(cur)

    def load_dict(self, cur, foreign_key):
        # NOTE: Should I load a single dictionary or all at once?
        return dict(cur.execute(self.load_dict_cmd, [foreign_key]).fetchall())
            
    def save(self, cur, foreign_key, data):
        self.update_keys(cur, data.keys())

        cur.execute(self.delete_values_cmd, [foreign_key])
        for (key,value) in data.items():
            cur.execute(self.insert_values_cmd, [foreign_key, self.keys[key], value])

            
        

    


if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_sqlitehelper', failfast=True, exit=False)

