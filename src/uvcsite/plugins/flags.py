from enum import Enum


States = Enum(
    'NOT_INSTALLED',
    'INSTALLED',
    'INCONSISTANT')


ResultTypes = Enum(
    'JSON',
    'PLAIN',
    'MESSAGE')
