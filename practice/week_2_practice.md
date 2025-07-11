# Week 2 Practice

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

**Question 1.1:** How many movies were released in 2022 that have an average vote of at least 7?

**Question 1.2:** Find the titles and release dates of 'horror' or 'thriller' movies with at least 500 votes.

**Question 1.3:** Find the title and average vote of non-English films with a popularity of at least 1-million.

**Question 1.4:** Show the title, release date, and language of movies released from 2019 to 2022 that are *not* action movies, comedies, or dramas.

## Handling NULL Values (IS NULL, IS NOT NULL)

**Question 2.1:** How many movies in the dataset are missing an overview?

**Question 2.2:** List the title and release date of all movies that have a popularity score but do not include a poster image.

## Column Aliases (AS)

**Question 3.1:** Retrieve the title, and Release_Date as Released, and Vote_Average as Rating, for all movies with fewer than 100 votes.

## Aggregate Functions

**Question 4.1:** What is the total number of movies in the dataset?

**Question 4.2:** What is the average popularity across all movies for which it is recorded?

**Question 4.3:** What is the highest vote average achieved by any movie, and what is the lowest recorded vote count?

**Question 4.4:** How many votes have been cast for movies in English? How many votes have been cast for movies not in English?

**Bonus:** What is the average number of votes cast per movie for movies in English? What is the average number of votes cast per movie for movies not in English?