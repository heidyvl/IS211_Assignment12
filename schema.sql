CREATE TABLE Quizzes (  id INTEGER PRIMARY KEY,  subject TEXT,  questions INTEGER,  date TEXT);
CREATE TABLE Students (  id    INTEGER PRIMARY KEY,   fname  TEXT,  lname TEXT);
CREATE TABLE Students_Results (  quiz INTEGER,  student INTEGER,  FOREIGN KEY(student) REFERENCES Students(id),  FOREIGN KEY(quiz) REFERENCES Quizzes(id));
