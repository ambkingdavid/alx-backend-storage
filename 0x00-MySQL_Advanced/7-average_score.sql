-- create a procedure ComputerAverageScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN p_user_id INT)
BEGIN
    DECLARE user_average FLOAT;
    
    -- Calculate the average score for the user
    SELECT AVG(score) INTO user_average
    FROM corrections
    WHERE user_id = p_user_id;
    
    -- Update the user's average score in the users table
    UPDATE users
    SET average_score = user_average
    WHERE id = p_user_id;
END;
//
DELIMITER ;
