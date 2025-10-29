SELECT
    location AS neighborhood,
    ROUND(AVG(price_per_sqft), 2) AS avg_price_per_sqft,
    COUNT(*) AS total_properties
FROM properties
GROUP BY location
ORDER BY avg_price_per_sqft DESC
LIMIT 5;


WITH MostExpensiveNeighborhood AS (
    SELECT location
    FROM properties
    GROUP BY location
    ORDER BY AVG(price_per_sqft) DESC
    LIMIT 1
)
SELECT 
    bedrooms,
    ROUND(AVG(price_rupees), 0) AS avg_price,
    COUNT(*) AS total_properties
FROM properties
WHERE location = (SELECT location FROM MostExpensiveNeighborhood)
  AND bedrooms IN (2, 3)
GROUP BY bedrooms
ORDER BY bedrooms;


SELECT
    location AS neighborhood,
    COUNT(*) AS listings_count
FROM properties
GROUP BY location
ORDER BY listings_count DESC;




SELECT *
FROM properties
WHERE location = 'Whitefield' AND bedrooms = 3
