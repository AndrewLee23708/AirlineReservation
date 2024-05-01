-- Attempt Purchase procedure

DELIMITER //
CREATE PROCEDURE attempt_purchase(IN flight_num INT, IN customer_email VARCHAR(50), IN agent_id INT, OUT success BOOLEAN)
BEGIN
    DECLARE seats INT;
    DECLARE tickets_sold INT;

    -- Get the number of seats available for the flight
    SELECT A.seats INTO seats
    FROM airplane A JOIN flight F ON A.airplane_id = F.airplane_id
    WHERE F.flight_num = flight_num;

    -- Get the current number of tickets sold
    SELECT COUNT(*) INTO tickets_sold
    FROM ticket
    WHERE flight_num = flight_num;

    -- Check if there are seats available
    IF tickets_sold < seats THEN
        -- If seats are available, insert the ticket and purchase
        INSERT INTO ticket (airline_name, flight_num)
        VALUES ((SELECT airline_name FROM flight WHERE flight_num = flight_num), flight_num);
        
        INSERT INTO purchases (ticket_id, customer_email, booking_agent_id, purchase_date)
        VALUES (LAST_INSERT_ID(), customer_email, agent_id, CURDATE());

        SET success = TRUE;
    ELSE
        -- If no seats are available, do not allow purchase
        SET success = FALSE;
    END IF;
END //
DELIMITER ;
