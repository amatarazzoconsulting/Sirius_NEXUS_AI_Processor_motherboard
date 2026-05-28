# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference
## By Anthony Matarazzo (c) 2026

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 1: Data Movement Instructions

### 1.1 MOV – Move Data

The MOV instruction is the most frequently executed instruction in any program. It transfers data from a source operand to a destination operand without modifying the source. The operation is conceptually simple, but the PIP CISC implementation includes sophisticated features for handling different data sizes, alignment conditions, and memory types including DRAM, flash, and remote memory.

**Encoding Format**

The MOV instruction uses opcode 0x01. The instruction header occupies the first 20 bits, with the opcode in bits 0-7, flags in bits 8-15, and operand count in bits 16-19. For a standard MOV with two operands, the operand count field is set to 2. The first operand descriptor follows the header and specifies the destination. The second operand descriptor specifies the source. If either operand is an immediate value, the payload containing that value follows the operand descriptors.

The flags field for MOV has special meaning. Bit 8, when set, indicates that the move is non-temporal, meaning that the data should not be cached. This is useful for streaming data that will be used only once, as it prevents cache pollution. Bit 9, when set, indicates that the move should use the largest available data path, up to 512 bits, regardless of the operand size. This allows the hardware to optimize bandwidth by moving data in larger chunks than the programmer requested. Bits 10-15 are reserved for future use.

The operand descriptor for a register operand uses type 0. The register number is stored in bits 9-15 of the descriptor, allowing access to any of the 32 general-purpose registers in a Math core, 32 registers in a Logic core, or 64 registers in a System core. The element size field in bits 4-6 specifies the width of the data being moved, from 8 bits to 512 bits. Moving a 512-bit value between registers uses a single instruction but may take multiple cycles depending on the data path width of the specific core implementation.

The operand descriptor for a memory operand uses type 1. The addressing mode is stored in bits 9-12, with mode 0 indicating direct addressing, mode 1 indicating base-plus-offset, mode 2 indicating base-plus-index, and mode 3 indicating base-plus-index-times-scale. The remaining bits specify which registers hold the base address, index, and scale factor. The memory address is computed by the address generation unit in parallel with instruction decode, adding zero latency to the instruction execution when the address is already in a register.

The operand descriptor for an immediate operand uses type 2. The size field specifies the width of the immediate value, and the value itself is stored in the payload section following the operand descriptors. Immediate values can be as small as 8 bits or as large as 512 bits. A 512-bit immediate value occupies 64 bytes of instruction stream space, which is large but useful for loading constants that would otherwise require multiple instructions to construct.

The operand descriptor for a remote memory operand uses type 4, a special case of memory addressing. The remote blade identifier is stored in bits 9-20, providing 12 bits of blade address sufficient for 4,096 blades in a unified system. The remaining bits specify the memory address on that blade using the same addressing modes as local memory. The hardware automatically routes the move request across the optical fabric, waits for the response, and completes the operation without software intervention.

**Operation Details**

When the MOV instruction executes, the following steps occur in order. The source operand is read from its location. For register sources, the value is available in the same cycle. For memory sources, the address generation unit computes the effective address, then the memory controller initiates a read. For local DRAM, the read takes approximately 100 nanoseconds. For remote memory on another blade, the read takes approximately 5 microseconds for the round trip across the optical fabric plus directory lookup. For flash memory, the read takes approximately 50 microseconds while the NAND chip reads the page into its buffer.

While the source is being fetched, the destination address is computed in parallel. For register destinations, no address computation is needed. For memory destinations, the address generation unit computes the effective address and checks the segment tree permissions to ensure that the destination is writable by the current owner. If the permission check fails, the instruction raises a protection fault before any data is transferred, preventing partial writes.

When the source data arrives, it is held in a temporary buffer while the destination is prepared. For register destinations, the data is written directly into the register file. The write port of the register file can accept one value per cycle, so MOV instructions that target registers can complete at a rate of one per cycle. For memory destinations, the data is written to the write buffer, which accumulates writes and sends them to memory in bursts. The MOV instruction completes as soon as the data is in the write buffer, allowing subsequent instructions to execute while the write proceeds in the background.

The MOV instruction updates no condition flags. This is intentional, because moving data should not affect the state of the arithmetic flags. A programmer who needs to test whether a value is zero after a move must use a separate TEST instruction. This separation of concerns simplifies the processor design because the MOV instruction does not need to wait for flag updates before retiring.

**Assembly Examples**

Example 1: Move between registers
```assembly
MOV R1, R2    ; Copy contents of register R2 into register R1
```

This instruction copies 32 bits from R2 to R1. The source and destination are both registers, so the operation completes in a single cycle. The original value in R2 is unchanged. This is the most common form of the MOV instruction and is used for almost every data transfer within a function.

Example 2: Move immediate value
```assembly
MOV R1, #42   ; Load the constant value 42 into register R1
```

The immediate value 42 is encoded in the instruction payload. For small constants like 42, the immediate fits in 8 bits and the instruction payload is only one byte. For larger constants, the payload size increases accordingly. The assembler automatically selects the smallest encoding that can represent the constant.

Example 3: Move from memory
```assembly
MOV R1, [R2]  ; Load the value at the memory address in R2 into R1
```

The memory address is computed as the contents of R2. This is a direct memory access, also known as a load. The memory controller reads 32 bits from that address and returns them to R1. The latency depends on whether the data is in cache, DRAM, or remote memory.

Example 4: Move to memory
```assembly
MOV [R1], R2  ; Store the value in R2 to the memory address in R1
```

This is a store operation. The value in R2 is written to the memory address computed from R1. The write is buffered, so the instruction completes quickly, but the actual write to memory may take many cycles. Subsequent loads to the same address will see the new value because the load checks the write buffer before going to memory.

Example 5: Move with base plus offset
```assembly
MOV R1, [R2 + 64]  ; Load from address R2 plus 64 bytes
```

The address generation unit adds the constant 64 to the value in R2 before sending the request to memory. This is useful for accessing fields within a structure, where the base address is in a register and the field offset is a compile-time constant. The constant is encoded in the operand descriptor, not in a separate payload, making the instruction compact.

Example 6: Move with index scaling
```assembly
MOV R1, [R2 + R3*8]  ; Load from address R2 plus R3 times 8
```

The index scaling mode multiplies the index register by 1, 2, 4, or 8 before adding to the base address. This is essential for array access, where the index is the element number and the scale is the element size. For an array of 64-bit integers, the scale is 8. This addressing mode computes the element address in a single instruction, eliminating the need for separate multiply and add instructions.

Example 7: Non-temporal move
```assembly
MOV.NT [R1], R2  ; Store with non-temporal hint, bypassing cache
```

The .NT suffix sets bit 8 of the flags field, indicating that the data should not be cached. The memory controller writes directly to DRAM without allocating a cache line. This is useful for streaming writes where the data will not be read again soon, because it prevents the cache from being polluted with data that will be evicted before it can be reused.

Example 8: Move to remote blade
```assembly
MOV @4:0x10000, R1  ; Move R1 to blade 4, address 0x10000
```

The @ symbol indicates a remote memory operand. The number before the colon is the blade identifier. The address after the colon is the memory address on that blade. The hardware sends a write request across the optical fabric to blade 4. The instruction completes when the write buffer on the local blade accepts the request; the actual write on the remote blade happens asynchronously.

Example 9: Move from remote blade
```assembly
MOV R1, @4:0x10000  ; Load from blade 4, address 0x10000 into R1
```

This instruction reads from remote memory. The hardware sends a read request to blade 4, which responds with the data. The requesting core stalls until the data arrives, which takes approximately 5 microseconds. During this stall, other cores on the same blade continue executing, and the stalled core consumes no power beyond leakage.

Example 10: Move from memory-mapped flash
```assembly
MOV R1, [0x100000000]  ; Load from flash address 0x100000000
```

The memory address 0x100000000 is in a region that has been mapped to flash storage by a previous MAP_STORAGE instruction. The memory controller detects that this address is in a flash region and sends a read command to the appropriate flash chip. The instruction stalls for approximately 50 microseconds while the flash chip reads the page. This is slow but still faster than a traditional file read, which would require an operating system call and data copying.

---

### 1.2 MOVSX – Move with Sign Extension

The MOVSX instruction moves a smaller signed integer into a larger register while preserving the sign of the value. When a signed 8-bit integer with value -1 (binary 0xFF) is moved into a 32-bit register, the result should be -1 (binary 0xFFFFFFFF). Sign extension fills the upper bits with copies of the most significant bit of the source value, ensuring that the numeric value remains the same after widening.

**Encoding Format**

MOVSX uses opcode 0x02. The instruction header is identical to MOV, with the opcode field set to 0x02. The operand count is always 2. The first operand descriptor specifies the destination, which must be a register. The second operand descriptor specifies the source, which can be a register, memory, or immediate. The source size must be smaller than the destination size. If the source and destination are the same size, the assembler should use MOV instead, because sign extension is unnecessary.

The flags field for MOVSX has bit 8 reserved for a special operation. When bit 8 is set, the instruction performs saturating sign extension. If the source value is too large to be represented in the destination size after extension, the result is clamped to the maximum or minimum representable value. This is useful for graphics and audio processing where overflow is undesirable. Bits 9-15 are reserved.

The destination descriptor must specify a register operand with type 0. The size field in bits 4-6 indicates the destination width. Valid sizes are 16, 32, 64, 128, 256, and 512 bits. The source descriptor can specify a register, memory, or immediate operand, but its size field must be smaller than the destination size. The source size can be 8, 16, 32, 64, or 128 bits, provided it is strictly less than the destination size.

**Operation Details**

When MOVSX executes, the first step is to read the source value. For an 8-bit source, the hardware reads a single byte. For a 16-bit source, it reads two bytes. The source value is then sign-extended to the destination width. Sign extension works by examining the most significant bit of the source value. If that bit is 1, indicating a negative number in two's complement representation, all additional bits in the destination are set to 1. If the most significant bit is 0, all additional bits are set to 0.

The sign extension logic is implemented as a combinational circuit that operates in a single cycle. The source value is fed into a shifter that replicates the most significant bit across the upper positions. The shifter width is parameterized by the source and destination sizes, allowing the same hardware to handle any combination. For a 8-bit source being extended to 512 bits, the shifter replicates the top bit across 504 positions, which is a wide but fast operation.

After sign extension, the result is written to the destination register. The write occurs in the same cycle as the extension, so the entire MOVSX instruction takes one cycle after the source is available. If the source is in memory, the memory access latency dominates. If the source is in another register, the instruction completes in one cycle. This makes MOVSX essentially free when used with register sources.

**Assembly Examples**

Example 1: Sign extend 8-bit to 32-bit
```assembly
MOVSX R1, R2  ; R2 contains 8-bit signed value, extend to 32-bit in R1
```

If R2 contains 0xFF (which is -1 in 8-bit signed), R1 becomes 0xFFFFFFFF (also -1). If R2 contains 0x7F (127), R1 becomes 0x0000007F (still 127). The sign extension preserves the numeric value.

Example 2: Sign extend from memory
```assembly
MOVSX R1, [R2]  ; Load byte from address in R2, sign extend to 32-bit
```

This instruction loads a single byte from memory, sign extends it to 32 bits, and stores the result in R1. This is common when processing strings or byte arrays where values are stored as signed 8-bit integers but need to be used in 32-bit arithmetic.

Example 3: Sign extend 16-bit to 64-bit
```assembly
MOVSX R1, R2  ; R2 contains 16-bit signed value, extend to 64-bit
```

The source register R2 is read as 16 bits, ignoring the upper 48 bits of the register. This allows a 16-bit value to be stored in a 64-bit register without taking extra space. The sign extension fills the upper 48 bits with copies of bit 15 of the source.

Example 4: Sign extend with saturation
```assembly
MOVSX.S R1, R2  ; Saturating sign extend from 8-bit to 32-bit
```

The .S suffix sets bit 8 of the flags field. If R2 contains 0x80 (-128 in 8-bit signed), the result in 32-bit would also be -128 (0xFFFFFF80), which fits. If R2 contained a value that would overflow after extension, which cannot happen because extension never changes the numeric value, the saturating mode would clamp. This instruction is included for symmetry with the unsigned version.

Example 5: Sign extend from immediate
```assembly
MOVSX R1, #-42  ; Sign extend immediate value -42 to 32-bit
```

The immediate value -42 is stored in the instruction payload as an 8-bit signed value. The MOVSX instruction sign extends it to 32 bits and loads it into R1. This is equivalent to MOV R1, #-42 but uses a smaller instruction encoding when the constant fits in a smaller size.

Example 6: Chain of sign extensions
```assembly
MOVSX R1, R2    ; Extend 8-bit to 16-bit in R1
MOVSX R3, R1    ; Extend 16-bit to 32-bit in R3
```

This sequence extends an 8-bit value to 32 bits using two MOVSX instructions. The intermediate 16-bit value in R1 is never used elsewhere. The compiler could combine these into a single MOVSX from 8-bit to 32-bit, but the two-instruction sequence is still correct.

Example 7: Sign extend for array index
```assembly
MOVSX R1, [R2]  ; Load signed byte from array at R2
ADD  R3, R3, R1 ; Add the signed value to accumulator
```

This pattern is common in sum-of-products calculations where array elements are stored as signed bytes but the accumulator is a 32-bit integer. The sign extension ensures that negative array elements subtract from the sum rather than becoming large positive numbers.

Example 8: Sign extend for pointer arithmetic
```assembly
MOVSX R1, [R2]  ; Load signed offset from table
LEA   R3, [R4 + R1] ; Compute base + signed offset
```

The signed offset is loaded from a table as an 8-bit value, sign extended to 64 bits, and used as an index into another table. This allows compact encoding of offsets in data structures where most offsets are small.

Example 9: Conditional sign extension
```assembly
CMP  R1, #0
BRANCH positive, skip
MOVSX R2, R2   ; Only executed if value is negative
skip:
```

The MOVSX instruction is placed inside a conditional branch. If the value is positive, sign extension does nothing because the upper bits are already zero, so the MOVSX could be omitted. This optimization is left to the compiler.

Example 10: Sign extend for remote memory
```assembly
MOVSX R1, @4:0x10000  ; Load signed byte from remote blade, sign extend
```

The remote memory access reads a single byte from blade 4. That byte is sign extended to 32 bits and stored in R1. The remote access latency of 5 microseconds dominates the execution time, but the sign extension adds no additional delay.

---

### 1.3 MOVZX – Move with Zero Extension

The MOVZX instruction moves a smaller unsigned integer into a larger register while filling the upper bits with zeros. When an unsigned 8-bit value of 0xFF (255) is moved into a 32-bit register, the result should be 0x000000FF (255). Zero extension is simpler than sign extension because the upper bits are always set to zero, regardless of the source value. This instruction is used for unsigned integers and for bit fields that should be treated as positive values.

**Encoding Format**

MOVZX uses opcode 0x03. The instruction format follows the same pattern as MOV and MOVSX. The header contains opcode 0x03, flags, and operand count of 2. The destination operand must be a register. The source operand can be a register, memory, or immediate. The source size must be smaller than the destination size. The flags field has bit 8 reserved for zero extension of packed data, which will be described in the vector instructions chapter.

The zero extension operation does not require any special hardware beyond a multiplexer that selects between the source value and zeros for the upper bits. The multiplexer is controlled by the difference between the destination size and the source size. For a 16-bit source extended to 64 bits, the lower 16 bits come from the source and the upper 48 bits are tied to ground, producing zeros.

**Operation Details**

The execution of MOVZX begins with reading the source value. For a memory source, the address is computed and the read is initiated. For a register source, the value is read from the register file. The source value is then zero-extended to the destination width. Unlike sign extension, zero extension does not examine the value; it simply places zeros in the upper bits. This can be implemented as a simple wiring: the lower bits of the destination are connected to the source, and the upper bits are connected to a constant zero.

After zero extension, the result is written to the destination register. The entire operation takes one cycle after the source is available. Because zero extension is simpler than sign extension, it uses slightly less power, but the difference is negligible in practice. The main advantage of MOVZX is semantic: it clearly indicates that the value is unsigned, helping both the programmer and the compiler reason about the code.

**Assembly Examples**

Example 1: Zero extend 8-bit to 32-bit
```assembly
MOVZX R1, R2  ; R2 contains 8-bit unsigned value, extend to 32-bit in R1
```

If R2 contains 0xFF (255), R1 becomes 0x000000FF (255). The upper 24 bits are zero. If the programmer had used MOVSX instead, R1 would become 0xFFFFFFFF (-1), which is a different value. Choosing the correct extension instruction is essential for correctness.

Example 2: Zero extend from memory
```assembly
MOVZX R1, [R2]  ; Load unsigned byte from address in R2
```

This loads a byte from memory and zero extends it to 32 bits. This is common when processing text or binary data where bytes represent unsigned quantities such as pixel values or characters.

Example 3: Zero extend 16-bit to 64-bit
```assembly
MOVZX R1, R2  ; R2 contains 16-bit unsigned value
```

The source register R2 is read as 16 bits, and the upper 48 bits of R1 are set to zero. This allows a 16-bit counter to be stored in a 64-bit register for use in 64-bit address calculations.

Example 4: Zero extend from immediate
```assembly
MOVZX R1, #255  ; Load 255 as 32-bit unsigned
```

The immediate 255 is stored as 8 bits in the instruction payload and zero extended to 32 bits. This uses less instruction space than a 32-bit immediate MOV, which would require 4 bytes of payload.

Example 5: Zero extend for array indexing
```assembly
MOVZX R1, [R2]  ; Load unsigned byte index
SHL   R1, R1, 2 ; Multiply by element size (4 bytes)
ADD   R3, R4, R1 ; Compute element address
```

This pattern loads an index from a byte array, treats it as unsigned, scales it to the element size, and uses it to index into another array. The zero extension ensures that the index is treated as a positive number between 0 and 255.

Example 6: Zero extend for bit fields
```assembly
MOVZX R1, R2  ; R2 contains packed bit fields
AND   R1, R1, #0x0F ; Extract low 4 bits as unsigned
```

The MOVZX alone does not extract bit fields; it only widens the value. After zero extension, the AND instruction masks off the unwanted bits. The combination loads a byte, widens it, and extracts a 4-bit field in two instructions.

Example 7: Zero extend for color components
```assembly
MOVZX R1, [R2]      ; Load blue component (0-255)
MOVZX R3, [R2+1]    ; Load green component
MOVZX R4, [R2+2]    ; Load red component
SHL   R4, R4, 16    ; Shift red to high byte
SHL   R3, R3, 8     ; Shift green to middle byte
OR    R1, R1, R3    ; Combine blue and green
OR    R1, R1, R4    ; Combine red
```

This sequence loads three bytes representing RGB color components, zero extends them to 32 bits, shifts them into position, and combines them into a single 32-bit RGB value. The zero extension ensures that the shifting and ORing produce the correct result.

Example 8: Zero extend for checksum
```assembly
MOVZX R1, [R2]  ; Load byte
ADD   R3, R3, R1 ; Add to running checksum
```

This simple loop computes a checksum by summing all bytes in a buffer. The MOVZX ensures that each byte is treated as a value between 0 and 255, not as a signed value that would become negative for bytes above 127.

Example 9: Zero extend from remote memory
```assembly
MOVZX R1, @4:0x10000  ; Load unsigned byte from remote blade
```

The remote access reads a byte from blade 4. That byte is zero extended to 32 bits. The remote latency dominates, but the zero extension adds no extra time.

Example 10: Comparison of MOVZX and MOVSX
```assembly
MOVZX R1, [buffer]   ; Load unsigned byte: 0xFF -> 0x000000FF (255)
MOVSX R2, [buffer]   ; Load signed byte:   0xFF -> 0xFFFFFFFF (-1)
CMP   R1, R2         ; Compare 255 and -1, not equal
```

This example demonstrates the difference between zero and sign extension. The same memory location containing 0xFF yields different values in R1 and R2. Understanding this difference is crucial for writing correct code that handles both signed and unsigned data.

---

### 1.4 LEA – Load Effective Address

The LEA instruction computes a memory address without accessing memory. Unlike MOV, which loads data from an address, LEA computes the address itself and stores it in a register. This is useful for pointer arithmetic, array indexing, and computing the addresses of structure fields. LEA can perform addition and scaling in a single instruction, replacing multiple arithmetic instructions.

**Encoding Format**

LEA uses opcode 0x04. The instruction header contains opcode 0x04, flags, and operand count of 2. The first operand is the destination register. The second operand is a memory address expression that is evaluated but not accessed. The flags field has bit 8 reserved for an address size override, allowing the computation to be performed in 32-bit mode even when the processor is in 64-bit mode. This is useful for legacy code and for certain pointer algorithms that rely on wrap-around behavior.

The memory address expression uses the same addressing modes as MOV, including base register, offset constant, index register, and scale factor. However, unlike MOV, the address is not used to access memory. Instead, the computed address value is written to the destination register. The address generation unit computes the address in the same way as for a memory access, but the memory controller is not invoked.

**Operation Details**

The LEA instruction executes in a single cycle, regardless of the complexity of the address expression. The address generation unit is a dedicated adder that can sum a base register, an index register multiplied by a scale factor, and a constant offset in parallel. The result is written directly to the destination register. Because no memory access occurs, LEA does not stall on cache misses or remote memory accesses.

The address computed by LEA is a virtual address, not a physical address. The segment tree translation is not performed because the address is not used to access memory. This means that LEA can compute addresses that would be invalid if accessed, such as addresses outside the current segment or addresses that cross segment boundaries. The computed address is simply the arithmetic result of the expression.

**Assembly Examples**

Example 1: Simple address computation
```assembly
LEA R1, [R2]  ; Copy R2 to R1
```

This LEA copies the value of R2 to R1 without accessing memory. It is equivalent to MOV R1, R2 but may have different timing characteristics on some implementations. Most programmers use MOV for this purpose, reserving LEA for more complex expressions.

Example 2: Add constant to register
```assembly
LEA R1, [R2 + 64]  ; R1 = R2 + 64
```

This adds 64 to the value in R2 and stores the result in R1. This is a common way to increment a pointer by a structure size. The addition is performed by the address generation unit without using the ALU, freeing the ALU for other operations.

Example 3: Add two registers
```assembly
LEA R1, [R2 + R3]  ; R1 = R2 + R3
```

This adds the values of R2 and R3 without accessing memory. This is a two-operand addition that does not modify either source register. The result is stored in R1. This is often more convenient than the ADD instruction, which modifies one of its operands.

Example 4: Add with scaling
```assembly
LEA R1, [R2 + R3*8]  ; R1 = R2 + (R3 * 8)
```

This computes the address of an element in an array of 8-byte elements. The base address is in R2, the element index is in R3, and the element size is 8 bytes. The address generation unit multiplies R3 by 8 using a shift, then adds the result to R2. This replaces a multiply instruction and an add instruction.

Example 5: Three-operand addition
```assembly
LEA R1, [R2 + R3 + 64]  ; R1 = R2 + R3 + 64
```

This adds two registers and a constant in a single instruction. The address generation unit sums all three components in parallel. The equivalent sequence using ADD would require two instructions: ADD R1, R2, R3 followed by ADD R1, R1, #64.

Example 6: Address of array element
```assembly
LEA R1, [array_base + R2*4]  ; R1 = array_base + (R2 * 4)
```

This computes the address of element R2 in an array of 32-bit integers. The base address array_base is an immediate constant encoded in the instruction. This is the most common use of LEA: computing the address of an element for later use in a MOV instruction.

Example 7: Pointer arithmetic for linked lists
```assembly
LEA R1, [R2 + 8]  ; R1 = R2 + 8 (skip to next field)
MOV R3, [R1]      ; Load the next pointer from the list node
```

This sequence advances a pointer by 8 bytes to reach the "next" field of a linked list node, then loads that field. The LEA computes the address, and the MOV loads the value. The two instructions execute in parallel on superscalar implementations.

Example 8: Address of structure field
```assembly
LEA R1, [R2 + offset_of_field]  ; R1 = R2 + field_offset
```

The constant offset_of_field is typically defined by the compiler as the byte offset of a field within a structure. The LEA computes the address of that field given the structure's base address in R2. This is generated by the compiler whenever a program takes the address of a structure member.

Example 9: Address of remote memory
```assembly
LEA R1, @4:0x10000  ; R1 = remote address descriptor
```

This LEA computes a remote address descriptor and stores it in R1. The descriptor includes the blade identifier and the offset. Subsequent memory operations using this descriptor will access the remote memory. This is used to precompute remote addresses for efficient access.

Example 10: Address for later use in loop
```assembly
LEA R1, [base]      ; R1 = base address
LEA R2, [base + size] ; R2 = base address + size
loop:
CMP R1, R2
BRANCH greater, done
; process element at address R1
LEA R1, [R1 + element_size]
BRANCH always, loop
done:
```

This loop uses LEA to compute the starting and ending addresses of a buffer, then uses LEA inside the loop to advance the pointer. The LEA instruction is used for pointer arithmetic, while separate MOV instructions are used for accessing the data. This separation of address calculation and data access is a hallmark of RISC-style programming and is fully supported by the PIP CISC architecture.

---

### 1.5 XCHG – Exchange Data

The XCHG instruction atomically exchanges the contents of two operands. After execution, the first operand contains the original value of the second operand, and the second operand contains the original value of the first operand. The exchange is atomic with respect to other cores and DMA devices, meaning that no other agent can observe the operation in progress. This makes XCHG useful for implementing spinlocks and other synchronization primitives.

**Encoding Format**

XCHG uses opcode 0x05. The instruction header contains opcode 0x05, flags, and operand count of 2. The flags field has bit 8 reserved for a memory ordering hint. When bit 8 is set, the exchange is performed with acquire-release semantics, meaning that all previous memory operations are completed before the exchange and all subsequent memory operations are started after the exchange. This is the default behavior for synchronization operations. When bit 8 is clear, the exchange is performed with relaxed semantics, which is faster but provides fewer ordering guarantees.

The operands can be registers or memory locations. At least one operand must be a register, because the exchange requires a temporary location to hold one value while the other is being loaded. The instruction cannot exchange two memory locations directly because that would require two memory accesses without an intervening register. If two memory locations need to be exchanged, the programmer must load one into a register, exchange with the other, then store the register back.

**Operation Details**

When XCHG executes with one register and one memory operand, the following steps occur atomically. The memory controller locks the cache line containing the memory operand, preventing any other core from accessing it. The current value of the memory location is read into a temporary buffer. The value from the register is written to the memory location. The temporary buffer value is written to the register. The cache line is unlocked. The entire sequence is indivisible; no other core can access that memory location between the read and the write.

When XCHG executes with two register operands, the exchange is performed within the register file in a single cycle. The register file has read ports for both source values and write ports for both destinations. The exchange is implemented by swapping the connections between the read and write ports, which is simpler than reading both values and then writing them back. The register file exchange operation is always atomic because only one instruction accesses the register file at a time.

**Assembly Examples**

Example 1: Exchange register with memory (spinlock acquire)
```assembly
XCHG R1, [lock]  ; Atomically exchange R1 with lock variable
```

This is the standard spinlock acquire operation. The lock variable is initially 0 (unlocked). The caller sets R1 to 1 (locked). The XCHG atomically swaps R1 with the lock variable. If the lock was 0, R1 becomes 0 and the lock becomes 1, indicating successful acquisition. If the lock was 1, R1 becomes 1 and the lock remains 1, indicating that the lock was already held.

Example 2: Exchange two registers
```assembly
XCHG R1, R2  ; Swap the contents of R1 and R2
```

This exchanges the values in R1 and R2. The operation takes one cycle and does not require a temporary register. This is more efficient than the three-instruction sequence using a temporary: MOV R3, R1; MOV R1, R2; MOV R2, R3.

Example 3: Exchange with release semantics
```assembly
XCHG.A R1, [lock]  ; Exchange with acquire-release semantics
```

The .A suffix sets bit 8 of the flags field, requesting acquire-release semantics. This ensures that all previous memory operations are completed before the exchange, and all subsequent memory operations are started after the exchange. This is the correct behavior for a spinlock release, where the lock must be released after all critical section operations are complete.

Example 4: Exchange with relaxed semantics
```assembly
XCHG.R R1, [counter]  ; Exchange with relaxed semantics
```

The .R suffix clears bit 8, requesting relaxed semantics. This is used when ordering does not matter, such as in a statistical counter where the exact order of updates is unimportant. Relaxed exchanges are faster because they do not require memory barrier instructions.

Example 5: Double-word exchange
```assembly
XCHG R1, [R2]  ; Exchange 64-bit value (if R1 is 64-bit)
```

The size of the exchange is determined by the register size. If R1 is a 64-bit register, the XCHG exchanges 64 bits between the register and memory. This is useful for exchanging pointers or double-word values.

Example 6: Byte exchange
```assembly
MOVZX R1, [R2]  ; Read current value
XCHG.B R1, [R2] ; Exchange byte (using size override)
```

The .B suffix indicates that the exchange should operate on a single byte, regardless of the register size. The upper bits of the register are zeroed after the exchange. This is useful for manipulating byte-sized synchronization variables.

Example 7: Exchange for double-checked locking
```assembly
CMP [flag], #0
BRANCH not_zero, skip
XCHG R1, [flag]  ; Attempt to acquire flag
CMP R1, #0
BRANCH not_zero, skip
; critical section
MOV [flag], #0   ; Release flag
skip:
```

This pattern implements double-checked locking. The flag is tested first without locking, then the lock is acquired, then the flag is tested again. The XCHG is used for the acquisition because it atomically reads the old value and writes the new value.

Example 8: Exchange for lock-free stack
```assembly
; R1 contains new node pointer
; R2 contains stack top address
loop:
MOV R3, [R2]          ; Load current top
MOV [R1 + offset_next], R3 ; Set new node's next to old top
XCHG R1, [R2]         ; Attempt to swap new top into place
CMP R1, R3            ; Check if exchange succeeded
BRANCH not_equal, loop ; Retry if someone else changed the top
```

This is the classic lock-free stack push operation using XCHG. The loop retries if the exchange fails because another thread modified the stack top between the load and the exchange.

Example 9: Exchange for ticket lock
```assembly
; R1 contains ticket number
XCHG R1, [next_ticket] ; Atomically get next ticket and increment
loop:
CMP R1, [now_serving]  ; Wait for ticket to be called
BRANCH less, loop
; critical section
ADD [now_serving], #1  ; Signal next ticket
```

The XCHG atomically reads the next_ticket counter and increments it by storing the new value. The old value (the ticket number) is returned in R1. This implements a fair ticket lock where threads are served in order of arrival.

Example 10: Exchange for remote memory
```assembly
XCHG R1, @4:0x10000  ; Exchange with memory on blade 4
```

This instruction exchanges the contents of R1 with a memory location on blade 4. The exchange is atomic across the optical fabric. The hardware locks the remote memory location during the exchange, preventing other cores on any blade from accessing it until the exchange completes. This enables distributed synchronization across the entire rack.

---

This concludes Chapter 1 of the Instruction Set Reference. The remaining chapters will cover Arithmetic Instructions, Logic and Bit Instructions, Control Flow Instructions, Vector and SIMD Instructions, Advanced Math Functions, Probabilistic Inference Instructions, System Instructions, Interconnect Instructions, Memory Management Instructions, and Protection Instructions. Each instruction will be documented with the same level of detail, including encoding, operation, operands, and ten assembly examples.


# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 2: Arithmetic Instructions

### 2.1 ADD – Add Operands

The ADD instruction performs binary addition on two operands and stores the result in the destination operand. Addition is the most fundamental arithmetic operation, forming the basis for address calculation, loop counting, accumulation, and countless other computations. The PIP CISC implementation of ADD supports multiple data sizes, vector operations, and saturating arithmetic for specialized domains like digital signal processing and machine learning.

**Encoding Format**

ADD uses opcode 0x10. The instruction header contains opcode 0x10, flags, and operand count of 2. The first operand is the destination, which is also the accumulator. The second operand is the source to be added. The result is stored in the destination, overwriting its original value. This two-operand form is the most common and matches the pattern of traditional CISC architectures.

The flags field controls several variations of the ADD operation. Bit 8, when set, indicates vector mode where the operands are treated as vectors of multiple elements rather than single values. Bits 9 and 10 encode the vector length: 00 for 128-bit vectors (default), 01 for 256-bit vectors, 10 for 512-bit vectors, and 11 for 1024-bit vectors. Bit 11, when set, indicates saturating arithmetic where results that overflow or underflow are clamped to the maximum or minimum representable value. Bit 12, when set, indicates that the addition should be performed using a rounding mode other than the default round-to-nearest. Bits 13-15 encode the rounding mode when bit 12 is set: 000 for round-to-nearest, 001 for round-toward-zero, 010 for round-up, 011 for round-down, 100 for round-to-nearest-ties-to-even.

The operand descriptors for ADD follow the standard format. The destination descriptor specifies a register or memory location. The source descriptor can specify a register, memory, immediate, or vector. When both operands are scalars, the addition is performed once. When both operands are vectors of the same length, the addition is performed element-wise, with each element in the destination vector receiving the sum of the corresponding elements in the two source vectors. When the destination is a vector and the source is a scalar, the scalar is broadcast to all vector elements before addition.

**Operation Details**

The ADD instruction executes in a single cycle for scalar operands when the data is already in registers. The arithmetic logic unit contains a dedicated adder that can add two values of up to 512 bits in one cycle. The adder uses a carry-lookahead architecture that computes all carry bits in parallel, avoiding the ripple delay that would plague a simple ripple-carry adder. For 512-bit addition, the carry-lookahead tree has 9 levels of logic, which is within the cycle time of a 2 GHz processor.

When the operands are in memory, the ADD instruction first loads the values, then performs the addition, then stores the result. The load and store are handled by the memory controller while the ALU is idle. The instruction stalls only if the memory system cannot keep up with the requests. For local DRAM with good cache behavior, the ADD instruction completes in approximately 100 nanoseconds. For remote memory, the latency is 5 microseconds. For flash memory, the latency is 50 microseconds.

The condition flags are updated after every ADD instruction, unless suppressed by the flag field. The zero flag is set if the result is zero. The sign flag is set to the most significant bit of the result, indicating a negative value in two's complement representation. The carry flag is set if the addition produced a carry out of the most significant bit, indicating unsigned overflow. The overflow flag is set if the addition produced a result whose sign differs from the sign that would be expected from adding the operands, indicating signed overflow.

For vector additions, the condition flags are updated based on the final element of the vector. The zero flag is set if every element of the result vector is zero. The sign flag is set to the most significant bit of the last element. The carry and overflow flags are set based on the last element only. This design allows vector code to test the overall result without examining each element individually.

**Assembly Examples**

Example 1: Simple integer addition
```assembly
ADD R1, R2    ; R1 = R1 + R2
```

This adds the contents of R2 to R1 and stores the result back in R1. The original value in R1 is lost. If the addition overflows, the overflow flag is set. The carry flag is set if there is a carry out of the most significant bit. This is the most common form of the ADD instruction.

Example 2: Addition with immediate value
```assembly
ADD R1, #42   ; R1 = R1 + 42
```

The immediate value 42 is encoded in the instruction payload. For small constants, this uses less instruction space than loading the constant into a register first. The assembler automatically selects the smallest encoding that can represent the constant.

Example 3: Addition from memory
```assembly
ADD R1, [R2]  ; R1 = R1 + value at address R2
```

This loads a value from memory at the address in R2, adds it to R1, and stores the result in R1. The memory access is handled by the memory controller, and the instruction stalls if the data is not in cache. This pattern is common when accumulating values from an array.

Example 4: Vector addition of two arrays
```assembly
ADD.V [R1], [R2], [R3]  ; Vector add: for i in 0..7, R1[i] = R2[i] + R3[i]
```

The .V suffix indicates vector mode. The instruction adds eight 32-bit elements (a 256-bit vector) from the arrays pointed to by R2 and R3, storing the eight results in the array pointed to by R1. The memory controller performs eight reads and eight writes, but the ALU performs the eight additions in parallel. This is 8 times faster than performing eight scalar ADD instructions.

Example 5: Broadcast scalar to vector
```assembly
ADD.V R1, R2, #1  ; Add 1 to every element of vector in R1
```

The destination R1 is a vector register. The source R2 is also a vector register. The second source is the immediate 1, which is broadcast to all elements of the vector. This adds 1 to every element of the vector, performing 16 additions in parallel if the vector length is 16 elements.

Example 6: Saturating addition
```assembly
ADD.S R1, R2    ; Saturating add: R1 = saturate(R1 + R2)
```

The .S suffix sets the saturating flag. If the addition overflows, the result is clamped to the maximum value. If the addition underflows (for signed addition where the result is less than the minimum), the result is clamped to the minimum value. Saturating arithmetic is used in audio processing to prevent clicks and pops caused by overflow wraparound.

Example 7: Address calculation with ADD
```assembly
ADD R1, R2      ; R1 = R1 + R2 (used as pointer arithmetic)
LEA R3, [R1]    ; R3 = R1 (for comparison)
```

This sequence adds two pointers, then copies the result to another register using LEA. The ADD modifies R1, while LEA leaves it unchanged. The programmer could have used LEA exclusively, but ADD is sometimes more convenient when the destination should be one of the sources.

Example 8: Loop counter increment
```assembly
ADD R1, #1      ; Increment loop counter
CMP R1, #100    ; Compare to limit
BRANCH less, loop ; Branch if not done
```

The ADD instruction increments the loop counter. The CMP instruction compares the counter to the limit. The BRANCH instruction conditionally jumps back to the loop. This three-instruction sequence is the standard loop structure generated by compilers.

Example 9: Remote memory addition
```assembly
ADD R1, @4:0x10000  ; R1 = R1 + value at remote address
```

This adds a value from remote memory on blade 4 to R1. The remote access takes approximately 5 microseconds. During this time, the core stalls. Other cores on the same blade continue executing, but the stalled core consumes power and generates heat while waiting.

Example 10: Multi-precision addition (128-bit)
```assembly
ADD R1, R2          ; Add low 64 bits
ADD.C R3, R4        ; Add high 64 bits with carry
```

The .C suffix indicates that the carry flag from the previous addition should be included. This sequence adds two 128-bit numbers stored in register pairs (R1,R3) and (R2,R4). The first ADD adds the low 64 bits and sets the carry flag if there is overflow. The second ADD with carry adds the high 64 bits plus the carry from the low addition. This pattern extends to arbitrary precision.

---

### 2.2 SUB – Subtract Operands

The SUB instruction performs binary subtraction, subtracting the second operand from the first and storing the result in the first operand. Subtraction is essential for computing differences, reversing pointer movements, and implementing comparison operations. The PIP CISC implementation of SUB shares the same flag update and vector capabilities as ADD, making it symmetric and predictable.

**Encoding Format**

SUB uses opcode 0x11. The instruction format is identical to ADD, with opcode 0x11 in the header. The flags field uses the same bits for vector mode, saturating arithmetic, and rounding mode control. The operand descriptors follow the same pattern, with the destination being the accumulator and the source being the value to subtract.

The key difference between ADD and SUB is that SUB computes destination minus source, not source minus destination. This asymmetric behavior means that the programmer must pay attention to operand order. The condition flags are updated based on the result of the subtraction. The zero flag is set if the result is zero. The sign flag is set to the most significant bit of the result. The carry flag is set if the subtraction required a borrow from beyond the most significant bit, which occurs when the source is larger than the destination in unsigned interpretation. The overflow flag is set if the subtraction overflows in signed interpretation.

**Operation Details**

The SUB instruction uses the same adder hardware as ADD, but with the source operand inverted before addition. Subtraction is implemented as addition of the two's complement: `dest = dest + (~src + 1)`. This transformation allows the ALU to reuse the adder for both addition and subtraction, saving silicon area. The inversion and increment are performed in the same cycle as the addition, adding no additional latency.

For saturating subtraction, the result is clamped to the minimum or maximum value if the subtraction would underflow or overflow. For unsigned saturating subtraction, subtracting a larger number from a smaller number yields zero rather than a large positive number due to wraparound. For signed saturating subtraction, subtracting a very negative number from a very positive number might overflow, and the result is clamped to the maximum value.

**Assembly Examples**

Example 1: Simple integer subtraction
```assembly
SUB R1, R2    ; R1 = R1 - R2
```

This subtracts the contents of R2 from R1 and stores the result in R1. If R1 is 100 and R2 is 30, the result is 70. If R1 is 30 and R2 is 100, the result is -70, and the carry flag is set because a borrow occurred.

Example 2: Subtraction with immediate
```assembly
SUB R1, #42   ; R1 = R1 - 42
```

This subtracts 42 from R1. This is commonly used to decrement a value by a constant that is not 1. For decrement by 1, the dedicated DEC instruction is more efficient, but SUB with immediate works correctly.

Example 3: Pointer subtraction
```assembly
SUB R1, R2    ; R1 = R1 - R2 (difference in bytes)
```

This computes the difference between two pointers. If both pointers point into the same array, the result is the distance in bytes between them. Dividing by the element size yields the index difference.

Example 4: Vector subtraction
```assembly
SUB.V [R1], [R2], [R3]  ; Vector subtract: R1[i] = R2[i] - R3[i]
```

This subtracts each element of the vector at R3 from the corresponding element of the vector at R2, storing the results at R1. This is used in image differencing, where the difference between two images highlights changes.

Example 5: Saturating subtraction
```assembly
SUB.S R1, R2    ; Saturating subtract: R1 = saturate(R1 - R2)
```

If the subtraction would underflow, the result is clamped to the minimum value. For unsigned subtraction, underflow produces zero. For signed subtraction, underflow produces the most negative value. This is used in audio processing to prevent clicks when subtracting signals.

Example 6: Loop counter with subtract
```assembly
SUB R1, #1      ; Decrement loop counter
CMP R1, #0      ; Test if zero
BRANCH greater, loop ; Branch if not zero
```

This subtracts 1 from the loop counter, tests if it is zero, and branches if it is not zero. The dedicated DEC instruction is more efficient for decrementing by 1, but SUB with immediate works and may be clearer in some contexts.

Example 7: Difference of memory values
```assembly
SUB R1, [R2]    ; R1 = R1 - value at address R2
```

This loads a value from memory and subtracts it from R1. This pattern is common when computing deltas or residuals, where a predicted value is stored in memory and the actual value is in a register.

Example 8: Absolute difference
```assembly
SUB R1, R2      ; R1 = R1 - R2
BRANCH positive, done
NEG R1, R1      ; If result negative, negate it
done:
```

This sequence computes the absolute difference between R1 and R2. The SUB computes the difference, which may be negative. The branch checks the sign, and the NEG instruction negates negative values to make them positive. This is a common pattern in distance calculations.

Example 9: Remote memory subtraction
```assembly
SUB R1, @4:0x10000  ; R1 = R1 - remote value
```

This subtracts a value from remote memory on blade 4. The remote access takes approximately 5 microseconds. The core stalls during this time. For distributed computations where each blade maintains a local copy of shared data, this instruction allows remote subtractions to be performed directly.

Example 10: Multi-precision subtraction (256-bit)
```assembly
SUB R1, R2          ; Subtract low 64 bits
SUB.C R3, R4        ; Subtract high 64 bits with borrow
SUB.C R5, R6        ; Subtract next 64 bits with borrow
SUB.C R7, R8        ; Subtract highest 64 bits with borrow
```

This sequence subtracts two 256-bit numbers stored in four registers each. The first SUB subtracts the low 64 bits and sets the carry flag if a borrow is needed. The subsequent SUB.C instructions include the borrow from the previous subtraction. This pattern extends to arbitrary precision.

---

### 2.3 MUL – Multiply Unsigned

The MUL instruction performs unsigned multiplication of two operands and stores the product. Multiplication is computationally expensive compared to addition, requiring more cycles and more hardware. The PIP CISC implementation includes a dedicated multiplier that can perform 512-bit by 512-bit multiplication in a single cycle, using a Wallace tree reduction network that sums partial products in parallel.

**Encoding Format**

MUL uses opcode 0x12. The instruction header contains opcode 0x12, flags, and operand count of 2. The first operand is the destination, which is also one of the sources. The second operand is the multiplier. The product is stored in the destination, which must be twice the width of the operands to avoid overflow. For example, multiplying two 32-bit numbers produces a 64-bit product that requires a 64-bit destination register.

The flags field includes bits for vector mode and rounding control, but saturating arithmetic is not applicable to multiplication because the product is stored in a double-width register that cannot overflow by definition. Bit 8 enables vector mode. Bits 9-10 set vector length. Bits 11-12 are reserved. Bits 13-15 set the rounding mode for floating-point multiplication.

When the operands are smaller than the destination register, the multiplication is performed at the operand width and the result is zero-extended to the destination width. For example, if the destination is 64 bits and both operands are 32 bits, the product is 64 bits and fits exactly. If the operands are 32 bits but the destination is 128 bits, the product is zero-extended to 128 bits.

**Operation Details**

The multiplier uses a modified Booth encoding to reduce the number of partial products. Booth encoding examines three bits of the multiplier at a time and selects -2, -1, 0, 1, or 2 times the multiplicand. This reduces the number of partial products from 512 to 256 for a 512-bit multiplication. The partial products are then summed using a Wallace tree of carry-save adders. The Wallace tree reduces 256 partial products to 2 numbers (a sum and a carry) in log2(256) = 8 levels of addition. The final sum is produced by a carry-propagate adder.

The multiplier is pipelined to allow back-to-back multiplications every cycle. The pipeline has three stages: Booth encoding, partial product reduction, and final addition. The latency is 3 cycles, but the throughput is 1 multiplication per cycle. This means that a sequence of independent multiplications can be performed at full speed, but a multiplication that depends on the result of a previous multiplication has a 3-cycle latency.

**Assembly Examples**

Example 1: Simple unsigned multiplication
```assembly
MUL R1, R2    ; R1 = R1 * R2 (unsigned)
```

This multiplies the unsigned value in R1 by the unsigned value in R2 and stores the product in R1. The product may be up to twice the width of the operands. If R1 and R2 are 32 bits, the product is 64 bits, and the upper 32 bits are stored in R1's upper half. The lower 32 bits are stored in the lower half.

Example 2: Multiplication with immediate
```assembly
MUL R1, #10   ; R1 = R1 * 10
```

This multiplies R1 by the immediate value 10. The immediate is zero-extended to the width of R1 before multiplication. This is useful for scaling values by small constants, such as converting from degrees to radians.

Example 3: Multiplication with memory operand
```assembly
MUL R1, [R2]  ; R1 = R1 * value at address R2
```

This loads a multiplier from memory and multiplies it with R1. The memory access is handled by the memory controller, and the instruction stalls if the data is not in cache. This pattern is common when multiplying by coefficients stored in a table.

Example 4: Vector multiplication (element-wise)
```assembly
MUL.V [R1], [R2], [R3]  ; Vector multiply: R1[i] = R2[i] * R3[i]
```

This multiplies each element of the vector at R2 by the corresponding element of the vector at R3, storing the results at R1. The vector length is specified in the flags field. For 512-bit vectors of 32-bit elements, this performs 16 multiplications in parallel, 16 times faster than scalar code.

Example 5: Dot product using multiply-add
```assembly
MUL R1, R2    ; R1 = R1 * R2
ADD R3, R1    ; R3 = R3 + R1 (accumulate)
```

This sequence multiplies two values and adds the product to an accumulator. The combination of MUL and ADD is so common that the FMA instruction (covered later) combines them into a single operation. However, separate MUL and ADD instructions are still useful when the multiplication and addition are not tightly coupled.

Example 6: Square calculation
```assembly
MUL R1, R1    ; R1 = R1 * R1 (square)
```

Multiplying a register by itself computes its square. This is useful for variance calculations, energy computations, and distance calculations where the square of a value is needed. The square operation uses the same multiplier as general multiplication.

Example 7: Scaling for fixed-point arithmetic
```assembly
MUL R1, #65536   ; Scale by 2^16 for fixed-point
SHR R1, R1, #16  ; Extract high 16 bits after scaling
```

This sequence multiplies by 2^16, then shifts right by 16, effectively leaving the original value unchanged but with an overflow flag that indicates whether the value was too large. This is used in fixed-point arithmetic to detect overflow during scaling operations.

Example 8: Multiplication with remote memory
```assembly
MUL R1, @4:0x10000  ; R1 = R1 * remote value
```

This multiplies R1 by a value stored on blade 4. The remote access takes approximately 5 microseconds. The core stalls during this time. This is useful for distributed matrix multiplication, where each blade stores a portion of the matrix.

Example 9: 128-bit by 128-bit multiplication
```assembly
MUL R1, R2    ; Multiply low 64 bits, get 128-bit product in (R3,R1)
MUL R3, R4    ; Multiply high 64 bits with different operands
```

The actual 128x128 multiplication requires four multiplications and several additions. The hardware multiplier can perform the 64x64 multiplications directly, and the programmer or compiler must combine them. The result is a 256-bit product stored in four registers.

Example 10: Polynomial evaluation with Horner's method
```assembly
MUL R1, R2    ; R1 = R1 * x
ADD R1, R3    ; R1 = R1 + coefficient
MUL R1, R2    ; R1 = R1 * x
ADD R1, R4    ; R1 = R1 + coefficient
MUL R1, R2    ; R1 = R1 * x
ADD R1, R5    ; R1 = R1 + coefficient
```

This sequence evaluates a polynomial using Horner's method: `((c3 * x + c2) * x + c1) * x + c0`. Each step multiplies by x and adds the next coefficient. The MUL and ADD instructions alternate, with the result of each step feeding into the next. This is more efficient than computing each power of x separately.

---

### 2.4 DIV – Divide Unsigned

The DIV instruction performs unsigned division, dividing the dividend by the divisor to produce a quotient and a remainder. Division is the most expensive arithmetic operation, requiring many cycles and specialized hardware. The PIP CISC implementation uses a radix-4 SRT division algorithm that produces two quotient bits per cycle, achieving a latency of approximately 100 cycles for 64-bit division.

**Encoding Format**

DIV uses opcode 0x14. The instruction header contains opcode 0x14, flags, and operand count of 2. The first operand is the dividend, stored in a register pair. The second operand is the divisor. The quotient is stored in the first register of the pair, and the remainder is stored in the second register. For example, if the dividend is in registers (R1,R2) with R1 holding the high word and R2 holding the low word, after DIV the quotient is in R1 and the remainder is in R2.

The flags field includes bits for vector mode, but division is rarely vectorized because the latency is high and the hardware cost is significant. Bit 8 enables vector mode, but most implementations will not support vector division in hardware, instead trapping to software emulation. Bits 9-15 are reserved.

Division by zero is a fatal error. The hardware detects division by zero and raises a divide-by-zero exception before any other operation. The exception handler can either terminate the process or emulate the division with a result defined by the operating system. The architectural behavior for division by zero is to set the quotient to all ones and the remainder to zero, but this behavior is configurable through a model-specific register.

**Operation Details**

The SRT division algorithm operates as follows. The divisor and dividend are normalized so that the most significant bit of the divisor is 1. Then, for each iteration, the algorithm examines the top few bits of the remainder and selects a quotient digit from the set {-2, -1, 0, 1, 2}. The quotient digit is used to subtract a multiple of the divisor from the remainder. The remainder is then shifted left by one position (two bits for radix-4) and the process repeats.

The quotient digits are stored in a redundant representation (signed-digit) until all iterations are complete. At the end, the quotient is converted to standard binary representation, and the remainder is adjusted to be non-negative. The conversion adds a small additional latency but allows the iterations to run faster because the quotient digit selection does not require precise comparison.

**Assembly Examples**

Example 1: Simple unsigned division
```assembly
DIV R1, R2    ; Divide (R1,R0) by R2, quotient in R1, remainder in R0
```

This divides the 64-bit dividend in (R1,R0) by the 32-bit divisor in R2. The quotient is stored in R1, and the remainder is stored in R0. The original dividend is overwritten. This is the most common form of division.

Example 2: Division of 32-bit values
```assembly
MOVZX R1, R3   ; Extend 32-bit dividend to 64 bits in (R1,R0)
DIV R1, R2     ; Divide by 32-bit divisor
```

To divide a 32-bit value, it must first be zero-extended to 64 bits. The upper 32 bits are stored in R1, and the lower 32 bits are stored in R0. After the division, the quotient is in R1 and the remainder is in R0. The remainder fits in 32 bits.

Example 3: Division with memory operand
```assembly
DIV R1, [R2]   ; Divide by divisor stored at address R2
```

This loads the divisor from memory before performing the division. The memory access is handled by the memory controller, and the instruction stalls if the data is not in cache. The division still takes approximately 100 cycles after the load completes.

Example 4: Check for divisibility
```assembly
DIV R1, R2     ; Divide
CMP R0, #0     ; Check remainder
BRANCH equal, divisible ; Branch if remainder is zero
```

This sequence tests whether R1 is divisible by R2. The DIV computes the quotient and remainder. The CMP instruction tests whether the remainder is zero. The BRANCH instruction jumps if the remainder is zero. This is more efficient than computing the remainder via multiplication and subtraction.

Example 5: Convert seconds to minutes and seconds
```assembly
MOV R1, seconds     ; Dividend in (R1,R0)
MOV R2, #60         ; Divisor = 60
DIV R1, R2          ; Quotient = minutes, remainder = seconds
```

This divides a number of seconds by 60, producing minutes in the quotient and remaining seconds in the remainder. This pattern extends to any unit conversion where the result is a quotient and remainder.

Example 6: Average calculation with remainder
```assembly
MOV R1, sum         ; Sum of values
MOV R2, count       ; Number of values
DIV R1, R2          ; Quotient = average, remainder = remainder
```

This computes the average of a set of numbers as an integer quotient and remainder. For precise floating-point averages, a separate conversion is needed, but integer division is sufficient for many applications such as pixel averaging.

Example 7: Division by power of two (optimized)
```assembly
SHR R1, R1, #3     ; R1 = R1 / 8 (optimized)
```

For division by a power of two, the compiler uses a shift instruction instead of a divide instruction. The shift is much faster (1 cycle vs 100 cycles). The programmer can write division by a power of two, and the compiler will automatically replace it with a shift when optimizations are enabled.

Example 8: Remote memory division
```assembly
DIV R1, @4:0x10000  ; Divide by divisor on remote blade
```

This loads the divisor from remote memory on blade 4, then performs the division. The remote access takes approximately 5 microseconds, and the division takes approximately 100 cycles (50 nanoseconds at 2 GHz), so the remote access dominates the latency.

Example 9: Multi-precision division
```assembly
; Division of 128-bit number by 64-bit number
; This requires multiple DIV instructions and is complex
```

Multi-precision division is complex and typically implemented in software using a combination of DIV instructions and manual adjustments. The hardware supports only up to 64-bit divisors; larger divisors must be handled by software algorithms that use the hardware divisor as a building block.

Example 10: Division for scaling
```assembly
MUL R1, #65536   ; Scale up by 2^16
DIV R1, R2       ; Divide by R2 (fixed-point division)
```

This sequence multiplies the dividend by 2^16 before division, effectively performing fixed-point division with 16 fractional bits. This is used in graphics and audio processing where fractional values need to be computed using integer arithmetic.

---

### 2.5 FMA – Fused Multiply-Add

The FMA instruction performs a fused multiply-add operation: `dest = (a * b) + c`. The key word is "fused" – the multiplication and addition are performed as a single operation with only one rounding at the end, rather than rounding the product then rounding the sum. This improves accuracy and performance for dot products, matrix multiplication, polynomial evaluation, and countless other computations.

**Encoding Format**

FMA uses opcode 0x18. The instruction header contains opcode 0x18, flags, and operand count of 3. The first operand is the destination, which stores the result. The second operand is the multiplier (a). The third operand is the multiplicand (b). The fourth operand is the addend (c). The instruction computes `dest = a * b + c`.

The flags field controls rounding mode and vector operation. Bits 8-9 set the rounding mode: 00 for round-to-nearest, 01 for round-toward-zero, 10 for round-up, 11 for round-down. Bit 10 enables vector mode. Bits 11-12 set the vector length. Bits 13-15 are reserved.

The FMA instruction is critical for matrix multiplication, where each output element is the sum of products of corresponding elements from a row and a column. Without FMA, each multiply and add would be separate instructions with separate rounding steps, leading to accumulated rounding errors. With FMA, the entire dot product can be computed with minimal error.

**Operation Details**

The FMA hardware computes the product `a * b` with infinite precision, using a 2N-bit product register where N is the operand width. For 64-bit floating-point operands, the product has 128 significant bits. The addend `c` is then added to this infinite-precision product, producing a sum with up to 129 bits of significance. Finally, the result is rounded to N bits according to the selected rounding mode.

The infinite-precision computation is expensive in hardware, requiring a 128-bit multiplier and a 130-bit adder. However, the fused operation saves one rounding step, which improves accuracy. For many algorithms, the improved accuracy allows the use of lower-precision arithmetic, which can be faster and more power-efficient.

**Assembly Examples**

Example 1: Simple FMA
```assembly
FMA R1, R2, R3, R4   ; R1 = (R2 * R3) + R4
```

This multiplies R2 by R3, adds R4, and stores the result in R1. The multiplication and addition are fused with a single rounding. The original values in R2, R3, and R4 are unchanged.

Example 2: FMA with immediate
```assembly
FMA R1, R2, R3, #1.0   ; R1 = (R2 * R3) + 1.0
```

The addend is an immediate floating-point constant 1.0. This is useful for adding a bias term after multiplication, such as in neural network neurons where the output is `sum(weights * inputs) + bias`.

Example 3: Dot product using FMA in a loop
```assembly
MOV R1, #0          ; Initialize accumulator to zero
MOV R2, #0          ; Initialize index
loop:
FMA R1, [R3+R2], [R4+R2], R1  ; accumulator += a[i] * b[i]
ADD R2, #8          ; Advance index by 8 bytes (two 32-bit floats)
CMP R2, #size
BRANCH less, loop
```

This loop computes the dot product of two vectors. Each iteration loads a pair of floating-point values from memory, multiplies them, and adds the product to the accumulator. The FMA instruction combines the multiplication and addition, and the accumulator is updated in place. The loop counter is incremented by 8 bytes because each float is 4 bytes and there are two floats per iteration (not shown in the load instructions).

Example 4: Matrix multiplication kernel
```assembly
; Outer loops omitted for clarity
; Inner loop: dot product of row i from matrix A and column j from matrix B
MOV R1, #0          ; Initialize accumulator
MOV R2, #0          ; Initialize index
inner:
FMA R1, [A_base + R2], [B_base + R2], R1
ADD R2, #4          ; Advance to next element (4 bytes)
CMP R2, #cols
BRANCH less, inner
MOV [C_base + offset], R1  ; Store result
```

This is the inner loop of matrix multiplication. For each output element, the loop iterates over the columns of the row of A and the rows of the column of B, accumulating the dot product using FMA. The FMA instruction is critical for performance because matrix multiplication is dominated by multiply-add operations.

Example 5: Polynomial evaluation with FMA
```assembly
; Evaluate f(x) = a*x^3 + b*x^2 + c*x + d using Horner's method
FMA R1, x, a, b     ; R1 = a*x + b
FMA R1, R1, x, c    ; R1 = (a*x + b)*x + c = a*x^2 + b*x + c
FMA R1, R1, x, d    ; R1 = (a*x^2 + b*x + c)*x + d = a*x^3 + b*x^2 + c*x + d
```

Horner's method evaluates a polynomial using repeated multiply-add operations. Each FMA combines a multiplication by x and an addition of the next coefficient. This is more accurate than separate multiply and add instructions because only one rounding occurs per step.

Example 6: Vector FMA for AI inference
```assembly
FMA.V R1, R2, R3, R4   ; Vector FMA: R1[i] = (R2[i] * R3[i]) + R4[i]
```

This performs element-wise FMA on vectors. For neural network inference, a layer computes `output = activation(weights * inputs + bias)`. The vector FMA computes the weights times inputs plus bias for all output neurons in parallel. The activation function is applied separately.

Example 7: Complex multiplication using FMA
```assembly
; Multiply (a + i*b) by (c + i*d) = (a*c - b*d) + i*(a*d + b*c)
FMA real, a, c, neg_b_d    ; real = a*c + (-b*d)
FMA imag, a, d, b_c        ; imag = a*d + b*c
```

Complex multiplication requires two multiplications and two additions. The FMA instruction can compute the real part as `a*c + (-b*d)` if the product `b*d` is precomputed and negated. The imag part is `a*d + b*c`. Using FMA saves instructions and improves accuracy.

Example 8: FMA with rounding mode
```assembly
FMA.RZ R1, R2, R3, R4   ; FMA with round-toward-zero
```

The .RZ suffix sets the rounding mode to round-toward-zero. This is useful for interval arithmetic where the result must be contained within a known bound. Rounding down and rounding up produce the interval boundaries.

Example 9: Remote memory FMA
```assembly
FMA R1, R2, @4:0x10000, R3   ; R1 = (R2 * remote) + R3
```

This multiplies R2 by a value on remote blade 4, then adds R3. The remote access takes approximately 5 microseconds. The FMA itself takes 2-3 cycles. This is useful for distributed matrix multiplication where each blade stores a portion of the matrix.

Example 10: FMA for error compensation
```assembly
; Kahan summation algorithm for high-precision accumulation
FMA sum, sum, #1.0, err   ; Temporarily add error term
FMA err, sum, #1.0, -sum  ; Compute new error
```

Kahan summation uses FMA to track rounding errors. The first FMA adds the error term to the sum. The second FMA computes the error introduced by that addition. This algorithm requires FMA to be effective; separate multiply and add instructions would not capture the rounding error correctly.

---

This concludes Chapter 2 of the Instruction Set Reference. The remaining chapters will cover Logic and Bit Instructions, Control Flow Instructions, Vector and SIMD Instructions, Advanced Math Functions, Probabilistic Inference Instructions, System Instructions, Interconnect Instructions, Memory Management Instructions, and Protection Instructions. Each instruction will be documented with the same level of detail, including encoding, operation, operands, and ten assembly examples.

# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 3: Logic and Bit Instructions

### 3.1 AND – Bitwise Logical AND

The AND instruction performs a bitwise logical AND operation between two operands. For each bit position, the result bit is 1 if and only if both corresponding bits in the source operands are 1. Otherwise, the result bit is 0. The AND instruction is fundamental for masking operations, clearing specific bits, testing bit patterns, and implementing Boolean logic in bitwise fashion.

**Encoding Format**

AND uses opcode 0x20. The instruction header contains opcode 0x20, flags, and operand count of 2. The first operand is the destination, which is also the accumulator. The second operand is the source. The result is stored in the destination, overwriting its original value.

The flags field controls vector mode and condition flag behavior. Bit 8, when set, indicates vector mode where the operands are treated as vectors of multiple elements. Bits 9 and 10 encode the vector length: 00 for 128-bit vectors, 01 for 256-bit vectors, 10 for 512-bit vectors, and 11 for 1024-bit vectors. Bit 11, when set, suppresses condition flag updates, which is useful when the result is not needed for branching. Bits 12-15 are reserved.

The operand descriptors for AND follow the standard format. The destination descriptor specifies a register or memory location. The source descriptor can specify a register, memory, immediate, or vector. When both operands are scalars, the AND operation is performed once across all bits of the operands. When both operands are vectors of the same length, the AND operation is performed element-wise.

**Operation Details**

The AND instruction executes in a single cycle for scalar operands when the data is already in registers. The arithmetic logic unit contains a dedicated bitwise logic unit that operates in parallel across all bits of the operands. For 512-bit operands, the logic unit consists of 512 independent AND gates operating simultaneously. This parallel design means that AND takes the same amount of time regardless of operand size, as long as the data path width matches.

When the operands are in memory, the AND instruction first loads the values, then performs the AND operation, then stores the result. The load and store are handled by the memory controller while the logic unit is idle. The instruction stalls only if the memory system cannot keep up with the requests. For local DRAM with good cache behavior, the AND instruction completes in approximately 100 nanoseconds.

The condition flags are updated after every AND instruction, unless suppressed. The zero flag is set if the result is zero. The sign flag is set to the most significant bit of the result. The carry and overflow flags are cleared because AND does not produce a carry or overflow. This behavior is consistent with the semantics of bitwise logical operations.

For vector AND operations, the condition flags are updated based on the final element of the vector. The zero flag is set if every element of the result vector is zero. The sign flag is set to the most significant bit of the last element. The carry and overflow flags are cleared.

**Assembly Examples**

Example 1: Simple bitwise AND
```assembly
AND R1, R2    ; R1 = R1 & R2 (bitwise)
```

This performs a bitwise AND between R1 and R2, storing the result in R1. Each bit of R1 becomes 1 only if the corresponding bits of both R1 and R2 were 1. This is the most common form of the AND instruction.

Example 2: Masking with immediate
```assembly
AND R1, #0xFF   ; R1 = R1 & 0xFF (keep only low 8 bits)
```

This clears all bits except the low 8 bits of R1. The immediate value 0xFF acts as a mask. This is commonly used to extract a byte from a larger word or to ensure that a value fits within a certain range.

Example 3: Clearing specific bits
```assembly
AND R1, #0xFFFFFF00   ; Clear low 8 bits of R1
```

This clears the low 8 bits of R1 while preserving the upper bits. The mask has zeros in the positions to clear and ones in the positions to keep. This is the opposite of masking; it clears rather than extracts.

Example 4: Testing bits without modifying
```assembly
AND R3, R1, R2   ; R3 = R1 & R2 (three-operand form using MOV first)
MOV R3, R1
AND R3, R2
```

The AND instruction modifies its destination, so testing bits requires copying to a temporary register first. This sequence copies R1 to R3, then ANDs with R2, leaving R1 unchanged. The result in R3 can be tested with a subsequent conditional branch.

Example 5: Testing if a value is zero
```assembly
AND R1, R1   ; R1 & R1 = R1 (sets flags without changing value)
BRANCH zero, is_zero
```

ANDing a register with itself leaves the register unchanged but updates the condition flags. This is a common way to test if a value is zero without modifying the value. The zero flag is set if R1 is zero, and the branch condition checks that flag.

Example 6: Aligning memory addresses
```assembly
AND R1, #0xFFFFFFF0   ; Align R1 to 16-byte boundary
```

This clears the low 4 bits of the address in R1, rounding it down to the nearest multiple of 16. This is used to align pointers to cache line boundaries or to satisfy alignment requirements of SIMD instructions.

Example 7: Vector bitwise AND
```assembly
AND.V R1, R2, R3   ; Vector AND: for each element, R1[i] = R2[i] & R3[i]
```

This performs bitwise AND on each element of two vectors. The vector length is specified in the flags field. For 512-bit vectors of 64-bit elements, this performs 8 AND operations in parallel. This is used in vectorized cryptography and data compression algorithms.

Example 8: Masked vector operations
```assembly
AND.V mask, mask, condition   ; Update mask vector based on condition
AND.V R1, R1, mask            ; Clear elements where mask is zero
```

This sequence uses a mask vector to selectively clear elements of another vector. The first AND updates the mask based on some condition (not shown). The second AND clears elements in R1 where the corresponding mask bit is zero. This implements conditional execution on vectors.

Example 9: Remote memory AND
```assembly
AND R1, @4:0x10000   ; R1 = R1 & value at remote address
```

This loads a value from remote memory on blade 4, performs a bitwise AND with R1, and stores the result in R1. The remote access takes approximately 5 microseconds. This is used in distributed bitmask operations where the mask is stored on a different blade.

Example 10: Power-of-two modulus using AND
```assembly
AND R1, #0x0F   ; R1 = R1 % 16 (if R1 is unsigned)
```

For unsigned integers, AND with (n-1) computes the remainder when dividing by a power of two n. This is much faster than a DIV instruction. The example computes R1 modulo 16. This works only when n is a power of two and the dividend is unsigned.

---

### 3.2 OR – Bitwise Logical OR

The OR instruction performs a bitwise logical OR operation between two operands. For each bit position, the result bit is 1 if at least one of the corresponding bits in the source operands is 1. The result bit is 0 only if both source bits are 0. The OR instruction is used for setting specific bits, combining flags, and implementing Boolean logic where any true condition yields true.

**Encoding Format**

OR uses opcode 0x21. The instruction format is identical to AND, with opcode 0x21 in the header. The flags field uses the same bits for vector mode and condition flag control. The operand descriptors follow the same pattern, with the destination being the accumulator and the source being the value to OR with.

The key difference between OR and AND is the logical operation performed. OR sets bits to 1 when either source bit is 1, while AND sets bits to 1 only when both source bits are 1. This asymmetry means that OR is used for setting bits (turning them on) while AND is used for clearing bits (turning them off).

**Operation Details**

The OR instruction uses the same bitwise logic unit as AND, but with OR gates instead of AND gates. For 512-bit operands, the logic unit consists of 512 independent OR gates operating simultaneously. The execution time is identical to AND: one cycle for register operands.

The condition flags are updated after every OR instruction. The zero flag is set if the result is zero. The sign flag is set to the most significant bit of the result. The carry and overflow flags are cleared.

**Assembly Examples**

Example 1: Simple bitwise OR
```assembly
OR R1, R2    ; R1 = R1 | R2 (bitwise)
```

This performs a bitwise OR between R1 and R2, storing the result in R1. Each bit of R1 becomes 1 if either the corresponding bit of R1 or R2 was 1. This is used to combine bit flags.

Example 2: Setting specific bits
```assembly
OR R1, #0x0F   ; Set low 4 bits of R1 to 1
```

This sets the low 4 bits of R1 to 1 without affecting the other bits. The immediate value has ones in the positions to set and zeros elsewhere. This is the complement of the AND clearing operation.

Example 3: Combining flag registers
```assembly
OR R1, R2   ; Combine error flags from two sources
```

If R1 contains error flags from one operation and R2 contains error flags from another, OR combines them so that the result has a flag set if either source had that flag set. This is used in status word accumulation.

Example 4: Converting ASCII digits
```assembly
OR R1, #0x30   ; Convert binary digit (0-9) to ASCII '0'-'9'
```

ASCII digits '0' through '9' are the binary values 0 through 9 plus 0x30. OR with 0x30 sets the high nibble to 0x3 while preserving the low nibble. This is faster than addition for this specific conversion.

Example 5: Force value to be odd
```assembly
OR R1, #1   ; R1 = R1 | 1 (guarantee low bit is set)
```

This forces the low bit of R1 to be 1, making the value odd regardless of its original value. This is used in algorithms that require odd numbers, such as certain primality tests.

Example 6: Building a composite value from fields
```assembly
OR R1, R2   ; R1 already contains high bits, OR in low bits
```

This sequence assumes R1 contains the high bits of a composite value and R2 contains the low bits with zeros in the high positions. OR combines them into a single register. This is used in constructing memory addresses from segment and offset.

Example 7: Vector bitwise OR
```assembly
OR.V R1, R2, R3   ; Vector OR: for each element, R1[i] = R2[i] | R3[i]
```

This performs bitwise OR on each element of two vectors. This is used in vectorized graphics operations where pixel values need to be combined using OR for certain compositing operations.

Example 8: Setting flags in a control register
```assembly
OR [control_reg], #ENABLE_BIT   ; Set enable bit in control register
```

This reads the control register from memory, ORs in the ENABLE_BIT, and writes it back. This is used to enable hardware features without disturbing other settings.

Example 9: Remote memory OR
```assembly
OR R1, @4:0x10000   ; R1 = R1 | value at remote address
```

This loads a value from remote memory, ORs it with R1, and stores the result in R1. This is used in distributed flag operations.

Example 10: Absolute value using OR and complement
```assembly
; Compute absolute value of signed integer in R1
MOV R2, R1
SAR R2, R2, #31   ; R2 = all ones if negative, zero if positive
XOR R1, R2        ; Complement if negative
SUB R1, R2        ; Add 1 if negative (two's complement negation)
```

This classic absolute value sequence uses OR implicitly through the XOR and SUB operations. The actual OR instruction is not used, but the pattern demonstrates how bitwise operations combine.

---

### 3.3 XOR – Bitwise Exclusive OR

The XOR instruction performs a bitwise exclusive OR operation between two operands. For each bit position, the result bit is 1 if the corresponding bits in the source operands are different. The result bit is 0 if they are the same. XOR has the useful property that XORing a value with itself produces zero, and XORing a value with zero leaves it unchanged.

**Encoding Format**

XOR uses opcode 0x22. The instruction format is identical to AND and OR, with opcode 0x22 in the header. The flags field uses the same bits for vector mode and condition flag control. The operand descriptors follow the same pattern.

XOR is particularly useful for toggling bits, zeroing registers, and implementing simple encryption. The property that `(A XOR B) XOR B = A` makes XOR its own inverse, which is valuable for cryptography and error correction.

**Operation Details**

The XOR instruction uses the bitwise logic unit with XOR gates. For 512-bit operands, the logic unit consists of 512 independent XOR gates. The execution time is one cycle for register operands.

The condition flags are updated after every XOR instruction. The zero flag is set if the result is zero. The sign flag is set to the most significant bit of the result. The carry and overflow flags are cleared.

**Assembly Examples**

Example 1: Simple bitwise XOR
```assembly
XOR R1, R2    ; R1 = R1 ^ R2 (bitwise)
```

This performs a bitwise XOR between R1 and R2, storing the result in R1. Bits that differ between R1 and R2 become 1; bits that are the same become 0.

Example 2: Zero a register
```assembly
XOR R1, R1    ; R1 = 0
```

XORing a register with itself produces zero. This is the fastest and most common way to zero a register, taking one cycle and requiring no immediate value. It also updates the zero flag, which can be used for conditional branches.

Example 3: Toggle specific bits
```assembly
XOR R1, #0x0F   ; Toggle low 4 bits of R1
```

This flips the low 4 bits of R1. Bits that were 0 become 1, and bits that were 1 become 0. The other bits are unchanged. This is used for invertible operations like toggling LED states.

Example 4: Simple XOR encryption
```assembly
XOR R1, key     ; Encrypt value in R1 with key
; ... later ...
XOR R1, key     ; Decrypt back to original
```

XOR encryption uses the property that XORing twice with the same key returns the original value. This is the basis of stream ciphers and one-time pads. The same instruction performs both encryption and decryption.

Example 5: Swapping registers without temporary
```assembly
XOR R1, R2    ; R1 = R1 ^ R2
XOR R2, R1    ; R2 = R2 ^ (R1 ^ R2) = R1
XOR R1, R2    ; R1 = (R1 ^ R2) ^ R1 = R2
```

This classic XOR swap exchanges the values of R1 and R2 without using a temporary register. Each XOR instruction modifies one register based on the current values. After three XORs, the values are swapped.

Example 6: Checking if two values are equal
```assembly
XOR R1, R2    ; R1 = R1 ^ R2
BRANCH zero, equal   ; Branch if result is zero (values were equal)
```

XOR produces zero only when the operands are equal. This is used to test equality without modifying the original values if a copy is made first. The example modifies R1, so a copy would be needed to preserve R1.

Example 7: Vector bitwise XOR
```assembly
XOR.V R1, R2, R3   ; Vector XOR: R1[i] = R2[i] ^ R3[i]
```

This performs bitwise XOR on each element of two vectors. This is used in vectorized encryption algorithms where each vector element is encrypted with the same key.

Example 8: Computing parity (simple version)
```assembly
XOR R1, R2    ; R1 = R1 ^ R2
XOR R1, R3    ; R1 = R1 ^ R3
AND R1, #1    ; Extract low bit for parity
```

This sequence computes the XOR of multiple values, which gives the parity (odd/even) of the number of set bits across all values when combined with population count. For simple parity, the low bit of the XOR of all values is the parity of the number of values.

Example 9: Remote memory XOR
```assembly
XOR R1, @4:0x10000   ; R1 = R1 ^ remote value
```

This loads a value from remote memory, XORs it with R1, and stores the result in R1. This is used in distributed encryption where the key is stored on a different blade.

Example 10: Gray code conversion
```assembly
; Convert binary to Gray code
XOR R1, R1, R1, LSR #1   ; R1 = R1 ^ (R1 >> 1)
```

Gray code is used in rotary encoders and error correction. The conversion from binary to Gray code is `gray = binary ^ (binary >> 1)`. This sequence (using a shift and XOR) computes the Gray code in a single instruction if the shift is combined, or two instructions otherwise.

---

### 3.4 NOT – Bitwise Logical NOT

The NOT instruction performs a bitwise logical NOT (one's complement) on a single operand. Each bit in the operand is inverted: 1 becomes 0, and 0 becomes 1. This is a unary operation, unlike AND, OR, and XOR which are binary. NOT is used for computing complements, implementing two's complement negation, and inverting flag conditions.

**Encoding Format**

NOT uses opcode 0x23. The instruction header contains opcode 0x23, flags, and operand count of 1. The single operand is both source and destination. The instruction inverts every bit of that operand and writes the result back.

The flags field has only bit 11 for suppressing condition flag updates. Vector mode is not applicable to NOT because the operation is applied uniformly across all bits regardless of element boundaries. Bits 8-10 and 12-15 are reserved.

The operand descriptor specifies a register or memory location. For memory operands, the instruction performs a read-modify-write cycle: the value is loaded from memory, inverted, and stored back. This is atomic with respect to other cores because the memory controller locks the cache line during the operation.

**Operation Details**

The NOT instruction executes in a single cycle for register operands. The bitwise logic unit inverts each bit using a NOT gate. For 512-bit operands, 512 NOT gates operate in parallel. The execution time is identical to AND, OR, and XOR.

The condition flags are updated after every NOT instruction. The zero flag is set if the result is zero. The sign flag is set to the most significant bit of the result. The carry and overflow flags are cleared.

**Assembly Examples**

Example 1: Simple bitwise NOT
```assembly
NOT R1    ; R1 = ~R1 (bitwise complement)
```

This inverts every bit of R1. Bits that were 1 become 0, and bits that were 0 become 1. This is the one's complement of the value.

Example 2: Two's complement negation
```assembly
NOT R1    ; R1 = ~R1
ADD R1, #1   ; R1 = ~R1 + 1 = -R1
```

Two's complement negation is computed by inverting all bits and adding 1. This sequence negates the value in R1. The NOT instruction performs the inversion, and the ADD adds 1.

Example 3: Bitwise NOT on memory
```assembly
NOT [R1]   ; Invert value at address R1 in place
```

This loads the value from memory at address R1, inverts it, and stores it back. The operation is atomic; no other core can access that memory location between the load and the store.

Example 4: Inverting condition flags
```assembly
NOT R1    ; Invert all bits, including condition flags if R1 holds flags
```

If R1 contains condition flags (or any bitmask), NOT inverts all condition bits. This is used to compute the complement of a condition (e.g., "not equal" instead of "equal").

Example 5: Creating a mask of all ones
```assembly
NOT R1    ; If R1 was zero, NOT makes it all ones
```

NOT of zero produces a register with all bits set to 1. This is useful for creating masks where every bit is set. The alternative (MOV with immediate -1) also works but NOT may be faster on some implementations.

Example 6: Computing absolute value using NOT
```assembly
; Alternative absolute value using NOT and ADD
MOV R2, R1
SAR R2, R2, #31   ; R2 = -1 if negative, 0 if positive
XOR R1, R2        ; Complement if negative
SUB R1, R2        ; Add 1 if negative
```

This sequence uses NOT implicitly through the XOR with all ones. The actual NOT instruction is not used, but the pattern demonstrates that NOT is equivalent to XOR with -1.

Example 7: Inverting a vector element-wise
```assembly
NOT.V R1, R2   ; Vector NOT: each element of R1 = ~element of R2
```

This inverts every bit of each element in the vector. For 512-bit vectors of 32-bit elements, this performs 16 NOT operations in parallel.

Example 8: Computing bitwise NAND
```assembly
AND R1, R2    ; R1 = R1 & R2
NOT R1        ; R1 = ~(R1 & R2) = NAND
```

NAND (NOT AND) is a universal logic gate; any Boolean function can be implemented using only NAND gates. This sequence computes the NAND of R1 and R2.

Example 9: Remote memory NOT
```assembly
NOT @4:0x10000   ; Invert value at remote address on blade 4
```

This inverts a value stored in remote memory on blade 4. The remote read and write take approximately 10 microseconds (5 each way). During this time, the core stalls.

Example 10: Signed magnitude to two's complement
```assembly
; Convert signed magnitude number in R1 to two's complement
CMP R1, #0
BRANCH positive, done
AND R1, #0x7FFFFFFF   ; Clear sign bit (assuming 32-bit)
NOT R1                ; Complement magnitude
ADD R1, #1            ; Add 1 to get two's complement negative
done:
```

Signed magnitude representation uses the high bit as sign and the remaining bits as magnitude. Converting to two's complement requires clearing the sign bit, then negating the magnitude if the original was negative. The NOT instruction performs the complement step.

---

### 3.5 TEST – Test Bits

The TEST instruction performs a bitwise AND between two operands but does not store the result. Only the condition flags are updated. TEST is used to examine specific bits without modifying any registers or memory locations. It is equivalent to AND followed by discarding the result, but TEST is encoded more compactly and explicitly indicates that the result is not needed.

**Encoding Format**

TEST uses opcode 0x24. The instruction header contains opcode 0x24, flags, and operand count of 2. The flags field has no bits defined except for bit 11 which suppresses condition flag updates (which would be pointless for TEST). Bits 8-10 and 12-15 are reserved.

The operand descriptors specify two sources. Neither operand is modified. The first operand is typically a register or memory location containing the value to test. The second operand is a mask, usually an immediate value or a register containing a mask.

**Operation Details**

The TEST instruction computes the bitwise AND of its two operands using the same logic unit as AND. The result is not stored anywhere; it is only used to update the condition flags. The zero flag is set if the AND result is zero. The sign flag is set to the most significant bit of the AND result. The carry and overflow flags are cleared.

Because TEST does not write any result, it does not require write bandwidth to the register file or memory. This makes TEST slightly more power-efficient than AND followed by a discard, and it avoids clobbering a register that might be needed later.

**Assembly Examples**

Example 1: Test a single bit
```assembly
TEST R1, #0x04   ; Test bit 2 (value 4) of R1
BRANCH not_zero, bit_set   ; Branch if bit 2 is set
```

This tests whether bit 2 of R1 is set. The mask 0x04 has only that bit set. The AND result is non-zero only if that bit is set. The branch checks the zero flag, which is cleared (not zero) when the bit is set.

Example 2: Test multiple bits (any)
```assembly
TEST R1, #0x0F   ; Test low 4 bits
BRANCH zero, none_set   ; Branch if none of the low 4 bits are set
```

This tests whether any of the low 4 bits are set. The mask has ones in all four positions. The AND result is zero only if all four bits are zero. The branch checks the zero flag; if set (result was zero), none of the bits were set.

Example 3: Test multiple bits (all)
```assembly
TEST R1, #0x0F   ; Test low 4 bits
CMP result, #0x0F   ; Need to check if all bits are set
```

TEST alone cannot test whether all bits in a mask are set because the AND result is non-zero if any bit is set. To test whether all bits are set, the programmer must use AND and then compare the result to the mask. This requires two instructions.

Example 4: Test sign bit
```assembly
TEST R1, #0x80000000   ; Test sign bit (32-bit)
BRANCH not_zero, negative   ; Branch if negative
```

The sign bit is the most significant bit. Testing it determines whether the value is negative (in two's complement representation). This is faster than comparing to zero because TEST does not require loading a zero immediate.

Example 5: Test for even/odd
```assembly
TEST R1, #1   ; Test low bit
BRANCH zero, even   ; Branch if low bit is 0 (even)
```

The low bit of an integer is 1 for odd numbers and 0 for even numbers. TEST with mask 1 tests this directly. This is faster than computing R1 % 2 using division.

Example 6: Test memory value
```assembly
TEST [R1], #0x80   ; Test high bit of byte at address R1
BRANCH not_zero, high_bit_set
```

This tests a bit in a memory location without loading the value into a register first. The memory controller reads the value, the ALU computes the AND, and the flags are updated. The value is discarded after the test.

Example 7: Test in a loop
```assembly
loop:
TEST [R1], #0x01   ; Test low bit of each byte in buffer
BRANCH not_zero, found   ; Exit if bit is set
ADD R1, #1         ; Advance pointer
CMP R1, R2         ; Check end of buffer
BRANCH less, loop
```

This loop scans a buffer for a byte with the low bit set. The TEST instruction tests each byte in place without modifying it or requiring a register load.

Example 8: Test remote memory
```assembly
TEST @4:0x10000, #0x01   ; Test remote bit on blade 4
BRANCH not_zero, remote_bit_set
```

This tests a bit in remote memory. The remote read takes approximately 5 microseconds. The branch checks the result without ever storing the remote value locally.

Example 9: Test using register mask
```assembly
TEST R1, R2   ; Test bits in R1 specified by mask in R2
BRANCH zero, no_bits_set
```

The mask does not have to be an immediate; it can come from a register. This allows dynamic testing where the mask varies at runtime. The branch checks whether any of the bits in the mask are set in R1.

Example 10: Test for power of two
```assembly
; Test if R1 is a power of two
MOV R2, R1
SUB R2, #1
AND R2, R1
TEST R2, #0   ; R2 is zero if power of two
BRANCH zero, is_power_of_two
```

A number is a power of two if it has exactly one bit set. The expression `(x & (x-1))` is zero exactly when x is a power of two (or zero). This sequence computes that expression and uses TEST to check if the result is zero. TEST with a zero mask is always zero, so this tests whether R2 is zero.

---

### 3.6 BSF – Bit Scan Forward

The BSF (Bit Scan Forward) instruction finds the index of the least significant set bit (lowest bit position containing a 1) in a source operand. The bit index is stored in the destination register, with bit 0 being the least significant bit. If the source operand is zero, the zero flag is set and the destination register is undefined. BSF is used in algorithms that process set bits one by one, such as finding the lowest set bit in a bitmask.

**Encoding Format**

BSF uses opcode 0x30. The instruction header contains opcode 0x30, flags, and operand count of 2. The first operand is the destination register for the bit index. The second operand is the source value to scan.

The flags field has bit 8 reserved for a special mode that returns the bit index plus one, which is useful for computing logarithms. Bits 9-15 are reserved.

The source operand can be a register or memory location. The destination must be a register. The source size can be 16, 32, 64, 128, 256, or 512 bits. The bit index is always stored in a 64-bit register, with the index ranging from 0 to (source size in bits minus 1).

**Operation Details**

The BSF instruction scans the source operand from bit 0 upward (least significant to most significant). It examines each bit in order until it finds a bit with value 1. The index of that bit is written to the destination register. If no bit is set (the source is zero), the zero flag is set and the destination register is not modified.

The scanning hardware is implemented using a priority encoder, a combinational circuit that finds the lowest set bit in constant time. For 512-bit operands, the priority encoder has 512 inputs and 9 outputs (since 2^9 = 512). The circuit uses a tree of smaller priority encoders to reduce gate delays. The entire operation takes one cycle.

**Assembly Examples**

Example 1: Find lowest set bit
```assembly
BSF R1, R2    ; R1 = index of lowest set bit in R2
BRANCH zero, no_bits   ; Branch if R2 was zero
```

This finds the position of the lowest set bit in R2. If R2 = 0b00001010 (decimal 10), the lowest set bit is at position 1 (2^1 = 2), so R1 becomes 1.

Example 2: Iterate over set bits
```assembly
loop:
BSF R1, R2        ; Find lowest set bit
BRANCH zero, done ; Exit when no bits remain
; Process bit at position R1
XOR R2, #1<<R1    ; Clear that bit (using shift)
BRANCH always, loop
```

This loop processes each set bit in R2 one by one. BSF finds the lowest set bit. The bit is cleared using XOR with a mask generated by shifting 1 left by the bit index. The loop continues until no bits remain.

Example 3: Find first non-zero byte
```assembly
BSF R1, R2        ; Find lowest set bit (position 0-7 for byte index)
SHR R1, R1, #3    ; Convert bit index to byte index
```

If R2 is a bitmask where each bit represents a byte, BSF finds the first byte with any set bit. Dividing the bit index by 8 gives the byte index. This is used in memory allocators to find free blocks.

Example 4: BSF on memory operand
```assembly
BSF R1, [R2]      ; Scan bits in memory at address R2
BRANCH zero, no_bits
```

This scans a value stored in memory without loading it into a register first. The memory controller reads the value, the priority encoder processes it, and the result is stored in R1. This saves a MOV instruction.

Example 5: BSF for binary logarithm floor
```assembly
BSF R1, R2        ; Does not give log2 (finds lowest bit, not highest)
```

BSF finds the lowest set bit, which is not the binary logarithm (which is the highest set bit). For logarithm, use BSR (Bit Scan Reverse) instead. BSF is used for different purposes.

Example 6: BSF for computing next power of two minus one
```assembly
BSF R1, R2        ; Find lowest set bit
NOT R2            ; Complement
ADD R2, #1        ; Add 1
BSF R1, R2        ; Find lowest set bit after transformation
```

This complex sequence is part of algorithms for finding the next power of two. The actual algorithm is more involved, but BSF is a key building block.

Example 7: BSF in a bitmap allocator
```assembly
; Allocate the first free block in a 512-bit allocation bitmap
BSF R1, [bitmap]   ; Find first free bit (assuming 0=free, 1=allocated)
CMP R1, #512
BRANCH greater_or_equal, no_free_blocks
; Mark block as allocated
OR [bitmap], #1<<R1   ; Set the bit (assuming 1=allocated)
```

This allocates the first free block in a bitmap where 0 indicates a free block. BSF finds the first zero bit. Because BSF finds ones, the bitmap is inverted or the allocation status is reversed.

Example 8: BSF on remote memory
```assembly
BSF R1, @4:0x10000   ; Scan bits in remote memory on blade 4
BRANCH zero, remote_no_bits
```

This scans a value in remote memory. The remote read takes approximately 5 microseconds. The priority encoding is performed locally after the data arrives.

Example 9: BSF for finding trailing zeros
```assembly
; Count trailing zeros in R2 (number of zeros before first 1)
BSF R1, R2        ; R1 = number of trailing zeros
```

The index of the lowest set bit is exactly the number of trailing zeros in the binary representation. This is used in the "count trailing zeros" operation, which is common in number theory and cryptography.

Example 10: BSF with bit index plus one
```assembly
BSF.P1 R1, R2     ; R1 = (index of lowest set bit) + 1 (if flag set)
```

The .P1 suffix (using bit 8 of flags) returns the bit index plus one. This is useful for algorithms that need a power of two or a shift amount. If the bit index is 3, the result is 4, which is 2^3.

---

### 3.7 BSR – Bit Scan Reverse

The BSR (Bit Scan Reverse) instruction finds the index of the most significant set bit (highest bit position containing a 1) in a source operand. The bit index is stored in the destination register, with bit 0 being the least significant bit. If the source operand is zero, the zero flag is set and the destination register is undefined. BSR is used to compute the floor of the binary logarithm, find the highest set bit for normalization, and implement priority encoders.

**Encoding Format**

BSR uses opcode 0x31. The instruction header contains opcode 0x31, flags, and operand count of 2. The format is identical to BSF, with the same flags and operand types. The only difference is the scan direction: BSR scans from the most significant bit downward, while BSF scans from the least significant bit upward.

The source operand can be a register or memory location. The destination must be a register. The source size can be 16, 32, 64, 128, 256, or 512 bits.

**Operation Details**

The BSR instruction scans the source operand from the most significant bit downward (from bit N-1 to bit 0). It examines each bit until it finds a bit with value 1. The index of that bit is written to the destination register. If no bit is set (the source is zero), the zero flag is set.

The scanning hardware uses a priority encoder that finds the highest set bit. For 512-bit operands, the priority encoder has 512 inputs and 9 outputs, similar to BSF but with reversed priority. The circuit uses a tree of smaller priority encoders. The entire operation takes one cycle.

**Assembly Examples**

Example 1: Find highest set bit
```assembly
BSR R1, R2    ; R1 = index of highest set bit in R2
BRANCH zero, no_bits   ; Branch if R2 was zero
```

This finds the position of the highest set bit in R2. If R2 = 0b00001010 (decimal 10), the highest set bit is at position 3 (2^3 = 8), so R1 becomes 3.

Example 2: Compute floor of binary logarithm
```assembly
BSR R1, R2    ; R1 = floor(log2(R2))
```

For a non-zero value R2, the index of the highest set bit is exactly the floor of the base-2 logarithm. This is used to compute the number of bits required to represent a number, or to find the nearest power of two.

Example 3: Normalize a floating-point mantissa
```assembly
BSR R1, R2        ; Find highest set bit in mantissa
SUB R1, #23       ; Subtract mantissa width (for 32-bit float)
SHL R2, R2, R1    ; Shift mantissa to normalize
```

Floating-point numbers store a mantissa with an implied leading 1. Normalization shifts the mantissa so that the highest set bit is in the correct position. BSR finds the shift amount.

Example 4: Find the next power of two
```assembly
BSR R1, R2        ; R1 = floor(log2(R2))
ADD R1, #1        ; R1 = floor(log2(R2)) + 1
MOV R3, #1
SHL R3, R3, R1    ; R3 = 2^(floor(log2(R2))+1) = next power of two
```

This computes the smallest power of two greater than or equal to R2. BSR gives the floor of the log, then adding 1 and shifting gives the next power. If R2 is already a power of two, this gives the next higher power, not the same power.

Example 5: BSR on memory operand
```assembly
BSR R1, [R2]      ; Scan bits in memory at address R2
BRANCH zero, no_bits
```

This scans a value stored in memory without loading it into a register first. The memory controller reads the value, the priority encoder processes it, and the result is stored in R1.

Example 6: BSR for priority encoding
```assembly
; Find the highest priority request in a bitmask (bit 0 = lowest priority)
BSR R1, requests   ; Highest set bit = highest priority
```

If higher priority is represented by higher bit positions, BSR directly gives the highest priority request. This is used in interrupt controllers and arbitration logic.

Example 7: BSR for leading zero count
```assembly
; Count leading zeros in 32-bit value R2
BSR R1, R2        ; R1 = floor(log2(R2))
SUB R1, #31, R1   ; Leading zeros = 31 - floor(log2(R2))
```

The number of leading zeros is computed from the position of the highest set bit. For a 32-bit value, the highest possible bit index is 31. Subtracting the BSR result from 31 gives the count of leading zeros.

Example 8: BSR on remote memory
```assembly
BSR R1, @4:0x10000   ; Scan bits in remote memory on blade 4
```

This scans a value in remote memory. The remote read takes approximately 5 microseconds. The result is the index of the highest set bit in that remote value.

Example 9: BSR for bit-reversal permutations
```assembly
BSR R1, R2        ; Find highest set bit
MOV R3, #1
SHL R3, R3, R1    ; Create mask of that bit
XOR R2, R3        ; Clear that bit
; Repeat for next highest bit
```

This loop extracts bits from highest to lowest, which can be used to reverse the order of bits or to implement certain permutations.

Example 10: BSR for detecting zero
```assembly
BSR R1, R2
BRANCH zero, value_is_zero   ; Branch if R2 was zero
; value is non-zero, R1 contains highest set bit index
```

The zero flag after BSR indicates whether the source was zero. This is more efficient than a separate CMP instruction because the flag is set as part of the scan.

---

### 3.8 SHL – Shift Left

The SHL (Shift Left) instruction shifts the bits of the first operand to the left by the number of positions specified by the second operand. Bits shifted out of the most significant position are lost, and zeros are shifted into the least significant positions. Shifting left by one position multiplies the value by two (for unsigned integers). SHL is used for multiplication by powers of two, extracting bit fields, and aligning data.

**Encoding Format**

SHL uses opcode 0x36. The instruction header contains opcode 0x36, flags, and operand count of 2. The first operand is the value to shift (destination). The second operand is the shift count. The result is stored in the destination.

The flags field has bit 8 for vector mode and bit 9 for saturating shift (where overflow beyond the maximum value is clamped). Bits 10-15 are reserved.

The shift count can be an immediate value or a register. If the shift count is in a register, only the low bits of the register are used (6 bits for 64-bit shifts, 7 bits for 128-bit shifts, etc.). Shift counts larger than the operand width produce a result of zero (for SHL) because all bits are shifted out.

**Operation Details**

The SHL instruction uses a barrel shifter, a combinational circuit that can shift a value by any amount in a single cycle. The barrel shifter consists of a series of multiplexers arranged in a logarithmic tree. For a 64-bit barrel shifter, there are 6 levels of multiplexers (2^6 = 64). The input is passed through each level, with each level either shifting by a power of two or not, based on the shift count bits.

The condition flags are updated after every SHL instruction. The zero flag is set if the result is zero. The sign flag is set to the most significant bit of the result. The carry flag is set to the last bit shifted out of the most significant position. The overflow flag is set if the sign of the result differs from the sign that would be expected from the original value multiplied by 2^count.

**Assembly Examples**

Example 1: Simple shift left
```assembly
SHL R1, #3    ; R1 = R1 << 3 (multiply by 8)
```

This shifts R1 left by 3 positions, which is equivalent to multiplying by 8. Bits 0-2 become zero, bit 3 becomes the original bit 0, etc. This is much faster than multiplication.

Example 2: Shift left by variable amount
```assembly
SHL R1, R2    ; R1 = R1 << (R2 & 0x3F)
```

This shifts R1 left by the number of bits specified in R2. Only the low 6 bits of R2 are used (for 64-bit operands). This is useful for variable scaling operations.

Example 3: Extract bit field from left
```assembly
SHL R1, #16   ; Shift left to align desired bits at the top
SHR R1, #16   ; Shift right to bring them to the bottom
```

This sequence extracts a bit field by shifting it to the top of the register (discarding higher bits), then shifting it back down to the bottom (discarding lower bits). The combined effect is a rotate, but the intermediate bits are cleared.

Example 4: Build a value from fields
```assembly
SHL R1, #16   ; Shift field 1 to high word
OR R1, R2     ; OR in field 2 (low word)
```

This builds a 32-bit value from two 16-bit fields. The first field is shifted left by 16 bits, then the second field is ORed into the low 16 bits.

Example 5: Vector shift left
```assembly
SHL.V R1, R2, #2   ; Each element of R1 = element of R2 << 2
```

This shifts each element of a vector left by the same amount. The vector length is specified in the flags field. For 512-bit vectors of 32-bit elements, this performs 16 shifts in parallel.

Example 6: Shift left with carry detection
```assembly
SHL R1, #1    ; R1 = R1 * 2
BRANCH carry, overflow   ; Branch if the high bit was set before shift
```

The carry flag after a left shift of 1 is set to the original most significant bit. This can be used to detect overflow when multiplying by 2, or to implement a shift-and-add multiplication algorithm.

Example 7: Power-of-two multiplication
```assembly
SHL R1, #10   ; R1 = R1 * 1024 (much faster than MUL)
```

Multiplying by a power of two using SHL is much faster than using MUL. The compiler automatically replaces multiplication by constants like 2, 4, 8, 16, etc. with SHL instructions.

Example 8: Remote memory shift
```assembly
SHL @4:0x10000, #3   ; Shift value at remote address left by 3
```

This shifts a value in remote memory. The remote read, shift, and write take approximately 10 microseconds (5 each way). The operation is atomic with respect to other cores.

Example 9: Saturating shift left
```assembly
SHL.S R1, #2   ; Shift left with saturation (clamp to max if overflow)
```

The .S suffix enables saturating shift. If shifting would cause overflow beyond the maximum representable value (or for signed values, beyond the most positive value), the result is clamped to the maximum. This is used in audio processing to prevent clipping.

Example 10: Shift for fixed-point arithmetic
```assembly
; Convert from integer to fixed-point with 16 fractional bits
SHL R1, #16    ; R1 = R1 * 65536 (now in fixed-point format)
```

Fixed-point numbers store an integer part and a fractional part in the same register. Converting an integer to fixed-point with 16 fractional bits requires shifting left by 16. This reserves the low 16 bits for the fractional part.

---

### 3.9 SHR – Shift Right

The SHR (Shift Right) instruction shifts the bits of the first operand to the right by the number of positions specified by the second operand. Bits shifted out of the least significant position are lost, and zeros are shifted into the most significant positions. Shifting right by one position divides the value by two (for unsigned integers). SHR is used for division by powers of two, extracting low-order bits, and unpacking data structures.

**Encoding Format**

SHR uses opcode 0x37. The instruction header contains opcode 0x37, flags, and operand count of 2. The format is identical to SHL, with the same flags and operand types. The direction is the only difference: SHR shifts right (toward less significant bits).

The shift count can be an immediate value or a register. Shift counts larger than the operand width produce a result of zero because all bits are shifted out.

**Operation Details**

The SHR instruction uses the same barrel shifter as SHL, but with the shift direction reversed. The barrel shifter can shift in either direction by reversing the order of the multiplexer stages. The operation takes one cycle.

The condition flags are updated after every SHR instruction. The zero flag is set if the result is zero. The sign flag is cleared because the most significant bit becomes zero (for SHR, not SAR). The carry flag is set to the last bit shifted out of the least significant position.

**Assembly Examples**

Example 1: Simple shift right
```assembly
SHR R1, #3    ; R1 = R1 >> 3 (divide by 8, unsigned)
```

This shifts R1 right by 3 positions, which is equivalent to unsigned division by 8. Bits 0-2 are lost, and zeros are shifted into bits 31-29.

Example 2: Extract low bits
```assembly
SHR R1, #16   ; R1 = R1 >> 16 (keep only high 16 bits)
SHL R1, #16   ; Shift back to align low bits
```

This extracts the high 16 bits of a 32-bit value by shifting right to bring them to the low position, then shifting left to restore their original alignment (with zeros in the low bits).

Example 3: Unsigned division by power of two
```assembly
SHR R1, #10   ; R1 = R1 / 1024 (unsigned)
```

Division by a power of two using SHR is much faster than using DIV. The compiler automatically replaces division by constants like 2, 4, 8, 16, etc. with SHR instructions for unsigned integers.

Example 4: Vector shift right
```assembly
SHR.V R1, R2, #2   ; Each element of R1 = element of R2 >> 2
```

This shifts each element of a vector right by the same amount. The vector length is specified in the flags field. For 512-bit vectors of 32-bit elements, this performs 16 shifts in parallel.

Example 5: Byte extraction from 32-bit word
```assembly
MOV R1, #0x12345678
SHR R1, #8      ; R1 = 0x00123456 (shift right by 8 bits = 1 byte)
AND R1, #0xFF   ; Extract low byte = 0x56
```

This extracts the low byte of a 32-bit word by shifting right by 8 bits, then masking. For extracting higher bytes, shifting by 16 or 24 bits is used.

Example 6: Shift right with carry detection
```assembly
SHR R1, #1    ; R1 = R1 >> 1
BRANCH carry, bit_was_set   ; Branch if low bit was set before shift
```

The carry flag after a right shift of 1 is set to the original least significant bit. This can be used to test whether a number is odd, or to implement shift-and-add multiplication algorithms.

Example 7: Align pointer to cache line
```assembly
SHR R1, #6    ; Divide by 64 (cache line size)
SHL R1, #6    ; Multiply by 64 (round down to cache line boundary)
```

This sequence rounds a pointer down to the nearest cache line boundary. Shifting right by 6 bits discards the low 6 bits (cache line offset), and shifting left restores the alignment.

Example 8: Remote memory shift right
```assembly
SHR @4:0x10000, #3   ; Shift value at remote address right by 3
```

This shifts a value in remote memory. The remote read, shift, and write take approximately 10 microseconds. The operation is atomic with respect to other cores.

Example 9: Extract bit field from the right
```assembly
; Extract 5-bit field starting at position 3
SHR R1, #3      ; Shift field to low bits
AND R1, #0x1F   ; Mask to keep only 5 bits
```

This extracts a bit field by first shifting the desired bits to the lowest positions, then masking to keep only the field width. The AND instruction performs the masking.

Example 10: Convert fixed-point to integer
```assembly
; Convert from fixed-point with 16 fractional bits to integer
SHR R1, #16    ; R1 = R1 / 65536 (integer part only)
```

Fixed-point numbers store an integer part and a fractional part in the same register. Converting to integer requires shifting right by the number of fractional bits, discarding the fractional part.

---

This concludes Chapter 3 of the Instruction Set Reference. The remaining chapters will cover Control Flow Instructions, Vector and SIMD Instructions, Advanced Math Functions, Probabilistic Inference Instructions, System Instructions, Interconnect Instructions, Memory Management Instructions, and Protection Instructions. Each instruction will be documented with the same level of detail.

# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 4: Control Flow Instructions

### 4.1 JMP – Unconditional Jump

The JMP instruction transfers execution control to a specified address unconditionally. The instruction pointer is set to the target address, and execution continues from that location. Unlike conditional branches, JMP does not examine any flags or conditions; it always transfers control. JMP is used for implementing loops, switch statements, jump tables, and for bypassing sections of code.

**Encoding Format**

JMP uses opcode 0x40. The instruction header contains opcode 0x40, flags, and operand count of 1. The single operand specifies the target address. The flags field has bit 8 reserved for a far jump (changing code segment), bit 9 for an indirect jump through a register, and bit 10 for a jump through memory. Bits 11-15 are reserved.

The target address can be specified in several ways. For a direct jump, the target is an immediate address encoded in the instruction payload. For a register indirect jump, the target is the address contained in a register. For a memory indirect jump, the target is the address stored at a memory location. The operand descriptor specifies which addressing mode is used.

The size of the target address depends on the addressing mode. For direct jumps within the same segment, the target is a 64-bit offset from the current instruction pointer. For far jumps, the target includes both a segment selector and an offset, totaling 80 bits. The instruction payload size varies accordingly.

**Operation Details**

When a JMP instruction executes, the following steps occur. The target address is computed based on the operand addressing mode. For direct jumps, the address is extracted from the instruction stream. For indirect jumps, the address is read from a register or from memory. The computed address is then written to the instruction pointer register.

The instruction pipeline is flushed when a JMP executes because the processor cannot predict the new instruction stream with certainty. The fetch unit begins fetching instructions from the new address in the next cycle. There is a small bubble in the pipeline (typically 2-3 cycles) while the new instructions are fetched and decoded. This bubble is unavoidable but is minimized by the branch predictor, which attempts to prefetch the target address before the JMP executes.

For far jumps that change the code segment, additional steps are required. The segment descriptor for the new code segment is loaded from the segment table. The hardware checks that the current owner has execute permission for that segment. If the permission check fails, a protection fault is raised before any code from the new segment is executed.

**Assembly Examples**

Example 1: Direct jump to label
```assembly
JMP target_label
; ... code skipped ...
target_label:
```

This is the simplest form of JMP. The assembler computes the distance from the current instruction to target_label and encodes it as an immediate offset. Execution continues at target_label.

Example 2: Jump through register
```assembly
JMP R1    ; Jump to address stored in R1
```

The address in R1 becomes the new instruction pointer. This is used for implementing jump tables, function pointers, and dynamic dispatch. The register can be loaded from memory or computed at runtime.

Example 3: Jump through memory
```assembly
JMP [R1]   ; Jump to address stored at memory location R1
```

This loads the target address from memory at the address in R1, then jumps to that address. This is used for implementing virtual function tables and certain forms of dynamic linking.

Example 4: Far jump to different code segment
```assembly
JMP.FAR 0x08:0x10000   ; Jump to segment 8, offset 0x10000
```

The .FAR suffix indicates a far jump that changes the code segment. The target is specified as segment:offset. This is used in operating system kernels to switch between different privilege levels or to call code in a different protection domain.

Example 5: Jump for loop implementation
```assembly
MOV R1, #0
loop_start:
; loop body
ADD R1, #1
CMP R1, #100
JNE loop_start   ; Equivalent to JMP if condition not met
```

The JNE instruction is a conditional branch; JMP would create an infinite loop. However, an unconditional JMP can be used at the end of a loop that always repeats:
```assembly
loop_start:
; loop body
JMP loop_start   ; Infinite loop (use with caution)
```

Example 6: Jump table implementation
```assembly
; R1 contains case index (0-3)
LEA R2, jump_table   ; R2 = address of jump table
SHL R1, #3           ; Multiply by 8 (address size)
ADD R2, R1           ; R2 = address of jump table entry
JMP [R2]             ; Jump to address stored in table

jump_table:
DQ case0_address
DQ case1_address
DQ case2_address
DQ case3_address
```

This is a classic jump table implementation for a switch statement. The index is scaled by the address size (8 bytes for 64-bit addresses), added to the table base, and the resulting memory location contains the target address.

Example 7: Remote jump
```assembly
JMP @4:0x10000   ; Jump to address on blade 4
```

This jumps to code located on a remote blade. The hardware sends a request across the optical fabric to blade 4, which begins executing from address 0x10000. The local blade's instruction pointer is updated to reflect the remote execution context. This enables distributed computing where code can be executed on the blade where the data resides.

Example 8: Short jump optimization
```assembly
JMP.S short_target   ; Short jump (8-bit offset)
```

The .S suffix indicates a short jump with an 8-bit offset. This uses less instruction space (only 2 bytes total) but can only reach targets within -128 to +127 bytes of the current instruction pointer. The assembler automatically selects the smallest encoding that can reach the target.

Example 9: Near jump optimization
```assembly
JMP.N near_target    ; Near jump (32-bit offset)
```

The .N suffix indicates a near jump with a 32-bit offset. This uses 5 bytes of instruction space and can reach any target within the same 4GB code segment. This is the default for most jumps in 64-bit code when the target is within the same segment.

Example 10: Far jump to hypervisor
```assembly
JMP.FAR hypervisor_entry   ; Jump to hypervisor code
```

In a virtualized environment, this far jump transfers control from a guest operating system to the hypervisor. The segment change triggers a privilege level change, and the hardware saves the current execution context before transferring control.

---

### 4.2 CALL – Call Subroutine

The CALL instruction transfers control to a subroutine while saving the return address so that execution can resume after the subroutine completes. The return address (the address of the instruction following the CALL) is pushed onto a hardware return stack. The instruction pointer is then set to the target address. CALL is used for implementing functions, procedures, and methods in high-level languages.

**Encoding Format**

CALL uses opcode 0x41. The instruction header contains opcode 0x41, flags, and operand count of 1. The operand specifies the target address, using the same addressing modes as JMP. The flags field has bit 8 for far calls (changing code segment), bit 9 for indirect calls through a register, and bit 10 for calls through memory. Bits 11-15 are reserved.

The return address is automatically pushed onto the hardware return stack. The return stack is separate from the data stack and is not accessible to software. This prevents corruption of return addresses and enables hardware support for return prediction. The return stack has 64 entries, sufficient for most call depths.

**Operation Details**

When a CALL instruction executes, the following steps occur. The address of the next instruction (current instruction pointer plus the length of the CALL instruction) is computed. This return address is pushed onto the hardware return stack. The target address is computed based on the operand addressing mode. The computed address is written to the instruction pointer.

The hardware return stack is a circular buffer with 64 entries. Each push stores the return address and increments the stack pointer. If the stack overflows (more than 64 nested calls), the oldest entry is overwritten, and the return predictor may produce incorrect predictions. The operating system can increase the effective stack depth by spilling the return stack to memory on deep call chains.

For far calls that change the code segment, additional steps are required. The return address includes both the current segment and offset. The segment descriptor for the new code segment is loaded and checked for execute permission. The previous segment is saved along with the return address.

**Assembly Examples**

Example 1: Simple subroutine call
```assembly
CALL subroutine
; ... code executed after subroutine returns ...
subroutine:
; subroutine body
RET
```

This calls the subroutine at label "subroutine". The return address (the instruction after the CALL) is saved. When the subroutine executes RET, control returns to that address.

Example 2: Call through register
```assembly
CALL R1    ; Call function whose address is in R1
```

The address in R1 becomes the subroutine entry point. This is used for calling function pointers, virtual functions, and callback functions. The register can be loaded from a virtual function table or passed as an argument.

Example 3: Call through memory
```assembly
CALL [R1]   ; Call function whose address is stored at memory address R1
```

This loads the target address from memory at the address in R1, then calls that address. This is used for calling functions through pointer-to-pointer indirection, such as in certain dynamic linking schemes.

Example 4: Far call to different segment
```assembly
CALL.FAR 0x08:0x10000   ; Call code in segment 8, offset 0x10000
```

The .FAR suffix indicates a far call that changes the code segment. The return address includes the current segment. This is used for system calls, calling kernel code from user space, and inter-segment function calls.

Example 5: Nested subroutine calls
```assembly
CALL outer
; ... returns here after outer and inner complete
outer:
CALL inner
RET
inner:
RET
```

This demonstrates nested calls. The return stack stores both return addresses. When inner returns, the top of the stack is the address after the CALL inner. When outer returns, the next address is the original return address.

Example 6: Call with argument passing (via registers)
```assembly
; Caller:
MOV R1, #42      ; First argument
MOV R2, #100     ; Second argument
CALL add_two
; Result is in R3

; Callee:
add_two:
ADD R3, R1, R2   ; R3 = R1 + R2
RET
```

Arguments are passed in registers. This is the standard calling convention for leaf functions and small argument counts. The caller loads arguments into registers, then calls the subroutine. The subroutine performs its computation and returns the result in a register.

Example 7: Call with stack arguments (for many arguments)
```assembly
; Caller:
SUB SP, #32      ; Allocate stack space for arguments
MOV [SP], #1     ; First argument
MOV [SP+8], #2   ; Second argument
MOV [SP+16], #3  ; Third argument
MOV [SP+24], #4  ; Fourth argument
CALL sum_four
ADD SP, #32      ; Deallocate stack space

; Callee:
sum_four:
ADD R1, [SP+8], [SP+16]   ; Add arguments 2 and 3
ADD R1, R1, [SP+24]       ; Add argument 4
ADD R1, R1, [SP]          ; Add argument 1
RET
```

For functions with many arguments, arguments are passed on the stack. The caller allocates stack space, writes arguments, then calls. The callee reads arguments from the stack. The return address is stored in the hardware return stack, not on the software stack.

Example 8: Tail call optimization
```assembly
; Instead of:
CALL subroutine
RET

; Use:
JMP subroutine   ; Tail call (no return needed)
```

When a function ends with a call to another function, the call can be replaced with a jump. This is called tail call optimization. The return address of the current function becomes the return address of the called function. This saves stack space and improves performance.

Example 9: Remote procedure call
```assembly
CALL @4:0x10000   ; Call function on blade 4
```

This calls a function located on a remote blade. The hardware sends the call request across the optical fabric. The remote blade executes the function and returns the result. The local blade's return stack stores the return address, and execution resumes after the remote call completes. This enables distributed computing with transparent remote procedure calls.

Example 10: Far call to system service
```assembly
; System call convention:
; R1 = system call number
; R2, R3 = arguments
CALL.FAR system_service_entry   ; Far call to kernel segment
```

This far call transfers control from user code to the operating system kernel. The segment change also changes the privilege level. The hardware saves the user segment and return address before entering the kernel. When the kernel executes the far return, it restores the user segment and returns to user code.

---

### 4.3 RET – Return from Subroutine

The RET instruction returns control from a subroutine to the calling function. The return address is popped from the hardware return stack and written to the instruction pointer. Execution continues at the instruction following the original CALL. RET is always used in conjunction with CALL and marks the end of a subroutine.

**Encoding Format**

RET uses opcode 0x42. The instruction header contains opcode 0x42, flags, and operand count of 0. There are no operands because the return address is obtained from the hardware return stack. The flags field has bit 8 for far returns (changing code segment), bit 9 for returning with a stack adjustment (popping additional arguments), and bit 10 for returning from an interrupt handler. Bits 11-15 are reserved.

The flags field may also contain an immediate value for the number of argument bytes to pop in calling conventions where the callee cleans the stack. This immediate is encoded in bits 11-15, allowing up to 31 argument bytes to be popped.

**Operation Details**

When a RET instruction executes, the following steps occur. The top of the hardware return stack is popped, providing the return address. This address is written to the instruction pointer. The pipeline is flushed, and fetch begins from the return address.

If the return stack is empty (no corresponding CALL), a return stack underflow exception is raised. This indicates a programming error, typically a mismatched CALL and RET.

For far returns, the return address includes a segment selector. The hardware loads the segment descriptor for that segment and checks that the current owner has execute permission. The privilege level may change as part of the far return, restoring the previous privilege level.

If the RET instruction includes a stack adjustment immediate, the software stack pointer is incremented by that amount after the return address is popped. This implements the "callee cleans the stack" calling convention.

**Assembly Examples**

Example 1: Simple return
```assembly
subroutine:
; subroutine body
RET   ; Return to caller
```

This is the simplest form of RET. It pops the return address from the hardware stack and jumps to it. The caller's execution resumes at the instruction after the CALL.

Example 2: Far return
```assembly
kernel_entry:
; kernel code
RET.FAR   ; Return to user code with segment change
```

The .FAR suffix indicates a far return that changes the code segment. This is used when returning from a far CALL. The hardware restores the previous code segment and privilege level.

Example 3: Return with argument cleanup
```assembly
subroutine:
; subroutine body that uses 8 bytes of stack arguments
RET #8   ; Return and pop 8 argument bytes from stack
```

This form of RET pops the return address, then adds 8 to the software stack pointer. This implements the "callee cleans the stack" calling convention used by the Pascal language and some C compilers for variadic functions.

Example 4: Return from interrupt handler
```assembly
interrupt_handler:
; save context, handle interrupt, restore context
RET.I   ; Return from interrupt, restoring saved flags
```

The .I suffix indicates a return from an interrupt handler. This form of RET also restores the saved condition flags and other privileged state that was saved when the interrupt occurred.

Example 5: Leaf function return
```assembly
leaf_function:
ADD R1, R1, #1   ; Simple operation
RET              ; Return immediately
```

A leaf function (one that does not call other functions) has a simple RET at the end. The return stack has exactly one entry, which is popped and used as the return address.

Example 6: Nested return sequence
```assembly
outer:
CALL inner
RET
inner:
RET
```

When inner executes RET, it returns to the instruction after CALL inner in outer. When outer executes RET, it returns to the caller of outer. The hardware return stack manages both return addresses correctly.

Example 7: Return from remote call
```assembly
; On remote blade:
remote_function:
; ... perform work ...
RET   ; Return to caller on original blade
```

When a remote function executes RET, the hardware sends a return message across the optical fabric. The calling blade receives the return notification and resumes execution. The remote return address is not stored locally; it is managed by the remote blade's hardware.

Example 8: Return with value in register
```assembly
; Caller:
CALL compute
; R1 now contains result

; Callee:
compute:
MOV R1, #42   ; Result in R1
RET
```

Results are returned in registers, typically R1 for integer results and FP1 for floating-point results. The RET instruction does not modify registers, so the result is preserved across the return.

Example 9: Return stack overflow handling
```assembly
; For very deep recursion (more than 64 levels)
deep_recursive:
SUB SP, #8        ; Allocate stack space for return address
MOV [SP], LR      ; Store return address to memory
; ... recursive call ...
MOV LR, [SP]      ; Restore return address from memory
ADD SP, #8        ; Deallocate stack space
RET
```

When the hardware return stack overflows (more than 64 nested calls), the operating system must spill return addresses to memory. This code sequence shows how a function can manually manage return addresses to avoid relying on the hardware stack.

Example 10: Return from fault handler
```assembly
page_fault_handler:
; Handle the page fault
; Fix the memory mapping
RET.F   ; Return to faulting instruction (re-execute it)
```

The .F suffix (fault return) returns to the instruction that caused the fault, rather than the next instruction. This is used in page fault handlers and other exception handlers where the faulting instruction must be retried after the condition that caused the fault has been corrected.

---

### 4.4 BRANCH – Conditional Branch

The BRANCH instruction transfers control to a target address if a specified condition is true, based on the condition flags. If the condition is false, execution continues with the next instruction. Conditional branches are the foundation of control flow in programs, enabling if statements, loops, switch statements, and all forms of conditional execution.

**Encoding Format**

BRANCH uses opcode 0x43. The instruction header contains opcode 0x43, flags, and operand count of 1. The operand specifies the target address, using the same addressing modes as JMP. The condition to test is encoded in the flags field.

The condition is specified by bits 8-11 of the flags field. The following conditions are defined:

- 0000: EQ (equal, zero flag set)
- 0001: NE (not equal, zero flag clear)
- 0010: LT (signed less than, sign flag not equal overflow flag)
- 0011: LE (signed less or equal, zero flag set or sign not equal overflow)
- 0100: GT (signed greater than, zero flag clear and sign equals overflow)
- 0101: GE (signed greater or equal, sign equals overflow)
- 0110: LO (unsigned lower, carry flag clear)
- 0111: LS (unsigned lower or same, carry flag clear or zero set)
- 1000: HI (unsigned higher, carry flag set and zero clear)
- 1001: HS (unsigned higher or same, carry flag set)
- 1010: CS (carry set)
- 1011: CC (carry clear)
- 1100: VS (overflow set)
- 1101: VC (overflow clear)
- 1110: MI (negative, sign flag set)
- 1111: PL (positive or zero, sign flag clear)

Bits 12-15 are reserved for future condition extensions.

**Operation Details**

When a BRANCH instruction executes, the condition flags are examined. If the specified condition is true, the target address is computed and written to the instruction pointer, and the pipeline is flushed. If the condition is false, execution continues with the next instruction.

The branch predictor attempts to guess whether the branch will be taken before the condition is evaluated. For backward branches (jumping to a lower address, typical of loops), the predictor assumes taken. For forward branches, the predictor assumes not taken. More sophisticated predictors use a branch history table to record the outcomes of previous executions of the same branch.

**Assembly Examples**

Example 1: Branch if equal
```assembly
CMP R1, R2
BRANCH EQ, equal_label   ; Branch if R1 == R2
```

This tests whether R1 and R2 are equal. The CMP instruction sets the condition flags. The BRANCH with EQ condition transfers control to equal_label if the zero flag is set (indicating equality).

Example 2: Branch if greater than (signed)
```assembly
CMP R1, R2
BRANCH GT, greater_label   ; Branch if R1 > R2 (signed)
```

This tests whether R1 is greater than R2 in signed integer comparison. The GT condition checks that the zero flag is clear and the sign flag equals the overflow flag.

Example 3: Branch if less than (unsigned)
```assembly
CMP R1, R2
BRANCH LO, lower_label   ; Branch if R1 < R2 (unsigned)
```

This tests whether R1 is lower than R2 in unsigned integer comparison. The LO condition checks that the carry flag is clear (indicating that R1 - R2 did not require a borrow).

Example 4: Loop with conditional branch
```assembly
MOV R1, #0
loop:
; loop body
ADD R1, #1
CMP R1, #100
BRANCH LT, loop   ; Branch back if R1 < 100
```

This implements a loop that executes 100 times. The loop counter R1 is incremented each iteration. The CMP compares it to 100. The LT condition branches back to the start of the loop while the counter is less than 100.

Example 5: If-then-else structure
```assembly
CMP R1, R2
BRANCH EQ, then_case
else_case:
; code for else
JMP end_if
then_case:
; code for then
end_if:
```

This implements an if-then-else structure. If the condition is true, the branch jumps to then_case. If false, execution falls through to else_case. The JMP at the end of else_case skips the then_case code.

Example 6: Short-circuit evaluation
```assembly
CMP R1, #0
BRANCH EQ, short_circuit   ; If R1 == 0, skip second test
CMP R2, #0
BRANCH EQ, short_circuit   ; If R2 == 0, skip to short_circuit
; both non-zero
```

This implements short-circuit logical AND. If R1 is zero, the code jumps to short_circuit without testing R2. This matches the semantics of the C && operator.

Example 7: Branch with condition from previous instruction
```assembly
ADD R1, R2
BRANCH VS, overflow_handler   ; Branch if addition overflowed
```

The ADD instruction sets the overflow flag if signed overflow occurred. The BRANCH instruction immediately after tests the overflow flag and branches to the overflow handler if set.

Example 8: Branch if carry set (for multi-precision)
```assembly
ADD R1, R2      ; Add low 64 bits
BRANCH CS, carry_handler   ; Branch if carry out
ADD R3, R4      ; Add high 64 bits (without carry since no branch)
```

This adds the low 64 bits of a 128-bit number. If a carry is generated, the CS branch jumps to a handler that adds the carry to the high bits. If no carry, execution continues with the high addition.

Example 9: Remote conditional branch
```assembly
CMP R1, @4:0x10000   ; Compare R1 with remote value
BRANCH EQ, remote_equal   ; Branch if equal
```

This compares a local register with a remote memory value. The remote read takes approximately 5 microseconds. The BRANCH then tests the condition flags and may jump to remote_equal on the same blade or potentially on a remote blade (using a remote label).

Example 10: Branch prediction hint
```assembly
BRANCH.PT EQ, likely_taken   ; Branch with "predict taken" hint
BRANCH.PN EQ, unlikely_taken ; Branch with "predict not taken" hint
```

The .PT and .PN suffixes provide hints to the branch predictor. .PT (predict taken) tells the hardware that this branch is likely to be taken, so it should prefetch instructions from the target. .PN (predict not taken) tells the hardware to prefetch from the fall-through path. These hints can improve performance when the programmer knows the likely outcome.

---

This concludes Chapter 4 of the Instruction Set Reference. The remaining chapters will cover Vector and SIMD Instructions, Advanced Math Functions, Probabilistic Inference Instructions, System Instructions, Interconnect Instructions, Memory Management Instructions, and Protection Instructions. Each instruction will be documented with the same level of detail.

# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 5: Vector and SIMD Instructions

### 5.1 ADDPS – Add Packed Single-Precision Floating-Point

The ADDPS instruction performs element-wise addition on packed single-precision floating-point values. A single instruction adds multiple pairs of floating-point numbers simultaneously, dramatically increasing throughput for graphics, scientific computing, and machine learning workloads. The "PS" suffix stands for "Packed Single-precision," indicating that each operand is a vector of 32-bit floating-point values.

**Encoding Format**

ADDPS uses opcode 0x50. The instruction header contains opcode 0x50, flags, and operand count of 3. The first operand is the destination vector. The second and third operands are the source vectors. The instruction computes destination[i] = source1[i] + source2[i] for each element i in the vector.

The flags field controls the vector length and rounding behavior. Bits 8-9 encode the vector length: 00 for 128-bit vectors (4 floats), 01 for 256-bit vectors (8 floats), 10 for 512-bit vectors (16 floats), and 11 for 1024-bit vectors (32 floats). Bits 10-12 encode the rounding mode for the addition. Bits 13-15 are reserved.

The vector operands must be aligned to their natural boundaries: 16-byte alignment for 128-bit vectors, 32-byte for 256-bit vectors, 64-byte for 512-bit vectors, and 128-byte for 1024-bit vectors. Misaligned operands cause an alignment exception, though the hardware can handle misaligned operands with a performance penalty.

**Operation Details**

The ADDPS instruction executes in a single cycle for vector lengths up to 512 bits when the operands are in registers. The floating-point adder unit contains multiple parallel adders: 4 for 128-bit vectors, 8 for 256-bit, 16 for 512-bit, and 32 for 1024-bit. Each adder operates independently on its pair of floating-point values.

The addition follows the IEEE 754 standard for floating-point arithmetic. Special values (infinity, NaN, denormals) are handled correctly. The rounding mode can be specified in the instruction flags, overriding the default rounding mode set in the floating-point control register.

For memory operands, the ADDPS instruction can perform vector loads as part of the operation. The memory controller fetches the entire vector in a single burst, and the adders begin processing as soon as the first elements arrive. This overlap of memory access and computation reduces the effective latency.

**Assembly Examples**

Example 1: Add two 128-bit vectors (4 floats)
```assembly
ADDPS XMM1, XMM2, XMM3   ; XMM1 = XMM2 + XMM3 (4 floats)
```

This adds the four 32-bit floating-point values in XMM2 to the four values in XMM3, storing the four results in XMM1. This is 4 times faster than performing four scalar ADD instructions.

Example 2: Add 256-bit vectors (8 floats)
```assembly
ADDPS.Y YMM1, YMM2, YMM3   ; YMM1 = YMM2 + YMM3 (8 floats)
```

The .Y suffix selects 256-bit vector length (8 floats). This performs 8 additions in parallel, suitable for AVX-style programming.

Example 3: Add 512-bit vectors (16 floats)
```assembly
ADDPS.Z ZMM1, ZMM2, ZMM3   ; ZMM1 = ZMM2 + ZMM3 (16 floats)
```

The .Z suffix selects 512-bit vector length (16 floats). This is the maximum vector length for the standard Math cores.

Example 4: Add vector from memory
```assembly
ADDPS XMM1, XMM2, [R1]   ; XMM1 = XMM2 + memory vector at R1
```

This adds a vector in register XMM2 to a vector stored in memory at address R1. The memory controller loads the 16 bytes (4 floats) from address R1 in a single burst.

Example 5: Add broadcast scalar to vector
```assembly
ADDPS XMM1, XMM2, XMM3_S   ; XMM1 = XMM2 + (XMM3[0] broadcast to all lanes)
```

The _S suffix indicates that the second source is a scalar broadcast from the low element of the vector register. This adds the same scalar value to every element of the vector.

Example 6: Vector addition for image blending
```assembly
; Blend two 4-pixel RGBA quads (16 bytes each)
ADDPS XMM1, XMM2, XMM3   ; Add color components
MULPS XMM1, XMM1, #0.5   ; Average (multiply by 0.5)
```

This blends two images by adding corresponding pixel values and then multiplying by 0.5 to compute the average. Four pixels are processed simultaneously.

Example 7: Remote vector addition
```assembly
ADDPS XMM1, XMM2, @4:0x10000   ; Add remote vector to local vector
```

This adds a vector stored on blade 4 to a local vector. The remote read takes approximately 5 microseconds, after which the addition proceeds at full speed.

Example 8: Vector addition with different rounding
```assembly
ADDPS.RZ XMM1, XMM2, XMM3   ; Add with round-toward-zero
```

The .RZ suffix sets the rounding mode to round-toward-zero. This is useful for interval arithmetic and for implementing certain numerical algorithms that require deterministic rounding.

Example 9: Horizontal addition (sum of vector elements)
```assembly
; No direct horizontal add in ADDPS, use HADDPS instead
HADDPS XMM1, XMM2, XMM3   ; Horizontal add (see separate instruction)
```

ADDPS performs element-wise addition, not horizontal addition. For horizontal addition (summing all elements of a vector), the HADDPS instruction is used.

Example 10: Masked vector addition
```assembly
; Assume mask in K1 register (512-bit mask, 16 bits)
ADDPS.K ZMM1, ZMM2, ZMM3, K1   ; Add only where mask bit is 1
```

The .K suffix enables masked execution. Only elements where the corresponding bit in mask register K1 is 1 are added; other elements are copied unchanged from ZMM1. This implements conditional vector operations.

---

### 5.2 MULPS – Multiply Packed Single-Precision Floating-Point

The MULPS instruction performs element-wise multiplication on packed single-precision floating-point values. It follows the same pattern as ADDPS but with multiplication instead of addition. MULPS is essential for scaling vectors, computing dot products (in combination with ADDPS), and implementing matrix multiplication.

**Encoding Format**

MULPS uses opcode 0x51. The instruction format is identical to ADDPS, with opcode 0x51 in the header. The flags field uses the same bits for vector length and rounding mode. The operand count is 3: destination, source1, and source2.

The multiplication follows IEEE 754 standards. Special values are handled correctly. Denormal inputs are treated as zero unless the flush-to-zero mode is enabled in the floating-point control register.

**Operation Details**

The MULPS instruction executes in a single cycle for vector lengths up to 512 bits when the operands are in registers. The floating-point multiplier unit contains parallel multipliers: 4 for 128-bit vectors, 8 for 256-bit, 16 for 512-bit, and 32 for 1024-bit. Each multiplier operates independently.

Floating-point multiplication is more complex than addition but still fits within a single cycle at 2 GHz. The multiplier uses a Wallace tree reduction for the mantissa product, followed by exponent addition and normalization. The result is rounded according to the specified rounding mode.

**Assembly Examples**

Example 1: Multiply two 128-bit vectors
```assembly
MULPS XMM1, XMM2, XMM3   ; XMM1 = XMM2 * XMM3 (4 floats)
```

This multiplies the four floats in XMM2 by the four floats in XMM3, storing the results in XMM1. This is 4 times faster than four scalar MUL instructions.

Example 2: Scale vector by scalar
```assembly
MULPS XMM1, XMM2, XMM3_S   ; XMM1 = XMM2 * XMM3[0] (broadcast)
```

This multiplies every element of XMM2 by the scalar value in the low element of XMM3. This is the standard way to scale an entire vector by a constant.

Example 3: Square vector elements
```assembly
MULPS XMM1, XMM2, XMM2   ; XMM1 = XMM2 * XMM2 (element-wise squares)
```

Multiplying a vector by itself squares each element. This is used in Euclidean distance calculations: `distance = sqrt(sum(x_i^2))`.

Example 4: 4x4 matrix multiplication (row by vector)
```assembly
; Multiply 4x4 matrix (rows in YMM0-YMM3) by 4-element vector (XMM4)
; Result in XMM5
MULPS XMM5, YMM0, XMM4_S   ; Row0 * vector (broadcast)
HADDPS XMM5, XMM5, XMM5    ; Horizontal sum (partial)
```

This shows the beginning of a matrix-vector multiplication. Each matrix row is multiplied element-wise by the vector, then the results are summed horizontally.

Example 5: Vector multiplication with memory operand
```assembly
MULPS XMM1, XMM2, [R1]   ; XMM1 = XMM2 * memory vector at R1
```

This multiplies a vector in XMM2 by a vector stored in memory. The memory is accessed as a single 16-byte burst.

Example 6: Complex multiplication using MULPS
```assembly
; Multiply complex numbers: (a+ib)*(c+id) = (ac-bd) + i(ad+bc)
; Real parts in XMM0[0], XMM1[0]; Imag parts in XMM0[1], XMM1[1]
MULPS XMM2, XMM0, XMM1      ; ac, ad, bc, bd (interleaved)
; ... additional shuffles and adds ...
```

Complex multiplication requires four real multiplications. MULPS can perform them in parallel if the data is arranged appropriately.

Example 7: Remote vector multiplication
```assembly
MULPS XMM1, XMM2, @4:0x10000   ; Multiply by remote vector
```

This multiplies a local vector by a vector stored on blade 4. The remote read takes approximately 5 microseconds, after which the multiplication proceeds at full speed.

Example 8: Element-wise multiplication for Hadamard product
```assembly
; Hadamard product (element-wise product) of two matrices
MULPS YMM1, YMM2, YMM3   ; Process 8 elements at once
```

The Hadamard product is simply element-wise multiplication. MULPS processes 8 elements at a time from two vectors, making it ideal for this operation.

Example 9: Masked multiplication
```assembly
MULPS.K ZMM1, ZMM2, ZMM3, K1   ; Multiply only where mask bit is 1
```

The .K suffix enables masked execution. Elements where the mask bit is 0 are copied unchanged from ZMM1; elements where the mask bit is 1 are replaced with the product.

Example 10: Multiplication with saturation for graphics
```assembly
MULPS.S XMM1, XMM2, #255   ; Scale to 0-255 range with saturation
```

The .S suffix enables saturating arithmetic. Values above 255 are clamped to 255, values below 0 are clamped to 0. This is used in graphics pipelines when converting floating-point colors to integer pixel values.

---

### 5.3 DOT – Vector Dot Product

The DOT instruction computes the dot product (scalar product) of two vectors. The dot product is the sum of the element-wise products: `dot = sum_i (a_i * b_i)`. This operation is fundamental to linear algebra, machine learning, graphics, and signal processing. A single DOT instruction replaces a loop of multiplication and addition instructions.

**Encoding Format**

DOT uses opcode 0x52. The instruction header contains opcode 0x52, flags, and operand count of 3. The first operand is the scalar destination (a register). The second and third operands are the source vectors. The instruction computes the dot product of the two vectors and stores the result in the destination register.

The flags field controls vector length and precision. Bits 8-9 encode the vector length: 00 for 128-bit (4 floats), 01 for 256-bit (8 floats), 10 for 512-bit (16 floats), and 11 for 1024-bit (32 floats). Bits 10-11 encode the accumulation precision: 00 for single-precision, 01 for double-precision, 10 for extended-precision, and 11 for mixed precision (products in double, sum in extended). Bits 12-15 are reserved.

The DOT instruction uses the fused multiply-add units internally. It multiplies corresponding pairs of elements and accumulates the products in a high-precision accumulator. The final result is rounded to the destination precision according to the current rounding mode.

**Operation Details**

The DOT instruction executes in a logarithmic number of cycles relative to the vector length. For a vector of N elements, the hardware performs N multiplications in parallel using the multiplier array, then reduces the N products to a single sum using a reduction tree. The reduction tree has log2(N) levels, each level adding pairs of partial sums.

For 16-element vectors (512 bits), the reduction tree has 4 levels. The total latency is 5 cycles: 1 cycle for multiplication, 4 cycles for reduction, plus 1 cycle for final rounding. This is dramatically faster than a scalar loop that would require 16 multiplications and 15 additions (31 cycles).

The DOT instruction can accumulate in higher precision than the inputs. Mixed-precision mode (bits 10-11 = 11) multiplies single-precision inputs, produces double-precision products, and accumulates in extended-precision (80-bit) temporary. This reduces rounding error for long dot products, such as those in matrix multiplication.

**Assembly Examples**

Example 1: Simple dot product of two 4-element vectors
```assembly
DOT R1, XMM2, XMM3   ; R1 = XMM2 · XMM3 (4 floats, single-precision)
```

This computes the dot product of the four floats in XMM2 and XMM3. The result is stored in scalar register R1. The dot product is `xmm2[0]*xmm3[0] + xmm2[1]*xmm3[1] + xmm2[2]*xmm3[2] + xmm2[3]*xmm3[3]`.

Example 2: Dot product for vector length
```assembly
DOT R1, XMM2, XMM2   ; R1 = |XMM2|^2 (squared length)
```

The dot product of a vector with itself gives the squared Euclidean length. The square root can then be computed with the SQRT instruction to get the actual length.

Example 3: Cosine similarity
```assembly
DOT R1, XMM2, XMM3   ; dot product
SQRT R2, R2          ; length of first vector (precomputed)
SQRT R3, R3          ; length of second vector (precomputed)
MUL R4, R2, R3       ; product of lengths
DIV R5, R1, R4       ; cosine = dot / (len1 * len2)
```

Cosine similarity measures the angle between two vectors. It is computed as the dot product divided by the product of the lengths. This sequence computes cosine similarity using DOT, SQRT, MUL, and DIV.

Example 4: Mixed-precision dot product for large vectors
```assembly
DOT.MP R1, ZMM2, ZMM3   ; Mixed precision: float multiply, double accumulate
```

The .MP suffix selects mixed-precision mode. The 16 pairs of floats are multiplied, producing 16 double-precision products. These are accumulated in an extended-precision register, then rounded to single-precision. This reduces rounding error for long dot products.

Example 5: Convolution using sliding dot product
```assembly
; Part of convolution: dot product of input window with kernel
DOT R1, XMM2, XMM3   ; kernel · input window
```

In convolutional neural networks, each output element is the dot product of a kernel with a window of input data. The DOT instruction accelerates this operation.

Example 6: Attention mechanism dot product
```assembly
; Attention: softmax(query · key^T)
DOT R1, XMM_query, XMM_key   ; query · key
```

Transformer attention mechanisms compute dot products between query and key vectors. The DOT instruction is the core operation of attention.

Example 7: Remote dot product
```assembly
DOT R1, XMM2, @4:0x10000   ; Dot product with remote vector
```

This computes the dot product of a local vector (XMM2) with a vector stored on blade 4. The remote vector is read (5 microseconds) before the dot product computation begins.

Example 8: Batch dot product (multiple vectors)
```assembly
; Process multiple dot products in a loop
loop:
DOT R1, XMM2, [R3]   ; Dot with vector from array
ADD R3, #16          ; Advance to next vector
ADD R2, #1
CMP R2, #100
BRANCH LT, loop
```

This loop computes the dot product of a fixed vector (XMM2) with 100 vectors stored in an array. The DOT instruction is called repeatedly, each time loading a new vector from memory.

Example 9: Dot product for linear regression prediction
```assembly
; prediction = dot(weights, features) + bias
DOT R1, XMM_weights, XMM_features
ADD R1, bias
```

Linear regression predictions are computed as the dot product of weight and feature vectors, plus a bias term. The DOT instruction computes the core product, and ADD adds the bias.

Example 10: Dot product with masking (sparse vectors)
```assembly
; For sparse vectors, use SPARSE_DOT instead
SPARSE_DOT R1, dense_vec, sparse_idx, sparse_val
```

For vectors with many zero elements, the SPARSE_DOT instruction is more efficient than DOT. DOT processes all elements, while SPARSE_DOT only processes non-zero elements.

---

### 5.4 CONV – 2D Convolution

The CONV instruction performs a 2D convolution operation in constant time. Convolution is the fundamental operation of convolutional neural networks, image processing filters, and signal processing. A single CONV instruction replaces a deeply nested loop of multiplications and additions, dramatically accelerating these workloads.

**Encoding Format**

CONV uses opcode 0x52 (alternative encoding, or 0x53 in some documentation). The instruction header contains opcode 0x53, flags, and operand count of 5. The operands are: output buffer base address, input buffer base address, kernel buffer base address, input dimensions, and stride.

The flags field controls kernel size, data type, and padding mode. Bits 8-9 encode kernel size: 00 for 3x3, 01 for 5x5, 10 for 7x7, and 11 for configurable (size from register). Bits 10-11 encode data type: 00 for 32-bit float, 01 for 16-bit float, 10 for 8-bit integer, and 11 for mixed precision. Bits 12-13 encode padding mode: 00 for valid (no padding), 01 for same (output same size as input), 10 for full (full convolution), and 11 for zero padding with configurable amount. Bits 14-15 are reserved.

The input dimensions operand is a 32-bit value encoding height in bits 0-15 and width in bits 16-31. The stride operand is a 16-bit value encoding vertical stride in bits 0-7 and horizontal stride in bits 8-15.

**Operation Details**

The CONV instruction uses a dedicated systolic array of multiply-accumulate units. The systolic array is sized to match the kernel: 3x3, 5x5, or 7x7. For configurable kernel sizes, the systolic array is reconfigured dynamically.

The input is streamed through the systolic array, with each MAC unit computing one element of the output feature map. The entire convolution completes in O(height * width) cycles, independent of kernel size. For a 3x3 kernel on a 224x224 image, the CONV instruction completes in approximately 50,176 cycles (224 * 224). A scalar implementation would require 224 * 224 * 3 * 3 = 451,584 multiplications and additions, a 9x speedup before considering loop overhead.

**Assembly Examples**

Example 1: 3x3 convolution on 224x224 image
```assembly
; Input at R1 (224x224 floats), kernel at R2 (3x3 floats)
; Output at R3 (222x222 floats, valid padding)
CONV R3, R1, R2, #0xE0E0, #1   ; 224=0xE0, stride=1
```

This performs a 3x3 convolution with valid padding (no padding). The output size is 222x222 because the kernel cannot extend beyond the input boundaries.

Example 2: Same padding convolution
```assembly
; Same padding: output same size as input (224x224)
CONV.PAD_SAME R3, R1, R2, #0xE0E0, #1
```

The .PAD_SAME suffix selects same padding mode. The input is padded with zeros so that the output has the same dimensions as the input.

Example 3: 5x5 convolution with stride 2
```assembly
; 5x5 kernel, stride 2, on 224x224 input
; Output size: (224-5)/2+1 = 110x110
CONV.K5 R3, R1, R2, #0xE0E0, #0x0202
```

The .K5 suffix selects a 5x5 kernel. The stride is encoded as 0x0202, meaning vertical stride 2 and horizontal stride 2. This reduces the output dimensions.

Example 4: Depthwise convolution (separate channels)
```assembly
; Depthwise: each input channel has its own kernel
; Input at R1 (CxHxW interleaved)
CONV.DEPTH R3, R1, R2, dimensions, stride
```

The .DEPTH suffix indicates depthwise convolution, where each input channel is convolved with its own kernel. This is used in efficient neural network architectures like MobileNet.

Example 5: Pointwise convolution (1x1 kernel)
```assembly
; 1x1 kernel (pointwise convolution)
CONV.K1 R3, R1, R2, dimensions, #1
```

A 1x1 convolution is equivalent to a fully connected layer applied at each position. The .K1 suffix selects a 1x1 kernel.

Example 6: 8-bit integer convolution for quantized networks
```assembly
; Quantized convolution: inputs and kernel are 8-bit integers
; Output is 32-bit integer accumulator
CONV.I8 R3, R1, R2, dimensions, stride
```

The .I8 suffix selects 8-bit integer mode. This is used for quantized neural networks, where lower precision reduces memory and increases speed.

Example 7: Remote convolution (distributed inference)
```assembly
; Input on blade 4, kernel local, output local
CONV R3, @4:0x10000, R2, dimensions, stride
```

This reads input data from remote blade 4, uses a local kernel, and writes the output locally. This enables distributed inference where different blades process different input regions.

Example 8: Transposed convolution (upsampling)
```assembly
; Transposed convolution (upsampling) for autoencoders
CONV.TRANS R3, R1, R2, dimensions, stride
```

The .TRANS suffix selects transposed convolution (also called deconvolution). This upscales the input, used in generative models and autoencoders.

Example 9: Dilated convolution (atrous convolution)
```assembly
; Dilated convolution with dilation rate 2
CONV.DILATE R3, R1, R2, dimensions, #0x0202, #2
```

The .DILATE suffix selects dilated convolution, where the kernel elements are spaced apart. This increases the receptive field without increasing kernel size.

Example 10: Grouped convolution
```assembly
; Grouped convolution with 4 groups
CONV.GROUP R3, R1, R2, dimensions, stride, #4
```

The .GROUP suffix selects grouped convolution, where input and output channels are divided into groups. This is used in ResNeXt and other efficient architectures.

---

### 5.5 SHUFPS – Shuffle Packed Single-Precision

The SHUFPS instruction reorders the elements within a vector of single-precision floating-point values. It selects elements from two source vectors and places them in arbitrary positions in the destination vector. Shuffling is essential for data reorganization, transposing matrices, and preparing data for SIMD operations.

**Encoding Format**

SHUFPS uses opcode 0x53. The instruction header contains opcode 0x53, flags, and operand count of 3. The first operand is the destination vector. The second and third operands are the source vectors. A fourth operand (encoded in the flags field) specifies the shuffle pattern.

The shuffle pattern is an 8-bit immediate value encoded in bits 8-15 of the flags field. The pattern is divided into four 2-bit fields, each specifying which source element goes into a destination position. For 128-bit vectors (4 elements), bits 0-1 select element for destination position 0, bits 2-3 for position 1, bits 4-5 for position 2, and bits 6-7 for position 3. A value of 0-3 selects from the first source; 4-7 selects from the second source (with 4 mapping to element 0 of the second source, etc.).

**Operation Details**

The SHUFPS instruction executes in a single cycle. The shuffle network is a crossbar switch that can route any input element to any output position. The crossbar has N inputs and N outputs, where N is the vector length (4, 8, 16, or 32). The crossbar uses multiplexers controlled by the shuffle pattern.

The shuffle pattern is evaluated at instruction decode time. The pattern is static (encoded in the instruction) for performance reasons. Dynamic shuffling (where the pattern comes from a register) is possible but slower, requiring a separate instruction.

**Assembly Examples**

Example 1: Basic shuffle of 4 elements
```assembly
SHUFPS XMM1, XMM2, XMM3, #0x1B   ; XMM1 = {XMM2[1],XMM2[0],XMM3[3],XMM3[2]}
```

The pattern 0x1B (binary 00011011) selects: position0 from source1 element1, position1 from source1 element0, position2 from source2 element3, position3 from source2 element2.

Example 2: Duplicate a single element to all positions
```assembly
SHUFPS XMM1, XMM2, XMM2, #0x00   ; Broadcast XMM2[0] to all positions
```

Pattern 0x00 selects element0 from source1 for all destination positions. This broadcasts the first element to the entire vector.

Example 3: Reverse vector order
```assembly
SHUFPS XMM1, XMM2, XMM2, #0x1B   ; Reverse order of 4 elements
```

Pattern 0x1B with the same source twice reverses the order: {3,2,1,0} becomes {0,1,2,3}.

Example 4: Interleave two vectors (for complex numbers)
```assembly
; Interleave real and imaginary parts from two vectors
; XMM2 = {r0,r1,r2,r3}, XMM3 = {i0,i1,i2,i3}
SHUFPS XMM1, XMM2, XMM3, #0x88   ; {r0,i0,r1,i1} (pattern 0x88 = 10 00 10 00)
```

This interleaves elements from two vectors, creating a vector of complex numbers with alternating real and imaginary parts.

Example 5: Transpose 4x4 matrix
```assembly
; Transpose a 4x4 matrix stored in 4 vectors
; YMM0 = row0, YMM1 = row1, YMM2 = row2, YMM3 = row3
SHUFPS YMM4, YMM0, YMM1, #0x44   ; {row0[0],row1[0],row0[2],row1[2]}
SHUFPS YMM5, YMM0, YMM1, #0xEE   ; {row0[1],row1[1],row0[3],row1[3]}
; ... continue for transposition
```

Matrix transposition requires a sequence of shuffles. This example shows the beginning of a 4x4 transpose using 256-bit vectors.

Example 6: Unpack low and high halves
```assembly
UNPCKLPS XMM1, XMM2, XMM3   ; Unpack low: {XMM2[0],XMM3[0],XMM2[1],XMM3[1]}
UNPCKHPS XMM1, XMM2, XMM3   ; Unpack high: {XMM2[2],XMM3[2],XMM2[3],XMM3[3]}
```

The UNPCKLPS and UNPCKHPS instructions are aliases for specific SHUFPS patterns. UNPCKLPS corresponds to pattern 0x44, UNPCKHPS to pattern 0xEE.

Example 7: Extract and broadcast element
```assembly
; Extract element 2 from XMM2 and broadcast to all positions
SHUFPS XMM1, XMM2, XMM2, #0xAA   ; 0xAA = 10 10 10 10 (binary)
```

Pattern 0xAA (binary 10101010) selects element2 (value 2) from the source for all destination positions.

Example 8: Shuffle for dot product (horizontal add preparation)
```assembly
; Prepare for horizontal add by pairing elements
SHUFPS XMM1, XMM2, XMM2, #0xB1   ; {XMM2[1],XMM2[0],XMM2[3],XMM2[2]}
ADDPS XMM1, XMM1, XMM2           ; Add pairs
```

This shuffle pairs adjacent elements in preparation for a horizontal add. The ADDPS then adds the pairs.

Example 9: Remote shuffle
```assembly
SHUFPS XMM1, XMM2, @4:0x10000, #0x1B   ; Shuffle with remote vector
```

This shuffles a local vector (XMM2) with a vector stored on blade 4. The remote vector is read (5 microseconds), then the shuffle executes locally.

Example 10: Masked shuffle
```assembly
SHUFPS.K XMM1, XMM2, XMM3, #0x1B, K1   ; Shuffle only where mask bit is 1
```

The .K suffix enables masked execution. Elements where the mask bit is 0 are copied unchanged from XMM1; elements where the mask bit is 1 are replaced with shuffled values.

---

This concludes Chapter 5 of the Instruction Set Reference. The remaining chapters will cover Advanced Math Functions, Probabilistic Inference Instructions, System Instructions, Interconnect Instructions, Memory Management Instructions, and Protection Instructions. Each instruction will be documented with the same level of detail.

# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 6: Advanced Math Functions

### 6.1 EXP – Exponential Function (e^x)

The EXP instruction computes the exponential function e raised to the power of the source operand. The exponential function appears in physics, chemistry, biology, finance, and machine learning (particularly in softmax and sigmoid activation functions). The PIP CISC implementation uses a minimax polynomial approximation with 14 terms, accurate to within 1 unit in the last place (ULP).

**Encoding Format**

EXP uses opcode 0x80. The instruction header contains opcode 0x80, flags, and operand count of 2. The first operand is the destination register. The second operand is the source value. The instruction computes destination = e^source.

The flags field controls precision and vector mode. Bit 8, when set, indicates vector mode where the operand is treated as a vector of multiple elements. Bits 9-10 encode the vector length: 00 for 128-bit (4 floats), 01 for 256-bit (8 floats), 10 for 512-bit (16 floats), and 11 for 1024-bit (32 floats). Bit 11, when set, enables reduced-precision mode (10 ULP accuracy, 2x faster). Bits 12-15 are reserved.

The source operand can be a register or memory location. The destination must be a register. The operand size can be 32-bit or 64-bit floating-point. The instruction automatically detects the precision from the operand descriptor.

**Operation Details**

The EXP instruction implements the exponential function using the following algorithm. First, the input x is reduced to the range [-ln2/2, ln2/2] by subtracting an integer multiple of ln2. The integer part becomes the exponent of the result. The reduced value is then passed through a minimax polynomial: `exp(x) ≈ 1 + x + x^2/2! + x^3/3! + ... + x^14/14!`. The polynomial coefficients are stored in a read-only memory within the floating-point unit.

The polynomial is evaluated using Horner's method for numerical stability. For single-precision, 10 terms are sufficient. For double-precision, 14 terms are used. The reduced-precision mode uses 6 terms and runs in half the cycles.

The result is constructed by multiplying the polynomial result by 2^(integer part). The multiplication is performed by adding the integer part to the exponent field of the floating-point result.

The EXP instruction completes in 15 cycles for single-precision, 22 cycles for double-precision, and 8 cycles for reduced-precision mode. The latency is fixed regardless of the input value.

**Assembly Examples**

Example 1: Basic exponential
```assembly
EXP R1, R2    ; R1 = e^R2 (single-precision)
```

This computes the exponential of the single-precision value in R2 and stores the result in R1. If R2 is 1.0, R1 becomes approximately 2.71828.

Example 2: Exponential for sigmoid function
```assembly
; Sigmoid: σ(x) = 1 / (1 + e^(-x))
NEG R2, R1        ; R2 = -x
EXP R3, R2        ; R3 = e^(-x)
ADD R3, #1.0      ; R3 = 1 + e^(-x)
DIV R4, #1.0, R3  ; R4 = 1 / (1 + e^(-x))
```

The sigmoid activation function is used in neural networks. This sequence computes sigmoid using NEG, EXP, ADD, and DIV.

Example 3: Exponential for softmax
```assembly
; Compute exp(x_i) for each element of vector
EXP.V XMM1, XMM2   ; XMM1[i] = e^(XMM2[i]) for all i
```

The softmax function requires exponentials of each input element. The vectorized EXP instruction computes all exponentials in parallel.

Example 4: Reduced-precision exponential for inference
```assembly
EXP.FAST R1, R2   ; Fast exponential (10 ULP accuracy)
```

The .FAST suffix selects reduced-precision mode. This is suitable for neural network inference where slight inaccuracies are acceptable in exchange for higher throughput.

Example 5: Exponential for exponential moving average
```assembly
; EMA: value = α * new + (1-α) * old, where α = 2/(span+1)
; Compute α using exponential? Actually use division, but decay uses exp
MOV R1, #-0.1
EXP R2, R1        ; R2 = e^(-0.1) ≈ 0.9048 (decay factor)
```

Exponential moving averages use a decay factor that can be computed using EXP of a negative number.

Example 6: Gaussian function using EXP
```assembly
; Gaussian: f(x) = a * e^(-(x-b)^2/(2c^2))
SUB R2, R1, mean      ; x - μ
MUL R2, R2, R2        ; (x-μ)^2
MOV R3, #2.0
MUL R3, variance, R3  ; 2σ^2
DIV R4, R2, R3        ; -(x-μ)^2/(2σ^2) (negative)
EXP R5, R4            ; e^(negative value)
MUL R6, amplitude, R5 ; a * e^(...)
```

The Gaussian (normal) distribution is fundamental to statistics. This sequence computes a Gaussian using SUB, MUL, DIV, EXP, and MUL.

Example 7: Exponential of remote value
```assembly
EXP R1, @4:0x10000   ; R1 = e^(remote value on blade 4)
```

This loads a value from remote memory, computes its exponential, and stores the result locally. The remote read takes approximately 5 microseconds, after which the EXP executes locally.

Example 8: Exponential for option pricing (Black-Scholes)
```assembly
; Black-Scholes uses e^(-rT) for discount factor
MOV R1, rate
MUL R1, R1, time    ; rT
NEG R1, R1          ; -rT
EXP R2, R1          ; e^(-rT)
```

Financial option pricing models use exponentials for discounting future cash flows. This sequence computes the discount factor.

Example 9: Exponential for decay in learning rate schedules
```assembly
; Exponential decay learning rate: lr = lr0 * e^(-k * step)
MUL R2, decay_rate, step
NEG R2, R2
EXP R3, R2
MUL lr, initial_lr, R3
```

Machine learning training often uses exponential decay of the learning rate. This sequence computes the decayed learning rate.

Example 10: Vector exponential for softmax in transformer
```assembly
; Compute all exponentials for softmax in attention
EXP.V ZMM1, ZMM2   ; 16 exponentials in parallel
; Then sum and divide for softmax
```

Transformer attention mechanisms compute softmax over query-key dot products. The vectorized EXP computes all exponentials for the softmax in parallel.

---

### 6.2 LOG – Natural Logarithm

The LOG instruction computes the natural logarithm (base e) of the source operand. The logarithm is the inverse of the exponential function: `log(e^x) = x`. The logarithm appears in information theory (entropy, mutual information), statistics (log-likelihood), and scientific computing. The PIP CISC implementation is accurate to within 1 ULP.

**Encoding Format**

LOG uses opcode 0x81. The instruction header contains opcode 0x81, flags, and operand count of 2. The first operand is the destination register. The second operand is the source value. The instruction computes destination = ln(source).

The flags field controls precision and vector mode identically to EXP. Bit 8 enables vector mode. Bits 9-10 encode vector length. Bit 11 enables reduced-precision mode (10 ULP, 2x faster). Bits 12-15 are reserved.

The source operand must be positive. If the source is zero or negative, the instruction raises an invalid operation exception and returns a NaN (Not a Number) result.

**Operation Details**

The LOG instruction implements the natural logarithm using the following algorithm. First, the input x is normalized to the range [1, 2) by extracting the exponent and mantissa. The logarithm is then `ln(x) = ln(mantissa) + exponent * ln(2)`. The reduced-range logarithm `ln(mantissa)` is computed using a minimax polynomial of degree 12 for single-precision and 18 for double-precision.

The polynomial coefficients are stored in the floating-point unit's read-only memory. The polynomial is evaluated using Horner's method. The final result is constructed by adding the exponent term.

The LOG instruction completes in 18 cycles for single-precision, 28 cycles for double-precision, and 10 cycles for reduced-precision mode.

**Assembly Examples**

Example 1: Basic logarithm
```assembly
LOG R1, R2    ; R1 = ln(R2) (natural log)
```

This computes the natural logarithm of R2. If R2 is e (approximately 2.71828), R1 becomes approximately 1.0.

Example 2: Log for entropy calculation
```assembly
; Entropy: H = -Σ p_i * log(p_i)
LOG R2, R1        ; R2 = ln(p_i)
MUL R3, R1, R2    ; p_i * ln(p_i)
ADD entropy, entropy, R3   ; accumulate
; At the end: H = -entropy
```

Entropy measures uncertainty in a probability distribution. This sequence contributes one term to the entropy sum.

Example 3: Log-likelihood for Gaussian distribution
```assembly
; Log-likelihood: ln(N(x|μ,σ)) = -0.5*ln(2πσ^2) - (x-μ)^2/(2σ^2)
MOV R1, variance
MUL R1, R1, #2π   ; 2πσ^2
LOG R2, R1         ; ln(2πσ^2)
MUL R2, R2, #-0.5  ; -0.5 * ln(2πσ^2)
; ... subtract quadratic term
```

Log-likelihoods are used in maximum likelihood estimation. This sequence computes the constant term of a Gaussian log-likelihood.

Example 4: Log for information gain
```coding
; Information gain = H(parent) - weighted sum H(children)
LOG R2, prob        ; ln(prob)
MUL R2, prob, R2    ; prob * ln(prob)
```

Decision tree learning uses information gain based on entropy. This sequence computes one term of the entropy calculation.

Example 5: Reduced-precision log for inference
```assembly
LOG.FAST R1, R2   ; Fast natural log (10 ULP accuracy)
```

The .FAST suffix selects reduced-precision mode. This is suitable for applications where approximate log values are acceptable.

Example 6: Log of remote value
```assembly
LOG R1, @4:0x10000   ; R1 = ln(remote value on blade 4)
```

This loads a value from remote memory, computes its logarithm, and stores the result locally.

Example 7: Log for cross-entropy loss
```assembly
; Cross-entropy: -Σ y_i * log(p_i)
LOG R3, R2        ; R3 = ln(p_i)
MUL R4, R1, R3    ; y_i * ln(p_i)
ADD loss, loss, R4
```

Cross-entropy is the standard loss function for classification neural networks. This sequence computes one term of the cross-entropy.

Example 8: Log for perplexity
```assembly
; Perplexity = e^(-(1/N) * Σ ln(p_i))
LOG.V XMM2, XMM1   ; ln(p_i) for all i
HADDPS XMM3, XMM2, XMM2   ; Sum of logs (horizontal add)
DIV R4, R4, #N     ; Average log
NEG R5, R4         ; -average log
EXP R6, R5         ; exp(-average log) = perplexity
```

Perplexity measures how well a probability model predicts a sample. It is the exponential of the negative average log-likelihood.

Example 9: Log for mutual information
```assembly
; MI = Σ p(x,y) * log(p(x,y) / (p(x)p(y)))
; Compute log ratio
DIV R4, joint, (px * py)   ; p(x,y)/(p(x)p(y))
LOG R5, R4         ; log of ratio
MUL R6, joint, R5  ; p(x,y) * log(...)
```

Mutual information measures dependence between random variables. This sequence computes one term of the mutual information sum.

Example 10: Vector log for softmax gradient
```assembly
; Softmax gradient: ∂L/∂z_i = p_i - y_i
; where p_i = e^z_i / Σ e^z_i
; Log space: log(p_i) = z_i - log(Σ e^z_j)
LOG.V ZMM2, ZMM1   ; Not directly used; LOG for other purposes
```

The softmax gradient does not directly use LOG, but logarithmic space computations often require LOG for numerical stability.

---

### 6.3 SQRT – Square Root

The SQRT instruction computes the square root of the source operand. The square root is the inverse of squaring: `sqrt(x)^2 = x`. Square roots appear in Euclidean distance calculations, standard deviations, normalizations, and many geometric computations. The PIP CISC implementation uses a fast Newton-Raphson iteration with a hardware seed, completing in a fixed number of cycles.

**Encoding Format**

SQRT uses opcode 0x8A. The instruction header contains opcode 0x8A, flags, and operand count of 2. The first operand is the destination register. The second operand is the source value. The instruction computes destination = sqrt(source).

The flags field controls precision and vector mode identically to EXP and LOG. Bit 8 enables vector mode. Bits 9-10 encode vector length. Bit 11 enables reduced-precision mode (2 ULP accuracy, 2x faster). Bits 12-15 are reserved.

The source operand must be non-negative. If the source is negative, the instruction raises an invalid operation exception and returns a NaN.

**Operation Details**

The SQRT instruction uses the following algorithm. First, the input x is normalized to the range [1, 4) by adjusting the exponent. An initial approximation of 1/sqrt(x) is obtained from a lookup table indexed by the top bits of the mantissa. This approximation is then refined using two iterations of the Newton-Raphson formula: `y = y * (3 - x * y^2) / 2`. After the iterations, the result is computed as `x * y`.

For double-precision, three iterations are used. For reduced-precision mode, one iteration is used.

The SQRT instruction completes in 8 cycles for single-precision, 14 cycles for double-precision, and 4 cycles for reduced-precision mode.

**Assembly Examples**

Example 1: Basic square root
```assembly
SQRT R1, R2    ; R1 = sqrt(R2)
```

This computes the square root of R2. If R2 is 4.0, R1 becomes 2.0. If R2 is 2.0, R1 becomes approximately 1.41421356.

Example 2: Euclidean distance between two vectors
```assembly
; distance = sqrt((x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2)
SUB R4, R1, R2    ; Δx
SUB R5, R3, R4    ; Δy (using different registers)
MUL R4, R4, R4    ; Δx^2
MUL R5, R5, R5    ; Δy^2
ADD R4, R4, R5    ; sum of squares
SQRT R6, R4       ; distance
```

Euclidean distance is the square root of the sum of squared differences. This sequence computes the 2D Euclidean distance.

Example 3: Standard deviation
```assembly
; σ = sqrt(Σ(x_i - μ)^2 / N)
; Assume sum_sq_diff already computed
DIV R2, sum_sq_diff, N   ; variance
SQRT R3, R2              ; standard deviation
```

Standard deviation is the square root of the variance. This sequence computes the population standard deviation.

Example 4: Root mean square (RMS)
```assembly
; RMS = sqrt(Σ x_i^2 / N)
; Assume sum_sq already computed
DIV R2, sum_sq, N   ; mean square
SQRT R3, R2         ; RMS
```

RMS is used in signal processing to measure the magnitude of a varying signal. This sequence computes RMS from the sum of squares.

Example 5: Vectorized square root for normalization
```assembly
; Normalize a vector: unit = vector / length
DOT R1, XMM2, XMM2   ; R1 = length^2
SQRT R2, R1          ; R2 = length
MULPS XMM3, XMM2, #1.0   ; Prepare reciprocal
DIVPS XMM3, XMM3, R2_S   ; XMM3 = vector / length
```

Vector normalization divides each component by the length. This sequence uses SQRT to compute the length, then divides each component.

Example 6: Fast square root for graphics
```assembly
SQRT.FAST R1, R2   ; Fast sqrt (2 ULP accuracy)
```

The .FAST suffix selects reduced-precision mode. This is suitable for graphics where slight inaccuracies are visually imperceptible.

Example 7: Square root of remote value
```assembly
SQRT R1, @4:0x10000   ; R1 = sqrt(remote value)
```

This loads a value from remote memory, computes its square root, and stores the result locally.

Example 8: Hypotenuse length
```assembly
; hypotenuse = sqrt(a^2 + b^2) (Pythagorean theorem)
MUL R3, R1, R1    ; a^2
MUL R4, R2, R2    ; b^2
ADD R5, R3, R4    ; a^2 + b^2
SQRT R6, R5       ; c = sqrt(a^2 + b^2)
```

The Pythagorean theorem computes the hypotenuse length. This sequence avoids overflow by using multiplication before addition.

Example 9: Geometric mean
```assembly
; Geometric mean = (Π x_i)^(1/N) = exp((1/N) * Σ ln(x_i))
; Or directly use SQRT for two numbers
MUL R3, R1, R2    ; product of two numbers
SQRT R4, R3       ; geometric mean of two numbers
```

The geometric mean of two numbers is the square root of their product. This is used in growth rate calculations.

Example 10: Vector magnitude for distance matrix
```assembly
; Compute distances from point to N points
; For each point: dx = x_i - x0, dy = y_i - y0
; distance = sqrt(dx^2 + dy^2)
SUB.V XMM2, XMM1, XMM0   ; dx for 4 points
MUL.V XMM3, XMM2, XMM2   ; dx^2
; ... similar for dy
ADD.V XMM5, XMM3, XMM4   ; dx^2 + dy^2
SQRT.V XMM6, XMM5        ; distances for 4 points
```

The vectorized SQRT computes distances for multiple points in parallel. This is used in k-nearest neighbors and clustering algorithms.

---

### 6.4 RSQRT – Reciprocal Square Root

The RSQRT instruction computes the reciprocal square root: `1 / sqrt(source)`. This is a specialized instruction that is both faster and more accurate than computing sqrt followed by division. The reciprocal square root appears in vector normalization, where dividing each component by the length is equivalent to multiplying by the reciprocal square root of the sum of squares.

**Encoding Format**

RSQRT uses opcode 0x8B. The instruction header contains opcode 0x8B, flags, and operand count of 2. The first operand is the destination register. The second operand is the source value. The instruction computes destination = 1 / sqrt(source).

The flags field controls precision and vector mode identically to SQRT. Bit 8 enables vector mode. Bits 9-10 encode vector length. Bit 11 enables reduced-precision mode. Bits 12-15 are reserved.

The source operand must be positive. If the source is zero, the instruction returns positive infinity. If the source is negative, it returns NaN.

**Operation Details**

The RSQRT instruction uses the same algorithm as SQRT but returns the reciprocal directly. The Newton-Raphson iteration for reciprocal square root is: `y = y * (3 - x * y^2) / 2`. This iteration converges to 1/sqrt(x) without requiring a division at the end.

The RSQRT instruction completes in 6 cycles for single-precision, 12 cycles for double-precision, and 3 cycles for reduced-precision mode. This is faster than SQRT because it avoids the final multiplication.

**Assembly Examples**

Example 1: Basic reciprocal square root
```assembly
RSQRT R1, R2    ; R1 = 1 / sqrt(R2)
```

This computes the reciprocal square root of R2. If R2 is 4.0, R1 becomes 0.5. If R2 is 2.0, R1 becomes approximately 0.70710678.

Example 2: Vector normalization using RSQRT
```assembly
; Normalize vector: unit = vector * (1 / length)
DOT R1, XMM2, XMM2   ; R1 = length^2
RSQRT R2, R1         ; R2 = 1 / length
MULPS XMM3, XMM2, R2_S   ; XMM3 = vector / length
```

This is the standard way to normalize a vector using RSQRT. It is faster than computing SQRT followed by division because RSQRT combines both operations.

Example 3: Fast inverse square root (classic algorithm)
```assembly
; Classic fast inverse sqrt from Quake (approximate)
; The PIP CISC RSQRT instruction makes this obsolete
RSQRT R1, R2   ; Accurate and fast
```

The classic "fast inverse square root" hack is no longer needed on PIP CISC because RSQRT provides accurate results in fixed latency.

Example 4: Vectorized normalization of multiple vectors
```assembly
; Normalize 4 vectors (4 components each, stored in 4 registers)
DOT.V R1, XMM2, XMM2   ; lengths^2 for 4 vectors (scalar results)
RSQRT.V XMM3, XMM1     ; 1/length for 4 vectors (broadcast result)
MULPS.V XMM4, XMM2, XMM3   ; Normalized vectors
```

The vectorized RSQRT computes reciprocal square roots for multiple vectors in parallel. Each vector's length is computed via DOT, then RSQRT processes all lengths simultaneously.

Example 5: RSQRT for lighting calculations (Phong reflection)
```assembly
; Phong lighting uses normalized vectors
; Compute normalized normal and light direction
RSQRT R3, R1   ; 1/|N|
MULPS N, N, R3_S
RSQRT R4, R2   ; 1/|L|
MULPS L, L, R4_S
; Then compute dot product for diffuse lighting
DOT R5, N, L
```

3D graphics lighting calculations require normalized vectors. RSQRT efficiently computes the normalization factors.

Example 6: Reduced-precision RSQRT for real-time graphics
```assembly
RSQRT.FAST R1, R2   ; Fast reciprocal sqrt (2 ULP accuracy)
```

The .FAST suffix selects reduced-precision mode. This is sufficient for real-time graphics where speed is more important than absolute accuracy.

Example 7: RSQRT of remote value
```assembly
RSQRT R1, @4:0x10000   ; R1 = 1/sqrt(remote value)
```

This loads a value from remote memory, computes its reciprocal square root, and stores the result locally.

Example 8: Computing standard deviation using RSQRT
```assembly
; σ = sqrt(variance) = variance * (1/sqrt(variance))
; This is not numerically optimal; use SQRT instead
```

While RSQRT could be used to compute standard deviation, SQRT is more direct and equally fast. RSQRT is best when the reciprocal is needed for subsequent multiplication.

Example 9: Coulomb's law computation
```assembly
; Force = k * q1 * q2 / r^2
; Compute 1/r using RSQRT of r^2
MUL R3, R1, R1    ; r^2 (if R1 is distance, not squared)
RSQRT R4, R3      ; 1/r
MUL R5, R4, R4    ; 1/r^2 (if needed)
MUL force, k, q1
MUL force, force, q2
MUL force, force, R5   ; k * q1 * q2 / r^2
```

Coulomb's law requires division by the square of the distance. This can be computed using RSQRT of distance^2, then squaring the result.

Example 10: RSQRT for gravitational force
```assembly
; F = G * m1 * m2 / r^2
; Compute 1/r^2 efficiently
RSQRT R4, R3      ; R3 = r^2, R4 = 1/r
MUL R5, R4, R4    ; 1/r^2
```

Gravitational force follows the same inverse-square law. RSQRT provides an efficient path to 1/r^2.

---

### 6.5 ERF – Error Function

The ERF instruction computes the error function, which is the integral of the Gaussian distribution. The error function is defined as `erf(x) = (2/√π) ∫₀ˣ e^{-t²} dt`. It appears in probability, statistics, heat transfer, and diffusion problems. The output ranges from -1 to 1.

**Encoding Format**

ERF uses opcode 0x8C. The instruction header contains opcode 0x8C, flags, and operand count of 2. The first operand is the destination register. The second operand is the source value. The instruction computes destination = erf(source).

The flags field controls precision and vector mode identically to other math functions. Bit 8 enables vector mode. Bits 9-10 encode vector length. Bit 11 enables reduced-precision mode (5 ULP accuracy, 2x faster). Bits 12-15 are reserved.

**Operation Details**

The ERF instruction implements the error function using a rational approximation with polynomial numerator and denominator. For small |x| (< 0.5), a Taylor series expansion is used. For large |x| (> 3), the complementary error function is used via the approximation `erf(x) = 1 - erfc(x)`. For intermediate values, a minimax rational approximation of degree 6/6 is used.

The ERF instruction completes in 20 cycles for single-precision, 35 cycles for double-precision, and 12 cycles for reduced-precision mode.

**Assembly Examples**

Example 1: Basic error function
```assembly
ERF R1, R2    ; R1 = erf(R2)
```

This computes the error function of R2. If R2 is 0, R1 is 0. If R2 is 1, R1 is approximately 0.8427. If R2 is infinity, R1 approaches 1.

Example 2: Cumulative distribution function of normal distribution
```assembly
; CDF of N(0,σ): Φ(x) = 0.5 * (1 + erf(x / (σ√2)))
MOV R2, #1.41421356   ; √2
MUL R2, sigma, R2     ; σ√2
DIV R3, x, R2         ; x / (σ√2)
ERF R4, R3            ; erf(x/(σ√2))
MUL R4, #0.5
ADD R5, #0.5, R4      ; Φ(x)
```

The cumulative distribution function of the normal distribution is expressed in terms of the error function. This sequence computes the CDF.

Example 3: Probability of a value within a range
```assembly
; P(a < X < b) = Φ(b) - Φ(a)
; Compute Φ(b) and Φ(a) using ERF
SUB R4, cdf_b, cdf_a   ; probability
```

The probability that a normally distributed random variable falls between a and b is the difference of the CDF values.

Example 4: Vectorized error function for multiple probabilities
```assembly
ERF.V XMM1, XMM2   ; Compute erf for 4 values in parallel
```

The vectorized ERF computes error functions for multiple inputs simultaneously, useful for batch probability calculations.

Example 5: Reduced-precision ERF for machine learning
```assembly
ERF.FAST R1, R2   ; Fast erf (5 ULP accuracy)
```

Some machine learning activation functions approximate the error function. Reduced-precision ERF is sufficient for inference.

Example 6: ERF of remote value
```assembly
ERF R1, @4:0x10000   ; R1 = erf(remote value)
```

This computes the error function of a value stored on a remote blade.

Example 7: Probabilistic error bounds
```assembly
; Probability that error exceeds threshold: P(|X| > t) = 1 - erf(t/√2)
MOV R2, #1.41421356
DIV R3, threshold, R2   ; t/√2
ERF R4, R3
MOV R5, #1.0
SUB R5, R5, R4          ; 1 - erf(t/√2)
```

This computes the tail probability of a normal distribution.

Example 8: Heat diffusion solution
```assembly
; Temperature at position x after time t: T = T0 * erf(x/(2√(αt)))
MUL R3, alpha, time
SQRT R4, R3            ; √(αt)
MUL R4, #2.0
DIV R5, x, R4
ERF R6, R5
MUL T, T0, R6
```

The error function appears in the solution to the heat equation. This sequence computes the temperature distribution.

Example 9: Gaussian probability density integral
```assembly
; ∫₀ˣ e^{-t²} dt = (√π/2) * erf(x)
MOV R3, #1.77245385   ; √π
MUL R3, R3, #0.5      ; √π/2
ERF R2, x
MUL result, R3, R2
```

The integral of the Gaussian function without normalization is proportional to the error function.

Example 10: ERF for Bayesian inference
```assembly
; Compute posterior probability using ERF-based prior
ERF.V ZMM1, ZMM2   ; Batch computation for multiple hypotheses
```

Bayesian inference with Gaussian priors often requires error function calculations for the posterior probabilities.

---

This concludes Chapter 6 of the Instruction Set Reference. The remaining chapters will cover Probabilistic Inference Instructions, System Instructions, Interconnect Instructions, Memory Management Instructions, and Protection Instructions. Each instruction will be documented with the same level of detail.

# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 7: Probabilistic Inference Instructions

### 7.1 HMM_FORWARD – Hidden Markov Model Forward Algorithm

The HMM_FORWARD instruction computes one step of the forward algorithm for a Hidden Markov Model. The forward algorithm calculates the probability of observing a sequence of emissions given an HMM, by recursively computing the probability of being in each state at each time step. This instruction is the core primitive for speech recognition, gesture recognition, bioinformatics sequence analysis, and any application involving sequential probabilistic inference.

**Encoding Format**

HMM_FORWARD uses opcode 0xA0. The instruction header contains opcode 0xA0, flags, and operand count of 5. The operands are: the destination vector for new forward probabilities, the source vector for previous forward probabilities, the transition matrix, the emission probabilities vector, and a scaling factor.

The flags field controls precision and vectorization. Bits 8-9 encode the number of states as a power of two: 00 for 64 states, 01 for 128 states, 10 for 256 states, and 11 for 512 states. Bits 10-11 encode the precision: 00 for 32-bit float, 01 for 64-bit float, 10 for 16-bit float, and 11 for mixed precision. Bit 12 enables automatic scaling to prevent underflow. Bit 13 enables the use of log-space probabilities (adding instead of multiplying). Bits 14-15 are reserved.

The transition matrix operand is a memory address pointing to an N x N matrix in row-major order, where N is the number of states. The emission probabilities operand is a vector of length N. The previous forward probabilities operand is a vector of length N. The destination operand is a vector of length N for the new probabilities. The scaling factor operand is a scalar memory address where the instruction stores the computed scaling factor for this step.

**Operation Details**

The HMM_FORWARD instruction computes for each current state j: `new_forward[j] = emission[j] × sum_over_i( old_forward[i] × transition[i][j] )`. The computation proceeds in three phases.

In the first phase, each of the N Math cores computes one term of the inner sum independently. The instruction distributes the old forward probabilities and the transition matrix columns across the cores. Core i computes `old_forward[i] × transition[i][j]` for a fixed j and all i, or for a fixed i and all j, depending on the hardware implementation. The communication fabric uses a butterfly network to exchange partial results.

In the second phase, the reduction network sums the N terms for each destination state using a tree of adders. This takes log2(N) cycles. The sums are then multiplied by the emission probabilities for each state.

In the third phase, the scaling factor is computed as the sum of all new forward probabilities. This sum is divided into the new probabilities to prevent underflow, and the scaling factor is stored at the provided address. The scaling factors for all time steps are used later to compute the total sequence probability.

The instruction completes in 2 + log2(N) cycles for the vector operations, plus memory access time for loading the transition matrix and emission probabilities. For a 256-state HMM, this is 2 + 8 = 10 cycles. A software implementation would require approximately 256 × 256 = 65,536 multiply-add operations, a speedup of over 6,500 times.

**Assembly Examples**

Example 1: Single forward step for 256-state HMM
```assembly
; R1 = previous forward probabilities (256 floats)
; R2 = transition matrix (256x256 = 65,536 floats)
; R3 = emission probabilities (256 floats)
; R4 = scaling factor address
; R5 = destination for new forward probabilities
HMM_FORWARD R5, R1, R2, R3, R4
```

This performs one step of the forward algorithm. The new forward probabilities are stored at R5, and the scaling factor is stored at R4.

Example 2: Complete forward algorithm for a sequence
```assembly
; Process a sequence of 1000 emissions
MOV R10, #0          ; time step counter
MOV R11, initial_probs   ; initial forward probabilities
MOV R12, scaling_factors  ; array to store scaling factors
MOV R13, emissions   ; array of emission probability vectors
MOV R14, transition  ; transition matrix (constant)
loop:
; Load emission probabilities for current time step
LEA R15, [R13 + R10*1024]   ; each emission vector is 256*4=1024 bytes
HMM_FORWARD R11, R11, R14, R15, [R12 + R10*4]
ADD R10, #1
CMP R10, #1000
BRANCH LT, loop
; Total log probability = sum(log(scaling_factors))
```

This loop processes an entire observation sequence. The forward probabilities are updated in place. The scaling factors are stored for later computation of the total sequence probability.

Example 3: Log-space forward algorithm
```assembly
HMM_FORWARD.LOG R5, R1, R2, R3, R4
```

The .LOG suffix indicates that probabilities are stored in log space. The instruction uses addition instead of multiplication and log-sum-exp instead of addition for the sum over states. This eliminates underflow entirely and is preferred for long sequences.

Example 4: Mixed-precision forward for long sequences
```assembly
HMM_FORWARD.MP R5, R1, R2, R3, R4
```

The .MP suffix selects mixed-precision mode. The transition probabilities are stored in 16-bit floats, the emission probabilities in 16-bit floats, but the forward probabilities are accumulated in 32-bit floats. This reduces memory bandwidth while maintaining accuracy.

Example 5: Remote HMM computation (distributed inference)
```assembly
; Transition matrix on blade 4, emissions local
HMM_FORWARD R5, R1, @4:0x10000, R3, R4
```

The transition matrix is stored on remote blade 4. The instruction streams the matrix across the optical fabric during computation, overlapping communication with computation.

Example 6: HMM with shared transition matrix across multiple sequences
```assembly
; Process 8 sequences in parallel on 8 blades
; Each blade has its own forward probabilities and emissions
; All blades share the same transition matrix (broadcast)
BROADCAST HMM_FORWARD R5, R1, @root:transition, R3, R4
```

The BROADCAST instruction sends the HMM_FORWARD instruction to all blades simultaneously. The transition matrix is read from the root blade's memory and broadcast to all blades.

Example 7: Forward algorithm with pruning (beam search)
```assembly
; After forward step, prune low-probability states
HMM_FORWARD R5, R1, R2, R3, R4
VECTOR_THRESHOLD K1, R5, #1e-10, GT   ; Keep states with prob > 1e-10
; Subsequent operations use mask K1 to skip pruned states
```

The VECTOR_THRESHOLD instruction creates a mask of states that survived pruning. Subsequent HMM_FORWARD instructions can use this mask to skip computations for pruned states.

Example 8: Hierarchical HMM with two-level state space
```assembly
; First level: 64 macro-states
; Second level: 4 micro-states per macro-state (256 total)
; Compute macro-state forward first, then micro-state
HMM_FORWARD macro_fwd, macro_prev, macro_trans, macro_emiss, scale
; For each macro-state, compute micro-state forward
```

Hierarchical HMMs reduce computational complexity by structuring the state space. This sequence computes the forward probabilities for the macro-states, then for the micro-states within each macro-state.

Example 9: HMM for speech recognition (phoneme models)
```assembly
; 3-state left-to-right HMM per phoneme, 64 phonemes
; Total states: 192
HMM_FORWARD R5, R1, R2, R3, R4
```

Speech recognition systems use left-to-right HMMs where transitions only go forward. The transition matrix is sparse, but the HMM_FORWARD instruction still operates on the full matrix. Sparse optimization can be enabled via configuration registers.

Example 10: Forward algorithm with posterior probability tracking
```assembly
; Compute forward probabilities and store for backward pass
; Needed for Baum-Welch training
HMM_FORWARD fwd_new, fwd_old, trans, emiss, scale
ST.V [fwd_buffer + t*1024], fwd_new   ; Store for later backward pass
```

The forward probabilities are stored for each time step. The backward pass (using HMM_BACKWARD) uses these stored values to compute posterior probabilities for training.

---

### 7.2 HMM_VITERBI – HMM Viterbi Algorithm

The HMM_VITERBI instruction computes one step of the Viterbi algorithm for finding the most probable state sequence. Unlike the forward algorithm which sums over all possible paths, the Viterbi algorithm takes the maximum over paths. This instruction is used for decoding speech recognition, gene finding, and any application where the best sequence of hidden states is needed.

**Encoding Format**

HMM_VITERBI uses opcode 0xA1. The instruction header contains opcode 0xA1, flags, and operand count of 5. The operands are: the destination vector for new Viterbi probabilities, the source vector for previous Viterbi probabilities, the transition matrix, the emission probabilities vector, and a backpointer matrix address.

The flags field uses the same encoding as HMM_FORWARD. Bits 8-9 encode the number of states. Bits 10-11 encode precision. Bit 12 enables log-space mode. Bits 13-15 are reserved.

The backpointer operand is a memory address where the instruction stores, for each current state j, the index i that maximized `old_viterbi[i] × transition[i][j]`. These backpointers are used to reconstruct the most probable state sequence after processing all observations.

**Operation Details**

The HMM_VITERBI instruction computes for each current state j: `new_viterbi[j] = emission[j] × max_i( old_viterbi[i] × transition[i][j] )`. The computation is similar to HMM_FORWARD, but the reduction network computes the maximum value and its index instead of the sum.

The instruction proceeds in three phases. In the first phase, each core computes `old_viterbi[i] × transition[i][j]` for a subset of the matrix. In the second phase, the reduction network finds the maximum value for each destination state and records the index that produced that maximum. In the third phase, the emission probability is multiplied, and the backpointer is stored.

The instruction completes in the same number of cycles as HMM_FORWARD: 2 + log2(N) cycles for the vector operations. The backpointer storage adds a memory write but does not affect the cycle count.

**Assembly Examples**

Example 1: Single Viterbi step for 256-state HMM
```assembly
; R1 = previous Viterbi probabilities (256 floats)
; R2 = transition matrix (256x256)
; R3 = emission probabilities (256 floats)
; R4 = backpointer matrix address
; R5 = destination for new Viterbi probabilities
HMM_VITERBI R5, R1, R2, R3, R4
```

This performs one step of the Viterbi algorithm. The new probabilities are stored at R5, and the backpointers are stored at R4. The backpointers occupy N integers (4 bytes each).

Example 2: Complete Viterbi decoding
```assembly
; Decode a sequence of 1000 emissions
MOV R10, #0          ; time step counter
MOV R11, initial_probs
MOV R12, backpointer_buffer
MOV R13, emissions
MOV R14, transition
loop:
LEA R15, [R13 + R10*1024]
LEA R16, [R12 + R10*1024]   ; backpointer for this step
HMM_VITERBI R11, R11, R14, R15, R16
ADD R10, #1
CMP R10, #1000
BRANCH LT, loop
; After loop, find best final state
; Trace back using stored backpointers to get state sequence
```

This loop processes the entire observation sequence. After the loop, the backpointers are traversed from the final time step back to the beginning to reconstruct the most probable state sequence.

Example 3: Log-space Viterbi (most common)
```assembly
HMM_VITERBI.LOG R5, R1, R2, R3, R4
```

The .LOG suffix indicates log-space probabilities. This eliminates underflow and simplifies the max operation (log(max) = max(log)). This is the standard form used in most Viterbi implementations.

Example 4: Viterbi with pruning (beam search)
```assembly
HMM_VITERBI R5, R1, R2, R3, R4
VECTOR_THRESHOLD K1, R5, #1e-10, GT
; Only keep best B states (beam width B)
VECTOR_COMPRESS R5, R5, K1   ; Compress to dense array
; Next step uses compressed state space
```

Beam search keeps only the best B states at each time step, dramatically reducing computation. The VECTOR_COMPRESS instruction removes pruned states.

Example 5: Remote Viterbi (distributed)
```assembly
; Transition matrix on blade 4
HMM_VITERBI R5, R1, @4:0x10000, R3, R4
```

The transition matrix is stored remotely. The instruction streams the matrix across the optical fabric, overlapping communication with computation.

Example 6: Viterbi for convolutional codes (error correction)
```assembly
; Convolutional code with 64 states (6-bit shift register)
; 2 output bits per input bit
HMM_VITERBI R5, R1, R2, R3, R4
```

Viterbi decoding of convolutional codes is a classic application. The state space size is 2^(K-1) where K is the constraint length. For K=7, there are 64 states.

Example 7: Viterbi with prior probabilities
```assembly
; Multiply Viterbi probabilities by prior before the first step
MUL.V R1, R1, prior   ; Apply prior
HMM_VITERBI R5, R1, R2, R3, R4
```

Prior probabilities can be incorporated by multiplying the initial Viterbi probabilities before the first step.

Example 8: Viterbi for gene finding
```assembly
; Gene finding HMM with 3 states per nucleotide position
; States: exon, intron, intergenic
; Total states: 3 × length of gene model
HMM_VITERBI R5, R1, R2, R3, R4
```

Bioinformatics gene finding uses HMMs with specialized state structures. The Viterbi algorithm finds the most probable gene structure.

Example 9: Viterbi with duration modeling (semi-Markov)
```assembly
; Semi-Markov HMM with explicit duration probabilities
; Requires additional bookkeeping beyond standard Viterbi
; Use multiple HMM_VITERBI calls for different durations
```

Semi-Markov HMMs model how long the system stays in each state. They require extensions to the standard Viterbi algorithm.

Example 10: Viterbi for online decoding (real-time)
```assembly
; Process emissions as they arrive, maintain best path
; Low latency: emit best partial path after fixed delay
loop:
WAIT_FOR_EMISSION
HMM_VITERBI R5, R1, R2, R3, R4
MOV R1, R5   ; Update for next step
; Output partial path after 100 steps
CMP R10, #100
BRANCH GE, output_path
```

Online Viterbi decoders process emissions in real time and can output partial paths with a fixed latency. This is used in real-time speech recognition.

---

### 7.3 HMM_BACKWARD – HMM Backward Algorithm

The HMM_BACKWARD instruction computes one step of the backward algorithm for a Hidden Markov Model. The backward algorithm computes the probability of the future observations given the current state, working backwards from the end of the sequence. Together with the forward algorithm, the backward algorithm enables the computation of posterior state probabilities and is essential for HMM training using the Baum-Welch algorithm.

**Encoding Format**

HMM_BACKWARD uses opcode 0xA2. The instruction header contains opcode 0xA2, flags, and operand count of 4. The operands are: the destination vector for new backward probabilities, the source vector for previous backward probabilities, the transition matrix, and the emission probabilities vector.

The flags field uses the same encoding as HMM_FORWARD. Bits 8-9 encode the number of states. Bits 10-11 encode precision. Bit 12 enables log-space mode. Bits 13-15 are reserved.

Unlike the forward algorithm, the backward algorithm does not require a scaling factor. The backward probabilities can become extremely small, so log-space mode is strongly recommended for long sequences.

**Operation Details**

The HMM_BACKWARD instruction computes for each current state i: `new_backward[i] = sum_j( transition[i][j] × emission[j] × old_backward[j] )`. The computation is similar to the forward algorithm but with the roles of i and j swapped and the emission applied at the current state rather than the next state.

The instruction proceeds in three phases. In the first phase, each core computes `transition[i][j] × emission[j] × old_backward[j]` for a subset of the matrix. In the second phase, the reduction network sums the contributions for each i. In the third phase, the result is stored.

The instruction completes in 2 + log2(N) cycles, identical to HMM_FORWARD.

**Assembly Examples**

Example 1: Single backward step
```assembly
; R1 = next backward probabilities (256 floats)
; R2 = transition matrix (256x256)
; R3 = emission probabilities (256 floats)
; R4 = destination for new backward probabilities
HMM_BACKWARD R4, R1, R2, R3
```

This performs one backward step, moving from time t+1 to time t. The new backward probabilities are stored at R4.

Example 2: Complete backward pass
```assembly
; Compute backward probabilities for a sequence of 1000 emissions
; Start with all ones at the end
MOV R10, #999        ; time step counter (starting from end)
MOV R11, ones        ; initial backward probabilities (all 1.0)
MOV R12, emissions   ; array of emission probability vectors
MOV R13, transition  ; transition matrix
; Precompute scaled emissions? Or compute on the fly
loop:
LEA R14, [R12 + R10*1024]   ; emission for time t
HMM_BACKWARD R11, R11, R13, R14
SUB R10, #1
CMP R10, #0
BRANCH GE, loop
; R11 now contains backward probabilities for time 0
```

This loop processes the observation sequence backwards, computing backward probabilities for each time step.

Example 3: Log-space backward algorithm
```assembly
HMM_BACKWARD.LOG R4, R1, R2, R3
```

The .LOG suffix selects log-space mode. This prevents underflow and uses log-sum-exp for the sum over states.

Example 4: Remote backward computation
```assembly
; Transition matrix on blade 4
HMM_BACKWARD R4, R1, @4:0x10000, R3
```

The transition matrix is stored remotely. The instruction streams the matrix across the optical fabric.

Example 5: Forward-backward for posterior probabilities
```assembly
; Compute posteriors: γ(t,i) = α(t,i) × β(t,i) / Σ_j α(t,j) × β(t,j)
; Assume forward probabilities stored in fwd_buffer
; Assume backward probabilities computed in bwd_buffer
MOV R10, #0
loop:
LD.V fwd, [fwd_buffer + R10*1024]
LD.V bwd, [bwd_buffer + R10*1024]
MUL.V gamma, fwd, bwd
; Normalize gamma
HADDPS sum, gamma, gamma   ; Sum all gamma values
DIV.V gamma, gamma, sum_S
ST.V [gamma_buffer + R10*1024], gamma
ADD R10, #1
CMP R10, #1000
BRANCH LT, loop
```

This loop computes the posterior state probabilities for each time step by combining forward and backward probabilities.

Example 6: Baum-Welch E-step using forward and backward
```assembly
; Accumulate expected transition counts
; This is the E-step of the Baum-Welch algorithm
HMM_BACKWARD bwd, bwd_next, trans, emiss
; Then compute xi(t,i,j) for all i,j and accumulate
```

The Baum-Welch algorithm uses both forward and backward probabilities to compute expected transition and emission counts for re-estimation.

Example 7: Backward with scaling for numerical stability
```assembly
; Use scaling factors from forward pass to scale backward pass
; This maintains numerical stability for long sequences
HMM_BACKWARD.SCALE R4, R1, R2, R3, [scale_buffer + t*4]
```

The .SCALE suffix indicates that the backward probabilities should be scaled using the scaling factors from the forward pass. This ensures that the forward and backward probabilities are on comparable scales.

Example 8: Parallel backward across multiple sequences
```assembly
; Process 8 sequences in parallel
BROADCAST HMM_BACKWARD R4, R1, @root:transition, R3
```

The BROADCAST instruction sends the HMM_BACKWARD instruction to all blades, each processing a different sequence.

Example 9: Backward for left-to-right HMM
```assembly
; For left-to-right HMMs, the transition matrix is upper triangular
; The hardware can exploit sparsity for speed
; Enable sparse mode via configuration register
CFG_HMM_SPARSE #1   ; Enable sparse mode
HMM_BACKWARD R4, R1, R2, R3
```

Left-to-right HMMs (common in speech recognition) have sparse transition matrices. The hardware can skip zero entries for improved performance.

Example 10: Backward for HMM with multiple observation streams
```assembly
; Separate emission probabilities for each stream
; Combine using product of independent streams
MUL.V R3_combined, R3_stream1, R3_stream2
HMM_BACKWARD R4, R1, R2, R3_combined
```

Some HMMs have multiple independent observation streams. The combined emission probability is the product of the individual stream probabilities.

---

### 7.4 SOFTMAX – Softmax Function

The SOFTMAX instruction computes the softmax function over a vector of logits. The softmax transforms a vector of real numbers into a probability distribution: `softmax(x)_i = e^{x_i} / Σ_j e^{x_j}`. The output values are positive and sum to 1. Softmax is the standard output activation function for multi-class classification in neural networks and appears in attention mechanisms.

**Encoding Format**

SOFTMAX uses opcode 0xA4. The instruction header contains opcode 0xA4, flags, and operand count of 2. The first operand is the destination vector. The second operand is the source vector. The instruction computes destination[i] = e^{source[i]} / Σ_j e^{source[j]} for all i.

The flags field controls vector length and precision. Bits 8-9 encode the vector length as a power of two: 00 for 4 elements (128-bit), 01 for 8 elements (256-bit), 10 for 16 elements (512-bit), and 11 for 32 elements (1024-bit). Bits 10-11 encode the precision: 00 for 32-bit float, 01 for 64-bit float, 10 for 16-bit float, and 11 for mixed precision. Bits 12-13 encode the normalization mode: 00 for full softmax (sum to 1), 01 for temperature-scaled softmax (divide logits by temperature first), 10 for sparse softmax (only compute for a subset), and 11 for log-softmax (compute log of softmax directly). Bits 14-15 are reserved.

The source operand must be a vector register or memory address. The destination operand can be the same as the source (in-place) or different.

**Operation Details**

The SOFTMAX instruction proceeds in three phases. In the first phase, the maximum value in the source vector is found. This is necessary for numerical stability, as exponentials of large numbers can overflow. The maximum is found using a reduction tree that takes log2(N) cycles.

In the second phase, each element is shifted by subtracting the maximum, then exponentiated using the EXP instruction. The exponentials are computed in parallel, taking 15 cycles for single-precision.

In the third phase, the exponentials are summed using a reduction tree (log2(N) cycles), and each exponential is divided by the sum. The divisions are performed in parallel.

The total latency is approximately 20 + 2×log2(N) cycles for single-precision. For a 16-element vector (512 bits), this is about 20 + 8 = 28 cycles.

**Assembly Examples**

Example 1: Basic softmax for 16 logits
```assembly
SOFTMAX ZMM1, ZMM2   ; ZMM1 = softmax(ZMM2), 16 elements
```

This computes the softmax of the 16 single-precision values in ZMM2 and stores the result in ZMM1. The output values are all between 0 and 1 and sum to 1.

Example 2: In-place softmax
```assembly
SOFTMAX ZMM1, ZMM1   ; Replace logits with probabilities
```

This computes the softmax in place, overwriting the input logits with the output probabilities. This saves register pressure.

Example 3: Temperature-scaled softmax
```assembly
; Temperature T controls sharpness: lower T = sharper distribution
SOFTMAX.TEMP ZMM1, ZMM2, #0.1   ; Very sharp (low temperature)
```

The .TEMP suffix indicates temperature scaling. The logits are divided by the temperature before softmax. A temperature of 0.1 produces a very sharp distribution (near one-hot). A high temperature produces a more uniform distribution.

Example 4: Log-softmax for numerical stability
```assembly
; log-softmax: log(softmax(x)) = x - log-sum-exp(x)
SOFTMAX.LOG ZMM1, ZMM2   ; ZMM1 = log(softmax(ZMM2))
```

The .LOG suffix computes the logarithm of the softmax directly, without computing the softmax first. This avoids underflow for very small probabilities and is used in cross-entropy loss calculations.

Example 5: Sparse softmax (only top-k)
```assembly
; Only compute softmax for the k highest logits
; This is used in efficient attention mechanisms
SOFTMAX.SPARSE ZMM1, ZMM2, K1, #8   ; Only top 8 elements
```

The .SPARSE suffix, combined with a mask register, computes softmax only for the selected elements. The remaining elements are set to zero. This is used in sparse attention mechanisms.

Example 6: Softmax for attention mechanism
```assembly
; Attention scores (Q·K^T) in ZMM1
; Apply softmax to get attention weights
SOFTMAX ZMM1, ZMM1   ; Attention weights (sum to 1)
; Then weighted sum of values: V · attention_weights
```

In transformer attention, softmax is applied to the dot product of queries and keys to produce attention weights. The weights sum to 1 and determine the contribution of each value.

Example 7: Remote softmax (distributed attention)
```assembly
; Logits stored on blade 4, compute softmax remotely
SOFTMAX R5, @4:0x10000   ; Softmax on remote blade
```

This computes softmax of a vector stored on a remote blade. The result can be stored locally or remotely. This enables distributed attention across multiple blades.

Example 8: Cross-entropy loss using softmax
```assembly
; Compute cross-entropy: -log(softmax(x)_c) where c is correct class
; Directly compute using log-softmax
SOFTMAX.LOG ZMM1, ZMM2   ; ZMM1 = log(softmax)
MOV R2, correct_class
EXTRACT R3, ZMM1, R2     ; R3 = log(probability of correct class)
NEG R4, R3               ; R4 = cross-entropy loss
```

Cross-entropy loss for classification is the negative log of the softmax probability of the correct class. The log-softmax variant avoids computing the softmax explicitly.

Example 9: Vector of softmaxes (batch processing)
```assembly
; Process 16 independent softmax operations, each on 16 elements
; This is 256 total elements in a 4096-bit register (if supported)
SOFTMAX ZMM1, ZMM2   ; 16 softmaxes in parallel
```

For batch processing, the vector length encoding can be set to process multiple independent softmax operations in a single instruction. Each group of elements is normalized independently.

Example 10: Gumbel-softmax for sampling
```assembly
; Gumbel-softmax: add Gumbel noise before softmax
; Sample from Gumbel distribution
GUMBEL ZMM3, noise   ; Generate Gumbel noise
ADD.V ZMM2, ZMM2, ZMM3   ; Add noise to logits
SOFTMAX ZMM1, ZMM2   ; Softmax with noise = differentiable sample
```

The Gumbel-softmax trick enables sampling from a categorical distribution while maintaining differentiability. This is used in variational autoencoders and reinforcement learning.

---

### 7.5 LOG_SUM_EXP – Log of Sum of Exponentials

The LOG_SUM_EXP instruction computes `log( Σ_i e^{x_i} )` for a vector of inputs. This operation appears frequently in log-space HMM computations, as the log of a sum of probabilities. Computing it directly as `log(sum(exp(x)))` can overflow, so the instruction uses the numerically stable formula: `log_sum_exp(x) = max(x) + log( Σ_i e^{x_i - max(x)} )`.

**Encoding Format**

LOG_SUM_EXP uses opcode 0xA5. The instruction header contains opcode 0xA5, flags, and operand count of 2. The first operand is the scalar destination. The second operand is the source vector. The instruction computes destination = log( Σ_i e^{source[i]} ).

The flags field encodes vector length and precision identically to SOFTMAX. Bits 8-9 encode vector length. Bits 10-11 encode precision. Bits 12-13 are reserved. Bit 14 enables the "log-space addition" mode where the instruction takes two log-probabilities and returns `log(e^a + e^b)`.

**Operation Details**

The LOG_SUM_EXP instruction proceeds in three phases. First, the maximum value in the vector is found using a reduction tree (log2(N) cycles). Second, each element is shifted by subtracting the maximum, exponentiated using EXP (15 cycles for single-precision), and summed using a reduction tree (log2(N) cycles). Third, the logarithm of the sum is computed using LOG (18 cycles) and added back to the maximum.

The total latency is approximately 35 + 2×log2(N) cycles for single-precision. A specialized "log-add" mode for two inputs completes in a single cycle.

**Assembly Examples**

Example 1: Basic log-sum-exp
```assembly
LOG_SUM_EXP R1, ZMM2   ; R1 = log( Σ e^{ZMM2[i]} )
```

This computes the log-sum-exp of the 16 values in ZMM2. The result is stored in scalar register R1.

Example 2: Log-space forward algorithm using LOG_SUM_EXP
```assembly
; Log-space forward: log(α_t(j)) = log(emission_j) + log-sum-exp_i( log(α_{t-1}(i)) + log(transition_ij) )
; This uses LOG_SUM_EXP for the sum over i
LOG_SUM_EXP R1, ZMM2   ; R1 = log-sum-exp of previous values
ADD R2, R1, log_emiss ; Add log emission
```

The log-space forward algorithm uses LOG_SUM_EXP to compute the log of the sum of exponentials.

Example 3: Log-add for two numbers
```assembly
; Compute log(e^a + e^b) = a + log(1 + e^{b-a}) for a >= b
LOG_SUM_EXP.2 R1, R2, R3   ; R1 = log(e^R2 + e^R3)
```

The .2 suffix indicates the two-input log-add mode. This is faster than the full vector version and completes in a single cycle.

Example 4: Log-space Viterbi with log-sum-exp for soft outputs
```assembly
; Soft-output Viterbi uses log-sum-exp instead of max
LOG_SUM_EXP R1, ZMM2   ; Soft maximum for each state
```

Soft-output Viterbi (SOVA) replaces the max operation with log-sum-exp to produce soft decisions (confidence values).

Example 5: Normalization in log-space
```assembly
; Normalize log-probabilities: log(p_i) - log(Σ p_j)
LOG_SUM_EXP R1, ZMM2   ; R1 = log(Σ p_j)
SUB.V ZMM3, ZMM2, R1_S   ; Normalized log-probabilities
```

To normalize log-probabilities so they sum to 1, subtract the log-sum-exp from each log-probability.

Example 6: Remote log-sum-exp
```assembly
LOG_SUM_EXP R1, @4:0x10000   ; Compute over remote vector
```

This computes log-sum-exp of a vector stored on a remote blade. The vector is streamed across the optical fabric.

Example 7: Log-sum-exp for mixture models
```assembly
; Gaussian mixture model: log(p(x)) = log-sum-exp( log(weight_k) + log(N(x|μ_k,σ_k)) )
; Compute component log-likelihoods in ZMM2
LOG_SUM_EXP R1, ZMM2   ; R1 = log(mixture density)
```

Mixture models compute the log probability as the log-sum-exp of weighted component log-likelihoods.

Example 8: Log-sum-exp for multi-sequence alignment
```assembly
; Align 8 sequences, compute log probability of alignment
LOG_SUM_EXP R1, ZMM2   ; Sum over alignment paths
```

In bioinformatics, sequence alignment algorithms use log-sum-exp to sum over all possible alignments.

Example 9: Numerical stable log-sum-exp with precomputed max
```assembly
; If max is already known, save the reduction step
; Use direct encoding with max in a register
LOG_SUM_EXP.M R1, ZMM2, R_max   ; R_max = precomputed max
```

The .M suffix indicates that the maximum value is provided in a register, saving the first reduction pass.

Example 10: Log-sum-exp for expectation-maximization
```assembly
; E-step: compute log-sum-exp of responsibilities
LOG_SUM_EXP R1, ZMM2   ; Log of total responsibility
```

The expectation-maximization algorithm uses log-sum-exp to compute normalization constants for the E-step.

---

### 7.6 SPARSE_DOT – Sparse Vector Dot Product

The SPARSE_DOT instruction computes the dot product of a dense vector and a sparse vector represented as an index-value list. This is essential for machine learning models with sparse features (such as recommendation systems, natural language processing with large vocabularies, and sparse neural networks) where most elements are zero and storing all zeros is wasteful.

**Encoding Format**

SPARSE_DOT uses opcode 0xA9. The instruction header contains opcode 0xA9, flags, and operand count of 4. The operands are: the scalar destination, the dense vector base address, the sparse index list address, and the sparse value list address.

The flags field controls the format of the sparse representation. Bits 8-9 encode the index size: 00 for 16-bit indices, 01 for 32-bit indices, 10 for 64-bit indices, and 11 for packed indices (multiple indices per word). Bits 10-11 encode the value precision: 00 for 32-bit float, 01 for 64-bit float, 10 for 16-bit float, and 11 for 8-bit integer. Bit 12 enables double-buffered streaming mode. Bits 13-15 are reserved.

The sparse representation consists of two parallel lists: an index list (starting at the address in the third operand) and a value list (starting at the address in the fourth operand). The lists are terminated by a sentinel index with a value of all ones (or a specified end-of-list marker).

**Operation Details**

The SPARSE_DOT instruction streams the index and value lists from memory. For each index, it loads the corresponding value from the dense vector and multiplies it by the sparse value. The products are accumulated in a high-precision accumulator. The instruction continues until the end-of-list marker is reached.

The dense vector must be stored contiguously in memory with elements of the specified precision. The indices are offsets from the base address, measured in elements (not bytes). For example, an index of 5 means the sixth element of the dense vector.

The instruction completes in one cycle per non-zero element, plus the memory access latency for streaming the lists. For a sparse vector with 32 non-zero entries, the instruction takes approximately 32 cycles.

**Assembly Examples**

Example 1: Basic sparse dot product
```assembly
; R1 = result, R2 = dense vector base
; R3 = index list, R4 = value list
SPARSE_DOT R1, R2, R3, R4
```

This computes the dot product of the dense vector at R2 and the sparse vector described by the index list at R3 and value list at R4.

Example 2: Sparse vector format in memory
```assembly
; Index list: 0x0000, 0x0005, 0x0012, 0xFFFF (terminator)
; Value list: 0.5, -0.3, 0.8, (any value for terminator)
; Dense vector length: at least 0x0012 + 1 = 19 elements
; Result = dense[0]*0.5 + dense[5]*(-0.3) + dense[18]*0.8
```

This shows the memory layout for a sparse vector with three non-zero elements.

Example 3: Sparse dot product for recommendation system
```assembly
; User vector (dense) at R2, item features (sparse) at R3,R4
; Compute predicted rating
SPARSE_DOT R1, R2, R3, R4   ; R1 = prediction
```

Recommendation systems represent users as dense embeddings and items as sparse bags of features. The predicted rating is the dot product.

Example 4: Batch of sparse dot products
```assembly
; Process 8 sparse vectors in parallel on 8 blades
BROADCAST SPARSE_DOT R1, R2, @blade:index, @blade:value
```

Each blade computes the dot product of the same dense vector (broadcast) with a different sparse vector stored on that blade.

Example 5: Sparse dot product with 8-bit values
```assembly
SPARSE_DOT.I8 R1, R2, R3, R4   ; 8-bit integer values
```

The .I8 suffix selects 8-bit integer values. The dense vector is also stored as 8-bit integers. The product is accumulated in a 32-bit integer before conversion to float.

Example 6: Sparse dot product for TF-IDF
```assembly
; Document vector (dense TF-IDF) at R2
; Query terms (sparse) at R3,R4
SPARSE_DOT R1, R2, R3, R4   ; Relevance score
```

Information retrieval uses dot products between query vectors (sparse) and document vectors (dense) for relevance scoring.

Example 7: Streaming sparse dot product (double-buffered)
```assembly
SPARSE_DOT.STREAM R1, R2, R3, R4   ; Stream mode
```

The .STREAM suffix enables double-buffered streaming. The instruction prefetches the next block of index-value pairs while computing the current block, hiding memory latency.

Example 8: Sparse dot product with negative indices (offset)
```assembly
; Use index base register to apply offset to all indices
MOV R5, #100   ; Base offset
SPARSE_DOT.OFFSET R1, R2, R3, R4, R5   ; Indices are relative to R5
```

The .OFFSET suffix adds a base offset to all indices. This allows reuse of the same sparse vector with different dense vector segments.

Example 9: Remote sparse dot product
```assembly
; Dense vector on blade 4, sparse lists local
SPARSE_DOT R1, @4:0x10000, R3, R4
```

This reads the dense vector from remote blade 4 while reading the sparse lists locally. The remote dense vector is accessed as needed for each index.

Example 10: Gradient computation with sparse features
```assembly
; Compute gradient for sparse feature j: gradient = error * value_j
; For all non-zero features in the sparse vector
SPARSE_DOT R1, R2, R3, R4   ; Forward pass (prediction)
SUB error, target, R1        ; Error
; For each non-zero feature: gradient_j = error * value_j
; This requires iterating over the sparse list again
```

In training, the gradient for sparse features is the product of the error and the feature value. The same sparse list is used.

---

This concludes Chapter 7 of the Instruction Set Reference. The remaining chapters will cover System Instructions, Interconnect Instructions, Memory Management Instructions, and Protection Instructions.

# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 8: System Instructions

### 8.1 SYSENTER – Enter Kernel Mode

The SYSENTER instruction transfers control from user code to the operating system kernel. It is the primary mechanism for making system calls, requesting operating system services, and entering privileged execution modes. Unlike a simple CALL instruction, SYSENTER changes the privilege level, saves the user context, and jumps to a predefined kernel entry point. The instruction is designed for low-latency system call entry, completing in a small number of cycles.

**Encoding Format**

SYSENTER uses opcode 0x60. The instruction header contains opcode 0x60, flags, and operand count of 0. There are no explicit operands because the target address and stack pointers are stored in model-specific registers configured during system initialization.

The flags field has bit 8 reserved for an asynchronous variant that returns immediately and signals completion via an interrupt. Bits 9-15 are reserved.

The following model-specific registers must be configured before SYSENTER is used:
- SYSENTER_CS: The code segment selector for kernel mode
- SYSENTER_ESP: The kernel stack pointer
- SYSENTER_EIP: The kernel entry point address
- SYSENTER_SS: The stack segment selector for kernel mode

These registers can only be written by code running at privilege level 0 (the highest privilege level).

**Operation Details**

When SYSENTER executes, the following steps occur in order. First, the current privilege level is checked. If the instruction is executed at privilege level 0, it raises an exception because SYSENTER is only valid from user mode (privilege level 3). The current user-mode instruction pointer, stack pointer, and flags are saved in hidden registers that are not accessible to software.

The processor then loads the kernel code segment from SYSENTER_CS, the kernel stack pointer from SYSENTER_ESP, and the kernel instruction pointer from SYSENTER_EIP. The stack segment is loaded from SYSENTER_SS. The privilege level is changed to 0. The instruction pointer is set to the kernel entry point, and execution continues in kernel mode.

The entire transition takes approximately 15 cycles on a 2 GHz core. This is significantly faster than an interrupt or trap gate, which can take 100 cycles or more.

The user context (registers R1 through R31, vector registers, and flags) is preserved. The kernel can access the saved user instruction pointer and stack pointer through model-specific registers. The kernel must save any registers it will modify before modifying them.

**Assembly Examples**

Example 1: Basic system call
```assembly
; User code:
MOV R1, #1        ; System call number (e.g., write)
MOV R2, fd        ; First argument (file descriptor)
MOV R3, buffer    ; Second argument (buffer address)
MOV R4, count     ; Third argument (byte count)
SYSENTER          ; Enter kernel
; Returns here after system call completes
```

This is the standard pattern for making a system call. Arguments are placed in registers according to the system call convention. The SYSENTER instruction transfers control to the kernel.

Example 2: Kernel entry point
```assembly
; Kernel code at SYSENTER_EIP:
sysenter_entry:
; Save user registers that will be used
PUSH R1
PUSH R2
PUSH R3
PUSH R4
; Get system call number from R1
CMP R1, #MAX_SYSCALL
BRANCH HI, invalid_syscall
; Jump through syscall table
LEA R5, syscall_table
SHL R1, #3         ; Multiply by 8 (address size)
ADD R5, R1
JMP [R5]           ; Call syscall handler
```

The kernel entry point saves any registers it will modify, then dispatches to the appropriate system call handler based on the system call number in R1.

Example 3: System call return (using SYSEXIT)
```assembly
; After system call handler completes:
; Restore saved registers
POP R4
POP R3
POP R2
POP R1
SYSEXIT           ; Return to user mode
```

The kernel restores the saved registers and executes SYSEXIT to return to user mode.

Example 4: System call with error handling
```assembly
; User code:
SYSENTER
BRANCH CS, error_handler   ; Check carry flag for error
; Success path
error_handler:
; Handle error (error code in R1)
```

Many operating systems use the carry flag to indicate whether a system call succeeded. The flag is set by the kernel before returning via SYSEXIT.

Example 5: Fast system call for getpid (no argument)
```assembly
; User code:
MOV R1, #GETPID_SYSCALL
SYSENTER
; Process ID returned in R1
```

Simple system calls that take no arguments can be very fast. The entire round trip (user->kernel->user) takes approximately 30 cycles.

Example 6: System call with validation
```assembly
; Kernel entry with parameter validation
sysenter_entry:
CMP R1, #MAX_SYSCALL
BRANCH HI, invalid
; Validate buffer address (R3)
SEGMENT_LOOKUP R5, R3   ; Get segment descriptor for address
TEST R5, #PERM_READ
BRANCH EQ, invalid
; Valid, proceed
```

The kernel validates all arguments before acting on them. The SEGMENT_LOOKUP instruction checks whether the user process has permission to access the provided address.

Example 7: Asynchronous system call
```assembly
; User code:
MOV R1, #ASYNC_SYSCALL
SYSENTER.ASYNC   ; Return immediately, completion signaled later
; Continue execution while kernel processes request
; Later, wait for completion interrupt
WAIT_FOR_INTERRUPT
```

The .ASYNC suffix indicates that the system call should return immediately. The kernel processes the request asynchronously and signals completion via an interrupt. This is used for I/O operations that may take a long time.

Example 8: Remote system call
```assembly
; User code on blade 1:
; System call should be executed on blade 4
MOV R1, #REMOTE_SYSCALL
MOV R5, #4        ; Target blade
SYSENTER.REMOTE   ; Execute syscall on blade 4
```

The .REMOTE suffix indicates that the system call should be executed on a different blade. The hardware sends the system call request across the optical fabric to the target blade, which executes the system call and returns the result.

Example 9: Nested system calls (not allowed)
```assembly
; Kernel code attempting SYSENTER:
SYSENTER   ; This will fault because already in kernel mode
```

Executing SYSENTER while already in kernel mode (privilege level 0) raises an exception. The kernel must use CALL or JMP to invoke other kernel functions.

Example 10: System call with user context access
```assembly
; Kernel accessing user registers saved by SYSENTER
; Saved user R1 is accessible via SYSENTER_USER_R1 (model-specific)
MOV R5, SYSENTER_USER_R1   ; Get user R1 value
; Modified user R1 will be restored on SYSEXIT
MOV SYSENTER_USER_R1, R6   ; Set new value for user R1 on return
```

The kernel can read and modify the saved user registers through model-specific registers. This allows system calls to return results in registers.

---

### 8.2 SYSEXIT – Exit Kernel Mode

The SYSEXIT instruction returns control from kernel mode to user code after a system call. It is the counterpart to SYSENTER and must only be executed from kernel mode. SYSEXIT restores the user context that was saved by SYSENTER and resumes user execution at the instruction following the original SYSENTER.

**Encoding Format**

SYSEXIT uses opcode 0x61. The instruction header contains opcode 0x61, flags, and operand count of 0. There are no explicit operands because the return address and stack pointers are restored from the saved context.

The flags field has bit 8 reserved for returning with a different stack pointer (useful for system calls that change the user stack). Bits 9-15 are reserved.

The following model-specific registers are used (restored from the values saved by SYSENTER):
- SYSEXIT_CS: The user code segment selector
- SYSEXIT_SS: The user stack segment selector
- The user instruction pointer and stack pointer are restored from hidden registers

**Operation Details**

When SYSEXIT executes, the following steps occur. First, the current privilege level is checked. If the instruction is executed at privilege level 3 (user mode), it raises an exception because SYSEXIT is only valid from kernel mode.

The processor then loads the user code segment from the saved context, the user stack pointer from the saved context, and the user instruction pointer from the saved context. The privilege level is changed to 3. Execution continues at the instruction following the original SYSENTER.

The entire transition takes approximately 12 cycles on a 2 GHz core.

**Assembly Examples**

Example 1: Basic return from system call
```assembly
; Kernel code after handling system call:
SYSEXIT   ; Return to user mode
```

This is the simplest form of SYSEXIT. It restores the saved user context and resumes user execution.

Example 2: System call returning a value
```assembly
; Kernel code:
MOV R1, result_value   ; Set return value
SYSEXIT                ; Return to user with result in R1
```

The kernel places the return value in R1. When SYSEXIT restores the user context, R1 contains this value.

Example 3: System call setting error flag
```assembly
; Kernel code (error case):
STC                    ; Set carry flag (error indicator)
SYSEXIT                ; Return with error flag set
```

The kernel can set condition flags before returning. The user code can test these flags to determine whether the system call succeeded.

Example 4: System call with modified stack pointer
```assembly
; Kernel code (changing user stack):
MOV SYSENTER_USER_ESP, new_stack   ; Change saved stack pointer
SYSEXIT.SP                         ; Return with new stack
```

The .SP suffix indicates that the user stack pointer should be changed to the value stored in SYSENTER_USER_ESP before returning. This is used for system calls that create new threads or change the stack layout.

Example 5: System call that never returns
```assembly
; Kernel code for process exit:
; Do not execute SYSEXIT
JMP scheduler   ; Switch to another process
```

A process that exits never executes SYSEXIT. The kernel scheduler switches to another process without returning to the exited process.

Example 6: System call with signal pending
```assembly
; Kernel code after system call:
; Check if signal pending for this process
CMP signal_pending, #0
BRANCH EQ, no_signal
; Deliver signal by modifying return address
MOV SYSENTER_USER_EIP, signal_handler
SYSEXIT   ; Return to signal handler, not original user code
no_signal:
SYSEXIT   ; Normal return
```

If a signal is pending for the process, the kernel can modify the saved instruction pointer to point to the signal handler instead of returning to the original user code.

Example 7: Remote system call return
```assembly
; On blade 4, after handling remote system call:
SYSEXIT.REMOTE   ; Return to caller on original blade
```

The .REMOTE suffix indicates that the return should be sent across the optical fabric to the blade that made the remote system call.

Example 8: System call with FPU state change
```assembly
; Kernel code modifying FPU state:
; Modify saved vector registers
MOV SYSENTER_USER_XMM0, new_value
SYSEXIT   ; Return with modified vector registers
```

The kernel can modify the saved vector registers, affecting the user's FPU state after the system call.

Example 9: Fast system call path (no register save)
```assembly
; For very simple system calls that don't modify registers:
; Skip saving registers at entry
sysenter_fast:
SYSEXIT   ; Return immediately
```

For extremely simple system calls (like getpid), the kernel may not need to save any registers. The entry and exit are very fast.

Example 10: System call with audit logging
```assembly
; Kernel code with audit:
; Log system call
CALL audit_log
SYSEXIT   ; Return even if audit fails (don't block user)
```

Audit logging should not block the system call return. The kernel logs the call and then returns to user mode even if the logging operation is not yet complete.

---

### 8.3 IN – Input from Port

The IN instruction reads a byte, word, or doubleword from an I/O port. I/O ports are separate address spaces used for communication with legacy devices such as serial ports, parallel ports, and certain system controllers. In the PIP CISC architecture, I/O ports are memory-mapped by default, but the IN/OUT instructions are provided for compatibility with legacy software and for accessing devices that do not support memory-mapped I/O.

**Encoding Format**

IN uses opcode 0x62. The instruction header contains opcode 0x62, flags, and operand count of 2. The first operand is the destination register. The second operand is the port number (immediate or from a register).

The flags field has bit 8 for string I/O (repeated IN for multiple values), bit 9 for the width (0=byte, 1=word, 2=doubleword, 3=quadword), and bits 10-15 reserved.

The port number can be an 8-bit immediate (ports 0-255) or a 16-bit value from a register (ports 0-65535). The destination register must be a general-purpose register. The size of the transfer is determined by the width field in the flags.

**Operation Details**

When IN executes, the following steps occur. The privilege level is checked. I/O port access is typically restricted to kernel mode, but the I/O privilege level (IOPL) field in the flags register can grant user-mode access to specific ports.

The port number is computed from the operand. The I/O controller reads the specified port. The data is returned and stored in the destination register. For byte accesses, the data is stored in the low 8 bits of the register; for word accesses, the low 16 bits; for doubleword accesses, the low 32 bits; for quadword accesses, the full 64 bits.

The instruction takes approximately 50 cycles for a local port access, as it involves communication with the I/O controller over a separate bus. For performance-critical code, memory-mapped I/O using MOV instructions is preferred.

**Assembly Examples**

Example 1: Read byte from port
```assembly
IN R1, #0x60   ; Read byte from keyboard controller port 0x60
```

This reads a byte from the keyboard controller. The data is stored in the low 8 bits of R1.

Example 2: Read word from port using register port number
```assembly
MOV R2, #0x3F8   ; COM1 serial port base
IN.W R1, R2      ; Read word from port 0x3F8 (COM1 data register)
```

The .W suffix selects word access. The port number is taken from register R2. This is useful when the port number is computed at runtime.

Example 3: Read doubleword from port
```assembly
IN.D R1, #0x1F0   ; Read doubleword from IDE primary data port
```

The .D suffix selects doubleword (32-bit) access. This reads 4 bytes from the specified port.

Example 4: String input (multiple bytes)
```assembly
; Read 32 bytes from port 0x3F8 into buffer at R1
MOV R2, #32      ; Count
IN.S R1, #0x3F8  ; String input (repeated)
```

The .S suffix enables string mode. The instruction reads count bytes from the port into consecutive memory locations starting at the address in R1.

Example 5: Read from port with I/O privilege check
```assembly
; User code attempting I/O port access
IN R1, #0x80    ; May fault if IOPL not set
```

User code may not have permission to access I/O ports. The I/O privilege level (IOPL) in the flags register determines which ports user code can access.

Example 6: Remote port access (virtualized)
```assembly
; Read from port on remote blade (virtual I/O)
IN R1, @4:0x60   ; Read from blade 4's port 0x60
```

The .REMOTE variant reads from an I/O port on a remote blade. This is used in virtualized environments where I/O devices are attached to a specific blade.

Example 7: Polling a device status port
```assembly
; Wait for device ready
loop:
IN R1, #0x3FD   ; Read COM1 line status register
TEST R1, #0x20  ; Test transmitter empty bit
BRANCH EQ, loop ; Loop if not ready
```

This polling loop waits for a serial port to be ready to transmit. The IN instruction reads the status port repeatedly until the ready bit is set.

Example 8: Read from port with timeout
```assembly
MOV R2, #1000000   ; Timeout counter
loop:
IN R1, #0x3FD
TEST R1, #0x01     ; Data ready bit
BRANCH NE, data_ready
SUB R2, #1
CMP R2, #0
BRANCH NE, loop
; Timeout occurred
```

This polling loop includes a timeout counter to prevent infinite waiting if the device never becomes ready.

Example 9: Read from configuration space (PCI)
```assembly
; Read from PCI configuration space
; First write address to config address port
MOV R1, #0x80000000   ; Enable bit + bus/device/function
OUT #0xCF8, R1        ; Write to config address port
IN R1, #0xCFC         ; Read from config data port
```

PCI configuration space is accessed using two ports: an address port and a data port. This sequence reads a 32-bit configuration value.

Example 10: Fast IN for performance counters
```assembly
; Read performance counter from port (if available)
IN.D R1, #0xE4   ; Read performance counter
```

Some systems provide performance counters accessible via I/O ports. This instruction reads the counter with minimal overhead.

---

### 8.4 OUT – Output to Port

The OUT instruction writes a byte, word, or doubleword to an I/O port. It is the counterpart to IN and is used for sending data to legacy devices. Like IN, OUT is primarily for compatibility; memory-mapped I/O using MOV is preferred for performance.

**Encoding Format**

OUT uses opcode 0x63. The instruction header contains opcode 0x63, flags, and operand count of 2. The first operand is the port number. The second operand is the source register or immediate value to output.

The flags field has bit 8 for string I/O (repeated OUT for multiple values), bit 9 for the width (0=byte, 1=word, 2=doubleword, 3=quadword), and bits 10-15 reserved.

The port number can be an 8-bit immediate or a 16-bit value from a register. The source can be a register or an immediate value.

**Operation Details**

When OUT executes, the following steps occur. The privilege level is checked. The port number is computed. The data from the source operand is written to the specified port. For byte writes, the low 8 bits are used; for word writes, the low 16 bits; for doubleword writes, the low 32 bits; for quadword writes, the full 64 bits.

The instruction takes approximately 50 cycles for a local port access.

**Assembly Examples**

Example 1: Write byte to port
```assembly
OUT #0x60, R1   ; Write byte from R1 to port 0x60
```

This writes a byte to the keyboard controller command port. The low 8 bits of R1 are used.

Example 2: Write word to serial port
```assembly
OUT.W #0x3F8, R1   ; Write word to COM1 data register
```

The .W suffix selects word access. The low 16 bits of R1 are written.

Example 3: Write immediate value to port
```assembly
OUT #0x80, #0x01   ; Write 0x01 to port 0x80 (POST code)
```

This writes an immediate value directly to a port, without using a register. This is common for debug ports where the value is a small constant.

Example 4: String output (multiple bytes)
```assembly
; Write 32 bytes from buffer at R1 to port 0x3F8
MOV R2, #32      ; Count
OUT.S #0x3F8, R1 ; String output
```

The .S suffix enables string mode. The instruction writes count bytes from consecutive memory locations starting at the address in R1 to the specified port.

Example 5: Device initialization sequence
```assembly
; Initialize serial port (COM1)
OUT #0x3FB, #0x80   ; Set DLAB=1 (enable baud rate divisor)
OUT #0x3F8, #0x0C   ; Low byte of divisor (9600 baud)
OUT #0x3F9, #0x00   ; High byte of divisor
OUT #0x3FB, #0x03   ; 8N1 format
```

This sequence initializes a serial port by writing configuration bytes to various control registers.

Example 6: Sending a command to a device
```assembly
; Send command 0x20 to IDE controller
OUT #0x1F7, #0x20   ; Write command to IDE command register
```

This sends a read command to an IDE hard drive controller.

Example 7: Remote port output (virtualized)
```assembly
; Write to port on remote blade
OUT.REMOTE @4:0x60, R1   ; Write to blade 4's port 0x60
```

The .REMOTE variant writes to an I/O port on a remote blade. This is used in virtualized environments.

Example 8: Generating a beep using PC speaker
```assembly
; Enable speaker output
IN R1, #0x61       ; Read port B
OR R1, #0x03       ; Set bits for speaker and timer
OUT #0x61, R1      ; Write back
; Set timer frequency (1.19318 MHz / desired frequency)
OUT #0x42, #0x34   ; Write to timer command port
OUT #0x40, #0x50   ; Low byte of divisor
OUT #0x40, #0x0C   ; High byte of divisor
```

This sequence programs the PC speaker to produce a tone.

Example 9: Debug output via POST port
```assembly
; Output debug code to POST port (commonly 0x80)
OUT #0x80, #0x12   ; Code 0x12 = "initializing memory controller"
```

Many systems use port 0x80 for Power-On Self-Test (POST) debug codes. This instruction outputs a debug code that can be observed on a logic analyzer or POST reader.

Example 10: OUT with register port number
```assembly
; Write to port number stored in R2
MOV R2, #0x3F8
OUT R2, R1         ; Write R1 to port in R2
```

The port number comes from a register. This is useful when the port number is computed at runtime or comes from a table.

---

### 8.5 CFG_VIDEO – Configure Video Output

The CFG_VIDEO instruction configures a video output tile to read a memory region as a framebuffer. Unlike traditional systems where video output requires a separate graphics card and driver, the PIP CISC architecture allows any memory region to be designated as a video framebuffer. The video output tile continuously scans this memory region and converts its contents to display signals (HDMI, DisplayPort, etc.).

**Encoding Format**

CFG_VIDEO uses opcode 0x64. The instruction header contains opcode 0x64, flags, and operand count of 5. The operands are: the framebuffer base address, the width in pixels, the height in pixels, the color format, and the refresh rate.

The flags field encodes the output tile identifier (bits 8-11, up to 16 video outputs) and the display interface (bits 12-14: 000=HDMI, 001=DisplayPort, 010=DVI, 011=VGA, 100=LVDS, 101=eDP). Bit 15 enables double-buffering with automatic page flipping.

The color format operand specifies the pixel encoding using an 8-bit value:
- 0x01: RGB888 (24-bit, 8 bits per channel)
- 0x02: RGB101010 (30-bit, 10 bits per channel)
- 0x03: RGBA8888 (32-bit with alpha)
- 0x04: YUV422 (16-bit, 4:2:2 subsampling)
- 0x05: YUV420 (12-bit, 4:2:0 subsampling)
- 0x06: Monochrome (8-bit grayscale)

The refresh rate is specified in millihertz (mHz). For example, 60000 for 60 Hz, 120000 for 120 Hz.

**Operation Details**

When CFG_VIDEO executes, the following steps occur. The instruction must be executed by a System core at privilege level 0 (kernel mode). The framebuffer address range is validated to ensure it falls within a memory segment that the current owner has permission to use as video memory.

The video output tile is configured with the specified parameters. It begins scanning the framebuffer at the next vertical blanking interval to avoid tearing. The tile reads the framebuffer at the refresh rate and generates the appropriate video signal on the specified display interface.

If double-buffering is enabled, the instruction also configures a second framebuffer. The video output tile alternates between the two buffers on each frame. The user can write to the inactive buffer while the active buffer is being displayed, then swap buffers with another CFG_VIDEO instruction.

**Assembly Examples**

Example 1: Configure 1920x1080 RGB output at 60 Hz
```assembly
; Configure video output 0 as 1080p RGB
CFG_VIDEO #0, framebuffer, #1920, #1080, #0x01, #60000
```

This configures video output 0 to display the memory region at address "framebuffer" as a 1920x1080 RGB framebuffer at 60 Hz.

Example 2: Configure 4K output with double buffering
```assembly
; Configure 3840x2160 RGBA output at 60 Hz with double buffering
CFG_VIDEO.DB #0, framebuffer0, #3840, #2160, #0x03, #60000
```

The .DB suffix enables double buffering. The hardware expects two consecutive framebuffers of size width × height × pixel_size.

Example 3: Change framebuffer address (page flip)
```assembly
; Swap to the other buffer in double-buffered configuration
CFG_VIDEO.SWAP #0, new_framebuffer   ; Set new framebuffer address
```

The .SWAP suffix changes the active framebuffer without reconfiguring other parameters. This is used for page flipping in animations and games.

Example 4: Configure DisplayPort output at 144 Hz
```assembly
; Configure 2560x1440 DisplayPort output at 144 Hz
CFG_VIDEO.DP #1, framebuffer, #2560, #1440, #0x01, #144000
```

The .DP suffix selects DisplayPort interface. The instruction configures video output 1.

Example 5: Configure YUV output for video playback
```assembly
; Configure YUV 4:2:0 output for efficient video display
CFG_VIDEO #2, yuv_buffer, #1920, #1080, #0x05, #60000
```

YUV formats are more efficient for video playback because they use less bandwidth than RGB.

Example 6: Configure multiple displays (extended desktop)
```assembly
; Two displays: output 0 and output 1
CFG_VIDEO #0, fb_left, #1920, #1080, #0x01, #60000
CFG_VIDEO #1, fb_right, #1920, #1080, #0x01, #60000
; Renderer writes to both framebuffers independently
```

This configures two independent video outputs, each with its own framebuffer. This implements an extended desktop across two monitors.

Example 7: Configure mirrored display (same framebuffer for both outputs)
```assembly
; Both outputs use the same framebuffer
CFG_VIDEO #0, shared_fb, #1920, #1080, #0x01, #60000
CFG_VIDEO #1, shared_fb, #1920, #1080, #0x01, #60000
```

Both video outputs read from the same framebuffer, creating a mirrored display.

Example 8: Remote video output (display connected to different blade)
```assembly
; Configure video output on blade 4 from local framebuffer
CFG_VIDEO.REMOTE @4:0, framebuffer, #1920, #1080, #0x01, #60000
```

The video output is physically attached to blade 4, but the framebuffer is on the local blade. The hardware streams the framebuffer across the optical fabric.

Example 9: Change resolution at runtime
```assembly
; Switch from 1080p to 4K
CFG_VIDEO #0, new_framebuffer, #3840, #2160, #0x01, #60000
```

The display can be reconfigured at any time. The change takes effect at the next vertical blanking interval.

Example 10: Disable video output
```assembly
; Turn off video output 0
CFG_VIDEO.OFF #0
```

The .OFF suffix disables the specified video output, stopping the scan-out process and powering down the display interface.

---

### 8.6 CFG_AUDIO – Configure Audio Output

The CFG_AUDIO instruction configures an audio output tile to read a circular buffer from memory and send samples to a DAC (Digital-to-Analog Converter). Like video, audio output is memory-mapped: the audio output tile continuously reads from a specified memory region (the circular buffer) and converts the samples to analog audio signals.

**Encoding Format**

CFG_AUDIO uses opcode 0x65. The instruction header contains opcode 0x65, flags, and operand count of 6. The operands are: the circular buffer base address, the buffer size in bytes, the sample rate in Hz, the bit depth, the channel count, and the channel mapping.

The flags field encodes the audio output tile identifier (bits 8-11, up to 16 audio outputs) and the interface (bits 12-14: 000=HDMI audio, 001=DisplayPort audio, 010=analog line out, 011=SPDIF, 100=I2S). Bit 15 enables hardware-accelerated mixing.

The channel mapping operand is a pointer to an array of 32 bytes (for up to 32 channels). Each byte specifies which physical speaker the corresponding channel should be routed to.

**Operation Details**

When CFG_AUDIO executes, the following steps occur. The instruction must be executed by a System core at privilege level 0. The circular buffer is validated and configured in the audio output tile. The tile begins reading samples from the buffer at the specified sample rate.

The audio output tile manages the circular buffer automatically. It maintains a read pointer that advances as samples are consumed. When the read pointer reaches the end of the buffer, it wraps to the beginning. The tile generates an interrupt when the buffer is half-empty, allowing software to refill it without underflow.

**Assembly Examples**

Example 1: Configure stereo audio at 48 kHz
```assembly
; Configure audio output 0 as stereo, 48 kHz, 16-bit
CFG_AUDIO #0, audio_buffer, #65536, #48000, #16, #2, channel_map
```

This configures a 64KB circular buffer (65536 bytes) for 48 kHz stereo audio with 16-bit samples. The channel map routes left channel to left speaker, right channel to right speaker.

Example 2: Configure 5.1 surround sound
```assembly
; 5.1 surround (6 channels) at 96 kHz
CFG_AUDIO #0, audio_buffer, #131072, #96000, #24, #6, surround_map
```

The channel map for 5.1 audio routes channels 0-5 to front left, front right, center, subwoofer, surround left, surround right.

Example 3: Configure HDMI audio output
```assembly
; HDMI audio embedded in video signal
CFG_AUDIO.HDMI #0, audio_buffer, #65536, #48000, #16, #2, channel_map
```

The .HDMI suffix configures audio to be embedded into the HDMI signal from video output 0.

Example 4: Configure multiple audio streams
```assembly
; Two independent audio outputs
CFG_AUDIO #0, game_audio, #32768, #48000, #16, #2, map1
CFG_AUDIO #1, music_audio, #32768, #48000, #16, #2, map2
```

This configures two separate audio outputs, allowing different audio streams to play through different physical outputs (e.g., headphones and speakers).

Example 5: Configure with hardware mixing
```assembly
; Enable hardware mixing for audio output 0
CFG_AUDIO.MIX #0, master_buffer, #65536, #48000, #16, #2, map
```

The .MIX suffix enables hardware-accelerated mixing. Multiple sources can write to different regions of the buffer, and the audio tile mixes them automatically.

Example 6: Change sample rate at runtime
```assembly
; Change from 48 kHz to 96 kHz
CFG_AUDIO #0, new_buffer, #131072, #96000, #16, #2, map
```

The audio configuration can be changed at runtime. The change takes effect after the current buffer is exhausted.

Example 7: Remote audio output
```assembly
; Audio output on blade 4, buffer on blade 1
CFG_AUDIO.REMOTE @4:0, audio_buffer, #65536, #48000, #16, #2, map
```

The audio output is physically on blade 4, but the audio data is streamed from blade 1 across the optical fabric.

Example 8: Configure audio input (microphone)
```assembly
; Configure audio input from microphone
CFG_AUDIO.IN #0, mic_buffer, #65536, #48000, #16, #1, mic_map
```

The .IN suffix configures audio input instead of output. The audio tile reads from the ADC and writes samples to the circular buffer.

Example 9: Configure for low-latency audio (gaming)
```assembly
; Small buffer for low latency (4096 bytes = 10.6 ms at 48 kHz)
CFG_AUDIO #0, small_buffer, #4096, #48000, #16, #2, map
```

A smaller buffer reduces latency at the cost of requiring more frequent refills. This is used for gaming and real-time audio processing.

Example 10: Disable audio output
```assembly
; Turn off audio output 0
CFG_AUDIO.OFF #0
```

The .OFF suffix disables the specified audio output, stopping the sample playback and powering down the audio interface.

---

### 8.7 RING_INIT – Initialize Circular Buffer

The RING_INIT instruction initializes a hardware-managed circular buffer. Circular buffers (also known as ring buffers) are used for streaming data between producers and consumers, such as audio samples being written by software and consumed by the audio output tile, or network packets being written by the network interface and read by software.

**Encoding Format**

RING_INIT uses opcode 0x66. The instruction header contains opcode 0x66, flags, and operand count of 4. The operands are: the buffer base address, the segment size in bytes, the number of segments, and a pointer to the ring control structure.

The flags field has bit 8 to enable hardware write pointer caching, bit 9 to enable interrupt on half-empty, bit 10 to enable interrupt on full, and bits 11-15 reserved.

The ring control structure is a 32-byte memory region that the hardware uses to maintain the read pointer, write pointer, and status flags. Software can read these pointers to determine how much data is available.

**Operation Details**

When RING_INIT executes, the following steps occur. The instruction validates the buffer address range and the segment sizes. The ring control structure is initialized with the buffer base address, segment size, and segment count. The read and write pointers are set to zero.

The hardware begins managing the buffer. When a producer writes data using RING_WRITE, the write pointer advances. When a consumer reads data, the read pointer advances (for output rings, the audio/video tile advances the read pointer; for input rings, software advances the read pointer).

If interrupts are enabled, the hardware generates an interrupt when the buffer is half-empty (meaning the consumer needs more data) or half-full (meaning the producer needs to consume data).

**Assembly Examples**

Example 1: Initialize audio output ring buffer
```assembly
; 64KB buffer divided into 16 segments of 4KB each
RING_INIT audio_buffer, #4096, #16, ring_ctrl
```

This initializes a circular buffer for audio output. The buffer is 64KB total, split into 16 segments of 4KB each.

Example 2: Initialize network receive ring
```assembly
; Network receive ring: 32 segments of 2KB each
RING_INIT net_rx_buffer, #2048, #32, net_rx_ctrl
```

This initializes a circular buffer for network packet reception. Each segment can hold one maximum-sized Ethernet packet.

Example 3: Initialize with interrupts enabled
```assembly
; Enable half-empty interrupt for audio playback
RING_INIT.INT audio_buffer, #4096, #16, ring_ctrl
```

The .INT suffix enables interrupts. When the ring is half-empty, the audio tile generates an interrupt to request more data.

Example 4: Query ring status
```assembly
; Read ring control structure to check available data
LD.W space_available, [ring_ctrl + #8]   ; Read available space
LD.W data_available, [ring_ctrl + #12]   ; Read available data
```

Software can read the ring control structure to determine how much data is available or how much space is free.

Example 5: Reset ring buffer
```assembly
; Reinitialize ring buffer (clear all pointers)
RING_INIT audio_buffer, #4096, #16, ring_ctrl
```

Reinitializing a ring buffer resets all pointers to zero, discarding any pending data.

Example 6: Remote ring buffer (shared between blades)
```assembly
; Ring buffer accessible from multiple blades
RING_INIT.REMOTE shared_buffer, #4096, #16, @4:ring_ctrl
```

The .REMOTE suffix places the ring control structure on a remote blade, allowing multiple blades to share a single ring buffer.

Example 7: Large ring for video streaming
```assembly
; Video ring buffer: 128 segments of 1MB each (128MB total)
RING_INIT video_buffer, #1048576, #128, video_ctrl
```

Large ring buffers reduce the frequency of interrupts at the cost of more memory. This is used for video streaming.

Example 8: Double ring for full duplex
```assembly
; Two rings: one for transmit, one for receive
RING_INIT tx_buffer, #2048, #32, tx_ctrl
RING_INIT rx_buffer, #2048, #32, rx_ctrl
```

Full-duplex communication requires separate rings for transmitting and receiving data.

Example 9: Ring with custom segment boundaries
```assembly
; Variable segment sizes not directly supported
; Use fixed segment size that matches average message size
RING_INIT message_buffer, #256, #128, msg_ctrl
```

Segment sizes are fixed. Choose a segment size that matches the average message size for best efficiency.

Example 10: Ring for DMA engine
```assembly
; DMA engine uses ring buffer for scatter-gather lists
RING_INIT dma_sg_list, #32, #256, dma_ctrl
```

The DMA engine uses a ring buffer of scatter-gather list entries. Each entry describes a data transfer.

---

### 8.8 RING_WRITE – Write to Ring Buffer

The RING_WRITE instruction writes data to a hardware-managed circular buffer. It automatically advances the write pointer and handles segment boundaries. If the buffer is full, the instruction can either stall until space is available or return an error, depending on the flags.

**Encoding Format**

RING_WRITE uses opcode 0x67. The instruction header contains opcode 0x67, flags, and operand count of 3. The operands are: the ring buffer identifier (or control structure address), the source data address, and the data length in bytes.

The flags field has bit 8 for non-blocking mode (return error if buffer full), bit 9 for scatter-gather (source is a list of buffers), and bits 10-15 reserved.

**Operation Details**

When RING_WRITE executes, the following steps occur. The ring control structure is read to determine the current write pointer and available space. If there is insufficient contiguous space for the data, and the buffer wraps, the instruction may need to split the write into two parts.

The data is copied from the source address to the buffer at the write pointer. The write pointer is advanced by the data length. If the pointer reaches the end of the buffer, it wraps to the beginning.

If the buffer is full and non-blocking mode is enabled, the instruction sets the error flag and returns without writing any data. If blocking mode is enabled (default), the instruction stalls until space becomes available.

**Assembly Examples**

Example 1: Write to audio ring buffer
```assembly
; Write 1024 bytes of audio samples to ring buffer 0
RING_WRITE #0, audio_samples, #1024
```

This writes audio samples to the ring buffer configured for audio output 0.

Example 2: Non-blocking write
```assembly
; Try to write, but don't stall if full
RING_WRITE.NB #0, audio_samples, #1024
BRANCH CS, buffer_full   ; Check carry flag for full condition
```

The .NB suffix selects non-blocking mode. If the buffer is full, the carry flag is set and the instruction returns immediately.

Example 3: Scatter-gather write
```assembly
; Write from multiple buffers (list of {addr, len} pairs)
RING_WRITE.SG #0, sg_list, #3   ; Write 3 buffers from list
```

The .SG suffix enables scatter-gather mode. The source address points to a list of (address, length) pairs.

Example 4: Write to remote ring buffer
```assembly
; Write to ring buffer on blade 4
RING_WRITE.REMOTE @4:0, local_data, #512
```

The .REMOTE suffix writes to a ring buffer whose control structure is on a remote blade.

Example 5: Write network packet to transmit ring
```assembly
; Send 1500-byte Ethernet packet
RING_WRITE #1, packet_buffer, #1500
```

The network interface consumes packets from the transmit ring buffer.

Example 6: Check available space before writing
```assembly
; Check ring control structure for available space
LD.W free_space, [ring_ctrl + #8]
CMP free_space, #1024
BRANCH LT, wait
RING_WRITE #0, data, #1024
```

Software can check the ring control structure to determine available space before attempting a write.

Example 7: Partial write when buffer is fragmented
```assembly
; Write large block that may wrap
RING_WRITE #0, large_data, #16384   ; Hardware handles wrapping
```

The hardware automatically handles wrapping when the write crosses a segment boundary or reaches the end of the buffer.

Example 8: Write with completion notification
```assembly
; Write and request completion interrupt
RING_WRITE.CMP #0, data, #1024
```

The .CMP suffix requests a completion interrupt after the write is fully processed by the consumer.

Example 9: Write to multiple rings (stream duplication)
```assembly
; Write same data to two rings
RING_WRITE #0, data, #1024
RING_WRITE #1, data, #1024
```

This writes the same data to two different ring buffers, duplicating the stream.

Example 10: Write with timeout
```assembly
; Try to write with 1000 cycle timeout
MOV R5, #1000
RING_WRITE.TO #0, data, #1024, R5
BRANCH CS, timeout   ; Timeout occurred
```

The .TO suffix enables timeout mode. If the buffer remains full for the specified number of cycles, the instruction returns with an error.

---

### 8.9 RING_SWAP – Swap Ring Buffer Pointers

The RING_SWAP instruction atomically swaps the read and write pointers of a ring buffer. This implements double-buffering: the producer writes to one buffer while the consumer reads from the other. When both are done, a single RING_SWAP instruction exchanges the roles of the two buffers, making the newly written buffer available for consumption and the consumed buffer available for writing.

**Encoding Format**

RING_SWAP uses opcode 0x68. The instruction header contains opcode 0x68, flags, and operand count of 1. The operand is the ring buffer identifier (or control structure address).

The flags field has bit 8 to wait for the consumer to finish before swapping (blocking swap), bit 9 for conditional swap (only swap if consumer is done), and bits 10-15 reserved.

**Operation Details**

When RING_SWAP executes, the following steps occur atomically. The read and write pointers are exchanged. The buffer that was being written becomes available for reading, and the buffer that was being read becomes available for writing. The "active" flag is toggled.

If blocking mode is enabled, the instruction stalls until the consumer has finished reading the current buffer before swapping. If conditional mode is enabled, the instruction checks whether the consumer is done and only swaps if it is; otherwise, it returns with an error flag.

**Assembly Examples**

Example 1: Double-buffered audio
```assembly
; Write to buffer A
RING_WRITE #0, audio_samples, #4096
; Swap buffers: A becomes readable, B becomes writable
RING_SWAP #0
; Write next block to buffer B while audio plays from A
RING_WRITE #0, audio_samples2, #4096
```

This implements double-buffered audio playback. The application writes to one buffer, swaps, then writes to the other buffer while the hardware plays from the first.

Example 2: Blocking swap for synchronization
```assembly
; Swap only when consumer is ready (blocking)
RING_SWAP.BLOCK #0
```

The .BLOCK suffix causes the instruction to stall until the consumer has finished reading the current buffer. This ensures that the producer never overwrites data that is still being consumed.

Example 3: Conditional swap (non-blocking)
```assembly
; Swap only if consumer is done
RING_SWAP.COND #0
BRANCH CS, consumer_busy   ; Swap not performed
```

The .COND suffix attempts the swap but does not stall. If the consumer is still busy, the carry flag is set and the swap does not occur.

Example 4: Video page flip
```assembly
; Prepare next frame in inactive buffer
RENDER next_frame
; Flip to show the new frame
RING_SWAP #0   ; Video output now shows next_frame
```

Video page flipping uses RING_SWAP to change the active framebuffer instantly at vertical blanking.

Example 5: Triple buffering
```assembly
; Three buffers: A (writing), B (displaying), C (ready)
; After writing A, swap to B, then write to C
RING_SWAP #0
RING_WRITE #0, new_data, #4096
```

Triple buffering uses multiple swaps to keep the display always fed while allowing the renderer to get ahead.

Example 6: Remote ring swap
```assembly
; Swap ring buffer on remote blade
RING_SWAP.REMOTE @4:0
```

The .REMOTE suffix swaps a ring buffer whose control structure is on a remote blade.

Example 7: Swap with consumer notification
```assembly
; Swap and notify consumer (generate interrupt)
RING_SWAP.INT #0
```

The .INT suffix generates an interrupt after the swap, notifying the consumer that new data is available.

Example 8: Polling for consumer completion
```assembly
; Wait for consumer to finish without blocking
wait:
RING_SWAP.COND #0
BRANCH CS, wait   ; Retry until swap succeeds
```

This loop polls the ring until the consumer finishes, then performs the swap. This is used when blocking is not acceptable.

Example 9: Producer-consumer handshake
```assembly
; Producer: write data, then swap
RING_WRITE #0, data, #1024
RING_SWAP #0
; Consumer: process data, then swap back
RING_SWAP #0
; After swap, buffer is ready for next write
```

This implements a handshake protocol between producer and consumer. Each swap signals that one side has completed its work.

Example 10: Multi-buffer streaming
```assembly
; Process 4 buffers in sequence
MOV R10, #4
loop:
RING_WRITE #0, [R1], #4096
RING_SWAP #0
ADD R1, #4096
SUB R10, #1
BRANCH GT, loop
```

This writes a sequence of buffers, swapping after each write to make them available to the consumer.

---

This concludes Chapter 8 of the Instruction Set Reference. The remaining chapters will cover Interconnect Instructions, Memory Management Instructions, and Protection Instructions.

# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 9: Interconnect Instructions

### 9.1 MAP_STORAGE – Map NAND Flash to Memory Address Space

The MAP_STORAGE instruction assigns a range of physical memory addresses to NAND flash storage. After mapping, load instructions to those addresses read directly from flash, and store instructions write directly to flash (subject to flash write endurance limitations). This eliminates the traditional storage stack entirely: there are no file systems, no block I/O drivers, no system call overhead. Storage becomes just another memory region.

**Encoding Format**

MAP_STORAGE uses opcode 0x70. The instruction header contains opcode 0x70, flags, and operand count of 4. The operands are: the flash chip identifier, the starting flash block address, the target memory base address, and the size in bytes.

The flags field encodes the flash interface type (bits 8-9: 00=ONFi, 01=Toggle, 10=NV-DDR3, 11=Raw NAND), the ECC strength (bits 10-12: 0=no ECC, 1=4-bit, 2=8-bit, 3=12-bit, 4=16-bit, 5=24-bit, 6=32-bit, 7=64-bit), and bit 13 for write-through caching (writes go directly to flash without cache). Bits 14-15 are reserved.

The flash chip identifier selects one of up to 128 flash chips on the motherboard. The starting block address is the block number within that chip (not a byte address). The target memory base address must be aligned to the flash page size (typically 16KB). The size must be a multiple of the flash page size.

**Operation Details**

When MAP_STORAGE executes, the following steps occur. The instruction must be executed by a System core at privilege level 0. The specified flash chip is verified to be present and functional. The address translation table in the memory controller is updated to map the target address range to the specified flash blocks.

After mapping, a load from the target address triggers the following hardware sequence. The memory controller calculates which flash chip, block, page, and offset are needed. It sends a read command to the flash chip. The flash chip reads the entire page (typically 16KB) into its internal buffer. The memory controller transfers the requested portion from the flash buffer to the requesting core. The entire operation takes approximately 50 microseconds, during which the core stalls.

Write operations are similar but also require erasing blocks before writing. The hardware manages the erase-before-write requirement automatically, but writes are much slower than reads (approximately 500 microseconds). For this reason, write-back caching using DRAM is strongly recommended.

**Assembly Examples**

Example 1: Map a 1GB flash partition to memory
```assembly
; Map flash chip 0, blocks 0-2047 (assuming 512KB blocks = 1GB)
; to memory address 0x100000000
MAP_STORAGE #0, #0, #0x100000000, #0x40000000
```

This maps the first 1GB of flash chip 0 to memory address 0x100000000. After this instruction, reading from address 0x100000000 reads from flash.

Example 2: Map with ECC enabled
```assembly
; Map with 8-bit ECC correction
MAP_STORAGE.ECC8 #0, #0, #0x100000000, #0x40000000
```

The .ECC8 suffix enables 8-bit error correction. The hardware automatically detects and corrects bit errors in flash reads.

Example 3: Map multiple chips (striping)
```assembly
; Map chips 0-3 as a striped array (RAID 0 style)
MAP_STORAGE #0, #0, #0x100000000, #0x10000000
MAP_STORAGE #1, #0, #0x110000000, #0x10000000
MAP_STORAGE #2, #0, #0x120000000, #0x10000000
MAP_STORAGE #3, #0, #0x130000000, #0x10000000
```

This maps four flash chips to contiguous memory addresses, effectively striping data across chips for increased bandwidth.

Example 4: Write-through caching for critical data
```assembly
; Map with write-through (bypass cache)
MAP_STORAGE.WT #0, #0, #0x100000000, #0x40000000
```

The .WT suffix enables write-through mode. Writes go directly to flash and do not dirty cache lines. This is used for critical data that must be persistent immediately.

Example 5: Remap a region (unmap first)
```assembly
; Unmap previous mapping (by setting size to 0)
MAP_STORAGE #0, #0, #0x100000000, #0
; Map new region
MAP_STORAGE #0, #2048, #0x100000000, #0x20000000
```

To change a mapping, first unmap the old region by setting the size to 0. Then map the new region.

Example 6: Remote storage mapping
```assembly
; Map flash on blade 4 to local memory address space
MAP_STORAGE.REMOTE @4:0, #0, #0x100000000, #0x40000000
```

The .REMOTE suffix maps flash on a remote blade. Loads to the mapped address trigger remote flash reads across the optical fabric.

Example 7: Map with different ECC strength
```assembly
; Map with 24-bit ECC for high-reliability storage
MAP_STORAGE.ECC24 #0, #0, #0x100000000, #0x40000000
```

Higher ECC strength provides better protection against bit errors but reduces usable capacity and increases latency.

Example 8: Query mapping status
```assembly
; Check if address is mapped to flash
SEGMENT_LOOKUP R1, #0x100000000
TEST R1, #SEGMENT_FLASH
BRANCH NE, is_flash
```

The SEGMENT_LOOKUP instruction can be used to determine whether a memory address is mapped to flash.

Example 9: Map for read-only boot partition
```assembly
; Map boot partition as read-only
MAP_STORAGE.RO #0, #0, #0x100000000, #0x10000000
```

The .RO suffix maps the region as read-only. Store instructions to this address range raise protection faults.

Example 10: Map with transparent compression
```assembly
; Map with hardware decompression (LZ4)
MAP_STORAGE.COMP #0, #0, #0x100000000, #0x40000000
```

The .COMP suffix enables hardware decompression. Data is stored compressed on flash and decompressed on read, trading CPU cycles for storage capacity.

---

### 9.2 EXPORT_MEMORY – Export Local Memory to Remote Blades

The EXPORT_MEMORY instruction makes a range of local memory accessible to other blades on the optical fabric. After export, remote blades can load from and store to the exported region using standard memory access instructions, with hardware maintaining cache coherence across blades. This enables distributed shared memory programming models where all blades share a single address space.

**Encoding Format**

EXPORT_MEMORY uses opcode 0x71. The instruction header contains opcode 0x71, flags, and operand count of 5. The operands are: the local base address, the size in bytes, the remote blade identifier (or broadcast for all blades), the remote base address (where the region appears in the remote address space), and the access permissions.

The flags field encodes the coherence mode (bits 8-9: 00=hardware coherent, 01=release consistency, 10=relaxed consistency, 11=uncached), the access type (bits 10-11: 00=read-write, 01=read-only, 10=write-only, 11=execute-only), and bit 12 for persistent export (survives reset). Bits 13-15 are reserved.

The access permissions operand is a 32-bit value. Bit 0 grants read permission, bit 1 grants write permission, bit 2 grants execute permission, bits 3-31 are reserved.

**Operation Details**

When EXPORT_MEMORY executes, the following steps occur. The instruction must be executed by a System core at privilege level 0. The local memory region is registered with the directory cache on the local blade and on the remote blade(s). The directory cache tracks which blades have cached copies of each cache line.

When a remote blade loads from the exported address, the following occurs. The remote blade's memory controller checks its directory cache. If the line is not present, it sends a request across the optical fabric to the home blade. The home blade returns the data. The remote blade caches the data and marks it as shared.

When a remote blade stores to the exported address, the directory protocol invalidates copies on all other blades before allowing the write to proceed. This ensures coherence but adds latency to writes.

**Assembly Examples**

Example 1: Export memory to a single remote blade
```assembly
; Export 1GB of local memory at 0x20000000 to blade 4
; Appears at address 0x30000000 on blade 4
EXPORT_MEMORY #0x20000000, #0x40000000, #4, #0x30000000, #0x03
```

The permission 0x03 grants read and write access. Blade 4 can now access this memory as if it were local.

Example 2: Export memory as read-only to all blades
```assembly
; Export read-only configuration data to all blades
EXPORT_MEMORY.RO #config_data, #4096, #0xFFFF, #0x100000, #0x01
```

The .RO suffix and permission 0x01 grant read-only access. The remote blade identifier 0xFFFF is the broadcast address, meaning all blades can access this region.

Example 3: Export with relaxed consistency
```assembly
; Export with relaxed memory consistency (higher performance)
EXPORT_MEMORY.RELAXED #0x20000000, #0x40000000, #4, #0x30000000, #0x03
```

The .RELAXED suffix selects relaxed consistency. The hardware does not enforce ordering between accesses to different addresses, which improves performance at the cost of programmer-visible reordering.

Example 4: Export uncached memory for I/O
```assembly
; Export uncached (each access goes directly to home blade)
EXPORT_MEMORY.UNCACHED #io_buffer, #4096, #4, #0x400000, #0x03
```

The .UNCACHED suffix disables caching. Every access goes across the optical fabric to the home blade. This is used for I/O buffers where coherence is not needed.

Example 5: Query export status
```assembly
; Check if memory is exported
SEGMENT_LOOKUP R1, #0x20000000
TEST R1, #SEGMENT_EXPORTED
BRANCH NE, is_exported
```

The SEGMENT_LOOKUP instruction returns segment information including whether the region is exported.

Example 6: Unexport memory
```assembly
; Unexport (stop sharing) by setting size to 0
EXPORT_MEMORY #0x20000000, #0, #4, #0, #0
```

Setting the size to 0 unexports the region. Remote blades can no longer access it.

Example 7: Export with execute permission (code sharing)
```assembly
; Export code section as execute-only
EXPORT_MEMORY.XO #code_start, #code_size, #0xFFFF, #0x500000, #0x04
```

The .XO suffix and permission 0x04 grant execute permission only. Remote blades can jump to code in this region but cannot read or write it.

Example 8: Persistent export across reset
```assembly
; Export that survives system reset (stored in non-volatile config)
EXPORT_MEMORY.PERSIST #0x20000000, #0x40000000, #4, #0x30000000, #0x03
```

The .PERSIST suffix stores the export configuration in non-volatile memory. The export is restored automatically after reset.

Example 9: Export with bandwidth reservation
```assembly
; Reserve 10 GB/s of fabric bandwidth for this export
EXPORT_MEMORY.BW #0x20000000, #0x40000000, #4, #0x30000000, #0x03, #10000000000
```

The .BW suffix includes a bandwidth reservation parameter. The fabric guarantees the specified bandwidth to this export.

Example 10: Export atomic region for locks
```assembly
; Export small region with hardware atomic support
EXPORT_MEMORY.ATOMIC #lock_var, #8, #0xFFFF, #0x600000, #0x03
```

The .ATOMIC suffix enables hardware support for atomic operations (XCHG, ADD.ATOMIC) on the exported region across blades.

---

### 9.3 REMOTE_CALL – Execute Function on Remote Blade

The REMOTE_CALL instruction executes a function on a remote blade and returns the result. This is the hardware equivalent of a remote procedure call (RPC), but with dramatically lower overhead because the hardware handles argument passing, context switching, and result return without software intervention. REMOTE_CALL enables distributed computing where computation moves to the data rather than data moving to computation.

**Encoding Format**

REMOTE_CALL uses opcode 0x72. The instruction header contains opcode 0x72, flags, and operand count of 5. The operands are: the target blade identifier, the target function address, the argument count, the argument list address, and the result return address.

The flags field encodes the execution mode (bits 8-9: 00=synchronous wait, 01=asynchronous with interrupt, 10=asynchronous with polling, 11=fire-and-forget), the core type (bits 10-11: 00=Math core, 01=Logic core, 10=System core, 11=any core), and bit 12 for trusted execution (bypass permission checks). Bits 13-15 are reserved.

The argument list is a contiguous array of 64-bit values (registers) to be passed to the remote function. The argument count must match the function's expected argument count.

**Operation Details**

When REMOTE_CALL executes, the following steps occur. The local blade sends a request packet across the optical fabric to the target blade. The request contains the function address, the arguments, and the return address.

The target blade receives the request and schedules the function for execution on the specified core type. The function executes in a privileged context that has access to the caller's memory region (if appropriate permissions are set).

When the function completes, it executes a special REMOTE_RETURN instruction (which is a variant of SYSEXIT). The target blade sends a response packet back to the caller containing the return value.

For synchronous calls, the calling core stalls until the response arrives. For asynchronous calls, the instruction returns immediately, and the result is delivered via interrupt or can be polled.

**Assembly Examples**

Example 1: Synchronous remote call
```assembly
; Call function at address 0x1000 on blade 4
; Pass two arguments from R1 and R2
; Result returned in R1
REMOTE_CALL #4, #0x1000, #2, arg_list, result_addr
```

The arguments are stored in a list at arg_list. The result is stored at result_addr, and also returned in R1.

Example 2: Asynchronous remote call with interrupt
```assembly
; Call remotely, continue execution, get interrupt when done
REMOTE_CALL.ASYNC #4, #0x1000, #2, arg_list, result_addr
; Continue with local work
; Interrupt handler will process result
```

The .ASYNC suffix selects asynchronous mode. The instruction returns immediately. When the remote function completes, an interrupt is generated.

Example 3: Fire-and-forget remote call
```assembly
; Start remote computation, don't wait for result
REMOTE_CALL.FF #4, #0x1000, #2, arg_list, #0
```

The .FF suffix (fire-and-forget) sends the request but does not expect a response. The result address is ignored. This is used for operations that do not need confirmation.

Example 4: Remote call on specific core type
```assembly
; Execute on a Logic core (good for branching)
REMOTE_CALL.LOGIC #4, #0x1000, #2, arg_list, result_addr
```

The .LOGIC suffix specifies that the function should run on a Logic core rather than any available core.

Example 5: Trusted remote call (bypass permissions)
```assembly
; Call with full privileges (system use only)
REMOTE_CALL.TRUSTED #4, #0x1000, #2, arg_list, result_addr
```

The .TRUSTED suffix bypasses permission checks. This instruction can only be executed from privilege level 0.

Example 6: Remote call with large arguments
```assembly
; Pass 8 arguments via list
arg_list:
DQ arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8
REMOTE_CALL #4, #0x1000, #8, arg_list, result_addr
```

The argument list can contain up to 16 arguments (limited by packet size). For more arguments, use a memory buffer and pass a pointer.

Example 7: Remote call to distributed matrix multiply
```assembly
; Each blade multiplies its portion of the matrix
MOV R10, #0
loop:
REMOTE_CALL.ASYNC R10, multiply_task, #3, task_args, result_addr
ADD R10, #1
CMP R10, #64
BRANCH LT, loop
; Wait for all to complete
BARRIER_SYNC
```

This dispatches 64 remote tasks to 64 blades, each computing a portion of a matrix multiplication. All tasks run in parallel.

Example 8: Remote call result polling
```assembly
; Start asynchronous remote call
REMOTE_CALL.ASYNC #4, #0x1000, #2, arg_list, result_addr
; Poll for completion
poll:
REMOTE_CALL.POLL #4, result_addr   ; Check if done
BRANCH CC, not_done
; Result is ready
```

The .POLL variant checks whether a previous asynchronous remote call has completed.

Example 9: Remote call to storage blade
```assembly
; Storage blade exports flash as memory, but has compute cores too
; Execute search directly on storage blade
REMOTE_CALL #4, search_function, #2, query_args, result_addr
```

This moves the computation to the storage blade, avoiding data transfer across the fabric. The search executes where the data lives.

Example 10: Remote call with timeout
```assembly
; Wait at most 1 million cycles for remote call to complete
REMOTE_CALL.TIMEOUT #4, #0x1000, #2, arg_list, result_addr, #1000000
BRANCH CS, timeout  ; Handle timeout
```

The .TIMEOUT suffix includes a timeout parameter. If the remote call does not complete within the specified cycles, the instruction returns with the carry flag set.

---

### 9.4 LINK_STATUS – Query Optical Link Health

The LINK_STATUS instruction returns status information about an optical link between blades. The optical fabric is critical for system operation, and monitoring link health is essential for detecting failures, balancing load, and planning maintenance. This instruction returns metrics including signal strength, error rates, and current bandwidth utilization.

**Encoding Format**

LINK_STATUS uses opcode 0x73. The instruction header contains opcode 0x73, flags, and operand count of 2. The operands are: the link identifier (destination blade number) and a pointer to a status structure.

The flags field encodes the statistics to return (bits 8-9: 00=basic status only, 01=include error counters, 10=include bandwidth history, 11=include all), and bits 10-15 reserved.

The status structure is a 64-byte memory region that receives the link information. The structure format is defined by the system firmware.

**Operation Details**

When LINK_STATUS executes, the following steps occur. The instruction queries the optical transceiver for the specified link. The transceiver reports status including: link up/down, signal strength in dBm, bit error rate (BER), packets sent, packets received, bytes transferred, CRC errors, alignment errors, and current bandwidth utilization.

The information is written to the status structure. The instruction completes in approximately 1 microsecond, most of which is waiting for the transceiver to report statistics.

**Assembly Examples**

Example 1: Query basic link status
```assembly
; Check if link to blade 4 is up
LINK_STATUS #4, status_buffer
LD.B R1, [status_buffer]   ; Status byte: 0=down, 1=up
```

The basic status byte indicates whether the link is operational.

Example 2: Query signal strength
```assembly
; Read signal strength in dBm
LINK_STATUS #4, status_buffer
LD.W R1, [status_buffer + #8]   ; Signal strength (fixed-point dBm)
```

Signal strength below -15 dBm indicates a failing cable or transceiver.

Example 3: Query bit error rate
```assembly
; Read bit error rate (BER)
LINK_STATUS #4, status_buffer
LD.D R1, [status_buffer + #16]   ; BER as floating-point
CMP R1, #1e-12
BRANCH GT, poor_quality   ; BER > 1e-12 is concerning
```

A high bit error rate indicates that the link is marginal and may fail soon.

Example 4: Query bandwidth utilization
```assembly
; Read current bandwidth usage (bytes per second)
LINK_STATUS #4, status_buffer
LD.D R1, [status_buffer + #32]   ; Bandwidth in MB/s
```

Bandwidth utilization can be used for load balancing decisions.

Example 5: Query error counters
```assembly
; Read CRC error count
LINK_STATUS.ERR #4, status_buffer
LD.D R1, [status_buffer + #40]   ; CRC error count
CMP R1, #1000
BRANCH GT, too_many_errors
```

The .ERR suffix includes error counters. A high error count indicates hardware problems.

Example 6: Periodic link monitoring
```assembly
; Monitor link health every second
loop:
LINK_STATUS #4, status_buffer
; Log status
CALL log_link_status
; Wait 1 second
MOV R1, #2000000000   ; 2 billion cycles at 2 GHz
WAIT R1
JMP loop
```

This loop continuously monitors link health for predictive failure detection.

Example 7: Remote link status (from another blade)
```assembly
; Query link status from blade 4's perspective
LINK_STATUS.REMOTE @4:0, #5, status_buffer
```

The .REMOTE suffix queries the status of blade 4's link to blade 5, as reported by blade 4.

Example 8: Link auto-negotiation status
```assembly
; Read negotiated link speed
LINK_STATUS #4, status_buffer
LD.B R1, [status_buffer + #1]   ; Speed code: 1=10G, 2=40G, 3=100G, 4=200G, 5=400G, 6=800G
```

This returns the speed that was automatically negotiated between the blades.

Example 9: Query link partner information
```assembly
; Read partner blade identifier
LINK_STATUS #4, status_buffer
LD.W R1, [status_buffer + #4]   ; Partner blade ID (should be 4)
```

This confirms that the link is connected to the expected blade.

Example 10: Clear error counters
```assembly
; Reset error counters after reading
LINK_STATUS.CLEAR #4, status_buffer
```

The .CLEAR suffix resets the error counters after reading them.

---

### 9.5 RACK_UNIFY – Unify Rack Memory

The RACK_UNIFY instruction configures the entire rack as a single shared memory space. After this instruction executes, every blade in the rack can access every memory location on every other blade using standard load and store instructions. The hardware directory cache maintains coherence across all blades. This transforms the rack from a cluster of independent computers into a single large shared-memory machine.

**Encoding Format**

RACK_UNIFY uses opcode 0x74. The instruction header contains opcode 0x74, flags, and operand count of 4. The operands are: the blade range (starting blade and ending blade), the global base address, and the interleaving granularity.

The flags field encodes the interleaving mode (bits 8-9: 00=round-robin, 01=stripe, 10=first-touch, 11=manual), the coherence protocol (bits 10-11: 00=directory, 01=broadcast, 10=hybrid, 11=release), and bit 12 for persistent configuration (survives reset). Bits 13-15 are reserved.

The interleaving granularity specifies how memory addresses are distributed across blades. A granularity of 64 bytes means that consecutive 64-byte blocks are assigned to consecutive blades in round-robin fashion.

**Operation Details**

When RACK_UNIFY executes, the following steps occur. The instruction must be executed by the rack management controller or a blade with special privileges. The instruction contacts all blades in the specified range to negotiate the unified address space.

Each blade reports its local memory capacity. The global address space is constructed by concatenating or interleaving the local memory regions according to the specified mode. The directory caches on all blades are configured to track the location of each memory page.

After unification, any blade can access any address. The hardware uses the directory cache to route requests to the blade that actually holds the data. If the directory cache misses, the hardware performs a directory lookup by broadcasting or consulting a global directory table.

**Assembly Examples**

Example 1: Unify all blades with round-robin interleaving
```assembly
; Unify blades 0-63 into single address space starting at 0
; 64-byte interleaving
RACK_UNIFY #0, #63, #0x00000000, #64
```

After this, memory addresses are interleaved across all 64 blades. Address 0 is on blade 0, address 64 on blade 1, address 128 on blade 2, etc.

Example 2: Concatenate memory (no interleaving)
```assembly
; Place blade 0 memory at 0, blade 1 at 1GB, etc.
RACK_UNIFY.STRIPE #0, #63, #0x00000000, #0
```

The .STRIPE suffix with zero granularity concatenates memory regions. Blade 0's memory occupies the lowest addresses, blade 1's the next, etc.

Example 3: First-touch allocation
```assembly
; Memory allocated on the blade that first writes to it
RACK_UNIFY.FT #0, #63, #0x00000000, #4096
```

The .FT suffix (first-touch) allocates physical memory on the blade that first writes to each page. This improves locality.

Example 4: Persistent unification across reset
```assembly
; Unify and persist configuration in non-volatile memory
RACK_UNIFY.PERSIST #0, #63, #0x00000000, #64
```

The .PERSIST suffix stores the configuration so that the rack remains unified after reset.

Example 5: Partial unification (subset of blades)
```assembly
; Unify only blades 16-31 for a specific application
RACK_UNIFY #16, #31, #0x100000000, #4096
```

This creates a unified memory space for a subset of blades, leaving other blades independent.

Example 6: Query unification status
```assembly
; Check if rack is unified
RACK_UNIFY.STATUS status_buffer
LD.B R1, [status_buffer]   ; 0=not unified, 1=unified
```

The .STATUS suffix returns the current unification configuration.

Example 7: Dynamic reconfiguration (add a blade)
```assembly
; Add blade 64 to the existing unified space
RACK_UNIFY.ADD #64, #0x200000000, #64
```

The .ADD suffix adds a new blade to an already unified system. The new blade's memory is added at the specified base address.

Example 8: Remove blade from unified space
```assembly
; Remove blade 32 (for maintenance)
RACK_UNIFY.REMOVE #32
```

The .REMOVE suffix removes a blade from the unified space. Any data stored on that blade must be migrated first.

Example 9: Query blade owning an address
```assembly
; Determine which blade holds address 0x12345678
RACK_UNIFY.QUERY #0x12345678, owner_buffer
LD.W R1, [owner_buffer]   ; Blade number
```

The .QUERY suffix returns the blade that physically holds a given memory address.

Example 10: Unify with broadcast coherence (small rack)
```assembly
; For small racks (<8 blades), broadcast is more efficient
RACK_UNIFY.BROADCAST #0, #7, #0x00000000, #64
```

The .BROADCAST suffix selects broadcast coherence. This is simpler and faster for small configurations.

---

### 9.6 WARP_SYNC – Synchronize Warp of Cores

The WARP_SYNC instruction synchronizes a warp of 32 Math cores. A warp is a group of cores that execute the same instruction in lockstep. WARP_SYNC ensures that all cores in the warp have reached the synchronization point before any core proceeds. This is essential for parallel algorithms where cores must coordinate before exchanging data.

**Encoding Format**

WARP_SYNC uses opcode 0x75. The instruction header contains opcode 0x75, flags, and operand count of 1. The operand is the warp identifier (0-311, since 10,000 cores / 32 cores per warp = 312 warps).

The flags field has bit 8 for "sync all warps" (global synchronization), bit 9 for "sync with timeout", and bits 10-15 reserved.

**Operation Details**

When WARP_SYNC executes, the following steps occur. The calling core enters a waiting state. The hardware tracks which cores in the warp have reached the synchronization point. When all 32 cores in the warp have executed WARP_SYNC, all cores are released simultaneously and continue execution.

If a core never reaches the sync point (due to an exception or infinite loop), the warp can deadlock. A timeout mechanism can be enabled to break the deadlock.

**Assembly Examples**

Example 1: Basic warp synchronization
```assembly
; All cores in warp 0 must reach this point before proceeding
WARP_SYNC #0
```

This ensures that all cores in warp 0 have completed their previous work before any core continues.

Example 2: Global synchronization of all warps
```assembly
; Synchronize all cores on the blade
WARP_SYNC.ALL
```

The .ALL suffix synchronizes all cores on the blade, not just those in a single warp.

Example 3: Synchronization with timeout
```assembly
; Wait at most 1000 cycles
WARP_SYNC.TIMEOUT #0, #1000
BRANCH CS, timeout_occurred
```

The .TIMEOUT suffix returns with the carry flag set if not all cores reached the sync point within the timeout period.

Example 4: Warp in parallel reduction
```assembly
; Parallel reduction: each core has a value, need to sum them
; First, each core writes its value to shared memory
ST.V value, [shared_base + core_id*4]
WARP_SYNC #0   ; Ensure all writes complete
; Core 0 sums all values
CMP core_id, #0
BRANCH NE, not_core0
; Summation code here
not_core0:
WARP_SYNC #0   ; Ensure core 0 finishes before others continue
```

This pattern uses warp synchronization to coordinate a parallel reduction.

Example 5: Barrier in SIMT execution
```assembly
; SIMT: all cores execute same instruction on different data
; Synchronize after memory access before next phase
LD.V data, [R1 + core_id*4]
WARP_SYNC #0   ; All loads complete
; Now process data
```

Warp synchronization ensures that all loads complete before the processing phase begins.

Example 6: Debugging with warp sync
```assembly
; Breakpoint synchronization
CMP R1, #0
BRANCH EQ, breakpoint
WARP_SYNC #0   ; Wait for breakpoint core
breakpoint:
; Core 0 stops here, others wait
```

This allows a single core to act as a breakpoint while others wait.

Example 7: Conditional synchronization
```assembly
; Only sync if mask bit is set
TEST core_mask, core_id
BRANCH EQ, skip_sync
WARP_SYNC #0
skip_sync:
```

This pattern allows some cores to skip synchronization.

Example 8: Nested synchronization
```assembly
; First sync for phase 1
WARP_SYNC #0
; Phase 1 work
; Second sync for phase 2
WARP_SYNC #0
```

Multiple synchronization points can be used to separate phases of computation.

Example 9: Synchronization across warps
```assembly
; Sync within warp first
WARP_SYNC #0
; Then sync across all warps
WARP_SYNC.ALL
```

A two-level synchronization ensures that all cores are ready.

Example 10: Timeout recovery
```assembly
WARP_SYNC.TIMEOUT #0, #10000
BRANCH CC, ok
; Timeout occurred - core may be hung
CALL report_hung_core
; Continue without the hung core
```

This pattern detects and recovers from hung cores.

---

### 9.7 REMOTE_ALLOC – Allocate Memory on Remote Blade

The REMOTE_ALLOC instruction allocates memory on a remote blade and returns the global address. This is the distributed equivalent of malloc, but the allocated memory resides on a different blade. Combined with REMOTE_CALL and EXPORT_MEMORY, REMOTE_ALLOC enables fully distributed data structures where each component is placed on the blade that will use it most.

**Encoding Format**

REMOTE_ALLOC uses opcode 0x76. The instruction header contains opcode 0x76, flags, and operand count of 3. The operands are: the target blade identifier, the allocation size in bytes, and the alignment requirement.

The flags field encodes the memory type (bits 8-9: 00=general purpose, 01=large page, 10=huge page, 11=contiguous), the cache policy (bits 10-11: 00=write-back, 01=write-through, 10=uncached, 11=write-combining), and bit 12 for zero-fill (initialize allocated memory to zero). Bits 13-15 are reserved.

**Operation Details**

When REMOTE_ALLOC executes, the following steps occur. The local blade sends an allocation request to the target blade. The target blade's memory allocator reserves a region of the requested size and alignment. The target blade returns the global address of the allocated region.

The allocated memory is automatically exported to the caller's address space. The caller can access the memory directly using standard load and store instructions.

**Assembly Examples**

Example 1: Allocate 1MB on blade 4
```assembly
; Allocate 1MB on blade 4, 64-byte aligned
REMOTE_ALLOC #4, #1048576, #64
; Address returned in R1
```

The allocated memory is accessible from the local blade at the address in R1.

Example 2: Allocate zero-filled memory
```assembly
; Allocate and zero-fill
REMOTE_ALLOC.ZERO #4, #1048576, #64
```

The .ZERO suffix ensures that all allocated memory is initialized to zero.

Example 3: Allocate large page (2MB)
```assembly
; Use 2MB huge pages for better TLB coverage
REMOTE_ALLOC.HUGE #4, #2097152, #2097152
```

The .HUGE suffix requests allocation using 2MB pages, reducing TLB pressure.

Example 4: Allocate contiguous physical memory
```assembly
; Allocate physically contiguous memory for DMA
REMOTE_ALLOC.CONTIG #4, #1048576, #4096
```

The .CONTIG suffix requests physically contiguous memory, required for some DMA operations.

Example 5: Allocate with specific cache policy
```assembly
; Allocate uncached memory for streaming data
REMOTE_ALLOC.UNCACHED #4, #1048576, #64
```

The .UNCACHED suffix disables caching for this region, suitable for write-once read-once streaming.

Example 6: Allocate and initialize with pattern
```assembly
; Allocate and fill with pattern
REMOTE_ALLOC #4, #1048576, #64
MOV R2, #0xDEADBEEF   ; Fill pattern
REMOTE_CALL #4, fill_function, #3, [R1, R2, #1048576], result
```

The allocation is followed by a remote call to fill the memory with a pattern.

Example 7: Allocate distributed array
```assembly
; Allocate portions of a large array on different blades
MOV R10, #0
MOV R11, #64   ; 64 blades
loop:
REMOTE_ALLOC R10, #16777216, #64   ; 16MB per blade
ST.V [array_base + R10*4], R1      ; Store base address in table
ADD R10, #1
CMP R10, R11
BRANCH LT, loop
```

This allocates a distributed array with 16MB on each of 64 blades.

Example 8: Free remote memory
```assembly
; Free previously allocated memory
REMOTE_ALLOC.FREE #4, R1   ; R1 contains address to free
```

The .FREE suffix frees memory previously allocated with REMOTE_ALLOC.

Example 9: Query allocation size
```assembly
; Get size of allocated block
REMOTE_ALLOC.SIZE #4, R1, size_buffer
```

The .SIZE suffix returns the size of an allocated block.

Example 10: Allocate with memory type hint
```assembly
; Allocate for GPU-like compute (write-combining)
REMOTE_ALLOC.WC #4, #1048576, #64
```

The .WC suffix (write-combining) optimizes for write-intensive workloads.

---

### 9.8 BROADCAST – Send Instruction to All Blades

The BROADCAST instruction sends the following instruction stream to all blades in the rack simultaneously. All blades execute the broadcasted instructions in parallel. This is used for initializing system state, distributing configuration parameters, and launching parallel computations across the entire rack.

**Encoding Format**

BROADCAST uses opcode 0x77. The instruction header contains opcode 0x77, flags, and operand count of 0. The flags field has bit 8 for "wait for completion" (stall until all blades finish), bit 9 for "exclude self" (broadcast to others only), and bits 10-15 reserved.

The instruction stream following the BROADCAST opcode is sent to all blades. The stream continues until a BROADCAST_END instruction is encountered.

**Operation Details**

When BROADCAST executes, the following steps occur. The local blade sends the following instruction stream to all blades (including itself by default). Each blade receives the stream and executes it from its own instruction pointer.

The broadcast stream can include any instructions, including REMOTE_CALL, WARP_SYNC, and even nested BROADCAST instructions. The stream is terminated by a BROADCAST_END instruction.

**Assembly Examples**

Example 1: Broadcast a NOP to all blades
```assembly
BROADCAST
NOP
BROADCAST_END
```

This sends a NOP instruction to all blades. It is useful for measuring broadcast latency.

Example 2: Broadcast initialization sequence
```assembly
BROADCAST
MOV R1, #0
MOV R2, #0
MOV R3, #0
BROADCAST_END
```

This initializes the first three registers to zero on every blade.

Example 3: Broadcast with completion wait
```assembly
BROADCAST.WAIT
; All blades execute this code
MOV R1, #42
BROADCAST_END
; Execution continues here after all blades complete
```

The .WAIT suffix causes the broadcasting blade to stall until all blades have finished executing the broadcasted stream.

Example 4: Broadcast to exclude self
```assembly
BROADCAST.OTHER
; This code runs on all blades except the broadcaster
CALL remote_function
BROADCAST_END
; Local blade continues immediately
```

The .OTHER suffix excludes the broadcasting blade, which continues execution in parallel with the broadcast.

Example 5: Broadcast a remote call
```assembly
; Make all blades call a function on blade 4
BROADCAST
REMOTE_CALL #4, sync_function, #0, #0, #0
BROADCAST_END
```

All blades simultaneously request remote execution on blade 4.

Example 6: Broadcast barrier
```assembly
; Simple barrier using broadcast
BROADCAST.WAIT
NOP
BROADCAST_END
; All blades reach this point simultaneously
```

This implements a global barrier. All blades wait for each other before proceeding.

Example 7: Broadcast configuration update
```assembly
; Update memory mapping on all blades
BROADCAST
MAP_STORAGE #0, #0, #0x100000000, #0x40000000
BROADCAST_END
```

This ensures that all blades have the same flash mapping.

Example 8: Broadcast with conditional execution
```assembly
; Only core 0 on each blade executes
BROADCAST
CMP core_id, #0
BRANCH NE, skip
CALL master_function
skip:
BROADCAST_END
```

Each blade runs the broadcasted code, but only core 0 executes the function.

Example 9: Nested broadcast (advanced)
```assembly
; First level: all blades
BROADCAST
; Second level: within each blade, all warps
WARP_SYNC.ALL
; Third level: within each warp, all cores
WARP_SYNC #0
BROADCAST_END
```

Nested broadcasts and synchronizations can create complex parallel patterns.

Example 10: Broadcast for distributed training
```assembly
; Synchronize model weights across all blades
BROADCAST.WAIT
; All blades load new weights from shared memory
LD.V ZMM1, [weights_base]
; All blades update local model
CALL update_model
BROADCAST_END
```

This broadcasts the weight update phase of distributed training.

---

### 9.9 BARRIER_SYNC – Global Barrier Synchronization

The BARRIER_SYNC instruction implements a global barrier that synchronizes all cores across all linked blades. Every core must execute BARRIER_SYNC before any core proceeds. This is the most powerful synchronization primitive in the system and is used for major phase transitions in parallel algorithms.

**Encoding Format**

BARRIER_SYNC uses opcode 0x78. The instruction header contains opcode 0x78, flags, and operand count of 0. The flags field has bit 8 for "timeout", bit 9 for "release on interrupt", and bits 10-15 reserved.

**Operation Details**

When BARRIER_SYNC executes, the following steps occur. The calling core enters a waiting state. The hardware tracks how many cores have reached the barrier across all blades. When the count reaches the total number of cores (or a configured subset), all waiting cores are released simultaneously.

The barrier can be configured to ignore failed cores (e.g., cores that have been disabled due to errors). The timeout mechanism prevents deadlock if a core never arrives.

**Assembly Examples**

Example 1: Basic global barrier
```assembly
; All cores on all blades wait for each other
BARRIER_SYNC
```

This is the simplest barrier. All cores must reach this point before any continue.

Example 2: Barrier with timeout
```assembly
; Wait at most 1 million cycles
BARRIER_SYNC.TIMEOUT #1000000
BRANCH CS, timeout
```

The .TIMEOUT suffix returns with the carry flag set if the barrier is not reached in time.

Example 3: Phase transition in iterative algorithm
```assembly
iteration_loop:
; Phase 1: compute local results
CALL local_compute
; Phase 2: combine results across all cores
BARRIER_SYNC
; Phase 3: update global state
CALL global_update
BARRIER_SYNC
; Loop
JMP iteration_loop
```

Barriers separate the phases of an iterative parallel algorithm.

Example 4: Barrier with release on interrupt
```assembly
; Allow barrier to be released by interrupt (e.g., debugger)
BARRIER_SYNC.INT
```

The .INT suffix allows an interrupt to release the barrier, useful for debugging.

Example 5: Conditional barrier
```assembly
; Only barrier if flag is set
CMP need_sync, #1
BRANCH NE, no_barrier
BARRIER_SYNC
no_barrier:
```

This allows some cores to skip the barrier.

Example 6: Barrier with core mask
```assembly
; Only synchronize specific cores
BARRIER_SYNC.MASK #0x0000FFFF   ; Only cores 0-15
```

The .MASK suffix only waits for cores specified in the mask.

Example 7: Barrier for distributed training epoch
```assembly
epoch_loop:
; Local training on each blade's data
CALL train_on_local_data
; Synchronize gradients across all blades
BARRIER_SYNC
; Update global model
CALL update_global_model
BARRIER_SYNC
JMP epoch_loop
```

This pattern is used in distributed training of neural networks.

Example 8: Barrier for debugging
```assembly
; Insert barrier to check state
BARRIER_SYNC
; All cores stop here, debugger can inspect
NOP
; Continue
```

A barrier can be used as a global breakpoint.

Example 9: Barrier with core counting
```assembly
; Query how many cores reached barrier
BARRIER_SYNC.COUNT count_buffer
```

The .COUNT suffix returns the number of cores that have reached the barrier.

Example 10: Persistent barrier
```assembly
; Barrier that persists across resets (for fault tolerance)
BARRIER_SYNC.PERSIST
```

The .PERSIST suffix ensures that if a core fails and resets, it will rejoin the barrier.

---

This concludes Chapter 9 of the Instruction Set Reference. The remaining chapters will cover Memory Management Instructions (SEGMENT_CREATE, SEGMENT_DELETE, SEGMENT_MODIFY, CAPABILITY_GRANT, CAPABILITY_ACCEPT, SEGMENT_LOOKUP, TLB_INVALIDATE) and Protection Instructions (OWNER_GET, OWNER_SET_PARENT, RING_SET, IRQ_SET, IO_MAP, SEGMENT_WALK).

# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 10: Memory Management Instructions

### 10.1 SEGMENT_CREATE – Create Memory Segment

The SEGMENT_CREATE instruction creates a new segment in the memory segment tree. Segments are the fundamental unit of memory management in the PIP CISC architecture, replacing traditional page tables. Each segment descriptor contains the segment's base address, size, owner, permissions, and a pointer to its child segments. This hierarchical structure enables efficient address translation, fine-grained protection, and capability-based security.

**Encoding Format**

SEGMENT_CREATE uses opcode 0xB0. The instruction header contains opcode 0xB0, flags, and operand count of 6. The operands are: the parent segment identifier, the base address, the size (as a power-of-two exponent), the owner identifier, the permissions mask, and a pointer to a segment descriptor buffer.

The flags field encodes the segment type (bits 8-11: 0=data, 1=code, 2=page table, 3=capability, 4=remote, 5=IO, 6-15 reserved) and bit 12 for "make persistent" (survives reset). Bits 13-15 are reserved.

The base address must be aligned to the segment size. The size is specified as an exponent: actual size = 2^(12 + size_field), where size_field is 0-47 (4KB to 2^59 bytes). The owner identifier is a 32-bit value. The permissions mask is an 8-bit value with bits for read, write, execute, create child, delegate, and seal.

**Operation Details**

When SEGMENT_CREATE executes, the following steps occur. The instruction must be executed at privilege level 0 or by an owner with the "create child" permission on the parent segment. A new segment descriptor is allocated from the segment table. The descriptor is initialized with the specified parameters. The parent segment's child pointer is updated to point to the new descriptor.

The segment descriptor buffer is filled with the new segment's information, including its segment identifier (index into the segment table). This identifier can be used in future memory management instructions.

The instruction completes in approximately 10 cycles, plus memory access time for the segment table.

**Assembly Examples**

Example 1: Create a data segment
```assembly
; Create a 1MB data segment (2^20 bytes, exponent 8 since 12+8=20)
; Parent segment 0 (root), base address 0x10000000, owner current
; Permissions: read, write, no execute, no child creation
SEGMENT_CREATE #0, #0x10000000, #8, current_owner, #0x03, desc_buffer
```

This creates a 1MB data segment. The segment identifier is returned in the descriptor buffer.

Example 2: Create a code segment
```assembly
; Create a 64KB code segment (2^16 bytes, exponent 4)
; Execute-only permission
SEGMENT_CREATE.CODE #0, #0x20000000, #4, current_owner, #0x04, desc_buffer
```

The .CODE suffix sets the segment type to code. The permission 0x04 grants execute permission only.

Example 3: Create a child segment
```assembly
; First, create a parent segment (a directory)
SEGMENT_CREATE #0, #0x30000000, #20, current_owner, #0x0F, parent_desc
; Then create a child within that parent
LD.W parent_id, [parent_desc]   ; Extract parent ID
SEGMENT_CREATE parent_id, #0x30001000, #12, current_owner, #0x03, child_desc
```

The parent segment has permission 0x0F (read, write, execute, create child). The child segment is created within the parent's address range.

Example 4: Create a remote segment (capability)
```assembly
; Create a segment that refers to memory on blade 4
SEGMENT_CREATE.REMOTE #0, #0x40000000, #20, current_owner, #0x03, desc_buffer, #4
```

The .REMOTE suffix creates a remote segment. The extra operand specifies the target blade.

Example 5: Create an I/O segment
```assembly
; Map I/O device registers into address space
SEGMENT_CREATE.IO #0, #0xFE000000, #12, current_owner, #0x03, desc_buffer
```

The .IO suffix creates a segment for memory-mapped I/O. Writes to this segment may have side effects.

Example 6: Create with limited permissions
```assembly
; Read-only segment (shared library)
SEGMENT_CREATE #0, #0x50000000, #24, current_owner, #0x01, desc_buffer
```

Permission 0x01 grants read-only access. Write attempts cause protection faults.

Example 7: Create sealed segment (immutable)
```assembly
; Sealed segment cannot be modified after creation
SEGMENT_CREATE.SEALED #0, #0x60000000, #20, current_owner, #0x01, desc_buffer
```

The .SEALED suffix sets the sealed bit. The segment descriptor cannot be modified after creation.

Example 8: Create persistent segment
```assembly
; Segment survives system reset
SEGMENT_CREATE.PERSIST #0, #0x70000000, #20, current_owner, #0x03, desc_buffer
```

The .PERSIST suffix stores the segment descriptor in non-volatile memory.

Example 9: Create with delegation permission
```assembly
; Segment that can be delegated to other owners
SEGMENT_CREATE #0, #0x80000000, #20, current_owner, #0x0B, desc_buffer
```

Permission 0x0B (binary 1011) grants read, write, and delegate permissions (bit 3 set for delegate).

Example 10: Create large segment (entire blade memory)
```assembly
; Create a segment covering all local memory (exponent 40 = 1TB)
SEGMENT_CREATE #0, #0x00000000, #40, current_owner, #0x03, desc_buffer
```

This creates a segment that covers the entire local address space.

---

### 10.2 SEGMENT_DELETE – Delete Memory Segment

The SEGMENT_DELETE instruction removes a segment from the segment tree. All child segments are recursively deleted as well. The memory previously covered by the segment becomes inaccessible. This instruction is used to free memory regions, unmap files, and remove capability delegations.

**Encoding Format**

SEGMENT_DELETE uses opcode 0xB1. The instruction header contains opcode 0xB1, flags, and operand count of 1. The operand is the segment identifier to delete.

The flags field has bit 8 for "force" (delete even if segment is in use), bit 9 for "lazy" (mark as deleted but delay reclamation), and bits 10-15 reserved.

**Operation Details**

When SEGMENT_DELETE executes, the following steps occur. The instruction must be executed by the segment owner or an ancestor owner. The segment and all its children are marked as deleted in the segment table. The TLB is invalidated for all addresses covered by the deleted segments.

If the "force" flag is set, the deletion proceeds even if other cores are currently accessing the segment. Those accesses may fault after deletion. If the "lazy" flag is set, the segment is marked as deleted but the physical memory is not reclaimed until all references are gone.

**Assembly Examples**

Example 1: Delete a single segment
```assembly
; Delete segment with ID 42
SEGMENT_DELETE #42
```

The segment and its descriptor are removed from the segment table.

Example 2: Delete with children
```assembly
; Delete a directory segment and all its children
SEGMENT_DELETE #10   ; Parent segment ID
```

All child segments are recursively deleted. The physical memory is reclaimed.

Example 3: Force delete (dangerous)
```assembly
; Force delete even if in use
SEGMENT_DELETE.FORCE #42
```

The .FORCE suffix deletes the segment regardless of whether other cores are accessing it.

Example 4: Lazy delete
```assembly
; Mark for deletion, reclaim later
SEGMENT_DELETE.LAZY #42
```

The .LAZY suffix marks the segment as deleted but does not immediately reclaim memory.

Example 5: Delete remote segment
```assembly
; Delete a segment on remote blade
SEGMENT_DELETE.REMOTE @4:42
```

The .REMOTE suffix deletes a segment whose descriptor is on a remote blade.

Example 6: Delete and unmap
```assembly
; Unmap a mapped file
SEGMENT_DELETE file_segment
```

When a file is no longer needed, deleting its segment unmaps it from the address space.

Example 7: Delete with TLB flush
```assembly
; Delete and ensure TLB is flushed
SEGMENT_DELETE #42
TLB_INVALIDATE.ALL   ; Flush all TLB entries
```

TLB entries for the deleted segment may persist. Explicit invalidation ensures correctness.

Example 8: Delete all child segments
```assembly
; Delete all children of segment 100 without deleting 100 itself
; This requires walking the segment tree manually
SEGMENT_WALK #100, walk_buffer
; Iterate over children and delete each
```

The SEGMENT_WALK instruction can be used to find all children of a segment.

Example 9: Delete and notify
```assembly
; Delete and send notification to users
SEGMENT_DELETE #42
; Broadcast to all blades that the segment is gone
BROADCAST
TLB_INVALIDATE #42
BROADCAST_END
```

After deletion, all blades should invalidate their TLBs for the deleted addresses.

Example 10: Delete with error recovery
```assembly
; Attempt to delete, handle error if segment not found
SEGMENT_DELETE #42
BRANCH CS, not_found   ; Carry flag set if segment doesn't exist
```

The carry flag indicates whether the segment existed.

---

### 10.3 SEGMENT_MODIFY – Modify Segment Permissions or Owner

The SEGMENT_MODIFY instruction changes the permissions or owner of an existing segment. This is used to grant or revoke access rights, change ownership for delegation, or seal/unseal segments. Permission changes take effect immediately for all future accesses; the TLB is automatically invalidated for the affected addresses.

**Encoding Format**

SEGMENT_MODIFY uses opcode 0xB2. The instruction header contains opcode 0xB2, flags, and operand count of 3. The operands are: the segment identifier, the new permissions mask (or owner identifier), and a flag indicating which field to modify.

The flags field has bit 8 for "change permissions", bit 9 for "change owner", bit 10 for "seal" (make immutable), bit 11 for "unseal", and bits 12-15 reserved.

**Operation Details**

When SEGMENT_MODIFY executes, the following steps occur. The instruction must be executed by the segment owner or an ancestor owner. The specified field in the segment descriptor is updated. The TLB is invalidated for all addresses in the segment. Subsequent accesses use the new permissions or ownership.

If the "seal" flag is set, the segment becomes immutable; no further modifications are possible. Sealing is irreversible.

**Assembly Examples**

Example 1: Change permissions to read-only
```assembly
; Make segment 42 read-only (remove write permission)
SEGMENT_MODIFY.PERM #42, #0x01
```

The .PERM suffix changes the permissions mask to 0x01 (read-only).

Example 2: Add execute permission
```assembly
; Add execute permission to segment 42
; Read current permissions, OR with 0x04, write back
SEGMENT_MODIFY.PERM #42, #0x05   ; Read + Execute
```

This adds execute permission while preserving read permission.

Example 3: Change owner
```assembly
; Transfer ownership of segment 42 to owner 4096
SEGMENT_MODIFY.OWNER #42, #4096
```

The .OWNER suffix changes the owner field. The new owner can now modify the segment.

Example 4: Seal a segment
```assembly
; Make segment 42 immutable
SEGMENT_MODIFY.SEAL #42
```

The .SEAL suffix sets the sealed bit. No further modifications to the segment descriptor are possible.

Example 5: Grant delegation permission
```assembly
; Add delegate permission to segment 42
SEGMENT_MODIFY.PERM #42, #0x0B   ; Read + Write + Delegate
```

The delegate permission (bit 3) allows the owner to create capabilities from this segment.

Example 6: Revoke all permissions
```assembly
; Make segment inaccessible
SEGMENT_MODIFY.PERM #42, #0x00
```

Setting permissions to zero makes the segment inaccessible to all.

Example 7: Modify remote segment
```assembly
; Change permissions on remote segment
SEGMENT_MODIFY.REMOTE @4:42, PERM, #0x01
```

The .REMOTE suffix modifies a segment descriptor on a remote blade.

Example 8: Unseal (if owner)
```assembly
; Unseal a segment (only possible if owner and not permanently sealed)
SEGMENT_MODIFY.UNSEAL #42
```

The .UNSEAL suffix removes the sealed bit, allowing modifications again.

Example 9: Atomic permission change
```assembly
; Change permissions only if segment is still owned by current owner
; The segment is not locked, but the operation is atomic
SEGMENT_MODIFY.PERM #42, #0x01
```

The descriptor update is atomic with respect to other cores.

Example 10: Verify change
```assembly
; Change permissions, then verify
SEGMENT_MODIFY.PERM #42, #0x01
SEGMENT_LOOKUP R1, #42   ; Look up segment by ID
AND R1, #0x07            ; Extract permissions
CMP R1, #0x01
BRANCH EQ, success
```

The SEGMENT_LOOKUP instruction confirms that the change took effect.

---

### 10.4 CAPABILITY_GRANT – Create Delegation Token

The CAPABILITY_GRANT instruction creates a cryptographically signed capability token that delegates access to a memory segment to another owner. The token can be transmitted over any communication channel (including insecure channels) because the signature prevents forgery. This implements capability-based security, where access rights are granted by passing tokens rather than by global privilege levels.

**Encoding Format**

CAPABILITY_GRANT uses opcode 0xB3. The instruction header contains opcode 0xB3, flags, and operand count of 5. The operands are: the segment identifier, the target owner identifier, the maximum permissions to grant, an expiration timestamp, and a pointer to a token buffer.

The flags field encodes the token type (bits 8-9: 00=one-time use, 01=bounded use count, 10=time-limited, 11=permanent), bit 10 for "revocable", bit 11 for "audit", and bits 12-15 reserved.

The token buffer is a 128-byte region that receives the signed token. The token includes the segment identifier, target owner, permissions, expiration, and a cryptographic signature.

**Operation Details**

When CAPABILITY_GRANT executes, the following steps occur. The instruction must be executed by the segment owner or an owner with delegate permission on the segment. A token is constructed containing the grant information. The token is signed using a hardware private key unique to the granting blade. The token is written to the token buffer.

The token can be transmitted to the target owner. The target owner uses CAPABILITY_ACCEPT to import the token and create a local segment.

**Assembly Examples**

Example 1: Grant read-only access
```assembly
; Grant read-only access to segment 42 to owner 4096
; Token expires in 1 hour
CAPABILITY_GRANT #42, #4096, #0x01, #3600, token_buffer
```

This creates a token that delegates read-only access. The token expires after 3600 seconds.

Example 2: Grant full access
```assembly
; Grant full access (read, write, execute, delegate)
CAPABILITY_GRANT #42, #4096, #0x0F, #0, token_buffer
```

A zero expiration means the token never expires.

Example 3: One-time use token
```assembly
; Token can only be used once
CAPABILITY_GRANT.ONCE #42, #4096, #0x03, #0, token_buffer
```

The .ONCE suffix creates a one-time token. After CAPABILITY_ACCEPT, the token is invalidated.

Example 4: Revocable token
```assembly
; Grant that can be revoked by the granter
CAPABILITY_GRANT.REVOKE #42, #4096, #0x03, #0, token_buffer
```

The .REVOKE suffix creates a revocable token. The granter can later revoke it using CAPABILITY_REVOKE.

Example 5: Audited token
```assembly
; Every access using this token is logged
CAPABILITY_GRANT.AUDIT #42, #4096, #0x01, #0, token_buffer
```

The .AUDIT suffix causes the hardware to log every access made using this capability.

Example 6: Limited-use token
```assembly
; Token valid for 1000 accesses
CAPABILITY_GRANT.COUNT #42, #4096, #0x01, #1000, token_buffer
```

The .COUNT suffix limits the token to the specified number of uses.

Example 7: Grant to multiple owners
```assembly
; Grant to owner 4096 with capability to further delegate
CAPABILITY_GRANT #42, #4096, #0x0F, #0, token_buffer
; Owner 4096 can now grant to others using the delegate permission
```

Delegation permission (bit 3) allows the recipient to create further grants.

Example 8: Remote grant
```assembly
; Grant access to segment on local blade to remote owner
CAPABILITY_GRANT.REMOTE #42, @4:4096, #0x01, #0, token_buffer
```

The .REMOTE suffix specifies that the target owner is on a remote blade.

Example 9: Grant with specific address range
```assembly
; Grant only a subrange of the segment (offset 4096, size 8192)
CAPABILITY_GRANT.SUB #42, #4096, #8192, #4096, #0x03, #0, token_buffer
```

The .SUB suffix restricts the grant to a subrange of the segment.

Example 10: Send token via message
```assembly
; Create token and send to remote blade via message queue
CAPABILITY_GRANT #42, #4096, #0x01, #0, token_buffer
; Copy token to message
MOV.V message_data, token_buffer, #128
; Send message to blade 4
SEND_MSG #4, message_data, #128
```

The token is copied into a message and transmitted to the remote blade.

---

### 10.5 CAPABILITY_ACCEPT – Import Capability Token

The CAPABILITY_ACCEPT instruction imports a capability token and creates a local segment that refers to the delegated memory. The token must be cryptographically valid, unexpired, and targeted to the accepting owner. After acceptance, the local segment can be used with standard load/store instructions.

**Encoding Format**

CAPABILITY_ACCEPT uses opcode 0xB4. The instruction header contains opcode 0xB4, flags, and operand count of 3. The operands are: a pointer to the token buffer, the desired local segment name (or zero for automatic), and a pointer to a descriptor buffer.

The flags field has bit 8 for "verify only" (test token without importing), bit 9 for "create persistent", and bits 10-15 reserved.

**Operation Details**

When CAPABILITY_ACCEPT executes, the following steps occur. The token is verified: the signature is checked, the expiration is validated, and the target owner is matched against the current owner. If verification fails, the instruction returns an error.

If verification succeeds, a new segment descriptor is created in the local segment table. The descriptor points to the remote memory (or local memory if the grant was local). The new segment's identifier is returned in the descriptor buffer.

**Assembly Examples**

Example 1: Accept a token
```assembly
; Import token from token_buffer, create new segment
CAPABILITY_ACCEPT token_buffer, #0, desc_buffer
LD.W new_seg_id, [desc_buffer]   ; Get new segment ID
```

The imported segment can now be accessed like any local segment.

Example 2: Verify token without importing
```assembly
; Check if token is valid without creating a segment
CAPABILITY_ACCEPT.VERIFY token_buffer, #0, desc_buffer
BRANCH CS, invalid_token
```

The .VERIFY suffix validates the token but does not create a segment.

Example 3: Accept with specific segment ID
```assembly
; Create segment with specific ID (100)
CAPABILITY_ACCEPT token_buffer, #100, desc_buffer
```

The segment ID 100 is used. If 100 is already in use, the instruction fails.

Example 4: Accept remote grant
```assembly
; Token was created on remote blade
CAPABILITY_ACCEPT token_buffer, #0, desc_buffer
```

The token contains the remote blade information. The new segment is marked as remote.

Example 5: Accept and persist
```assembly
; Import and make persistent across resets
CAPABILITY_ACCEPT.PERSIST token_buffer, #0, desc_buffer
```

The .PERSIST suffix stores the new segment descriptor in non-volatile memory.

Example 6: Accept with reduced permissions
```assembly
; Accept but use only read permission (ignore write permission in token)
; This requires modifying the descriptor after import
CAPABILITY_ACCEPT token_buffer, #0, desc_buffer
LD.W seg_id, [desc_buffer]
SEGMENT_MODIFY.PERM seg_id, #0x01   ; Reduce to read-only
```

The acceptor can voluntarily reduce the granted permissions.

Example 7: Batch accept
```assembly
; Accept multiple tokens in a loop
MOV R10, #0
MOV R11, #100   ; 100 tokens
loop:
LEA R12, [token_array + R10*128]
CAPABILITY_ACCEPT R12, #0, desc_buffer
LD.W [seg_array + R10*4], [desc_buffer]
ADD R10, #1
CMP R10, R11
BRANCH LT, loop
```

This imports an array of tokens, creating a segment for each.

Example 8: Accept with timeout check
```assembly
; Check expiration before accepting
CAPABILITY_ACCEPT.VERIFY token_buffer, #0, desc_buffer
BRANCH CS, expired
CAPABILITY_ACCEPT token_buffer, #0, desc_buffer
```

The verify step checks expiration without committing to import.

Example 9: Accept and use immediately
```assembly
; Import and access the memory
CAPABILITY_ACCEPT token_buffer, #0, desc_buffer
LD.W seg_base, [desc_buffer + #8]   ; Base address from descriptor
MOV R1, [seg_base]                  ; Read first word of imported memory
```

The imported segment is immediately accessible.

Example 10: Accept with auditing
```assembly
; Accept token that requires auditing
CAPABILITY_ACCEPT token_buffer, #0, desc_buffer
; All accesses to this segment will be logged by hardware
```

If the token was created with the audit flag, the hardware logs all accesses.

---

### 10.6 SEGMENT_LOOKUP – Look Up Segment Descriptor

The SEGMENT_LOOKUP instruction returns the segment descriptor for a given virtual address or segment identifier. This is used by the operating system to inspect memory mappings, validate addresses, and debug protection faults. The instruction does not perform any access checks; it simply returns the descriptor.

**Encoding Format**

SEGMENT_LOOKUP uses opcode 0xB5. The instruction header contains opcode 0xB5, flags, and operand count of 2. The operands are: the virtual address (or segment ID) and a pointer to a descriptor buffer.

The flags field has bit 8 for "lookup by ID" (first operand is segment ID, not address), bit 9 for "walk tree" (return full path of descriptors), and bits 10-15 reserved.

**Operation Details**

When SEGMENT_LOOKUP executes, the following steps occur. The address translation hardware walks the segment tree to find the leaf segment containing the address. The segment descriptor is copied to the descriptor buffer. If the address is not mapped, the instruction returns with the carry flag set.

If the "walk tree" flag is set, the instruction returns an array of descriptors for all ancestors of the address.

**Assembly Examples**

Example 1: Look up address
```assembly
; Find which segment contains address 0x10000000
SEGMENT_LOOKUP #0x10000000, desc_buffer
BRANCH CS, not_mapped
```

The descriptor buffer contains the segment information.

Example 2: Look up by segment ID
```assembly
; Get descriptor for segment 42
SEGMENT_LOOKUP.ID #42, desc_buffer
```

The .ID suffix interprets the first operand as a segment ID.

Example 3: Walk tree for debugging
```assembly
; Get full path of descriptors for address
SEGMENT_LOOKUP.WALK #0x10000000, path_buffer
; path_buffer contains root, intermediate, and leaf descriptors
```

This is useful for debugging protection faults.

Example 4: Check permissions
```assembly
; Verify that address is writable
SEGMENT_LOOKUP #0x10000000, desc_buffer
BRANCH CS, invalid
LD.B R1, [desc_buffer + #13]   ; Permissions byte
TEST R1, #0x02                  ; Test write bit
BRANCH EQ, not_writable
```

The permissions byte is extracted from the descriptor.

Example 5: Get segment size
```assembly
; Get size of segment containing address
SEGMENT_LOOKUP #0x10000000, desc_buffer
LD.B R1, [desc_buffer + #4]    ; Size exponent
MOV R2, #1
SHL R2, R2, #12                ; 4096
SHL size, R2, R1               ; 4096 * 2^exponent = actual size
```

The size is encoded as a power-of-two exponent.

Example 6: Get segment owner
```assembly
; Get owner of segment
SEGMENT_LOOKUP #0x10000000, desc_buffer
LD.W R1, [desc_buffer + #9]    ; Owner ID
```

The owner field identifies who can modify the segment.

Example 7: Check if address is in flash
```assembly
; Determine if address is mapped to flash storage
SEGMENT_LOOKUP #0x10000000, desc_buffer
LD.B R1, [desc_buffer + #0]    ; Type byte
TEST R1, #0x03                  ; Check if type is flash
```

The segment type indicates whether the memory is DRAM, flash, or I/O.

Example 8: Find base address
```assembly
; Get the base address of the segment containing address
SEGMENT_LOOKUP #0x10000000, desc_buffer
LD.D R1, [desc_buffer + #16]   ; Base address (64-bit)
```

The base address is the start of the segment.

Example 9: Look up remote address
```assembly
; Look up address on remote blade
SEGMENT_LOOKUP.REMOTE @4:0x10000000, desc_buffer
```

The .REMOTE suffix looks up an address in a remote blade's segment tree.

Example 10: Validate system call arguments
```assembly
; System call: validate user buffer
; R1 = user address, R2 = length
SEGMENT_LOOKUP R1, desc_buffer
BRANCH CS, invalid_address
LD.B R3, [desc_buffer + #13]    ; Permissions
TEST R3, #0x01                   ; Read permission?
BRANCH EQ, no_read_permission
; Also check that the entire range is within the same segment
```

This is the standard way to validate user-provided addresses in system calls.

---

### 10.7 TLB_INVALIDATE – Invalidate TLB Entry

The TLB_INVALIDATE instruction removes one or more entries from the Translation Lookaside Buffer (TLB). The TLB caches segment tree lookups for fast address translation. When a segment descriptor is modified or deleted, the TLB must be invalidated to prevent stale translations. This instruction is used by the operating system after memory map changes.

**Encoding Format**

TLB_INVALIDATE uses opcode 0xB6. The instruction header contains opcode 0xB6, flags, and operand count of 1. The operand is the address range to invalidate (or a segment ID).

The flags field has bit 8 for "invalidate by segment ID", bit 9 for "invalidate all", bit 10 for "invalidate range", bit 11 for "global invalidation (broadcast)", and bits 12-15 reserved.

**Operation Details**

When TLB_INVALIDATE executes, the following steps occur. The specified TLB entries are marked as invalid. Future accesses to those addresses will cause a TLB miss and trigger a segment tree walk. The invalidation is local to the current core unless the "global" flag is set.

If the "global" flag is set, the invalidation is broadcast to all cores on the blade (or all blades if combined with BROADCAST).

**Assembly Examples**

Example 1: Invalidate a single page
```assembly
; Invalidate TLB for address 0x10000000
TLB_INVALIDATE #0x10000000
```

The TLB entry for that specific page is invalidated.

Example 2: Invalidate by segment ID
```assembly
; Invalidate all TLB entries for segment 42
TLB_INVALIDATE.ID #42
```

The .ID suffix interprets the operand as a segment ID.

Example 3: Invalidate all TLB entries
```assembly
; Flush entire TLB
TLB_INVALIDATE.ALL
```

The .ALL suffix invalidates every TLB entry on the current core.

Example 4: Global invalidation (broadcast to all cores)
```assembly
; Invalidate address on all cores on this blade
TLB_INVALIDATE.GLOBAL #0x10000000
```

The .GLOBAL suffix sends the invalidation to all cores on the blade.

Example 5: Invalidate range
```assembly
; Invalidate all addresses from 0x10000000 to 0x20000000
TLB_INVALIDATE.RANGE #0x10000000, #0x20000000
```

The .RANGE suffix invalidates all TLB entries within the specified range.

Example 6: Broadcast invalidation to all blades
```assembly
; Invalidate address on every blade in the rack
BROADCAST
TLB_INVALIDATE #0x10000000
BROADCAST_END
```

Using BROADCAST, the invalidation is sent to all blades.

Example 7: Invalidate after permission change
```assembly
; Change segment permissions, then invalidate TLB
SEGMENT_MODIFY.PERM #42, #0x01
TLB_INVALIDATE.ID #42
```

TLB invalidation ensures that subsequent accesses use the new permissions.

Example 8: Invalidate and wait
```assembly
; Invalidate and ensure completion before continuing
TLB_INVALIDATE #0x10000000
FENCE   ; Wait for invalidation to complete
```

A FENCE instruction ensures that the invalidation has propagated.

Example 9: Selective invalidation
```assembly
; Invalidate only if address is in a specific range
CMP R1, #0x10000000
BRANCH LO, skip
CMP R1, #0x20000000
BRANCH HI, skip
TLB_INVALIDATE R1
skip:
```

The invalidation is conditional on the address range.

Example 10: Debug TLB state
```assembly
; Invalidate and then check that entry is gone
TLB_INVALIDATE #0x10000000
; Try to access the address (will cause TLB miss)
MOV R2, [0x10000000]   ; This will trigger segment tree walk
```

After invalidation, the next access to the address forces a fresh translation.

---

This concludes Chapter 10 of the Instruction Set Reference. The final chapter will cover Protection Instructions (OWNER_GET, OWNER_SET_PARENT, RING_SET, IRQ_SET, IO_MAP, SEGMENT_WALK, and privilege management).

# PIP CISC Unified Compute Platform
## Complete Instruction Set Reference

**Volume 3: Instruction Set Architecture**
**Production Version 2.0**

---

## Chapter 11: Protection Instructions

### 11.1 OWNER_GET – Get Current Owner Information

The OWNER_GET instruction returns the current owner identifier and the ancestor chain. The owner identifier is a 32-bit value that determines what memory segments the currently executing code can access. The ancestor chain is the list of parent owners from the current owner up to the root owner (owner 0). This instruction is used by the operating system to determine its privilege level and by applications to query their security context.

**Encoding Format**

OWNER_GET uses opcode 0xB7. The instruction header contains opcode 0xB7, flags, and operand count of 2. The operands are: a pointer to a buffer for the owner identifier, and a pointer to a buffer for the ancestor chain.

The flags field has bit 8 for "include depth" (return the number of ancestors), bit 9 for "validate chain" (verify the chain is intact), and bits 10-15 reserved.

**Operation Details**

When OWNER_GET executes, the following steps occur. The current owner identifier (stored in a privileged register) is written to the first buffer. The ancestor chain is traversed from the current owner up to owner 0. Each ancestor's owner ID is written to the second buffer. The number of ancestors is returned in a register.

The instruction completes in a single cycle, as the owner information is cached in the core.

**Assembly Examples**

Example 1: Get current owner
```assembly
; Get current owner ID
OWNER_GET owner_buffer, #0
LD.W R1, [owner_buffer]   ; R1 = current owner
```

This returns the owner identifier of the currently executing code.

Example 2: Get owner and ancestors
```assembly
; Get owner and full ancestor chain
OWNER_GET owner_buffer, ancestors_buffer
LD.W R1, [owner_buffer]          ; Current owner
LD.W R2, [ancestors_buffer]      ; Parent owner
LD.W R3, [ancestors_buffer+4]    ; Grandparent owner
; etc.
```

The ancestor chain reveals the privilege hierarchy.

Example 3: Check privilege level
```assembly
; Check if code is running at hypervisor level (owner 3)
OWNER_GET owner_buffer, #0
LD.W R1, [owner_buffer]
CMP R1, #3
BRANCH EQ, is_hypervisor
```

Different owner IDs correspond to different privilege levels.

Example 4: Get ancestor depth
```assembly
; Get number of ancestors (depth in owner tree)
OWNER_GET.DEPTH owner_buffer, ancestors_buffer
LD.W R1, [ancestors_buffer]   ; Depth count
```

The .DEPTH suffix returns the depth (number of ancestors) in the first word of the ancestors buffer.

Example 5: Validate owner chain
```assembly
; Verify that the owner chain is intact (no corruption)
OWNER_GET.VALIDATE owner_buffer, ancestors_buffer
BRANCH CS, chain_corrupted
```

The .VALIDATE suffix checks that the ancestor chain is consistent. The carry flag is set if corruption is detected.

Example 6: Compare owners for access check
```assembly
; Check if current owner is ancestor of target owner
OWNER_GET owner_buffer, ancestors_buffer
LD.W R1, [owner_buffer]           ; Current owner
LD.W R2, [ancestors_buffer+8]     ; Target owner's ancestor
CMP R1, R2
BRANCH EQ, is_ancestor
```

This implements the owner hierarchy check for memory access.

Example 7: Debug owner context
```assembly
; Print owner context for debugging
CALL print_owner
OWNER_GET owner_buffer, ancestors_buffer
; Print each ancestor
```

Debugging output can show the full owner hierarchy.

Example 8: Remote owner query
```assembly
; Get owner of code running on remote blade
OWNER_GET.REMOTE @4:0, owner_buffer, #0
```

The .REMOTE suffix queries the owner on a remote blade.

Example 9: Owner in exception handler
```assembly
; Exception handler: determine which owner caused the fault
OWNER_GET owner_buffer, #0
LD.W R1, [owner_buffer]   ; Owner that was executing
; R1 may be different from the handler's owner
```

Exception handlers can query the owner that was executing when the fault occurred.

Example 10: Capability delegation verification
```assembly
; Verify that current owner can accept a capability for target owner
OWNER_GET owner_buffer, ancestors_buffer
LD.W current_owner, [owner_buffer]
CMP current_owner, target_owner
BRANCH EQ, can_accept   ; Same owner
; Check if current_owner is ancestor of target_owner
; ... ancestor check logic ...
```

This verifies that the current owner is authorized to accept a capability token.

---

### 11.2 OWNER_SET_PARENT – Set Owner Parent

The OWNER_SET_PARENT instruction modifies the parent of an owner in the owner hierarchy. This instruction can only be executed by the root owner (owner 0) or by an owner with special system privileges. It is used during system initialization to build the owner tree, and during runtime to restructure trust domains.

**Encoding Format**

OWNER_SET_PARENT uses opcode 0xB8. The instruction header contains opcode 0xB8, flags, and operand count of 2. The operands are: the owner identifier to modify, and the new parent owner identifier.

The flags field has bit 8 for "create if missing" (create the owner entry if it doesn't exist), bit 9 for "move subtree" (move all descendants as well), and bits 10-15 reserved.

**Operation Details**

When OWNER_SET_PARENT executes, the following steps occur. The instruction must be executed at privilege level 0 (root owner). The owner hierarchy table is updated to set the parent of the specified owner to the new parent. If the "move subtree" flag is set, all descendants of the owner are moved as well.

The instruction completes in approximately 10 cycles. Changes take effect immediately for all cores.

**Assembly Examples**

Example 1: Set parent during boot
```assembly
; During system initialization, set up owner hierarchy
OWNER_SET_PARENT #1, #0   ; Owner 1 is child of root
OWNER_SET_PARENT #2, #1   ; Owner 2 is child of owner 1
OWNER_SET_PARENT #3, #1   ; Owner 3 is also child of owner 1
```

This builds a hierarchical trust structure.

Example 2: Create new owner
```assembly
; Create a new owner (4096) as child of owner 256
OWNER_SET_PARENT.CREATE #4096, #256
```

The .CREATE suffix creates the owner entry if it does not already exist.

Example 3: Move entire subtree
```assembly
; Move owner 100 and all its descendants under owner 200
OWNER_SET_PARENT.MOVE #100, #200
```

The .MOVE suffix moves the entire subtree, preserving relationships among descendants.

Example 4: Re-parent isolated owner
```assembly
; Owner 500 was orphaned; reattach under owner 1
OWNER_SET_PARENT #500, #1
```

This reattaches an owner that was previously detached.

Example 5: Verify parent setting
```assembly
; Set parent, then verify
OWNER_SET_PARENT #42, #10
OWNER_GET owner_buffer, ancestors_buffer
; Check that ancestor chain includes 10
```

Verification ensures the change took effect.

Example 6: Remote parent setting
```assembly
; Set parent on remote blade's owner table
OWNER_SET_PARENT.REMOTE @4:42, #10
```

The .REMOTE suffix modifies the owner table on a remote blade.

Example 7: Temporary re-parenting
```assembly
; Temporarily move owner under root for privileged operation
OWNER_SET_PARENT #100, #0
; Perform privileged operation
CALL privileged_function
; Restore original parent
OWNER_SET_PARENT #100, #10
```

This pattern is used to temporarily elevate privileges.

Example 8: Detach owner (orphan)
```assembly
; Detach owner 200 (set parent to 0, but not under root's protection)
OWNER_SET_PARENT #200, #0
```

A detached owner has no ancestors but is still under the root's authority.

Example 9: Validate owner hierarchy after change
```assembly
; After moving owners, validate all chains
OWNER_SET_PARENT.MOVE #100, #200
; Iterate over owners to validate
CALL validate_all_owner_chains
```

A consistency check ensures no cycles were introduced.

Example 10: Persistent owner configuration
```assembly
; Set parent and make configuration persistent
OWNER_SET_PARENT #4096, #256
; Store owner table to non-volatile memory
CALL save_owner_table
```

Owner configurations can be saved across resets.

---

### 11.3 RING_SET – Map Ring Numbers to Owner Hierarchy

The RING_SET instruction configures the mapping from traditional x86-style ring numbers (0-3) to the PIP CISC owner hierarchy. This provides backward compatibility for legacy operating systems that expect a ring-based protection model. The mapping is stored in a table that the hardware consults when a ring-relative instruction (such as certain system calls) is executed.

**Encoding Format**

RING_SET uses opcode 0xC0. The instruction header contains opcode 0xC0, flags, and operand count of 2. The operands are: the ring number (0-3) and the owner identifier to map it to.

The flags field has bit 8 for "set default" (map all unconfigured rings to this owner), bit 9 for "clear mapping", and bits 10-15 reserved.

**Operation Details**

When RING_SET executes, the following steps occur. The instruction must be executed at privilege level 0. The ring-to-owner mapping table is updated. When code executes with a given ring number (e.g., from a legacy task segment), the hardware translates that ring to the corresponding owner.

If the "clear mapping" flag is set, the mapping for the specified ring is removed. If the "set default" flag is set, all rings that are not explicitly mapped use the specified owner.

**Assembly Examples**

Example 1: Map ring 0 to owner 2 (kernel)
```assembly
; Map ring 0 (most privileged) to owner 2
RING_SET #0, #2
```

Legacy kernel code running in ring 0 will have owner 2 privileges.

Example 2: Map all rings
```assembly
; Map all four rings
RING_SET #0, #2   ; Kernel
RING_SET #1, #3   ; Device drivers
RING_SET #2, #4   ; System services
RING_SET #3, #5   ; User applications
```

This creates a complete ring-to-owner mapping.

Example 3: Set default owner
```assembly
; Any unmapped ring uses owner 5
RING_SET.DEFAULT #5
```

The .DEFAULT suffix sets the default owner for all rings without explicit mappings.

Example 4: Clear ring mapping
```assembly
; Remove mapping for ring 2
RING_SET.CLEAR #2
```

The .CLEAR suffix removes the mapping, causing ring 2 to use the default owner.

Example 5: Query ring mapping
```assembly
; Read current mapping for ring 0 (use SEGMENT_LOOKUP on mapping table)
; The mapping table is at a known system address
LD.W R1, [ring_map_table + #0]   ; Owner for ring 0
```

The ring mapping table is readable by the operating system.

Example 6: Temporary ring override
```assembly
; Temporarily change ring 3 mapping for a specific process
RING_SET #3, #4096   ; Process-specific owner
CALL user_process
RING_SET #3, #5      ; Restore default
```

This allows per-process owner mapping.

Example 7: Remote ring mapping
```assembly
; Set ring mapping on remote blade
RING_SET.REMOTE @4:0, #0, #2
```

The .REMOTE suffix sets the mapping on a remote blade.

Example 8: Compatibility mode
```assembly
; Configure for legacy OS compatibility
RING_SET #0, #2     ; Kernel
RING_SET #3, #5     ; User
RING_SET.DEFAULT #5 ; Everything else
```

This provides a simple two-ring model (kernel/user) for legacy operating systems.

Example 9: Save and restore ring mappings
```assembly
; Save current mappings
LD.W R1, [ring_map_table]    ; Ring 0 mapping
LD.W R2, [ring_map_table+4]  ; Ring 1 mapping
; Change mappings
RING_SET #0, #100
; ... do work ...
; Restore
RING_SET #0, R1
```

Mappings can be saved and restored for context switching.

Example 10: Validate ring configuration
```assembly
; Check that all rings map to valid owners
MOV R10, #0
loop:
LD.W R1, [ring_map_table + R10*4]
CMP R1, #0
BRANCH EQ, invalid   ; Owner 0 is reserved for hardware
ADD R10, #1
CMP R10, #4
BRANCH LT, loop
```

A validation loop ensures all ring mappings are valid.

---

### 11.4 IRQ_SET – Assign Interrupt to Owner

The IRQ_SET instruction assigns an interrupt request line (IRQ) to a specific owner. When the specified interrupt occurs, the hardware transfers control to the interrupt handler registered by that owner. This enables multiple operating systems or virtual machines to share hardware interrupts, with each owner receiving only the interrupts assigned to it.

**Encoding Format**

IRQ_SET uses opcode 0xC1. The instruction header contains opcode 0xC1, flags, and operand count of 2. The operands are: the IRQ number and the target owner identifier.

The flags field has bit 8 for "enable", bit 9 for "disable", bit 10 for "steal" (take from current owner), and bits 11-15 reserved.

**Operation Details**

When IRQ_SET executes, the following steps occur. The instruction must be executed at privilege level 0. The interrupt controller is programmed to deliver the specified IRQ to the target owner. The target owner must have registered an interrupt handler via the interrupt descriptor table.

If the "steal" flag is set, the IRQ is taken from its current owner without requiring that owner's cooperation.

**Assembly Examples**

Example 1: Assign timer interrupt to owner 2
```assembly
; Timer IRQ (typically IRQ 0) goes to owner 2
IRQ_SET #0, #2
```

Owner 2's timer handler will be invoked on each timer tick.

Example 2: Assign keyboard interrupt to owner 5
```assembly
; Keyboard IRQ (IRQ 1) goes to user application owner 5
IRQ_SET #1, #5
```

A user application can directly receive keyboard interrupts.

Example 3: Enable an IRQ
```assembly
; Enable IRQ 4 (COM1) for owner 3
IRQ_SET.ENABLE #4, #3
```

The .ENABLE suffix ensures the IRQ is enabled after assignment.

Example 4: Disable an IRQ
```assembly
; Disable IRQ 4 (stop delivering interrupts)
IRQ_SET.DISABLE #4, #0
```

The .DISABLE suffix disables the IRQ. The owner is ignored.

Example 5: Steal IRQ from another owner
```assembly
; Take IRQ 0 from current owner and give to owner 2
IRQ_SET.STEAL #0, #2
```

The .STEAL suffix forcibly reassigns the IRQ. This requires root privilege.

Example 6: Query IRQ owner
```assembly
; Read current owner of IRQ 0 (use memory-mapped interrupt controller)
LD.W R1, [IRQ_OWNER_TABLE + #0*4]
```

The interrupt controller's owner table is memory-mapped.

Example 7: Assign multiple IRQs to same owner
```assembly
; Assign all IRQs for a sound card to driver owner 100
IRQ_SET #10, #100   ; Sound card IRQ
IRQ_SET #11, #100   ; DMA IRQ
IRQ_SET #12, #100   ; MPU-401 IRQ
```

A device driver may need multiple IRQs.

Example 8: Remote IRQ assignment
```assembly
; Assign IRQ on remote blade 4 to owner 2 on that blade
IRQ_SET.REMOTE @4:0, #0, #2
```

The .REMOTE suffix sets the IRQ mapping on a remote blade.

Example 9: Restore default IRQ mapping
```assembly
; Reset IRQ 0 to default owner (usually owner 1)
IRQ_SET #0, #1
```

This restores the default mapping.

Example 10: IRQ mapping for virtualization
```assembly
; Virtual machine 1 (owner 4096) gets keyboard and mouse
IRQ_SET #1, #4096   ; Keyboard
IRQ_SET #12, #4096  ; Mouse
; Virtual machine 2 (owner 4097) gets timer
IRQ_SET #0, #4097   ; Timer
```

Virtual machines receive isolated interrupt assignments.

---

### 11.5 IO_MAP – Map I/O Device into Segment Tree

The IO_MAP instruction maps a memory-mapped I/O device into the segment tree. Device registers become accessible via normal load and store instructions, but with the important distinction that accesses may have side effects (e.g., reading a status register may clear bits, writing a command register may start a DMA transfer). IO_MAP is used by device drivers to gain access to hardware.

**Encoding Format**

IO_MAP uses opcode 0xC2. The instruction header contains opcode 0xC2, flags, and operand count of 4. The operands are: the physical base address of the I/O device, the size in bytes, the target segment (where to create the mapping), and the permissions.

The flags field encodes the device type (bits 8-11: 0=memory, 1=PCI config space, 2=USB host controller, 3=storage controller, 4=network interface, 5=video, 6=audio, 7-15=reserved), bit 12 for "write-combining", and bit 13 for "prefetchable". Bits 14-15 are reserved.

**Operation Details**

When IO_MAP executes, the following steps occur. The instruction must be executed at privilege level 0. A new segment is created (or an existing segment is modified) to map the I/O device's physical address range into the specified target segment.

Accesses to the mapped addresses bypass the cache by default (unless caching is explicitly enabled). The device type informs the hardware about any special access semantics.

**Assembly Examples**

Example 1: Map PCI configuration space
```assembly
; Map PCI configuration space for bus 0
IO_MAP.PCI #0xCF800000, #0x1000000, #segment_io, #0x03
```

The .PCI suffix maps PCI configuration space. Accesses use PCI-specific addressing.

Example 2: Map a UART
```assembly
; Map a 16550 UART at physical address 0x3F8
IO_MAP #0x3F8, #8, #segment_uart, #0x03
```

The UART's registers are now accessible at the base address in segment_uart.

Example 3: Map with write-combining for frame buffer
```assembly
; Map video frame buffer with write-combining
IO_MAP.WC #0xA0000, #0x20000, #segment_fb, #0x03
```

The .WC suffix enables write-combining, improving performance for linear frame buffer writes.

Example 4: Map read-only device status
```assembly
; Map read-only device status registers
IO_MAP #0x4000, #0x100, #segment_status, #0x01   ; Read-only
```

Read-only mapping prevents accidental writes to status registers.

Example 5: Map USB host controller
```assembly
; Map EHCI USB host controller
IO_MAP.USB #0xFE000000, #0x1000, #segment_usb, #0x03
```

The .USB suffix indicates a USB host controller, enabling special USB-specific access optimizations.

Example 6: Unmap a device
```assembly
; Remove I/O device mapping (set size to 0)
IO_MAP #0, #0, #segment_uart, #0
```

Unmapping makes the device inaccessible.

Example 7: Map network interface with prefetch
```assembly
; Map network card with prefetch enabled
IO_MAP.PREFETCH #0xFE200000, #0x10000, #segment_net, #0x03
```

The .PREFETCH suffix allows the hardware to prefetch from this region.

Example 8: Remote device mapping
```assembly
; Map device on remote blade 4
IO_MAP.REMOTE @4:0x3F8, #8, @4:segment_uart, #0x03
```

The .REMOTE suffix maps a device attached to a remote blade.

Example 9: Map multiple BARs of a PCI device
```assembly
; PCI device with multiple Base Address Registers (BARs)
IO_MAP #0xFE000000, #0x1000, #segment_bar0, #0x03
IO_MAP #0xFE001000, #0x100, #segment_bar1, #0x03
IO_MAP #0xFE001100, #0x2000, #segment_bar2, #0x03
```

A PCI device may have multiple memory regions.

Example 10: Query I/O mapping
```assembly
; Check if an address is an I/O mapping
SEGMENT_LOOKUP #0x3F8, desc_buffer
LD.B R1, [desc_buffer + #0]   ; Segment type
CMP R1, #5                    ; Type 5 = I/O device
BRANCH EQ, is_io_device
```

Segment lookup reveals the type of a mapping.

---

### 11.6 SEGMENT_WALK – Walk Segment Tree

The SEGMENT_WALK instruction traverses the segment tree from the root to the leaf containing a specified address, returning the full path of segment descriptors. This is used by debuggers, memory analysis tools, and the operating system to inspect the memory hierarchy. The instruction returns an array of descriptors, one for each level of the tree.

**Encoding Format**

SEGMENT_WALK uses opcode 0xC3. The instruction header contains opcode 0xC3, flags, and operand count of 3. The operands are: the virtual address to walk, a pointer to a buffer for the descriptor array, and the maximum number of descriptors to return.

The flags field has bit 8 for "include leaf" (include the final segment descriptor), bit 9 for "validate only" (just check walkability), and bits 10-15 reserved.

**Operation Details**

When SEGMENT_WALK executes, the following steps occur. The hardware walks the segment tree from the root. At each level, the segment descriptor is copied to the buffer. The walk continues until a leaf segment is reached or the maximum count is exceeded. The number of descriptors written is returned in a register.

If the "validate only" flag is set, the walk is performed but no descriptors are written; only the success/failure status is returned.

**Assembly Examples**

Example 1: Walk address to leaf
```assembly
; Get full path for address 0x10000000
SEGMENT_WALK #0x10000000, desc_buffer, #10
; Returns: root, intermediate, leaf descriptors
```

The buffer contains all segment descriptors in the path.

Example 2: Validate address walkability
```assembly
; Check if address can be walked without storing descriptors
SEGMENT_WALK.VALIDATE #0x10000000, #0, #0
BRANCH CS, not_walkable
```

The .VALIDATE suffix only checks validity, not storing descriptors.

Example 3: Get segment depth
```assembly
; Determine how many levels deep an address is
SEGMENT_WALK #0x10000000, desc_buffer, #10
LD.W R1, [desc_buffer]   ; First word is count of descriptors
; Number of descriptors = depth + 1 (root is always first)
```

The depth indicates how many segment levels were traversed.

Example 4: Debug protection fault
```assembly
; In fault handler, walk the faulting address
SEGMENT_WALK fault_address, desc_buffer, #10
; Examine each segment's permissions to find the violation
```

This is used to diagnose protection faults.

Example 5: Walk all segments in a directory
```assembly
; Walk all children of a directory segment
; First, get the directory segment's child list
SEGMENT_LOOKUP.ID dir_id, dir_desc
LD.W child_id, [dir_desc + #14]   ; Child pointer
; Then walk each child
```

Walking child segments requires iterating through the segment table.

Example 6: Remote segment walk
```assembly
; Walk address on remote blade
SEGMENT_WALK.REMOTE @4:0x10000000, desc_buffer, #10
```

The .REMOTE suffix walks the segment tree on a remote blade.

Example 7: Walk and verify permissions
```assembly
; Walk address and verify read permission at every level
SEGMENT_WALK #0x10000000, desc_buffer, #10
MOV R10, #0
loop:
LD.B R1, [desc_buffer + R10*16 + #13]   ; Permissions byte (offset in descriptor)
TEST R1, #0x01                           ; Read bit
BRANCH EQ, no_read_permission
ADD R10, #1
CMP R10, walk_depth
BRANCH LT, loop
```

Every segment in the path must grant the required permission.

Example 8: Walk for memory map generation
```coding
; Generate a complete memory map by walking all segments from root
SEGMENT_WALK.ROOT #0, desc_buffer, #4096
; Process each descriptor to build a memory map
```

Walking from the root (address 0) enumerates all mapped memory.

Example 9: Walk with partial results
```assembly
; Walk but stop after 3 levels
SEGMENT_WALK #0x10000000, desc_buffer, #3
; Buffer contains only root, level1, level2 (not leaf)
```

Limiting the depth is useful for examining intermediate segments.

Example 10: Walk for capability debugging
```assembly
; Walk a capability-sealed segment to verify sealing
SEGMENT_WALK cap_address, desc_buffer, #10
LD.B R1, [desc_buffer + #14]   ; Flags byte
TEST R1, #0x20                  ; Sealed bit
BRANCH NE, is_sealed
```

The sealed bit in the segment descriptor indicates immutability.

---

### 11.7 CPUID – Processor Identification

The CPUID instruction returns processor identification and feature information. It is used by operating systems and applications to determine what instruction set extensions are available, the number of cores, cache sizes, and other processor-specific parameters. This instruction is essential for portable software that must adapt to different hardware capabilities.

**Encoding Format**

CPUID uses opcode 0x7D. The instruction header contains opcode 0x7D, flags, and operand count of 1. The operand is the information leaf to return (a 32-bit selector).

The flags field has bits 8-11 for the subleaf (for leaves that have multiple subleaves), and bits 12-15 reserved.

The instruction returns up to four 64-bit values in registers R1, R2, R3, and R4 (or in vector registers for extended information).

**Operation Details**

When CPUID executes, the following steps occur. The processor looks up the information for the requested leaf and subleaf. The results are written to registers. The instruction completes in a single cycle.

Standard leaves include:
- Leaf 0: Maximum leaf number and vendor string
- Leaf 1: Processor model, stepping, and feature flags
- Leaf 2: Cache and TLB information
- Leaf 3: Processor serial number (if enabled)
- Leaf 4: Deterministic cache parameters
- Leaf 7: Extended feature flags (AVX, etc.)
- Leaf 0x80000000: Extended maximum leaf
- Leaf 0x80000001: Extended feature flags
- Leaf 0x40000000: PIP CISC specific features

**Assembly Examples**

Example 1: Get vendor string
```assembly
; Get vendor string (e.g., "PIPCISCA")
CPUID #0
; R1, R2, R3 contain vendor string characters
```

The vendor string identifies the processor manufacturer.

Example 2: Check for AVX support
```assembly
; Check if AVX instructions are supported
CPUID #1
TEST R3, #0x10000000   ; AVX bit (bit 28 of feature flags)
BRANCH NE, avx_supported
```

Feature flags indicate which instruction set extensions are present.

Example 3: Get number of Math cores
```assembly
; Get number of Math cores on this blade
CPUID #0x40000000   ; PIP CISC specific leaf
SHR R1, R1, #16     ; Math core count in high word
AND R1, #0xFFFF     ; Extract
```

PIP CISC specific leaves return architecture-specific information.

Example 4: Get cache line size
```assembly
; Get L1 cache line size
CPUID #2
AND R1, #0xFF       ; Low byte contains cache line size
```

Cache line size is needed for alignment optimizations.

Example 5: Check for HMM instructions
```assembly
; Check if HMM_FORWARD is supported
CPUID #0x40000001   ; Feature leaf for math extensions
TEST R1, #0x01      ; HMM feature bit
BRANCH NE, hmm_supported
```

Software can check for specific instruction support.

Example 6: Get processor frequency
```assembly
; Get nominal processor frequency in MHz
CPUID #0x40000002
; R1 contains frequency in MHz
```

The processor frequency is returned in a register.

Example 7: Get TLB size
```assembly
; Get number of TLB entries
CPUID #2
SHR R1, R1, #8      ; Shift to get TLB entry count
AND R1, #0xFF
```

TLB size information helps with performance tuning.

Example 8: Check for virtualization support
```assembly
; Check if hardware virtualization is supported
CPUID #1
TEST R3, #0x20      ; VMX bit
BRANCH NE, virt_supported
```

Virtualization extensions are reported via feature flags.

Example 9: Get power management features
```assembly
; Check for power management features
CPUID #6
AND R1, #0x01       ; Digital thermal sensor
BRANCH NE, dts_present
```

Power management features are reported in leaf 6.

Example 10: Get maximum vector length
```assembly
; Get maximum supported vector length in bytes
CPUID #0x40000003
; R1 contains maximum vector length (16, 32, 64, or 128)
```

The maximum vector length determines available SIMD width.

---

### 11.8 RDTSC – Read Time-Stamp Counter

The RDTSC instruction reads the processor's time-stamp counter, a 128-bit register that counts the number of cycles since the processor was reset. The counter is monotonically increasing and is synchronized across all cores on the same blade (and across all blades in a unified rack). RDTSC is used for high-resolution timing, performance measurement, and benchmarking.

**Encoding Format**

RDTSC uses opcode 0x7E. The instruction header contains opcode 0x7E, flags, and operand count of 0. The flags field has bit 8 for "serializing" (wait for all previous instructions to complete), and bits 9-15 reserved.

The counter value is returned in a 128-bit register pair: the low 64 bits in R1 and the high 64 bits in R2.

**Operation Details**

When RDTSC executes, the following steps occur. The current value of the time-stamp counter is read. If the serializing flag is set, the processor waits for all previous instructions to retire before reading the counter. The counter value is written to R1 (low 64 bits) and R2 (high 64 bits).

The counter increments at the nominal processor frequency (e.g., 2 GHz). The 128-bit counter overflows after approximately 2^128 / 2e9 seconds, which is effectively never.

**Assembly Examples**

Example 1: Read timestamp
```assembly
; Read current cycle count
RDTSC
; R1:R2 contains 128-bit cycle count
```

The timestamp can be used as a high-resolution clock.

Example 2: Measure code execution time
```assembly
; Measure cycles for a block of code
RDTSC.SERIAL
MOV R3, R1   ; Save start low
MOV R4, R2   ; Save start high
; ... code to measure ...
RDTSC.SERIAL
SUB R1, R3   ; Difference low
SUBC R2, R4  ; Difference high with borrow
```

The .SERIAL suffix ensures accurate measurement by waiting for previous instructions.

Example 3: Convert cycles to nanoseconds
```assembly
; Convert cycle count to nanoseconds
RDTSC
; Get frequency from CPUID
CPUID #0x40000002   ; R1 = frequency in MHz
MUL R3, R1, #1000   ; Convert to KHz
; R1:R2 cycles / (frequency/1e9) = nanoseconds
```

Timestamps can be converted to real time using the processor frequency.

Example 4: Time-stamp for random seed
```assembly
; Use timestamp as entropy source
RDTSC
XOR R1, R2          ; Combine high and low
; Use R1 as seed for PRNG
```

The low bits of the timestamp provide high-entropy random data.

Example 5: Sequential timestamp reads
```assembly
; Read two timestamps to measure interval
RDTSC
MOV R5, R1
MOV R6, R2
; ... some work ...
RDTSC
SUB R1, R5
SUBC R2, R6
; R1:R2 is the interval length
```

This pattern is used for profiling.

Example 6: Global synchronized timestamp
```assembly
; In a unified rack, timestamps are synchronized
BROADCAST
RDTSC
ST.V [timestamp_buffer + core_id*16], R1:R2
BROADCAST_END
```

All blades return the same timestamp value (within a few cycles).

Example 7: Timestamp with core ID
```assembly
; Combine timestamp with core ID for unique identifier
RDTSC
CPUID #0x40000004   ; Get core ID in R3
SHL R3, R3, #64
OR R2, R2, R3       ; Combine core ID with high bits
```

A unique identifier can be formed by combining timestamp and core ID.

Example 8: Wait for specific timestamp
```assembly
; Busy-wait until timestamp reaches target
RDTSC
CMP R1, target_low
BRANCH HI, done
CMP R2, target_high
BRANCH LO, wait
```

This implements a spin-wait loop.

Example 9: Timestamp difference for logging
```assembly
; Log timestamp at entry and exit of function
PUSH_FUNCTION
RDTSC
ST.V [log_entry], R1:R2
CALL function
RDTSC
ST.V [log_exit], R1:R2
POP_FUNCTION
```

Timestamps can be logged for performance analysis.

Example 10: Deterministic timing
```assembly
; Execute code for exactly 1000 cycles
RDTSC
MOV R5, R1
MOV R6, R2
ADD R5, #1000
ADDC R6, #0
wait_loop:
RDTSC
CMP R1, R5
BRANCH LO, wait_loop
CMP R2, R6
BRANCH LO, wait_loop
```

This busy-waits for a precise number of cycles.

---

### 11.9 NOP – No Operation

The NOP (No Operation) instruction performs no operation and consumes one cycle. It is used for instruction alignment, timing delays, placeholder for dynamically modified code, and padding. The NOP instruction does not modify any registers, memory, or flags.

**Encoding Format**

NOP uses opcode 0x00. The instruction header contains opcode 0x00, flags, and operand count of 0. The instruction is encoded as a single 16-bit word: all zeros. The flags field is ignored.

Multiple NOP instructions can be encoded as a multi-byte NOP sequence for alignment purposes.

**Operation Details**

When NOP executes, the following steps occur. The instruction is fetched and decoded. The processor determines that no operation is to be performed. The instruction pointer advances to the next instruction. No state is modified.

The NOP instruction consumes one cycle in the pipeline. Multiple NOPs consume multiple cycles.

**Assembly Examples**

Example 1: Simple NOP
```assembly
NOP   ; Do nothing for one cycle
```

This is the simplest form of NOP.

Example 2: Alignment padding
```assembly
; Align the next instruction to a 16-byte boundary
ALIGN 16
NOP
NOP
NOP
; Next instruction starts at aligned address
```

NOPs are inserted to align code for performance.

Example 3: Timing delay loop
```assembly
; Delay for approximately 100 cycles
MOV R1, #100
delay_loop:
NOP
SUB R1, #1
BRANCH NE, delay_loop
```

NOPs can be used in timing loops when precise delays are needed.

Example 4: Placeholder for hotpatch
```assembly
; Placeholder for function call that will be filled later
NOP
NOP
NOP
NOP
NOP   ; 5 NOPs = room for 5-byte JMP instruction
; Later, patch NOPs with JMP to instrumentation code
```

NOPs serve as placeholders for dynamically inserted code.

Example 5: Pipeline filler
```assembly
; After a branch, fill delay slot with NOP
BRANCH target
NOP   ; Delay slot (executed even if branch taken)
```

Some pipeline architectures have delay slots after branches.

Example 6: Debug breakpoint placeholder
```assembly
; Placeholder for breakpoint
NOP
; Replace with BREAK instruction when debugging
```

NOPs can be replaced with breakpoints by a debugger.

Example 7: Multi-byte NOP for alignment
```assembly
; Multi-byte NOP (often encoded as MOV R1, R1)
NOP.MULTI #7   ; 7-byte NOP sequence
```

Long NOP sequences are encoded as multiple single-byte NOPs or a single multi-byte NOP.

Example 8: NOP in self-modifying code
```assembly
; Initially NOP, later replaced with actual instruction
NOP
; Self-modifying code writes MOV R1, #42 over the NOP
```

NOP provides a safe initial instruction that can be overwritten.

Example 9: NOP for cache line fill
```assembly
; Ensure loop occupies exactly one cache line
MOV R1, #0
loop:
ADD R1, #1
CMP R1, #100
BRANCH LT, loop
NOP   ; Pad to cache line boundary
```

NOPs can align loops within a single cache line.

Example 10: NOP for power management
```assembly
; Idle loop with NOPs
idle:
NOP
NOP
NOP
JMP idle
```

NOPs in an idle loop consume power; a HLT instruction is better for power saving.

---

### 11.10 HLT – Halt Core

The HLT (Halt) instruction stops the core until an interrupt occurs. The core enters a low-power state, reducing power consumption to near zero. When an interrupt is received, the core wakes up and executes the interrupt handler. After the interrupt handler returns, execution continues with the instruction following the HLT. HLT is used by the idle loop of the operating system.

**Encoding Format**

HLT uses opcode 0x7F. The instruction header contains opcode 0x7F, flags, and operand count of 0. The flags field has bit 8 for "stop granting" (disable bus master capability), bit 9 for "deep sleep" (deeper power savings, longer wakeup), and bits 10-15 reserved.

**Operation Details**

When HLT executes, the following steps occur. The processor core stops fetching and executing instructions. The clock to most of the core is gated, significantly reducing power. The cache and register file retain their state. The core monitors the interrupt controller for pending interrupts.

When an interrupt occurs, the core powers back up, saves its state, and jumps to the interrupt handler. After the interrupt handler executes IRET, execution resumes at the instruction after the HLT.

**Assembly Examples**

Example 1: Basic halt
```assembly
; Stop core until next interrupt
HLT
```

This is the idle loop for a core with no work.

Example 2: OS idle loop
```assembly
; Operating system idle loop
idle:
HLT
JMP idle   ; In case of spurious wakeup
```

The idle loop halts the core until an interrupt occurs.

Example 3: Halt with deep sleep
```assembly
; Deeper power savings (longer wakeup time)
HLT.DEEP
```

The .DEEP suffix saves more power but takes longer to wake up.

Example 4: Halt with bus disable
```assembly
; Stop granting bus requests (for I/O)
HLT.STOP
```

The .STOP suffix tells the bus controller not to grant requests to this core.

Example 5: Application idle waiting
```assembly
; Application waiting for event
wait:
CMP event_ready, #0
BRANCH EQ, wait
HLT   ; Not typically used by applications
```

Applications usually use yield or sleep system calls, not HLT.

Example 6: Halt in bootloader
```assembly
; Bootloader error: halt forever
error:
HLT
JMP error
```

A fatal error in the bootloader halts the core.

Example 7: Halt with wake-on-LAN
```assembly
; Configure for wake-on-LAN then halt
CFG_NETWORK_WOL #1   ; Enable wake-on-LAN
HLT
```

The core will wake up when a magic packet is received.

Example 8: Power management test
```assembly
; Test power consumption with HLT
; Measure current draw before and after
CALL measure_power
HLT
CALL measure_power   ; Should be much lower
```

HLT is used in power management testing.

Example 9: Halt in firmware
```assembly
; Firmware halts after POST if no boot device
no_boot_device:
HLT
JMP no_boot_device
```

Firmware uses HLT in error conditions.

Example 10: Halt with timer wakeup
```assembly
; Set timer for 1 second, then halt
CFG_TIMER #1000000000   ; Set timer for 1 second
HLT
; Core wakes up when timer expires
CALL on_timer_wakeup
```

A timer can be set to wake the core after a specified interval.

---

This concludes Chapter 11 and the complete Instruction Set Reference for the PIP CISC Unified Compute Platform.

The instruction set documented across these eleven chapters provides a complete programming model for the platform, from basic data movement and arithmetic to advanced vector processing, probabilistic inference, system management, interconnect, memory management, and protection. Each instruction has been specified with its encoding, operation, operands, and assembly examples sufficient for both compiler writers and assembly language programmers.

