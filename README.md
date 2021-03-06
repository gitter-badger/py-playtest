# PyPlaytest

[![Build Status](https://travis-ci.org/dat-boris/py-playtest.svg?branch=master)](https://travis-ci.org/dat-boris/py-playtest)
[![codecov](https://codecov.io/gh/dat-boris/py-playtest/branch/master/graph/badge.svg)](https://codecov.io/gh/dat-boris/py-playtest)

A library for implementing framework to do virtual playtesting for
boardgames.

- Provide basic components to make it easy to create new prototypes

- Wraps an API around the game you created to integrate with [OpenAI gym](https://gym.openai.com/)
  or a default integration harness.

# A Quick Demo

To see a demo of this game, clone this repo and run:

```
pipenv install
PYTHONPATH=. pipenv shell example/play.py
```

And you will be able to use our interactive harness to play the game.

```
📢: Resetting game.

📢: Start of next round!

📢: Player 0 - it is your turn!

📢: Let's see your two card.

🤔: How much you want to bet?

Player 0 taking action...
{'discarded': [],
 'others': [{'bank': 10, 'bet': 0}],
 'self': {'bank': 10, 'bet': 0, 'hand': ['7h', '7s']}}
👀 Please enter action ([bet(0->10)]):
```

And you can continue playing the prototype.

You can observe the code that generates the game (in a few lines of python!)
in [pt-blackjack/game.py](pt-blackjack/game.py).

# Creating the AI

> Experimental feature: this is a very basic generic game AI that we built!

In play testing a game, one enemy is the problem with context switching between
different players. This makes it hard to understand your design from player's
prospective. This allows us to train a simple AI that is useful for testing the
game.

To create the bot, do:

```
PYTHONPATH=. pipenv shell example/train.py
```

Which will then output the bot to the a weight file (`<bot>.h5f`) folder. You can then
play against the bot by doing:

```
PYTHONPATH=. pipenv shell example/play.py --ai
```

Which then you can start the game against the AI from the loaded AI weight file.

# Getting started

To get started, read the docs at [here](#todo).

```
pip install playtest
```

Then can just `import playtest` and get started in creating your prototype.
