from flask import Flask, render_template, request, redirect, url_for, flash  # For flask implementation
from bson import ObjectId  # For ObjectId to work
from pymongo import MongoClient
import os
import logging
import dbMongoInsert
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc@123'

@app.route('/')
def getFun():
    #x= request.args.get('x')
    #x=['Venkat','Somu','GV','Raghu','Saro','Balu']
    #y= request.args.get('arg2')
    ##  return render_template('intro.html')
    mems=dbMongoInsert.listRecords()
    #return 'getFun' + str(len(mems))
    return render_template('intro.html', title='Welcome',members=mems)
    #return "Flask render template example"

@app.route('/list')
def listFun():
    listval = dbMongoInsert.listRecords()
    return render_template('list.html', arg3= listval)

@app.route('/ind')
def indFun():
    return 'From ind Fun'


@app.route('/<HouseNumber>')
def member(HouseNumber):
    mem = dbMongoInsert.get_member(HouseNumber)
    return render_template('member.html', member=mem)


@app.route('/create', methods=('GET', 'POST'))
def create_member():
    if request.method == 'POST':
        HNU = request.form['HouseNumber']
        ONA = request.form['OwnerName']
        MOB = request.form['MobileNumber']

        if not HNU:
            flash('House Number is required!')
        else:
           dbMongoInsert.InsertMemberRecord(HNU,ONA,MOB)
           return redirect(url_for('getFun'))

    return render_template('createmember.html')


@app.route('/edit/<HouseNumber>', methods=('GET', 'POST'))
def edit_member(HouseNumber):
    mem = dbMongoInsert.get_member(HouseNumber)

    if request.method == 'POST':
        HNU = request.form['HouseNumber']
        ONA = request.form['OwnerName']
        MOB = request.form['MobileNumber']

        if not HNU:
            flash('House Number is required!')
        else:
            dbMongoInsert.UpdateMemberRecord(mem.get("_id"),HNU,ONA,MOB)
            return redirect(url_for('getFun'))

    return render_template('editmember.html', member=mem)

@app.route('/delete/<HouseNumber>', methods=('POST',))
def delete_member(HouseNumber):
    mem = dbMongoInsert.get_member(HouseNumber)
    dbMongoInsert.DeleteMemberRecord(mem.get("_id"))
    flash('"{}" was successfully deleted!'.format(mem['HouseNumber']))
    return redirect(url_for('getFun'))

if __name__ == "__main__":
    app.run(debug=True)