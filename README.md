# imap-idle-sync

## Introduction
A very simple script to hook up to a IMAP server using IDLE and execute a script when remote state changes. It also runs it in case of connection death, and each 10 minutes. Only SSL targets are supported. This doesn't really aim to be generic.

I use it to sync two active IMAP accounts along with `isync` (see `imap-idle-isync` directory). Kind of like a live backup. There are plenty of programs like this on GitHub. Tried all of them before writing my own, none worked for me.

A template dockerfile is given so the program to be executed can just be put on top.

No dependencies! I had issues with Python's `imaplib`, so I send raw messages.

## Usage
Both in manual daemoning (no config files) and using Docker, the following arguments are available:

- `REMOTE` and `PORT`: IMAP server to connect to. Default value for `PORT` is 993.
- `USERNAME` and `PASSWORD`, both in plain text.
- `SYNC`: command to run when a syncing is happening.
- `TIMEOUT`: How much to wait before resetting the connection (in case it died; there are no heartbeats while in IDLE mode).
- `ERRWAIT`: In case the connection failed, how much time to wait before trying to reconnect.

TIMEOUT is set to 10 minutes (600 seconds) by default. ERRWAIT is set to TIMEOUT.