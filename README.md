# Poh-Tah-Toe - MENACE based Tic-Tac-Toe in Python!
Made by Potato GameDev on the Potato stream: https://www.twitch.tv/potatogamedev

## Description

This project is a simple implementation of the classic Tic-Tac-Toe game using Pygame, featuring an AI based on the MENACE (Machine Educable Noughts and Crosses Engine) algorithm. 
The AI can be trained through self-play to improve its performance over time.

## Why?

The motivation behind this project is to explore the concept of machine learning through a historical lens by implementing MENACE, one of the earliest examples of an AI for games.
MENACE was originally designed by Donald Michie in 1961 and serves as a fascinating case study in reinforcement learning.
This project aims to provide an educational and interactive way to understand the principles of AI and machine learning.

## Quick Start

To get started with the Poh-Tah-Toe game, follow these steps:

1. Clone the repository:
    ```bash
    git clone git@github.com:PotatoGameDev/poh-tah-toe.git
    cd poh-tah-toe
    ```
3. Run the game:
    ```bash
    python main.py
    ```

## Usage

The game can be run in two modes: interactive and training.

### Interactive Mode

To play against the MENACE-based AI interactively, simply run the game without any arguments:
```bash
python main.py
```

### Training Mode

To train the AI by having it play against itself, use the --training or --training-games arguments:

Run 1000 AI vs AI games in headless (no UI) mode:

```bash
python main.py --training
```

Run a specific number of AI vs AI games in headless (no UI) mode:
```
bash
python main.py --training-games 500
```

If you want to start with clean slate, delete knowledge.json file in the main project dir.


## Contributing

Contributions are welcome! If you have any improvements or suggestions, please fork the repository and create a pull request. Here are some areas where you can contribute:

    Enhancing the AI algorithm
    Improving the game UI
    Adding more features and functionalities
    Fixing bugs and issues

Please make sure to follow the standard Git workflow:

    Fork the repository
    Create a new branch (git checkout -b feature-branch)
    Commit your changes (git commit -m 'Add some feature')
    Push to the branch (git push origin feature-branch)
    Create a pull request
