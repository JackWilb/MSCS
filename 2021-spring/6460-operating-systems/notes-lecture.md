## What is an OS

- Interface between users and hardware
- Manages shared resources
    - Protects processes from one another
- Provides common services
    - fs, virt-memory, network, cpu
- Goals
    - convenient to use
    - efficient


## Userspace vs Kernelspace

Userspace
    Most programs

Kernelspace  
- Privileged access to abstracted resources (writing a file to disk, etc.)
    - A program could corrupt the disk, the privileged operators shouldn't


## OS Techniques

Abstraction

- Abstracting over physical resources
    - What interface do we give to applications?
- Called a virtualization
    - Input interface
    - Output interface
    - e.g. a thread is a virtualized cpu core
- Goal
    - Try to add no cost to the use of the physical hardware in the virtualization
- Challenges
    - What are the right mechanisms to virtualize safely?
        - How?
    - What are the right policies?
        - What/When?
    - What keeps programs from circumventing the safeguards? (using syscalls)


## Required C knowledge

- Doubly linked list
- Pointers to pointers


## Context Switching


## Process Management
PCB: Process control blocks


## Fork and Exec
Fork makes a copy of the currently running process.

Exec replaces the current running process with another.

Using them together can all you to run another program with a ton of config, changing user, piping output, etc.

Zombie process: Child called exit, but parent hasn't called wait to check the return code


## Scheduling
- Workload: set of job descriptions (arrival time, run time)
  - Job: View as current CPU burst of process 
  - Process alternates between CPU and I/O
  - Moves between ready and blocked queues
- Scheduler: Logic that decides which ready job to run
- Metric: Measurement of scheduling quality
    - Maybe fairness/responsiveness

Options:
- Minimize turnaround time
- Minimize response time
- Minimize waiting time
- Maximize throughput
- Maximize resource utilization
- Minimize overhead
- Maximize fairness

turnaround time = (completion_time - arrival_time)

FIFO scheduler - Optimizes turn around time (assuming no I/O, known + same run time, same arrival time). If we relax constraints, a long first process is bad for avg. turn around time (convoy effect).

SJF (shortest job first) - optimal if we relax same runtime constraint. If we relax same arrival time constraint, this is a problem because we can't deschedule the task.

STCF (shortest time to completion first) - deschedule long running tasks and run the shortest ones. This is optimal for average turnaround time, but run time is never known so we can't really do this.

Round Robin - Alternate processes between running and descheduled. Worst case for turnaround, best for response time.

## Preemptive scheduler
Allows for context switch. Usually uses timer interrupts.



