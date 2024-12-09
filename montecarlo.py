# montecarlo.py

import numpy as np
import pandas as pd
from itertools import permutations, combinations_with_replacement

class Die:
    """
    A Die has N sides/faces and associated weights.
    
    Methods:
    - change_weight(face, new_weight): Change the weight of a single face.
    - roll(n=1): Roll the die n times and return results as a list.
    - show(): Return the internal dataframe of faces and weights.
    """
    def __init__(self, faces: np.ndarray):
        """
        Initialize the Die object with an array of faces.
        
        Parameters
        ----------
        faces : np.ndarray
            An array of distinct faces (strings or numbers).
        
        Raises
        ------
        TypeError
            If faces is not a NumPy array.
        ValueError
            If faces are not distinct.
        """
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a NumPy array.")
        if len(set(faces)) != len(faces):
            raise ValueError("Faces must be distinct.")

        # Initialize all weights to 1.0
        self._df = pd.DataFrame({'face': faces, 'weight': np.ones(len(faces))})
        self._df.set_index('face', inplace=True)

    def change_weight(self, face, new_weight):
        """
        Change the weight of a single side of the die.
        
        Parameters
        ----------
        face : str or int
            The face whose weight is to be changed.
        new_weight : float or int
            The new weight.
        
        Raises
        ------
        IndexError
            If the face is not found in the die faces.
        TypeError
            If the new weight is not numeric.
        """
        if face not in self._df.index:
            raise IndexError("Face not found in die.")
        try:
            new_weight = float(new_weight)
        except ValueError:
            raise TypeError("Weight must be numeric.")
        self._df.at[face, 'weight'] = new_weight

    def roll(self, n=1):
        """
        Roll the die n times.
        
        Parameters
        ----------
        n : int, default 1
            Number of rolls.
        
        Returns
        -------
        list
            A list of outcomes.
        """
        faces = self._df.index.values
        weights = self._df['weight'].values
        probabilities = weights / weights.sum()
        return list(np.random.choice(faces, size=n, p=probabilities))

    def show(self):
        """
        Show the current state of the die's faces and weights.
        
        Returns
        -------
        pd.DataFrame
            A copy of the internal dataframe.
        """
        return self._df.copy()


class Game:
    """
    A Game consists of rolling one or more similar dice a number of times.
    
    Methods:
    - play(n_rolls): Roll all dice n_rolls times and store the results.
    - show(form='wide'): Show the most recent results in wide or narrow form.
    """
    def __init__(self, dice: list):
        """
        Initialize a Game with a list of Die objects.
        
        Parameters
        ----------
        dice : list of Die
            A list containing one or more Die objects.
        """
        self.dice = dice
        self._results = None

    def play(self, n_rolls: int):
        """
        Play the game by rolling all dice n_rolls times.
        
        Parameters
        ----------
        n_rolls : int
            Number of times to roll all dice.
        
        Stores
        ------
        self._results : pd.DataFrame
            The results of the rolls in wide format.
        """
        all_results = {}
        for i, die in enumerate(self.dice):
            all_results[i] = die.roll(n_rolls)

        self._results = pd.DataFrame(all_results)
        self._results.index.name = 'roll_number'

    def show(self, form='wide'):
        """
        Show the results of the most recent play.
        
        Parameters
        ----------
        form : str, default 'wide'
            'wide' or 'narrow' form of the dataframe.
        
        Returns
        -------
        pd.DataFrame
            The results dataframe in the specified format.
        
        Raises
        ------
        ValueError
            If form is not 'wide' or 'narrow'.
        """
        if self._results is None:
            return None
        if form == 'wide':
            return self._results.copy()
        elif form == 'narrow':
            narrow = self._results.stack()
            narrow.index.set_names(['roll_number', 'die_number'], inplace=True)
            return pd.DataFrame(narrow, columns=['outcome'])
        else:
            raise ValueError("form must be 'wide' or 'narrow'.")


class Analyzer:
    """
    An Analyzer takes the results of a single Game and computes statistics.
    
    Methods:
    - jackpot(): Counts how many rolls resulted in all faces being the same.
    - face_counts_per_roll(): Computes face counts for each roll.
    - combo(): Computes combinations of faces rolled and their counts.
    - permutation(): Computes permutations of faces rolled and their counts.
    """
    def __init__(self, game: Game):
        """
        Initialize the Analyzer with a Game object.
        
        Parameters
        ----------
        game : Game
            The game object whose results are to be analyzed.
        
        Raises
        ------
        ValueError
            If the input is not a Game object.
        """
        if not isinstance(game, Game):
            raise ValueError("Analyzer requires a Game object.")
        self.game = game
        self._df_results = game.show('wide')
        self.jackpot_count = None
        self.face_counts = None
        self.combo_counts = None
        self.permutation_counts = None

    def jackpot(self):
        """
        Count how many times all dice showed the same face.
        
        Returns
        -------
        int
            The number of jackpots.
        """
        df = self._df_results
        self.jackpot_count = df.apply(lambda x: len(set(x)) == 1, axis=1).sum()
        return self.jackpot_count

    def face_counts_per_roll(self):
        """
        Count the occurrences of each face in each roll.
        
        Returns
        -------
        pd.DataFrame
            Dataframe with roll_number as index, face values as columns,
            and counts as values.
        """
        df = self._df_results
        # Get all unique faces from all dice
        unique_faces = pd.unique(df.values.ravel())
        counts_per_roll = {}
        for idx, row in df.iterrows():
            counts = {face: (row == face).sum() for face in unique_faces}
            counts_per_roll[idx] = counts
        self.face_counts = pd.DataFrame.from_dict(counts_per_roll, orient='index', columns=unique_faces)
        return self.face_counts

    def combo(self):
        """
        Compute the distinct combinations of faces rolled, ignoring order.
        
        Returns
        -------
        pd.DataFrame
            MultiIndex of unique combinations and their counts.
        """
        df = self._df_results
        combo_list = df.apply(lambda x: tuple(sorted(x)), axis=1)
        combo_counts = combo_list.value_counts()
        self.combo_counts = pd.DataFrame(combo_counts, columns=['count'])
        return self.combo_counts

    def permutation(self):
        """
        Compute distinct permutations of faces rolled, order-dependent.
        
        Returns
        -------
        pd.DataFrame
            MultiIndex of unique permutations and their counts.
        """
        df = self._df_results
        perm_list = df.apply(lambda x: tuple(x), axis=1)
        perm_counts = perm_list.value_counts()
        self.permutation_counts = pd.DataFrame(perm_counts, columns=['count'])
        return self.permutation_counts
