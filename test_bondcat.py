import unittest
from bondcat import BondFetchCat
from service import DB
from unittest.mock import patch
from test_data import test_response, stored_data

class BondCatTest(unittest.TestCase):
    # Bondcat could fetch bond stagging information from the internet
    # The information should have bond name, stagging date, release date
    # When there are new bonds, save to db.
    def test_can_fetch_information(self):
        res = None
        with patch('requests.get') as mock_get:
            mock_get.return_value = test_response
            cat = BondFetchCat()
            res = cat.fetch_bonds()
            self.assertEqual(res[0]['CORRESNAME'], test_response[0]['CORRESNAME'])
            self.assertEqual(res[0]['STARTDATE'], test_response[0]['STARTDATE'])

        with patch('bondcat.BondFetchCat._select_all_bonds') as mock_select_all_bond:
            mock_select_all_bond.return_value = stored_data
            cat = BondFetchCat()
            new_bonds = cat.filter_new_bonds(res)
            self.assertNotEqual(new_bonds, stored_data)

    def test_can_infor_user(self):
        pass
    # Bondcat should info the user whether there are bonds available for stagging, 
    # if not, don't send notification. If it is, send notification via telegram.


class ServiceTest(unittest.TestCase):
    def setUp(self):
        self.db = DB(test=True)
        self.db.cur.execute('''
            CREATE TABLE bonds (bonds_name text, start_date text)
        ''')
        # self.db.cur.executemany()

    def test_db_exist(self):
        # db = DB(test=True)
        self.assertIsNotNone(self.db)


    def test_select_all_bonds(self):
        all_bonds_in_db = self.db.select_all_bonds()

        self.db.cur.execute("select * from bonds")
        saved_bonds = self.db.cur.fetchall()

        self.assertEqual(all_bonds_in_db, saved_bonds)
        

    def test_select_bonds_at_someday(self):
        bonds_of_a_day = self.db.select_bonds_at("2021-11-01T00:00:00")

        self.db.cur.execute("select * from bonds WHERE start_date = '2021-11-01T00:00:00'")
        saved_bonds = self.db.cur.fetchall()

        self.assertEqual(bonds_of_a_day, saved_bonds)

    def test_save_bonds(self):
        only_wanted_cols = [(bond['CORRESNAME'], bond['STARTDATE']) for bond in stored_data]
        self.db.save_bonds(only_wanted_cols)

        self.db.cur.execute("select * from bonds")
        saved_bonds = self.db.cur.fetchall()

        self.assertEqual(saved_bonds, only_wanted_cols)


if __name__ == '__main__':
    unittest.main()