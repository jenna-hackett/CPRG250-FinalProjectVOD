/*
  Script Name: top_directors_report.sql
  Author: JH
  Date: 08/12/2025
  -----------------------------------------------
  Report Title: Top Directors by Movie Count
  Description: This report lists the top 10 directors with the most movies in the database,
               along with the average duration of their films.
*/

SELECT
  d.director_first_name,
  d.director_last_name,
  COUNT(m.movie_id) AS total_movies, -- Group function to count the number of movies per director
  ROUND(AVG(m.movie_duration)) AS average_duration_minutes /* Group function and single-row function
  															to calculate the average movie duration */
FROM
  directors AS d
JOIN
  movies AS m ON d.director_id = m.director_id /* Joins directors to movies to link directors 
  												to their films */
GROUP BY
  d.director_id, d.director_first_name, d.director_last_name /* Groups results by director to 
  																aggregate data */
ORDER BY
  total_movies DESC -- Sorts the results to show directors with the most movies first
LIMIT 10; -- Restricts the report to the top 10 directors