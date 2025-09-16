/*
  Script Name: top_10_most_rented_movies.sql
  Author: JH
  Date: 08/12/2025
 
  Report Title: Top 10 Most Rented Movies
  Description: This report identifies the movies with the highest rental counts
*/

SELECT
  m.movie_title,
  COUNT(r.movie_id) AS total_rentals -- Counts the number of times each movie has been rented
FROM movies AS m
JOIN rentals AS r
  ON m.movie_id = r.movie_id -- Joins the movies/rentals on the movie_id
GROUP BY
  m.movie_title -- Groups the results by movie title to count rentals for each movie
ORDER BY
  total_rentals DESC -- Sorts results in descending order to show most rented movies first
LIMIT 10;