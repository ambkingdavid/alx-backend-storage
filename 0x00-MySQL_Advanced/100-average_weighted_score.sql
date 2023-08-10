-- create procedure
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN p_user_id INT)
BEGIN
    DECLARE user_weighted_average FLOAT;
    
    -- Calculate the weighted average score for the user
    SELECT SUM(c.score * p.weight) / SUM(p.weight) INTO user_weighted_average
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = p_user_id;
    
    -- Update the user's average weighted score in the users table
    UPDATE users
    SET average_score = user_weighted_average
    WHERE id = p_user_id;
END;
//
DELIMITER ;
