

For question 4, I ran the c programs in KLEE's online web editor to check the programs and verify the output. You could easily run them on the command line with:

```
clang -emit-llvm -c quicksort.c
./a.out
clang -emit-llvm -c buggy-quicksort.c
./a.out
```

to get the same output.
