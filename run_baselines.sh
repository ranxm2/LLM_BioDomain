uv run python -m baselines.random_ranker main
uv run python -m baselines.eval eval

uv run python -m baselines.random_ranker main --seed 27
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/random/seed_27.json' \
  --leaderboard_path './Experiment/00-Baselines/random/seed_27_leaderboard.csv' \
  --method_name 'random_seed_27'

uv run python -m baselines.random_ranker main --seed 2025
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/random/seed_2025.json' \
  --leaderboard_path './Experiment/00-Baselines/random/seed_2025_leaderboard.csv' \
  --method_name 'random_seed_2025'