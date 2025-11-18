## Chapter 7: Using the command-line connection tool Plink

Plink is a command-line connection tool similar to UNIX `ssh`. It is mostly used for automated operations, such as making CVS access a repository on a remote server.

Plink is probably not what you want if you want to run an interactive session in a console window.

### 7.1 Starting Plink

Plink is a command line application. This means that you cannot just double-click on its icon to run it and instead you have to bring up a console window. In Windows 95, 98, and ME, this is called an ‘MS-DOS Prompt’, and in Windows NT, 2000, and XP, it is called a ‘Command Prompt’. It should be available from the Programs section of your Start Menu.

In order to use Plink, the file `plink.exe` will need either to be on your `PATH` or in your current directory. To add the directory containing Plink to your `PATH` environment variable, type into the console window:

    set PATH=C:\path\to\putty\directory;%PATH%

This will only work for the lifetime of that particular console window. To set your `PATH` more permanently on Windows NT, 2000, and XP, use the Environment tab of the System Control Panel. On Windows 95, 98, and ME, you will need to edit your `AUTOEXEC.BAT` to include a `set` command like the one above.

### 7.2 Using Plink

This section describes the basics of how to use Plink for interactive logins and for automated processes.

Once you've got a console window to type into, you can type `plink --help` to bring up a usage message. This tells you the version of Plink you're using, and gives you a brief summary of how to use Plink:

    C:\>plink --help
    Plink: command-line connection utility
    Release 0.83
    Usage: plink [options] [user@]host [command]
           ("host" can also be a PuTTY saved session name)
    Options:
      -V        print version information and exit
      -pgpfp    print PGP key fingerprints and exit
      -v        show verbose messages
      -load sessname  Load settings from saved session
      -ssh -telnet -rlogin -raw -serial
                force use of a particular protocol
      -ssh-connection
                force use of the bare ssh-connection protocol
      -P port   connect to specified port
      -l user   connect with specified username
      -batch    disable all interactive prompts
      -proxycmd command
                use 'command' as local proxy
      -sercfg configuration-string (e.g. 19200,8,n,1,X)
                Specify the serial configuration (serial only)
    The following options only apply to SSH connections:
      -pwfile file   login with password read from specified file
      -D [listen-IP:]listen-port
                Dynamic SOCKS-based port forwarding
      -L [listen-IP:]listen-port:host:port
                Forward local port to remote address
      -R [listen-IP:]listen-port:host:port
                Forward remote port to local address
      -X -x     enable / disable X11 forwarding
      -A -a     enable / disable agent forwarding
      -t -T     enable / disable pty allocation
      -1 -2     force use of particular SSH protocol version
      -4 -6     force use of IPv4 or IPv6
      -C        enable compression
      -i key    private key file for user authentication
      -noagent  disable use of Pageant
      -agent    enable use of Pageant
      -no-trivial-auth
                disconnect if SSH authentication succeeds trivially
      -noshare  disable use of connection sharing
      -share    enable use of connection sharing
      -hostkey keyid
                manually specify a host key (may be repeated)
      -sanitise-stderr, -sanitise-stdout, -no-sanitise-stderr, -no-sanitise-stdout
                do/don't strip control chars from standard output/error
      -no-antispoof   omit anti-spoofing prompt after authentication
      -m file   read remote command(s) from file
      -s        remote command is an SSH subsystem (SSH-2 only)
      -N        don't start a shell/command (SSH-2 only)
      -nc host:port
                open tunnel in place of session (SSH-2 only)
      -sshlog file
      -sshrawlog file
                log protocol details to a file
      -logoverwrite
      -logappend
                control what happens when a log file already exists
      -shareexists
                test whether a connection-sharing upstream exists


Once this works, you are ready to use Plink.

### 7.2.1 Using Plink for interactive logins

To make a simple interactive connection to a remote server, just type `plink` and then the host name:

    C:\>plink login.example.com

    Debian GNU/Linux 2.2 flunky.example.com
    flunky login:


You should then be able to log in as normal and run a session. The output sent by the server will be written straight to your command prompt window, which will most likely not interpret terminal control codes in the way the server expects it to. So if you run any full-screen applications, for example, you can expect to see strange characters appearing in your window. Interactive connections like this are not the main point of Plink.

