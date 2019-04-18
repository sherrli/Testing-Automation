To build a docker container that sits on top of your OS, and run a testscript inside that container,  
```
docker build -t testscript .  
docker run testscript
```
**requirements.txt** is a list of python3 package dependencies that the testscript.py would need in order to run.  
**Dockerfile** is the file that tells the docker image what to install inside the container.
