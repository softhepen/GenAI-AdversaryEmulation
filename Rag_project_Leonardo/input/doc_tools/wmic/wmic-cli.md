[Global Parameters] <command>

The following global parameters are available:

/NAMESPACE           Path to the namespace against which the alias must operate.

/ROLE                Path to the role containing the alias definitions.

/NODE                Servers against which the alias will operate.

/IMPLEVEL            Client implementation level.

/AUTHLEVEL           Client authentication level.

/LOCALE              Language ID to be used by the client.

/PRIVILEGES          Enable or disable all privileges.

/TRACE               Sends debug information output to stderr.

/RECORD              Records all input commands and output.

/INTERACTIVE         Sets or resets interactive mode.

/FAILFAST            Sets or resets FailFast mode.

/USER                User to be used during the session.

/PASSWORD            Password to be used for session access.

/OUTPUT              Specifies the mode for output redirection.

/APPEND              Specifies the mode for output redirection.

/AGGREGATE           Sets or resets aggregate mode.

/AUTHORITY           Specifies the <authority type> for the connection.

/?[:<BRIEF|FULL>]    Usage information.

In the current role, the following aliases are available:

ALIAS                    - Accesses aliases available in the local system.

BASEBOARD                - Management of the baseboard (also known as motherboard or system board).

BIOS                     - Management of basic I/O services (BIOS).

BOOTCONFIG               - Management of boot configuration.

CDROM                    - Management of the CD-ROM drive.

COMPUTERSYSTEM           - Management of the system.

CPU                      - Management of the CPU.

CSPRODUCT                - Computer information contained in SMBIOS.

DATAFILE                 - Management of data files.

DCOMAPP                  - Management of COM applications.

DESKTOP                  - Management of the user desktop.

DESKTOPMONITOR           - Management of the desktop monitor.

DEVICEMEMORYADDRESS      - Management of device memory addresses.

DISKDRIVE                - Management of physical disk drives.

DISKQUOTA                - Disk space usage for NTFS volumes.

DMACHANNEL               - Management of DMA (Direct Memory Access) channels.

ENVIRONMENT              - Management of system environment settings.

FSDIR                    - Management of file system directory entries.

GROUP                    - Management of group accounts.

IDECONTROLLER            - Management of IDE controllers.

IRQ                      - Management of IRQ (Interrupt Request Line).

JOB                      - Provides access to scheduled processes via the Task Scheduler service.

LOADORDER                - Management of system services defining execution dependencies.

LOGICALDISK              - Management of local storage devices.

LOGON                    - Logon sessions.

MEMCACHE                 - Management of cache memory.

MEMORYCHIP               - Information about memory chips.

MEMPHYSICAL              - Management of the computerâ€™s physical memory.

NETCLIENT                - Management of network clients.

NETLOGIN                 - Management of network logon information (for a specific user).

NETPROTOCOL              - Management of protocols (and related network characteristics).

NETUSE                   - Management of active network connections.

NIC                      - Management of NICs (Network Interface Controllers).

NICCONFIG                - Management of network adapters.

/NTDOMAIN                - Management of NT domains.

NTEVENT                  - Entries in the NT event log.

NTEVENTLOG               - Management of the NT event log file.

ONBOARDDEVICE            - Management of common onboard devices integrated into the motherboard (system board).

OS                       - Management of installed operating systems.

PAGEFILE                 - Management of the virtual memory swap file.

PAGEFILESET              - Management of paging file settings.

PARTITION                - Management of partitioned areas of a physical disk.

PORT                     - Management of I/O ports.

PORTCONNECTOR            - Management of physical connection ports.

PRINTER                  - Management of printing devices.

PRINTERCONFIG            - Management of printer configuration.

PRINTJOB                 - Management of print jobs.

PROCESS                  - Management of processes.

PRODUCT                  - Management of installation package activities.

QFE                      - QFE (Quick Fix Engineering).

QUOTASETTING             - Disk quota setting information on a volume.

RDACCOUNT                - Management of Remote Desktop Connection permissions.

