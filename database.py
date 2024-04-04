import contextlib
import sqlite3
#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite?mode=ro'

# This function takes in all the user input and returns a tuple that
# contains all rows where user input matches database entries.
def course_overviews(dept, num, area, title):

    with sqlite3.connect(DATABASE_URL, isolation_level=None,
        uri=True) as connection:

        with contextlib.closing(connection.cursor()) as cursor:
            # This set of if-else statements help us handle the
            # case where users entered nothing for a column. They
            # also help us handle the escape characters.

            if title is not None:
                title = title.replace("%", r"\%")
                title = title.replace("_", r"\_")
                title = "%" + title + "%"
            else:
                title = "%"

            if dept is not None:
                dept = dept.replace("%", r"\%")
                dept = dept.replace("_", r"\_")
                dept = "%" + dept + "%"
            else:
                dept = "%"

            if area is not None:
                area = area.replace("%", r"\%")
                area = area.replace("_", r"\_")
                area = "%" + area + "%"
            else:
                area = "%"

            if num is not None:
                num = num.replace("%", r"\%")
                num = num.replace("_", r"\_")
                num = "%" + num + "%"
            else:
                num = "%"

            # SQL queries to create the prepared statement.
            stmt_str = "SELECT classid, dept, coursenum, "
            stmt_str += "area, title "
            stmt_str += "FROM courses, classes, crosslistings "
            stmt_str += "WHERE courses.courseid = "
            stmt_str += "classes.courseid "
            stmt_str += "AND courses.courseid = "
            stmt_str += "crosslistings.courseid "
            stmt_str += "AND dept LIKE ? ESCAPE '\\' "
            stmt_str += "AND coursenum LIKE ? ESCAPE '\\' "
            stmt_str += "AND area LIKE ? ESCAPE '\\' "
            stmt_str += "AND title LIKE ? ESCAPE '\\' "
            stmt_str += "ORDER BY dept, coursenum, classid"
            cursor.execute(stmt_str, (dept, num, area, title))
            # Using the cursor to create the tuple.
            table = cursor.fetchall()
            return table
