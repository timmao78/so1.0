import unittest
import so_func
from datetime import datetime, timedelta
import pandas as pd
from pandas.testing import assert_series_equal

class TestSoFunc(unittest.TestCase):

    def test_get_exercise_time(self):
        # first day is Monday
        result = so_func.get_exercise_time('20', '06')
        ref = datetime(2020, 6, 24, 15)
        self.assertEqual(result, ref)
        result = so_func.get_exercise_time('2020', '06')
        ref = datetime(2020, 6, 24, 15)
        self.assertEqual(result, ref)
        result = so_func.get_exercise_time(2020, 6)
        ref = datetime(2020, 6, 24, 15)
        self.assertEqual(result, ref)
        result = so_func.get_exercise_time(20, 6)
        ref = datetime(2020, 6, 24, 15)
        self.assertEqual(result, ref)

        # first day is Tuesday
        result = so_func.get_exercise_time('20', '09')
        ref = datetime(2020, 9, 23, 15)
        self.assertEqual(result, ref)

        # first day is Wednesday
        result = so_func.get_exercise_time('20', '01')
        ref = datetime(2020, 1, 22, 15)
        self.assertEqual(result, ref)

        # first day is Thursday
        result = so_func.get_exercise_time('20', '10')
        ref = datetime(2020, 10, 28, 15)
        self.assertEqual(result, ref)

        # first day is Friday
        result = so_func.get_exercise_time('20', '05')
        ref = datetime(2020, 5, 27, 15)
        self.assertEqual(result, ref)

        # first day is Saturday
        result = so_func.get_exercise_time('20', '02')
        ref = datetime(2020, 2, 26, 15)
        self.assertEqual(result, ref)

        # first day is Sunday
        result = so_func.get_exercise_time('20', '03')
        ref = datetime(2020, 3, 25, 15)
        self.assertEqual(result, ref)

    def test_get_T(self):
        current_time_object = [datetime(2020, 3, 25, 15), datetime(2020, 3, 25, 15)-timedelta(days=365)]
        result = so_func.get_T('20', '03', pd.Series(current_time_object))
        ref = pd.Series([0.0, 1.0])
        assert_series_equal(result, ref)

if __name__ == '__main__':
    unittest.main()
