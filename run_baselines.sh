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
uv run -m baselines.Qwen post_process
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines/Qwen3-0.6B-No-Thinking/seed_2025.jsonl"
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines/Qwen3-0.6B-No-Thinking/seed_42.jsonl"
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/Qwen3-0.6B-No-Thinking/seed_42-post.json' \
  --leaderboard_path './Experiment/00-Baselines/Qwen3-0.6B-No-Thinking/seed_42-post.csv' \
  --method_name 'Qwen3-06B-No-Thinking_seed_42'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/Qwen3-0.6B-No-Thinking/seed_27-post.json' \
  --leaderboard_path './Experiment/00-Baselines/Qwen3-0.6B-No-Thinking/seed_27-post.csv' \
  --method_name 'Qwen3-06B-No-Thinking_seed_27'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/Qwen3-0.6B-No-Thinking/seed_2025-post.json' \
  --leaderboard_path './Experiment/00-Baselines/Qwen3-0.6B-No-Thinking/seed_2025-post.csv' \
  --method_name 'Qwen3-06B-No-Thinking_seed_2025'

# Qwen3-8B
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines/Qwen3-8B-No-Thinking/seed_27.jsonl"
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines/Qwen3-8B-No-Thinking/seed_2025.jsonl"
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines/Qwen3-8B-No-Thinking/seed_42.jsonl"

uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/Qwen3-8B-No-Thinking/seed_42-post.json' \
  --leaderboard_path './Experiment/00-Baselines/Qwen3-8B-No-Thinking/seed_42-post.csv' \
  --method_name 'Qwen3-8B-No-Thinking_seed_42'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/Qwen3-8B-No-Thinking/seed_27-post.json' \
  --leaderboard_path './Experiment/00-Baselines/Qwen3-8B-No-Thinking/seed_27-post.csv' \
  --method_name 'Qwen3-8B-No-Thinking_seed_27'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines/Qwen3-8B-No-Thinking/seed_2025-post.json' \
  --leaderboard_path './Experiment/00-Baselines/Qwen3-8B-No-Thinking/seed_2025-post.csv' \
  --method_name 'Qwen3-8B-No-Thinking_seed_2025'



# ====== FXS ======
# EditDist
uv run -m baselines.LevED main \
  --output_dir "./Experiment/00-Baselines-FXS/LevEditDist" \
  --dataset_path "./data/FXS_bidomain_annotation_certain_formatted.csv" \
  --biodomain_type "FXS"
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/LevEditDist/seed_42.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/LevEditDist/seed_42.csv' \
  --method_name 'LevED_seed_42'

# SapBERT
uv run -m baselines.SapBERT main \
  --output_dir "./Experiment/00-Baselines-FXS/SapBERT" \
  --dataset_path "./data/FXS_bidomain_annotation_certain_formatted.csv" \
  --biodomain_type "FXS"
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/SapBERT/seed_42.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/SapBERT/seed_42.csv' \
  --method_name 'SapBERT_seed_42'

# Eval Qwen
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines-FXS/Qwen3-0.6B-No-Thinking/seed_27.jsonl"
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines-FXS/Qwen3-0.6B-No-Thinking/seed_2025.jsonl"
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines-FXS/Qwen3-0.6B-No-Thinking/seed_42.jsonl"
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/Qwen3-0.6B-No-Thinking/seed_42-post.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/Qwen3-0.6B-No-Thinking/seed_42-post.csv' \
  --method_name 'Qwen3-06B-No-Thinking_seed_42'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/Qwen3-0.6B-No-Thinking/seed_27-post.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/Qwen3-0.6B-No-Thinking/seed_27-post.csv' \
  --method_name 'Qwen3-06B-No-Thinking_seed_27'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/Qwen3-0.6B-No-Thinking/seed_2025-post.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/Qwen3-0.6B-No-Thinking/seed_2025-post.csv' \
  --method_name 'Qwen3-06B-No-Thinking_seed_2025'
# 8B
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines-FXS/Qwen3-8B-No-Thinking/seed_27.jsonl"
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines-FXS/Qwen3-8B-No-Thinking/seed_2025.jsonl"
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines-FXS/Qwen3-8B-No-Thinking/seed_42.jsonl"
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/Qwen3-8B-No-Thinking/seed_42-post.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/Qwen3-8B-No-Thinking/seed_42-post.csv' \
  --method_name 'Qwen3-06B-No-Thinking_seed_42'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/Qwen3-8B-No-Thinking/seed_27-post.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/Qwen3-8B-No-Thinking/seed_27-post.csv' \
  --method_name 'Qwen3-06B-No-Thinking_seed_27'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/Qwen3-8B-No-Thinking/seed_2025-post.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/Qwen3-8B-No-Thinking/seed_2025-post.csv' \
  --method_name 'Qwen3-06B-No-Thinking_seed_2025'
# 0.6B Thinking
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines-FXS/Qwen3-0.6B/seed_27.jsonl" --biodomain_type "FXS"
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines-FXS/Qwen3-0.6B/seed_2025.jsonl" --biodomain_type "FXS"
uv run -m baselines.Qwen post_process --result_path "./Experiment/00-Baselines-FXS/Qwen3-0.6B/seed_42.jsonl" --biodomain_type "FXS"
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/Qwen3-0.6B/seed_42-post.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/Qwen3-0.6B/seed_42-post.csv' \
  --method_name 'Qwen3-06B_seed_42'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/Qwen3-0.6B/seed_27-post.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/Qwen3-0.6B/seed_27-post.csv' \
  --method_name 'Qwen3-06B_seed_27'
uv run python -m baselines.eval eval \
  --result_path './Experiment/00-Baselines-FXS/Qwen3-0.6B/seed_2025-post.json' \
  --leaderboard_path './Experiment/00-Baselines-FXS/Qwen3-0.6B/seed_2025-post.csv' \
  --method_name 'Qwen3-06B_seed_2025'