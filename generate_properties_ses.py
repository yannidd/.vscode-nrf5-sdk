import json
import pprint
import os
from lxml import html
import xml.etree.ElementTree as ET

proj_dir = 'pca10040/s132' 

c_cpp_properties_dir = '.vscode/c_cpp_properties.json'
tasks_dir = '.vscode/tasks.json'
launch_dir = '.vscode/launch.json'
ses_dir = proj_dir + '/ses'

# Find the ses project file
ses_files = os.listdir(ses_dir)
ses_projects = [i for i in ses_files if '.emProject' in i]

# Load the data from the json files and the ses project file
with open(c_cpp_properties_dir, 'r+') as file:
  c_cpp_properties_data = json.load(file)
with open(tasks_dir, 'r+') as file:
  tasks_data = json.load(file)
with open(launch_dir, 'r+') as file:
  launch_data = json.load(file)
with open(ses_dir + '/' + ses_projects[0], 'r+') as file:
  ses_data = file.read()
  ses_data = ses_data.split('\n')

# Extract the include folders
include_folders = []
for line in ses_data:
  if 'c_user_include_directories' in line:
    include_folders.extend(line
      .replace('c_user_include_directories=', '')
      .replace(';../../../../../../', ' $\{workspaceFolder\}/../../../')
      .replace(';../../../',          ' $\{workspaceFolder\}/')
      .replace('"../../../',          ' $\{workspaceFolder\}/')
      .replace(';../../',             ' $\{workspaceFolder\}/' + proj_dir.split('/')[0] + '/')
      .replace(';../',                ' $\{workspaceFolder\}/' + proj_dir + '/')
      .replace(';',                   ' ')
      .replace('\\',                  '')
      .replace('"',                   '')
      .strip()
      .split(' '))
    break

# Extract the defines
defines = []
for line in ses_data:
  if 'c_preprocessor_definitions' in line:
    defines.extend(line
      .replace('c_preprocessor_definitions=', '')
      .replace('"',                   '')
      .strip()
      .split(';'))
    break

# Replace new values in the json files
c_cpp_properties_data['configurations'][0]['includePath'] = include_folders
c_cpp_properties_data['configurations'][0]['browse']['path'] = include_folders
c_cpp_properties_data['configurations'][0]['defines'] = defines

tasks_data['tasks'][0]['command'] = 'cd ./' + proj_dir + '/armgcc; make'
tasks_data['tasks'][1]['command'] = 'cd ./' + proj_dir + '/armgcc; make'

launch_data['configurations'][0]['executable'] = './' + proj_dir + '/armgcc/_build/nrf52832_xxaa.out'

# Dump the new data into the json file
with open(c_cpp_properties_dir, 'w') as file:
  json.dump(c_cpp_properties_data, file, indent=2)
with open(tasks_dir, 'w') as file:
  json.dump(tasks_data, file, indent=2)
with open(launch_dir, 'w') as file:
  json.dump(launch_data, file, indent=2)
