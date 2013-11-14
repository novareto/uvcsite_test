# -*- coding: utf-8 -*-

import grok
import uvcsite


grok.templatedir('templates')


class NotFound(uvcsite.Page, grok.components.NotFoundView):
    """Not Found Error View
    """
    def update(self):
        super(NotFound, self).update()
        uvcsite.logger.error(
            'NOT FOUND: %s' % self.request.get('PATH_INFO', ''))


class SystemError(uvcsite.Page, grok.components.ExceptionView):
    """Custom System Error for UVCSITE
    """

    def __init__(self, context, request):
        super(SystemError, self).__init__(context, request)
        self.context = grok.getSite()
        self.origin_context = context

    def update(self):
        super(SystemError, self).update()
        uvcsite.logger.error(self.origin_context)
