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
DELIMITER ; $$
