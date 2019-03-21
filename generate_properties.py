import json
import pprint

proj_dir = 'pca10040/s132' 

c_cpp_properties_dir = '.vscode/c_cpp_properties.json'
tasks_dir = '.vscode/tasks.json'
launch_dir = '.vscode/launch.json'
makefile_dir = proj_dir + '/armgcc/Makefile'

# Load the data from the json files and the makefile
with open(c_cpp_properties_dir, 'r+') as file:
  c_cpp_properties_data = json.load(file)
with open(tasks_dir, 'r+') as file:
  tasks_data = json.load(file)
with open(launch_dir, 'r+') as file:
  launch_data = json.load(file)
with open(makefile_dir, 'r+') as file:
  makefile_data = file.read()
  makefile_data = makefile_data.split('\n')

# Extract the include folders
include_folders = []
in_inc_folders = False
for line in makefile_data:
  if 'INC_FOLDERS' in line:
    in_inc_folders = True
    continue
  if in_inc_folders and line == '':
    in_inc_folders = False
    break
  if in_inc_folders:
    include_folders.append(line
      .replace('$(SDK_ROOT)', '$\{workspaceFolder\}/../../..')      
      .replace('$(PROJ_DIR)', '$\{workspaceFolder\}')        
      .replace('../config', '$\{workspaceFolder\}/' + proj_dir + '/config')
      .replace('\\', '')
      .strip())

# Extract the defines
defines = []
in_defines = False
for line in makefile_data:
  if not in_defines and 'CFLAGS' in line:
    in_defines = True
    continue
  if in_defines and line == '':
    in_defines = False
    break
  if in_defines and 'CFLAGS += -D' in line:
    defines.append(line
      .replace('CFLAGS += -D', '')
      .strip())

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
