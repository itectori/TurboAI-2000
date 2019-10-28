# TurboAI-2000

This is a small implementation (aka not optimized) of the Monte-Carlo Tree Search algorithm (MCTS).
This implementation is mostly based on [this paper](https://web.stanford.edu/~surag/posts/alphazero.html), which is a popularization of the AlphaZero's implementation.
On this repository, you can find multiple small games (Tic-Tac-Toe, Connect 4 ...) that the AI can learn by reinforcement.
Feel free to implement your own game!

## Requirements

* python >= 3.6

## Installation

Run the following script to install all dependencies and start the environment.

```bash
source setup.sh
```

## Usage

The entry point of the program is the `turboAI.py` file at the root of the repository.

```
Usage: python3 turboAI.py <command> [args...]
```

Here is the list of the available commands and their arguments:

| Command | arguments | description
|--|--|--|
| train | *game config ai* | Train the ai to play the given game. |
| play_humans | *game* | Start a game between 2 humans. |
| play_human_vs_ai | *game human_side ai* | Start a game against the given ai. **human_side** is either 1 or 2. |
| play_ais | *game ai_1 ai_2* | Start a game between 2 ais. |

For example, if you want to challenge your ai "Bobby" at connect 4, you have to do something like:

```bash
# Train Bobby to play Connect 4
python3 turboAI.py learn connect4 connect4/default.config Bobby

# Play against Bobby as player 2
python3 turboAI.py play_human_vs_ai connect4 2 Boby
```

## Implement your own game

`comming soon`
