-- Average score
-- reates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.
DELIMITER $$ ;
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
  DECLARE weighted_sum DOUBLE;
  DECLARE sum INT;
  SELECT SUM(weight) INTO sum FROM corrections INNER JOIN projects ON corrections.project_id=projects.id WHERE corrections.user_id=user_id;
  SELECT SUM((score * weight) / sum) INTO weighted_sum FROM corrections INNER JOIN projects ON corrections.project_id=projects.id WHERE corrections.user_id=user_id;
  UPDATE users SET average_score = weighted_sum WHERE id=user_id;
END$$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE max INT;
  DECLARE x INT;
  DECLARE current_id INT;
  SELECT COUNT(*) INTO max FROM users;
  SET x = 0;
  loop_label: LOOP
  SELECT id INTO current_id FROM users LIMIT 1 OFFSET x;
  CALL ComputeAverageWeightedScoreForUser(current_id);
  SET x = x + 1;
  IF x >= max 
  THEN
  LEAVE loop_label;
  END IF;
  END LOOP;
END $$
DELIMITER ; $$
