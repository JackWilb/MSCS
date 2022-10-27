Jack Wilburn
Assignment 3

1. Data Dependences (30 points)

    Consider a 32-bit in-order pipeline that has the following stages. Note the many differences from the examples in class: a stage that converts CISC instructions to micro-ops, one stage to do register reads, one stage to do register writes, four stages to access the data memory, and three stages for the FP-ALU. For the questions below, assume that each CISC instruction is simple and is converted to a single micro-op.

    Fetch 	uOp Convert 	Decode 	Regread 	IntALU 	Regwrite
    IntALU 	Datamem1 	Datamem2 	Datamem3 	Datamem4 	Regwrite
    FPALU1 	FPALU2 	FPALU3 	Regwrite

    After instruction fetch, the instruction goes through the micro-op conversion stage, a Decode stage where dependences are analyzed, and a Regread stage where input operands are read from the register file. After this, an instruction takes one of three possible paths. Int-adds go through the stages labeled "IntALU" and "Regwrite". Loads/stores go through the stages labeled "IntALU", "Datamem1", "Datamem2", "Datamem3", "Datamem4", and "Regwrite". FP-adds go through the stages labeled "FPALU1", "FPALU2", "FPALU3", and "Regwrite". Assume that the register file has an infinite number of write ports so stalls are never introduced because of structural hazards. How many stall cycles are introduced between the following pairs of successive instructions (i) for a processor with no register bypassing and (ii) for a processor with full bypassing?

    1. Int-add, followed by a dependent Int-add
    2. Load, followed by a dependent FP-add
    3. Load, providing the address operand for a store
    4. FP-add, providing the data operand for a store  

    
    **ANSWER**  
    1.
    
    No bypassing:
    ```
    FE  uO  DE  RR  AL  RW*  
        FE  uO  DE  DE  DE  %RR  AL RW
    ```

    2 stall cycles

    Bypassing:
    ```
    FE  uO  DE  RR  AL*  RW
        FE  uO  DE  RR  %AL  RW
    ```
    No stall cycle  
    2.
    
    No bypassing:
    ```
    FE  uO  DE  RR  AL  DM1 DM2 DM3 DM4 RW*
        FE  uO  DE  DE  DE  DE  DE  DE  DE  %RR  FA1 FA2 FA3 RW
    ```

    6 stall cycles

    Bypassing:
    ```
    FE  uO  DE  RR  AL  DM1 DM2 DM3 DM4* RW
        FE  uO  DE  DE  DE  DE  DE  RR  %FA1 FA2 FA3 RW
    ```

    4 stall cycles  
    3.
    
    No bypassing:
    ```
    FE  uO  DE  RR  AL  DM1 DM2 DM3 DM4 RW*
        FE  uO  DE  DE  DE  DE  DE  DE  DE  %RR  AL  DM1 DM2 DM3 DM4 RW*
    ```

    6 stall cycles

    Bypassing:
    ```
    FE  uO  DE  RR  AL  DM1 DM2 DM3 DM4* RW
        FE  uO  DE  DE  DE  DE  RR  AL  %DM1 DM2 DM3 DM4 RW
    ```

    3 stall cycles  
    4.
    
    No bypassing:
    ```
    FE  uO  DE  RR  FA1 FA2 FA3 RW*
        FE  uO  DE  DE  DE  DE  DE  %RR  AL  DM1 DM2 DM3 DM4* RW
    ```

    4 stall cycles

    Bypassing:
    ```
    FE  uO  DE  RR  FA1 FA2 FA3* RW
        FE  uO  DE  DE  RR  AL  %DM1 DM2 DM3 DM4* RW
    ```

    1 stall cycle


2. Branch delay slot and stalls (30 points)

    Consider the following skeletal code segment, where the branch is taken 90% of the time and not-taken 10% of the time.

    Consider a 10-stage in-order processor, where the instruction is fetched in the first stage, and the branch outcome is known after three stages. Estimate the average CPI of the processor under the following scenarios (assume that all stalls in the processor are branch-related and branches account for 15% of all executed instructions):
    On every branch, fetch is stalled until the branch outcome is known.
    Every branch is predicted not-taken and the mis-fetched instructions are squashed if the branch is taken.
    The processor has two delay slots and the two instructions following the branch are always fetched and executed, and
    You are unable to find any instructions to fill the delay slots.
    You are able to move two instructions before the branch into the delay slots.
    You are able to move two instructions from the taken block into the delay slots.
    You are able to move two instructions from the not-taken block into the delay slots. 

    **ANSWER**  
    1. In this case, the processor will stall for 2 cycles while it calculates the branch result. This happens 15 % of the time so the slowdown would go from 1 to (1 + (0.15 * 2)) = 1.3 cpi. 
    2. In this case, the processor does work that is not useful 90% of the time after the branch. That's the equivalent of 2 stall cycles 90% of the time we see a branch. Thus CPI would be reduced from 1 to (1 + (0.15 * 2 * 0.9)) = 1.27 cpi. 
    3. 
        1. This is case 1 above. 1.3 CPI
        2. In this case, there is no stalls while waiting for the branch. The CPI remains 1.
        3. In this case, you stall only 10% of the time. Thus the CPI is (1 + (0.15 * 2 * 0.1)) = 1.03 cpi
        4. In this case, you stall 90% of the time. Thus the CPI is (1 + (0.15 * 2 * 0.9)) = 1.27 cpi


3. Deep Pipelines (40 points)

    Consider an unpipelined processor where it takes 8ns to go through the circuits and 0.2ns for the latch overhead. Assume that the Point of Production and Point of Consumption in the unpipelined processor are separated by 4ns. Assume that one-third of all instructions do not introduce a data hazard and two-thirds of all instructions depend on their preceding instruction. What is the throughput of the processor (in BIPS) for (i) an unpipelined processor, (ii) a 10-stage pipeline, and (iii) a 20-stage pipeline. 

    **ANSWER**  
    1. 1 instruction every 8.2ns, 0.12 BIPS.
    2. No hazard: 0.8ns + 0.2ns = 1ns. Hazard: (4ns / 0.8ns) * 1ns = 5ns. (1/3 * 1ns) + (2/3 * 5ns) = 3.66ns. 0.27 BIPS
    3. No hazard: 0.4ns + 0.2ns = 0.6ns. Hazard: (4ns / 0.4ns) * 0.6ns = 6ns. (1/3 * 0.6ns) + (2/3 * 6ns) = 4.2ns.  0.24 BIPS
