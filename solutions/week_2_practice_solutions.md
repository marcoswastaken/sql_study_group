# Week 2 Practice Solutions

## SQL Practice

**Scenario:** You're a movie data analyst, and you want to understand the characteristics of films in this dataset.

**Dataset Links:**
- [Movies Dataset](https://huggingface.co/datasets/Pablinho/movies-dataset)
- [Dataset Viewer](https://huggingface.co/datasets/Pablinho/movies-dataset/viewer/default/train)

### Tip

This data isn't perfectly clean, so when you are dealing with the vote count and vote average columns you may encounter strings which are not valid numbers. One approach to handling this is to use `TRY_CAST`, which will attempt to cast the values and return `NULL` if it fails. For instance this query will yield the rows with valid integer vote counts greater than 200:

```sql
SELECT *
FROM train
WHERE TRY_CAST(Vote_Count AS INTEGER) >= 200;
```

## Advanced WHERE Operators (AND, OR, NOT, IN, BETWEEN, LIKE)

### Question 1.1: How many movies were released in 2022 that have an average vote of at least 7?

```sql
SELECT COUNT(*) AS movie_count
FROM train
WHERE Release_Date LIKE '%2022%'
  AND TRY_CAST(Vote_Average AS FLOAT) >= 7;
```

### Question 1.2: Find the titles and release dates of 'horror' or 'thriller' movies with at least 500 votes.

```sql
SELECT Title, Release_Date
FROM train
WHERE (Genres LIKE '%Horror%' OR Genres LIKE '%Thriller%')
  AND TRY_CAST(Vote_Count AS INTEGER) >= 500;
```

### Question 1.3: Find the title and average vote of non-English films with a popularity of at least 1-million.

```sql
SELECT Title, Vote_Average
FROM train
WHERE Original_Language != 'en'
  AND TRY_CAST(Popularity AS FLOAT) >= 1000000;
```

### Question 1.4: Show the title, release date, and language of movies released from 2019 to 2022 that are *not* action movies, comedies, or dramas.

```sql
SELECT Title, Release_Date, Original_Language
FROM train
WHERE Release_Date BETWEEN '2019-01-01' AND '2022-12-31'
  AND Genres NOT LIKE '%Action%'
  AND Genres NOT LIKE '%Comedy%'
  AND Genres NOT LIKE '%Drama%';
```

## Handling NULL Values (IS NULL, IS NOT NULL)

### Question 2.1: How many movies in the dataset are missing an overview?

```sql
SELECT COUNT(*) AS missing_overview_count
FROM train
WHERE Overview IS NULL OR Overview = '';
```

### Question 2.2: List the title and release date of all movies that have a popularity score but do not include a poster image.

```sql
SELECT Title, Release_Date
FROM train
WHERE Popularity IS NOT NULL
  AND (Poster_Path IS NULL OR Poster_Path = '');
```

## Column Aliases (AS)

### Question 3.1: Retrieve the title, and Release_Date as Released, and Vote_Average as Rating, for all movies with fewer than 100 votes.

```sql
SELECT Title,
       Release_Date AS Released,
       Vote_Average AS Rating
FROM train
WHERE TRY_CAST(Vote_Count AS INTEGER) < 100;
```

## Aggregate Functions

### Question 4.1: What is the total number of movies in the dataset?

```sql
SELECT COUNT(*) AS total_movies
FROM train;
```

### Question 4.2: What is the average popularity across all movies for which it is recorded?

```sql
SELECT AVG(TRY_CAST(Popularity AS FLOAT)) AS average_popularity
FROM train
WHERE TRY_CAST(Popularity AS FLOAT) IS NOT NULL;
```

### Question 4.3: What is the highest vote average achieved by any movie, and what is the lowest recorded vote count?

```sql
SELECT MAX(TRY_CAST(Vote_Average AS FLOAT)) AS highest_vote_average,
       MIN(TRY_CAST(Vote_Count AS INTEGER)) AS lowest_vote_count
FROM train
WHERE TRY_CAST(Vote_Average AS FLOAT) IS NOT NULL
  AND TRY_CAST(Vote_Count AS INTEGER) IS NOT NULL;
```

### Question 4.4: How many votes have been cast for movies in English? How many votes have been cast for movies not in English?

```sql
-- English movies
SELECT SUM(TRY_CAST(Vote_Count AS INTEGER)) AS english_votes
FROM train
WHERE Original_Language = 'en'
  AND TRY_CAST(Vote_Count AS INTEGER) IS NOT NULL;

-- Non-English movies
SELECT SUM(TRY_CAST(Vote_Count AS INTEGER)) AS non_english_votes
FROM train
WHERE Original_Language != 'en'
  AND TRY_CAST(Vote_Count AS INTEGER) IS NOT NULL;
```

### Bonus: What is the average number of votes cast per movie for movies in English? What is the average number of votes cast per movie for movies not in English?

```sql
-- English movies
SELECT AVG(TRY_CAST(Vote_Count AS INTEGER)) AS avg_votes_english
FROM train
WHERE Original_Language = 'en'
  AND TRY_CAST(Vote_Count AS INTEGER) IS NOT NULL;

-- Non-English movies
SELECT AVG(TRY_CAST(Vote_Count AS INTEGER)) AS avg_votes_non_english
FROM train
WHERE Original_Language != 'en'
  AND TRY_CAST(Vote_Count AS INTEGER) IS NOT NULL;
```
