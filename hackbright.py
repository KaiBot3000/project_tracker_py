"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """
        INSERT INTO Students VALUES(?, ?, ?)"""
        
    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """
        SELECT * FROM Projects WHERE title = ?
        """

    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    print "Project: %s \nID: %s \nTitle: %s \nDescription: %s \nMax Grade: %s" % (
        title, row[0], row[1], row[2], row[3])

def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """
        SELECT grade FROM grades
        WHERE student_github = ? AND project_title = ?
        """
    db_cursor.execute(QUERY, (github, title))
    row = db_cursor.fetchone()
    print "%s got %s on %s" %(github, row[0],title)


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
        INSERT INTO Grades VALUES (?, ?, ?)
    """

    db_cursor.execute(QUERY, (github, title, grade))
    db_connection.commit()

    print "Successfully graded %s with a %s on %s" % (github, grade, title)



def add_project(title, description, max_grade):
    """Add a project to the Projects table."""

    QUERY = """
        INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)
    """

    db_cursor.execute(QUERY, (title, description, max_grade))
    db_connection.commit()

    print "Successfully added %s: %s with a max grade of %s" % (title, description, max_grade)

def get_grade_by_student(first_name):
    """Get all of a student's grades, line by line."""

    QUERY = """
        SELECT g.project_title, g.grade 
        FROM Students AS s JOIN Grades AS g 
        ON s.github = g.student_github
        WHERE s.first_name = ?
    """

    db_cursor.execute(QUERY, (first_name,))
    row = db_cursor.fetchall()
    
    if row != []:
        for project in row:
            print 'Grade for %s: %s' %(project[0], project[1])
    else:
        print 'Please try again and enter a FIRST NAME'



def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split('|')
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0] #works
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args[:3]   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "get_project_by_title":
            title = args[0] #works
            get_project_by_title(title)

        elif command == "get_grade_by_github_title":
            github, title = args[:2]
            get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            github, title, grade = args[:3]
            assign_grade(github, title, grade)

        elif command == "add_project":
            title, description, max_grade = args[:3]
            add_project(title, description, max_grade)

        elif command == "get_grade_by_student":
            first_name = args[0] #doesn't work
            get_grade_by_student(first_name)


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
