# Random Ranker
uv run python -m baselines.random_ranker main --seed 42
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

  # Graph Traversal
  uv run python -m baselines.graph_traversal main --seed 42
  uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/graph_traversal/seed_42.json' \
  --leaderboard_path './Experiment/00-Baselines/graph_traversal/seed_42_leaderboard.csv' \
  --method_name 'random_seed_42'

  uv run python -m baselines.graph_traversal main --seed 27
  uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/graph_traversal/seed_27.json' \
  --leaderboard_path './Experiment/00-Baselines/graph_traversal/seed_27_leaderboard.csv' \
  --method_name 'random_seed_27'

  uv run python -m baselines.graph_traversal main --seed 2025
  uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/graph_traversal/seed_2025.json' \
  --leaderboard_path './Experiment/00-Baselines/graph_traversal/seed_2025_leaderboard.csv' \
  --method_name 'random_seed_2025'


# Edit Distance
uv run -m baselines.LevED main
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/LevEditDist/seed_42.json' \
  --leaderboard_path './Experiment/00-Baselines/LevEditDist/seed_42.csv' \
  --method_name 'LevED_seed_42'

# SapBERT
uv run -m baselines.SapBERT main
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/SapBERT/seed_42.json' \
  --leaderboard_path './Experiment/00-Baselines/SapBERT/seed_42.csv' \
  --method_name 'SapBERT_seed_42'

# Qwen3-0.6B
nohup uv run -m baselines.Qwen main > Qwen3-0.6B.log 2>&1 &