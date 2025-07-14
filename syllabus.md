# 8-Week SQL Study Group Syllabus

Comprehensive week-by-week breakdown with specific LeetCode problems and learning objectives

## Week 1: Introduction to Databases & Basic SELECT Queries

This week will cover the basics of databases and SQL. We will start with the basics of databases and SQL, and then move on to more advanced topics.

**Core Concepts:**
- What is a database?
- Relational Database (RDBMS)?
- Basic SQL Syntax
- SELECT, FROM, WHERE (basic operators: =, >, <, >=, <=, !=/<>)
- ORDER BY
- LIMIT/TOP

**Learning Objectives:**
- Understand basic database structure
- Write simple queries to retrieve and filter specific columns
- Sort results
- Limit output

**SQLZoo Exercises:**
- [0. SELECT basics](https://sqlzoo.net/wiki/SELECT_basics)
- [1. SELECT names](https://sqlzoo.net/wiki/SELECT_names)
- [2. SELECT from WORLD Tutorial](https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial)

**LeetCode Practice (Easy to Medium):**
- **1757. Recyclable and Low Fat Products**
  - Basic SELECT and WHERE with AND
- **595. Big Countries**
  - Basic SELECT and WHERE with OR
- **584. Find Customer Referee**
  - Basic SELECT and WHERE with IS NULL or !=

**Additional Resources:**
- [Mode Analytics SQL Tutorial: Basic SQL](https://mode.com/sql-tutorial/sql-basics/)

**Note:** Make sure you are checking for updates on Slack for important announcements.

---

## Week 2: Advanced Filtering, Aliases, & Introduction to Aggregate Functions

**Core Concepts:**
- Advanced WHERE operators (AND, OR, NOT, IN, BETWEEN, LIKE)
- Handling NULL values (IS NULL, IS NOT NULL)
- Column Aliases (AS)
- Introduction to Aggregate Functions (COUNT(), SUM(), AVG(), MIN(), MAX()) without GROUP BY

**Learning Objectives:**
- Construct complex filtering conditions
- Filter on ranges/lists/patterns
- Handle NULLs
- Rename columns
- Use basic aggregates on entire tables

**SQLZoo Exercises:**
- [3. SELECT from Nobel Tutorial](https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial)
- [6. SUM and COUNT](https://sqlzoo.net/wiki/SUM_and_COUNT)
  - Focus on aggregates without GROUP BY

**LeetCode Practice (Easy to Medium):**
- **183. Customers Who Never Order**
  - Uses NOT IN or LEFT JOIN... IS NULL, good for NULL understanding early on, though JOIN is formally later
- **1683. Invalid Tweets**
  - Uses LENGTH function, CHAR_LENGTH in MySQL, introduces a simple function with WHERE
- **1148. Article Views I**
  - Simple SELECT DISTINCT, WHERE, ORDER BY - distinct is also a good concept here

**Additional Resources:**
- [W3Schools SQL Tutorial](https://www.w3schools.com/sql/)

---

## Week 3: Grouping Data with GROUP BY & HAVING

**Core Concepts:**
- GROUP BY clause
- Using aggregate functions with GROUP BY
- HAVING clause
- Difference between WHERE and HAVING

**Learning Objectives:**
- Group data
- Calculate aggregates for groups
- Filter groups
- Understand logical order of operations

**SQLZoo Exercises:**
- [6. SUM and COUNT](https://sqlzoo.net/wiki/SUM_and_COUNT)
  - Focus on GROUP BY examples

**LeetCode Practice (Easy to Medium):**
- **596. Classes More Than 5 Students**
  - Classic GROUP BY and HAVING
- **1729. Find Followers Count**
  - GROUP BY, COUNT, ORDER BY
- **1050. Actors and Directors Who Cooperated At Least Three Times**
  - GROUP BY multiple columns, COUNT, HAVING

**Additional Resources:**
- [Mode Analytics SQL Tutorial: Aggregations](https://mode.com/sql-tutorial/sql-aggregations/)

---

## Week 4: Joining Tables – INNER & LEFT JOINs

**Core Concepts:**
- Primary/foreign keys
- INNER JOIN
- LEFT JOIN (or LEFT OUTER JOIN)
- ON clause
- Table aliases in joins

**Learning Objectives:**
- Identify when JOIN is needed
- Write INNER JOIN and LEFT JOIN queries
- Understand how NULLs are handled in LEFT JOINs

**SQLZoo Exercises:**
- [7. The JOIN operation](https://sqlzoo.net/wiki/The_JOIN_operation)
- [8. More JOIN operations](https://sqlzoo.net/wiki/More_JOIN_operations)
  - Start this section

**LeetCode Practice (Easy to Medium):**
- **175. Combine Two Tables**
  - Basic LEFT JOIN
- **586. Customer Placing the Largest Number of Orders**
  - Can be solved with JOIN, GROUP BY, ORDER BY, LIMIT. Subquery or CTE is also an option learned later
- **197. Rising Temperature**
  - Requires a JOIN (often self-join conceptually or using date functions) and comparing values from different rows/dates. Note: Could also use LAG() which is a window function, but good to try with JOINs first

**Additional Resources:**
- [Mode Analytics SQL Tutorial: Joins](https://mode.com/sql-tutorial/sql-joins/)

---

## Week 5: More JOINs, Subqueries & Common Table Expressions (CTEs)

**Core Concepts:**
- RIGHT JOIN
- FULL OUTER JOIN
- SELF JOIN
- Subqueries (scalar, in WHERE, SELECT, FROM)
- Introduction to CTEs (WITH clause)

**Learning Objectives:**
- Utilize different JOIN types
- Implement SELF JOINs
- Write subqueries
- Start using CTEs for readability

**SQLZoo Exercises:**
- [8. More JOIN operations](https://sqlzoo.net/wiki/More_JOIN_operations)
  - Complete this section
- [4. SELECT within SELECT Tutorial](https://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial)
- [9. Using Null](https://sqlzoo.net/wiki/Using_Null)

**LeetCode Practice (Easy to Medium):**
- **181. Employees Earning More Than Their Managers**
  - Classic SELF JOIN or subquery
- **182. Duplicate Emails**
  - Can use GROUP BY and HAVING, or a subquery with IN
- **627. Swap Salary**
  - This is an UPDATE statement, good for a brief look at DML, but primarily for CASE statement logic. If focusing purely on SELECT practice for this week, maybe 176. Second Highest Salary which uses subqueries/CTEs/offset
- **176. Second Highest Salary**
  - Good for subqueries, OFFSET, or even window functions later

**Additional Resources:**
- [Mode Analytics SQL Tutorial: Subqueries & CTEs](https://mode.com/sql-tutorial/sql-subqueries-common-table-expressions/)

---

## Week 6: String Functions, Date/Time Functions & Data Types

**Core Concepts:**
- Common SQL Data Types
- String manipulation (CONCAT, SUBSTRING, LENGTH, UPPER, LOWER, REPLACE, TRIM)
- Date/time functions (NOW(), CURRENT_DATE, EXTRACT(), DATE_ADD(), DATE_FORMAT())
- Syntax varies by SQL dialect

**Learning Objectives:**
- Understand common data types
- Manipulate strings
- Extract date components
- Perform basic date calculations/formatting

**SQLZoo Exercises:**
- **Apply functions within problems from previous sections**
  - Look for function examples in Numeric Examples section

**LeetCode Practice (Easy to Medium):**
- **1484. Group Sold Products By The Date**
  - Uses GROUP_CONCAT (MySQL specific, but concept of string aggregation), COUNT DISTINCT, GROUP BY date
- **1527. Patients With a Condition**
  - Uses LIKE for pattern matching, good string practice
- **196. Delete Duplicate Emails**
  - This is a DELETE problem, but often involves subqueries to identify duplicates first. Good conceptual DML practice. Alternatively, 1667. Fix Names in a Table for string functions like UPPER, LOWER, CONCAT, SUBSTRING
- **1667. Fix Names in a Table**
  - Excellent for UPPER, LOWER, SUBSTRING, CONCAT

**Additional Resources:**
- **SQL dialect documentation**
  - Refer to documentation for your specific SQL dialect (e.g., PostgreSQL, MySQL) for string and date/time functions. W3Schools is a good quick reference.

**Note:** This week relies more on other resources for function-specific practice.

---

## Week 7: Data Definition Language (DDL) & Data Manipulation Language (DML)

**Core Concepts:**
- DDL (CREATE TABLE, ALTER TABLE, DROP TABLE, basic constraints)
- DML (INSERT INTO, UPDATE, DELETE)

**Learning Objectives:**
- Understand DDL/DML
- Write basic CREATE TABLE
- Perform INSERT, UPDATE, DELETE
- Understand WHERE clause importance in DML

**SQLZoo Exercises:**
- **SQLZoo is query-focused**
  - Practice DDL/DML in a local database

**LeetCode Practice (Easy to Medium):**
- **627. Swap Salary**
  - Actually an UPDATE problem. Good for DML practice.
- **196. Delete Duplicate Emails**
  - A DELETE problem. Requires identifying rows to delete, often with a subquery.

**Additional Resources:**
- **Local database setup**
  - SQLite via DB Browser for SQLite, PostgreSQL, MySQL
- [Mode Analytics SQL Tutorial: DDL and DML](https://mode.com/sql-tutorial/sql-ddl-dml/)

**Note:** Focus for this week: Set up a local database (e.g., SQLite). Try to CREATE the tables from LeetCode problems. INSERT some sample data. UPDATE it. DELETE it. This hands-on practice is crucial for DDL/DML.

---

## Week 8: Introduction to Window Functions & Comprehensive Review

**Core Concepts:**
- Window Functions (ROW_NUMBER(), RANK(), DENSE_RANK())
- OVER() clause (PARTITION BY, ORDER BY)

**Learning Objectives:**
- Understand window functions
- Use ROW_NUMBER(), RANK(), DENSE_RANK()
- Apply basic PARTITION BY and ORDER BY

**SQLZoo Exercises:**
- [11. Window functions](https://sqlzoo.net/wiki/Window_functions)
- [10. Self join](https://sqlzoo.net/wiki/Self_join)
  - Review, or see if window functions offer alternative solutions

**LeetCode Practice (Easy to Medium):**
- **177. Nth Highest Salary**
  - Can be solved with window functions, subqueries, or LIMIT/OFFSET
- **184. Department Highest Salary**
  - Find employees who have the highest salary in each department. Uses JOIN and can be elegantly solved with window functions or subqueries
- **626. Exchange Seats**
  - Uses CASE statements and window functions like LEAD, LAG, or ROW_NUMBER can simplify logic
- **185. Department Top Three Salaries**
  - Classic window function problem with DENSE_RANK or RANK

**Additional Resources:**
- [Mode Analytics SQL Tutorial: Window Functions](https://mode.com/sql-tutorial/sql-window-functions/)

**Note:** Comprehensive Review: Revisit challenging problems, mixed problem sets, Q&A.

---

## Study Tips

- Practice Regularly: Dedicate at least 2-3 hours per week to hands-on practice
- Join Online Communities: Participate in SQL forums and Discord communities
- Build Projects: Apply learned concepts to real-world scenarios
- Document Progress: Keep notes on challenging concepts and solutions
- Review Regularly: Revisit previous weeks' material to reinforce learning
