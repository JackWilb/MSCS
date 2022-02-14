## RC4

To run the RC4 code, use the command `python3 homework2-rc4.py`. This will give hex. To get ints, remove the `hex()` cast and the subset that removes the `0x` from the start of each group.


## encrypt/decrypt
For the encryption and decryption, I've provided two example below. They are only a single bit different. See the per round log in the the per-round-output.txt file
```
python homework2-enc-dec.py encrypt 6 3 3 5 5 6 a a
>> input: ['6', '3', '3', '5', '5', '6', 'a', 'a']
>> output:  Ò É « J Ô © á p

python homework2-enc-dec.py decrypt Ò É « J Ô © á p
>> input: ['Ò', 'É', '«', 'J', 'Ô', '©', 'á', 'p']
>> output:  6 3 3 5 5 6 a a




python homework2-enc-dec.py encrypt 6 3 3 5 5 6 b a
>> input: ['6', '3', '3', '5', '5', '6', 'b', 'a']
>> output:  Ò É « J Ô © D p

python homework2-enc-dec.py decrypt Ò É « J Ô © D p
>> input: ['Ò', 'É', '«', 'J', 'Ô', '©', 'D', 'p']
>> output:  6 3 3 5 5 6 b a
```
