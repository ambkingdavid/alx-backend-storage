-- Select the band name and calculate the lifespan based on split and formed years
SELECT 
    band_name,
    -- If the band has split, calculate the difference between split and formed years
    -- Otherwise, calculate the difference between 2022 and formed year
    IF(split IS NULL, 2022 - formed, split - formed) AS lifespan
FROM 
    metal_bands
-- Filter bands with the style 'Glam rock'
WHERE 
    style LIKE '%Glam rock%'
-- Order the results by lifespan in descending order
ORDER BY 
    lifespan DESC;
