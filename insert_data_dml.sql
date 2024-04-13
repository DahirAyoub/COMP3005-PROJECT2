INSERT INTO Members (name, email, joindate, gender, password) VALUES
('John Doe', 'john.doe@example.com', '2024-04-01', 'Male', 'pass1234'),
('Jane Smith', 'jane.smith@example.com', '2024-04-02', 'Female', 'pass5678'),
('Alice Johnson', 'alice.j@example.com', '2024-04-03', 'Female', 'pass91011'),
('Bob Brown', 'bob.brown@example.com', '2024-04-04', 'Male', 'pass1213'),
('Charlie Davis', 'charlie.d@example.com', '2024-04-05', 'Other', 'pass1415'),
('Diana Ross', 'diana.ross@example.com', '2024-04-06', 'Female', 'pass1617'),
('Evan Smith', 'evan.smith@example.com', '2024-04-07', 'Male', 'pass1819'),
('Fiona Green', 'fiona.green@example.com', '2024-04-08', 'Female', 'pass2021'),
('George King', 'george.king@example.com', '2024-04-09', 'Male', 'pass2223'),
('Helen Ford', 'helen.ford@example.com', '2024-04-10', 'Female', 'pass2425');

INSERT INTO FitnessGoals (MemberID, GoalType, GoalValue, StartDate, Status) VALUES
(1, 'Lose Weight', '5kg', '2024-04-15', 'In Progress'),
(2, 'Gain Muscle', '3kg', '2024-04-16', 'Not Started'),
(3, 'Increase Stamina', '10km Running', '2024-04-17', 'In Progress'),
(4, 'Lose Weight', '8kg', '2024-04-18', 'In Progress'),
(5, 'Improve Flexibility', 'Able to touch toes', '2024-04-19', 'Completed'),
(6, 'Gain Muscle', '5kg', '2024-04-20', 'Not Started'),
(7, 'Lose Weight', '10kg', '2024-04-21', 'In Progress'),
(8, 'Lose Weight', '15kg', '2024-04-22', 'In Progress'),
(9, 'Increase Stamina', 'Half Marathon', '2024-04-23', 'Planned'),
(10, 'Improve Flexibility', 'Full Split', '2024-04-24', 'Not Started');


INSERT INTO HealthMetrics (MemberID, MetricType, MetricValue, DateRecorded) VALUES
(1, 'Weight', '80kg', '2024-04-10'),
(1, 'Height', '175cm', '2024-04-10'),
(2, 'Weight', '65kg', '2024-04-11'),
(2, 'Height', '160cm', '2024-04-11'),
(3, 'Weight', '90kg', '2024-04-12'),
(3, 'Height', '180cm', '2024-04-12'),
(4, 'Weight', '70kg', '2024-04-13'),
(4, 'Height', '165cm', '2024-04-13'),
(5, 'Weight', '60kg', '2024-04-14'),
(5, 'Height', '170cm', '2024-04-14'),
(6, 'Weight', '85kg', '2024-04-15'),
(6, 'Height', '175cm', '2024-04-15'),
(7, 'Weight', '75kg', '2024-04-16'),
(7, 'Height', '168cm', '2024-04-16'),
(8, 'Weight', '92kg', '2024-04-17'),
(8, 'Height', '182cm', '2024-04-17'),
(9, 'Weight', '77kg', '2024-04-18'),
(9, 'Height', '174cm', '2024-04-18'),
(10, 'Weight', '85kg', '2024-04-19'),
(10, 'Height', '176cm', '2024-04-19');


-- Insert sample trainers with expanded information
INSERT INTO Trainers (Name, PhoneNumber, Email) VALUES
('John Doe', '123-456-7890', 'johndoe@example.com'),
('Jane Smith', '987-654-3210', 'janesmith@example.com');

-- Assume you have a Rooms table and its entries are already defined as previously outlined

-- Insert sample sessions now linking to MemberID and RoomID
INSERT INTO Schedule (TrainerID, SessionType, StartTime, EndTime, MemberID, RoomID, Status, ClassType) VALUES
((SELECT TrainerID FROM Trainers WHERE Name = 'John Doe'), 'Personal', '2024-05-01 10:00', '2024-05-01 11:00', 1, 1, 'Booked', 'Yoga'),
((SELECT TrainerID FROM Trainers WHERE Name = 'Jane Smith'), 'Group', '2024-05-02 15:00', '2024-05-02 16:00', 2, 2, 'Booked', 'Weightlifting');
