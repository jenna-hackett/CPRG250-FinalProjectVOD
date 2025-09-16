/*
  Script Name: top_comedy_renters.sql
  Author: JH
  Date: 08/12/2025
  -----------------------------------------------
  Report Title: Top Ranked Customers for Comedy Movie Rentals
  Description: This report uses a subquery to find movies in the 'Comedy' category
               and then ranks the top 10 customers based on how many of those movies
               they have rented.
*/

SELECT
  UPPER(c.customer_first_name) AS first_name, -- Convert all names to upper case
  UPPER(c.customer_last_name) AS last_name,
  COUNT(r.rental_id) AS total_comedy_rentals, 
   -- OLAP function to rank customers
  RANK() OVER (ORDER BY COUNT(r.rental_id) DESC) AS rental_rank
FROM
  customers AS c
JOIN
  rentals AS r ON c.customer_id = r.customer_id
WHERE
  r.movie_id IN (
    -- Subquery to get all movie IDs for the 'Comedy' category
    SELECT
      movie_id
    FROM
      movie_categories
    WHERE
      category_name = 'Comedy'
  )
GROUP BY
  c.customer_id,
  c.customer_first_name,
  c.customer_last_name
ORDER BY
  rental_rank
LIMIT 10;