RDNIC                    - Management of Remote Desktop Connection for a specific network adapter.

RDPERMISSIONS            - Permissions for a specific Remote Desktop Connection.

RDTOGGLE                 - Remote enable/disable of Remote Desktop Sharing listener.

RECOVEROS                - Information collected from memory when an operating system error occurs.

REGISTRY                 - Management of the system registry.

SCSICONTROLLER           - Management of SCSI controllers.

SERVER                   - Management of server information.

SERVICE                  - Management of service applications.

SHADOWCOPY               - Management of shadow copies.

SHADOWSTORAGE            - Management of shadow copy storage area.

SHARE                    - Management of shared resources.

SOFTWAREELEMENT          - Management of elements of a software product installed on a system.

SOFTWAREFEATURE          - Management of subsets of software products from SoftwareElement.

SOUNDDEV                 - Management of audio devices.

STARTUP                  - Management of commands automatically executed when users log on.

SYSACCOUNT               - Management of system accounts.

SYSDRIVER                - Management of system drivers for basic services.

SYSTEMENCLOSURE          - Management of the physical system enclosure.

SYSTEMSLOT               - Management of physical connection points such as ports, slots, peripherals, and proprietary connectors.

TAPEDRIVE                - Management of tape drives.

TEMPERATURE              - Management of data from a temperature sensor (electronic thermometer).

TIMEZONE                 - Management of time zone data.

UPS                      - Management of UPS (Uninterruptible Power Supply) units.

USERACCOUNT              - Management of user accounts.

VOLTAGE                  - Management of voltage sensor data (electronic voltmeter).

VOLUME                   - Management of local storage volumes.

VOLUMEQUOTASETTING       - Associates disk quota settings with a specific disk volume.

VOLUMEUSERQUOTA          - Management of per-user storage volume quotas.

WMISET                   - Management of WMI service operational parameters.

Additional Commands

CLASS     - Switches to the full WMI schema.

PATH      - Switches to full WMI object paths.

CONTEXT   - Displays the status of all global options.

QUIT/EXIT - Exits the program.


Parameters

NODE: Specifies which servers the alias will operate against.

Usage:

/NODE:<computer ID list>

NOTE:

<computer ID list> ::= <@filename | computer ID> | <@filename | computer ID> <,computer ID list>

If the option value contains special characters such as - or /, it must be enclosed in quotation marks.

USER: Provides the user to be used during the session.

Usage:

/USER:<userid>

NOTE: The user must be provided in the format <domain>\<user>. If the option value contains special characters such as - or /, it must be enclosed in quotation marks.

PASSWORD: Provides the password to be used for the session connection.

Usage:

/PASSWORD:<password>

NOTE: If the option value contains special characters such as - or /, it must be enclosed in quotation marks.

AUTHLEVEL: Specifies the authentication level for the command line. Default setting: Pktprivacy.

Usage:

/AUTHLEVEL:<authlevel>

Available authentication levels:

Default

None

Connect

Call

Pkt

Pktintegrity

Pktprivacy

IMPLEVEL: Determines which impersonation level the command line must use. Default setting: Impersonate.

Usage:

/IMPLEVEL:<impersonation level>[/AUTHORITY:<authority type>]

Available impersonation levels:

Anonymous

Identify

Impersonate

Delegate

NOTE: Use the /AUTHORITY parameter to specify the authority type.

TRACE: Specifies whether debug output information should be copied to stderr during request processing.

Usage:

/TRACE:<option>

NOTE: Allowed values for <option> are ON or OFF.

RECORD: Records all WMIC commands and output into an XML file.

Usage:

/RECORD:<file path>

NOTE: If the option value contains special characters such as - or /, it must be enclosed in quotation marks.


Aliases

PROCESS: Process management. BNF usage pattern:

(<alias> [WMIObject] | <alias> [<where clause>] | [<alias>] <where clause>) [<verb clause>]

Usage:

PROCESS ASSOC [<format identifier>]

PROCESS CALL <method name> [<actual parameter list>]

PROCESS CREATE <assignment list>

PROCESS DELETE

