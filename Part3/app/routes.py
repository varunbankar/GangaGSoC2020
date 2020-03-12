########################################
######## GANGA CHALLENGE PART 3 ########
########################################

# Imports
from app import app
from flask import render_template, request, flash, redirect, url_for, jsonify
import json
import ganga
import ganga.ganga
from ganga import Job, Executable, Local, jobs, config
from GangaCore.Utility.Config import getConfig

#--------------------------------------#

# Enable Ganga Monitoring
ganga.enableMonitoring()

#--------------------------------------#

# Home Page
@app.route("/")
@app.route("/home")
def home():
    """ Home Page """

    # Get last 10 jobs slice
    recent = list(jobs[-10:])
    recent.reverse()

    # Dashboard values
    dashboard = {
        "running": len(jobs.select(status="running")),
        "completed": len(jobs.select(status="completed")),
        "failed": len(jobs.select(status="failed")),
        "recent": recent,
    }

    status_color = {"new": "info", "completed": "success", "failed": "danger", "running": "primary", "submitted": "secondary"}

    return render_template("home.html", title="Home", status_color=status_color, dashboard=dashboard)

#--------------------------------------#

# Create Page
@app.route("/create")
def create():
    """ Create Page """

    return render_template("create.html", title="Create")

#--------------------------------------#

# Deploy Ganga Job (Sleep=60)
@app.route("/deploy/sleep")
def deploy_sleep():
    """ Deploy Ganga Job which executes Sleep=60 """

    # Submit Job
    submitSleepJob(60)

    # Notify and redirect to Create Page
    flash("A Ganga Job to execute Sleep(60) submitted.", "success")
    return redirect(url_for("create"))

#--------------------------------------#

# Deploy Multiple Ganga Job (Sleep=)
@app.route("/deploy/test")
def deploy_test_jobs():
    """ Deploy 15 Ganga Job which executes Sleep at different time intervals """

    # Submit jobs
    time = 15
    for i in range(0, 15):
        submitSleepJob(time)
        time += 5
    
    # Notify and redirect to Create Page
    flash("Submitted 15 Test Jobs", "success")
    return redirect(url_for("create"))

#--------------------------------------#

# Jobs Page
@app.route("/jobs")
def jobsList():
    """ Jobs Page to list all the jobs """

    # Get jobs list
    jlist = list(jobs)
    jlist.reverse()

    status_color = {"new": "info", "completed": "success", "failed": "danger", "running": "primary", "submitted": "secondary"}

    return render_template("jobs.html", title="Jobs", jlist=jlist, status_color=status_color)

#--------------------------------------#   

# Config Page
@app.route("/config", methods=["GET", "POST"])
def configList():
    """ Config Page to list all the config """

    sections = []
    configList = []

    # Store section names in configList
    for c in config:
        configList.append(c)

    # If specific config section is asked, serve that config section table only
    if request.method == "POST":
        
        # Get section name from form data
        sectionName = request.form.get("section")

        if sectionName is not None:

            # Get that particular config
            section = getConfig(str(sectionName))
            sections.append(section)

            return render_template("config.html", title="Config", sections=sections, configList=configList)

        else:

            flash("Please select a config section to view.", "warning")

    # Get complete config sections
    for c in configList:
        section = getConfig(c)
        sections.append(section)

    return render_template("config.html", title="Config", sections=sections, configList=configList)

#--------------------------------------#

# API to get Jobs Details
@app.route("/api/info", methods=["POST", "GET"])
@app.route("/api/info/<int:job_id>", methods=["GET", "POST"])
def info_api(job_id=None):
    """ Return details about jobs """

    # If method is POST
    if request.method == "POST":

        if job_id is None:

            # Get job ids data to give information about
            data = request.form.get("job_ids")
            job_ids = json.loads(data)

            # Store job info in a list
            job_info = []
            for j_id in job_ids:
                j = jobs(int(j_id))
                info = {
                    "id": j.id,
                    "name": j.name,
                    "status": j.status
                }
                job_info.append(info)

            # Return json version of the about list
            return jsonify(job_info)

        else:

            # Return information of a particular job ID
            job_ids = [].append(job_id)
            job_info = []

            for j_id in job_ids:
                j = jobs(int(j_id))
                info = {
                    "id": j.id,
                    "name": j.name,
                    "status": j.status
                }
                job_info.append(info)

            return jsonify(job_info)
    
    # If method is GET

    job_ids = []
    job_info = []

    # Store job ids in a list
    if job_id is None:
        for j in jobs:
            job_ids.append(j.id)
    else:
        job_ids.append(int(job_id))

    # Use the list to get job information
    for j_id in job_ids:
        j = jobs(int(j_id))
        info = {
            "id": j.id,
            "name": j.name,
            "status": j.status
        }
        job_info.append(info)

    # Send information
    return jsonify(job_info)

#--------------------------------------#

# API for Dashboard Numbers
@app.route("/api/dashboard", methods=["POST", "GET"])
def dashboard_api():
    """ API to get running, completed, failed job numbers """

    dashboard = {
        "running": len(jobs.select(status="running")),
        "completed": len(jobs.select(status="completed")),
        "failed": len(jobs.select(status="failed")),
    }

    return jsonify(dashboard)

#--------------------------------------#

# Submit Ganga Job which executed Sleep for 'sec' seconds
def submitSleepJob(sec):
    """ Sumbit Ganga Job which executes Sleep for 'sec' number of seconds """

    name = f"Sleep Ganga Job (Seconds={sec})"
    j = Job(name=name)
    j.application = Executable()
    j.application.exe = '/bin/sleep'
    j.application.args = str(sec)
    j.submit()

#--------------------------------------#

