# sparty
```
_|_|_|    _|_|_|     _|_|    _|_|_|    _|_|_|_|_|  _|      _|
_|        _|    _|  _|    _|  _|    _|      _|        _|  _|
_|_|    _|_|_|    _|_|_|_|  _|_|_|        _|          _|
	_|  _|        _|    _|  _|    _|      _|          _|
_|_|_|    _|        _|    _|  _|    _|      _|          _|
```

Sparty is an open source tool written in Python to audit web applications using Sharepoint and frontpage architecture. The motivation behind this tool is to provide an easy and robust way to scrutinize the security configurations of sharepoint and frontpage based web applications. Due to the complex nature of these web administration software, it is required to have a simple and efficient tool that gathers information, check access permissions, dump critical information from default files and perform automated exploitation if security risks are identified. A number of automated scanners fall short of this and Sparty is a solution to that.

__Webpage__:       <http://sparty.secniche.org>  
__Documentation__: <http://sparty.secniche.org/usage.html>

```
-----------------------------------
Functionalities and capabilities !
-----------------------------------
1. Sharepoint and Frontpage Version Detection!
2. Dumping Password from Exposed Configuration Files!
3. Exposed Sharepoint/Frontpage Services Scan!
4. Exposed Directory Check!
5. Installed File and Access Rights Check!
6. RPC Service Querying!
7. File Enumeration!
8. File Uploading Check!

-----------------------------------------------
Additional notes about working and design
----------------------------------------------
1. This version of sparty is written in Python 2.6 (final) running on backtrack 5.0.
2. This version (v 0.1) primarily includes assessment of configuration flaws.
3. This version is based on the practical testing and assessment of frontpage & sharepoint.
```

## Getting Started
### Prerequisites
1. Python 3.8~ is required.
2. Run `python -m pip install -r requirements.txt`

### Things to take care of while using sparty
Please take this into consideration:

1. Always specify https | http explcitly !
2. Always provide the proper directory structure where sharepoint/frontpage is installed !
3. Do not specify '/' at the end of url !

### Usage

```
Usage: sparty.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Frontpage::
    -f FRONTPAGE, --frontpage=FRONTPAGE
                        <FRONTPAGE = pvt | bin> -- to check access permissions
                        on frontpage standard files in vti or bin directory!

  Sharepoint::
    -s SHAREPOINT, --sharepoint=SHAREPOINT
                        <SHAREPOINT = forms | layouts | catalog> -- to check
                        access permissions on sharepoint standard files in
                        forms or layouts or catalog directory!

  Mandatory::
    -u URL, --url=URL   target url to scan with proper structure

  Information Gathering and Exploit::
    -v FINGERPRINT, --http_fingerprint=FINGERPRINT
                        <FINGERPRINT = ms_sharepoint | ms_frontpage> --
                        fingerprint sharepoint or frontpage based on HTTP
                        headers!
    -d DUMP, --dump=DUMP
                        <DUMP = dump | extract> -- dump credentials from
                        default sharepoint and frontpage files (configuration
                        errors and exposed entries)!
    -l DIRECTORY, --list=DIRECTORY
                        <DIRECTORY = list | index> -- check directory listing
                        and permissions!
    -e EXPLOIT, --exploit=EXPLOIT
                        EXPLOIT = <rpc_version_check | file_upload |
                        config_check> -- exploit vulnerable installations by
                        checking RPC querying and file uploading
    -i SERVICES, --services=SERVICES
                        SERVICES = <serv | services> -- checking exposed
                        services !

  General::
    -x EXAMPLES, --examples=EXAMPLES
                        running usage examples !
```

## Authors

* __Aditya K Sood__ - _Initial Work_ - [Twitter](https://twitter.com/adityaksood)
* __Angus Johnston__ - _Python 3 Support_ - [Twitter](https://twitter.com/DakuTree)

See also the list of [contributors](https://github.com/DakuTree/sparty/graphs/contributors) who participated in this project.

## License

This project is licensed under the BSD License - see the [LICENSE.md](LICENSE.md) file for details
