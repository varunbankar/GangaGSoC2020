########################################
######## GANGA CHALLENGE PART 3 ########
########################################

# Imports
from app import app
from flask import render_template, request, flash, redirect, url_for, jsonify
import json
import ganga
from ganga import Job, Executable, Local, jobs, config
from GangaCore.Utility.Config import getConfig

#--------------------------------------#

ganga.enableMonitoring()

#--------------------------------------#

# Home Page Route
@app.route("/")
@app.route("/home")
def home():

    recent = list(jobs[-10:])
    recent.reverse()

    dashboard = {
        "running": len(jobs.select(status="running")),
        "completed": len(jobs.select(status="completed")),
        "failed": len(jobs.select(status="failed")),
        "recent": recent,
    }

    status_color = {"new": "info", "completed": "success", "failed": "danger", "running": "primary", "submitted": "secondary"}

    return render_template("home.html", title="Home", status_color=status_color, dashboard=dashboard, recent=recent)

#--------------------------------------#

@app.route("/create")
def create():
    return render_template("create.html", title="Create")

#--------------------------------------#

@app.route("/deploy/sleep")
def deploy_sleep():
    submitSleepJob(60)
    flash("A Ganga Job to execute Sleep(60) submitted.", "success")
    return redirect(url_for("home"))


@app.route("/deploy/test")
def deploy_test_jobs():
    time = 10
    for i in range(0, 15):
        submitSleepJob(time)
        time += 5
    
    flash("Submitted 15 Test Jobs", "success")
     
    return redirect(url_for("jobsList"))

#--------------------------------------#

@app.route("/jobs")
def jobsList():
    jlist = list(jobs)
    jlist.reverse()
    status_color = {"new": "info", "completed": "success", "failed": "danger", "running": "primary", "submitted": "secondary"}
    return render_template("jobs.html", title="Jobs", jlist=jlist, status_color=status_color)

#--------------------------------------#   

@app.route("/config", methods=["GET", "POST"])
def configList():

    sections = []
    configList = []

    for c in config:
        configList.append(c)

    if request.method == "POST":
        sectionName = request.form.get("section")
        if sectionName is not None:
            section = getConfig(str(sectionName))
            sections.append(section)
            return render_template("config.html", title="Config", sections=sections, configList=configList)
        else:
            flash("Please select a config section to view.", "warning")

    for c in configList:
        section = getConfig(c)
        sections.append(section)

    return render_template("config.html", title="Config", sections=sections, configList=configList)

#--------------------------------------#

@app.route("/api/info", methods=["POST", "GET"])
@app.route("/api/info/<int:job_id>", methods=["GET", "POST"])
def info_api(job_id=None):
    """Return details about the job."""

    if request.method == "POST":
        if job_id is None:
            data = request.form.get("job_ids")
            job_ids = json.loads(data)
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
        else:
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
    
    job_ids = []
    job_info = []

    if job_id is None:
        for j in jobs:
            job_ids.append(j.id)
    else:
        job_ids.append(int(job_id))

    for j_id in job_ids:
        j = jobs(int(j_id))
        info = {
            "id": j.id,
            "name": j.name,
            "status": j.status
        }
        job_info.append(info)

    return jsonify(job_info)

#--------------------------------------#

@app.route("/api/dashboard", methods=["POST", "GET"])
def dashboard_api():

    dashboard = {
        "running": len(jobs.select(status="running")),
        "completed": len(jobs.select(status="completed")),
        "failed": len(jobs.select(status="failed")),
    }

    return jsonify(dashboard)

#--------------------------------------#


def submitSleepJob(sec):

    name = f"Sleep Ganga Job (Seconds={sec})"
    j = Job(name=name)
    j.application = Executable()
    j.application.exe = '/bin/sleep'
    j.application.args = str(sec)
    j.submit()


