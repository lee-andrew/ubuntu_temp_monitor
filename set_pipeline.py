import yaml
import json

filename = './pipeline_creds.yml'

resources_template = """
---
resources:
- name: git_monitor
  type: git
  tags: [public]
  source:
    uri: git@github.com:lee-andrew/ubuntu_temp_monitor.git
    private_key:
- name: git_monitor_trigger
  type: git
  tags: [public]
  source:
    uri: git@github.com:lee-andrew/ubuntu_temp_monitor.git
    private_key:
    paths:
      - thresholds/thresholds.yml
"""

jobs_template = """
jobs:
- name: Reapply Monitor Pipeline
  plan:
  - get: git_monitor
    tags: [public]
  - get: git_monitor_trigger
    tags: [public]
    trigger: true
  - task: apply_pipeline
    tags: [public]
    file: git_monitor/tasks/apply_pipeline/task.yml
    params: {}
"""

with open(filename, 'r') as stream:
    try:
        creds = yaml.load(stream)
        resources = yaml.load(resources_template)
        resources["resources"][0]["source"]["private_key"] = creds["private_key"]
        resources["resources"][1]["source"]["private_key"] = creds["private_key"]
        jobs = yaml.load(jobs_template)
        jobs["jobs"][0]["plan"][2]["params"]["creds"] = creds
        jobs["jobs"][0]["plan"][2]["params"]["concourse_host"] = creds["concourse_host"]
        jobs["jobs"][0]["plan"][2]["params"]["concourse_username"] = creds["concourse_username"]
        jobs["jobs"][0]["plan"][2]["params"]["concourse_password"] = creds["concourse_password"]
        resources["jobs"] = jobs["jobs"]
        print(json.dumps(resources))
    except yaml.YAMLError as exc:
        print(exc)