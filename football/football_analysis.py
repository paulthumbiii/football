import pandas as pd
import matplotlib.pyplot as plt

# --- STEP 1: LOAD THE CSV ---
try:
    df = pd.read_csv("results.csv")
    # Convert date to datetime objects
    df["date"] = pd.to_datetime(df["date"])
    print("--- 1. File Loaded Successfully ---\n")
except FileNotFoundError:
    print("Error: 'results.csv' not found. Ensure it is in the same folder as this script.")
    exit()

# --- BASIC EXPLORATION ---
print("--- BASIC EXPLORATION ---")
# 1. Total matches
print(f"Total matches: {df.shape[0]}")

# 2. Earliest and latest year
print(f"Earliest Year: {df['date'].dt.year.min()}")
print(f"Latest Year: {df['date'].dt.year.max()}")

# 3. Unique countries (teams)
unique_teams = pd.concat([df['home_team'], df['away_team']]).nunique()
print(f"Unique Teams: {unique_teams}")

# 4. Most frequent home team
most_home = df["home_team"].value_counts().head(1)
print(f"Most frequent home team:\n{most_home}\n")


# --- GOALS ANALYSIS ---
print("--- GOALS ANALYSIS ---")
df["total_goals"] = df["home_score"] + df["away_score"]

# 1. Average goals
print(f"Average goals per match: {df['total_goals'].mean():.2f}")

# 2. Highest scoring match
high_score = df.loc[df['total_goals'].idxmax()]
print(f"Highest scoring match: {high_score['home_team']} vs {high_score['away_team']} ({high_score['total_goals']} goals)")

# 3. Home vs Away goals
home_sum = df['home_score'].sum()
away_sum = df['away_score'].sum()
print(f"Total Home Goals: {home_sum}")
print(f"Total Away Goals: {away_sum}")
print("More goals are scored at HOME" if home_sum > away_sum else "More goals scored AWAY")

# 4. Most common total goals
print(f"Most common total goals: {df['total_goals'].mode()[0]}\n")


# --- MATCH RESULTS ---
print("--- MATCH RESULTS ---")
def match_result(row):
    if row["home_score"] > row["away_score"]:
        return "Home Win"
    elif row["home_score"] < row["away_score"]:
        return "Away Win"
    else:
        return "Draw"

df["result"] = df.apply(match_result, axis=1)

# 1. Percentage of home wins
home_win_pct = (df["result"] == "Home Win").mean() * 100
print(f"Percentage of home wins: {home_win_pct:.2f}%")

# 2. Does home advantage exist?
# If home wins > away wins, then yes.
away_win_pct = (df["result"] == "Away Win").mean() * 100
if home_win_pct > away_win_pct:
    print(f"Yes, home advantage exists (Home: {home_win_pct:.1f}% vs Away: {away_win_pct:.1f}%)")

# 3. Most wins historically
def get_winner(row):
    if row["result"] == "Home Win": return row["home_team"]
    if row["result"] == "Away Win": return row["away_team"]
    return "None"

df["winner"] = df.apply(get_winner, axis=1)
most_wins = df[df["winner"] != "None"]["winner"].value_counts().idxmax()
print(f"Country with most wins: {most_wins}\n")


# --- VISUALIZATION ---
print("Closing charts will allow the script to continue...")

# 1. Histogram of goals
plt.figure(figsize=(10, 5))
df["total_goals"].hist(bins=20, color='skyblue', edgecolor='black')
plt.title("Distribution of Goals Per Match")
plt.xlabel("Total Goals")
plt.ylabel("Frequency")
plt.show()

# 2. Bar chart of outcomes
plt.figure(figsize=(8, 5))
df["result"].value_counts().plot(kind='bar', color=['green', 'orange', 'blue'])
plt.title("Match Outcomes")
plt.ylabel("Count")
plt.show()

# 3. Top 10 teams by total wins
plt.figure(figsize=(12, 6))
df[df["winner"] != "None"]["winner"].value_counts().head(10).plot(kind='bar', color='gold')
plt.title("Top 10 Teams by Historical Wins")
plt.ylabel("Total Wins")
plt.show()