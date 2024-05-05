delete from booking_agent_work_for;
delete from permission;
delete from purchases;
delete from Airline_Staff;
delete from Customer;
delete from Booking_agent;
delete from Ticket;
delete from Flight;
delete from Airport;
delete from Airplane;
delete from Airline;

-- Airlines
INSERT INTO airline VALUES ('Delta');
INSERT INTO airline VALUES ('ANA');

-- Airports
INSERT INTO airport VALUES ('JFK', 'New York');
INSERT INTO airport VALUES ('PVG', 'Shanghai');
INSERT INTO airport VALUES ('HND', 'Tokyo');

-- Customers
-- pass is lol
INSERT INTO customer VALUES ('andrewlee23708@gmail.com', 'Andrew Lee', '$2b$12$JzrUR7NIuSmI2I3d3f9OQ.JFk69H7b6RzFBmu0D3x7h.OUt/hCg1K', '100', 'Main St', 'New York', 'NY', 1234567890, 'AA1234567', '2030-12-31', 'USA', '1990-01-01');
INSERT INTO customer VALUES ('victoriamiao@gmail.com', 'Victoria Miao', '$2b$12$jLMl3XXD80cRhSAniPqbH.GRA2HUpjYZQavsrP3sW3PNUrDTcdKue', '101', 'Second St', 'Shanghai', 'SH', 1234567891, 'BB1234567', '2030-11-30', 'China', '1992-02-02');

-- Booking Agents
-- Password is lol
INSERT INTO booking_agent VALUES ('al7329@nyu.edu', '$2b$12$JXMrKjmQ6nX5Hvgzg.Vs3urKQS3fc.f0dFP1lBNXD1dkf0r2doU4W', 10001);
INSERT INTO booking_agent VALUES ('agent@example.com', '$2b$12$JXMrKjmQ6nX5Hvgzg.Vs3urKQS3fc.f0dFP1lBNXD1dkf0r2doU4W', 10002);

-- Airplanes
INSERT INTO airplane VALUES ('Delta', 1, 15);
INSERT INTO airplane VALUES ('Delta', 2, 5);   -- small seating to test seating limitations
INSERT INTO airplane VALUES ('ANA', 3, 10);

-- Airline Staff
-- pass is 123
INSERT INTO airline_staff VALUES ('staff_admin', '$2b$12$EYU.gplaBU8n4XfQb3xPVuQSCJ3bF5SJGGgdAPzRzE1JddSMBvmsa', 'John', 'Doe', '1980-03-15', 'Delta');
INSERT INTO airline_staff VALUES ('staff_operator', '$2b$12$mH7q92JnsJvmSi8vKluTqeJuKtFTsye7qbPq0T/rKWZotOjbOoR1m', 'Jane', 'Doe', '1985-04-16', 'Delta');

-- Flights
INSERT INTO flight VALUES ('Delta', 101, 'JFK', '2023-05-15 08:00:00', 'PVG', '2023-05-16 09:00:00', 800, 'in_progress', 1);
INSERT INTO flight VALUES ('Delta', 102, 'JFK', '2023-06-20 09:00:00', 'HND', '2023-06-21 10:00:00', 900, 'upcoming', 2);
INSERT INTO flight VALUES ('ANA', 201, 'PVG', '2023-07-15 11:00:00', 'HND', '2023-07-15 15:00:00', 750, 'delayed', 3);

-- Booking Agent Work Assignments
INSERT INTO booking_agent_work_for VALUES ('al7329@nyu.edu', 'Delta');
INSERT INTO booking_agent_work_for VALUES ('al7329@nyu.edu', 'ANA');

-- Permissions
INSERT INTO permission VALUES ('staff_admin', 'Admin');
INSERT INTO permission VALUES ('staff_operator', 'Operator');



-- Criterias
-- 1. Register an account and log in to your account
-- 2. Release the session after logging out of the account
-- 3. Staff cannot create a new airport
-- 4. Admin creates a new airport
-- 5. Build a new plane
-- 6. Create a new flight
-- 7. Customer/agent purchases air tickets
-- 8. Ticket exceeds limit check (consider when tickets cannot be purchased)