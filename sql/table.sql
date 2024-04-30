CREATE TABLE airline(
    name VARCHAR(20),
    PRIMARY KEY (name)
);

CREATE TABLE airport(
    name VARCHAR(20),
    city VARCHAR(20) NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE airplane(
    id INT,
    seats INT,
    airline_name VARCHAR(20),
    PRIMARY KEY (id),
    FOREIGN KEY (airline_name) REFERENCES airline(name)
);

CREATE TABLE airline_staff (
    username VARCHAR(20),
    password VARCHAR(20) NOT NULL,
    first_name VARCHAR(20) NOT NULL, 
    last_name VARCHAR(20) NOT NULL,
    date_of_birth DATE,
    airline_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (airline_name) REFERENCES airline(name)
);

CREATE TABLE permission (
    username VARCHAR(20),
    permission VARCHAR(20),
    PRIMARY KEY (username, permission),
    FOREIGN KEY (username) REFERENCES airline_staff(username)
);

CREATE TABLE flight(
    flight_num INT,
    departure_time DATETIME,
    arrival_time DATETIME,
    price DECIMAL(10,2),
    status VARCHAR(20),
    airline_name VARCHAR(20),
    arrival_airport_name VARCHAR(50),
    departure_airport_name VARCHAR(50),
    airplane_id INT,
    PRIMARY KEY (flight_num),
    FOREIGN KEY (airline_name) REFERENCES airline(name),
    FOREIGN KEY (arrival_airport_name) REFERENCES airport(name),
    FOREIGN KEY (departure_airport_name) REFERENCES airport(name),
    FOREIGN KEY (airplane_id) REFERENCES airplane(id)
);

CREATE TABLE booking_agent(
    email VARCHAR(50),
    password VARCHAR(20) NOT NULL,
    booking_agent_id INT UNIQUE,
    PRIMARY KEY (email)
);

CREATE TABLE ba_works_for(
    email VARCHAR(50),
    name VARCHAR(20),
    PRIMARY KEY (email, name),
    FOREIGN KEY (email) REFERENCES booking_agent(email),
    FOREIGN KEY (name) REFERENCES airline(name)
);

CREATE TABLE customer(
    email VARCHAR(50),
    name VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    building_number INT,
    street VARCHAR(20),
    city VARCHAR(20),
    state VARCHAR(20),
    phone_number VARCHAR(20),
    passport_number VARCHAR(20) UNIQUE,
    passport_expiration DATE,
    passport_country VARCHAR(30),
    date_of_birth DATE,
    PRIMARY KEY(email)
);

CREATE TABLE ticket(
    ticket_id INT,
    flight_num INT,
    customer_email VARCHAR(50),
    booking_agent_email VARCHAR(20),
    PRIMARY KEY (ticket_id),
    FOREIGN KEY (flight_num) REFERENCES flight(flight_num),
    FOREIGN KEY (customer_email) REFERENCES customer(email),
    FOREIGN KEY (booking_agent_email) REFERENCES booking_agent(email)
);

CREATE TABLE staff_works_for(
    username VARCHAR(20),
    name VARCHAR(20),
    PRIMARY KEY (username, name),
    FOREIGN KEY (username) REFERENCES airline_staff(username),
    FOREIGN KEY (name) REFERENCES airline(name)
);
