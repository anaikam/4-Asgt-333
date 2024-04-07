#!/usr/bin/env python

#-----------------------------------------------------------------------
# courses.py
#
#-----------------------------------------------------------------------
import sys
import flask
import database
from regdetails import class_details
#-----------------------------------------------------------------------
app = flask.Flask(__name__, template_folder='.')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    table = database.course_overviews("", "", "", "")
    html_code = flask.render_template('index.html', table = table)
    response = flask.make_response(html_code)
    return response

@app.route('/searchresults', methods=['GET'])
def search_results():
    dept = flask.request.args.get('dept')
    num = flask.request.args.get('coursenum')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')
    
    if dept is None:
        dept = ''
    if num is None:
        num = ''
    if area is None:
        area = ''
    if title is None:
        title = ''
    try:
        #handles the database (querying)
        table = database.course_overviews(dept, num, area, title)
        html_code = flask.render_template('courses.html', table=table)
        response = flask.make_response(html_code)   
        return response

    #handle error cases
    except Exception as ex:
        html_code = flask.render_template('error_courses.html', ex = ex,
            message = "A server error occurred. "
            + "Please contact the system administrator.")
        print(str(ex), file=sys.stderr)
        response = flask.make_response(html_code)
        return response

@app.route('/regdetails', methods=['GET'])
def regdetails():
    classid = flask.request.args.get('classid')
    dept = flask.request.args.get('dept')
    num = flask.request.args.get('coursenum')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')

    #handles the missing classid, non-int classid errors
    if classid in ('', None):
        html_code = flask.render_template('error_details.html',
            message = "missing classid")
        response = flask.make_response(html_code)
        return response
    if classid.isdigit() is False:
        html_code = flask.render_template('error_details.html',
            message = "non-integer classid")
        response = flask.make_response(html_code)
        return response

    try:
        gen_table, prof_table, dept_table = class_details(classid)
        department_table = []

        #grabs the correct departments and professors
        for row3 in dept_table:
            if gen_table[0][0] == row3[0]:
                department_table.append([row3[1], row3[2]])
        professors_table = []
        for row2 in prof_table:
            if gen_table[0][0] == row2[0]:
                professors_table.append(row2[1])
        html_code = flask.render_template('regdetails.html',
            classid=classid, general_table=gen_table[0],
            prof_table=professors_table,
            dept_table=department_table, dept=dept,
            area=area, coursenum=num, title=title)
        response = flask.make_response(html_code)
        return response

    #handles no classid error
    except Exception as ex:
        if(str(ex) == "cannot unpack non-iterable OperationalError object"):
            html_code = flask.render_template('error_details.html', ex = ex,
            message = "A server error occurred. "
            + "Please contact the system administrator.")
            print(str(ex), file=sys.stderr)
            response = flask.make_response(html_code)
            return response
        html_code = flask.render_template('error_details.html',
            ex = ex, message = "no class with classid "
            + classid + " exists")
        print(str(ex), file=sys.stderr)
        response = flask.make_response(html_code)
        return response
