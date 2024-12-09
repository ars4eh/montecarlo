## Metadata
**Author:** Austin Samhric  
**Project Name:** Monte Carlo Simulator

This project provides a Python-based Monte Carlo simulation toolkit that allows you to create and analyze dice-based games. The simulation is performed through three main classes:

- **Die:** Represents a single die with customizable faces and weights.
- **Game:** Represents a game composed of one or more dice and simulates multiple rolls.
- **Analyzer:** Provides methods to analyze the results of a game (e.g., counting jackpots, face frequencies, and generating permutations and combinations).


## Installation

Use the package manager to install montecarlo.

```bash
pip install montecarlo
```

## Usage

Below are a few quick code examples to help you get started after installing the package.

```python
from montecarlo.montecarlo import Die, Game, Analyzer
import numpy as np

# Create a fair 6-sided die
faces = np.array([1,2,3,4,5,6])
fair_die = Die(faces)

# Roll the die 5 times
outcomes = fair_die.roll(5)
print("Die outcomes:", outcomes)

# Create a game with 2 fair dice
d1 = Die(faces)
d2 = Die(faces)
game = Game([d1, d2])
game.play(10)
print("Game results (wide):")
print(game.show('wide'))

# Analyze the game
analyzer = Analyzer(game)
jackpot_count = analyzer.jackpot()
print("Number of jackpots:", jackpot_count)

# Face counts per roll
face_counts = analyzer.face_counts_per_roll()
print("Face counts per roll:")
print(face_counts)

# Combinations of outcomes
combo_df = analyzer.combo()
print("Combo counts:")
print(combo_df)

# Permutations of outcomes
perm_df = analyzer.permutation()
print("Permutation counts:")
print(perm_df)
```

## API Description

```python
Class: Die

A Die object represents a single die with N faces, each having a weight that influences rolling probability.

Methods:
	•	__init__(self, faces: np.ndarray)
	•	Initializes the die with given faces.
	•	Parameters:
	•	faces (np.ndarray): Distinct face values (strings or numbers).
	•	Raises:
	•	TypeError if faces is not a NumPy array.
	•	ValueError if faces are not distinct.
	•	change_weight(self, face, new_weight)
	•	Changes the weight of a single side.
	•	Parameters:
	•	face (str|int): The face whose weight to change.
	•	new_weight (float|int): The new weight.
	•	Raises:
	•	IndexError if the face is not found.
	•	TypeError if the new weight is not numeric.
	•	roll(self, n=1)
	•	Rolls the die n times and returns a list of results.
	•	Parameters:
	•	n (int): Number of rolls, default 1.
	•	Returns:
	•	list: The outcomes of the rolls.
	•	show(self)
	•	Returns a DataFrame of the die’s faces and their weights.
	•	Returns:
	•	pd.DataFrame: Copy of the faces and weights.

Class: Game

A Game object takes one or more dice and rolls them together a specified number of times.

Methods:
	•	__init__(self, dice: list)
	•	Initializes a game with a list of Die objects.
	•	Parameters:
	•	dice (list): A list of Die objects.
	•	play(self, n_rolls: int)
	•	Plays the game by rolling all dice n_rolls times.
	•	Parameters:
	•	n_rolls (int): Number of rolls.
	•	show(self, form='wide')
	•	Shows the results of the most recent play.
	•	Parameters:
	•	form (str): ‘wide’ or ‘narrow’ format.
	•	Returns:
	•	pd.DataFrame: The results DataFrame.
	•	Raises:
	•	ValueError if the form argument is invalid.

Class: Analyzer

An Analyzer object takes a Game’s results and computes statistical analyses such as jackpots, face counts, combinations, and permutations.

Methods:
	•	__init__(self, game: Game)
	•	Initializes the analyzer with a Game object.
	•	Parameters:
	•	game (Game): The game to analyze.
	•	Raises:
	•	ValueError if the input is not a Game object.
	•	jackpot(self)
	•	Counts how many rolls resulted in all dice showing the same face.
	•	Returns:
	•	int: Number of jackpots.
	•	face_counts_per_roll(self)
	•	Counts the occurrences of each face per roll.
	•	Returns:
	•	pd.DataFrame: Index is roll number, columns are faces, values are counts.
	•	combo(self)
	•	Computes distinct combinations of faces rolled (order-independent).
	•	Returns:
	•	pd.DataFrame: MultiIndex for combinations and their counts.
	•	permutation(self)
	•	Computes distinct permutations of faces rolled (order-dependent).
	•	Returns:
	•	pd.DataFrame: MultiIndex for permutations and their counts.
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
