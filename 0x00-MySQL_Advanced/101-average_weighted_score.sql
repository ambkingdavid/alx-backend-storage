-- create procedure
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE user_weighted_average FLOAT;
    
    -- Declare cursor to iterate through users
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Calculate the weighted average score for the user
        SELECT SUM(c.score * p.weight) / SUM(p.weight) INTO user_weighted_average
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Update the user's average weighted score in the users table
        UPDATE users
        SET average_score = user_weighted_average
        WHERE id = user_id;
    END LOOP;
    CLOSE cur;
END;
//
DELIMITER ;
