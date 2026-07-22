# Operating Systems

An operating system (OS) is software that manages computer hardware and provides services for running application programs. It acts as an intermediary between users and the hardware, handling resource allocation, process management, memory management, and I/O operations.

## Processes and Threads

A process is an instance of a running program with its own memory space, program counter, registers, and resources. Each process has a Process Control Block (PCB) that stores its state information. Processes are isolated from each other — one process cannot directly access another's memory.

A thread is a lightweight unit of execution within a process. Threads within the same process share memory and resources, making inter-thread communication faster but also introducing synchronization challenges. Context switching between threads is cheaper than between processes because threads share the address space.

Multithreading allows concurrent execution within a single process. Common threading models include user-level threads (managed by the application) and kernel-level threads (managed by the OS). Most modern systems use a hybrid approach.

## Process Scheduling

The CPU scheduler determines which process runs next. Scheduling algorithms include:

- **First-Come, First-Served (FCFS)**: Simple queue, can cause convoy effect where short processes wait behind long ones.
- **Shortest Job First (SJF)**: Minimizes average waiting time but requires knowledge of burst times.
- **Round Robin (RR)**: Each process gets a fixed time quantum. Good for interactive systems.
- **Priority Scheduling**: Processes assigned priorities. Risk of starvation for low-priority processes, mitigated by aging.
- **Multilevel Queue**: Multiple queues with different scheduling algorithms for different process types.

## Memory Management

The OS manages both physical and virtual memory. Key concepts include:

**Virtual Memory** allows processes to use more memory than physically available by using disk space as an extension of RAM. Each process has a virtual address space that is mapped to physical memory through page tables. The Memory Management Unit (MMU) handles address translation.

**Paging** divides memory into fixed-size blocks called pages (typically 4KB). The page table maps virtual pages to physical frames. When a process accesses a page not in physical memory, a page fault occurs, and the OS loads the page from disk.

**Page Replacement Algorithms** decide which page to evict when physical memory is full. Common algorithms include FIFO (first in, first out), LRU (least recently used), and Optimal (evict the page that won't be used for the longest time — theoretical, used as a benchmark).

**Segmentation** divides memory into variable-sized segments based on logical divisions (code segment, data segment, stack segment). Modern systems often combine paging and segmentation.

## Synchronization

When multiple threads access shared resources, synchronization mechanisms prevent race conditions:

- **Mutex (Mutual Exclusion)**: A lock that only one thread can hold at a time.
- **Semaphore**: A counter that controls access to a resource. Binary semaphores are similar to mutexes. Counting semaphores allow a fixed number of concurrent accesses.
- **Monitor**: A high-level synchronization construct that encapsulates shared data and operations.
- **Deadlock**: Occurs when processes are waiting for resources held by each other. Four conditions must hold simultaneously: mutual exclusion, hold and wait, no preemption, and circular wait.

## File Systems

File systems organize data on storage devices. Common file systems include NTFS (Windows), ext4 (Linux), and APFS (macOS). Key concepts include inodes (metadata about files), directory structures, and journaling (recording changes before applying them to prevent corruption during crashes). File allocation strategies include contiguous allocation, linked allocation, and indexed allocation.
