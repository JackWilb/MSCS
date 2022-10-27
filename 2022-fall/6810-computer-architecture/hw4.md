Jack Wilburn
Assignment 4

1. Loop unrolling and SW pipelining (70 points)
    1. Show the schedule (what instruction issues in what cycle) for the default code. (15 points)
    2. How should the compiler order instructions to minimize stalls (without unrolling)(note that the execution of a NOP instruction is effectively a stall)? Show the schedule. How many cycles can you save per iteration, compared to the default schedule? (15 points)
    3. What is the minimum unroll degree to eliminate stall cycles? Show the schedule for the unrolled code. (20 points)
    4. Come up with a software-pipelined version of the code (no unrolling). Use appropriate register names and displacements in your code. When this code executes, will it experience any stalls? (20 points) 

    **ANSWER**  
    1. 1 - L.D F2, 0(R1) // Get w[i]  
       2 - L.D F4, 0(R2) // Get x[i]  
       3 - stall  
       4 - stall  
       5 - MUL.D F6, F2, F4 // Multiply two numbers  
       6 - stall  
       7 - stall  
       8 - stall  
       9 - stall  
       10 - stall  
       11 - S.D F6, 0(R1) // Store the result into w[i]  
       12 - DADDUI R1, R1, #-8 // Decrement R1  
       13 - DADDUI R2, R2, #-8 // Decrement R2   
       14 - BNE R1, R3, Loop // Check if we've reached the end of the loop  
       15 - NOP
    2. 1 - L.D F2, 0(R1) // Get w[i]  
       2 - L.D F4, 0(R2) // Get x[i]  
       3 - DADDUI R1, R1, #-8 // Decrement R1  
       4 - DADDUI R2, R2, #-8 // Decrement R2  
       5 - MUL.D F6, F2, F4 // Multiply two numbers  
       6 - stall  
       7 - stall  
       8 - stall  
       9 - stall   
       10 - BNE R1, R3, Loop // Check if we've reached the end of the loop  
       11 - S.D F6, 8(R1) // Store the result into w[i]  

       This saves 4 cycles.
    3. Attempt with 3:
       1 - L.D F2, 0(R1) // Get w[i]  
       2 - L.D F4, 0(R2) // Get x[i]  
       3 - L.D F6, -8(R1) // Get w[i - 1]  
       4 - L.D F8, -8(R2) // Get x[i - 1]  
       5 - L.D F10, -16(R1) // Get w[i - 2]  
       6 - L.D F12, -16(R2) // Get x[i - 2]  
       7 - MUL.D F18, F2, F4 // Multiply two numbers  
       8 - MUL.D F20, F6, F8 // Multiply two numbers  
       9 - MUL.D F22, F10, F12 // Multiply two numbers  
       10 - DADDUI R1, R1, #-24 // Decrement R1  
       11 - DADDUI R2, R2, #-24 // Decrement R2  
       12 - stall
       13 - S.D F18, 24(R1) // Store the result into w[i]  
       14 - S.D F20, 16(R1) // Store the result into w[i] 
       15 - BNE R1, R3, Loop // Check if we've reached the end of the loop  
       16 - S.D F24, 8(R1) // Store the result into w[i]

       I played with moving the timings around above, but as I moved things around I would still need to introduce stall cycles to make it work. It seems you're stealing instructions from further down the schedule that you need in order to give breathing room between instructions

    
       1 - L.D F2, 0(R1) // Get w[i]  
       2 - L.D F4, 0(R2) // Get x[i]  
       3 - L.D F6, -8(R1) // Get w[i - 1]  
       4 - L.D F8, -8(R2) // Get x[i - 1]  
       5 - L.D F10, -16(R1) // Get w[i - 2]  
       6 - L.D F12, -16(R2) // Get x[i - 2]  
       7 - L.D F14, -24(R1) // Get w[i - 3]  
       8 - L.D F16, -24(R2) // Get x[i - 3]  
       9 - MUL.D F18, F2, F4 // Multiply two numbers  
       10 - MUL.D F20, F6, F8 // Multiply two numbers  
       11 - MUL.D F22, F10, F12 // Multiply two numbers  
       12 - MUL.D F24, F14, F16 // Multiply two numbers  
       13 - DADDUI R1, R1, #-32 // Decrement R1  
       14 - DADDUI R2, R2, #-32 // Decrement R2  
       15 - S.D F18, 32(R1) // Store the result into w[i]  
       16 - S.D F20, 24(R1) // Store the result into w[i]  
       17 - S.D F22, 16(R1) // Store the result into w[i]  
       18 - BNE R1, R3, Loop // Check if we've reached the end of the loop  
       19 - S.D F24, 8(R1) // Store the result into w[i]  

       The minimum unroll degree for this set of instructions is 4.

    4. 1 - S.D F6, 16(R1) // Store the result into w[i] (16 offset)  
       2 - MUL.D F6, F2, F4 // Multiply two numbers  
       3 - L.D F2, 0(R1) // Get w[i]  
       4 - L.D F4, 8(R2) // Get x[i]  
       5 - DADDUI R1, R1, #-8 // Decrement R1  
       7 - BNE R2, R3, Loop // Check if we've reached the end of the loop  
       6 - DADDUI R2, R2, #-8 // Decrement R2   

       There will be no stalls in the above code. The mult to store is has 5 useful instructions between it. The load to mult has 4 useful instructions.

2. Branch predictors (30 points)  
    Consider the following tournament branch predictor that employs a selector with 64K entries (2-bit saturating counters). The selector picks a prediction out of either a global predictor (16-bit global history is XOR-ed with 16 bits of branch PC to index into a table of 3-bit saturating counters) or a local predictor (8 bits of branch PC index into level-1, 11 bits of local history from level-1 are concatenated with 4 other bits of branch PC to generate the index into level-2 that has 3-bit saturating counters). What is the total capacity of the entire branch prediction system?

    **ANSWER**  
    Selector: 64Kb * 2b = 128Kb  
    Global: 64Kb * 3b = 192Kb  
    Local: (2^8 * 11b) + (2^15 * 3b) = 101120b

    Adding this together gives approximately 422Kb of capacity.

    Note: I'm not confident in my local calculation, perhaps the 11b should be 15b, since the 11b are concatenated with 4b from the PC.

