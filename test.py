from Models.artist import *
from Models.album import Album
from Services.logger import Logger

a = Artist()
b = Album()

log = Logger('test.log', 'DEBUG')

a.name = 'Ian'
b.name = 'Bree'

log.log_error('test error')
log.log_info('test info')

print a.name
print b.name
