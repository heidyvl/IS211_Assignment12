CREATE TABLE Students(
  id    INTEGER PRIMARY KEY, 
  f_name  TEXT
  l_name  TEXT
);

CREATE TABLE Quizzes(
  id INTEGER PRIMARY KEY,
  subject TEXT,
  duration INTEGER,
  date TEXT
  
);

CREATE TABLE Students_Results(
  FOREIGN KEY(student) REFERENCES Students(id)
  FOREIGN KEY(quiz) REFERENCES Quizzes(id)
);



SELECT * FROM Students;
SELECT * FROM Quizzes;
SELECT * FROM Students_Results;
