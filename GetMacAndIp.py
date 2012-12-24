import socket,traceback
import threading
import uuid



node = uuid.getnode()
mac = uuid.UUID(int = node).hex[-12:]
print 'localhost mac is : '+str(mac)

