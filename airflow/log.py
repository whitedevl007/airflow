# import subprocess


# import subprocess
# import sys

# def sub():
#     command = 'sparse run --name first_topology'
#     working_directory = '/home/nizam/project/Kafka-Storm'
#     module_directory = '/home/nizam/project/Kafka-Storm/src'  # Replace '/path/to/module' with the actual path to the module's directory

#     sys.path.insert(0, module_directory)  # Add the module directory to sys.path

#     process = subprocess.Popen(
#         command,
#         shell=True,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         cwd=working_directory
#     )

#     for line in iter(process.stdout.readline, b''):
#         print(line.decode().strip())

#     process.communicate()

#     if process.returncode == 0:
#         print("Command executed successfully.")
#     else:
#         print(f"Command failed with return code {process.returncode}.")

# sub()
