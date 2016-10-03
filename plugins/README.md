## How to Code your own plugin:

More information and a little Tutorial coming soon!

## 1. Plugin template
#### 1.1 General
You can find a little template plugin file in `plugins/template/template.py` But you can also take a look in all other plugins.

A plugin must be in an seperate folder with the same name of the .py file

#### 1.2 Plugin Init `.onLoad()`
This `.onLoad()` routine is called one time for initialize the plugin

#### 1.3 Plugin call `.run()`
This `.run()` routine is called every time an alarm comes in

Here are the information from BOSWatch available. See section `5. Process the data from BOSWatch`


## 2. Use Global Logging
#### 2.1 Init and Use
First you must import the logging module
```python
import logging # Global logger
```
Now you can send log messages with:

```python
logging.LOGLEVEL("MESSAGE")
```
You must replace the word `LOGLEVEL` with one if the following `debug`, `info`, `warning` or `error`

To use the right loglevel see next section `2.2 Choose right Loglevel`

#### 2.2 Choose right Loglevel
`debug`
all messages to find errors and for the internal program flow.

`info`
messages that serve only to inform the user.

`warning`
Warnings are notes and technical errors. Never leads to terminate BOSWatch.

`error`
An error that does not necessarily lead to end of BOSWatch, but an administrator intervention required.

`critical`
errors leading to the end of boswatch immediate - **in plugins not allowed** (Plugin cannot crash the entire program)


## 3. Use config file
#### 3.1 Own configuration in config.ini
First you must set a new Section in `config.ini`
A section is between brackets. Its recommended to give the section the same name as the plugin. `[SECTION_NAME]`

Now you can an set a unlimited number of options with its own value in these format: `OPTION = VALUE`.

Here is the sample from the template plugin:
```python
[template]
test1 = testString
test2 = 123456
```

#### 3.2 Read data from config.ini
To read yout configuration data you must import the `globals.py` where the global config-object is located:
```python
from includes import globalVars  # Global variables
```

Now you can get your configuration data with:
```python
VALUE = globals.config.get("SECTION", "OPTION") #Gets any value
```
or better, use this:
```python
VALUE = globals.config.getint("SECTION", "OPTION") #Value must be an Integer
VALUE = globals.config.getfloat("SECTION", "OPTION") #Value must be an Float
VALUE = globals.config.getboolean("SECTION", "OPTION") #Value must be an Boolean
```


## 4. Global helper functions
#### 4.1 configHandler.py
First you must include the helper file
```python
from includes.helper import configHandler
```
##### 4.1.1 `.checkConfig(section)`
This function read all options from a config section and prints it to the debug log. The return value is `true`, also the section var is empty. In case of error a `false` is returned and error printed to log.
```python
if configHandler.checkConfig("template"): #check config file
  ########## User Plugin CODE ##########
  pass
```


#### 4.2 timeHandler.py
First you must include the helper file
```python
from includes.helper import timeHandler
```
##### 4.2.1 `.curtime(format)`
```python
timeHandler.curtime() # returns a formated datetime string
```
you can give the function an format string. See https://docs.python.org/2/library/time.html#time.strftime

default (without format parameter) the function returns a date time with this format `%d.%m.%Y %H:%M:%S`
##### 4.2.2 `.getDate()`
```python
timeHandler.getDate() # returns the current date in format `%d.%m.%Y`
```
##### 4.2.3 `.getTime()`
```python
timeHandler.getTime() # returns the current time in format `%H:%M:%S`
```
##### 4.2.4 `.getTimestamp()`
```python
timeHandler.getTimestamp() # returns the current linux timestamp
```

#### 4.3 wildcardHandler.py
First you must include the helper file
```python
from includes.helper import wildcardHandler
```
##### 4.3.1 `.replaceWildcards(text,data)`
```python
wildcardHandler.replaceWildcards(text,data) # replace all standard wildcards
```
replace all the standard wildcards in the given text
the function needs the data[ ] var

defined wildcards:

**General:**
- `%TIME%` = Time (by script)
- `%DATE%` = Date (by script)
- `%DESCR%` = Description from csv-file

- `%BR%` = new line
- `%LPAR%` = "("
- `%RPAR%` = ")"

**FMS:**
- `%FMS%` = FMS Code
- `%STATUS%` = FMS Status
- `%DIR%` = Direction of the telegram (0/1)
- `%DIRT%` = Direction of the telegram (Text-String)
- `%TSI%` = Tactical Short Information (I-IV)

**ZVEI:**
- `%ZVEI%` = ZVEI 5-tone Code

**POCSAG:**
- `%RIC%` = Pocsag RIC
- `%FUNC%` = Pocsac function/Subric (1-4)
- `%FUNCCHAR%` = Pocsac function/Subric als character (a-d)
- `%MSG%` = Message of the Pocsag telegram
- `%BITRATE%` = Bitrate of the Pocsag telegram

## 5. Process the data from BOSWatch
Three parameters are passed during the alarm to the .run() method

#### 5.1 typ
Thats the function of the alarm. Possible values are `FMS`, `ZVEI` or `POC`

#### 5.2 freq
The reception frequency of the tuner in Hz

#### 5.3 data[ ]
You can get an information with `data["INFO"]`
In the data map are the folowing informations:

**ZVEI:**
- zvei
- description
- timestamp

**FMS:**
- fms
- status
- direction
- directionText
- tsi
- description
- timestamp

**POCSAG:**
- ric
- function
- functionChar
- msg
- bitrate
- description
- timestamp
