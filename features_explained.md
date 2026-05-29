# Sirius NEXUS AI Processor Gen5: Complete Feature List and Descriptions

This document provides a comprehensive catalog of every feature in the Sirius NEXUS AI Processor Gen5, organized by functional category. Each feature is described in detail, including its purpose, implementation, performance impact, and how it integrates with other features. The descriptions are written to be accessible to both technical and non-technical readers, explaining not just what the feature does but why it matters.

---

## Section 1: Core Architecture Features

### 1.1 Unified Memory Address Space

The unified memory address space eliminates the traditional separation between DRAM, storage, and remote memory by mapping every byte of data into a single 128-bit address space. A programmer writing a load instruction does not need to know whether the target address is on the same blade, on a different blade in the same rack, or on a blade four racks away. The hardware automatically routes the request across the appropriate interconnect, waits for the response, and returns the data. This abstraction simplifies programming dramatically because developers no longer need to manage separate memory pools, file buffers, or network transfers. The operating system is not involved in most memory accesses; the hardware handles everything. For a database engine, this means a 100TB dataset can be mapped directly into memory, and queries access it with load instructions instead of read system calls. For distributed computing, this means processes on different blades can share data structures using ordinary pointers instead of message passing.

The unified address space is implemented through the segment tree, a hierarchical structure that maps virtual addresses to physical locations. The root segment covers the entire rack. Child segments represent individual blades, memory banks, processes, and allocation regions. The address translation hardware walks this tree in constant time per level, with a 128-entry TLB caching frequently used segments. When a load instruction targets an address that is not in the TLB, the hardware walks the segment tree, loading segment descriptors from a reserved region of physical memory. The walk takes 12 cycles for a 6-level tree, after which the address is translated and the access proceeds. The TLB is tagged with the owner identifier, so switching between processes does not require flushing the TLB.

### 1.2 Heterogeneous Core Complex

The heterogeneous core complex recognizes that no single core type is optimal for all workloads. The Sirius NEXUS processor therefore includes four specialized core types: Math cores optimized for vector and matrix operations, Logic cores optimized for branching and searching, System cores optimized for I/O and memory management, and Approximate Compute Units (ACUs) optimized for low-precision inference where small errors are acceptable. This division allows each core to be smaller, faster, and more power-efficient than a general-purpose core that tries to do everything.

The Math core complex contains 32,000 cores arranged in a grid on the interposer. Each Math core has 16 ALUs that can operate on 512-bit vectors, 64 vector registers, and 512KB of L1 cache. The ALUs can be partitioned into 16 32-bit lanes, 8 64-bit lanes, 4 128-bit lanes, 2 256-bit lanes, or 1 512-bit lane, depending on the instruction. This flexibility allows the Math core to efficiently process both packed SIMD data and scalar values. The Logic core complex contains 8,192 cores optimized for integer operations, with a neural branch predictor achieving 98 percent accuracy for AI workloads. The System core complex contains 800 cores running at 4 GHz, handling the operating system, interrupts, and memory management. The ACU complex contains 65,536 cores that can run at 8 times the speed of exact cores when 5 percent error is acceptable.

### 1.3 Optical Fabric Interconnect

The optical fabric interconnect connects blades into a single, cache-coherent shared-memory system using light instead of electricity. Each blade has 12 optical transceivers, each operating at 800 gigabits per second over a single fiber, for a total off-board bandwidth of 9.6 terabits per second. The fibers are connected to a passive backplane that routes signals between blades within the same rack, or to active optical switches for connections between racks. The optical link is memory-mapped: a load instruction to a remote address triggers the hardware to send a request across the optical fabric, wait 5 microseconds for the response, and return the data.

The optical transceiver uses coarse wavelength-division multiplexing with four wavelengths per fiber: 1270, 1290, 1310, and 1330 nanometers. Each wavelength carries 200 gigabits per second using PAM-4 modulation. The transceiver is implemented as a silicon photonic integrated circuit with micro-ring modulators for transmission and germanium photodetectors for reception. The laser source is external, mounted on the substrate next to the photonic chip. The directory cache on each blade tracks which blades have copies of each cache line, and the coherence protocol sends invalidation messages when a write occurs. This enables true shared-memory programming across the entire data center, something that is impossible with traditional message-passing clusters.

