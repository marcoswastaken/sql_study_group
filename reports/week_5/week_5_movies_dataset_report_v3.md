# Week 5 Practice - Movies Dataset

**Description:** Advanced JOIN operations, subqueries, and Common Table Expressions (CTEs) using real-world movie data with ratings, languages, and temporal information
**Database:** data_movies_dataset.db
**Total Exercises:** 6
**Focus Topics:** RIGHT JOIN, FULL OUTER JOIN, SELF JOIN, Subqueries (scalar, WHERE, SELECT, FROM), CTEs (WITH clause), Advanced data analysis, Real-world data quality handling

*Report generated on: 2025-07-15 17:44:08*

---

## Exercise 1: Languages with Limited Movie Selection - RIGHT JOIN

**Difficulty:** Easy
**Topics:** RIGHT JOIN, COUNT aggregation, GROUP BY, HAVING clause, ORDER BY

### Problem Statement

Find all languages that appear as the primary language in fewer than 10 movies in our database. Use a RIGHT JOIN to ensure all languages are considered, even those with zero movies. Show the language code, language name, and the actual count of movies for each language. Filter out invalid language codes that contain URLs or are blank. Order by movie count ascending, then by language code.

### SQL Solution

```sql
SELECT
    l.language_code,
    l.language_name,
    COUNT(ml.movie_id) AS movie_count
FROM movie_languages ml
RIGHT JOIN languages l ON ml.language_id = l.language_id
WHERE l.language_code NOT LIKE '%http%'
    AND l.language_code != ''
    AND LENGTH(l.language_code) <= 3
GROUP BY l.language_id, l.language_code, l.language_name
HAVING COUNT(ml.movie_id) < 10
ORDER BY movie_count ASC, l.language_code;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.1s
- **Rows returned:** 20
- **Columns:** language_code, language_name, movie_count

#### Top 20 Results

| language_code | language_name | movie_count |
| --- | --- | --- |
| et | Other Language | 0 |
| bn | Other Language | 1 |
| ca | Other Language | 1 |
| eu | Other Language | 1 |
| la | Other Language | 1 |
| lv | Other Language | 1 |
| ml | Other Language | 1 |
| ms | Other Language | 1 |
| nb | Other Language | 1 |
| he | Other Language | 2 |
| ro | Other Language | 2 |
| ta | Other Language | 2 |
| ar | Arabic | 3 |
| fa | Other Language | 3 |
| hu | Other Language | 3 |
| is | Other Language | 3 |
| uk | Other Language | 3 |
| cs | Other Language | 4 |
| el | Other Language | 5 |
| fi | Other Language | 5 |

---

## Exercise 2: Year's Most vs Least Popular Movies - SELF JOIN

**Difficulty:** Medium
**Topics:** SELF JOIN, Comparison operators, Calculated fields, NULL handling

### Problem Statement

For each year, find the most popular and least popular movies released that year. Use a SELF JOIN to compare movies within the same release year. Show the year, most popular movie title and score, least popular movie title and score, and the popularity gap between them. Only include years with at least 10 movies and limit to 10 results ordered by popularity gap descending.

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
) >= 10
AND m1.popularity IS NOT NULL
AND m2.popularity IS NOT NULL
AND SUBSTR(m1.release_date, 1, 4) ~ '^[0-9]{4}$'
ORDER BY popularity_gap DESC
LIMIT 10;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.262s
- **Rows returned:** 20
- **Columns:** release_year, most_popular_movie, highest_popularity, least_popular_movie, lowest_popularity, popularity_gap

#### Top 20 Results

| release_year | most_popular_movie | highest_popularity | least_popular_movie | lowest_popularity | popularity_gap |
| --- | --- | --- | --- | --- | --- |
| 2021 | Spider-Man: No Way Home | 5083.95 | The United States vs. Billie Holiday | 13.35 | 5070.60 |
| 2022 | The Batman | 3827.66 | Tony Hawk: Until the Wheels Fall Off | 13.45 | 3814.21 |
| 2020 | Chernobyl: Abyss | 601.96 | Violent Delights | 13.36 | 588.60 |
| 1986 | Exploits of a Young Don Juan | 396.95 | Peggy Sue Got Married | 13.44 | 383.51 |
| 2018 | Avengers: Infinity War | 338.40 | The Quietude | 13.37 | 325.03 |
| 2012 | The Amazing Spider-Man | 306.38 | Viva l'Italia | 13.37 | 293.00 |
| 2009 | Avatar | 297.36 | Laid to Rest | 13.40 | 283.95 |
| 2005 | Batman Begins | 265.81 | I'm in Love With My Little Sister | 13.36 | 252.45 |
| 2019 | My Hero Academia: Heroes Rising | 239.60 | Impetigore | 13.36 | 226.24 |
| 2014 | The Amazing Spider-Man 2 | 231.44 | My Love, My Bride | 13.38 | 218.06 |
| 2001 | Harry Potter and the Philosopher's Stone | 230 | The Mexican | 13.38 | 216.62 |
| 2016 | Doctor Strange | 228.27 | The Offering | 13.36 | 214.91 |
| 2015 | Dragon Ball Z: Resurrection 'F' | 220.05 | The Atticus Institute | 13.36 | 206.69 |
| 2002 | Harry Potter and the Chamber of Secrets | 210.84 | Life or Something Like It | 13.37 | 197.47 |
| 2017 | Coco | 210.53 | Our Souls at Night | 13.38 | 197.15 |
| 2011 | Real Steel | 203.84 | Take Shelter | 13.38 | 190.47 |
| 2007 | I Am Legend | 199.25 | The Kite Runner | 13.37 | 185.88 |
| 2004 | Harry Potter and the Prisoner of Azkaban | 189.77 | Dead Man's Shoes | 13.38 | 176.40 |
| 2010 | Iron Man 2 | 183.14 | Arctic Predator | 13.38 | 169.75 |
| 1972 | What the Peeper Saw | 181.32 | Roma | 14.01 | 167.31 |

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
- **Execution time:** 0.011s
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

## Exercise 4: Top Movie by Decade - Subquery in FROM

**Difficulty:** Hard
**Topics:** Subquery in FROM, MAX function, GROUP BY, HAVING clause, BETWEEN operator

### Problem Statement

Find the most popular movie from each decade using a subquery in the FROM clause. First, create a subquery that finds the maximum popularity score for each decade (1980s, 1990s, 2000s, etc.). Then join this result back to the movies table to get the actual movie details. Show decade, movie title, and popularity score.

### SQL Solution

```sql
SELECT
    decade_popularity.decade,
    m.title AS most_popular_movie,
    decade_popularity.max_popularity
