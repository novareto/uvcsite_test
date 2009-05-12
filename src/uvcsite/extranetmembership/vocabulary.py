import grok                                                                                                                
from zope.schema.vocabulary import SimpleVocabulary
from zope.app.schema.vocabulary import IVocabularyFactory

class VocabularyBerechtigungen(grok.GlobalUtility):
    """Vocabulary factory for workflow states.
    """
    grok.implements(IVocabularyFactory)
    grok.name('VocabularyBerechtigungen')

    def __call__(self, context):
        items=[('uvc.ManageKontakt', 'uvc.ManageKontakt'),
               ('uvc.RolleMember', 'uvc.RolleMember'), 
               ('Manager', 'Manager'), 
               ('Entgeltnachweis', 'Entgeltnachweis')]
        items.sort()
        return SimpleVocabulary.fromItems(items)

