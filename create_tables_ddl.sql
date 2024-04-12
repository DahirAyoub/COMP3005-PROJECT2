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