PROCESS GET [<property list>] [<get parameters>]

PROCESS LIST [<list format>] [<list parameters>]

SERVICE: Service application management.

Usage:

SERVICE ASSOC [<format identifier>]

SERVICE CALL <method name> [<actual parameter list>]

SERVICE CREATE <assignment list>

SERVICE DELETE

SERVICE GET [<property list>] [<get parameters>]

SERVICE LIST [<list format>] [<list parameters>]


SYSDRIVER: System driver management for a basic service.

Usage:

SYSDRIVER ASSOC [<format identifier>]

SYSDRIVER CALL <method name> [<actual parameter list>]

SYSDRIVER CREATE <assignment list>

SYSDRIVER DELETE

SYSDRIVER GET [<property list>] [<get parameters>]

SYSDRIVER LIST [<list format>] [<list parameters>]


STARTUP: Management of commands automatically executed when users log on.

Usage:

STARTUP ASSOC [<format identifier>]

STARTUP CREATE <assignment list>

STARTUP DELETE

STARTUP GET [<property list>] [<get parameters>]

STARTUP LIST [<list format>] [<list parameters>]

LOGICALDISK: Local storage device management.

Usage:

LOGICALDISK ASSOC [<format identifier>]

LOGICALDISK CALL <method name> [<actual parameter list>]

LOGICALDISK CREATE <assignment list>

LOGICALDISK DELETE

LOGICALDISK GET [<property list>] [<get parameters>]

LOGICALDISK LIST [<list format>] [<list parameters>]

LOGICALDISK SET [<assignment list>]

USERACCOUNT: User account management.

Usage:

USERACCOUNT ASSOC [<format identifier>]

USERACCOUNT CALL <method name> [<actual parameter list>]

USERACCOUNT CREATE <assignment list>

USERACCOUNT DELETE

USERACCOUNT GET [<property list>] [<get parameters>]

USERACCOUNT LIST [<list format>] [<list parameters>]

USERACCOUNT SET [<assignment list>]

REGISTRY: System registry management.

Usage:

REGISTRY ASSOC [<format identifier>]

REGISTRY CREATE <assignment list>

REGISTRY DELETE

REGISTRY GET [<property list>] [<get parameters>]

REGISTRY LIST [<list format>] [<list parameters>]

REGISTRY SET [<assignment list>]

NTEVENT: NT event log entries.

Usage:

NTEVENT ASSOC [<format identifier>]

NTEVENT CREATE <assignment list>

NTEVENT DELETE

NTEVENT GET [<property list>] [<get parameters>]

NTEVENT LIST [<list format>] [<list parameters>]

COMPUTERSYSTEM: System management.

Usage:

COMPUTERSYSTEM ASSOC [<format identifier>]

COMPUTERSYSTEM CALL <method name> [<actual parameter list>]

COMPUTERSYSTEM CREATE <assignment list>

COMPUTERSYSTEM DELETE

COMPUTERSYSTEM GET [<property list>] [<get parameters>]

COMPUTERSYSTEM LIST [<list format>] [<list parameters>]

COMPUTERSYSTEM SET [<assignment list>]

OS: Installed operating system management.

Usage:

OS ASSOC [<format identifier>]

OS CALL <method name> [<actual parameter list>]

OS CREATE <assignment list>

OS DELETE

OS GET [<property list>] [<get parameters>]

OS LIST [<list format>] [<list parameters>]

OS SET [<assignment list>]

NICCONFIG: Network adapter configuration management.

Usage:

NICCONFIG ASSOC [<format identifier>]

NICCONFIG CALL <method name> [<actual parameter list>]

NICCONFIG CREATE <assignment list>

NICCONFIG DELETE

NICCONFIG GET [<property list>] [<get parameters>]

NICCONFIG LIST [<list format>] [<list parameters>]

NETUSE: Active network connection management.

Usage:

NETUSE ASSOC [<format identifier>]

NETUSE CREATE <assignment list>

NETUSE DELETE

NETUSE GET [<property list>] [<get parameters>]

NETUSE LIST [<list format>] [<list parameters>]


