### 1.4 Rack-Scale Coherent Memory

The RACK_UNIFY instruction configures the entire rack as a single shared memory space, transforming up to 20 blades into one large shared-memory machine. After this instruction executes, every blade can access every memory location on every other blade using standard load and store instructions. The hardware directory cache routes requests to the blade that holds the data, and the coherence protocol maintains consistency across all blades. The programmer sees a single address space spanning the entire rack and does not need to manage communication explicitly.

For larger configurations, multiple racks can be connected using active optical switches. The switches have 256 ports and can route signals between racks with 1 microsecond of latency. Up to 256 racks can be connected, providing a total of 5,120 blades, 51.2 million Math cores, 10.5 million Logic cores, 655,000 ACU cores, 320 petabytes of HBM3e memory, and 512 petabytes of memory-mapped flash storage. The entire system appears as a single shared-memory computer, with the hardware managing all communication and coherence transparently. This scales to 65,536 blades using a hierarchical directory protocol, with the directory cache on each blade tracking local cache lines and a global directory tracking lines that are shared across racks.

### 1.5 Segment Tree Memory Protection

The segment tree memory protection replaces traditional page tables with a hierarchical capability-based system that is more secure and more flexible. Each segment descriptor is 128 bits and contains the segment type (data, code, I/O, or capability), size (from 4KB to 1 exabyte), base address, owner identifier, permissions (read, write, execute, create child, delegate, seal), and a pointer to child segments. The segment tree is stored in a reserved region of physical memory, with the root segment descriptor in a dedicated register that can only be written by the highest privilege level.

When a program accesses a memory address, the hardware walks the segment tree, checking permissions at each level. The walk uses the address bits as indices into segment tables at each level. For a 6-level tree, the walk takes 12 cycles if the segment descriptors are not in the TLB, or 2 cycles if they are cached. The TLB has 128 entries and is fully associative, tagged with the owner identifier. The owner hierarchy replaces traditional privilege rings: owner 0 is the hardware, owner 1 is the boot firmware, owner 2 is the hypervisor, owners 3-255 are virtual machine monitors, owners 256-4095 are operating systems, and owners 4096 and above are user processes.

Capability tokens are cryptographically signed messages that grant access to a specific segment. The CAPABILITY_GRANT instruction creates a token signed with the grantor's private key. The token contains the segment identifier, maximum permissions, and expiration time. The recipient uses CAPABILITY_ACCEPT to verify the signature and create a local segment mapping. Tokens can be transmitted over insecure channels because the signature prevents forgery. This eliminates entire classes of attacks: buffer overflows cannot access memory outside the segment because the hardware checks boundaries on every access, use-after-free cannot access freed memory because the segment tree marks freed segments as invalid, and Spectre attacks cannot read kernel memory because the speculative execution unit respects segment permissions.

---

## Section 2: Memory and Storage Features

### 2.1 ROMB Gen2 Optical Memory

ROMB Gen2 (Read-Only Memory Board, second generation) is a revolutionary optical memory that provides 1.5 terabytes of storage per stack with 0.95 nanosecond access latency and 3.2 terabytes per second bandwidth. Unlike DRAM, which has 100 nanosecond latency and requires refresh, or flash, which has 50 microsecond latency, ROMB Gen2 uses optical waveguides printed in glass with femtosecond lasers. Each bit is represented by the presence or absence of a waveguide segment. When reading, a laser pulse is sent through the row waveguide; if the waveguide is continuous (1 bit), the pulse reaches the detector; if there is a gap (0 bit), the pulse is blocked.

The ROMB Gen2 stack contains 128 planes, each with 1,048,576 rows and 1,048,576 columns. The address decoder selects the row using a tree of micro-ring resonators, then launches a 100 picosecond laser pulse. The pulse propagates at 0.2mm per picosecond, reaching the detector array at the far end. The detectors are germanium photodiodes with 50 picosecond response time, and the output is amplified and serialized onto optical fibers back to the memory controller. The entire read operation takes 0.95 nanoseconds from address to data.

