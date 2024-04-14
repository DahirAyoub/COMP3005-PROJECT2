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
    Email VARCHAR(255) UNIQUE,
    Password CHAR(60) NOT NULL,
    JoinDate DATE NOT NULL,
    Gender VARCHAR(50),
    PhoneNumber VARCHAR(15) UNIQUE
);


-- Creating table for Schedule with corrected references and full integration
CREATE TABLE Schedule (
    SessionID SERIAL PRIMARY KEY,
    TrainerID INT,
    MemberID INT [],
    RoomID INT,
    BookingID INT,
    SessionType VARCHAR(50),
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    Price DECIMAL(10, 2), 
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

-- Table for Admin Staff
CREATE TABLE Staff (
    StaffID SERIAL INT PRIMARY KEY,
    Name VARCHAR(255),
    PhoneNumber VARCHAR(15) UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    JoinDate DATE NOT NULL,
    IsOwner BOOLEAN DEFAULT FALSE;
);


CREATE TABLE Room (
    RoomID SERIAL INT PRIMARY KEY,
    RoomName VARCHAR(255),
    Capacity INT,
    Type VARCHAR(255),
    Status VARCHAR(255)
);

CREATE TABLE Room_Bookings (
    BookingID SERIAL INT PRIMARY KEY,
    RoomID INT,
    TrainerID INT,
    BookingStartTime TIMESTAMP,
    BookingEndTime TIMESTAMP,
    ClassType VARCHAR(100),
    FOREIGN KEY (RoomID) REFERENCES Room (RoomID),
    FOREIGN KEY (StaffID) REFERENCES Admin_Staff (StaffID)
);

CREATE TABLE Equipment (
    EquipmentID SERIAL INT PRIMARY KEY,
    EquipmentName VARCHAR(255),
    Status VARCHAR(100),
    LastMaintenanceDate DATE,
    WarrantyDate DATE
);
