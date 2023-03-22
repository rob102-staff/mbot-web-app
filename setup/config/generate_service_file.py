import os

# call whoami on the shell and get the output

# this is the username that will be used to run the service

os.system("whoami > username.txt")

# open the file and read the username

with open("username.txt", "r") as f:
    username = f.read()
username = username.strip()

# remove the file
os.remove("username.txt")

with open("mbotapi.service.template", "r") as f:
    template = f.read()

# replace the username in the template
template = template.replace("$USER$", username)

with open("mbotapi.service", "w") as f:
    f.write(template)
