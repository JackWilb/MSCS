Jack Wilburn
Assignment 2

1. Pipelining (40 points)  
An un-pipelined processor takes 14 ns to work on one instruction. It then takes 0.2 ns to latch its results into latches. I was able to create a new pipelined processor by converting the circuits into 8 sequential pipeline stages. The stages have the following lengths: 1.6ns; 1.8ns; 1.4ns; 1.9ns; 2.1ns; 0.9ns; 1.7ns; 2.6ns. Answer the following, assuming that there are no stalls in the pipeline.  
What are the cycle times in both processors?  
What are the clock speeds in both processors?  
What are the IPCs in both processors (averaged across millions of instructions and assuming no pipeline hazards)?  
How long does it take to finish one instruction in both processors (in nano-seconds and cycles)?
What is the speedup provided by the 8-stage pipeline?  
If I was able to build a magical 1000-stage pipeline, where each stage took an equal amount of time, what speedup would I get?   

    **ANSWER** 
    1. The total time per cycle for the un-pipelined processor is 14 + 0.2 = 14.2ns. The total time per cycle for the pipelined processor is the largest time we have to wait, plus the latch, 2.6 + 0.2 = 2.8ns.
    2. Clock speeds are: un-pipelined, 1 / 14.2ns = 70.4225 MHz; pipelined, 1 / 2.8ns = 357.143 MHz.
    3. Each processor is working through 1 instruction per cycle (when the pipeline has filled for the pipelined processor, with no hazards)
    4. It takes the un-pipelined processor 1 cycle to finish one instruction, or 14.2ns. The pipelined processor takes a little longer, 8 cycles or 22.4ns.
    5. The speed up is 357.143 MHz / 70.4225 MHz = 5.07
    6. In this ideal case, the pipelined processor would have a cycle time of (14ns / 1000) + 0.2ns = 0.214ns, a clock speed of 1 / 0.214ns = 4.673 Ghz, and a speedup of 4.673 Ghz / 70.4225 MHz = 66.35


2. Instructions in the 5-Stage Pipeline (20 points)  
What does a load instruction do in the ALU stage of the basic 5-stage pipeline?  
Provide two example instructions that do not write to registers.  
Provide an example instruction that writes to memory.  
Provide an example instruction that does not use the ALU stage of the pipeline.  
Provide an example instruction that does nothing in the DM stage of the pipeline.  
Specify the number of input registers used by the following instructions: ADD, LD, ST.   

    **ANSWER**  
    1. The load (LD) instruction is calculating the address to load in the ALU stage.
    2. A store (ST) does not write to registers and neither does a branch if zero (BRZ).
    3. The store (ST) instruction writes out a register to system memory.
    4. Branching (BRZ) does not use the ALU, the REG stage handles the logic for branching.
    5. The ADD instruction does nothing in the DM stage.
    6. ADD has 2 input registers and LD/ST have 2 input register each a register with a memory address and a register to read or write to.

3. Data Dependencies (40 points)  
Consider a basic 5-stage in-order pipeline similar to the one discussed in class. How many stall cycles are introduced between the following pairs of successive instructions (i) for a processor with no register bypassing and (ii) for a processor with full bypassing? Use pipeline diagrams for each case to show if/how the second instruction is stalled.  
Int-add, followed by a dependent Int-add  
Load, followed by a dependent Int-add  
Load, providing the data for a Store  
Int-add, providing the data for a Store  

    **ANSWER**  PoP = *, PoC = %
    1. No bypassing:
    IF      DR      AL      DM      R*W
            IF      DR      DR      D%R      AL      DM      RW

    2 stalls

    Bypassing:
    IF      DR      AL*      DM      RW
            IF      DR      %AL      DM      RW

    0 stalls

    2. No bypassing:
    IF      DR      AL      DM      R*W
            IF      DR      DR      D%R      AL      DM      RW

    2 stalls

    Bypassing:
    IF      DR      AL      DM*      RW
            IF      DR      DR      %AL      DM      RW

    1 stalls

    3. No bypassing:
    IF      DR      AL      DM      R*W
            IF      DR      DR      D%R      AL      DM      RW

    2 stalls

    Bypassing:
    IF      DR      AL      DM*      RW
            IF      DR      AL      %DM      RW

    0 stalls

    4. No bypassing:
    IF      DR      AL      DM      R*W
            IF      DR      DR      D%R      AL      DM      RW

    2 stalls

    Bypassing:
    IF      DR      AL*      DM      RW
            IF      DR      AL      %DM      RW

    0 stalls

    
 