ROMB Gen2 is ideal for storing AI model weights, which are read frequently but never change during inference. A 1.8 trillion parameter model at INT4 requires 900 gigabytes of storage, which fits entirely in one ROMB Gen2 stack. The 0.95 nanosecond access latency means the model weights can be read as fast as the compute cores can consume them, eliminating the memory bottleneck that plagues traditional systems. ROMB Gen2 is also used for system firmware, mathematical constants, fixed algorithms, and immutable database facts. The optical waveguides are written once during manufacturing and cannot be changed, which makes ROMB Gen2 tamper-proof and immune to malware.

### 2.2 Memory-Mapped NAND Flash

The MAP_STORAGE instruction assigns a range of physical memory addresses to NAND flash storage, making flash accessible via standard load and store instructions. After mapping, a load from the target address triggers a hardware flash read: the memory controller calculates which flash chip, block, page, and offset are needed, sends a read command to the flash chip, waits 50 microseconds for the page to be read, and transfers the requested data to the core. The operating system is not involved, there are no system calls, and there is no data copying.

The NAND flash array provides up to 200 terabytes of storage per blade, with the flash chips soldered directly to the motherboard substrate. The 100TB configuration uses eighty 1.28TB chips arranged on both sides of the substrate. The chips use 3D NAND technology with 128 layers of floating-gate transistors, providing a storage density of 10 gigabits per square millimeter. The read latency is 50 microseconds, the write latency is 500 microseconds, and the erase latency is 5 milliseconds. The helper cores in the HBM stacks handle the flash translation layer, maintaining a mapping from logical addresses to physical flash blocks using a log-structured merge tree.

Memory-mapped flash eliminates the traditional storage stack entirely. A database no longer needs a buffer pool or a storage engine; it simply maps its dataset into memory and accesses it with load instructions. A file system becomes unnecessary because files are just ranges of memory addresses. A program that reads a 100GB file does not need to call read() and wait for data to be copied from the page cache; it just loads from the mapped address and the hardware reads directly from flash. This reduces latency by a factor of 1,000 for random reads and improves throughput by a factor of 10 for sequential reads.

### 2.3 Hardware Compression Engine

The hardware compression engine is integrated into the memory controller and the Data Movement Engine, providing transparent compression of memory and storage. The engine uses a two-stage pipeline: first, a predictor transform applies delta or XOR encoding to the data; second, an entropy encoder (RLE, Huffman, or LZ77) compresses the residuals. The predictor adapts to the data type, using byte-lag for text, integer delta for timestamps, and XOR for floating-point values. The entropy encoder is selected automatically based on the distribution of the residuals, with a learned neural network predicting the best encoder for each block.

The compression engine achieves a 5:1 compression ratio for AI model weights, 8:1 for timestamps, 4:1 for text, and 2:1 for random data. The effective capacity of ROMB Gen2 increases from 1.5TB to 7.5TB for AI weights and from 1.5TB to 384TB for timestamps. The effective capacity of NAND flash increases from 100TB to 500TB for AI weights and from 100TB to 800TB for databases. The compression and decompression operate at the full memory bandwidth of 3.2 terabytes per second, adding only 6.95 watts of power consumption.

The compression engine also supports adaptive lag encoding, which detects segments of data that have consistent statistical properties and resets the predictor at segment boundaries. This is particularly effective for time-series data, where the pattern may change over time. The learned compression neural network (128 inputs, 32 hidden neurons, 6 outputs) predicts the optimal compression parameters based on recent access patterns, achieving 92 percent accuracy in predicting the best predictor mode and 95 percent accuracy in predicting the best entropy encoder.

### 2.4 HBM3e Main Memory

The HBM3e memory stacks provide 64 gigabytes of main memory per blade with 4 terabytes per second of bandwidth. Eight stacks are attached to the interposer around the perimeter of the core complex, each stack containing eight DRAM dies vertically interconnected with through-silicon vias, plus a base logic die with the memory controller and 32 helper cores. The memory controller includes a 32-entry command queue that reorders requests to maximize row hits, improving the row hit rate from 50 percent to 80 percent and reducing the average latency from 100 nanoseconds to 65 nanoseconds.

The helper cores run at 1 GHz and handle error correction, refresh management, and address translation for memory-mapped I/O. The error correction uses a Reed-Solomon code that can correct up to 8 bit errors per 256-byte block, with the helper cores computing the syndromes and correcting errors in the background. The refresh management ensures that all DRAM rows are refreshed within the 64 millisecond window, with the helper cores scheduling refreshes during idle periods to minimize impact on performance. The address translation for memory-mapped I/O allows I/O devices to be mapped into the address space, so that load and store instructions can access device registers directly.

