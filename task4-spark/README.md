# Task 4. Spark
#### Requirements:

* python 3
* java 1.8 or higher
* $JAVA_HOME set up

### Launch:
1. (optional) setup [virtualenv](https://virtualenv.pypa.io/en/stable/installation/). I was using it, so every python file is prefixed with #!/venv/bin/python3 for you to execute it directly. Don't forget to grant execution rights though!
1. Install python dependencies:<br/>
`$ pip3 install -r requirements.txt`
- Export evnironmental variable needed for spark:<br/>`$ export PYSPARK_PYTHON=python3`
- Dump texts to JSON files (with count for every word in file):<br/>
`$ python3 preprocessing.py`

- Launch search application:<br/>
`$ python3 mb25.py "Любовный роман"`
