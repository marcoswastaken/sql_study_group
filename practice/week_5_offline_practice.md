# Week 5 Practice

The data cards for a collection of tables is provided. For each exercise, come up with a SQL query that addresses the problem statement.

## 📚 Data Dictionary

### decades
**Row Count:** 102

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| decade_id | BIGINT | Yes | FK | Unique identifier for each decade period, used for SELF JOIN exercises and temporal analysis |
| decade_start | DOUBLE | Yes |  | Starting year of the decade (e.g., 2010 for the 2010s), extracted from movie release dates |
| decade_end | DOUBLE | Yes |  | Ending year of the decade (e.g., 2019 for the 2010s), calculated as decade_start + 9 |
| decade_name | VARCHAR | Yes |  | Human-readable decade label (e.g., '2010s', '1990s') for display purposes and easier filtering |

### languages
**Row Count:** 44

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| language_id | BIGINT | Yes | FK | Unique identifier for each language, used as foreign key in movie_languages junction table |
| language_code | VARCHAR | Yes |  | ISO-like language code (e.g., 'en', 'fr', 'ja') from the original dataset, used for mapping to movies |
| language_name | VARCHAR | Yes |  | Human-readable language name (e.g., 'English', 'French', 'Japanese') with CASE logic for major languages, 'Other Language' for unmapped codes |

### movie_languages
**Row Count:** 9,992

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| movie_id | BIGINT | Yes | FK | Unique identifier for each movie, used as foreign key in movie_ratings junction table |
| language_id | BIGINT | Yes | FK | Unique identifier for each language, used as foreign key in movie_languages junction table |

### movie_ratings
**Row Count:** 9,991

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| movie_id | BIGINT | Yes | FK | Unique identifier for each movie, used as foreign key in movie_ratings junction table |
| rating_id | BIGINT | Yes | FK | Unique identifier for each rating, used as foreign key in movie_ratings junction table |

### movies
**Row Count:** 9,337

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| movie_id | BIGINT | Yes | FK | Unique identifier for each movie, used as foreign key in movie_languages, movie_ratings, and movies junction tables |
| title | VARCHAR | Yes |  | Movie title, used for JOIN operations and filtering |
| release_date | VARCHAR | Yes |  | Movie release date, used for temporal analysis and JOIN operations |
| overview | VARCHAR | Yes |  | Movie overview, used for JOIN operations and filtering |
| popularity | DECIMAL(10,3) | Yes |  | Movie popularity score, used for JOIN operations and filtering |
| vote_count | INTEGER | Yes |  | Number of votes for the movie, used for JOIN operations and filtering |
| poster_url | VARCHAR | Yes |  | URL of the movie poster, used for JOIN operations and filtering |

### ratings
**Row Count:** 74

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| rating_id | BIGINT | Yes | FK | Unique identifier for each rating, used as foreign key in movie_ratings junction table |
| rating_score | DECIMAL(3,1) | Yes |  | Movie rating score, used for JOIN operations and filtering |
| rating_category | VARCHAR | Yes |  | Human-readable rating category (e.g., 'Excellent', 'Very Good', 'Good', 'Average', 'Poor') based on rating score |

---

## 🎯 Practice Exercises

### Exercise 1: Exceptional Movies Among Excellent Ratings

**Problem Statement:**
Identify the standout performers among movies with 'Excellent' ratings. Find movies that are significantly more popular than the typical excellent movie - specifically those with popularity at least 500 points above the average for all excellent-rated movies. Display the movie title, popularity score, rating category, and the amount by which they exceed the excellent average. Order results by the excess amount in descending order.

---

### Exercise 2: Decade Champions

**Problem Statement:**
Determine which movie achieved the highest popularity in each decade. Your analysis should span from the 1980s through the 2020s, showing the decade name, the champion movie's title, and its popularity score. Only include decades that have movies in the database. Results should be ordered chronologically by decade.

**Helpful Tip:** The SUBSTR function extracts part of a text string. Syntax: `SUBSTR(text, start_position, length)`. Examples: `SUBSTR('2023-12-25', 6, 2)` returns '12' (month), `SUBSTR('Hello World', 1, 5)` returns 'Hello', `SUBSTR('ABC123DEF', 4, 3)` returns '123'. When extracting from dates, you can get specific parts like years or months.

---

### Exercise 3: Recent Movie Popularity Extremes

**Problem Statement:**
Analyze popularity extremes in recent movie releases from 2015 to 2025. For each year, identify both the most and least popular movies released. Your result should show the release year, both movie titles with their popularity scores, and calculate the popularity gap between them. Only include years that released at least 5 movies. Results should be ordered chronologically by year.

---

### Exercise 4: Cinema Language Success Analysis

**Problem Statement:**
Evaluate the success of different movie languages in our database. Focus on languages that have produced at least 20 movies, and calculate their movie count, average popularity, and average rating. Rank these languages by both movie count and average popularity, then categorize them into performance tiers (Top 25%, Upper 25%, Lower 25%, Bottom 25%) based on popularity. Display all statistics with rankings ordered by movie count (highest first).

---

### Exercise 5: Movie Industry Evolution Report

**Problem Statement:**
Generate a comprehensive decade-by-decade analysis of movie industry trends. For each decade that has at least 50 movies, calculate the total number of movies produced, average popularity, and count of unique languages used. Additionally, identify the most common rating category across all movies. Present results showing decade name, movie statistics, language diversity, and the overall most common rating, ordered chronologically by decade.

---
