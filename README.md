File Tracker Worker Background
-------------
This is a part of full solution to detects duplicat files in directory, 
This micro-serves consume to messages from changes queue and start his work as following:
1. start handel removed file and delete the file from DB
2. handel modified file and record changes in log file (all the handlers record in log)
3. start works on added files, checking if file md5 already exists in DB, if not exists adding the file to DB and if exists add to file name "_DUP_#" at the end


## python version supported
```sh
Python 3.11.0
```

## Update config
```sh
  $ vim config.yml
```
please change the configuration
```yml
rabitMQ:
   host: localhost
   port: 5672
   queue_name: changes
directory: C:\Users\PycharmProjects\fileTracker\files
db_name: \Users\PycharmProjects\fileTrackerWorker\file_tracker
```

## Creating Virtual Environments
```sh
  $ python3 -m venv venv
```

## Run Virtual Environments
```sh
  $ source venv/bin/activate
```

## Update pip
```sh
  $ pip install --upgrade pip   
```

## Install requirements
```sh
  $ pip install -r requirements.txt
```

## run application
```shell
  $ python3 main.py
```
