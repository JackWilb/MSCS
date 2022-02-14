My homework 3 work consists of 3 files:

- homework3-expo.py
- homework3-client.py
- homework3-server.py

With these 3 files you can simulate a Diffie-Hellman key exchange.

To run the expo file, modify the python to run a computation, and then run the file with:

```
python3 homework3-expo.py
```

To simulate a Diffie-Hellman key exchange run:

```
# in one terminal session
python3 homework3-server.py

> Server, Bob, received 179464
> Server, Bob, sending 449485
> Server, Bob, computes key as 475269


# in another terminal session
python3 homework3-client.py

> Client, Alice, sending 179464
> Client, Alice, received 449485
> Client, Alice, computes key as 475269
```