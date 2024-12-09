# test_montecarlo.py

import unittest
import numpy as np
from montecarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    def setUp(self):
        self.faces = np.array([1,2,3])
        self.die = Die(self.faces)

    def test_init(self):
        self.assertEqual(len(self.die.show()), 3)
        
    def test_change_weight(self):
        self.die.change_weight(2, 2.0)
        self.assertEqual(self.die.show().loc[2,'weight'], 2.0)
        
    def test_roll(self):
        result = self.die.roll(5)
        self.assertEqual(len(result), 5)
        
    def test_show(self):
        df = self.die.show()
        self.assertIn('weight', df.columns)


class TestGame(unittest.TestCase):
    def setUp(self):
        faces = np.array([1,2,3])
        d1 = Die(faces)
        d2 = Die(faces)
        self.game = Game([d1,d2])

    def test_play(self):
        self.game.play(10)
        self.assertEqual(self.game.show('wide').shape[0], 10)
        
    def test_show_wide(self):
        self.game.play(5)
        df_wide = self.game.show('wide')
        self.assertEqual(df_wide.shape[0],5)
        
    def test_show_narrow(self):
        self.game.play(5)
        df_narrow = self.game.show('narrow')
        self.assertEqual(df_narrow.index.names, ['roll_number','die_number'])
        
    def test_show_bad_input(self):
        with self.assertRaises(ValueError):
            self.game.show(form='invalid')


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        faces = np.array([1,2,3])
        d1 = Die(faces)
        d2 = Die(faces)
        g = Game([d1,d2])
        g.play(10)
        self.analyzer = Analyzer(g)

    def test_init(self):
        self.assertIsInstance(self.analyzer, Analyzer)
        
    def test_jackpot(self):
        # Can't guarantee any jackpot with random data, but test method runs
        jp = self.analyzer.jackpot()
        self.assertIsInstance(jp, int)
        
    def test_face_counts_per_roll(self):
        fc = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(fc, pd.DataFrame)
        
    def test_combo(self):
        c = self.analyzer.combo()
        self.assertIsInstance(c, pd.DataFrame)
        
    def test_permutation(self):
        p = self.analyzer.permutation()
        self.assertIsInstance(p, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
