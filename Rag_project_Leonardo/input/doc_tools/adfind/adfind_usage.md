AdFind Usage
adfind /?
AdFind V01.62.00cpp Joe Richards (support@joeware.net) October 2023

-help         Basic help.
-?            Basic help.
-??           Advanced/Expert help.
-????         Shortcut help.
-sc?          Shortcut help.
-meta?        Metadata help.
-regex?       Regular Expressions help.
-gui          Combine with help switch to open that output in text editor.

Usage:
 AdFind [switches] [-b basedn] [-f filter] [attr list]

   basedn        RFC 2253 DN to base search from.
                 If no base specified, defaults to default NC.
                 Base DN can also be specified as a SID, GUID, or IID.
   filter        RFC 2254 LDAP filter.
                 If no filter specified, defaults to objectclass=*.
   attr list     List of specific attributes to return, if nothing specified
                 returns 'default' attributes, aka * set.

  Switches: (designated by - or /)

           [CONNECTION OPTIONS]
   -h host:port  Host and port to use. If not specified uses port 389 on
                 default LDAP server. Localhost can be specified as '.'.
                 Port can also be specified via -p and -gc.
                 IPv6 IP address w/ port is specified [address]:port
   -gc           Search Global Catalog (port 3268).
   -p port       Alternate method to specify port to connect to.

           [QUERY OPTIONS]
   -s scope      Scope of search. Base, One[Level], Sub[tree].
   -t xxx        Timeout value for query, default 120 seconds.

           [OUTPUT OPTIONS]
   -c            Object count only.
   -dn           Object DN's only.
   -appver       Output AdFind versioning info.


  Notes:
    o This tool was written with simple US ASCII in mind. UNICODE and special
      ASCII characters such as characters with umlauts or graphics may not
      be output correctly due to how the command prompt handles those
      characters. If you see this occurring, redirect the output to a text file
      with the command prompt redirection symbol (>) and it is possible the
      program will give the desired output.


  Ex1:
    adfind -b dc=joehome,dc=net -f "objectcategory=computer"
      Find all computer objects in joehome.net and displays all attributes

  Ex2:
    adfind -b dc=joehome,dc=net -f "objectcategory=computer" cn createTimeStamp
      Find all computer objects in joehome.net and displays cn and createTimeStamp

  Ex3:
    adfind -h .:50000 -b cn=ab -f "objectcategory=person"
      Find all person objects on cn=ab container of local ADAM instance


 This software is Freeware. Use at your own risk.
 I do not warrant this software to be fit for any purpose or use and
 I do not guarantee that it will not damage or destroy your system.
 Contact support@joeware.net via email for licensing information to package
 this utility in commercial products.

 See full Warranty documentation or download the latest version
 on http://www.joeware.net.

 If you have improvement ideas, bugs, or just wish to say Hi, I
 receive email 24x7 and read it in a semi-regular timeframe.
 You can usually find me at support@joeware.net

adfind /??
AdFind V01.62.00cpp Joe Richards (support@joeware.net) October 2023

-help         Basic help.
-?            Basic help.
-??           Advanced/Expert help.
-????         Shortcut help.
-sc?          Shortcut help.
-meta?        Metadata help.
-regex?       Regular Expressions help.
-gui          Combine with help switch to open that output in text editor.

