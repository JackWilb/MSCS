Jack Wilburn
Assignment 1

1. Power and Energy (30 points)  
Consider a processor that runs at 2 GHz and 1.1 Volt. When running a given CPU-bound program, the processor consumes 110 W, of which 20 W is leakage. The program takes 50 seconds to execute. The processor is capable of running at different voltages and frequencies. Can you compute the following values: (i) The smallest time it takes to execute the program. (ii) The highest power to execute the program. (iii) The lowest energy to execute the program. Assumptions: The processor is capable of executing safely at voltages between 0.9 V to 1.2 V. Voltage and frequency follow a linear relationship (i.e., if voltage doubles, frequency doubles as well).  
**ANSWER**  
1. The smallest time it would take to complete the program would be when the processor is running at it's highest speed. That is the most GHz. The maximum GHz is 2 GHz * (1.2 volts / 1.1 volts) = 2.18 GHz. 2.18 GHz / 2.0 GHz is 1.09, a 9% increase in speed. The time it would take to complete the program is 50 sec / 1.09 = 45.871559 sec
2. From above, the highest possible frequency is 2.18 Ghz and the highest voltage is 1.2 volts. That's a 9% increase in voltage and frequency for a (1.09)^2 = 1.188, 18.8% increase in power consumption. This is likely just affecting the dynamic power, so (90 * 1.188) + 20 = 126.9 watts.
3. The lowest possible frequency is 2 GHz * (0.9 volts / 1.1 volts) = 1.64 GHz, and the lowest possible voltage is 0.9 volts. 0.9 / 1.1 is 0.82, an 18% decrease in power. Using DVFS we see that the total power reduction under this paradigm is (0.82)^2 = 0.669, a 33% reduction. Again, this is likely just for dynamic power so (90 * 0.669) + 20 = 80.3 watts.

2. Power and Energy (30 points)  
Consider a processor running at 3 GHz and 1 Volt. It executes a program that finishes in 100 seconds, while consuming 20 W leakage power and 80 W dynamic power. Let's call this the baseline. I'm able to engage DFS to scale down the frequency (and hence power) of the processor. But this usually causes the program to consume more processor energy than the baseline. The only way my processor can consume less energy than the baseline is if the program is highly memory-bound. The program is considered Y% memory-bound if Y% of the execution time in the baseline is spent accessing memory -- note that this portion of the execution time is unaffected by frequency scaling on the processor. What is the minimum value of Y such that operating at a frequency of 1.5 GHz causes the program to consume less processor energy than the baseline?  
**ANSWER**  
In the case that the processor is running at 3 GHz, the processor uses 100W of power at all times. In the case that it's at 1.5Ghz, it uses (80 * 0.5) + 20 = 60W of power at all times. The question is essentially asking, at which point is the slowness okay, because the reduction in power is so much, given that memory accesses take a constant amount of time. In the full speed case, the processor takes Y time in memory bound work and 1 - Y time in computation work, all at 100 watts. In the half speed case it takes Y time in memory bound work and 2 * (1 - Y) time in computational work, all at 60 watts. Using these equations, we can see where the break even point is by setting them equal.

100 * (Y + (1 - Y)) = 60 * (Y + 2(1 - Y))

Solving this equation yields Y = 1/3. The minimum value of Y such that operating at a frequency of 1.5 GHz causes the program to consume less processor energy than the baseline is 33.33. Thus if more than 1/3 of the time is spent accessing memory, the slower speed would be better for total energy consumption.


3. Sum of Execution Times (20 points)  
A 4-program benchmark suite has execution times as listed below for 3 different systems. Assume that System-A is the reference machine. How does the performance of system-C compare against that of system-B? Show this comparison for all three metrics (sum of execution times, sum of weighted execution times, and GM of execution times). Report the comparison in terms of speedup.

    |Program|P|Q|R|S|
    |-                               |-     |-    |-    |-  |
    |Exec times on System-A (seconds)|100   |120  |80   |400|
    |Exec times on System-B (seconds)|120   |80   |100  |300|
    |Exec times on System-C (seconds)|90    |110  |90   |500|

    **ANSWER**  
    System B:
    - sum of execution times: 120 + 80 + 100 + 300 = 600
    - sum of weighted execution times (using system A as reference):  = (120 / 100) + (80 / 120) + (100 / 80) + (300 / 400) = 3.86
    - GM of execution times = (120 * 80 * 100 * 300) ^ 0.25 = 130.27

    System C:
    - sum of execution times: 90 + 110 + 90 + 500 = 790
    - sum of weighted execution times (using system A as reference): (90 / 100) + (110 / 120) + (90 / 80) + (500 / 400) = 4.19
    - GM of execution times = (90 * 110 * 90 * 500) ^ 0.25 = 145.28

    Relative to C, B gives a speed up of SET: 1.31, SWET: 1.09, GM: 1.12.

4. Performance Equation (20 points)  
My new laptop has a clock speed that is 10% higher than my old laptop. I run the same five binaries on both machines. Each binary runs for roughly the same number of cycles on each machine. The IPCs of the binaries are listed in the table below. State a single number that is representative of the performance improvement provided by my new laptop.

    |Program           |P  |Q  |R  |S  |T  |
    |-                 |-  |-  |-  |-  |-  |
    |IPCs on old laptop|0.6|0.8|0.4|1.1|1.4|
    |IPCs on old laptop|0.7|0.6|0.3|1.1|1.5|

    **ANSWER**  
    Let's take the arithmetic mean of the IPC for each machine. That would be (0.6 + 0.8 + 0.4 + 1.1 + 1.4) / 4 = 1.075 for the old laptop and (0.7 + 0.6 + 0.3 + 1.1 + 1.5) / 4 = 1.05 for the new machine. Now we can multiply this by 1 for the old machine and 1.1 for the new machine to represent the 10% increase in clock speed. We get 1.075 for the old machine and 1.155 for the new machine. That's 1.155 / 1.075 = 1.074, a 7.4% speedup for the new machine vs. the old machine.
