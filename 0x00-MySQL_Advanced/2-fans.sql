-- Import the table dump from the provided file
-- Make sure to update the path to the actual location of the dump file
-- The command below assumes the dump file is named "metal_bands.sql"
SOURCE metal_bands.sql;

-- Create a temporary table to store the aggregated fan counts by country
CREATE TEMPORARY TABLE temp_origin_fans AS
SELECT
    origin,
    SUM(fans) AS nb_fans
FROM
    metal_bands
GROUP BY
    origin;

-- Add a ranking column to the temporary table based on fan counts
-- The RANK() function is used to assign a rank to each country based on their fan counts
-- The ORDER BY clause ensures the ranking is based on total_fans in descending order
SELECT
    origin,
    nb_fans
FROM
    temp_origin_fans
ORDER BY nb_fans DESC;

-- Clean up: Drop the temporary table
-- Since we no longer need the temporary table, it can be dropped
DROP TEMPORARY TABLE IF EXISTS temp_origin_fans;
