#!/usr/bin/env python3

import os, socket, ssl, time

getEnv = lambda n, d=None: x if (x := os.getenv(n)) is not None else d

REMOTE = getEnv('REMOTE')
if REMOTE is None:
	print('No remote?')
	exit(1)

PORT = int(getEnv('PORT', 993))
USER = getEnv('USERNAME')
PASS = getEnv('PASSWORD')
SYNC = getEnv('SYNC')
if SYNC is None:
	print('No sync command?')
	exit(2)

TIMEOUT = int(getEnv('TIMEOUT', 10*60))
ERRWAIT = int(getEnv('ERRWAIT', TIMEOUT))



context = ssl.create_default_context()

def recvuntil(s, text):
        ret = b''
        while text.upper() not in ret.upper():
                ret += s.recv(1)
        return ret

def waitForOK(s, ctr):
        ret = recvuntil(s, ('\n%d OK' % ctr).encode())
        ret += recvuntil(s, b'\n')
        return ret

def connect():
        s = socket.create_connection((REMOTE, PORT))
        s.settimeout(TIMEOUT)
        ss = context.wrap_socket(s, server_hostname=REMOTE)
        ss.sendall(('1 LOGIN "'+USER+'" "'+PASS+'"\n').encode())
        print(waitForOK(ss, 1).decode())
        ss.sendall(b'2 SELECT INBOX\n')
        print(waitForOK(ss, 2).decode())
        ss.sendall(b'3 IDLE\n')
        print(recvuntil(ss, b'+ entering idle mode').decode())
        return ss

def off(s):
        s.sendall(('\n4 logout').encode())
        s.close()

if __name__ == '__main__':
        os.system(SYNC)
        s = connect()
        while True:
                try:
                        recvuntil(s, b'*')
                        s.recv(1024) # Not beautiful
                except KeyboardInterrupt: break
                except:
                        # Probably a timeout, but it doesn't matter
                        # Just reset everything
                        # It might fail!
                        while True:
                                try:
                                        off(s)
                                        os.system(SYNC)
                                        s = connect()
                                        break
                                except:
                                        time.sleep(ERRWAIT)
                                        os.system(SYNC)
                        continue

                # Got one
                os.system(SYNC)
