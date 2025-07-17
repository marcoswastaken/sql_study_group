# Week 5 Practice - Movies Dataset

**Description:** Advanced JOIN operations, subqueries, and Common Table Expressions (CTEs) using real-world movie data with ratings, languages, and temporal information
**Database:** data_movies_dataset.db
**Total Exercises:** 6
**Focus Topics:** RIGHT JOIN, FULL OUTER JOIN, SELF JOIN, Subqueries (scalar, WHERE, SELECT, FROM), CTEs (WITH clause), Advanced data analysis, Real-world data quality handling

*Report generated on: 2025-07-15 16:16:04*

---

## Exercise 1: Languages Without Movies - RIGHT JOIN

**Difficulty:** Easy
**Topics:** RIGHT JOIN, IS NULL, Unmatched records, ORDER BY

### Problem Statement

Find all languages that don't have any movies in our database. This is a classic RIGHT JOIN scenario to find unmatched records. Show the language code and language name for languages that have zero movies. Order by language code.

### SQL Solution

```sql
SELECT l.language_code, l.language_name
FROM movie_languages ml
RIGHT JOIN languages l ON ml.language_id = l.language_id
WHERE ml.language_id IS NULL
ORDER BY l.language_code;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.134s
- **Rows returned:** 1
- **Columns:** language_code, language_name

#### Top 20 Results

| language_code | language_name |
| --- | --- |
| et | Other Language |

---

## Exercise 2: Decade Popularity Comparison - SELF JOIN

**Difficulty:** Medium
**Topics:** SELF JOIN, Date extraction, Multiple conditions, Calculated fields

### Problem Statement

Compare movies within the same decade to find popularity gaps. Use a SELF JOIN to find pairs of movies from the same decade where one movie has significantly higher popularity (at least 200 points higher) than another. Show both movie titles, their popularity scores, and the decade name. Limit to 10 results ordered by popularity difference.

### SQL Solution

```sql
SELECT
    m1.title AS popular_movie,
    m1.popularity AS popular_score,
    m2.title AS less_popular_movie,
    m2.popularity AS less_popular_score,
    d.decade_name,
    (m1.popularity - m2.popularity) AS popularity_gap
FROM movies m1
JOIN movies m2 ON m1.movie_id != m2.movie_id
JOIN decades d ON TRY_CAST(SUBSTR(m1.release_date, 1, 4) AS INTEGER) >= d.decade_start
    AND TRY_CAST(SUBSTR(m1.release_date, 1, 4) AS INTEGER) <= d.decade_end
JOIN decades d2 ON TRY_CAST(SUBSTR(m2.release_date, 1, 4) AS INTEGER) >= d2.decade_start
    AND TRY_CAST(SUBSTR(m2.release_date, 1, 4) AS INTEGER) <= d2.decade_end
WHERE d.decade_name = d2.decade_name
    AND m1.popularity > m2.popularity + 200
    AND m1.popularity IS NOT NULL
    AND m2.popularity IS NOT NULL
    AND TRY_CAST(SUBSTR(m1.release_date, 1, 4) AS INTEGER) IS NOT NULL
    AND TRY_CAST(SUBSTR(m2.release_date, 1, 4) AS INTEGER) IS NOT NULL
ORDER BY popularity_gap DESC
LIMIT 10;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 1.555s
- **Rows returned:** 20
- **Columns:** popular_movie, popular_score, less_popular_movie, less_popular_score, decade_name, popularity_gap

#### Top 20 Results

| popular_movie | popular_score | less_popular_movie | less_popular_score | decade_name | popularity_gap |
| --- | --- | --- | --- | --- | --- |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2016.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2019.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2021.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2018.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2014.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2020.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2015.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2017.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2013.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 2012.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The Offering | 13.36 | 2016.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The Offering | 13.36 | 2012.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The Offering | 13.36 | 2014.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The Offering | 13.36 | 2013.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | The Offering | 13.36 | 2015.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | Violent Delights | 13.36 | 2016.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | Violent Delights | 13.36 | 2013.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | Violent Delights | 13.36 | 2017.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | Violent Delights | 13.36 | 2014.0s | 5070.60 |
| Spider-Man: No Way Home | 5083.95 | Violent Delights | 13.36 | 2020.0s | 5070.60 |

---

## Exercise 3: Above Average Movies by Rating Category - Scalar Subquery

**Difficulty:** Medium
**Topics:** Scalar subquery, Correlated subquery, AVG function, Multiple JOINs

### Problem Statement

Find movies that have above-average popularity within their specific rating category (Excellent, Very Good, Good, etc.). Use a scalar subquery to calculate the average popularity for each rating category. Show movie title, popularity, rating category, and how much above the category average they are (as `above_average_by`). Order by the difference descending and limit to 15 results.

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
        WHERE r2.rating_category = r.rating_category
            AND m2.popularity IS NOT NULL
    ), 2) AS above_average_by
