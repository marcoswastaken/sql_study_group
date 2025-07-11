# Week 3 Practice Solutions

## Dataset Overview

**Dataset:** [MLB Data](https://huggingface.co/datasets/TJStatsApps/mlb_data)

This dataset contains information about individual pitches or at-bats, including:

**Identifiers:**
- game_pk, game_date, batter_id, batter_name, pitcher_id, pitcher_name, ab_number

**Pitch/At-bat Details:**
- pitch_type, pitch_description, play_code, strikes_after, balls_after, outs_after, end_speed, start_speed, sz_bot, sz_top, p_direction, vz0, vy0, vx0, va0, event, event_type, rbi, away_score, home_score, is_pitch, is_play, is_strike, is_swing, is_out, is_ball, is_review, plate_time, extension, spin_rate, spin_direction, launch_speed, launch_angle, launch_location, trajectory, hardness, hit_x, hit_y, inning_play, pfx_x, pfx_z, px, pz, type_confidence

**Team Information:**
- batter_team_id, batter_team_name, pitcher_team_id, pitcher_team_name

**Handedness:**
- batter_hand, pitcher_hand

## Practice Questions with Solutions

### Question 1: Total Pitches by Pitcher

**Question:** How many pitches did each pitcher throw in total? List the pitcher's name and the total count of pitches.

**Expected Output Columns:** pitcher_name, total_pitches

```sql
SELECT pitcher_name, 
       COUNT(*) AS total_pitches
FROM train 
WHERE is_pitch = TRUE
GROUP BY pitcher_name
ORDER BY total_pitches DESC;
```

### Question 2: Average Exit Speed by Pitch Type

**Question:** What is the average end_speed (exit speed) for each pitch_type?

**Expected Output Columns:** pitch_type, average_end_speed

```sql
SELECT pitch_description, 
       AVG(end_speed) AS average_end_speed
FROM train 
WHERE is_pitch = TRUE 
  AND end_speed IS NOT NULL
GROUP BY pitch_description
ORDER BY average_end_speed DESC;
```

### Question 3: Batters with More Than 12000 At-Bats

**Question:** Find the batter_name of all batters who had more than 12000 at-bats (ab_number). Count each unique ab_number for a given batter.

**Expected Output Columns:** batter_name, total_at_bats

```sql
SELECT batter_name, 
       COUNT(*) AS total_at_bats
FROM train
GROUP BY batter_name
HAVING COUNT(*) > 12000
ORDER BY total_at_bats DESC;
```

### Question 4: Games with High Scoring Away Teams

**Question:** List game_pk and game_date for games where the away_score was ever greater than 5. (Note: away_score is likely a running score, so we're looking for any instance where it surpassed 5 in that game).

**Expected Output Columns:** game_pk, game_date

```sql
SELECT game_pk, 
       game_date
FROM train
GROUP BY game_pk, game_date
HAVING MAX(away_score) > 5
ORDER BY game_date DESC;
```

### Question 5: Pitchers with a High Number of "Strikeout" Events

**Question:** Identify pitcher_name who had more than 2 "strikeout" event_types.

**Expected Output Columns:** pitcher_name, strikeout_count

```sql
SELECT pitcher_name, 
       COUNT(*) AS strikeout_count
FROM train
WHERE event_type = 'Strikeout'
GROUP BY pitcher_name
HAVING COUNT(*) > 2
ORDER BY strikeout_count DESC;
```

### Question 6: Batter-Pitcher Matchups with At Least 3 Interactions

**Question:** Find pairs of batter_name and pitcher_name who faced each other at least 3 times (i.e., had at least 3 distinct ab_number interactions).

**Expected Output Columns:** batter_name, pitcher_name, interaction_count

```sql
SELECT batter_name, 
       pitcher_name, 
       COUNT(DISTINCT ab_number) AS interaction_count
FROM train
GROUP BY batter_name, pitcher_name
HAVING COUNT(DISTINCT ab_number) >= 3
ORDER BY interaction_count DESC;
```

### Question 7: Average Launch Speed for "Groundout" Events by Batter Handedness

**Question:** Calculate the average launch_speed for event_type 'Groundout', broken down by batter_hand.

**Expected Output Columns:** batter_hand, average_launch_speed

```sql
SELECT batter_hand, 
       AVG(launch_speed) AS average_launch_speed
FROM train
WHERE event_type = 'Groundout'
  AND launch_speed IS NOT NULL
GROUP BY batter_hand
ORDER BY average_launch_speed DESC;
```

### Question 8: Pitch Types with a Minimum Number of Occurrences and High Average Spin Rate

**Question:** Which pitch_types appear at least 5 times and have an AVG(spin_rate) greater than 2000?

**Expected Output Columns:** pitch_type, pitch_count, average_spin_rate

```sql
SELECT pitch_type, 
       COUNT(*) AS pitch_count, 
       AVG(spin_rate) AS average_spin_rate
FROM train
WHERE spin_rate IS NOT NULL
  AND is_pitch = TRUE
GROUP BY pitch_type
HAVING COUNT(*) >= 5 
  AND AVG(spin_rate) > 2000
ORDER BY average_spin_rate DESC;
```

### Question 9: Games with More Home Runs than Strikeouts

**Question:** Identify game_pk where the total count of event_type 'Home Run' is greater than the total count of event_type 'Strikeout'.

**Expected Output Columns:** game_pk

```sql
SELECT game_pk
FROM train
WHERE event_type IN ('Home Run', 'Strikeout')
GROUP BY game_pk
HAVING SUM(CASE WHEN event_type = 'Home Run' THEN 1 ELSE 0 END) > 
       SUM(CASE WHEN event_type = 'Strikeout' THEN 1 ELSE 0 END)
ORDER BY game_pk;
```

### Question 10: Pitcher Hand vs. Batter Hand Matchups with High Average Launch Angle

**Question:** For each unique combination of pitcher_hand and batter_hand, find the average launch_angle. Only include combinations where the average launch_angle is greater than 15 degrees and there are at least 10 occurrences of that matchup.

**Expected Output Columns:** pitcher_hand, batter_hand, average_launch_angle

```sql
SELECT pitcher_hand, 
       batter_hand, 
       AVG(launch_angle) AS average_launch_angle
FROM train
WHERE launch_angle IS NOT NULL
GROUP BY pitcher_hand, batter_hand
HAVING AVG(launch_angle) > 15 
  AND COUNT(*) >= 10
ORDER BY average_launch_angle DESC;
``` 