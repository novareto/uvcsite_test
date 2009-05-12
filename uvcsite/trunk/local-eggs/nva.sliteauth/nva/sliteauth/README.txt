Test for nva.sliteauth
======================
:doctest: 

Um sämtliche ENMS Funktionalitäten im abzudecken
müssen wir das Inteface uvcsite.extranetmenbership.interfaces
IUsermanagement erfüllen.

  >>> from nva.sliteauth.usermanagement import UserManagement
  >>> um = UserManagement()

Da wir mit Unterkennung arbeiten müssen wir in der Lage sein
von Benuzterkennungen immer den Mitgliedsnummer und die laufende
Nummer herausbekommen das machen wir mit der Methode zerlegUser

  >>> user = "0101010001"
  >>> um.zerlegUser(user)
  ['0101010001', '00']
  >>> um.zerlegUser(user+'-01')
  ['0101010001', '01']

Wir finden einen User über die getUser Methode als Ergebnis
sollten wir ein Dict mit den Eigenschaften des User bekommen

  >>> um.getUser(user)
  {'passwort': u'passwort', 'mnr': u'0101010001', 'az': u'00', 'rollen': u'uvc.Unfallanzeige', 'email': u'cklinger@novareto.de'}
  >>> unknown = um.getUser('notknown')
  >>> print unknown
  None

Ok versuchen wir nun einen neuen User anzulegen. 
Unsere formlib library liefert uns immer ein dict object.

  >>> nuser = {'mnr':'0101010002', 'passwort':'test', 'email':'klaus@test.de', 'rollen': 'uvc.ManageSeite'}
  >>> status = um.addUser(**nuser)
  >>> print status
  None

Wenn die Schreiboperation erfolgreich war sollten wir den User über die getUser Methode bekommen

  >>> um.getUser('0101010002')
  {'passwort': u'test', 'mnr': u'0101010002', 'az': u'00', 'rollen': u'uvc.ManageSeite', 'email': u'klaus@test.de'}

  
  >>> nuser01 = {'mnr':'0101010002-01', 'passwort':'test', 'email':'klaus@test.de', 'rollen': 'uvc.ManageSeite'}
  >>> status = um.addUser(**nuser01)
  >>> print status
  None

  >>> um.getUserGroups('0101010002')
  [{'passwort': u'test', 'mnr': u'0101010002', 'az': u'01', 'rollen': u'uvc.ManageSeite', 'email': u'klaus@test.de'}]

Natürlich muss es möglich sein User upzudaten...

  >>> uUser = {'passwort': u'xtest', 'mnr': u'0101010002', 'az': u'00', 'rollen': u'uvc.ManageSeite', 'email': u'xklaus@test.de'}
  >>> um.updUser(**uUser)
  >>> um.getUser("0101010002")
  {'passwort': u'xtest', 'mnr': u'0101010002', 'az': u'00', 'rollen': u'uvc.ManageSeite', 'email': u'xklaus@test.de'}

  >>> um.delUser('0101010002')
  >>> um.delUser('0101010002-01')

  >>> #import interlude
  >>> #interlude.interact(locals())
