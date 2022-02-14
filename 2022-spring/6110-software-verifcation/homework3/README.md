Commands for Q1:

```
rumur q1-peterson.m --output q1-peterson.c
cc -std=c11 -O3 q1-peterson.c -lpthread -mcx16
./a.out

# For symmetry reduction
rumur q1-peterson.m --output q1-peterson.c --symmetry-reduction exhaustive
cc -std=c11 -O3 q1-peterson.c -lpthread -mcx16
./a.out
```

For Q3 I was in ispin doing the commands there. See the file for changes, I only changed the atomic wait in the handle section.