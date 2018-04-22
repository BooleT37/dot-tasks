# Task 3. Hadoop

### Launch:
1. Set hadoop path to $HADOOP<br/>
`$ HADOOP=/usr/local/hadoop/`

1. Grant execution permissions to mapper and reducer:<br/>
`$ chmod +x ./mapper.py`<br/>
`$ chmod +x ./reducer.py`

1. (optional) Test mapper:<br/>
`$ echo "Apple was inside it apple was inside apple was ouside" | ./mapper.py`

1. (optional) Test reducer:<br/>
`$ echo "Apple was inside it apple was inside apple was ouside" | ./mapper.py | ./reducer.py`

1. Run the program:<br/>
`$ $HADOOP/bin/hadoop jar $HADOOP/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar \
	-input ./input  -output ./output \
	-file ./mapper.py -mapper ./mapper.py \
	-file ./reducer.py -reducer ./reducer.py`