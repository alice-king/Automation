import sys
import os
import requests
import json
import time

def main():
    token=sys.argv[1]
    status='success' if len(sys.argv)<3 else sys.argv[2]
    if status not in ['queued','in_progress','completed','action_required','cancelled','failure','neutral','success','skipped','stale','timed_out']:
        status='success'
    workflow_name=os.getenv('GITHUB_WORKFLOW')
    baseurl=os.getenv('GITHUB_API_URL')+'/repos/'+os.getenv('GITHUB_REPOSITORY')+'/actions/'
    headers={'Authorization':'token '+token,'Accept':'application/vnd.github.v3+json'}
    workflows=requests.get(baseurl+'workflows',headers=headers).json()['workflows']
    for workflow in workflows:
        if workflow_name==workflow['name'] or workflow_name==workflow['path']:
            runs=requests.get(baseurl+'workflows/'+str(workflow['id'])+'/runs?status='+status,headers=headers).json()['workflow_runs']
            for run in runs:
                requests.delete(baseurl+'runs/'+str(run['id']),headers=headers)

if __name__ == "__main__":
    main()