The HBM3e stacks are positioned within 25mm of the Math cores, minimizing the distance that signals must travel. The 4 terabyte per second bandwidth is sufficient to feed all 32,000 Math cores simultaneously, assuming each core consumes 125 megabytes per second. The memory controller uses a quality-of-service scheduler that prioritizes loads over stores and critical loads over prefetches, ensuring that latency-sensitive operations are not delayed by bandwidth-heavy streaming operations.

### 2.5 Hardware Cache Coherence Directory

The hardware cache coherence directory tracks the location of every cache line in the system, enabling efficient shared-memory programming across up to 5,120 blades. The directory is implemented in the silicon interposer and contains 1 million entries, each storing the physical address, the MESI state (Modified, Exclusive, Shared, Invalid), and a 128-bit vector of sharers for local cores. For remote cache lines, the directory entry contains the blade identifier instead of the vector of sharers, with a separate remote table of 64,000 entries.

When a core reads a cache line, it sends a request to the directory. If the directory indicates the line is in Shared state, the directory returns the data from memory. If the line is in Exclusive or Modified state on another core, the directory forwards the request to that core, which supplies the data directly. When a core writes to a cache line, the directory sends invalidation messages to all sharers before allowing the write to proceed. The coherence protocol is implemented as a finite-state machine in the interposer, with a directory cache that stores recently used directory entries.

For remote accesses across the optical fabric, the directory uses wavelength-division multiplexing to send coherence messages in parallel. Each blade has its own wavelength for broadcasting coherence requests, and the directory is distributed across all blades using a hash of the memory address. This design scales to 65,536 blades, with coherence latency of 5 microseconds for remote accesses within the same rack and 10 microseconds for accesses across racks. The directory is the key enabler of the shared-memory programming model, allowing programmers to write parallel code without managing communication explicitly.

---

## Section 3: Compute Features

### 3.1 INT4 Inference Acceleration

The INT4 inference acceleration features are designed for quantized neural network inference, where model weights are stored in 4-bit integers instead of 16-bit or 32-bit floating-point. The INT4 cores use 4-bit multipliers implemented as lookup tables rather than full multipliers, reducing power consumption by a factor of 4 and increasing throughput by a factor of 4 compared to FP16. The MATMULI4 instruction uses a 64x64 systolic array to compute matrix multiplications in 64 cycles, achieving 4,096 multiply-add operations per cycle.

The SOFTMAXI4 instruction computes softmax on INT4 logits by dequantizing to FP16, computing the softmax in FP16, and quantizing back to INT4. The dequantization and quantization use learned scale factors per tensor, with the scale factor stored in a register and applied using a multiplier and shifter. The ATTENTIONI4 instruction computes scaled dot-product attention entirely in INT4, with FP16 used only for the softmax. The instruction takes six operands and completes in 125,000 cycles for a sequence length of 2048 and head dimension of 64, compared to 1,000,000 cycles for a software implementation.

The GELUI4 instruction uses a 16-entry lookup table to compute the GELU activation function in 1 cycle, with accuracy within 1 percent of the true GELU. The LAYERNORMI4 instruction computes layer normalization in 50 cycles for a 512-element vector, with the mean and variance computed in FP16 and the normalization and quantization performed in parallel. The RESIDUALI4 instruction adds residual connections in 5 cycles, with dequantization to FP16, addition, and quantization back to INT4. Together, these instructions enable the entire transformer inference pipeline to run in INT4, achieving 8 times the throughput of FP16 with less than 1 percent accuracy loss.

### 3.2 Approximate Compute Units (ACU)

The Approximate Compute Units (ACUs) are a novel feature that trades small accuracy losses for large speed gains in inference workloads. Each ACU core contains 8 approximate ALUs that implement multiplication by skipping carry propagation, with four selectable modes: Exact (0% error, 1x speed), Approx-1 (0.1% error, 2x speed), Approx-2 (1% error, 4x speed), and Approx-3 (5% error, 8x speed). The ACU chiplet contains 256 cores and is positioned alongside the Math cores on the interposer, with a balanced blade containing 256 ACU chiplets and 256 Math chiplets.

