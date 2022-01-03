CREATE DATABASE IF NOT EXISTS sqlAlchemy;
USE sqlAlchemy;

CREATE TABLE Project IF NOT EXISTS(
    project_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(30),
    description VARCHAR(255),
    PRIMARY KEY(project_id)
);

CREATE TABLE Tasks IF NOT EXISTS(
    task_id INT NOT NULL AUTO_INCREMENT,
    project_id INT,
    description VARCHAR(100),
    PRIMARY KEY(task_id)
    FOREIGN KEY(project_id) REFERENCES Project(project_id)
);
/*
INSERT INTO Project(title, description) VALUES
("Organize Photos", "Organize old iPhone photos by year"),
("Read more", "Read book per month this year");

INSERT INTO Tasks(project_id, description) VALUES
(1, "Organize 2019 photos"),
(1, "Organize 2020 photos"),
(2, "Read the Huntress");
*/