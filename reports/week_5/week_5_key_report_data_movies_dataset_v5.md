# Week 5 Practice - Movies Dataset

**Description:** Advanced JOIN operations, subqueries, and Common Table Expressions (CTEs) using real-world movie data with ratings, languages, and temporal information
**Database:** data_movies_dataset.db
**Total Exercises:** 5
**Focus Topics:** SELF JOIN, Subqueries (scalar, WHERE, SELECT, FROM), CTEs (WITH clause), Advanced data analysis, Real-world data quality handling

*Report generated on: 2025-07-16 16:41:11*

---

## Exercise 1: Exceptional Movies Among Excellent Ratings

**Difficulty:** Medium
**Topics:** Scalar subquery, Correlated subquery, AVG function, Multiple JOINs, Threshold filtering

### Problem Statement

Identify the standout performers among movies with 'Excellent' ratings. Find movies that are significantly more popular than the typical excellent movie - specifically those with popularity at least 500 points above the average for all excellent-rated movies. Display the movie title, popularity score, rating category, and the amount by which they exceed the excellent average. Order results by the excess amount in descending order.

### SQL Solution

```sql
SELECT
    m.title,
    m.popularity,
    r.rating_category,
    ROUND(m.popularity - (
        SELECT AVG(m2.popularity)
        FROM movies m2
        JOIN movie_ratings mr2 ON m2.movie_id = mr2.movie_id
        JOIN ratings r2 ON mr2.rating_id = r2.rating_id
        WHERE r2.rating_category = 'Excellent'
            AND m2.popularity IS NOT NULL
    ), 2) AS above_average_by
FROM movies m
JOIN movie_ratings mr ON m.movie_id = mr.movie_id
JOIN ratings r ON mr.rating_id = r.rating_id
WHERE r.rating_category = 'Excellent'
    AND m.popularity IS NOT NULL
    AND m.popularity > (
        SELECT AVG(m2.popularity) + 500
        FROM movies m2
        JOIN movie_ratings mr2 ON m2.movie_id = mr2.movie_id
        JOIN ratings r2 ON mr2.rating_id = r2.rating_id
        WHERE r2.rating_category = 'Excellent'
            AND m2.popularity IS NOT NULL
    )
ORDER BY above_average_by DESC;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.095s
- **Rows returned:** 4
- **Columns:** title, popularity, rating_category, above_average_by

#### Top 20 Results

| title | popularity | rating_category | above_average_by |
| --- | --- | --- | --- |
| Spider-Man: No Way Home | 5083.95 | Excellent | 5007.50 |
| The Batman | 3827.66 | Excellent | 3751.21 |
| Sing 2 | 1112.90 | Excellent | 1036.45 |
| The Seven Deadly Sins: Cursed by Light | 647.54 | Excellent | 571.09 |

---

## Exercise 2: Decade Champions

**Difficulty:** Hard
**Topics:** Table JOIN, Reference table usage, MAX function, Correlated subquery, Date range filtering

### Problem Statement

Determine which movie achieved the highest popularity in each decade. Your analysis should span from the 1980s through the 2020s, showing the decade name, the champion movie's title, and its popularity score. Only include decades that have movies in the database. Results should be ordered chronologically by decade.

### SQL Solution

```sql
SELECT
    d.decade_name,
    m.title AS most_popular_movie,
    m.popularity AS max_popularity
FROM decades d
JOIN movies m ON CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) BETWEEN d.decade_start AND d.decade_end
WHERE m.popularity IS NOT NULL
    AND SUBSTR(m.release_date, 1, 4) ~ '^[0-9]{4}$'
    AND m.popularity = (
        SELECT MAX(m2.popularity)
        FROM movies m2
        WHERE CAST(SUBSTR(m2.release_date, 1, 4) AS INTEGER) BETWEEN d.decade_start AND d.decade_end
            AND m2.popularity IS NOT NULL
            AND SUBSTR(m2.release_date, 1, 4) ~ '^[0-9]{4}$'
    )
ORDER BY d.decade_start;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.007s
- **Rows returned:** 5
- **Columns:** decade_name, most_popular_movie, max_popularity

#### Top 20 Results

| decade_name | most_popular_movie | max_popularity |
| --- | --- | --- |
| 1980s | Exploits of a Young Don Juan | 396.95 |
| 1990s | Toy Story | 171.71 |
| 2000s | Avatar | 297.36 |
| 2010s | Avengers: Infinity War | 338.40 |
| 2020s | Spider-Man: No Way Home | 5083.95 |

---

## Exercise 3: Recent Movie Popularity Extremes

**Difficulty:** Medium
**Topics:** SELF JOIN, Comparison operators, Calculated fields, NULL handling, Date filtering

### Problem Statement

Analyze popularity extremes in recent movie releases from 2015 to 2025. For each year, identify both the most and least popular movies released. Your result should show the release year, both movie titles with their popularity scores, and calculate the popularity gap between them. Only include years that released at least 5 movies. Results should be ordered chronologically by year.

