import grok
from zope.component import getUtility, queryUtility

from pysqlite2 import dbapi2 as sqlite

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



class UserManagement(grok.GlobalUtility):
    #grok.implements(IUserManagement)
    #grok.name('novareto')

    def getConn(self):
        db = '/'.join(__file__.split('/')[:-1]) + '/extranetusers.sqlite'
        conn = sqlite.connect(db)
        conn.row_factory = dict_factory
	return conn


    def zerlegUser(self, mnr):
	if len(mnr) > 10:
	    return mnr.split('-')
	return [mnr, '00'] 

    def getUser(self, mnr):
	mnr, az = self.zerlegUser(mnr)
	sql = """SELECT * FROM users WHERE mnr = '%s' AND az = '%s'""" %(mnr, az)
	conn = self.getConn()
	cur = conn.cursor()
	cur.execute(sql)
	erg = cur.fetchone()
	cur.close()
	conn.close()
	return erg

    def getUserGroups(self, mnr):
	mnr, az = self.zerlegUser(mnr)
	sql = """SELECT * FROM users WHERE mnr = '%s' AND az != '%s'""" %(mnr, az)
	conn = self.getConn()
	cur = conn.cursor()
	cur.execute(sql)
	erg = cur.fetchall()
	cur.close()
	conn.close()
	return erg

    def addUser(self, **kw):
	mnr, az = self.zerlegUser(kw.get('mnr'))
        sql = """INSERT INTO users (mnr, az, passwort, email, rollen) 
	         VALUES ('%s', '%s', '%s', '%s', '%s')""" %(mnr, az, kw.get('passwort'), kw.get('email'), kw.get('rollen'))
	conn = self.getConn()
	cur = conn.cursor()
	cur.execute(sql)
	cur.close()
	conn.commit()
	conn.close()
	return


    def updUser(self, **kw):
	mnr, az = self.zerlegUser(kw.get('mnr'))
	sql = """UPDATE users SET passwort='%s', email='%s', rollen='%s'
	         WHERE mnr = '%s' AND az = '%s'""" %(kw.get('passwort'), kw.get('email'), kw.get('rollen'), mnr, az)
        conn = self.getConn()
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	return


    def delUser(self, mnr):
	mnr, az = self.zerlegUser(mnr)
	sql = """DELETE FROM users WHERE mnr = '%s' AND az = '%s'""" %(mnr, az)
	conn = self.getConn()
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	return

