# Nonogram RL Environment

This project implements a **Nonogram (Picross) environment** for reinforcement learning in Python.  
It includes:

- A `Board` class to generate and manage Nonogram puzzles.
- A Gym-compatible `NonogramEnv` environment.
- ANSI-rendered board with **hints, colored 3x3 tiles, and cumulative points**.
- A baseline random agent example.

---

## Folder Structure

```
nonogram_rl/
│── __init__.py        # Package initialization
│── board.py           # TileState enum and Board class
│── env.py             # Gym environment wrapper
baseline.py  # Simple baseline agent
```

---

## Requirements

- Python 3.9+
- `gymnasium` library
- `numpy`

Install dependencies:

```bash
pip install gymnasium numpy
```

*Optional for Windows terminals*: If ANSI colors don’t display correctly, install `colorama`:

```bash
pip install colorama
```

---

## Usage

### Run the random baseline agent

```bash
python baseline.py
```

This will:

- Randomly mark each tile (never unmarked)
- Avoid re-marking tiles
- Render the board after each step
- Print reward and cumulative points
- Stop when the puzzle is solved

---

### Example code for using the environment

```python
from nonogram_rl import NonogramEnv, TileState

# Create environment
env = NonogramEnv(rows=5, cols=5, seed=42)

obs, _ = env.reset()
env.render()

# Take an example action
# Mark tile at row=0, col=0 as FILLED
for i in range(5):
    for j in range(5):
        action = (i, j, 1)  # (row, col, mark_index) -> 0=UNMARKED, 1=FILLED, 2=EMPTY
        obs, reward, terminated, truncated, info = env.step(action)

        print("After action:")
        env.render()
        print(f"Reward: {reward}")
```

---