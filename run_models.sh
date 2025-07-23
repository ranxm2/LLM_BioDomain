#!/bin/bash




python -m source.gemini.gemini_biodomain \
 --key_path keys/gemini_key.txt \
 --result_dir Experiment/Gemini/01-Reference_free/03-Name_strcuture_similarity/ 


python -m source.gemini.gemini_biodomain \
  --key_path keys/gemini_key.txt \
  --df_go_path data/go_root_paths.csv \
  --obo_path data/go-basic.obo \
  --similarity_path data/go_similarity.csv \
  --result_dir Experiment/Gemini/
  -




# deepseek



python -m source.deepseek.deepseek_biodomain \
  --key_path keys/deepseek_key.txt \
  --df_go_path data/go_root_paths.csv \
  --obo_path data/go-basic.obo \
  --similarity_path data/go_jaccard_long_filtered.csv \
  --result_dir Experiment/DeepSeek/



