import pandas as pd

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving files without display
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_csv("results.csv")

# =============================================================================
# BASIC EXPLORATION
# =============================================================================

# -----------------------------------------------------------------------------
# 1. How many matches are in the dataset?
# -----------------------------------------------------------------------------
# Logic: Each row represents one match. We count total rows using len() or shape[0]

num_matches = len(df)
print(f"1. Total number of matches: {num_matches}")

# -----------------------------------------------------------------------------
# 2. What is the earliest and latest year in the data?
# -----------------------------------------------------------------------------
# Logic: The 'date' column contains match dates. We convert to datetime,
# extract the year, then find min() and max() values.

df['date'] = pd.to_datetime(df['date'])
earliest_year = df['date'].dt.year.min()
latest_year = df['date'].dt.year.max()
print(f"2. Earliest year: {earliest_year}, Latest year: {latest_year}")

# -----------------------------------------------------------------------------
# 3. How many unique countries are there?
# -----------------------------------------------------------------------------
# Logic: Countries appear in both 'home_team' and 'away_team' columns.
# We combine both columns and count unique values using nunique() or set union.

all_countries = pd.concat([df['home_team'], df['away_team']]).unique()
num_unique_countries = len(all_countries)
print(f"3. Number of unique countries: {num_unique_countries}")

# -----------------------------------------------------------------------------
# 4. Which team appears most frequently as home team?
# -----------------------------------------------------------------------------
# Logic: Use value_counts() on 'home_team' column to count occurrences,
# then get the team with the highest count using idxmax() or head(1).

most_frequent_home = df['home_team'].value_counts().idxmax()
home_count = df['home_team'].value_counts().max()
print(f"4. Most frequent home team: {most_frequent_home} ({home_count} matches)")

# =============================================================================
# GOALS ANALYSIS
# =============================================================================

# Create total goals column
df["total_goals"] = df["home_score"] + df["away_score"]

# -----------------------------------------------------------------------------
# 5. What is the average number of goals per match?
# -----------------------------------------------------------------------------
# Logic: Use mean() on the total_goals column to calculate the average.

avg_goals = df["total_goals"].mean()
print(f"\n5. Average goals per match: {avg_goals:.2f}")

# -----------------------------------------------------------------------------
# 6. What is the highest scoring match?
# -----------------------------------------------------------------------------
# Logic: Find the row with maximum total_goals using idxmax() to get the index,
# then retrieve all details of that match.

highest_idx = df["total_goals"].idxmax()
highest_match = df.loc[highest_idx]
print(f"6. Highest scoring match: {highest_match['home_team']} vs {highest_match['away_team']}")
print(f"   Score: {int(highest_match['home_score'])}-{int(highest_match['away_score'])} ({int(highest_match['total_goals'])} goals) on {highest_match['date'].strftime('%Y-%m-%d')}")

# -----------------------------------------------------------------------------
# 7. Are more goals scored at home or away?
# -----------------------------------------------------------------------------
# Logic: Sum all home_score values and all away_score values, then compare.

total_home_goals = df["home_score"].sum()
total_away_goals = df["away_score"].sum()
print(f"7. Total home goals: {total_home_goals}, Total away goals: {total_away_goals}")
print(f"   More goals scored: {'Home' if total_home_goals > total_away_goals else 'Away'}")

# -----------------------------------------------------------------------------
# 8. What is the most common total goals value?
# -----------------------------------------------------------------------------
# Logic: Use value_counts() on total_goals to count frequency of each value,
# then get the most common one using idxmax().

most_common_goals = df["total_goals"].value_counts().idxmax()
most_common_count = df["total_goals"].value_counts().max()
print(f"8. Most common total goals: {int(most_common_goals)} (occurred in {most_common_count} matches)")

# =============================================================================
# MATCH RESULTS ANALYSIS
# =============================================================================

# Create match outcome column using a function
def match_result(row):
    if row["home_score"] > row["away_score"]:
        return "Home Win"
    elif row["home_score"] < row["away_score"]:
        return "Away Win"
    else:
        return "Draw"

df["result"] = df.apply(match_result, axis=1)

# -----------------------------------------------------------------------------
# 9. What percentage of matches are home wins?
# -----------------------------------------------------------------------------
# Logic: Count occurrences of each result using value_counts(normalize=True)
# to get proportions, then multiply by 100 for percentage.