FROM (
    SELECT
        CAST((CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) / 10) * 10 AS VARCHAR) || 's' AS decade,
        MAX(m.popularity) AS max_popularity
    FROM movies m
    WHERE m.popularity IS NOT NULL
        AND SUBSTR(m.release_date, 1, 4) ~ '^[0-9]{4}$'
        AND CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) >= 1980
    GROUP BY CAST((CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) / 10) * 10 AS VARCHAR) || 's'
    HAVING COUNT(m.movie_id) >= 20
) AS decade_popularity
JOIN movies m ON m.popularity = decade_popularity.max_popularity
WHERE SUBSTR(m.release_date, 1, 4) ~ '^[0-9]{4}$'
    AND CAST((CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) / 10) * 10 AS VARCHAR) || 's' = decade_popularity.decade
ORDER BY decade_popularity.decade;


```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.007s
- **Rows returned:** 20
- **Columns:** decade, most_popular_movie, max_popularity

#### Top 20 Results

| decade | most_popular_movie | max_popularity |
| --- | --- | --- |
| 1980.0s | The Shining | 57.14 |
| 1981.0s | Porno | 81.95 |
| 1982.0s | First Blood | 52.45 |
| 1983.0s | Scarface | 61.98 |
| 1984.0s | Indiana Jones and the Temple of Doom | 58.70 |
| 1985.0s | High School Teacher: Maturing | 139.47 |
| 1986.0s | Exploits of a Young Don Juan | 396.95 |
| 1987.0s | Predator | 58.09 |
| 1988.0s | Child's Play | 67.72 |
| 1989.0s | The Little Mermaid | 128.23 |
| 1990.0s | Dragon Ball Z: The Tree of Might | 100.71 |
| 1991.0s | Beauty and the Beast | 109.65 |
| 1992.0s | Batman Returns | 161.32 |
| 1993.0s | Dragon Ball Z: Broly – The Legendary Super Saiyan | 144.38 |
| 1994.0s | The Lion King | 162.05 |
| 1995.0s | Toy Story | 171.71 |
| 1996.0s | Scream | 77.60 |
| 1997.0s | Titanic | 123.01 |
| 1998.0s | Mulan | 129.34 |
| 1999.0s | Toy Story 2 | 149.03 |

---

## Exercise 5: Language Performance Analytics - Multi-step CTE

**Difficulty:** Hard
**Topics:** CTE (WITH clause), Window functions, ROW_NUMBER, NTILE, CASE WHEN, Multi-step analysis

### Problem Statement

Analyze language performance using a two-step approach with Common Table Expressions. Step 1: Calculate movie counts, average popularity, and average rating for each language that has at least 20 movies. Step 2: Rank languages by both movie count and average popularity, then assign performance tiers (Top 25%, Upper 25%, Lower 25%, Bottom 25%) based on popularity rankings. Show all statistics and tier assignments.

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
- **Execution time:** 0.009s
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

## Exercise 6: Movie Database Insights - Multiple CTEs

**Difficulty:** Hard
**Topics:** Multiple CTEs, Subqueries in SELECT, Aggregate functions, ORDER BY with LIMIT, Complex multi-table analysis

### Problem Statement

Use multiple Common Table Expressions to analyze different aspects of the movie database. Create three separate CTEs: 1) Calculate rating distribution (count of movies per rating category), 2) Find decade trends (average popularity per decade for decades with 50+ movies), and 3) Identify language diversity (count of unique languages per decade). Show the complete decade trends and language diversity data, along with summary insights.

### SQL Solution

```sql
WITH rating_distribution AS (
    SELECT
        r.rating_category,
        COUNT(m.movie_id) AS movie_count
    FROM ratings r
    JOIN movie_ratings mr ON r.rating_id = mr.rating_id
    JOIN movies m ON mr.movie_id = m.movie_id
    GROUP BY r.rating_category
),
decade_trends AS (
    SELECT
        CAST((CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) / 10) * 10 AS VARCHAR) || 's' AS decade,
        COUNT(m.movie_id) AS movies_in_decade,
        ROUND(AVG(m.popularity), 2) AS avg_popularity
    FROM movies m
    WHERE m.popularity IS NOT NULL
        AND SUBSTR(m.release_date, 1, 4) ~ '^[0-9]{4}$'
        AND CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) >= 1980
    GROUP BY CAST((CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) / 10) * 10 AS VARCHAR) || 's'
    HAVING COUNT(m.movie_id) >= 50
),
language_diversity AS (
    SELECT
        CAST((CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) / 10) * 10 AS VARCHAR) || 's' AS decade,
        COUNT(DISTINCT l.language_id) AS unique_languages
    FROM movies m
    JOIN movie_languages ml ON m.movie_id = ml.movie_id
    JOIN languages l ON ml.language_id = l.language_id
    WHERE SUBSTR(m.release_date, 1, 4) ~ '^[0-9]{4}$'
        AND CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) >= 1980
    GROUP BY CAST((CAST(SUBSTR(m.release_date, 1, 4) AS INTEGER) / 10) * 10 AS VARCHAR) || 's'
)
SELECT
    dt.decade,
    dt.movies_in_decade,
    dt.avg_popularity,
    ld.unique_languages,
    (SELECT rating_category FROM rating_distribution ORDER BY movie_count DESC LIMIT 1) AS most_common_rating
