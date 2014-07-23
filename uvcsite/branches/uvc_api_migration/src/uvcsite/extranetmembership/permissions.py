from grokcore.security import name, permissions, Role, Permission


class MasterUser(Role):
    name('uvc.MasterUser')
    permissions('uvc.ManageCoUsers')


class ManageCoUsers(Permission):
    name('uvc.ManageCoUsers')
