CREATE TABLE airline (
  airline_name varchar(50) NOT NULL,
  PRIMARY KEY(airline_name)
);

CREATE TABLE airline_staff (
  username varchar(100) NOT NULL,
  password varchar(100) NOT NULL,       -- if password not big enough encryption will be lost
  first_name varchar(100) NOT NULL, 
  last_name varchar(100) NOT NULL,
  date_of_birth date NOT NULL,
  airline_name varchar(50) NOT NULL,
  PRIMARY KEY(username),
  FOREIGN KEY(airline_name) REFERENCES airline(airline_name)
);

CREATE TABLE permission (
  username varchar(100) NOT NULL,
  permission_type varchar(100) NOT NULL,
  PRIMARY KEY(username, permission_type),
  FOREIGN KEY(username) REFERENCES airline_staff(username)
);

CREATE TABLE airplane (
  airline_name varchar(50) NOT NULL,
  airplane_id int(20) NOT NULL,
  seats int(100) NOT NULL,
  PRIMARY KEY(airline_name, airplane_id),
  FOREIGN KEY(airline_name) REFERENCES airline(airline_name)
);

CREATE TABLE airport (
  airport_name varchar(50) NOT NULL,
  airport_city varchar(100) NOT NULL,
  PRIMARY KEY(airport_name)
);

CREATE TABLE booking_agent (
  email varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  booking_agent_id int(20) NOT NULL,
  PRIMARY KEY(email)
);

CREATE TABLE booking_agent_work_for (
  email varchar(100) NOT NULL,
  airline_name varchar(50) NOT NULL,
  PRIMARY KEY(email, airline_name),
  FOREIGN KEY(email) REFERENCES booking_agent(email),
  FOREIGN KEY(airline_name) REFERENCES airline(airline_name)
);

CREATE TABLE customer (
  email varchar(100) NOT NULL,
  name varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  building_number varchar(100) NOT NULL,
  street varchar(100) NOT NULL,
  city varchar(100) NOT NULL,
  state varchar(100) NOT NULL,
  phone_number varchar(20) NOT NULL,
  passport_number varchar(20) NOT NULL,
  passport_expiration date NOT NULL,
  passport_country varchar(100) NOT NULL,
  date_of_birth date NOT NULL,
  PRIMARY KEY(email)
);

CREATE TABLE flight (
  airline_name varchar(50) NOT NULL,
  flight_num int(20) NOT NULL,
  departure_airport varchar(50) NOT NULL,
  departure_time datetime NOT NULL,
  arrival_airport varchar(50) NOT NULL,
  arrival_time datetime NOT NULL,
  price decimal(10,0) NOT NULL,
  status varchar(100) NOT NULL,
  airplane_id int(20) NOT NULL,
  PRIMARY KEY(airline_name, flight_num),
  FOREIGN KEY(airline_name, airplane_id) REFERENCES airplane(airline_name, airplane_id),
  FOREIGN KEY(departure_airport) REFERENCES airport(airport_name),
  FOREIGN KEY(arrival_airport) REFERENCES airport(airport_name)
);

CREATE TABLE ticket (
  ticket_id int(20) NOT NULL AUTO_INCREMENT, -- VERY IMPORTANT, WILL NOT WORK WITHOUT AUTOINCREMENT
  airline_name varchar(50) NOT NULL,
  flight_num int(20) NOT NULL,
  PRIMARY KEY(ticket_id),
  FOREIGN KEY(airline_name, flight_num) REFERENCES flight(airline_name, flight_num)
);

CREATE TABLE purchases (
  ticket_id int(20) NOT NULL,
  customer_email varchar(100) NOT NULL,
  booking_agent_id int(20),
  purchase_date date NOT NULL,
  PRIMARY KEY(ticket_id, customer_email),
  FOREIGN KEY(ticket_id) REFERENCES ticket(ticket_id),
  FOREIGN KEY(customer_email) REFERENCES customer(email)
);
