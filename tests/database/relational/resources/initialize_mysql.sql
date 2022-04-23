CREATE DATABASE IF NOT EXISTS sqlAlchemy;
USE sqlAlchemy;

CREATE TABLE IF NOT EXISTS project(
    projectId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(30),
    description VARCHAR(255),
    PRIMARY KEY(projectId)
);

CREATE TABLE IF NOT EXISTS task(
    taskId INT NOT NULL AUTO_INCREMENT,
    projectId INT,
    description VARCHAR(100),
    PRIMARY KEY(taskId),
    FOREIGN KEY(projectId) REFERENCES project(projectId)
);

DELETE * FROM Project;
DELETE * FROM Tasks;

INSERT INTO Project(title, description) VALUES
("Organize Photos", "Organize old iPhone photos by year"),
("Read more", "Read book per month this year");

INSERT INTO Tasks(project_id, description) VALUES
(1, "Organize 2019 photos"),
(1, "Organize 2020 photos"),
(2, "Read the Huntress");
