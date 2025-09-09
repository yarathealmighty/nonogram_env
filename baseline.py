import random
from nonogram_rl import NonogramEnv, TileState

def random_baseline(env: NonogramEnv):
    obs, _ = env.reset()
    rows, cols = env.rows, env.cols

    marked_tiles = set()

    step_count = 0
    while not env.board.is_solved():
        unmarked_positions = [
            (r, c) for r in range(rows) for c in range(cols)
            if (r, c) not in marked_tiles
        ]

        if not unmarked_positions:
            break

        r, c = random.choice(unmarked_positions)
        marked_tiles.add((r, c))

        solution_mark = env.board._solution_tilemap[r][c]
        mark = random.choice([TileState.FILLED, TileState.EMPTY])

        action_idx = 1 if mark == TileState.FILLED else 2

        obs, reward, terminated, truncated, info = env.step((r, c, action_idx))
        step_count += 1

        print(f"Step {step_count}: Marking tile ({r},{c}) as {mark.name}, Reward={reward}")
        points = env.render()

        if terminated:
            print("Puzzle solved!")
            break

    print(f"Finished in {step_count} steps, total points: {env.total_points}")


if __name__ == "__main__":
    total_points = 0
    runs = 200
    #0.98/0.2/1.65 15x15
    #0.33/-0.01/-0.36 10x10 - 200 runs
    #-0.62/-0.2/-0.5 5x5 - 200 runs
    for i in range(runs):
        env = NonogramEnv(rows=15, cols=15, seed=42)
        random_baseline(env)
        total_points += env.total_points
        env.close()
    print(f"Average points over {runs} runs: {total_points / runs}")