The ACU includes a confidence estimation unit that predicts the expected error for each operation based on the input values. The confidence estimation unit uses a small neural network with 16 inputs (the 4-bit values of the two operands), 8 hidden neurons, and 4 outputs (one per approximation mode). The network is trained online using the actual error rates, with weight updates performed by a dedicated training unit running in the background. For operations with low expected error, the ACU automatically uses faster approximation modes; for operations with high expected error, the ACU falls back to exact mode.

The ACU is ideal for deep neural network inference, where small errors in intermediate layers are imperceptible in the final output. For a 100-layer transformer, the first 20 layers might run in exact mode, the middle 60 layers in Approx-2 mode, and the last 20 layers in Approx-1 mode, achieving an overall speedup of 4x with less than 0.5 percent accuracy loss. The ACU can also be used for image processing, where 5 percent error is visually imperceptible, and for audio processing, where 1 percent error is inaudible. The built-in self-test characterizes the error rates of each approximate ALU at power-on, ensuring consistent behavior across different chips and operating conditions.

### 3.3 Posit Arithmetic Unit

The Posit arithmetic unit implements the Type-III unum number system, which has several advantages over IEEE 754 floating-point. Posits have tapered precision, meaning more bits near 1.0 where precision matters most, and fewer bits near extremes. They have no NaN or infinity; every bit pattern represents a valid number. They have larger dynamic range: a 32-bit posit has 10 times the dynamic range of a 32-bit float, and a 64-bit posit has 100 times the dynamic range of a 64-bit float. They also have higher accuracy: a 32-bit posit can represent values with the same accuracy as a 64-bit float for many operations.

The Posit unit implements addition, multiplication, fused multiply-add, and conversion to and from IEEE floats. The addition and multiplication latency is 3 cycles for 32-bit posits and 4 cycles for 64-bit posits, compared to 4 cycles for IEEE floats. The fused multiply-add latency is 4 cycles for 32-bit posits and 5 cycles for 64-bit posits. The conversion to and from IEEE floats takes 3 cycles for 32-bit and 4 cycles for 64-bit.

The Posit unit is particularly useful for scientific computing, where the larger dynamic range eliminates underflow and overflow issues. It is also useful for AI training, where the higher accuracy per bit allows using lower precision for the same accuracy. A model trained with 32-bit posits can achieve the same accuracy as a model trained with 64-bit floats, reducing memory bandwidth and storage requirements by half. The Posit unit is implemented as a custom design using TSMC's standard cell libraries, occupying 50 million transistors and consuming 1 watt of power.

### 3.4 Hardware Grammar Parsing Engine (HGPE)

The Hardware Grammar Parsing Engine (HGPE) is a dedicated accelerator for parsing structured data, accelerating JSON, XML, CSV, Protocol Buffers, source code, and network protocols by factors of 100 to 160,000. The HGPE contains 64 parallel parser units, each with a grammar memory of 1MB (up to 65,536 BNF rules), a 4K-entry parse stack, a 256-entry token buffer, and an AST builder that can allocate 16 million nodes. The parser units are connected to a common grammar memory and can operate independently on different segments of the input.

The HGPE takes a BNF grammar compiled to a pushdown automaton, then processes the input at up to 3.2 terabytes per second in parallel mode. The pattern matcher supports literal strings, character classes, ranges, wildcards, repetitions, alternations, and regular expressions, with hardware implementations for each pattern type. The AST builder allocates nodes in a dedicated memory region, linking them into a tree structure without software intervention.

The HGPE is programmable via the PARSE_DEFINE_GRAMMAR instruction, which compiles a BNF grammar into the hardware representation. The compiled grammar can be stored in ROMB Gen2 and loaded at boot. The PARSE instruction then processes input data, producing an AST in memory. The AST_WALK instruction traverses the AST with a visitor callback, and the AST_QUERY instruction extracts values using a path expression like "$.users[0].name". The HGPE reduces parsing time for a 1GB JSON file from 50 seconds to 0.0003 seconds, and reduces HTTP request parsing latency from 2 microseconds to 0.02 microseconds.

### 3.5 Learned Branch Predictor