### SQL Solution

```sql
SELECT
    CAST(SUBSTR(m1.release_date, 1, 4) AS INTEGER) AS release_year,
    m1.title AS most_popular_movie,
    m1.popularity AS highest_popularity,
    m2.title AS least_popular_movie,
    m2.popularity AS lowest_popularity,
    (m1.popularity - m2.popularity) AS popularity_gap
FROM movies m1
JOIN movies m2 ON SUBSTR(m1.release_date, 1, 4) = SUBSTR(m2.release_date, 1, 4)
    AND m1.movie_id != m2.movie_id
WHERE m1.popularity = (
    SELECT MAX(m3.popularity)
    FROM movies m3
    WHERE SUBSTR(m3.release_date, 1, 4) = SUBSTR(m1.release_date, 1, 4)
        AND m3.popularity IS NOT NULL
)
AND m2.popularity = (
    SELECT MIN(m4.popularity)
    FROM movies m4
    WHERE SUBSTR(m4.release_date, 1, 4) = SUBSTR(m2.release_date, 1, 4)
        AND m4.popularity IS NOT NULL
        AND m4.popularity > 0
)
AND (
    SELECT COUNT(*)
    FROM movies m5
    WHERE SUBSTR(m5.release_date, 1, 4) = SUBSTR(m1.release_date, 1, 4)
) >= 5
AND m1.popularity IS NOT NULL
AND m2.popularity IS NOT NULL
AND SUBSTR(m1.release_date, 1, 4) ~ '^[0-9]{4}$'
AND CAST(SUBSTR(m1.release_date, 1, 4) AS INTEGER) BETWEEN 2015 AND 2025
ORDER BY release_year;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.158s
- **Rows returned:** 9
- **Columns:** release_year, most_popular_movie, highest_popularity, least_popular_movie, lowest_popularity, popularity_gap

#### Top 20 Results

| release_year | most_popular_movie | highest_popularity | least_popular_movie | lowest_popularity | popularity_gap |
| --- | --- | --- | --- | --- | --- |
| 2015 | Dragon Ball Z: Resurrection 'F' | 220.05 | The Atticus Institute | 13.36 | 206.69 |
| 2016 | Doctor Strange | 228.27 | The Offering | 13.36 | 214.91 |
| 2017 | Coco | 210.53 | Our Souls at Night | 13.38 | 197.15 |
| 2018 | Avengers: Infinity War | 338.40 | The Quietude | 13.37 | 325.03 |
| 2019 | My Hero Academia: Heroes Rising | 239.60 | Impetigore | 13.36 | 226.24 |
| 2020 | Chernobyl: Abyss | 601.96 | Violent Delights | 13.36 | 588.60 |
| 2021 | Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 5070.60 |
| 2022 | The Batman | 3827.66 | Tony Hawk: Until the Wheels Fall Off | 13.45 | 3814.21 |
| 2023 | Fast & Furious 10 | 181.22 | The Little Mermaid | 14.02 | 167.20 |

---

## Exercise 4: Cinema Language Success Analysis

**Difficulty:** Hard
**Topics:** CTE (WITH clause), Window functions, ROW_NUMBER, NTILE, CASE WHEN, Multi-step analysis

### Problem Statement

Evaluate the success of different movie languages in our database. Focus on languages that have produced at least 20 movies, and calculate their movie count, average popularity, and average rating. Rank these languages by both movie count and average popularity, then categorize them into performance tiers (Top 25%, Upper 25%, Lower 25%, Bottom 25%) based on popularity. Display all statistics with rankings ordered by movie count (highest first).

### SQL Solution

```sql
WITH language_stats AS (
    SELECT
        l.language_name,
        COUNT(m.movie_id) AS movie_count,
        ROUND(AVG(m.popularity), 2) AS avg_popularity,
        ROUND(AVG(r.rating_score), 2) AS avg_rating
    FROM languages l
    JOIN movie_languages ml ON l.language_id = ml.language_id
    JOIN movies m ON ml.movie_id = m.movie_id
    LEFT JOIN movie_ratings mr ON m.movie_id = mr.movie_id
    LEFT JOIN ratings r ON mr.rating_id = r.rating_id
    WHERE m.popularity IS NOT NULL
    GROUP BY l.language_name
    HAVING COUNT(m.movie_id) >= 20
),
language_rankings AS (
    SELECT
        language_name,
        movie_count,
        avg_popularity,
        avg_rating,
        ROW_NUMBER() OVER (ORDER BY movie_count DESC) AS count_rank,
        ROW_NUMBER() OVER (ORDER BY avg_popularity DESC) AS popularity_rank,
        NTILE(4) OVER (ORDER BY avg_popularity) AS popularity_quartile
    FROM language_stats
)
SELECT
    language_name,
    movie_count,
    avg_popularity,
    avg_rating,
    count_rank,
    popularity_rank,
    CASE popularity_quartile
        WHEN 4 THEN 'Top 25%'
        WHEN 3 THEN 'Upper 25%'
        WHEN 2 THEN 'Lower 25%'
        WHEN 1 THEN 'Bottom 25%'
    END AS popularity_tier
