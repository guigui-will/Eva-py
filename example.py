from eva_dcl import Eva, EvaMap, EvaList
import os

config = Eva(os.path.join(os.path.dirname(__file__), 'config.eva'))

project_name = config.get('project', 'name')
print(f'Running {project_name} project')

dev = config.get('dev', 'name')
print(f'created by {dev}')

dev_messages: EvaList = config.get('dev', 'messages')
message = dev_messages.get(0)
print(f'{dev} said: {message}')

# 67 Lucas e meu kwaii 