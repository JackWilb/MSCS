Jack Wilburn
Assignment 9

1. Consistency Models (40 points)

For the multi-threaded program below, what are all the valid outputs (printed value of A) for a sequentially consistent execution of the program? Before these threads start executing, A and B are both initialized to zero. Assume that each line of code below corresponds to one assembly instruction.

Thread 1              instruction name
B = 100;              A
A = 150;              B

Thread 2              instruction name
if ((B+A) > 80)       a
then A = A - B;       b
print A;              c

For a sequentially consistent execution of the program, there are 10 possible outcomes. Let's explore them all:

ABabc = 50 (if is true)
AaBbc = 50 (if is true)
AabBc = 150 (if is true)
AabcB = -100 (if is true)
aABbc = 150 (if is false)
aAbBc = 150 (if is false)
aAbcB = 0 (if is false)
abABc = 150 (if is false)
abAcB = 0 (if is false)
abcAB = 0 (if is false)

The possible outcomes are -100, 0, 50, and 150


What are possible valid outputs if the code in each thread is encapsulated within lock and unlock statements as shown below (again assuming a sequentially consistent processor)?

Thread 1
lock (L1);
B = 100;
A = 150;
unlock (L1);

Thread 2
lock (L1);
if ((B+A) > 80)
then A = A - B;
print A;
unlock (L1);

If the code in each thread is encapsulated within lock and unlock statements, then the possible outputs for the value of A in a sequentially consistent execution of the program are 50 and 0.

The possible ordering of the instructions are just the threads in different orders, thanks to the locks. That means we can execute the following patterns to get the following outcomes:

T1,T2 = 50
T2,T1 = 0

2. Consistency Models (20 points)

We discussed in class that high-performance techniques like out-of-order scheduling can yield unintuitive/unexpected outputs in multi-threaded programs written with a sequentially consistent model. We ultimately had a solution (a relaxed consistency model) that offered a relatively simple programming model and relatively high performance. To achieve this solution, briefly summarize what the programmer has to do, and what the hardware designer has to do.

The programmer must use a relaxed consistency model, which allows for the possibility of different threads seeing different versions of shared data at different times. This can be achieved by using special memory operations and synchronization instructions, such as LL-SC or compare-and-swap, which allow threads to update shared data in a way that is visible to other threads in a controlled and predictable manner. The hardware designer must design the processor to support these special memory operations and synchronization instructions, and to execute them in a way that maintains the integrity of the shared data and ensures that the results of the program are consistent with the relaxed consistency model. They must also ensure that if the instructions are executed out of order, that they respect the sequential commits to the register file.

3. Synchronization (20 points)

Briefly describe how LL-SC works by answering the following: 

i. What happens when the LL instruction is executed? 
ii. What happens when the SC instruction is executed?
iii. What is the benefit of using LL-SC instead of test-and-test-and-set?


LL-SC instructions are a synchronization mechanism used to implement atomic operations in parallel computing. When the LL instruction is executed, it loads a memory location into a register in the CPU and records the memory address in a special LL/SC tag. The tag is a simple binary bit that tells the CPU if the data has already been modified since the LL instruction. When the SC instruction is executed, the tag is checked and the the CPU either executes the store or discards the instruction. In the case that the tag has been modified, the code is usually retried until the whole block of instructions run as one atomic operation. One benefit of using LL-SC instead of test-and-test-and-set is that it can potentially reduce the number of retries needed to complete an atomic operation. This can improve the performance of parallel programs that use atomic operations extensively.

4. Networking (10 points)

Why is the West-First routing algorithm better than Dimension-Order routing and Fully Adaptive routing?

In general, West-First routing is a simple and efficient routing algorithm that is often used in two-dimensional mesh networks. It works by routing packets from the source to the destination along the westward direction first. This guarantees that there won't be any deadlocks in the routing. Dimension-Order routing is also deadlock free, fully adaptive routing, gives no such guarantees. This is the main benefit of West-First routing vs. Fully Adaptive routing. Dimension-Order routing is similiar to West-First routing, but is inferior, because it slightly less flexible. It has 4 of the 8 possible turns disabled. This leads to less flexibility when we want to do a hybrid adaptive routing paradigm.

5. Networking (10 points)

I'm trying to design a network topology for a system with 64 nodes. If my choices are a torus topology or a hypercube topology, what are the trade-offs that should guide my decision? 

When comparing a torus topology and a hypercube topology for a network with 64 nodes, there are a few key trade-offs to consider. One trade-off is the cost and complexity of the network. In general, a hypercube topology will require more links and hardware than a torus topology with the same number of nodes. This can make a hypercube more expensive and harder to implement and maintain. This trade off in links and hardware is made up for by improved performance and shorter paths between nodes. Ultimately, the decision between a torus and a hypercube topology will depend on the specific needs and constraints of the system. It may be useful to consider factors such as the required performance, cost, and flexibility of the network when making this decision.
