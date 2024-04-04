#!/usr/bin/env python

#-----------------------------------------------------------------------
# regdetails.py
# Author: Vivian Ha & Anaika Mehra
#-----------------------------------------------------------------------
import contextlib
import sqlite3
#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite?mode=ro'

def class_details(classid):

    with sqlite3.connect(DATABASE_URL, isolation_level=None,
        uri=True) as connection:

        with contextlib.closing(connection.cursor()) as cursor:
            # First prepared statement to find details given
            # the id of the class.
            print("goes in with statement ")
            stmt_str = "SELECT classes.courseid, days, starttime, "
            stmt_str += "endtime, bldg, roomnum, area, title, "
            stmt_str += "descrip, prereqs "
            stmt_str += "FROM classes, courses, crosslistings "
            stmt_str += "WHERE courses.courseid = "
            stmt_str += "classes.courseid "
            stmt_str += "AND courses.courseid = "
            stmt_str += "crosslistings.courseid "
            stmt_str += "AND classid LIKE ? "
            stmt_str += "ORDER BY coursenum"
            print(stmt_str)
            print([classid])
            print(type([classid]))
            cursor.execute(stmt_str, [classid])
            table = cursor.fetchall()
            print("1")

            # Second prepared statement to find the professor names
            # for the respective class. We can't do this in the
            # first statement as profs doesn't have course id.
            stmt_str_2 = "SELECT courseid, profname "
            stmt_str_2 += "FROM coursesprofs, profs "
            stmt_str_2 += "WHERE coursesprofs.profid = "
            stmt_str_2 += "profs.profid "
            stmt_str_2 += "ORDER BY profname"
            cursor.execute(stmt_str_2)
            table2 = cursor.fetchall()

            # Third prepared statement to find the various
            # departments that the class is listed under. We can't
            # do this in the first statement as we could have
            # multiple depts for one class.
            stmt_str_3 = "SELECT courses.courseid, dept, coursenum "
            stmt_str_3 += "FROM classes, courses, crosslistings "
            stmt_str_3 += "WHERE courses.courseid = "
            stmt_str_3 += "classes.courseid "
            stmt_str_3 += "AND courses.courseid = "
            stmt_str_3 += "crosslistings.courseid "
            stmt_str_3 += "AND classid LIKE ? "
            stmt_str_3 += "ORDER BY dept, coursenum"
            print("complete statement")
            print(stmt_str_3)
            cursor.execute(stmt_str_3, [classid])
            print("fails at execute of classid")
            table3 = cursor.fetchall()

            return table, table2, table3