FROM decade_trends dt
JOIN language_diversity ld ON dt.decade = ld.decade
ORDER BY dt.decade;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.008s
- **Rows returned:** 20
- **Columns:** decade, movies_in_decade, avg_popularity, unique_languages, most_common_rating

#### Top 20 Results

| decade | movies_in_decade | avg_popularity | unique_languages | most_common_rating |
| --- | --- | --- | --- | --- |
| 1984.0s | 52 | 23.61 | 4 | Good |
| 1985.0s | 74 | 22.17 | 7 | Good |
| 1986.0s | 66 | 29.81 | 7 | Good |
| 1987.0s | 66 | 20.64 | 7 | Good |
| 1988.0s | 77 | 23.83 | 6 | Good |
| 1989.0s | 76 | 22.87 | 5 | Good |
| 1990.0s | 73 | 25.99 | 7 | Good |
| 1991.0s | 76 | 24.68 | 6 | Good |
| 1992.0s | 86 | 25.12 | 7 | Good |
| 1993.0s | 114 | 25.03 | 7 | Good |
| 1994.0s | 100 | 26.08 | 7 | Good |
| 1995.0s | 104 | 26.62 | 8 | Good |
| 1996.0s | 91 | 22.85 | 5 | Good |
| 1997.0s | 112 | 26.51 | 11 | Good |
| 1998.0s | 124 | 24.70 | 9 | Good |
| 1999.0s | 113 | 27.23 | 7 | Good |
| 2000.0s | 131 | 25.36 | 12 | Good |
| 2001.0s | 152 | 28.70 | 8 | Good |
| 2002.0s | 156 | 28.75 | 8 | Good |
| 2003.0s | 174 | 28.12 | 14 | Good |

---
