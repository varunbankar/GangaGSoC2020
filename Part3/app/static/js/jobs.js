document.addEventListener('DOMContentLoaded', () => {
    setInterval(refreshStatus, 2000);
});

// Refresh Status of Jobs (Not of jobs with status = [completed, new, failed])
function refreshStatus() {

    job_ids = []
    document.querySelectorAll('.job').forEach(function(job) {
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
    request.send(data)

    request.onload = () => {

        if (request.status == 200) {
            const data = JSON.parse(request.responseText)
            data.forEach(function(job) {
                document.querySelector(`#job${job.id}`).children[1].children[0].innerHTML = `${job.status}`
                document.querySelector(`#job${job.id}`).dataset.status = `${job.status}`
                document.querySelector(`#job${job.id}`).children[1].children[0].className = `badge badge-${status_color[job.status]} badge-pill`
            })
        }
        
    }

}