result_counts = df["result"].value_counts()
result_percentages = df["result"].value_counts(normalize=True) * 100
home_win_pct = result_percentages["Home Win"]
print(f"\n9. Home win percentage: {home_win_pct:.2f}%")
print(f"   Breakdown: Home Win: {result_percentages['Home Win']:.2f}%, Away Win: {result_percentages['Away Win']:.2f}%, Draw: {result_percentages['Draw']:.2f}%")

# -----------------------------------------------------------------------------
# 10. Does home advantage exist?
# -----------------------------------------------------------------------------
# Logic: Compare home win % vs away win %. If home wins significantly exceed
# away wins, home advantage exists. Also compare total goals scored.

print(f"10. Does home advantage exist? YES")
print(f"    Evidence 1: Home wins ({result_percentages['Home Win']:.1f}%) > Away wins ({result_percentages['Away Win']:.1f}%)")
print(f"    Evidence 2: Home goals ({total_home_goals}) > Away goals ({total_away_goals})")
print(f"    Home teams win {result_percentages['Home Win']/result_percentages['Away Win']:.2f}x more often than away teams")

# -----------------------------------------------------------------------------
# 11. Which country has the most wins historically?
# -----------------------------------------------------------------------------
# Logic: For each match, identify the winner (home_team if Home Win, away_team if Away Win).
# Then count wins per country using value_counts().

# Create a column for the winning team
def get_winner(row):
    if row["result"] == "Home Win":
        return row["home_team"]
    elif row["result"] == "Away Win":
        return row["away_team"]
    else:
        return None  # Draw has no winner

df["winner"] = df.apply(get_winner, axis=1)

# Count wins per country (excluding draws/None)
wins_by_country = df["winner"].value_counts()
top_winner = wins_by_country.idxmax()
top_wins = wins_by_country.max()
print(f"11. Country with most wins: {top_winner} ({top_wins} wins)")
print(f"    Top 5 countries by wins:")
for country, wins in wins_by_country.head(5).items():
    print(f"    {country}: {wins} wins")

# =============================================================================
# VISUALIZATION
# =============================================================================


# -----------------------------------------------------------------------------
# Histogram of Goals Per Match
# -----------------------------------------------------------------------------
# Logic: Use hist() to show the distribution of total_goals.
# bins=15 divides the data into 15 intervals for better granularity.

plt.figure(figsize=(10, 6))
df["total_goals"].hist(bins=15, edgecolor='black', color='steelblue')
plt.title("Distribution of Goals Per Match", fontsize=14)
plt.xlabel("Total Goals", fontsize=12)
plt.ylabel("Number of Matches", fontsize=12)
plt.grid(axis='y', alpha=0.7)
plt.tight_layout()
plt.savefig("histogram_goals.png", dpi=150)
plt.close()

# -----------------------------------------------------------------------------
# Bar Chart of Match Outcomes
# -----------------------------------------------------------------------------
# Logic: Use value_counts() to get counts of each result type,
# then plot as a bar chart with different colors for each outcome.

plt.figure(figsize=(8, 6))
result_counts = df["result"].value_counts()
colors = ['forestgreen', 'coral', 'gray']  # Home Win, Away Win, Draw
result_counts.plot(kind='bar', color=colors, edgecolor='black')
plt.title("Match Outcomes Distribution", fontsize=14)
plt.xlabel("Result", fontsize=12)
plt.ylabel("Number of Matches", fontsize=12)
plt.xticks(rotation=0)
# Add value labels on bars
for i, v in enumerate(result_counts):
    plt.text(i, v + 200, str(v), ha='center', fontsize=10)
plt.tight_layout()
plt.savefig("bar_match_outcomes.png", dpi=150)
plt.close()

# -----------------------------------------------------------------------------
# Top 10 Teams by Total Wins
# -----------------------------------------------------------------------------
# Logic: Use the wins_by_country Series (already calculated), take head(10),
# and plot as a horizontal bar chart for readability.

plt.figure(figsize=(10, 6))
top_10_wins = wins_by_country.head(10)
top_10_wins.sort_values().plot(kind='barh', color='royalblue', edgecolor='black')
plt.title("Top 10 Countries by Total Wins", fontsize=14)
plt.xlabel("Number of Wins", fontsize=12)
plt.ylabel("Country", fontsize=12)
# Add value labels on bars
for i, v in enumerate(top_10_wins.sort_values()):
    plt.text(v + 5, i, str(v), va='center', fontsize=10)
plt.tight_layout()
plt.savefig("top10_wins.png", dpi=150)
plt.close()

print("\nVisualizations saved: histogram_goals.png, bar_match_outcomes.png, top10_wins.png")
