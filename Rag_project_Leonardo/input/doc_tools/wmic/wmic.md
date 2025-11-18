# WMIC: WMI command-line utility

## Article
**15/07/2024**
**10 contributors**

## In this article
- Alias
- Switch
- Verbs
- Switches
- Show 2 more

## Important
WMIC is deprecated as of Windows 10, version 21H1; and as of the 21H1 semi-annual channel release of Windows Server. This utility is superseded by Windows PowerShell for WMI; see **Chapter 7 - Working with WMI**. This deprecation applies only to the WMIC utility. Windows Management Instrumentation (WMI) itself is not affected. Also see **Windows 10 features we're no longer developing**.

The WMI command-line (WMIC) utility provides a command-line interface for Windows Management Instrumentation (WMI). WMIC is compatible with existing shells and utility commands. The following information is a general reference guide for WMIC. For more information and guidelines on how to use WMIC, including additional information on aliases, verbs, switches, and commands, see:
- **Using Windows Management Instrumentation command-line**
- **WMIC - Take command-line control over WMI**

## Alias
An alias is a friendly renaming of a class, property, or method that makes WMI easier to use and read. You can determine what aliases are available for WMIC through the `/?` command. You can also determine the aliases for a specific class using the `<className> /?` command. For more information, see **WMIC aliases**.

## Switch
A switch is a WMIC option that you can set globally or optionally. For a list of available switches, see **WMIC switches**.

## Verbs
To use verbs in WMIC, enter the alias name followed by the verb. If an alias doesn't support a verb, you receive the message *"provider is not capable of the attempted operation."* For more info, see **WMIC verbs**.

Most aliases support the following verbs:

### ASSOC
Returns the result of the `Associators of (<wmi_object>)` query where `<wmi_object>` is the path of objects returned by the `PATH` or `CLASS` commands. The results are instances associated with the object. When `ASSOC` is used with an alias, the classes with the class underlying the alias are returned. By default, the output is returned in HTML format.

#### The `ASSOC` verb has the following switches:
- **`/RESULTCLASS:<classname>`**: Returned endpoints associated with the source object must belong to, or be derived from, the specified class.
- **`/RESULTROLE:<rolename>`**: Returned endpoints must play a specific role in associations with the source object.
- **`/ASSOCCLASS:<assocclass>`**: Returned endpoints must be associated with the source through the specified class, or one of its derived classes.

**Example:**
```cmd
os assoc
```

### CALL
Executes a method.

**Example:**
```cmd
service where caption="telnet" call startservice
```

> **Note:** To determine the methods available for a given class, use `/?`. For example, `service where caption="telnet" call /?` lists the available functions for the service class.

### CREATE
Creates a new instance and sets the property values. `CREATE` can't be used to create a new class.

**Example:**
```cmd
environment create name="temp"; variablevalue="new"
```

### DELETE
Deletes the current instance or set of instances. `DELETE` can be used to delete a class.

**Example:**
```cmd
process where name="calc.exe" delete
```

### GET
Retrieves specific property values.

#### The `GET` verb has the following switches:
- **`/VALUE`**: Output is formatted with each value listed on a separate line and with the name of the property.
- **`/ALL`**: Output is formatted as a table.
- **`/TRANSLATE:<translation table>`**: Translates the output using the translation table named by the command. The translation tables `BasicXml` and `NoComma` are included with WMIC.
- **`/EVERY:<interval>`**: Repeats the command every `<interval>` seconds.
- **`/FORMAT:<format specifier>`**: Specifies a keyword or XSL file name to format the data.

**Example:**
```cmd
process get name
```

### LIST
Shows data. `LIST` is the default verb.

#### The `LIST` verb has the following adverbs:
- **`BRIEF`**: Core set of properties.
- **`FULL`**: Full set of properties (default).
- **`INSTANCE`**: Instance paths only.
- **`STATUS`**: Status of the objects.
- **`SYSTEM`**: System properties.

#### The `LIST` verb has the following switches:
- **`/TRANSLATE:<translation table>`**: Translate the output using the specified translation table.
- **`/EVERY:<interval>`**: Repeat the command every `<interval>` seconds.
- **`/FORMAT:<format specifier>`**: Specifies a keyword or XSL file name to format the data.

**Example:**
```cmd
process list brief
```

### SET
Assigns values to properties.

**Example:**
```cmd
environment set name="temp", variablevalue="new"
```

## Switches
Global switches are used to set defaults for the WMIC environment. You can view the current value of the conditions set by these switches by entering the `CONTEXT` command.

- **`/NAMESPACE`**: Namespace that the alias typically uses. Default is `root\cimv2`.
- **`/ROLE`**: Namespace where WMIC looks for aliases and other WMIC info.
- **`/NODE`**: Computer names, comma delimited.
- **`/IMPLEVEL`**: Impersonation level.
- **`/AUTHLEVEL`**: Authentication level.
- **`/LOCALE`**: Locale.
- **`/PRIVILEGES`**: Enables or disables all privileges.
- **`/TRACE`**: Displays the success or failure of all functions used to execute WMIC commands.
- **`/RECORD`**: Records all output to an XML file.
- **`/INTERACTIVE`**: Typically, delete commands are confirmed.
- **`/FAILFAST`**: If ON, the `/NODE` computers are pinged before sending WMIC commands.
- **`/USER`**: User name used by WMIC when accessing the `/NODE` computers.
- **`/PASSWORD`**: Password used by WMIC when accessing the `/NODE` computers.
- **`/OUTPUT`**: Specifies a mode for all output redirection.
- **`/APPEND`**: Specifies a mode for output redirection without clearing destination.
- **`/AGGREGATE`**: Used with the LIST and GET `/EVERY` switch.

## Requirements
- **Minimum supported client**: Windows Vista
- **Minimum supported server**: Windows Server 2008