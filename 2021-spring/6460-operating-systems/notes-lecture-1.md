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