FROM movies m
JOIN movie_ratings mr ON m.movie_id = mr.movie_id
JOIN ratings r ON mr.rating_id = r.rating_id
WHERE m.popularity > (
    SELECT AVG(m2.popularity)
    FROM movies m2
    JOIN movie_ratings mr2 ON m2.movie_id = mr2.movie_id
    JOIN ratings r2 ON mr2.rating_id = r2.rating_id
    WHERE r2.rating_category = r.rating_category
        AND m2.popularity IS NOT NULL
)
AND m.popularity IS NOT NULL
ORDER BY above_average_by DESC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.009s
- **Rows returned:** 20
- **Columns:** title, popularity, rating_category, above_average_by

#### Top 20 Results

| title | popularity | rating_category | above_average_by |
| --- | --- | --- | --- |
| Spider-Man: No Way Home | 5083.95 | Excellent | 5007.50 |
| The Batman | 3827.66 | Excellent | 3751.21 |
| No Exit | 2618.09 | Good | 2580.86 |
| Encanto | 2402.20 | Very Good | 2355.75 |
| The King's Man | 1895.51 | Very Good | 1849.06 |
| The Commando | 1750.48 | Good | 1713.26 |
| Scream | 1675.16 | Good | 1637.94 |
| Scream | 1675.16 | Very Good | 1628.71 |
| Kimi | 1601.78 | Good | 1564.56 |
| Fistful of Vengeance | 1594.01 | Average | 1559.29 |
| Eternals | 1537.41 | Very Good | 1490.95 |
| Pursuit | 1501.52 | Average | 1466.80 |
| My Hero Academia: World Heroes' Mission | 1485.06 | Very Good | 1438.61 |
| Restless | 1468.38 | Average | 1433.65 |
| Nightmare Alley | 1455.14 | Very Good | 1408.69 |
| Nightmare Alley | 1455.14 | Very Good | 1408.69 |
| The Ice Age Adventures of Buck Wild | 1431.31 | Very Good | 1384.85 |
| Hotel Transylvania: Transformania | 1373.78 | Very Good | 1327.33 |
| Texas Chainsaw Massacre | 1312.79 | Average | 1278.06 |
| The Requin | 1252.32 | Poor | 1217.36 |

---

## Exercise 4: Most Popular Movie by Decade - Subquery in FROM

**Difficulty:** Hard
**Topics:** Subquery in FROM, MAX function, GROUP BY, Complex JOINs

### Problem Statement

Create a decade summary showing the most popular movie from each decade. Use a subquery in the FROM clause to first find the maximum popularity per decade, then join back to get the movie details. Show decade name, movie title, and popularity score. Handle cases where multiple movies might tie for highest popularity by showing just one.

### SQL Solution

