import os

print("-----------------")
print("Checking if the logging file exists")
assert os.path.isfile("log_worker.yaml") == True
print("Checking if the config file exists")
assert os.path.isfile("config.ini") == True
print("Checking if the DB migration file exists")
assert os.path.isfile("log_migrate_db.yaml") == True
print("Checking if the naked.py file exists")
assert os.path.isfile("naked.py") == True
print("Test done")
print("-----------------")