The learned branch predictor uses a neural network to predict branch directions with 98 percent accuracy for AI workloads, compared to 85 percent for traditional predictors. The neural network has 64 inputs (the history of the last 64 branches, both global and local), 32 hidden neurons with ReLU activation, and 1 output neuron with sigmoid activation (0 for not taken, 1 for taken). The weights total 2,048 (64×32 + 32×1) stored as 16-bit fixed-point numbers, for a total of 4KB of weight storage.

The predictor is trained online using stochastic gradient descent with a learning rate of 0.01. The training runs in the background, updating weights every 1,000 branches to amortize overhead. The hardware implementation uses fixed-point arithmetic and can update all weights in 2 cycles (1,000 cycles per 1,000 branches, or 1 cycle per branch amortized). The inference is pipelined to complete in 2 cycles, overlapped with the fetch stage so that the prediction is available when the instruction is decoded.

The learned branch predictor also supports indirect branches, where the target address depends on a register value. For indirect branches, the network has 8 output neurons that index into a 256-entry target table, with the output selecting which target to use. The indirect branch predictor achieves 95 percent accuracy for virtual function calls and switch statements, compared to 60 percent for traditional predictors.

### 3.6 Variable-Precision Vector Units

The variable-precision vector units allow per-element precision control, so that different elements in the same vector can have different precisions. The precision mask register (PMR) is a 64-bit register per vector register, with each 2-bit field encoding precision: 00=INT4, 01=INT8, 10=FP16, 11=FP32. The PMR is loaded from memory or set by the SET_PRECISION instruction, and the vector ALU automatically adapts to the precision of each operand.

The variable-precision ALU can split its 512-bit datapath into 128×4-bit lanes, 64×8-bit lanes, 32×16-bit lanes, or 16×32-bit lanes, controlled by the precision mask. This allows mixed-precision matrices where the diagonal is high precision and off-diagonals are low precision, reducing memory bandwidth by 50 percent and increasing compute throughput by 30 percent for mixed-precision models.

The variable-precision feature is integrated with the Register Data Type Mapping (RDTM) feature, which sets the default precision for all registers. The SET_REG_TYPE instruction can override the default for individual registers, and the precision mask can specify different precisions for different elements of the same register. This provides fine-grained control over precision, allowing programmers to optimize accuracy and performance on a per-element basis.

### 3.7 Hardware Transactional Memory

Hardware Transactional Memory (HTM) allows programmers to write lock-free data structures without the complexity of manual lock-free algorithms. A transaction is a sequence of memory operations that either all commit or all abort. The XBEGIN instruction starts a transaction and specifies a fallback handler address. The XEND instruction commits the transaction, making all writes visible atomically. If a conflict occurs (another core writes to a location in the read set), the transaction aborts and execution jumps to the fallback handler.

The HTM uses the existing directory cache to track read and write sets, adding 2 bits per cache line to indicate whether the line is in the read set or write set. A 64KB transaction buffer stores speculative writes, allowing the transaction to be rolled back on abort. Conflict detection logic monitors external writes to lines in the read set, aborting the transaction if a conflict is detected. The transaction buffer can hold up to 64KB of speculative writes, which is sufficient for most critical sections.

HTM simplifies parallel programming by eliminating deadlocks and reducing the need for fine-grained locking. A hash table lookup that would require multiple locks can be wrapped in a transaction, and the hardware will automatically retry if there is contention. For a hash table with 64 threads, HTM achieves 25 times the throughput of fine-grained locking. The XTEST instruction tests whether the current core is in a transaction, allowing libraries to adapt their behavior based on whether they are called from within a transaction.

---

## Section 4: I/O and Interconnect Features

### 4.1 Data Movement Engine (DME)

The Data Movement Engine (DME) is a dedicated coprocessor that executes data movement programs without involving the System cores. The DME has 4KB of instruction memory and 32 64-bit data registers, and can execute programs that include LOAD, STORE, FILTER, SORT, AGGREGATE, FORMAT, SCATTER, and GATHER operations. A program is launched with the DME_EXEC instruction, and the DME runs independently, generating an interrupt when complete.

The DME can copy data between memory regions at the full memory bandwidth of 4 terabytes per second, with optional XOR for RAID or encryption. It can filter records by a predicate, keeping only those that match. It can sort data by a key using a hardware merge sort. It can aggregate data, computing sum, count, min, max, or average. It can convert data formats, such as from INT4 to FP16. It can scatter data to non-contiguous addresses or gather data from non-contiguous addresses.