```sql
SELECT
    decade_max.decade_name,
    ANY_VALUE(m.title) AS most_popular_movie,
    decade_max.max_popularity
FROM (
    SELECT
        d.decade_name,
        MAX(m.popularity) AS max_popularity
    FROM decades d
    JOIN movies m ON TRY_CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) >= d.decade_start
        AND TRY_CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) <= d.decade_end
    WHERE m.popularity IS NOT NULL
        AND TRY_CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) IS NOT NULL
    GROUP BY d.decade_name
) AS decade_max
JOIN movies m ON m.popularity = decade_max.max_popularity
JOIN decades d ON TRY_CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) >= d.decade_start
    AND TRY_CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) <= d.decade_end
    AND d.decade_name = decade_max.decade_name
WHERE TRY_CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) IS NOT NULL
GROUP BY decade_max.decade_name, decade_max.max_popularity
ORDER BY decade_max.decade_name;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.013s
- **Rows returned:** 20
- **Columns:** decade_name, most_popular_movie, max_popularity

#### Top 20 Results

| decade_name | most_popular_movie | max_popularity |
| --- | --- | --- |
| 1902.0s | A Trip to the Moon | 18.36 |
| 1920.0s | Nosferatu | 28.64 |
| 1921.0s | Nosferatu | 28.64 |
| 1922.0s | Nosferatu | 28.64 |
| 1925.0s | King Kong | 24.99 |
| 1926.0s | King Kong | 24.99 |
| 1927.0s | King Kong | 24.99 |
| 1929.0s | Snow White and the Seven Dwarfs | 103.38 |
| 1930.0s | Snow White and the Seven Dwarfs | 103.38 |
| 1931.0s | Snow White and the Seven Dwarfs | 103.38 |
| 1932.0s | Snow White and the Seven Dwarfs | 103.38 |
| 1933.0s | Snow White and the Seven Dwarfs | 103.38 |
| 1935.0s | Snow White and the Seven Dwarfs | 103.38 |
| 1936.0s | Snow White and the Seven Dwarfs | 103.38 |
| 1937.0s | Snow White and the Seven Dwarfs | 103.38 |
| 1938.0s | Pinocchio | 89.00 |
| 1939.0s | Pinocchio | 89.00 |
| 1940.0s | Pinocchio | 89.00 |
| 1941.0s | Cinderella | 126.86 |
| 1942.0s | Cinderella | 126.86 |

---

## Exercise 5: Language Popularity Rankings - Multi-step CTE

**Difficulty:** Hard
**Topics:** CTE (WITH clause), Window functions, ROW_NUMBER, NTILE, CASE WHEN, Multi-step analysis

### Problem Statement

Use Common Table Expressions to perform a multi-step language analysis. First CTE: calculate movie counts and average popularity by language. Second CTE: add rankings based on movie count and popularity. Final query: show languages with their statistics and tier classification (Top 25%, Upper 25%, etc.). Only include languages with at least 20 movies.

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
| Swedish | 26 | 21.84 | 7.07 | 14 | 15 | Bottom 25% |
| Thai | 26 | 56.84 | 6.47 | 15 | 2 | Top 25% |

---

## Exercise 6: Comprehensive Data Quality Report - Advanced CTE

**Difficulty:** Hard
**Topics:** Advanced CTE, CROSS JOIN, Data quality analysis, Conditional aggregation, CASE WHEN, Complex business logic

### Problem Statement

Create a comprehensive data quality analysis using multiple CTEs. Analyze missing data patterns, coverage statistics, and data completeness across different aspects of the movie database. The final result should be a single-row summary showing overall data health metrics and a quality grade.

### SQL Solution

```sql
WITH data_quality_metrics AS (
    SELECT
        COUNT(*) AS total_movies,
        COUNT(CASE WHEN vote_count IS NULL THEN 1 END) AS missing_vote_count,
        COUNT(CASE WHEN popularity IS NULL THEN 1 END) AS missing_popularity,
        COUNT(CASE WHEN popularity > 1000 THEN 1 END) AS high_popularity_outliers,
        ROUND(COUNT(CASE WHEN vote_count IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) AS vote_coverage_pct
    FROM movies
),
language_coverage AS (
    SELECT
        COUNT(DISTINCT m.movie_id) AS movies_with_language,
        COUNT(DISTINCT l.language_id) AS unique_languages,
        ROUND(COUNT(DISTINCT m.movie_id) * 100.0 / (SELECT COUNT(*) FROM movies), 2) AS language_coverage_pct
    FROM movies m
    JOIN movie_languages ml ON m.movie_id = ml.movie_id
    JOIN languages l ON ml.language_id = l.language_id
),
rating_coverage AS (
    SELECT
        COUNT(DISTINCT m.movie_id) AS movies_with_ratings,
        ROUND(COUNT(DISTINCT m.movie_id) * 100.0 / (SELECT COUNT(*) FROM movies), 2) AS rating_coverage_pct,
        MIN(r.rating_score) AS min_rating,
        MAX(r.rating_score) AS max_rating
    FROM movies m
    JOIN movie_ratings mr ON m.movie_id = mr.movie_id
    JOIN ratings r ON mr.rating_id = r.rating_id
)
SELECT
    'Data Quality Report' AS report_type,
    dq.total_movies,
    dq.missing_vote_count,
    dq.missing_popularity,
    dq.vote_coverage_pct,
    lc.language_coverage_pct,
    rc.rating_coverage_pct,
    rc.min_rating,
    rc.max_rating,
    CASE
        WHEN lc.language_coverage_pct >= 95 AND rc.rating_coverage_pct >= 95 AND dq.vote_coverage_pct >= 90 THEN 'A - Excellent'
        WHEN lc.language_coverage_pct >= 85 AND rc.rating_coverage_pct >= 85 AND dq.vote_coverage_pct >= 75 THEN 'B - Good'
        WHEN lc.language_coverage_pct >= 70 AND rc.rating_coverage_pct >= 70 AND dq.vote_coverage_pct >= 60 THEN 'C - Fair'
        ELSE 'D - Needs Improvement'
    END AS overall_data_quality_grade
FROM data_quality_metrics dq
CROSS JOIN language_coverage lc
CROSS JOIN rating_coverage rc;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.005s
- **Rows returned:** 1
- **Columns:** report_type, total_movies, missing_vote_count, missing_popularity, vote_coverage_pct, language_coverage_pct, rating_coverage_pct, min_rating, max_rating, overall_data_quality_grade

#### Top 20 Results

| report_type | total_movies | missing_vote_count | missing_popularity | vote_coverage_pct | language_coverage_pct | rating_coverage_pct | min_rating | max_rating | overall_data_quality_grade |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Data Quality Report | 9337 | 2 | 1 | 99.98 | 99.99 | 99.98 | 0 | 10 | A - Excellent |

---
