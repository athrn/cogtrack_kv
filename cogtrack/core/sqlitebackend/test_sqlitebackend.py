# -*- coding: utf-8 -*-
import unittest as ut

from sqlitebackend import SqliteBackend

class Tests(ut.TestCase):
    def test10_creation(self):
        backend = SqliteBackend(':memory:')
        backend.initialize()
        self.assertEqual("1.0", backend.db_version)

    def test11_recreation(self):
        a = SqliteBackend(':memory:')
        a.initialize()
        self.assertEqual("1.0", a.db_version)
        
        b = SqliteBackend(con=a.con)
        b.initialize()
        self.assertEqual("1.0", b.db_version)

if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