FROM language_rankings
ORDER BY count_rank;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.008s
- **Rows returned:** 15
- **Columns:** language_name, movie_count, avg_popularity, avg_rating, count_rank, popularity_rank, popularity_tier

#### Top 20 Results

| language_name | movie_count | avg_popularity | avg_rating | count_rank | popularity_rank | popularity_tier |
| --- | --- | --- | --- | --- | --- | --- |
| English | 8970 | 43.15 | 6.37 | 1 | 3 | Top 25% |
| Japanese | 679 | 39.54 | 6.94 | 2 | 4 | Upper 25% |
| French | 357 | 37.11 | 6.39 | 3 | 7 | Upper 25% |
| Spanish | 353 | 38.22 | 6.55 | 4 | 6 | Upper 25% |
| Other Language | 214 | 34.31 | 6.35 | 5 | 9 | Lower 25% |
| Korean | 178 | 33.55 | 6.85 | 6 | 10 | Lower 25% |
| Italian | 156 | 29.43 | 6.46 | 7 | 12 | Bottom 25% |
| Chinese | 138 | 30.02 | 6.69 | 8 | 11 | Lower 25% |
| Mandarin | 108 | 23.31 | 6.54 | 9 | 14 | Bottom 25% |
| German | 101 | 24.07 | 6.68 | 10 | 13 | Bottom 25% |
| Russian | 91 | 38.23 | 6.82 | 11 | 5 | Upper 25% |
| Portuguese | 43 | 35.36 | 6.33 | 12 | 8 | Lower 25% |
| Hindi | 35 | 74.27 | 6.68 | 13 | 1 | Top 25% |
| Thai | 26 | 56.84 | 6.47 | 14 | 2 | Top 25% |
| Swedish | 26 | 21.84 | 7.07 | 15 | 15 | Bottom 25% |

---

## Exercise 5: Movie Industry Evolution Report

**Difficulty:** Hard
**Topics:** Multiple CTEs, Complex JOIN operations, Aggregate functions, Subqueries in SELECT, Industry trend analysis

### Problem Statement

Generate a comprehensive decade-by-decade analysis of movie industry trends. For each decade that has at least 50 movies, calculate the total number of movies produced, average popularity, and count of unique languages used. Additionally, identify the most common rating category across all movies. Present results showing decade name, movie statistics, language diversity, and the overall most common rating, ordered chronologically by decade.

### SQL Solution

```sql
WITH decade_movie_stats AS (
    SELECT
        d.decade_name,
        COUNT(m.movie_id) AS total_movies,
        ROUND(AVG(m.popularity), 2) AS avg_popularity
    FROM decades d
    JOIN movies m ON CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) BETWEEN d.decade_start AND d.decade_end
    WHERE m.popularity IS NOT NULL
        AND SUBSTR(m.release_date, 1, 4) ~ '^[0-9]{4}$'
    GROUP BY d.decade_name, d.decade_start
    HAVING COUNT(m.movie_id) >= 50
),
decade_language_diversity AS (
    SELECT
        d.decade_name,
        COUNT(DISTINCT l.language_id) AS unique_languages
    FROM decades d
    JOIN movies m ON CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) BETWEEN d.decade_start AND d.decade_end
    JOIN movie_languages ml ON m.movie_id = ml.movie_id
    JOIN languages l ON ml.language_id = l.language_id
    WHERE SUBSTR(m.release_date, 1, 4) ~ '^[0-9]{4}$'
    GROUP BY d.decade_name
),
rating_distribution AS (
    SELECT
        r.rating_category,
        COUNT(m.movie_id) AS movie_count
    FROM ratings r
    JOIN movie_ratings mr ON r.rating_id = mr.rating_id
    JOIN movies m ON mr.movie_id = m.movie_id
    GROUP BY r.rating_category
)
SELECT
    dms.decade_name,
    dms.total_movies,
    dms.avg_popularity,
    dld.unique_languages,
    (SELECT rating_category FROM rating_distribution ORDER BY movie_count DESC LIMIT 1) AS most_common_rating
FROM decade_movie_stats dms
JOIN decade_language_diversity dld ON dms.decade_name = dld.decade_name
ORDER BY dms.decade_name;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.005s
- **Rows returned:** 5
- **Columns:** decade_name, total_movies, avg_popularity, unique_languages, most_common_rating

#### Top 20 Results

| decade_name | total_movies | avg_popularity | unique_languages | most_common_rating |
| --- | --- | --- | --- | --- |
| 1980s | 587 | 23.04 | 16 | Good |
| 1990s | 993 | 25.53 | 16 | Good |
| 2000s | 1983 | 29.51 | 22 | Good |
| 2010s | 3814 | 32.68 | 37 | Good |
| 2020s | 1322 | 107.79 | 33 | Good |

---
