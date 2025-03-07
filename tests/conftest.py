import os
import sys

project_route = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_route)
print("Project_Route : ",project_route)
print(sys.path)