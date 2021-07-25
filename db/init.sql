CREATE DATABASE citiesData;
use citiesData;

CREATE TABLE IF NOT EXISTS addresses (
    `First_Name` VARCHAR(21) CHARACTER SET utf8,
    `Last_Name` VARCHAR(8) CHARACTER SET utf8,
    `Street` VARCHAR(32) CHARACTER SET utf8,
    `City` VARCHAR(11) CHARACTER SET utf8,
    `State` VARCHAR(3) CHARACTER SET utf8,
    `Postal_Code` INT
);
INSERT INTO addresses VALUES
    ('John','Doe','120 jefferson st.','Riverside',' NJ', 08075),
    ('Jack','McGinnis','220 hobo Av.','Phila',' PA',09119),
    ('John "Da Man"','Repici','120 Jefferson St.','Riverside',' NJ',08075),
    ('Stephen','Tyler','7452 Terrace "At the Plaza" road','SomeTown','SD', 91234),
    (NULL,'Blankman',NULL,'SomeTown',' SD', 00298),
    ('Joan "the bone", Anne','Jet','9th, at Terrace plc','Desert City','CO',00123);
