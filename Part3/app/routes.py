import os
import datetime
from app import app, db
from flask import render_template, request, flash, redirect, url_for
import ganga
import ganga.ganga
from ganga import Job, Executable, Local, File

ganga.enableMonitoring()

currentDir = os.path.dirname(os.path.realpath(__file__))

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")

@app.route("/create")
def create():
    return render_template("create.html", title="Create")

@app.route("/submit")
def sumbit():
    return "#TODO"
