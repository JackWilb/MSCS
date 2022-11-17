Jack Wilburn
Assignment 6

1. LSQ (30 points)

The table below lists a sequence of loads and stores in the LSQ, when their one/two input operands are made available, and their computed effective addresses. Estimate when the address calculation happens for each ld/st and when each ld/st accesses the data memory. Assume that the processor does no memory dependence prediction to speculatively issue loads. 

|   LD/ST   |   The register for the address calculation is made available   |   The register that must be stored into memory is made available    |   The calculated effective address   |   Address Calculated   |   Data memory access time   |
|---|---|---|---|---|
|  LD  |  4  |  -  |  abce  |  5   |       6  |
|  ST  |  9  |  3  |  abdd  |  10  |  commit  |
|  LD  |  2  |  -  |  abcd  |  3   |      11  |
|  LD  |  5  |  -  |  abdd  |  6   |      11  |
|  ST  |  2  |  3  |  abdd  |  3   |  commit  |
|  LD  |  6  |  -  |  abdd  |  7   |       8  |
|  LD  |  1  |  -  |  abce  |  2   |      11  |

2. Memory access times (30 points)

Consider a processor and a program that would have an IPC of 1 with a perfect 1-cycle L1 cache. Assume that each additional cycle for cache/memory access causes program execution time to increase by one cycle. Assume the following MPKIs and latencies for the following caches:

  L1: 16 KB: 1-cycle: 40 MPKI
  L2: 1 MB: 8-cycle: 25 MPKI
  L3: 16 MB: 30-cycle: 10 MPKI
  L4: 64 MB: 60-cycle: 5 MPKI
  Memory: 250 cycles 

Estimate the program execution times for the following cache hierarchy configurations. Which cache hierarchy is the best, and (in one sentence) can you reason about why it emerges as the best design point?

L1-L2-L3-L4-memory:
L1: 960 instructions (1 cycle)
L2: 15 instructions (8 cycles)
L3: 15 instructions (30 cycles)
L4: 5 instructions (60 cycles)
Memory: 5 instructions (250 cycles)

Total cycles: (960 * 1) + (15 * 8) + (15 * 30) + (5 * 60) + (5 * 250) = 3080

L1-L2-L3-memory:
L1: 960 instructions (1 cycle)
L2: 15 instructions (8 cycles)
L3: 15 instructions (30 cycles)
Memory: 10 instructions (250 cycles)

Total cycles: (960 * 1) + (15 * 8) + (15 * 30) + (10 * 250) = 4030

L1-L2-L4-memory:
L1: 960 instructions (1 cycle)
L2: 15 instructions (8 cycles)
L4: 20 instructions (60 cycles)
Memory: 5 instructions (250 cycles)

Total cycles: (960 * 1) + (15 * 8) + (20 * 60) + (5 * 250) = 3530

The best is the cache with all levels. This is likely because with each level, you have a chance to hit and reduce the overall execution times of going deeper into the cache/memory.


3. Cache Organization (20 points)

A 48 MB L3 cache has a 128 byte block (line) size and is 12-way set-associative. How many sets does the cache have? How many bits are used for the offset, index, and tag, assuming that the CPU provides 40-bit addresses? How large is the tag array? (If you do not explain your steps, you will not receive partial credit for an incorrect answer.)

Sets: (48 * 2^10) / (12 * 2^7) = 32

Offset bits: log(128) = 7
Index bits: log(32) = 5
Tag bits: 40 - 7 - 5 = 28

Tag array: 28b * 12 * 32 = 10752b

4. Cache Miss Rates (20 points)

For the following access pattern: (i) Indicate if each access is a hit or miss. (ii) What is the hit rate? Assume that the cache has 2 sets and is 2-way set-associative. Assume that block A maps to set 0, B to set 1, C to set 0, D to set 1, E to set 0, F to set 1. Assume an LRU replacement policy.

Does the hit rate improve if you assume a fully-associative cache of the same size, i.e., 1 set and 4 ways? Again, indicate if each access is a hit or a miss.

Access pattern: A B C D E A C E A C E 

2 set - 2 way
1.  A - miss
2.  B - miss
3.  C - miss
4.  D - miss
5.  E - miss
6.  A - miss
7.  C - miss
8.  E - miss
9.  A - miss
10. C - miss
11. E - miss

Miss rate: 100%

1 set - 4 way
1.  A - miss
2.  B - miss
3.  C - miss
4.  D - miss
5.  E - miss
6.  A - miss
7.  C - hit
8.  E - hit
9.  A - hit
10. C - hit
11. E - hit

Miss rate: 6/11 = 54.5%

The hit rate improves with 1 set 4 ways
