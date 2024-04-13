CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password CHAR(60) NOT NULL,
    JoinDate DATE NOT NULL,
    Gender VARCHAR(50)
);

ALTER TABLE Members
ALTER COLUMN Password TYPE VARCHAR(255);

CREATE TABLE FitnessGoals (
    GoalID SERIAL PRIMARY KEY,
    MemberID INT NOT NULL,
    GoalType VARCHAR(255) NOT NULL,
    GoalValue VARCHAR(255) NOT NULL,
    StartDate DATE NOT NULL,
    Status VARCHAR(100),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

CREATE TABLE HealthMetrics (
    MetricID SERIAL PRIMARY KEY,
    MemberID INT NOT NULL,
    MetricType VARCHAR(255) NOT NULL,
    MetricValue VARCHAR(255) NOT NULL,
    DateRecorded DATE NOT NULL,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Creating table for Trainers with corrected schema
CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    PhoneNumber VARCHAR(15),
    Email VARCHAR(255) UNIQUE
);

-- Creating table for Schedule with corrected references and full integration
CREATE TABLE Schedule (
    SessionID SERIAL PRIMARY KEY,
    TrainerID INT,
    MemberID INT,
    RoomID INT,
    SessionType VARCHAR(50),
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    Status VARCHAR(50),
    ClassType VARCHAR(100),
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);
