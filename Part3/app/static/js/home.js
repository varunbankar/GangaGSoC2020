document.addEventListener('DOMContentLoaded', () => {
    Joke()
    setInterval(Joke, 8000);
    setInterval(refreshStatus, 5000);
    setInterval(refreshStats, 5000);
});

// AJAX request to get a programming joke from a API
function Joke() {

    const request = new XMLHttpRequest();
    request.open('GET', 'https://official-joke-api.appspot.com/jokes/programming/random');
    request.send()

    request.onload = () => {

        if (request.status == 200) {
            const data = JSON.parse(request.responseText)
            document.querySelector('#setup').innerHTML = `${data[0].setup}`;
            document.querySelector('#punchline').innerHTML = `&nbsp;`
            setTimeout(() => { document.querySelector('#punchline').innerHTML = `${data[0].punchline}`; }, 2000);
        }

    }

}

// Refresh Status of Recent Jobs (Not of jobs with status = [completed, new, failed])
function refreshStatus() {

    job_ids = []
    document.querySelectorAll('.recent-job').forEach(function(job) {
        if (job.dataset.status != "completed" && job.dataset.status != "new" && job.dataset.status != "failed"){
            job_ids.push(job.dataset.id)
        }
    });

    if (job_ids.length != 0) {
        sendData(job_ids)
    }

}

status_color = {"new": "info", "completed": "success", "failed": "danger", "running": "primary", "submitted": "secondary"}

// AJAX request to server to get job status
function sendData(job_ids) {

    const request = new XMLHttpRequest();
    request.open('POST', `/api/info`);
    const data = new FormData();
    data.append('job_ids', JSON.stringify(job_ids));
    request.send(data);

    request.onload = () => {

        if (request.status == 200) {
            const data = JSON.parse(request.responseText)
            data.forEach(function(job) {
                document.querySelector(`#job${job.id}`).children[0].innerHTML = `${job.status}`;
                document.querySelector(`#job${job.id}`).dataset.status = `${job.status}`;
                document.querySelector(`#job${job.id}`).children[0].className = `badge badge-${status_color[job.status]} badge-pill`;
            })
        }
    }

}

// Refresh Dashboard Stats
function refreshStats() {

    const request = new XMLHttpRequest();
    request.open('POST', `/api/dashboard`);
    request.send();

    request.onload = () => {

        if (request.status == 200) {
            const data = JSON.parse(request.responseText)
            document.querySelector(`#running`).innerHTML = `${data.running}`;
            document.querySelector(`#completed`).innerHTML = `${data.completed}`;
            document.querySelector(`#failed`).innerHTML = `${data.failed}`;
        }
    }

}