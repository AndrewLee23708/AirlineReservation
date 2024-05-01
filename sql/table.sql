CREATE TABLE airline (
    airline_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (airline_name)
);

CREATE TABLE airport (
    airport_name VARCHAR(20) NOT NULL,
    airport_city VARCHAR(20) NOT NULL,
    PRIMARY KEY (airport_name)
);

CREATE TABLE airplane (           --include airline_name, weak dependency
    airplane_id INT NOT NULL,
    seats INT NOT NULL,
    airline_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (airline_name, airplane_id),
    FOREIGN KEY (airline_name) REFERENCES airline (airline_name)
);

CREATE TABLE airline_staff (
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    airline_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (airline_name) REFERENCES airline (airline_name)
);

CREATE TABLE permission (
    username VARCHAR(20) NOT NULL,
    permission VARCHAR(20) NOT NULL,
    PRIMARY KEY (username, permission),
    FOREIGN KEY (username) REFERENCES airline_staff (username)
);

CREATE TABLE flight (
    flight_num INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    airline_name VARCHAR(20) NOT NULL,
    departure_airport VARCHAR(20) NOT NULL,
    arrival_airport VARCHAR(20) NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    airplane_id INT NOT NULL,
  PRIMARY KEY(airline_name, flight_num),
  FOREIGN KEY(airline_name, airplane_id) REFERENCES airplane(airline_name, airplane_id),
    FOREIGN KEY (departure_airport) REFERENCES airport (airport_name),
    FOREIGN KEY (arrival_airport) REFERENCES airport (airport_name)
);

CREATE TABLE booking_agent (
    email VARCHAR(50) NOT NULL,
    password VARCHAR(20) NOT NULL,
    booking_agent_id INT UNIQUE NOT NULL,
    PRIMARY KEY (email)
);

CREATE TABLE ba_works_for (
    booking_agent_email VARCHAR(50) NOT NULL,
    airline_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (booking_agent_email, airline_name),
    FOREIGN KEY (booking_agent_email) REFERENCES booking_agent (email),
    FOREIGN KEY (airline_name) REFERENCES airline (airline_name)
);

CREATE TABLE customer (
    email VARCHAR(50) NOT NULL,
    name VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    building_number INT NOT NULL,
    street VARCHAR(20) NOT NULL,
    city VARCHAR(20) NOT NULL,
    state VARCHAR(20) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    passport_number VARCHAR(20) UNIQUE NOT NULL,
    passport_expiration DATE NOT NULL,
    passport_country VARCHAR(30) NOT NULL,
    date_of_birth DATE NOT NULL,
    PRIMARY KEY (email)
);

CREATE TABLE ticket (         -- takes weak dependency from flight 
    ticket_id INT AUTO_INCREMENT  NOT NULL,         -- DB will have no tickets until customers purchase
    flight_num INT NOT NULL,
    airline_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (ticket_id),
    FOREIGN KEY(airline_name, flight_num) REFERENCES flight(airline_name, flight_num)
);

CREATE TABLE purchases (
    ticket_id INT NOT NULL,
    customer_email VARCHAR(50) NOT NULL,
    booking_agent_id VARCHAR(50) NULL,  -- Switched to ba_ID, easier for input: Optional purchases so BA not necessary. 
    purchase_date DATE NOT NULL,
    PRIMARY KEY (ticket_id, customer_email),
    FOREIGN KEY (ticket_id) REFERENCES ticket (ticket_id),
    FOREIGN KEY (customer_email) REFERENCES customer (email),
    FOREIGN KEY (booking_agent_id) REFERENCES booking_agent (booking_agent_id)
);