In order to connect with a different protocol, you can give the command line options `-ssh`, `-ssh-connection`, `-telnet`, `-rlogin`, or `-raw`. To make an SSH connection, for example:

    C:\>plink -ssh login.example.com
    login as:


If you have already set up a PuTTY saved session, then instead of supplying a host name, you can give the saved session name. This allows you to use public-key authentication, specify a user name, and use most of the other features of PuTTY:

    C:\>plink my-ssh-session
    Sent username "fred"
    Authenticating with public key "fred@winbox"
    Last login: Thu Dec  6 19:25:33 2001 from :0.0
    fred@flunky:~$


(You can also use the `-load` command-line option to load a saved session; see [section 3.11.3.1](Chapter3.html#using-cmdline-load). If you use `-load`, the saved session exists, and it specifies a hostname, you cannot also specify a `host` or `user@host` argument - it will be treated as part of the remote command.)

### 7.2.2 Using Plink for automated connections

More typically Plink is used with the SSH protocol, to enable you to talk directly to a program running on the server. To do this you have to ensure Plink is _using_ the SSH protocol. You can do this in several ways:

*   Use the `-ssh` option as described in [section 7.2.1](#plink-usage-interactive).
*   Set up a PuTTY saved session that describes the server you are connecting to, and that also specifies the protocol as SSH.
*   Set the Windows environment variable `PLINK_PROTOCOL` to the word `ssh`.

Usually Plink is not invoked directly by a user, but run automatically by another process. Therefore you typically do not want Plink to prompt you for a user name or a password.

Next, you are likely to need to avoid the various interactive prompts Plink can produce. You might be prompted to verify the host key of the server you're connecting to, to enter a user name, or to enter a password.

To avoid being prompted for the server host key when using Plink for an automated connection, you can first make a _manual_ connection (using either of PuTTY or Plink) to the same server, verify the host key (see [section 2.2](Chapter2.html#gs-hostkey) for more information), and select ‘Accept’ to add the host key to the Registry. After that, Plink commands connecting to that server should not give a host key prompt unless the host key changes. Alternatively, you can specify the appropriate host key(s) on Plink's command line every time you use it; see [section 3.11.3.22](Chapter3.html#using-cmdline-hostkey).

To avoid being prompted for a user name, you can:

*   Use the `-l` option to specify a user name on the command line. For example, `plink login.example.com -l fred`.
*   Set up a PuTTY saved session that describes the server you are connecting to, and that also specifies the username to log in as (see [section 4.15.1](Chapter4.html#config-username)).

To avoid being prompted for a password, you should almost certainly set up public-key authentication. (See [chapter 8](Chapter8.html#pubkey) for a general introduction to public-key authentication.) Again, you can do this in two ways:

*   Set up a PuTTY saved session that describes the server you are connecting to, and that also specifies a private key file (see [section 4.22.1](Chapter4.html#config-ssh-privkey)). For this to work without prompting, your private key will need to have no passphrase.
*   Store the private key in Pageant. See [chapter 9](Chapter9.html#pageant) for further information.

Once you have done all this, you should be able to run a remote command on the SSH server machine and have it execute automatically with no prompting:

    C:\>plink login.example.com -l fred echo hello, world
    hello, world

    C:\>


Or, if you have set up a saved session with all the connection details:

    C:\>plink mysession echo hello, world
    hello, world

    C:\>


Then you can set up other programs to run this Plink command and talk to it as if it were a process on the server machine.

### 7.2.3 Plink command line options

Plink accepts all the general command line options supported by the PuTTY tools. See [section 3.11.3](Chapter3.html#using-general-opts) for a description of these options.

Plink also supports some of its own options. The following sections describe Plink's specific command-line options.

#### 7.2.3.1 `-batch`: disable all interactive prompts

If you use the `-batch` option, Plink will never give an interactive prompt while establishing the connection. If the server's host key is invalid, for example (see [section 2.2](Chapter2.html#gs-hostkey)), then the connection will simply be abandoned instead of asking you what to do next.

This may help Plink's behaviour when it is used in automated scripts: using `-batch`, if something goes wrong at connection time, the batch job will fail rather than hang.

If another program is invoking Plink on your behalf, then you might need to arrange that that program passes `-batch` to Plink. See [section 7.4](#plink-git) for an example involving Git.

#### 7.2.3.2 `-s`: remote command is SSH subsystem

If you specify the `-s` option, Plink passes the specified command as the name of an SSH ‘subsystem’ rather than an ordinary command line.

(This option is only meaningful with the SSH-2 protocol.)

#### 7.2.3.3 `-share`: Test and try to share an existing connection.

This option tries to detect if an existing connection can be shared (See [section 4.17.5](Chapter4.html#config-ssh-sharing) for more information about SSH connection sharing.) and reuses that connection.

A Plink invocation of the form:

    plink -share <session>


will test whether there is currently a viable ‘upstream’ for the session in question, which can be specified using any syntax you'd normally use with Plink to make an actual connection (a host/port number, a bare saved session name, `-load`, etc). If no ‘upstream’ viable session is found and `-share` is specified, this connection will be become the ‘upstream’ connection for subsequent connection sharing tries.

(This option is only meaningful with the SSH-2 protocol.)

#### 7.2.3.4 `-shareexists`: test for connection-sharing upstream

This option does not make a new connection; instead it allows testing for the presence of an existing connection that can be shared. (See [section 4.17.5](Chapter4.html#config-ssh-sharing) for more information about SSH connection sharing.)

A Plink invocation of the form:

    plink -shareexists <session>


will test whether there is currently a viable ‘upstream’ for the session in question, which can be specified using any syntax you'd normally use with Plink to make an actual connection (a host/port number, a bare saved session name, `-load`, etc). It returns a zero exit status if a usable ‘upstream’ exists, nonzero otherwise.

(This option is only meaningful with the SSH-2 protocol.)

#### 7.2.3.5 `-sanitise-`_stream_: control output sanitisation

In some situations, Plink applies a sanitisation pass to the output received from the server, to strip out control characters such as backspace and the escape character.

The idea of this is to prevent remote processes from sending confusing escape sequences through the standard error channel when Plink is being used as a transport for something like `git` or CVS. If the server actually wants to send an error message, it will probably be plain text; if the server abuses that channel to try to write over unexpected parts of your terminal display, Plink will try to stop it.

By default, this only happens for output channels which are sent to a Windows console device, or a Unix terminal device. (Any output stream going somewhere else is likely to be needed by an 8-bit protocol and must not be tampered with at all.) It also stops happening if you tell Plink to allocate a remote pseudo-terminal (see [section 3.11.3.12](Chapter3.html#using-cmdline-pty) and [section 4.24.1](Chapter4.html#config-ssh-pty)), on the basis that in that situation you often _want_ escape sequences from the server to go to your terminal.

But in case Plink guesses wrong about whether you want this sanitisation, you can override it in either direction, using one of these options:

`-sanitise-stderr`

Sanitise server data written to Plink's standard error channel, regardless of terminals and consoles and remote ptys.

`-no-sanitise-stderr`

Do not sanitise server data written to Plink's standard error channel.

`-sanitise-stdout`

Sanitise server data written to Plink's standard output channel.

`-no-sanitise-stdout`

Do not sanitise server data written to Plink's standard output channel.

#### 7.2.3.6 \-no-antispoof: turn off authentication spoofing protection prompt

In SSH, some possible server authentication methods require user input (for example, password authentication, or entering a private key passphrase), and others do not (e.g. a private key held in Pageant).

If you use Plink to run an interactive login session, and if Plink authenticates without needing any user interaction, and if the server is malicious or compromised, it could try to trick you into giving it authentication data that should not go to the server (such as your private key passphrase), by sending what _looks_ like one of Plink's local prompts, as if Plink had not already authenticated.

To protect against this, Plink's default policy is to finish the authentication phase with a final trivial prompt looking like this:

    Access granted. Press Return to begin session.


so that if you saw anything that looked like an authentication prompt _after_ that line, you would know it was not from Plink.

That extra interactive step is inconvenient. So Plink will turn it off in as many situations as it can:

*   If Plink's standard input is not pointing at a console or terminal device – for example, if you're using Plink as a transport for some automated application like version control – then you _can't_ type passphrases into the server anyway. In that situation, Plink won't try to protect you from the server trying to fool you into doing so.
*   If Plink is in batch mode (see [section 7.2.2](#plink-usage-batch)), then it _never_ does any interactive authentication. So anything looking like an interactive authentication prompt is automatically suspect, and so Plink omits the anti-spoofing prompt.

But if you still find the protective prompt inconvenient, and you trust the server not to try a trick like this, you can turn it off using the ‘`-no-antispoof`’ option.

7.3 Using Plink in batch files and scripts
------------------------------------------

Once you have set up Plink to be able to log in to a remote server without any interactive prompting (see [section 7.2.2](#plink-usage-batch)), you can use it for lots of scripting and batch purposes. For example, to start a backup on a remote machine, you might use a command like:

    plink root@myserver /etc/backups/do-backup.sh


Or perhaps you want to fetch all system log lines relating to a particular web area:

    plink mysession grep /~fred/ /var/log/httpd/access.log > fredlog


Any non-interactive command you could usefully run on the server command line, you can run in a batch file using Plink in this way.

### 7.4 Using Plink with Git

To use Plink for Git operations performed over SSH, you can set the environment variable `GIT_SSH_COMMAND` to point to Plink.

For example, if you've run PuTTY's full Windows installer and it has installed Plink in the default location, you might do this:

    set GIT_SSH_COMMAND="C:\Program Files\PuTTY\plink.exe"


or if you've put Plink somewhere else then you can do a similar thing with a different path.

This environment variable accepts a whole command line, not just an executable file name. So you can add Plink options to the end of it if you like. For example, if you're using Git in a batch-mode context, where your Git jobs are running unattended and nobody is available to answer interactive prompts, you might also append the ‘`-batch`’ option ([section 7.2.3.1](#plink-option-batch)):

    set GIT_SSH_COMMAND="C:\Program Files\PuTTY\plink.exe" -batch


and then if Plink unexpectedly prints a prompt of some kind (for example, because the SSH server's host key has changed), your batch job will terminate with an error message, instead of stopping and waiting for user input that will never arrive.

(However, you don't _always_ want to do this with Git. If you're using Git interactively, you might _want_ Plink to stop for interactive prompts – for example, to let you enter a password for the SSH server.)

### 7.5 Using Plink with CVS

To use Plink with CVS, you need to set the environment variable `CVS_RSH` to point to Plink:

    set CVS_RSH=\path\to\plink.exe


You also need to arrange to be able to connect to a remote host without any interactive prompts, as described in [section 7.2.2](#plink-usage-batch).

You should then be able to run CVS as follows:

    cvs -d :ext:user@sessionname:/path/to/repository co module


If you specified a username in your saved session, you don't even need to specify the ‘user’ part of this, and you can just say:

    cvs -d :ext:sessionname:/path/to/repository co module


### 7.6 Using Plink with WinCVS

Plink can also be used with WinCVS. Firstly, arrange for Plink to be able to connect to a remote host non-interactively, as described in [section 7.2.2](#plink-usage-batch).

Then, in WinCVS, bring up the ‘Preferences’ dialogue box from the _Admin_ menu, and switch to the ‘Ports’ tab. Tick the box there labelled ‘Check for an alternate `rsh` name’ and in the text entry field to the right enter the full path to `plink.exe`. Select ‘OK’ on the ‘Preferences’ dialogue box.

Next, select ‘Command Line’ from the WinCVS ‘Admin’ menu, and type a CVS command as in [section 7.5](#plink-cvs), for example:

    cvs -d :ext:user@hostname:/path/to/repository co module


or (if you're using a saved session):

    cvs -d :ext:user@sessionname:/path/to/repository co module


Select the folder you want to check out to with the ‘Change Folder’ button, and click ‘OK’ to check out your module. Once you've got modules checked out, WinCVS will happily invoke plink from the GUI for CVS operations.