Usage:
 AdFind [switches] [-b basedn] [-f filter] [attr list]

   basedn        RFC 2253 DN to base search from.
                 If no base specified, defaults to default NC.
                 Base DN can also be specified as a SID, GUID, or IID.
   filter        RFC 2254 LDAP filter.
                 If no filter specified, defaults to objectclass=*.
   attr list     List of specific attributes to return, if nothing specified
                 returns 'default' attributes, aka * set.

  Switches: (designated by - or /)

           [CONNECTION OPTIONS]
   -h host:port  Host and port to use. If not specified uses port 389 on
                 default LDAP server. Localhost can be specified as '.'.
                 Port can also be specified via -p and -gc.
                 IPv6 IP address w/ port is specified [address]:port
   -gc           Search Global Catalog (port 3268).
   -gcb          Combines -gc -null switches. i.e. Full forest search.
   -gco          Only use GC port; do not use port 389. Note that normal secure bind
                 will start with Kerberos and Kerberos will do some SRV record
                 lookups and some LDAP "pings" to UDP 389. To avoid you should
                 also use -arecex and -ntlm (or -digest or -simple).
   -this xxx     Combines -s BASE and -b xxx
   -p port       Alternate method to specify port to connect to.
   -hh host:port Combines -h with -arecex
   -hd host:port Combines -h with -default
   --------------Advanced--------------
   -writeable    Use a writeable domain controller.
   -kerbenc      Kerberos Encryption (LDAP_OPT_ENCRYPT).
   -ssl          Use SSL
   -sslignoresrvcert  Ignore any problems with the SSL server cert.
   -starttls     Use StartTLS
   -arecex       Hostname has a actual host name, not domain name.
   -url xx       Specify LDAP(S) URL.
                  o LDAP://host:port/basedn?comma_delim_attribs?scope?filter
                  o See https://www.ldap.com/ldap-urls

           [QUERY OPTIONS]
   -s scope      Scope of search. Base, OneLevel, Subtree.
   -base         Alias for -s base.
   -one          Alias for -s onelevel.
   -onelevel     Alias for -s onelevel.
   -sub          Alias for -s subtree.
   -subtree      Alias for -s subtree.
   -t xxx        Timeout value for query, default 120 seconds.
   --------------Advanced--------------
   -bb xx        Base level query of XX. Combines -b xx and -s base.
   -nopaging     [BETA] Turn off paging. Also turns off referrals.
   -nopaging2    [BETA] Turn off paging. Does not turn off referrals.
   -ps size      Page size, default page size = 1000.
   -maxe xx      Max number of entries to be returned.
   -upto xx Process up to xx piped in objects and then stop.
   -null         Use null base.
   -root         Determine and use root partition for BaseDN.
   -config       Determine and use configuration partition for BaseDN.
   -schema       Determine and use schema partition for BaseDN.
   -default      Determine and use default partition for BaseDN.
   -rb xx        Relative Base, use with special BaseDN's above.
                     So you could specify -default and -rb cn=users.
                     Can also use -rb when piping DNs in.
   -rbb xx       Same as -rb but with -s base added.
   -users        Use cn=users,<default domain> for base.
   -forestdns    Use ForestDNS NDNC for base.
   -domaindns    Use DomainDNS NDNC for base. Use default domain by default.
   -dcs          Use Domain Controllers container of default domain for base.
   -gpo          Use System Policies container of default domain for base.
   -psocontainer Use PSO Container of default domain for base.
   -quotas       Use NTDS Quotas container of default domain for base.
   -ldappolicy   Use Ldap Query Policies container for base.
   -xrights      Use Extended Rights container for base.
   -partitions   Use Partitions container for base.
   -sites        Use Sites container for base.
   -subnets      Use Subnets container for base.
   -exch         Use Exchange Services container for base.
   -pki          Use CN=Public Key Services,CN=Services,<configDN> for base.
   -fsps         Use Foreign Security Principals container for base.
   -sitelinks    Use Site Links Container for base.
   -legacydns    Use Legacy DNS Container for base.
   -displayspecifiers User Display Specifiers container in config for base.
   -ds           Use Directory Service container in config for base.
   -svcs         Use Services container in config for base.
   -fgpp         Use Password Settings Container for base.
   -msa          Use Managed Service Accounts Container for base.
   -roles        Use Roles relative base (for ADLDS).
   -delobjs      Use Deleted Objects relative base from whatever base defined plus -showdel.
   -do           Alias for -delobjs.
   -delobjs+     Use Deleted Objects relative base from whatever base defined plus -showdel+.
   -do+          Alias for -delobjs+.
   -sort key     Server side sort by key (Note: Sorts can time out easily).
   -sorta key    Same as -sort key but also adds key attribute to output.
   -rsort key    Reverse server side sort by key.
   -rsorta key   Same as -rssort key but also adds key attribute to output.
   --------------Expert--------------
   -stdinsort xx Sorts DN's that have been piped in in multi-DN mode, the
                 default sort is hierarchical, but can specify case-sensitive
                 alphabetic sort with csalpha or case-insensitive with cialpha
   -srvctls xx   Inserts arbitrary server controls. Delimiter is ;
   -showdel      Inserts show deleted objects server control into query.
   -showdel+     Inserts show deleted objects, links, and recycled objects control.
   -showdelobjlinks Inserts show deactivated links server control.
   -showrecycled Inserts show recycled objects server control.
   -pr           Phantom Root, search all NCs that are subordinate
                 to the search base - special. Used primarily with
                 ADAM or if need to search Schema, Config, etc
   -prb          -pr combined with -null, Phantom Root from root of directory.
   -asq xx       Attribute Scoped Query focused on attribute xx
   -bit          Special filter conversion enable
                    :AND:= converts to :1.2.840.113556.1.4.803:=
                    :OR:= converts to :1.2.840.113556.1.4.804:=
                    :INCHAIN:= converts to :1.2.840.113556.1.4.1941:=
                    :NEST:= converts to :1.2.840.113556.1.4.1941:=
                    :DNWDATA:= converts to :1.2.840.113556.1.4.2253:=
   -binenc       Transform filter elements to proper format:
                    {{GUID:guid value}} converts to LDAP format of binary.
                    {{SID:sid value}} converts to LDAP format of binary.
                    {{BIN:hex string}} converts to LDAP format of hex binary.
                    {{BASE64:Base 64 string}} converts to LDAP format of BASE64.
                    {{UTC:YYYY/MM/DD-HH:MM:SS}} converts to int8 of UTC date/time.
                    {{UTCGT:YYYY/MM/DD-HH:MM:SS}} converts to Generalized Time of UTC date/time.
                    {{LOCAL:YYYY/MM/DD-HH:MM:SS}} converts to int8 of Local date/time.
                    {{LOCALGT:YYYY/MM/DD-HH:MM:SS}} converts to Generalized Time of Local date/time.
                    {{LOCALGTIPA:YYYY/MM/DD-HH:MM:SS}} is similar to LOCALGT but uses "Z" instead of ".0Z".
                    {{CURRENT:xx}} converts to int8 of Current date/time as modified
                       by xx. Two formats are allowed, dd:mm:hh:ss where dd is an
                       integer value for days, mm for minutes, hh for hours, and ss
                       for seconds and each value can be prefixed with the
                       minus(-) sign. The second format is (-)nnz where nn
                        is an integer value and z is d, m, h, or s.
                    {{CURRENTGT:xx}} is similar to CURRENT but generalized time format.
                    {{CURRENTGTIPA:xx}} is similar to CURRENTGT but uses "Z" instead of ".0Z".
   -nr           Do not follow referrals - client side.
   -nrss         Tells AD not to generate continuation referrals.
   -ff filenm    Pulls query filter from file named filenm.
   -noautoranging  Disables autoranging feature so you can request specific
                   ranges of multivalue attributes.
   -fdnx         Filter DN Expansion. Allows use of some normalized strings that
                 are expanded on the fly when submitted to the LDAP Server.
                    [ROOT]      - Expand to Forest Root Domain DN
                    [CONFIG]    - Expand to Configuration NC DN
                    [SCHEMA]    - Expand to Schema NC DN
                    [DEFAULT]   - Expand to Default NC DN
                    [DOMAINDNS] - Expand to Domain DNS (default domain) NC DN
                    [FORESTDNS] - Expand to Forest DNS NC DN

           [OUTPUT OPTIONS]
   -c            Object count only
   -c2           Object count only but allow object filtering with -incldn/-excldn
   -dn           Object DN's only
   -appver       Output AdFind versioning info.
   --------------Advanced--------------
   -dpdn         Display Parent DN
   -pdn          Display Parent DN only
   -pdnq         Display Parent DN only in -dsq format (quoted DN)
   -pdnu         Display unique Parent DNs only
   -pdnuq        Display unique Parent DNs only in -dsq format (quoted DN)
   -pdnucounts xx [BETA] Displays unique Parent DNs and then counts of objects in each container.
                             if xx is specified, it is a filename to write CSV output version.
   -dpcanonical  Display Parent Canonical Value - can also use attribute parentCanonical.
   -objectdomaindn  Display object's domain's DN - can also use attribute objectDomainDN.
   -objectdomaindns Display object's domain's DNS - can also use attribute objectDomainDNS.
   -nodn         Do not output DN
   -stripdn      Strip DN's down to only RDN value
   -nolabel      Don't display attribute labels.
   -noctl        Filter control chars out of attrib value output.
   -exclrepl     Exclude display of certain replication related attributes.
                   dSASignature, masteredBy, msDS-IsFullReplicaFor
                   msDs-masteredBy, repsFrom, repsTo, replUpToDateVector
   -nonoise      Alias for -exclrepl
   -excl xx      Exclude display of certain attribs.
                    xx List must be semi-colon delimited
                    -excl "objectclass;memberof;name"
   -excldn xx    Exclude objects with given string in DN. Multiple
                 strings delimited by semi-colon (;). Cannot be 
                 combined with the -c option. xx can be a regex.
   -excldndelim  Specify a delimiter for -excldn, default is (;).
   -incldn xx    Output only objects with given string in DN. Multiple
                 strings delimted by semi-colon (;). Cannot be 
                 combined with -c option. xx can be a regex.
   -incldndelim  Specify a delimiter for -incldn, default is (;).
   -incllike xx  Only display attributes that match xx. Delimited by semicolon (;).
   -excllike xx  Only display attributes that do not match xx.
   -dsq          DSQuery style quoted DN output
   -dsnq         Non-quoted DNs only output (-dsq without the quotes)
   -tdc          Decode common 64 bit (int8) time fields (pwdLastSet, etc)
   -tdcs         Decode common 64 bit (int8) time fields string sortable format (pwdLastSet, etc)
   -tdcgt        Decode Generalized Time fields (whenChanged, etc)
   -tdcgts       Decode Generalized Time fields string sortable format (whenChanged, etc)
   -tdcd         Decode time with delta. Int8 only.
   -tdcda        Decode time with delta. Int8 and Generalized Time.
   -tdcdshort    Decode time with delta. Short output format.
   -tdca         Combined -tdc and -tdcgt
   -tdcas        Combined -tdcs and -tdcgts
   -utc          Use with tdc*, decodes to UTC instead of localtime.
   -tdctzstr     Set your own TimeZone String, e.g. EDT instead of Eastern Daylight Time.
   -tdcfmt xxx   Define format for -tdc/-tdcgt/-tdca/tdcd.
   -tdcsfmt xxx  Define format for -tdcs/-tdcgts/-tdcas/tdcd.
                 NOTE: The TDC format strings allow you to change the output
                 format of the various -tdc* switches. Pass a string into the
                 the switch defining the required format. Special format modifiers:
                     %MM%    - 2 digit month
                     %DD%    - 2 digit day
                     %YYYY%  - 4 digit year
                     %HH%    - 2 digit hour (24 hour format)
                     %mm%    - 2 digit minute
                     %ss%    - 2 digit second
                     %ms%    - 2 digit millisecond
                     %TZ%    - Time Zone value
                     %INT8%  - Raw Integer8 time format
                     %%      - Percent symbol
                 Default format for -tdc is %MM%/%DD%/%YYYY%-%HH%:%mm%:%ss% %TZ%
                 Default format for -tdcs is %YYYY%/%MM%/%DD%-%HH%:%mm%:%ss% %TZ%
   -int8time xx  Add attribute(s) to list for decoding as int8. Semicolon delimited.
   -int8time- xx Remove attribute(s) from list to be decoded as int8. Semicolon delimited.
                 INT8 Notes:
                 ===========
                   AdFind has many attributes that are pre-defined as time and
                   duration attributes that will be decoded by the -tdc* switches.
                   In addition, AdFind will search the schema looking for all 2.5.5.16
                   attributes and anything with the string 'time' in the lDAPDisplayName
                   or adminDescription will be added to the list of attributes to
                   to be decoded as time attributes. Anything with either 'duration'
                   or 'interval' will be decoded as interval attributes.

   -samdc        Decode SAM Type attributes:
                   forceLogoff, groupType, lockoutDuration, lockoutObservationWindow,
                   machinePasswordChangeInterval, maxPwdAge, maxRenewAge, maxTicketAge,
                   minPwdAge, minTicketAge, msDS-IsUserCachableAtRODC, msDS-LockoutDuration,
                   msDS-LockoutObservationWindow, msDS-MaximumPasswordAge,
                   msDS-MinimumPasswordAge, msDS-SupportedEncryptionTypes,
                   msDS-User-Account-Control-Computed, nTMixedDomain, pekKeyChangeInterval,
                   proxyLifetime, pwdProperties, sAMAccountType, trustAttributes,
                   trustDirection, trustType, userAccountControl
   -flagdc       Decode various flag type attributes:
                   dSHeuristics, instanceType, msDS-Behavior-Version,
                   mS-DS-ReplicatesNCReason, options, packageFlags, schemaFlagsEx
                   searchFlags, systemFlags, validAccesses, msDS-RevealedUsers.
   -schdc        Decode attributeSyntax, objectClassCategory, and objectVersion and also
                 enables -flagdc switch.
   -sitenamedc   Decode site name GUIDs to site names.
   -alldc        Enable all decode options EXCEPT -sddc/-sddl.
   -alldc+       Enable all decode options including -sddc/-sddl.
   -alldcd       -alldc combined with -tdcda.
   -elapsed      Display elapsed time in seconds that the search occupied.
   -selapsed     Display elapsed time in seconds for various points of execution.
   -elapsedms    Display elapsed time in milliseconds that the search occupied.
   -selapsedms   Display elapsed time in milliseconds for various points of execution.
   -list         List style output, no DNs, no labels.
   -qlist        Quoted list, like -list but with quotes.
   -sl           Sorted List, shortcut for -sort -list
   -progress     Display Progress Bar for multi-DN operations in the title bar.
   -cv           Count values, requires -csv mode
   -cva xx       Count values for specified attributes only. Delimited by semicolons (;).
   -hint         Outputs "hint" parameter information for AdFind/AdMod, specifically:
                    -h switch   -p switch   -u switch   -up switch   -simple switch
                    -hh switch   -url switch
   -jtsv         Combines -csv -csvdelim \t -csvmvdelim |
   -jtsv2        Combines -jtsv -csvnoheader -csvnoq
   -fl           Combines -jtsv2 and -list.
   -jcsv2        Combines -csv -csvnoheader -csvnoq
   -csv xxx      CSV output, xxx is an optional string that specifies value to
                 use for empty attribs.
   -gcsv         Generic CSV mode. Combines -csv, -replacedn _all
   -adcsv xxx    Special CSV mode for interacting with other joeware tools.
                 xxx is an optional string that specifies value to use for
                 use for empty attribs.
   -csvdelim x   Delimiter to use for separating attributes in CSV output,
                 default (,).
   -csvmvdelim x Delimiter to use for separating multiple values in output,
                 default (;).
                 NOTE: The -csvdelim and -csvmvdelim switches allow you to
                 specify control characters such as tab via standard c\c++ printf
                 character sequences. For example tab is \t. There is no
                 filtering in place to validate that intelligent characters are
                 selected so if you choose \n you own the problem. :)
   -csvq x       Character to use for quoting attributes, default (").
   -csvnoq       Set Quote character to null - i.e. no quote character.
   -nocsvq       Alias for -csvnoq.
   -csvqesc      CSV Quote escape character. default (\)
   -nocsvheader  Don't output attribute header.
   -csvnoheader  Alias for -nocsvheader.
   -csvsh x      CSV Smart Header. When redirecting to a file (x) a header will
                 be written if file x doesn't exist or has a zero length. This is
                 useful especially for CMD FOR /F or PoSh foreach().
   -csvconnerr   Insert Host Connection Error in CSV output file.
   -csvxl        Excel CSV mode, sets quote escape character to " and changes
                 " in DNs to "" which makes the output incompatible with
                 any CSV type tools that modify AD such as AdMod.
   -csvfinalcount  Display number of rows at the end of the output. ObjCount=xxx.
                 CSV Notes:
                 ==========
                  o The CSV mode requires you to specify the attributes you want
                    returned. 
                  o To specify a static column specify an argument of the form
                    of header:value

   -attrprefix x    Prefix character for attribute output, default is greater than (>).
   -attrvaldelim x  Delimiter character between attribute and value, default is colon (:).
   -xmod         Used -attrprefix/-attrvaldelim to output object similar to AdMod input format.
   -soao         Sort order attrib output, sorts attrib names for each record.
   -oao xxx      Order attrib output, orders attrib output by specified order.
                 xxx allows you to specify NULL value for specified attributes.
   -noerr        Do not write errors to stderr/stdout when output is redirected.
   -pause        Forces AdFind not to exit until <ENTER> is pressed when prompted.
   -gplinkmulti  Output GPO DNs in gPLink attribute as a multi-valued attribute.
   --------------Expert--------------
   -ic           Intermediate count (for multi-dn mode).
   -ictsv        Intermediate count TSV output (for multi-dn mode).
   -db           Display base DN (for multi-dn mode).
   -objcnterrlevel  Object count only, send to command prompt ERRORLEVEL variable.
   -resolvesids  Resolve SIDs to names
   -resolvesidsgeneric xxx Resolve SIDs but transform domain names to xxx. Default xxx = [DOMAIN]
                              NOTE: All domains will have the same xxx value.
   -resolvesidsgenex Resolve SIDs but transform root domain name to {{*rootdns*}} and ALL
                     other domains in forest to {{*domaindns*}}
   -resolvesidsldap  Uses LDAP to resolve SIDs to DNs. This is done automatically
                     when connecting to ADAM for ADAM SecPrins.
   -sidtype      Output SID types - USER, GROUP, WELLKNOWN, BI-GROUP, etc
   -rawsddl      Show rawsddl.
   -rawsddlnl    Does not include [SDDL] label prefix on -rawsddl output.
   -rawsddlexpl  Show rawsddl explicit ACEs only.
   -sddc / -sddl      Partial decode of security descriptors
   -sddc+ / -sddl+    Better partial decode of security descriptors
   -sddc++ / -sddl++  Even better decode of security descriptors
   -sddc+++ / -sddl+++ Combines -sddl++ with -resolvesids
   -sddc3 / -sddl3    Alias for -sddl+++
   -sdpipe       Output explicit ACEs of security descriptor in -adcsv format.
   -sdpipe+      Adds -resolvesidsgeneric to -sdpipe.
   -sdpipe+x     Adds -resolvesidsgenex to -sdpipe.
   -daclpipe     Output explicit ACEs of DACL only in -adcsv format.
   -daclpipe+    Adds -resolvesidsgeneric to -daclpipe.
   -daclpipe+x   Adds -resolvesidsgenex to -daclpipe.
   -sdna         SD info Non-Admin. Allows non-admins to get some SD Info (same as -nosacl)
   -sddlpsflag   Mark property sets in SDDL output
   -sdcsvsingle xx Special CSV output of Security Descriptor with one ACE per line broken out.
                       Note: xx is optional string values that can be combined:
                               d - Use defaultSecurityDescriptor instead of nTSecurityDescriptor
                               e - Explicit ACEs only
                               f - Full mode, enable -sddl++, -csv, and -resolvesids.
                               g - Generic secprins, replace domain with [DOMAIN].
                               r - Insert -replacedn _all to genericize the DN.
                               x - Like g but with -resolvesidsgenex versus -resolvesidsgeneric
   -sdcsvsinglesort xx Same as -sdcsvsingle but with sorted output. Same values for xx.
   -acecount     Numbers each ACE on the ACE output line in the -sddl+ and higher output.
   -sidbinout xx SID binary pack as unicode string output (unfriendly format)
   -guidbinout xx GUID binary pack as unicode string output (unfriendly format)
                   Note: For -sidbinout, -guidbinout you have the option to
                         to specify format type via xx parameter:
                           HEX for Hex output
                           BASE64 for Base64 output
   -binsize x    Output binary attribute size. x defines units, default
                 is bytes, use KB, or MB for KiloBytes or MegaBytes.
   -binsizenl    Do not put string label on end of BinSize output.
   -extname      Shows Extended Name format DNs, i.e. GUID/SID info
   -exterr       Show Extended Error info. DSID Info...
   -norrerr      Do not throw errors if invalid range is specified on attribute.
   -owner        Display Owner - will show as attrib _OBJECT_OWNER
   -owneronly    Display DN and Owner only
   -ownercsv     Display DN and Owner only, Semicolon delimited output
   -ameta xx     Display Attribute Replication MetaData (msDS-ReplAttributeMetaData)
                   xx can be a semicolon delimited list of specific attributes.
   -ametal xx    -ameta combined with -list
   -ametanl xx   -ameta combined with -nolabel
   -vmeta xx     Display Linked Value Replication MetaData (msDS-ReplValueMetaData)
                 Note: The value for xx in -ameta/-vmeta can be a -metafilter string.
   -vmetal xx    -vmeta combined with -list
   -vmetanl xx   -vmeta combined with -nolabel
   -vmetaplus    Combined with -vmeta switches to display additional meta info.
   -vmeta+       Alias for -vmetaplus.
   -metas xx     Both attribute and value metadata.
   -metasnl xx   -metas but with no label.
   -metasl xx    -metas but in list format.
   -metamvcsv       Output metadata in MV CSV type format
   -metamvcsva xx   Specify properties list to output for attribute metadata (delimiter: ;)
                      Field Names: attribute datetime dsa usnlocal usnorig version
   -metamvcsvv xx   Specify properties list to output for value metadata (delimiter: ;)
                      Field Names: attribute datetime dn dsa state usnlocal usnorig version initialaddtime removetime
   -dloid        Don't load OID's for GUID/SID decode
   -ddo          Display Dynamic Object attributes if present.
   -showttll     Display Link TTL values.
   -mvfilter xx       Multivalue filter. (Also works on single value attributes)
   -mvnotfilter xx    Multivalue NOT filter. (Also works on single value attributes)
   -mvfiltercs        Make filter case sensitive.
   -mvfilterdelim xx  Delimiter between multiple filter definitions. Default (;)
                 Multivalue Filter Notes:
                 ========================
                   Filters are specified in the format:
                        attribute1=filter;attribute2=filter,etc
                   Alternate filter format is:
                        attribute1=filter1;filter2;filterN;attribute2=filter1
                   The default semi-colon delimiter can be modified with the
                   -mvdelimiter switch. These are simple exists or not exists
                   filters, the values are scanned for the string and if there
                   is a match, the value is displayed or not based on whether
                   it is a NOT filter or show filter. If a semicolon is part of a
                   returned attribute name, the match will be made on the attribute
                   name itself so extensions like ;binary or ;range= will not be
                   part of the matching. Do not use * or ? in the filter as a
                   wildcard because it will not be used as a wildcard.
                   Ex: -mvfilter proxyaddresses=smtp;proxyaddresses=sip;mail=@domain.com
                   Ex: -mvfilter proxyaddresses=smtp;sip;mail=@domain.com
   -mvsort xx    Sort the values in a multivalue attribute. Default *.
   -mvrsort xx   Sort the values in a multivalue attribute in reverse. Default *.
                   Notes: -mvsort and -mvrsort specify the multivalue attribute(s)
                          to sort via semicolon delimited list. To make the sort
                          case insensitive for an attribute append :ci onto the
                          the attribute name. To select all MV attribs specify *.
   -metasort xx  See adfind /meta?
   -sddlfilter xx    SDDL filter, use with -sddl++
   -sddlnotfilter xx SDDL NOT filter, use with -sddl++
                 SDDL Filter Notes:
                 ==================
                   Filters are specified in the format:
                     acetype;aceflags;rights;objectguid;inheritobjectguid;account
                   If you want to specify an empty value for one of the fields use
                   the tilde (~) for the field value to do so. You do not have to
                   specify values for all fields. An empty field indicates to match
                   on anything. You can only specify a single filter and a single
                   NOT filter.
                   NOTE: Previously the dash (-) was the empty value character.
                   Ex1: -sddlfilter ;inherited
                           Only display inherited ACEs
                   Ex2: -sddlnotfilter ;inherited
                           Only display non-inherited ACEs
                   Ex3: -sddlfilter allow;;;;;joe
                           Display allow ACEs for account with joe in the value
                   Ex4: -sddlfilter allow;;;;;administrators
                           Display all ACEs except allow ACEs for administrators
   -recmute      Suppress display of DN if all attributes are empty. This is
                 primarily in place for the -sddlfilter options.
   -recmutedsq   -recmute functionality but only output quoted DNs of objects with values.
   -noowner      Do not retrieve owner info for Security Descriptors
   -nogroup      Do not retrieve group info for Security Descriptors
   -nodacl       Do not retrieve DACL info for Security Descriptors
   -nosacl       Do not retrieve SACL info for Security Descriptors
   -onlydacl     Only retrieve DACL info for Security Descriptors
   -onlysacl     Only retrieve SACL info for Security Descriptors
   -onlydaclflag Only retrieve DACL and display DACL flag
   -onlysaclflag Only retrieve SACL and display SACL flag
   -onlyaclflags Only retrieve DACL/SACL and display ACL flags
   -onlyaclprot  Only display protected ACLs (i.e. ACLs that do not inherit).
   -onlyaclunprot  Only display unprotected ACLs (i.e. ACLs that inherit).
   -sdsize x     Output Security Descriptor Size. x defines units, default
                 is bytes, use KB, or MB for KiloBytes or MegaBytes.
   -sdsizenl     Do not put string label on end of SDSize output.
   -sdblob       Display the Security Descriptor as a HEX BLOB.
   -sdbinout     Alias for -sdblob
   -dplsids      Use older method for resolving SIDs for SDDLs (generally slower).
   -jsd xxx      SD Decode shortcut - adds ntsecuritydescriptor -sddl++, resolvesids.
   -jsdnl xxx    Same as -jsd but add -nolabel
   -jsdnlb xxx   Same as -jsdnl but add -s base
   -jsde xxx     SD Decode shortcut explicits - adds ntsecuritydescriptor -sddl++, resolvesids.
   -jsdenl xxx   Same as -jsde but add -nolabel
   -jsdenlb xxx  Same as -jsdenl but add -s base
                 JSD NOTES:
                 ==========
                 The -jsd* switches take an optional parameter specifying filters
                 using a format of <sddlfilter>:<sddlnotfilter> or regex.
                 The optional filters are parsed off and passed to the sddlfilter or
                 sddlnotfilter switches so use the usage info for those switches as
                 a guide for that format. You can use blah or blah:blah2 or :blah.
                 For regex you can use m/regex/options or !m/regex/options.
   -metafilter xxx      Filter metadata output. (both attributes)
   -metafilterattr xxx  Filter metadata output. (msDS-ReplAttributeMetaData)
   -metafilterval xxx   Filter metadata output. (msDS-ReplValueMetaData)
                 METADATA FILTER NOTES:
                 ======================
                 When using the -sc objsmeta shortcut or when specifying that
                 AdFind should return the binary versions of the metadata
                 attributes msDS-ReplAttributeMetaData;binary and
                 msDS-ReplValueMetaData;binary you can configure some specific
                 filtering on fields of the metadata. You can specify several
                 filters by separating them with a semi-colon (;). If you specify
                 several filters of the same type, i.e. two or more version filters
                 they are OR'ed together. If you specify several filters of different
                 types they are AND'ed together. The available fields are:
                    attribute [both] -  specify LDAP attribute name.
                        ex: -metafilterattr cn;description
                    time [both] - specify time=(wildcard time value)
                        ex: -metafilterattr time=2010/03/29
                    site [both] - specify site=(site name)
                        ex: -metafilterattr site=MySite
                    server [both] - specify server=(server name | nodeleted)
                        ex: -metafilterattr server=MyServer
                        ex: -metafilterattr server=nodeleted
                    originating USN [both] - specify usnorig=(USN)
                        ex: -metafilterattr usnorig=12345
                    local USN [both] - specify usnloc=(USN)
                        ex: -metafilterattr usnloc=12345
                    version [both] - specify ver=(version)
                        ex: -metafilterattr ver=19771107
                    state [ReplVal] - specify state=(state)
                        ex: -metafilterval state=(+)
                    link value [ReplVal] - specify link=(link value)
                        ex: -metafilterval link=cn=administrators
   -nirs           Not in Result Set option. Enables sorted order output and
                   requests the constructed attribute 'allowedAttributes' and
                   determines what attributes that could be populated for an
                   object that AREN'T populated for the object and populates those
                   attribute's value with <NOT IN RETURN SET>. The attributes
                   'allowedAttributes' and 'allowedAttributesEffective' will
                   both show as <INTENTIONALLY MUTED> for ease of reading the
                   output. Cannot be used with -CSV. Use with -list to just list
                   all possibly attributes of an object.
   -nirsx          Similar to -nirs but uses 'allowedAttributeEffective' which
                   "sort of" returns attributes that AD defines as writeable for the
                   current user. In reality not all of the attributes may truly be writeable.
                   Use with -list to just list the effective writeable attributes.
   -nirsonly       Used with -nirs/-nirsx and ONLY shows attributes with no values.
   -subset x       Output only a subset of the returned results. By default output
                   will contain every 10 objects, specify X for alternate value.
   -objfilefolder x [BETA] Output returned objects in individual files in top level folder
                   specified by x. Each file is written under the top level folder
                   by the most specific class specified by the objects
                   structuralObjectCategory values. The file names will be based
                   on the objectGUID.
   -exportfile x=y  Export binary of attribute y to file x. Semicolon delimited.
                    Think of it as file x = attribute y info. Can also just
                    specify the attribute name and it will use the RDN of the object
                    appended with .bin (or .jpg for attributes with photo in the
                    name) for the file name. If the attribute is multivalued _x
                    will be appended where x will be a consecutive number.
                    If there is a filename collision _x will also be appended
                    to the filename. So a collision on a multivalued attribute
                    could end up with a name like jpegPhoto.jpg_1_0. You can also
                    specify {rdn} in the specified file name and {rdn} will be
                    replaced with the actual RDN string such as Export_{rdn}.file.

           [AUTHENTICATION OPTIONS]
   --------------Advanced--------------
   -u userdn     Userid authentication. AD simple bind supports All ID
                 formats and secure bind only supports ID formats 1 and 2.
                 No userid specified indicates anonymous authentication.
                     ID Formats
                     1. domain\userid
                     2. user@domain.com (userPrincipalName)
                     3. cn=user,ou=someou,dc=domain,dc=com (DN)
   -up pwd       Password for specified userid. * indicates to ask for password.
                 Password can be clear text password or ENCPWD:xxx format as
                 created by -encpwd switch
   -simple       Simple Bind
   -digest       Digest Authentication (LDAP_AUTH_DIGEST)
                    Notes: ADLDS - Can be used with DN and UPN
                           AD    - Can be used with flatdomainname\samname,
                                       dnsdomainname\samname, and UPN
                           If SAMNAME/UPN is changed password needs to be changed
                              as DIGEST hashes are calculated at password change.
                           Alternately account can be set with reversible encryption.
   -ntlm         NTLM Authentication (LDAP_AUTH_NTLM)

           [MISC OPTIONS]
   --------------Expert--------------
   -po           Print options. This switch will dump to the command line
                 all switches with values and attributes specified.
   -allowdupeargs Disables argument filtering such that you could specify the
                  same argument (attribute) multiple times for CSV output.
   -decint xx    Decode int8 interval value.
   -decutc xx    Decode int8 value to UTC time string.
   -declocal xx  Decode int8 value to local time string.
   -encutc xx    Encode UTC time to int8. Format: YYYY/MM/DD-HH:MM:SS
   -enclocal xx  Encode local time to int8. Format: YYYY/MM/DD-HH:MM:SS
   -enccurrent xx Encode current time to int8.
                   xx is required to be a string of one of two formats
                   Format 1: dd:hh:mm:ss
                      where dd is days, hh is hours, mm is minutes, ss is secs
                      each value can be prefixed with a minus (-) symbol.
                      Ex: 00:-20:-30:00 for -20 hours and 30 minutes.
                   Format 2: (-)nnZ
                      where nn is an integer and Z is d, h, m, or s.
                      Ex: -20h for -20 hours.
                   The strings are a modifier from the current time. If you
                   want the current time in int8, specify 0d for the string.
   -decdelta xx  Decode delta time value.
   -encpwd xx    Encodes password xx for -up switch. Not required, use to assist
                 with some additional security.
   -encguidtoiid xx Encodes GUID to IID (BASE64 GUID)
   -deciidtoguid xx Decodes IID (BASE64 GUID) to GUID
   -encguidtohex xx Encoded GUID to Hex String
   -dechextoguid xx Decodes Hex String to GUID
   -encsidtohex xx  Encoded SID to Hex String
   -dechextosid xx  Decodes Hex String to SID
   -nopagingcheck Disable LDAP paging OID existence check on startup.
   -decsddlacl x Decodes ACL x specified in SDDL format. Use -h to specify
                 machine to use for resolving SIDs to names.
   -filterbreakdown xx  Breaks down LDAP filter specified in xx into a more
                        readable format. Can specify filter as param or with -f.
   -expandfilter xx     Alias for -filterbreakdown.
   -dnbreakout xx:yy  Break DN xx into various components. Valid values for yy:
       CANONICAL_NAME        - lockout.test.loc/System/Policies
       DN                    - CN=Policies,CN=System,DC=lockout,DC=test,DC=loc
       DOMAIN                - DC=lockout,DC=test,DC=loc
       EXPLODED_DN           - CN=Policies;CN=System;DC=lockout;DC=test;DC=loc
       GRANDPARENT           - DC=lockout,DC=test,DC=loc
       NAME                  - Policies
       NDC                   - CN=Policies,CN=System
       PARENT                - CN=System,DC=lockout,DC=test,DC=loc
       PARENTRDN             - CN=System
       PARENT_CANONICAL_NAME - lockout.test.loc/System
       RDN                   - CN=Policies
   -rootdse      Returns and decodes RootDSE + some non-default attribs.
                    Attributes Decoded:
                      * domainControllerFunctionality
                      * domainFunctionality
                      * forestFunctionality
                      * supportedCapabilities
                      * supportedControl
                      * supportedExtension
   -rootdseanon  Like RootDSE but anonymous.
   -fullrootdse xxx Returns and decodes RootDSE + all non-default attribs.  If
                    xxx is specified as the string "bin" the ;binary option
                    will be appended to the appropriate attributes and cause
                    their decode via AdFind versus getting XML versions.
   -adminrootdse xxx Returns and decodes RootDSE + all non-default attribs including admin.
                     Like with -fullrootdse "bin" can be used for ;binary.
   -rootdseinternals Display even more rootdse information, requires admin to see everything.
   -extsrvinfo   Give additional server info for bind string info.
   -domainlist xx  Shortcut -sc domainlist promoted to normal switch, see shortcut help for info.
   -domainncsl xx  Shortcut -sc domainncsl promoted to normal switch, see shortcut help for info.
   -dclist xx      Shortcut -sc dclist promoted to normal switch, see shortcut help for info.
   -fsmo xx        Shorcut -sc fsmo promoted to normal switch, see shortcut help for info.
   -replacedn xxx:yyy  Replaces xxx in DNs with yyy. Following special cases:
                     ""         alias for _all
                     _all         replaces all of the following:
                     _config      Configuration DN replaced with <CONFIG>
                     _schema      Schema DN replaced with <SCHEMA>
                     _default     Default NC DN replaced with <DEFAULTNC>
                     _root        Root NC DN replaced with <ROOT>
                     _sites       Sites DN replaced with <SITES>
                     _subnets     Subnets DN replaced with <SUBNETS>
                     _system      System DN replaced with <SYSTEM>
                     _exch        Exchange services DN replaced with <EXCH>
                     _dcs         Domain Controllers DN replaced with <DCS>
                     _fsps        ForeignSecurityPrincipal DN replaced with <FSPS>
                     _msa         Managed Service Accounts DN replaced with <MSA>
                     _psc         Password Settings Container DN replaced with <PSA>
                     _gpo         Group Policy Container DN replaced with <GPO>
                     _services    Services DN in Config NC replaced with <SERVICES>
                     Not specifying a value is alias for _all
   -replacedndelim x   Specifies delimiter to separate replacedn strings
   -sslinfo      Doesn't return any data other than SSL Certificate and Connection info
   -e xxx        Load switches from environment. Will read env vars with prefix
                 and dash (adfind-) by default and load them in. To
                 specify a different prefix, specify string after -e. For
                 example to specify the host switch create an env var of 
                 adfind-h. To specify properties specify the env var adfind-
                 or adfind-props. To specify a switch that doesn't take a
                 a value, specify a value of {~} because you can't set a
                 an environment variable to blank. By default, AdFind will read any
                 environment variables prefixed with (joeware-default-adfind-)
                 without specifying -e.
                    Ex: Queries ADAM on localhost port 5000 for subnets.
                       set adam1-h=.:5000
                       set adam1-config={~}
                       set adam1-f=objectcategory=subnet
                       set adam1-props=name siteobject
                       set adam1-u=thispc\myid
                       set adam1-up=ENCPWD:EhfEeD0ZVyV9O2AdWzoNyXzYrQwVJm9cN1
                       adfind -e adam1

   -ef xxx       Load switches from file (default file = adfind.cf), one 
                 switch per line. Properties can be placed on multiple lines
                    Ex: Queries ADAM on localhost port 5000 for subnets.
                       adam1.cf
                         -h .:5000
                         -config
                         -f objectcategory=subnet
                         name siteobject
                       adfind -ef adam1.cf

                 By default AdFind will process the default configuration
                 file 'joeware_default_adfind.cf' without specifying -ef.

      ENVIRONMENT NOTES
         There are five levels for specifying switches, a lower level will
         not override a higher level. The levels from highest to lowest:
            1. Command line switches
            2. Environment variable specified via -e
            3. Environment file specified via -ef
            4. Default environment variables prefixed with joeware-default-adfind-
            5. Default environment file joeware_default_adfind.cf


   -inputdn xx   Specifies DN for LDAP_SERVER_INPUT_DN_OID.
   -ldapping xx  Special LDAP "ping" functionality. xx has one optional value:
                    !closest when you don't want next closest site.
   -netlogonexdc Modifies output format for LDAP Ping to alternate format.
   -ldappingex xx  -ldapping + -netlogonexdc.
   -dncharvalidation [BETA] Bounce DNs with non-US ASCII Characters (c & 0x80 > 0)
   -dirsync xx   Enable DirSync query. xx is prior DirSync Cookie or Cookie File.
                 If nothing is specified, it will look for a default file that is
                 named .\adfind_x.y_cookie.dirsync where x.y is the NC being
                 queried converted from DC=blah,DC=blah to blah.blah format. 
                 If the default file is empty or non-existent it will create it.
                 To specify a specific filename, use the format FILE:filename.
                 To specify a cookie, just specify the cookie string.
                 Specify filter with -f as normal to filter what is returned.
   -dirsyncro xx Identical to -dirsync but will not update the cookie file.
   -dirsync_opts xx  Options for DirSync. Values for xx:
                           OS  - Object Security Mode (Should work without high level access)
                           AFO - Ancestors First Order (Helps with chicken/egg issues)
                           IV  - Incremental Values (useful for large groups)
   -dirsync_maxbytes xx  Maximum number of bytes for return sets, minimum 100k, default 1MB
   -dirsync_cont xx  Continuous dirsync, sleep xx seconds between passes.

   Notes about DIRSYNC functionality
     The DirSync functionality is very different from normal LDAP queries, make no assumptions
     about the output formatting. TEST! Some additional switches that should generally be used
     with -dirsync are -extname and -showdel+ to turn on extended DN names and deleted objects.
     By default, nTSecurityDescriptor will be output as -rawSDDLExpl mode. You can override with
     -rawsddl if you need the inherited ACEs with the security descriptor.
     Please review the Microsoft LDAP DirSync documentation:
         https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/2213a7f2-0a36-483c-b2a4-8574d53aa1e3
         https://docs.microsoft.com/en-us/windows/win32/ad/polling-for-changes-using-the-dirsync-control

   -stats        Display STATS control info
   -stats+       Display STATS control info + some analysis.
   -statsonly    Display STATS control info - ONLY
   -stats+only   Display STATS control info + some analysis - ONLY
   -statsonlynodata  Display STATS control info, no data return
   -stats+onlynodata  Display STATS control info + some analysis, no data return
   -statsnofilter Don't output LDAP filter.

   Notes about STATS functionality
     All of the STATS options require user have DEBUG_PRIVILEGE
     on the domain controller queried.

     All switches except the two with nodata appended will return the query result
     set in the background but will not display it. The nodata switches work with
     with Windows Server 2003 and better and will tell AD not to return the data
     set but to instead just return what would happen if it did. 

     Hit rate is a function of data in the directory and the specific filter
     being used; it is not an absolute measure across directories.

     You could use a query of (&(objectcategory=person)(objectclass=user))
     in one directory and get a hit rate of 95% but then in another that has
     a bunch of contacts could get a hit rate of 40% or less.


     STATS against 2K AD is pretty boring, so don't bother as ADFIND
     will almost certainly say the data is worthless, and not display it.


  Notes:
    o AdFind was written with simple US ASCII in mind. UNICODE and special
      ASCII characters such as characters with umlaut's or graphics may not
      be output correctly due to how the command prompt handles those
      characters. If you see this occurring, redirect the output to a text file
      with the command prompt redirection symbols and it is possible the program
      will operate correctly. If not, you do not need to tell me, I know and I
      am working to correct it in some future version... no timeline.

    o AdFind will decode the following attributes whenever encountered:
        * any GUID attributes
        * generic binary decode to hex string
        * msDS-Cached-Membership
        * msDS-NCReplCursors
        * msDS-NCReplInboundNeighbors
        * msDS-NCReplOutboundNeighbors
        * msDS-ReplAllInboundNeighbors
        * msDS-ReplAllOutboundNeighbors
        * msDS-ReplAttributeMetaData
        * msDS-ReplConnectionFailures
        * msDS-ReplLinkFailures
        * msDS-ReplPendingOps
        * msDS-ReplQueueStatistics
        * msDS-ReplValueMetaData
        * msDS-RetiredReplNCSignatures
        * msDS-Site-Affinity
        * msDS-TopQuotaUsage
        * msPKIRoamingTimeStamp
        * retiredReplDSASignatures

    o In V01.40.00 AdFind gained the ability to take in a stream of DNs through
      the STDIN pipe - one DN per line. In this mode, the default search scope
      of AdFind changes from SUBTREE to BASE.



  Ex1:
    adfind -b dc=joehome,dc=net -f "objectcategory=computer"
      Find all computer objects in joehome.net and displays all attributes

  Ex2:
    adfind -b dc=joehome,dc=net -f "objectcategory=computer" cn createTimeStamp
      Find all computer objects in joehome.net and displays cn and createTimeStamp

  Ex3:
    adfind -h .:50000 -b cn=ab -f "objectcategory=person"
      Find all person objects on cn=ab container of local ADAM instance

  Ex4:
    adfind -schema  -f "objectcategory=attributeschema" ldapdisplayname -list
      List ldapdisplaynames of all attributes defined in schema.

  Ex5:
    adfind -gc -u domain\user -up passwd -b  -f name=joe
      Search GC with userid domain\user and password passwd for objects with name=joe

  Ex6:
    adfind -default -rb cn=users -f "&(objectcategory=person)(samaccountname=*)"
      Show all users in the default domain's cn=users container.

  Ex7:
    adfind -default -showdel -f isdeleted=TRUE
      Show deleted objects in default partitions deleted objects container

  Ex8:
    adfind -default -f "&(name=bob*)(instancetype=4)" -stats+only
      Show STATS result from specified query.
  Ex9:
    adfind -default -f name=administrators member -list | adfind samaccountname
      Dump administrators group membership and then retrieve sAMAccountNames.
  Ex10:
    adfind -encpwd MySecurePassword1!
      Encode password for use in -up switch.
  Ex11:
    adfind -rootdse -u dom\myuser -up ENCPWD:EhfEeD0ZV -simple
      Simple bind with specified credentials and return rootdse.
  Ex12:
    adfind -default -rb ou=MyUsers -objfilefolder c:\temp\ad_out
      Output all objects in MyUsers OU to specified folder structure.


 This software is Freeware. Use at your own risk.
 I do not warrant this software to be fit for any purpose or use and
 I do not guarantee that it will not damage or destroy your system.
 Contact support@joeware.net via email for licensing information to package
 this utility in commercial products.

 See full Warranty documentation or download the latest version
 on http://www.joeware.net.

 If you have improvement ideas, bugs, or just wish to say Hi, I
 receive email 24x7 and read it in a semi-regular timeframe.
 You can usually find me at support@joeware.net

adfind /sc?
AdFind V01.62.00cpp Joe Richards (support@joeware.net) October 2023

-help         Basic help.
-?            Basic help.
-??           Advanced/Expert help.
-????         Shortcut help.
-sc?          Shortcut help.
-meta?        Metadata help.
-regex?       Regular Expressions help.
-gui          Combine with help switch to open that output in text editor.

Usage:
 AdFind [switches] [-b basedn] [-f filter] [attr list]

   basedn        RFC 2253 DN to base search from.
                 If no base specified, defaults to default NC.
                 Base DN can also be specified as a SID, GUID, or IID.
   filter        RFC 2254 LDAP filter.
                 If no filter specified, defaults to objectclass=*.
   attr list     List of specific attributes to return, if nothing specified
                 returns 'default' attributes, aka * set.

  Switches: (designated by - or /)


   AdFind Shortcuts
   ================
   AdFind allows you to specify shortcuts. Shortcuts are not actual commands
   themselves but instead are shortcuts to other commands so you do not have
   to recall or type the longer commands. Anything one of the shortcuts does
   is actually a combination of various other switches. To see exactly what
   switches are specified on your behalf, use the -po switch in combination
   with the shortcut switch and it will show you everything that AdFind is
   processing.

   Since these shortcuts are simply a combination of switches auto-entered for
   you it means that generally you can use the other switches in AdFind to add
   to the query to focus it further or get output closer to what you need. In
   addition, most of the shortcuts support the added switch -af xxx, this
   allows you to 'add on' to the filter that is specified by the shortcut
   in case you want to make the filter more granular. Also if you want to change
   which attributes are returned, you can add additional attributes by specifying
   them in the normal manner. If you want to reset the list of attributes returned
   and specify your own, prefix one of the attributes with an underscore (_attr).
   If you want to remove one or more of the attributes from the list you can
   can specify the attribute with a trailing dash (attr-).

   If you have an issue with any of these shortcuts, remember you can just 
   enter the proper combination of real switches yourself. In general the 
   shortcuts will work on Windows 2000 AD, Windows Server 2003 AD, and ADAM.
   There are however some shortcuts that will not work on Windows 2000 AD
   and those have been noted and where possible I have added other shortcuts
   specific to Windows 2000 to try and get the same info. There are also some
   shortcuts that are specific to AD or ADAM. The name of the shortcut should
   help in the event that a switch is specific to ADAM or AD in most cases
   This isn't for all cases because there are shortcuts that don't work on
   Windows 2000 AD or Windows Server 2003 AD but expect to work in a future
   version of AD.

   When in doubt, just try the switches, AdFind is a query only tool, it can
   not harm your directory by writing data to it because it can't write.

   --------------Shortcuts--------------
   -af xxx                 Add filter to hardcoded filter in most shortcuts


   -sc policies            Display forest policy info.
   -sc dompol              Display Domain Policy, specify domain base or -default.

   -sc modes               Show DC, Domain, and Forest Mode info from RootDSE

   -sc forestmodes         Show modes from NC partition objects for forest
   -sc forestmodes:csv     Same as above but CSV output

   -sc dcmodes             Show modes of all DCs in forest from config
   -sc dcmodes:csv         Same as above but CSV output

   -sc masterncs           Show NCs mastered by all DCs in forest
   -sc masterncs:csv       Same as above but CSV output

   -sc domainncs           Show all domain partitions of forest
   -sc domainncs:csv       Same as above but CSV output
   -sc domainncsl          List domain partitions (DN Format) as list output
   -sc domainncsl:q        Same as above but quoted list output
   -sc domainncsl:noroot   List domain partitions (DN Format) EXCEPT the root domain as list output
   -sc domainncsl:root     List root domain partition (DN Format) as list output
        NOTE: There is now a switch for the domainncsl shortcut. -domainncsl
              Instead of specifying a colon between domainncsl and the extra params, separate by a space
   -sc domainlist          Dump all Domain NCs in forest in sorted DNS list format
   -sc domainlist:short    Dump all Domain NCs in forest in sorted SHORT hostname list format
   -sc domainlist:noroot   Dump all Domain NCs in forest EXCEPT the root domain in DNS list format
   -sc domainlist:root     Dump root Domain NC in forest in DNS list format
        NOTE: There is now a switch for the domainlist shortcut. -domainlist
              Instead of specifying a colon between domainlist and the extra params, separate by a space

   -sc ridpool             Dump Decoded Rid Pool Info

   -sc appparts            Show application partitions
   -sc appparts:csv        Same as above but CSV output
   -sc apppartsl           Same as above but list output
   -sc apppartsl:q         Same as above but quoted list output

   -sc appparts+           Show application partitions (extra info)
   -sc appparts+:csv       Same as above but CSV output

   -sc adsid:xx            Resolve Active Directory SID (xx) to object
   -sc adguid:xx           Resolve Active Directory GUID (xx) to object

   -sc whoami              Display authenticated user info and token
   -sc whoami:csv          Same as above but CSV output
   -sc adinfo              Active Directory Info with whoami info.

   ACL / SECURITY DESCRIPTOR / SECURITY SHORTCUTS
   **********************************************
   -sc sdfilter:xx         Display SDs for objects, if xx specified, filter for
                           that string using MVFILTERing.
   -sc sdfilterns:xx       Same as above but don't return SACL
   -sc explaces            Display explicit ACEs
   -sc aclnoinherit        Display protected ACLs (i.e. inheritance blocked)
   -sc getacl              Combines -resolvesids, -s base, -sddl++, -sdna
   -sc getacls             Combines -resolvesids, -s subtree, -sddl++, -sdna
   -sc dsd:xx              Retrieve defaultSecurityDescriptor for xx in -adcsv format.
   -sc cclone              Container Clone. ADCSV output for key container attributes.
   -sc cclone+             -sc cclone + -resolvesidsgeneric .
   -sc cclone+x            -sc cclone +  -resolvesidsgenx.
   -sc sdcsvdmp:xx         Dump CSVs in SD CSV Single mode with DNs and SIDs genericized.
                             Specify xx to specify domain replacement string.

   The next few commands use the following filter:
     Filter: (|(objectclass=domaindns)(ou=*)(o=*)
               (&(objectclass=container)(|(iscriticalsystemobject=TRUE)
                 (systemFlags=-1946157056))(!(objectclass=grouppolicycontainer))))

   -sc ccs                 Common container search, specifies filter above.
   -sc cexplaces:xx        Display explicit ACEs only for specific container type objects.
                           xx will be appended to -sddlfilter ;;;;;<xx>
   -sc caclnoinherit       Display protected ACLs but only for specific container objects
                              with same filter used for -sc cexplaces

   -sc accessrights        Display effective allowed attributes and child classes as well
                              as well as rights to modify Security Descriptor.
   -sc accesscheck         Alias for -sc accessrights.
   -sc daclcsvdmp:xxx      Dump Security Descriptor DACL in generic single ACE CSV mode, use xxx for DOMAIN replacement
   -sc daclcsvdump:xxx     Alias for -sc daclcsvdump
   -sc sdcsvdmp:xxx        Dump Security Descriptor in generic single ACE CSV mode, use xxx for DOMAIN replacement
   -sc sdcsvdump:xxx       Alias for -sc sdcsvdump
                             NOTE: For daclcsvdmp and sdcsvdump if no xxx specified uses -resolvesidsgenex


   REPLICATION / METADATA SHORTCUTS
   ********************************
   -sc objmeta:xxx         Object metadata for single object xxx
   -sc showmeta:xxx        Alias for objmeta
   -sc objsmeta:xxx        Object metadata for multiple objects base xxx
   -sc showmetas:xxx       Alias for objsmeta
   -sc legacylvr:xxx       Show any legacy members in object xxx
   -sc legacylvrs:xxx      Show any legacy members in multiple objects base xxx
   -sc legacygroupmembers:xxx  Show legacy group members from base xxx
   -sc replqueue           Show replication info for DC
   -sc ncrepl              Show replication info by NC, specify NC separately.
   -sc replstat:server     Shows replication info for server.
            Note: See adfind /meta? for more information


   QUICK OBJECT LOOKUP SHORTCUTS
   *****************************
   -sc fo:xx               Find object in GC with name xx.
   -sc kids:xx             Dump one level kids of DN xx.
   -sc u:xx                Find user in GC with name/samaccountname of xx.
   -sc userinfo:xx         Get common attributes for user xx.
   -sc g:xx                Find group in GC with name/samaccountname of xx.
   -sc c:xx                Find computer in GC with name/samaccountname of xx.
   -sc ou:xx               Find OU in GC with name of xx.
   -sc spn:xx              Find object with SPN cifs/xx or host/xx.
   -sc email:xx            Find object with email address of xx.
   -sc site:xx             Find AD site with name xx.
   -sc subnet:xx           Find AD subnet with name xx.
   -sc export              Filter out most attributes that are not needed in export. (no CSV)
   -sc export_user         Include standard writeable attributes for user. Does not filter for users.
   -sc export_group        Include standard writeable attributes for group. Does not filter for groups.
   -sc export_container    Include standard writeable attributes for container/OU. Does not filter
                               for containers and OUs.
   -sc export_x            [BETA] Include standard writeable attributes for most objects.
   -sc export_gpo          Include standard attributes for gpo. Does not filter for gpos.
   -sc sddldmp             Dump SDDLs for all objects.
   -sc sddlmap             Dump GUIDs needed for decoding SDDLs.
   -sc sitedmp             Dump all objects (except subnets) under sites container.
   -sc sitelinkdmp:xx      Dump site link objects for site named x
   -sc sitelinkdmpl:xx     Same as -sc sitelinkdmp but list mode
   -sc subnetdmp           Dump all subnets.
   -sc gpodmp              Dump all objects under GPO container.
   -sc fspdmp              Dump foreign security principals.
   -sc oudmp               Dump OUs.
   -sc dcdmp               Dump Domain Controllers.
   -sc dclist              Dump Domain Controllers FQDNs. Return DCs for specific
                           domain by specifying that domain for the base. Return DCs
                           for forest by specifying -gcb.
   -sc dclistf             Alias for -sc dclist + -gcb
   -sc dclist:rodc         Dump RO Domain Controllers FQDNs.
   -sc dclist:!rodc        Dump Writeable Domain Controllers FQDNs.
   -sc dclist:short        Dump Domain Controllers Short Host Names.
   -sc dclist:short:xx     Dump Domain Controllers Short Host Names, xx can be rodc,!rodc.
   -sc dclist:dn           Dump Domain Controllers Distinguished Names.
   -sc dclist:dn:xx        Dump Domain Controllers Distinguished Names, xx can be rodc,!rodc.
        NOTE: There is now a switch for the dclist shortcut. -dclist
              Instead of specifying a colon between dclist and the extra params, separate by a space
   -sc dcdmp:csv           Dump Domain Controllers in CSV format.
                           RODC (for RODCs), !RODC (for all writeable DCs).
   -sc dcdmp:RODC          Dump RODC Domain Controllers.
   -sc dcdmp:!RODC         Dump NOT RODC Domain Controllers - writeable DCs.
   -sc trustdmp            Dumps trust objects.
   -sc admincountdmp       Dump objects with adminCount set with DACL flags.
   -sc adobjcnt            Count of all objects in specified NC.
   -sc adobjcnt:user       Count of all user objects in specified NC.
   -sc adobjcnt:contact    Count of all contact objects in specified NC.
   -sc adobjcnt:computer   Count of all computer objects in specified NC.
   -sc adobjcnt:group      Count of all group objects in specified NC.
   -sc adobjcnt:ou         Count of all OU objects in specified NC.
   -sc adobjcnt:site       Count of all site objects in specified NC.
   -sc adobjcnt:subnet     Count of all subnet objects in specified NC.
   -sc adobjcnt:gpo        Count of all GPO objects in specified NC.
   -sc adobjcnt:fsp        Count of all foreign security principal objects in specified NC.
   -sc adobjcnt:mailbox    Count of all mailbox objects in specified NC.
   -sc users_disabled      Dump disabled users.
   -sc users_noexpire      Dump non-expiring users.
   -sc users_accexpired    Dump accounts that are expired (NOT password expiration).
   -sc users_pwdnotreqd    Dump users set with password not required.
   -sc computers_disabled  Dump computers that are disabled.
   -sc computers_pwdnotreqd Dump computers set with password not required.
   -sc computers_active    Dump computers that are enabled and password last
                           set and lastlogontimestamp <= 90 days. Req DFL2.
   -sc computers_inactive  Dump computers that are disabled or password last set
                           or lastlogontimestamp > 90 days. Req DFL2.
   -sc rodc_cacheable:xx   Check to see if secprin xx DN is cacheable on any RODCs.
   -sc structdmp           Best effort structure output of Active Directory.
   -sc structdump          Alias for -sc structdmp.
   -sc fgpps:xx            Dump Fine Grained Password Policy. Optional value xx=report.
   -sc fgpps:short         Dump Fine Grained Password Policy. Report Mode.
   -sc psos                Alias for fgpps.


   SCHEMA SHORTCUTS
   ****************
   -sc schver              Output Schema Version
   -sc sguid:xx            Resolves rightsGuid or schemaIdGuid to object
                           will not work on Windows 2000. Use next switches.
   -sc s2kguid:xx          Resolves schemaIDGuid to object
   -sc r2kguid:xx          Resolves rightsGuid to object

   -sc findpropsetrg:xx    Resolves property set displayname to rightsGuid
   -sc permguid:xx         Alias for findpropsetrg.
   -sc propsetmembers:xx   Finds all attributes with specified rightsGuid
   -sc propsetmembersl:xx  Same as above but sorted list output
   -sc listpropsets        List the available Property Sets
   -sc listpropsetsl       Same as above but sorted list output of displaynames
   -sc listpropsetscsv     Same as above but CSV output, displayname/rightsguid
   -sc listvwrites         List the available Validated Writes
   -sc listvwritesl        Same as above but sorted list output of displaynames
   -sc listvwritescsv      Same as above but CSV output, displayname/rightsguid
   -sc listxrights         List the available Extended Rights
   -sc listxrightsl        Same as above but sorted list output of displaynames
   -sc listxrightscsv      Same as above but CSV output, displayname/rightsguid

   -sc s:xx                Find schema objects by name/lDAPDisplayName
   -sc sl:xx               Same as above but sorted list output
                           NOTE: For -sc s: and -sc sl: append ;class or ;attr
                                 to focus on classes or attributes.

   -sc scontains:xx        Find classes an attribute is directly part of
   -sc scontainsl:xx       Same as above but sorted list output

   -sc cc:xx               Find classes that include specified class
   -sc ccl:xx              Same as above but sorted list output

   -sc pas                 Display attributes marked for PAS inclusion
   -sc pasl                Same as above but sorted list output

   -sc ropas               Display attributes marked for RODC replication
   -sc ropasl              Same as above but sorted list output
   -sc !ropas              Display attributes NOT marked for RODC replication
   -sc !ropasl             Same as above but sorted list output

   -sc indexed             Display attributes marked as indexed
   -sc indexedl            Same as above but sorted list output

   -sc tuple               Display attributes marked as tuple indexed
   -sc tuplel              Same as above but sorted list output

   -sc cindexed            Display attributes marked as container indexed
   -sc cindexedl           Same as above but sorted list output

   -sc sindexed            Display attributes marked as subtree indexed
   -sc sindexedl           Same as above but sorted list output

   -sc confidential        Display attributes marked as confidential
   -sc confidentiall       Same as above but sorted list output

   -sc copy                Display attributes marked to be copied
   -sc copyl               Same as above but sorted list output

   -sc constructed         Display contructed attributes
   -sc constructedl        Same as above but sorted list output

   -sc cat1                Display category 1 attributes
   -sc cat1l               (cat one el) Same as above but sorted list output

   -sc norepl              Display non-replicated attributes
   -sc norepll             Same as above but sorted list output

   -sc norepl+             Display non-replicated attributes (no links)
   -sc norepll+            Same as above but sorted list output

   -sc anr                 Display ANR attributes
   -sc anrl                Same as above but sorted list output

   -sc tombstone           Display attributes maintained in tombstone
   -sc tombstonel          Same as above but sorted list output

   -sc linked              Display linked value attributes
   -sc linkedl             Same as above but sorted list output
   -sc linked:fwd          Display forward linked value attributes
   -sc linkedl:fwd         Same as above but sorted list output
   -sc linked:rev          Display reverse linked value attributes
   -sc linkedl:rev         Same as above but sorted list output

   -sc syscrit             System Critical attributes
   -sc syscritl            Same as above but sorted list output

   -sc sdump               Dump schema in generic format for comparison
   -sc sdump:csv           Same as above but CSV output
   -sc sdump:attrib        Dump just the attribs.
   -sc sdump:class         Dump just the classes.
   -sc schemadmp           This is an alias for -sc sdump.

   -sc xrdump              Dump Extended rights for comparison
   -sc xrdump:csv          Dump Extended rights for comparison
   -sc xrdump:propset      Dump Property Sets for comparison
   -sc xrdump:vwrite       Dump Validated Writes for comparison
   -sc xrdump:xright       Dump Extended Rights for comparison
   -sc xrdmp               This is an alias for -sc xrdump.


   UNIVERSAL GROUP CACHING SHORTCUTS
   *********************************
   -sc ugcenabled          Sites enabled for Universal Group Caching (UGC)
   -sc ugcenabledl         Same as above but sorted list output

   -sc usedugc             Display users/computers that have used UGC
   -sc usedugc:decode      Same as above but decode values

   -sc dumpugcinfo         Dump info for users/computers that have used UGC
   -sc dumpugcinfo:decode  Same as above but decode values


   FSMO SHORTCUTS
   **************
   -sc fsmo                Display all FSMOs in domain of DC plus forest roles

   -sc fsmo:domain         Display all FSMOs in domain of DC
   -sc fsmo:pdc            Display PDC FSMO
   -sc fsmo:rid            Display RID FSMO
   -sc fsmo:im             Display Infrastructure Master FSMO

   -sc fsmo:forest         Display forest FSMOs
   -sc fsmo:schema         Display Schema FSMO
   -sc fsmo:dnm            Display Domain Naming Master FSMO


   EXCHANGE SHORTCUTS
   ******************
   -sc exchaddresses       Display objects with Exch addresses and addresses
   -sc exchaddresses:xx    Same as above, but only display addresses with xx
   -sc exchmbxs            Display objects with Exchange Mailboxes
   -sc exchsmtpaddr        Display SMTP addresses for Exchange enabled objects
   -sc exchprimarysmtp     Display Primary SMTP addresses for Exchange enabled objects
   -sc exchme:xx           Display objects that are Exchange mail enabled. If
                           xx is specified, it should be one of the strings:
                           users, contacts, or groups and focuses the query on those
                           object types.
   -scexchnosys            Add on to filter out Exchange system objects


   ADAM / ADLDS SHORTCUTS
   **********************
   -sc adamsid:xx          Resolve ADAM SID (xx) to object
   -sc adamguid:xx         Resolve ADAM GUID (xx) to object

   -sc caua                Add Constructed ADAM User Attribs for display
   -sc adam_info           Alias for -sc caua
   -sc adamobjcnt          Count of all objects in ADAM instance.
   -sc adamobjcnt:user     Count of all user objects in ADAM instance.
   -sc adamobjcnt:contact  Count of all contact objects in ADAM instance.
   -sc adamobjcnt:computer Count of all computer objects in ADAM instance.
   -sc adamobjcnt:group    Count of all group objects in ADAM instance.
   -sc adamobjcnt:ou       Count of all OU objects in ADAM instance.
   -sc adamobjcnt:site     Count of all site objects in ADAM instance.
   -sc adamobjcnt:subnet   Count of all subnet objects in ADAM instance.
   -sc adamobjcnt:gpo      Count of all GPO objects in ADAM instance.
   -sc adamobjcnt:fsp      Count of all foreign security principal objects in ADAM instance.
   -sc adamobjcnt:mailbox  Count of all mailbox objects in ADAM.
   -sc adam_fo:xx          Find object in ADAM with name xx.
   -sc adam_u:xx           Find user in ADAM with name xx.
   -sc adam_ou:xx          Find OU in ADAM with name xx.
   -sc adam_email:xx       Find object in ADAM with email address xx.
   -sc adam_spn:xx         Find object in ADAM with SPN xx.
   -sc adam_g:xx           Find group in ADAM with name xx.
   -sc ldsldapurl:xx       Return LDS LDAP URLs for instances with instancename xx.
   -sc ldsldapsurl:xx      Return LDS LDAPS URLs for instances with instancename xx.
   -sc ldsinstances:xx     Return info on instances with instancename xx.


  Ex1:
    adfind -sc exchaddresses:smtp
      Dump all Exchange objects and their SMTP proxyaddresses

  Ex2:
    adfind -sc indexedl
      Display sorted list of lDAPDisplayNames of indexed attributes

  Ex3:
    adfind -sc sl:msds*
      Display sorted list of lDAPDisplayNames of schema objects starting with msds

  Ex4:
    adfind -sc sdump
      Dump schema in generic format for WINDIFF compare with another schema




 This software is Freeware. Use at your own risk.
 I do not warrant this software to be fit for any purpose or use and
 I do not guarantee that it will not damage or destroy your system.
 Contact support@joeware.net via email for licensing information to package
 this utility in commercial products.

 See full Warranty documentation or download the latest version
 on http://www.joeware.net.

 If you have improvement ideas, bugs, or just wish to say Hi, I
 receive email 24x7 and read it in a semi-regular timeframe.
 You can usually find me at support@joeware.net

adfind /meta?
AdFind V01.62.00cpp Joe Richards (support@joeware.net) October 2023

-help         Basic help.
-?            Basic help.
-??           Advanced/Expert help.
-????         Shortcut help.
-sc?          Shortcut help.
-meta?        Metadata help.
-regex?       Regular Expressions help.
-gui          Combine with help switch to open that output in text editor.

Usage:
 AdFind [switches] [-b basedn] [-f filter] [attr list]

   basedn        RFC 2253 DN to base search from.
                 If no base specified, defaults to default NC.
                 Base DN can also be specified as a SID, GUID, or IID.
   filter        RFC 2254 LDAP filter.
                 If no filter specified, defaults to objectclass=*.
   attr list     List of specific attributes to return, if nothing specified
                 returns 'default' attributes, aka * set.

  Switches: (designated by - or /)

   MetaData Help
   =============
   AdFind has the ability to decode various metadata type attributes. These
   attributes can give information about replication status of the server
   itself or replication metadata for individual objects.

   These special attributes are normally returned from Active Directory in
   XML format. This is a bit bulky and can be tough to read without cleanup
   so I have added the ability decode the attributes and cut down the amount
   of data passed over the wire. Using the ;binary option when specifying an
   attribute causes AD to reformat certain attributes and send them across as
   binary blocks of data. When requesting the meta attributes outlined below
   if you do not specify the ;binary option, they will be returned in the
   native format, if you add the ;binary option, they will be returned in the
   alternate format and AdFind will decode the strings to its format.

   To further assist the ease of retrieving this information, see the shortcut
   usage menu via adfind /sc?
   Also see -metafilter* switches under the output section of AdFind /??

   MetaData Attributes
   -------------------
   msDS-ReplQueueStatistics  - RootDSE attribute
       Replication queue statistics. Output is labeled. No sort options.

   msDS-ReplPendingOps - RootDSE attribute
       Any replications operations currently in progress. Output is labeled.
       Default sort order is server return order. Sort options - dsa,date

   msDS-ReplConnectionFailures - RootDSE attribute
   msDS-ReplLinkFailures - RootDSE attribute
       Replication failure information. Output is labeled. Default sort order
       is by DSA. Sort options - dsa,date

   msDS-ReplAllInboundNeighbors - RootDSE attribute
   msDS-ReplAllOutboundNeighbors - RootDSE attribute
       Replication info for all direct neighbors. Output is labeled. Default
       sort order is by DSA. Sort options - dsa,date,nc,err

   msDS-TopQuotaUsage - RootDSE attribute
       Indicates the top object owners on a given server. Output is labeled.
       Default sort order is server return order. Sort options - nc,owner.

   msDS-NCReplInboundNeighbors - Naming Context attribute
   msDS-NCReplOutboundNeighbors - Naming Context attribute
       Replication for all direct neighbors for the specific NC. Output is
       labeled. Default sort order is by DSA. Sort options - dsa,date,nc,err

   msDS-NCReplCursors - Naming Context attribute
       Replication cursors by DSA by context. Output format:
            HighestUSN LastSyncTime DSA
       Default sort order is last sync time. Sort options - lastsync,dsa

   msDS-ReplAttributeMetaData - Object Level attribute
       Replication metadata for object. Output format:
             USNLocal DSA USNOrig Date/Time Version Attribute
       Default sort order is date. Sort options - attrib,DSA,date,usnloc,usnorig,ver

   msDS-ReplValueMetaData - Object Level attribute (FFL2+ only - i.e. LVR Replication)
       Replication value metadata for object. Output format:
             attribute USNLocal DSA USNOrig Date/Time Version State ObjectDN
       Default sort order is date. Sort options - attrib,obj,DSA,state,date,usnloc,usnorig,ver


   Sort Options
   ------------
   The decoded output for most of the metadata attributes can be sorted to various
   fields in the output. The specific fields for each attribute are listed with
   the description of the attributes. In order to change the sort field, use the
   -metasort switch. Specify the switch combined with the options specified above
   to change the sort order. If value has a dash (-) appended, the search order
   is reversed. Note that if there are more than 1000 values returned the output will
   not be fully sorted. This is due to how the values are returned, coupled with memory
   and CPU utilization issues in trying to maintain and sort all of that information.
   Visualize a group with 500k users in it. A purposeful decision to be fast and not
   eat up resources was made versus to guarantee sort order in those conditions.

   Filter Options
   The decoded output for msDS-ReplAttributeMetaData;binary and
   msDS-ReplValueMetaData;binary can be filtered using -metafilter* switches. You
   can specify several filters by separating them with a semi-colon (;). If you
   specify several filters of the same type, i.e. two or more version filters
   they are OR'ed together. If you specify several filters of different types they
   are AND'ed together.

  Ex1:
    adfind -rootdse msDS-TopQuotaUsage;binary
      Get top 10 quota users in decoded format

  Ex2:
    adfind -b cn=someobject,ou=someou,dc=test,dc=loc -s base msDS-ReplAttributeMetaData;binary
      Get attribute metadata for specified object in decoded format

  Ex3:
    adfind -b dc=test,dc=loc -s base msDS-ReplAttributeMetaData;binary -metafilter maxpwdage
      Get attribute metadata for maxpwdage attribute for domain.




 This software is Freeware. Use at your own risk.
 I do not warrant this software to be fit for any purpose or use and
 I do not guarantee that it will not damage or destroy your system.
 Contact support@joeware.net via email for licensing information to package
 this utility in commercial products.

 See full Warranty documentation or download the latest version
 on http://www.joeware.net.

 If you have improvement ideas, bugs, or just wish to say Hi, I
 receive email 24x7 and read it in a semi-regular timeframe.
 You can usually find me at support@joeware.net

adfind /regex?
AdFind V01.62.00cpp Joe Richards (support@joeware.net) October 2023
-help         Basic help.
-?            Basic help.
-??           Advanced/Expert help.
-????         Shortcut help.
-sc?          Shortcut help.
-meta?        Metadata help.
-regex?       Regular Expressions help.
-gui          Combine with help switch to open that output in text editor.

Usage:
 AdFind [switches] [-b basedn] [-f filter] [attr list]

   basedn        RFC 2253 DN to base search from.
                 If no base specified, defaults to default NC.
                 Base DN can also be specified as a SID, GUID, or IID.
   filter        RFC 2254 LDAP filter.
                 If no filter specified, defaults to objectclass=*.
   attr list     List of specific attributes to return, if nothing specified
                 returns 'default' attributes, aka * set.

  Switches: (designated by - or /)


   AdFind Regular Expressions
   ==========================
   AdFind allows you to specify regular expressions as an ongoing beta feature. 
   The functionality is provided by the boost::regex (boost 1.71.0). You can find
   more information on this module at
         https://www.boost.org/doc/libs/1_71_0/libs/regex/doc/html/index.html
   I have enabled boost::regex::perl and will try to make the functionality as similar
   to perl regex functionality as possible.

   This functionality is beta while I try to sort out how people will use the functionality
   and how the Boost RegEx module functions. As of right now the functionality is primarily
   "inclusive" functionality meaning that you can use regexs to make inclusive choices.
   There is also, as of V01.53.00, some limited exclusive functionality where you can exclude
   things. This exclude functionality is enabled with !m instead of m.
   If you have any questions, comments, thoughts on this functionality
   please email me at support@joeware.net and give me the details.

   You specify regular expressions as an addendum on attributes when you specify attributes
   to return and display. Currently there is no global regular expression capability that
   simultaneously works across all attributes. To specify a regular expresion append a
   colon and then the regular expression like "attributename:m/regex/options". Generally
   it will be a good idea to include the whole value, attribute and regular
   expression, in quotes in case there are any characters that the shell consider as
   special and blows up the parameter handling. For exclusionary matching, use !m instead of m.

   The current functionality includes regex match which is specified with m/regex/options
   and regex substitute s/regex/replace/options as well as !m/regex/options exclusion match.
   The options available are i for case-insensitive search and g for global search.
   A note for global search in that the version of boost::regex I am using is not compiled with
   the experimental feature BOOST_REGEX_MATCH_EXTRA due to performance concerns so marked
   subexpression captures may be limited.

   Again, for V01.53.00 I have added !m/regex/options which is just like m/regex/options
   but it will return data that doesn't match.

   Special characters that need to be "escaped" with \ are .[{}()*+?|^$ for matches because
   they have special functions just like with perl. Allegedly you should be able to escape \ with
   a \ as well but I have not found that to work well and instead use \x5c instead.

   There isn't likely to be a joeware tutorial on regular expressions, please check out the perl
   tutorials on regular expressions. If you attempt a regular expression and it doens't work
   try to duplicate with perl and see if the functionality is the same. If it works under perl
   and doesn't work with the boost::regex functionality in AdFind please email me with details.

   For the -jsd* switches you can replace the include:exclude parameter with a regular expression.
   This will only allow the inclusive regular expression and not an exclusionary value.

  Ex1:
    adfind -f "ou=*" -jsdenl "m/\[owner|\[group|allow.+(domain admins|account operators)/i"
      Retrieve all OUs and output owner, group, and any ACEs with domain admins or account ops.

  Ex2:
    adfind -f description=* description:s/administrators/***ADMINS***/ig
      Retrieve all objects that have a description and replace "administrators" with "***ADMINS***".

  Ex3:
    adfind -f description=*adm* description:s/(adm\w+)/\U\1/ig
      Retrieve all objects that have a description including *adm* and replace "adm*" with
      uppercase version of match.
  Ex4:
    adfind -f "ou=*" -jsdenl "!m/\[owner|\[group|allow.+(domain admins|account operators)/i"
      Retrieve all OUs Security Descriptors and output everything but owner, group, and any ACEs
      with domain admins or account ops.

  Ex5:
    adfind -f "ou=*" -jsdenl "!m/(NT AUTHORITY|BUILTIN)/i"
      Retrieve all OUs Security Descriptors and output any lines that don't contain BUILTIN or
      NT AUTHORITY.




 This software is Freeware. Use at your own risk.
 I do not warrant this software to be fit for any purpose or use and
 I do not guarantee that it will not damage or destroy your system.
 Contact support@joeware.net via email for licensing information to package
 this utility in commercial products.

 See full Warranty documentation or download the latest version
 on http://www.joeware.net.

 If you have improvement ideas, bugs, or just wish to say Hi, I
 receive email 24x7 and read it in a semi-regular timeframe.
 You can usually find me at support@joeware.net
