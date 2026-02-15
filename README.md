# International Football Results Analysis

Analysis of international football match results from 1872 to 2026 using Python and Pandas.

## Dataset

The dataset contains **49,071 international football matches** sourced from [Kaggle](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017).

## Analysis Overview

### Basic Exploration
1. Total number of matches in the dataset
2. Earliest and latest year in the data
3. Number of unique countries
4. Most frequent home team

### Goals Analysis
5. Average goals per match
6. Highest scoring match
7. Home vs away goals comparison
8. Most common total goals value

### Match Results
9. Home win percentage
10. Does home advantage exist?
11. Country with most wins historically

### Visualizations
- **histogram_goals.png** - Distribution of goals per match
- **bar_match_outcomes.png** - Match outcomes (Home Win/Away Win/Draw)
- **top10_wins.png** - Top 10 countries by total wins

## Key Findings

| Metric | Value |
|--------|-------|
| Total Matches | 49,071 |
| Date Range | 1872 - 2026 |
| Unique Countries | 333 |
| Avg Goals/Match | 2.94 |
| Home Win % | 49.00% |
| Most Wins | Brazil (669) |

## Requirements

```
pandas
matplotlib
```

## Usage

```bash
python project.py
```

## Files

- `project.py` - Main analysis script
- `results.csv` - Match results dataset
- `former_names.csv` - Country name mappings (historical)
