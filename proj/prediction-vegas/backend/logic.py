import pandas as pd
import requests
import nflreadpy as nfl
from datetime import datetime
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf
import os
import random
import math

def logic(years, player, pTeamA, cTeamA, currentW, currentY, PREDICT2, csv):
  all_teams = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB":  "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KC":  "Kansas City Chiefs",
    "LV":  "Las Vegas Raiders",
    "LAC": "Los Angeles Chargers",
    "LA": "Los Angeles Rams",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE":  "New England Patriots",
    "NO":  "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SF":  "San Francisco 49ers",
    "SEA": "Seattle Seahawks",
    "TB":  "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Commanders"
  }
  pTeam = all_teams[pTeamA]
  # Load player game-level stats for multiple seasons
  player_stats = nfl.load_player_stats(years) #just add commas and extra years for more years
  # Load all available team level stats
  team_stats = nfl.load_team_stats(seasons=True)
  # nflreadpy uses Polars instead of pandas. Convert to pandas if needed:
  ps_pandas = player_stats.to_pandas()
  ts_pandas = team_stats.to_pandas()
  # ========
  # new set
  # ========
  # cleaning up the data, getting rid of unnecessary stats and positions
  remove = ["player_name", "game_id", "headshot_url", "season_type", "player_id", 
            "position", "team",
            "sacks_suffered", "sack_yards_lost", "sack_fumbles",
            "sack_fumbles_lost", "passing_first_downs", "passing_2pt_conversions",
            "rushing_fumbles", "rushing_fumbles_lost", "rushing_first_downs",
            "rushing_2pt_conversions", "receiving_fumbles", "receiving_fumbles_lost",
            "receiving_first_downs", "receiving_2pt_conversions", "def_tackles_solo",
            "def_tackles_with_assist", "def_tackle_assists", "def_tackles_for_loss",
            "def_tackles_for_loss_yards", "def_fumbles_forced", "def_sacks",
            "def_sack_yards", "def_qb_hits", "def_interceptions", "def_interception_yards",
            "def_pass_defended", "def_tds", "def_fumbles", "def_safeties", "fumble_recovery_own",
            "fumble_recovery_yards_own", "fumble_recovery_opp", "fumble_recovery_yards_opp",
            "fumble_recovery_tds", "penalties", "penalty_yards", "fg_made", "fg_att", "fg_missed",
            "fg_blocked", "fg_long", "fg_pct", "fg_made_0_19", "fg_made_20_29", "fg_made_30_39",
            "fg_made_40_49", "fg_made_50_59", "fg_made_60_", "fg_missed_0_19", "fg_missed_20_29",
            "fg_missed_30_39", "fg_missed_40_49", "fg_missed_50_59", "fg_missed_60_",
            "fg_made_list", "fg_missed_list", "fg_blocked_list", "fg_made_distance",
            "fg_missed_distance", "fg_blocked_distance", "pat_made", "pat_att", "pat_missed",
            "pat_blocked", "pat_pct", "gwfg_made", "gwfg_att", "gwfg_missed", "gwfg_blocked",
            "gwfg_distance", "special_teams_tds", "misc_yards", "punt_returns",
            "punt_return_yards", "kickoff_returns", "kickoff_return_yards", "air_yards_share",
            "wopr", "fantasy_points" , "fantasy_points_ppr", "rushing_epa",
            "receptions", "targets", "receiving_tds", "receiving_air_yards", 
            "receiving_yards_after_catch", "receiving_epa", "racr", "target_share",
            "carries", "rushing_tds", 
            "completions", "attempts", "passing_tds", "passing_interceptions",
            "passing_air_yards", "passing_yards_after_catch", "passing_epa",
            "passing_cpoe", "pacr"]

  bad_positions = ["SPEC", "DL", "OL", "DB", "LB"]
  ps_new = ps_pandas.drop(remove, axis=1)
  for i in bad_positions:
    ps_new = ps_new[ps_new["position_group"] != i]
  ps_new = ps_new[ps_new["player_display_name"] == player]
  mahTeam = ps_new

  if ps_new.iloc[0]["position_group"] == "QB":
    removeN = ["rushing_yards", "receiving_yards"]
    goal = "passing_yards"

  if ps_new.iloc[0]["position_group"] == "RB":
    removeN = ["passing_yards", "receiving_yards"]
    goal = "rushing_yards"

  if ps_new.iloc[0]["position_group"] == "WR" or ps_new.iloc[0]["position_group"] == "TE" :
    removeN = ["passing_yards", "rushing_yards"]
    goal = "receiving_yards"
  ps_new = ps_new.drop(removeN, axis=1)
  # cleaning up and formatting data
  mahDF = ps_new.to_numpy()
  MAH = pd.DataFrame(np.array(mahDF), columns=ps_new.columns)
  mahTeam = pd.DataFrame(np.array(mahTeam), columns=mahTeam.columns)
  MAH = MAH[MAH["week"] <= 18]
  mahTeam = mahTeam[mahTeam["week"] <= 18]
  # ========
  # new set
  # ========
  scores = []
  for a in range(len(mahTeam.index)):
      target_opponent = mahTeam.iloc[a]['opponent_team']
      current_week = mahTeam.iloc[a]['week']
      current_season = mahTeam.iloc[a]['season']
      stat_allowed_list = []
      # Filter ts_pandas for the opponent's historical game rows
      opponent_history = ts_pandas[
          (ts_pandas['team'] == target_opponent) &
          (ts_pandas['season'] == current_season) &
          (ts_pandas['week'] <= current_week) &
          (ts_pandas['week'] > (current_week - 7))
      ].copy()
      # Iterate through the opponent's recent games to find the stat they allowed
      for _, game_row in opponent_history.iterrows():
          historical_opponent_team = game_row["opponent_team"]
          historical_week = game_row['week']
          # Look up the stat for that team in that specific week
          player_stats = ts_pandas[
              (ts_pandas['team'] == historical_opponent_team) &
              (ts_pandas['team'] != target_opponent) &
              (ts_pandas['season'] == current_season) &
              (ts_pandas['week'] == historical_week)
          ]
          if not player_stats.empty:
              stat_value = player_stats.iloc[0][goal]
              stat_allowed_list.append(stat_value)
          elif historical_week == 1:
              stat_allowed_list.append(0)
      # Calculate the average of the collected stats allowed
      if stat_allowed_list:
          average_stat = np.mean(stat_allowed_list)
          scores.append(int(average_stat))
  MAH['d_rank'] = scores
  # ========
  # new set
  # ========
  MAH_filtered = MAH.copy()
  # Load the CSV
  csv_df = pd.read_csv(csv)
  # Parse the CSV columns into (week, year) pairs, skipping the first 3 identifier columns
  week_columns = {}
  for col in csv_df.columns[3:]:
      parts = col.replace('Week ', '').split(', ')
      week_num = int(parts[0])
      year = int(parts[1])
      week_columns[col] = (week_num, year)
  # Get the player's row from the CSV using MAH's player name
  player_name = MAH_filtered['player_display_name'].iloc[0]
  csv_row = csv_df[csv_df['Player'].str.strip() == player_name.strip()]
  if csv_row.empty:
      print(f"Player '{player_name}' not found in CSV")
  else:
      csv_row = csv_row.iloc[0]
      # Build a mapping of (week, year) -> stat value from the CSV
      csv_week_map = {}
      for col, (week_num, year) in week_columns.items():
          val = csv_row[col]
          if pd.isna(val) or val == 0:
              csv_week_map[(week_num, year)] = None
          else:
              csv_week_map[(week_num, year)] = val
      # Map each row in MAH_filtered to the corresponding CSV value
      new_col = []
      rows_to_drop = []
      for i, row in MAH_filtered.iterrows():
          key = (int(row['week']), int(row['season']))
          val = csv_week_map.get(key, None)

          if val is None:
              rows_to_drop.append(i)
          else:
              new_col.append((i, val))
      # Drop rows where CSV had 0 or no data
      MAH_filtered = MAH_filtered.drop(index=rows_to_drop).reset_index(drop=True)
      # Add the new column to the trimmed MAH_filtered
      MAH_filtered['vegas'] = [v for _, v in new_col]
  MAH_filtered = MAH_filtered.dropna()
  MAHp = MAH_filtered.copy()
  # ========
  # new set
  # ========
  # List to hold the passing yards allowed for the last 7 games
  yards_allowed_list = []
  # Filter ts_pandas for the opponent's historical game rows
  targetTeam = ts_pandas[
      (ts_pandas['team'] == cTeamA) &
      (ts_pandas['season'] == currentY) &
      (ts_pandas['week'] <= (currentW - 1)) &
      (ts_pandas['week'] > (currentW - 7))
  ].copy()
  # Iterate through the opponent's last 7 games to find the yards they let up
  for _, game_row in targetTeam.iterrows():
      historical_passer_team = game_row["opponent_team"]
      historical_week = game_row['week']
      # Look up the offensive stats for that team in that specific week
      # This is the amount of goal yards the opponent allowed (the opponent's opponent's goal yards).
      passer_stats = ts_pandas[
          (ts_pandas['team'] == historical_passer_team) &
          (ts_pandas['team'] != cTeamA) &
          (ts_pandas['season'] == currentY) &
          (ts_pandas['week'] == historical_week)
      ]
      if not passer_stats.empty:
          yds = passer_stats.iloc[0][goal]
          yards_allowed_list.append(yds)
  # Calculate the average of the collected yards allowed
  average_yards = np.mean(yards_allowed_list)
  PREDICT = int(average_yards)
  MAHp = MAHp.drop(["season", "week", "player_display_name", "position_group", "opponent_team"], axis=1)
  # ========
  # new set
  # ========
  SEED_VALUE = 42
  os.environ['PYTHONHASHSEED'] = str(SEED_VALUE)
  random.seed(SEED_VALUE)
  np.random.seed(SEED_VALUE)
  tf.keras.utils.set_random_seed(SEED_VALUE)
  # actual ML stuff
  # -----
  #
  # edit the value of "games" variable, tinker with it to get more accurate results
  #
  # -----
  games = 3 # Look-back window (Timesteps)
  stats = MAHp.shape[1] # Number of features ex ('tar', 'rec', 'yar', 'td')
  target_col = goal # The stat we are predicting
  # SCALING AND PREPROCESSING
  features = MAHp[MAHp.columns].values
  target = MAHp[target_col].values.reshape(-1, 1)
  # Initialize scalers
  feature_scaler = MinMaxScaler(feature_range=(0, 1))
  target_scaler = MinMaxScaler(feature_range=(0, 1))
  # Scale the data
  scaled_features = feature_scaler.fit_transform(features)
  scaled_target = target_scaler.fit_transform(target)
  # TIME-SERIES TRANSFORMATION (WINDOWING)
  def create_sequences(data, target_data, timesteps):
      X, y = [], []
      for i in range(len(data) - timesteps):
          # X: sequence of 'timesteps' entries (Games i to i+timesteps-1)
          X.append(data[i:(i + timesteps)])
          # y: the target value at the next step (Game i+timesteps)
          y.append(target_data[i + timesteps])
      return np.array(X), np.array(y)
  X_data, y_data = create_sequences(scaled_features, scaled_target, games)
  # The seeding above ensures that random operations like this will be the same
  split_idx = int(len(X_data) * 0.8)
  # Split the small dataset (e.g., use the last 2 samples for testing/validation)
  X_train = X_data[:split_idx]
  y_train = y_data[:split_idx]
  X_val = X_data[split_idx:]
  y_val = y_data[split_idx:]
  # MODEL ARCHITECTURE (As in your image)
  model = Sequential()
  model.add(LSTM(
      units=50, # Number of neurons in the layer
      return_sequences=False,
      input_shape=(games, stats)
  ))
  # Dropout uses randomness controlled by the seed
  model.add(Dropout(0.5))
  model.add(Dense(units=1, activation='linear'))
  # MODEL COMPILATION (As in your image)
  model.compile(
      optimizer='adam',
      loss='mean_squared_error',
      metrics=['mae']
  )
  early_stop = EarlyStopping(
      monitor='val_loss', # Watch the validation loss
      patience=20,        # Stop after 20 epochs with no improvement
      verbose=0,
      restore_best_weights=True # Keep the best model weights found
  )
  # MODEL TRAINING
  print("Starting Model Training...")
  history = model.fit(
      X_train,
      y_train,
      epochs=200, # A typical number for a small dataset to start
      batch_size = min(256, len(X_train) // 10),
      validation_data=(X_val, y_val),
      callbacks=[early_stop],
      verbose=0
  )
  print("Model Training Complete.")
  # Prepare the historical data (The last 3 games from the original features)
  last_games_historical = features[-games:].copy()
    # Create a placeholder for the next game
  next_game_placeholder = last_games_historical[-1].copy()
  # Set the 'tar' column (index 0) to our user-defined value
  D_index = MAHp.columns.get_loc('d_rank')
  yar_index = MAHp.columns.get_loc(goal)
  VEGAS_index = MAHp.columns.get_loc('vegas')
  # Set the specific condition
  next_game_placeholder[D_index] = PREDICT
  next_game_placeholder[VEGAS_index] = PREDICT2
  # set yard to 0, the model will ignore these specific values for the game
  next_game_placeholder[yar_index] = 0.0
  # Combine historical sequence with the conditional game data
  # The X_predict input must be a sequence of games.
  # We use the previous few games, and the partially-defined next game.
  X_predict_input = np.vstack([last_games_historical[1:], next_game_placeholder.reshape(1, -1)])
  # Scale and Reshape the final input
  X_predict_scaled = feature_scaler.transform(X_predict_input)
  X_predict_final = X_predict_scaled.reshape(1, games, stats) # Shape: (1, 3, 11)
  # Get the scaled prediction
  scaled_prediction = model.predict(X_predict_final, verbose=0)
  # Inverse transform to get the actual yardage number
  prediction = target_scaler.inverse_transform(scaled_prediction)
  final_prediction = prediction[0][0]

  return round(float(final_prediction),2)
