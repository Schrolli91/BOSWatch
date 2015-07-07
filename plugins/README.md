### How to Code your own plugin:

More information and a little Tutorial coming soon!

### 1. Plugin template
##### 1.1 General
You can find a little template plugin file in `plugins/template/template.py`

##### 1.2 Plugin Init `.onLoad()`
This `.onLoad()` routine is called one time for initialize the plugin

##### 1.3 Plugin call `.run()`
This `.run()` routine is called every time an alarm comes in


### 2. Use Global Logging
##### 2.1 Init and Use
First you must import the logging module
```python
import logging # Global logger
```
Now you can send log messages with:

```python
logging.LOGLEVEL("MESSAGE")
```
You must replace the word `LOGLEVEL` with one if the following `debug`, `info`, `warning`, `error`, `exception` or `critical`

To use the right loglevel see next section `2.2 Choose right Loglevel`

##### 2.2 Choose right Loglevel
`debug`
all messages  to find errors and for the internal program flow

`info`
messages that serve only to inform the user

`warning`


`error`
error does not lead to the end of boswatch

`Exception`

`critical`
errors leading to the end of boswatch immediate - in plugins not allowed


### 3. Use config file
##### 3.1 Own configuration in config.ini
First you must set a new Section in `config.ini`
A section is between brackets. Its recommended to give the section the same name as the plugin. `[SECTION_NAME]`

Now you can an set a unlimited number of options with its own value in these format: `OPTION = VALUE`.

Here is the sample from the template plugin:
```python
[template]
test1 = testString
test2 = 123456
```

##### 3.2 Read data from config.ini
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


### 4. Global helper functions
##### 4.1 timeHandler.py
##### 4.2 wildcardHandler.py


### 5. Process the data from BOSWatch
Three parameters are passed during the alarm to the .run() method

##### 5.1 typ
Thats the function of the alarm. Possible values are **FMS**, **ZVEI** or **POC**

##### 5.2 freq
The reception frequency of the tuner in Hz

##### 5.3 data[ ]
