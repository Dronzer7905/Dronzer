import urllib.request
import json
import sys

req = urllib.request.Request('https://api.github.com/repos/Dronzer7905/Dronzer/actions/runs', headers={'User-Agent': 'Mozilla/5.0'})
try:
    res = urllib.request.urlopen(req)
    data = json.loads(res.read())
    run = data['workflow_runs'][0]
    print(f"Status: {run['status']}, Conclusion: {run['conclusion']}, ID: {run['id']}")
    
    # fetch jobs for the run
    jobs_req = urllib.request.Request(f"https://api.github.com/repos/Dronzer7905/Dronzer/actions/runs/{run['id']}/jobs", headers={'User-Agent': 'Mozilla/5.0'})
    jobs_res = urllib.request.urlopen(jobs_req)
    jobs_data = json.loads(jobs_res.read())
    
    for job in jobs_data['jobs']:
        if job['conclusion'] == 'failure':
            print(f"Job failed: {job['name']}")
            # fetch logs
            log_req = urllib.request.Request(f"https://api.github.com/repos/Dronzer7905/Dronzer/actions/jobs/{job['id']}/logs", headers={'User-Agent': 'Mozilla/5.0'})
            try:
                log_res = urllib.request.urlopen(log_req)
                logs = log_res.read().decode('utf-8')
                print(logs[-5000:])
            except Exception as e:
                print(f"Could not fetch logs: {e}")
except Exception as e:
    print(f"Error: {e}")