The DME is programmable via a simple assembly language, with programs stored in ROMB Gen2 and loaded at boot. For example, a program to filter a database table and compute the average of a column would be: LOAD src, record_size; FILTER age > 30; AGGREGATE sum(salary), count(*); STORE dst. This program executes without any System core involvement, freeing the System cores for other tasks.

### 4.2 In-Memory Compute (IMC)

In-Memory Compute (IMC) pushes simple database operations into the memory controller helper cores, eliminating the need to move data to the CPU. The IMC instructions (MEM_SCAN, MEM_FILTER, MEM_AGGREGATE, MEM_BITMAP) are executed by the 32 helper cores in each HBM stack, directly on the data in DRAM. The helper cores run at 1 GHz and have 16KB of instruction memory and 16KB of data memory.

MEM_SCAN scans a range of memory for a pattern, returning the addresses where the pattern is found. MEM_FILTER filters records by a predicate, writing the matching records to a destination. MEM_AGGREGATE computes sum, count, min, max, or average of a column. MEM_BITMAP creates a bitmap of which records match a predicate, which can then be used for bitmap indexing.

IMC reduces the data movement for database operations by a factor of 10 to 100. A scan of 1GB of data that would take 20 milliseconds on the CPU takes 2 milliseconds with IMC, and the data never leaves the memory controller. The helper cores also handle the compression and decompression of data in memory, further reducing data movement.

### 4.3 Register Data Type Mapping (RDTM)

Register Data Type Mapping (RDTM) reduces instruction size by 42 percent by moving type and vector length information out of individual instructions and into configuration registers. A single SET_REG_MAP instruction configures the data type (INT4, INT8, INT16, INT32, INT64, FP16, FP32, or FP64) and vector length (128, 256, 512, or 1024 bits) for all subsequent instructions until changed. This design recognizes that most programs operate on the same data types for long periods, especially in AI workloads where entire inference runs use the same precision throughout.

The RDTM feature includes per-register overrides, allowing individual registers to have different types from the default. The SET_REG_TYPE instruction sets the type for a specific register, and the GET_REG_TYPE instruction retrieves the current type. The per-register overrides are stored in a table in memory pointed to by a control register, with each entry containing the type, vector length, rounding mode, and a valid bit.

RDTM reduces the average instruction size from 48 bits (6 bytes) to 28 bits (3.5 bytes), increasing L1 instruction cache capacity by 71 percent. For a tight loop that performs 1,000 FMA operations, the code size drops from 15,000 bytes to 8,006 bytes, a 47 percent reduction. The decode bandwidth doubles from 1 instruction per cycle to 2 instructions per cycle, increasing IPC by 15 percent.

### 4.4 Configurable I/O (Video and Audio)

The CFG_VIDEO and CFG_AUDIO instructions configure video and audio output tiles to read memory regions as framebuffers and audio buffers. The video output tile continuously scans a memory region and converts its contents to display signals (HDMI, DisplayPort, DVI, VGA, LVDS, or eDP). The instruction takes the framebuffer base address, width, height, color format (RGB888, RGB101010, RGBA8888, YUV422, YUV420, or monochrome), and refresh rate. Double-buffering mode configures a second framebuffer, with the tile alternating between the two buffers on each frame.

The audio output tile reads a circular buffer from memory and sends samples to a DAC. The instruction takes the circular buffer base address, buffer size, sample rate, bit depth, channel count, and channel mapping. The tile maintains a read pointer that advances as samples are consumed, generating an interrupt when the buffer is half-empty. Hardware-accelerated mixing allows multiple sources to write to different regions of the buffer, with the tile mixing them automatically.

The configurable I/O eliminates the need for separate graphics and audio drivers. A program can write pixels directly to the framebuffer memory region without making system calls, and the video output tile will display them at the next vertical blank. This reduces latency from microseconds to nanoseconds and simplifies the software stack.

---

## Section 5: Security Features

### 5.1 Capability-Based Security

Capability-based security replaces traditional page tables and privilege rings with a hierarchical system of cryptographic capabilities. Each memory segment has an owner and a set of permissions (read, write, execute, create child, delegate, seal). Access requires a capability token that is cryptographically signed by the segment owner. The token contains the segment identifier, maximum permissions, and expiration time, and is signed with the owner's private key.

