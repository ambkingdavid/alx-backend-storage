-- Create a procedure(function) in mysql database
DELIMITER //
CREATE PROCEDURE AddBonus(IN p_user_id INT, IN p_project_name VARCHAR(255), IN p_score INT)
BEGIN
    -- Check if the project exists, if not, create it
    DECLARE project_id INT;

    SELECT id INTO project_id
    FROM projects
    WHERE name = p_project_name;

    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (p_project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Insert the new correction
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (p_user_id, project_id, p_score);

    -- Update the user's average score
    UPDATE users
    SET average_score = (SELECT AVG(score) FROM corrections WHERE user_id = p_user_id)
    WHERE id = p_user_id;
END;
//
DELIMITER ;
