-- Creating table for Members
CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    JoinDate DATE NOT NULL,
    Gender VARCHAR(255)
);

-- Creating table for Trainers
CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255) NOT NULL,
    JoinDate DATE NOT NULL,
    Gender VARCHAR(255),
    PhoneNumber VARCHAR(100) UNIQUE
);

-- Creating table for Room
CREATE TABLE Room (
    RoomID SERIAL PRIMARY KEY,
    RoomName VARCHAR(255),
    Capacity INT,
    Type VARCHAR(255),
    Status VARCHAR(255)
);

-- Creating table for Equipment
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    EquipmentName VARCHAR(255),
    Status VARCHAR(100),
    LastMaintenanceDate DATE,
    WarrantyDate DATE
);

-- Creating table for Staff
CREATE TABLE Staff (
    StaffID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    PhoneNumber VARCHAR(15) UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    JoinDate DATE NOT NULL,
    IsOwner BOOLEAN DEFAULT FALSE
);

-- Creating table for FitnessGoals
CREATE TABLE FitnessGoals (
    GoalID SERIAL PRIMARY KEY,
    MemberID INT NOT NULL,
    GoalType VARCHAR(255) NOT NULL,
    GoalValue VARCHAR(255) NOT NULL,
    StartDate DATE NOT NULL,
    Status VARCHAR(100),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Creating table for HealthMetrics
CREATE TABLE HealthMetrics (
    MetricID SERIAL PRIMARY KEY,
    MemberID INT NOT NULL,
    MetricType VARCHAR(255) NOT NULL,
    MetricValue VARCHAR(255) NOT NULL,
    DateRecorded DATE NOT NULL,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Creating table for Schedule
CREATE TABLE Schedule (
    SessionID SERIAL PRIMARY KEY,
    TrainerID INT,
    RoomID INT,
    BookingID INT,
    SessionType VARCHAR(50) CHECK (SessionType IN ('Personal', 'Group')),
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    Price DECIMAL(10, 2),
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

-- Associative table for Members and Schedules
CREATE TABLE ScheduleMembers (
    MemberID INT,
    SessionID INT,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (SessionID) REFERENCES Schedule(SessionID),
    PRIMARY KEY (MemberID, SessionID)
);

-- Creating table for Room_Bookings
CREATE TABLE Room_Bookings (
    BookingID SERIAL PRIMARY KEY,
    RoomID INT,
    TrainerID INT,  
    BookingStartTime TIMESTAMP,
    BookingEndTime TIMESTAMP,
    ClassType VARCHAR(100),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID)
);
