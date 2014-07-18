# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

from grokcore.component import global_utility
from zope.generations.generations import SchemaManager
from zope.generations.interfaces import ISchemaManager


UVCSchemaManager = SchemaManager(
    minimum_generation = 1,
    generation = 1,
    package_name = __name__
    )

global_utility(
    UVCSchemaManager,
    provides=ISchemaManager,
    name="uvcsite",
    direct=True
    )
