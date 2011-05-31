from Mailman.MySQLConnector import MySQLConnector
from Mailman.ForgeSecurityManager import ForgeSecurityManager
import os
import re

##############################
# Local Configuration Load
# Taken from Codendi/src/utils/include.py
##############################
def load_local_config(filename):
    """Local Configuration Load"""
    try:
        f = open(filename)
    except IOError, (errno, strerror):
        print "Can't open %s: I/O error(%s): %s" % (filename, errno, strerror)
    else:
        comment_pat   = re.compile("^\s*\/\/")
        empty_pat     = re.compile("^\s*$")
        assign_pat    = re.compile("^\s*\$(.*);\s*$")
        nodollar_pat  = re.compile("(\s+)\$")
        dottoplus_pat = re.compile("(\s+)\.(\s+)")
        # filter end of line comment, but beware of things like http:// or ldap:// -> make sure there is a blank char before the '//'
        nocomment_pat = re.compile(" \/\/.*")
        while True:
            line = f.readline()
            if not line: break
            if comment_pat.match(line) or empty_pat.match(line): continue
            m = assign_pat.match(line)
            if m is not None:
                n = nodollar_pat.sub(" ",m.group(1))
                n = dottoplus_pat.sub(" + ",n)
                n = nocomment_pat.sub("",n)
                exec n in globals()
        f.close()

def load_codendi_conf():
    db_include = os.getenv('CODENDI_LOCAL_INC','')
    if db_include is "":
        db_include = "/etc/codendi/conf/local.inc"
    load_local_config(db_include)
    load_local_config(db_config_file)
    

def extendMemberAdaptor(list):
    load_codendi_conf()
    dbparam={}
    #Config to connect to database
    dbparam['dbhost'] = sys_dbhost
    dbparam['dbuser']= sys_dbuser
    dbparam['dbpassword'] = sys_dbpasswd
    dbparam['database'] = sys_dbname
    dbparam['refresh'] = 360

    dbparam['mailman_table']= 'plugin_mailman'#table where mailman stores memeberships info
    ######################      
    # Session Management #
    ######################
    #Forge default session
    dbparam['cookiename']='CODENDI_session_hash'
    dbparam['queryCookieMail']="SELECT email FROM session,user WHERE user.user_id=session.user_id AND session_hash = '%s';"
    dbparam['queryCookieId']="SELECT user_id FROM session WHERE session_hash = '%s';"

    dbparam['queryIsAdmin'] = "SELECT COUNT(*) FROM mail_group_list WHERE list_admin=%s AND list_name='%s';"
    dbparam['queryIsMonitoring'] = "SELECT COUNT(*) FROM "+dbparam['mailman_table']+", user "+" WHERE user.email = "+dbparam['mailman_table']+".address"+" AND user.user_id=%s AND listname='%s';"
    dbparam['queryIsSiteAdmin'] = "SELECT count(*) AS count FROM user_group WHERE user_id=%s AND group_id=1 AND admin_flags='A';"

    #Forge ZendSession
    #dbparam['cookiename']='zend_cookie_session'
    #dbparam['queryCookieMail']="""select substring(session_data,'email";s:[0-9]*?:"(.*)";s') from plugin_zendsession where session_hash='%s';"""
    #dbparam['queryCookieId']="""SELECT substring(session_data,'user_id";i:([0-9]{1,})') FROM plugin_zendsession WHERE session_hash='%s';"""

    ######################
    # Type of connection #
    ######################
    db = MySQLConnector(list,dbparam)
    list._memberadaptor = db

def extendSecurityManager(list):
    sm = ForgeSecurityManager(list)
    list._securitymanager = sm