The CAPABILITY_GRANT instruction creates a token, and the CAPABILITY_ACCEPT instruction verifies the token and creates a local segment mapping. Tokens can be transmitted over insecure channels because the signature prevents forgery. The hardware verifies the signature using the public key of the owner, which is stored in a protected register.

This model eliminates entire classes of attacks. A buffer overflow cannot be used to access memory outside the segment because the hardware checks the segment boundaries on every access. A use-after-free cannot access memory that has been freed because the segment tree marks freed segments as invalid. A Spectre attack cannot read kernel memory because the speculative execution unit respects the segment permissions. The capability tokens cannot be forged because they are cryptographically signed.

### 5.2 Speculative Execution Sandbox

The speculative execution sandbox isolates speculative execution into a separate "speculative domain," preventing Spectre-style attacks that leak information through side channels. Loads from unauthorized segments in speculative execution return a dummy value (zero) rather than the actual data. The dummy value is tagged with a SPEC bit in the register file, and any instruction using a SPEC register produces a SPEC result. Instructions that could leak information (stores, branches) check for SPEC inputs; if a SPEC value is used, the pipeline flushes and the speculation is rolled back.

The sandbox adds 2 bits per cache line to track speculative state (NORMAL, SPECULATIVE_READ, SPECULATIVE_WRITE). Speculative reads mark the cache line as SPECULATIVE_READ, and speculative writes create a copy in a speculative buffer. The sandbox has a performance overhead of only 2 percent for normal workloads, compared to 20-50 percent for software mitigations like LFENCE or retpoline.

### 5.3 Secure Boot and Measured Boot

Secure boot ensures that only signed software can run on the blade. The boot ROM contains a public key that is used to verify the digital signature of the second-stage bootloader. The second-stage bootloader verifies the signature of the operating system kernel. If any signature is invalid, the blade halts and lights a red LED. The signatures are created using the grantor's private key, which is stored in a hardware security module at the factory.

Measured boot extends secure boot by recording the measurements (hashes) of each stage of the boot process in the TPM (Trusted Platform Module). The measurements can be attested to a remote verifier, which can confirm that the blade is running the expected software. The TPM is integrated into the System core chiplet and has its own dedicated memory and processor.

The hardware root of trust is a small, immutable circuit that generates and stores cryptographic keys. The root of trust is implemented in the System core chiplet and is isolated from the rest of the chip by a hardware firewall. The root of trust generates the keys for secure boot, memory encryption, and network encryption. The keys are stored in a one-time programmable memory and cannot be read or modified by software.

---

## Section 6: Performance Summary

The Sirius NEXUS AI Processor Gen5 delivers 677,027 tokens per second for LLM inference (LLaMA-3 70B), which is 2,708 times faster than NVIDIA H100 (250 tokens per second). It consumes 240 watts, compared to 700 watts for H100, achieving 2,821 tokens per joule, which is 7,836 times more energy-efficient than H100 (0.36 tokens per joule). The cost per million tokens is $0.000018, which is 1,833 times cheaper than H100 ($0.033 per million tokens).

The JSON parsing speed is 50 gigabytes per second in sequential mode and 3.2 terabytes per second in parallel mode (64 parsers), compared to 0.02 gigabytes per second for Python JSON. The HTTP request parsing speed is 50 million requests per second, compared to 500,000 requests per second for nginx. The database index scan speed is 6 billion lookups per second, compared to 10 million lookups per second for traditional DRAM.

The effective memory capacity with compression is 12 terabytes for ROMB Gen2 (8:1 compression ratio for AI weights) and 800 terabytes for NAND flash (8:1 compression ratio for databases). The blade contains 149,120 cores (32,000 Math, 8,192 Logic, 3,200 System, 65,536 ACU) on a 200mm by 500mm board, consuming 240 watts. A 256-rack data center with 5,120 blades delivers 3.46 trillion tokens per second, 23,552 images per second for diffusion models, and 30.9 trillion database lookups per second.

The Sirius NEXUS AI Processor Gen5 is the most advanced computing platform ever designed. It is faster, more energy-efficient, more cost-effective, and more secure than any competing product. It is the foundation for the next decade of artificial intelligence.
