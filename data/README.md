# How to import data into Weaviate

Pre-requisite

- The Weaviate instance must already finished starting, the instance is accesible via the FastAPI address, i.e. http://localhost:8088
  - Check if the instance is up and running by go to the address http://localhost:8088/v1

Steps:

Navigate to the Data directory from the root(/)
-|
|- utils\
 |- weaviate\
 |- **\*data\*** # This one
|- .gitignore
|- LICENSE
|- README.md

1. install dependencies with `pip3 install -r requirements.txt`
2. run the python file `python3 import.py`
3. Wait till finish, it will take a while
4. Verify that successfull import by go to http://localhost:8088/v1/objects
5. Around 25 objects should be present(but there are more, it just limit to 25, don't worry)
