### How to Code your own plugin:

More information and a little Tutorial coming soon!

### Plugin template
##### General
You can find a little template plugin file in `plugins/template/template.py`
##### .onLoad()
This onLoad() routine is called one time for initialize the plugin
##### .run()
This onLoad() routine is called every time an alarm comes in

### Use Global Logging
##### Init and Use
##### Choose right Loglevel

### Use config file
##### Own configuration in config.ini
First you must set a new Section in `config.ini`
A section is between brackets. Its recommended to give the section the same name as the plugin. `[SECTION_NAME]`

Now you can an set a unlimited number of options with its own value in these format: `OPTION = VALUE`.

Here is the sample from the template plugin:
```python
[template]
test1 = testString
test2 = 123456
```

##### Read data from config.ini
To read yout configuration data you must import the `globals.py` where the global config-object is located:
```python
from includes import globals  # Global variables
```

Now you can get your configration data with:
```python
VALUE = globals.config.get("SECTION", "OPTION") #Gets any value
```
or better, use this:
```python
VALUE = globals.config.getint("SECTION", "OPTION") #Value must be an Integer
VALUE = globals.config.getfloat("SECTION", "OPTION") #Value must be an Float
VALUE = globals.config.getboolean("SECTION", "OPTION") #Value must be an Boolean
```


### Global helper functions
##### timeHandler.py
##### wildcardHandler.py

### Process the data from BOSWatch
Three parameters are passed during the alarm to the .run() method
##### typ
Thats the function of the alarm. Possible values are **FMS**, **ZVEI** or **POC**
##### freq
The reception frequency of the tuner in Hz
##### data[ ]
