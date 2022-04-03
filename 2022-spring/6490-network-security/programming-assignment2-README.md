# Programming Assignment 2

To run the code run:

```
python programming-assignment2.py
diff programming-assignment2-50KB.txt programming-assignment2-received-data.txt
```


## Implemented protocol

```
Handshake:

Client                                       Server

                      "AES"
-------------------------------------------------->

                  Server Cert
<--------------------------------------------------

            Client Cert, Encrypted RA
-------------------------------------------------->

                  Encrypted RB
<--------------------------------------------------


**BOTH PARTIES CALCULATE KAB = RA ^ RB**


                   Client HMAC
-------------------------------------------------->

                   Server HMAC
<--------------------------------------------------





Key Exchange:

            KAB{
              client_auth_key,
              client_encryption_key, 
              KA-{
                client_auth_key,
                client_encryption_key
              }
            }
-------------------------------------------------->

            KAB{
              server_auth_key,
              server_encryption_key, 
              KB-{
                client_auth_key,
                client_encryption_key
              }
            }
<--------------------------------------------------





Data Transfer:

server_encryption_key{ filename, client_auth_key{filename} }
-------------------------------------------------->

        client_encryption_key{ file_data }
<--------------------------------------------------

server_encryption_key{ "received", client_auth_key{"received"} }
-------------------------------------------------->

client_encryption_key{ sha256(file), server_auth_key{sha256(file)} }
<--------------------------------------------------
```
