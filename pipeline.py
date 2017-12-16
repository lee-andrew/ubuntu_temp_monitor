resources = """
resources:
- name: git_monitor
  type: git
  tags: [public]
  source:
    uri: git@github.com:lee-andrew/ubuntu_temp_monitor.git
    branch: master
    private_key: ((private_key))
    
- name: 5m
  type: time
  tags: [public]
  source: {interval: 5m}

"""
resource_state_template = """
- name: git_monitor_trigger_%(state)s
  type: git
  tags: [public]
  source:
    uri: git@github.com:lee-andrew/ubuntu_temp_monitor.git
    branch: master
    private_key: ((private_key))
    paths: [state/%(state)s]
"""

jobs = """
jobs:
- name: temp_monitor
  plan:
  - get: 5m
    tags: [public]
    trigger: true
  - get: git_monitor
    tags: [public]
  - task: read_temp
    tags: [public]
    params:
      ssh_user: ((ssh_user))
      ssh_pass: ((ssh_pass))
      ssh_host: ((ssh_host))
    file: git_monitor/tasks/get_status/task.yml
    
  - task: git_state
    tags: [public]
    params:
      git_user: ((git_user))
      git_email: ((git_email))
      cpu_temp_threshold: ((cpu_temp_threshold))
      gpu_temp_threshold: ((gpu_temp_threshold))
      psu_temp_threshold: ((psu_temp_threshold))
      sys_temp_threshold: ((sys_temp_threshold))
      cpu_fan_threshold: ((cpu_fan_threshold))
      case_fan1_threshold: ((case_fan1_threshold))
      case_fan2_threshold: ((case_fan2_threshold))
    file: git_monitor/tasks/status_threshold/task.yml
    
  - put: git_monitor
    tags: [public]
    params: {repository: output}      
"""

job_state_template = """  
- name: notify_%(state)s
  plan:
  - get: git_monitor_trigger_%(state)s
    tags: [public]
    trigger: true
  - get: git_monitor
    tags: [public]
  - task: notify
    input_mapping: {git_monitor_trigger: git_monitor_trigger_%(state)s}
    tags: [public]
    params:
      bot_type: %(state)s
      discord_webhook: ((discord_webhook))
    file: git_monitor/tasks/post_state/task.yml
"""

states = [
  "case_fan1",
  "case_fan2",
  "cpu_fan",
  "cpu_temp",
  "gpu_temp",
  "psu_temp",
  "sys_temp",
]
for state in states:
  resources = resources + resource_state_template % { "state": state }
  jobs = jobs + job_state_template % { "state": state }
print (resources + jobs)