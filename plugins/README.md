## How to Code your own plugin:

More information and a little Tutorial coming soon!

## 1. Plugin template
#### 1.1 General
You can find a little template plugin file in `plugins/template/template.py`

#### 1.2 Plugin Init `.onLoad()`
This `.onLoad()` routine is called one time for initialize the plugin

#### 1.3 Plugin call `.run()`
This `.run()` routine is called every time an alarm comes in


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
You must replace the word `LOGLEVEL` with one if the following `debug`, `info`, `warning`, `error`, `exception` or `critical`

To use the right loglevel see next section `2.2 Choose right Loglevel`

#### 2.2 Choose right Loglevel
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
from includes import globals  # Global variables
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
#### 4.1 timeHandler.py
First you must include the helper file
```python
from includes.helper import timeHandler
```
##### 4.1.1 `.curtime(format)`
```python
timeHandler.curtime() # returns a formated datetime string
```
you can give the function an format string. See https://docs.python.org/2/library/time.html#time.strftime

default (without format parameter) the function returns a date time with this format `%d.%m.%Y %H:%M:%S`
##### 4.1.2 `.getDate()`
```python
timeHandler.getDate() # returns the current date in format `%d.%m.%Y`
```
##### 4.1.3 `.getTime()`
```python
timeHandler.getTime() # returns the current time in format `%H:%M:%S`
```
##### 4.1.4 `.getTimestamp()`
```python
timeHandler.getTimestamp() # returns the current linux timestamp
```

#### 4.2 wildcardHandler.py
First you must include the helper file
```python
from includes.helper import wildcardHandler
```
##### 4.2.1 'replaceWildcards(text,data)'
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
In the data map are the folowing informations:

**ZVEI:**
- zvei
- description

**FMS:**
- fms
- status
- direction
- directionText
- tsi
- description

**POCSAG:**
- ric
- function
- functionChar
- msg
- bitrate
- description
