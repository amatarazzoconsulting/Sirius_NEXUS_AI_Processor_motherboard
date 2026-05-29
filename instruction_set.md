# Sirius NEXUS AI Processor Gen5

## Volume 1: Complete Instruction Set Reference

# Sirius NEXUS AI Processor Gen5 - Complete Instruction Set Summary

## All 132 Instructions with Brief Function Descriptions

### Data Movement Instructions (5)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| MOV | dest, src | Copy data from source to destination |
| MOVSX | dest, src | Move with sign extension (small to large signed) |
| MOVZX | dest, src | Move with zero extension (small to large unsigned) |
| LEA | dest, [addr] | Load effective address (compute address without accessing memory) |
| XCHG | a, b | Atomically exchange two operands |

### Arithmetic Instructions (9)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| ADD | dest, src | dest = dest + src |
| SUB | dest, src | dest = dest - src |
| MUL | dest, src | Unsigned multiplication (dest = dest × src) |
| IMUL | dest, src | Signed multiplication |
| DIV | dest, src | Unsigned division (quotient in dest, remainder in R0) |
| IDIV | dest, src | Signed division |
| INC | dest | Increment by 1 |
| DEC | dest | Decrement by 1 |
| FMA | dest, a, b, c | Fused multiply-add: dest = (a × b) + c (single rounding) |

### Logic and Bit Instructions (9)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| AND | dest, src | Bitwise AND: dest = dest & src |
| OR | dest, src | Bitwise OR: dest = dest \| src |
| XOR | dest, src | Bitwise XOR: dest = dest ^ src |
| NOT | dest | Bitwise NOT: dest = ~dest |
| TEST | a, b | Bitwise AND, set flags only (no result stored) |
| BSF | dest, src | Bit scan forward: find lowest set bit index |
| BSR | dest, src | Bit scan reverse: find highest set bit index |
| SHL | dest, count | Shift left: dest = dest << count |
| SHR | dest, count | Shift right (logical): dest = dest >> count |

### Control Flow Instructions (4)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| JMP | target | Unconditional jump to target address |
| CALL | target | Call subroutine (pushes return address) |
| RET | (none) | Return from subroutine (pops return address) |
| BRANCH | cond, target | Conditional branch based on condition flags (EQ, NE, LT, LE, GT, GE, LO, LS, HI, HS, CS, CC, VS, VC, MI, PL) |

### Vector and SIMD Instructions (5)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| ADDPS | dest, src1, src2 | Add packed single-precision floats (element-wise) |
| MULPS | dest, src1, src2 | Multiply packed single-precision floats (element-wise) |
| DOT | dest, src1, src2 | Vector dot product: sum(src1[i] × src2[i]) |
| CONV | out, in, ker, dims, stride | 2D convolution using systolic array |
| SHUFPS | dest, src1, src2, mask | Shuffle elements from two vectors using mask |

### Advanced Math Functions (16)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| EXP | dest, src | Exponential: e^src |
| LOG | dest, src | Natural logarithm: ln(src) |
| LOG2 | dest, src | Base-2 logarithm: log₂(src) |
| LOG10 | dest, src | Base-10 logarithm: log₁₀(src) |
| POW | dest, base, exp | Power function: base^exp |
| SIN | dest, src | Trigonometric sine (radians) |
| COS | dest, src | Trigonometric cosine (radians) |
| TAN | dest, src | Trigonometric tangent (radians) |
| ARCTAN | dest, src | Inverse tangent (returns radians) |
| ARCTAN2 | dest, y, x | Two-argument inverse tangent |
| SQRT | dest, src | Square root: √src |
| RSQRT | dest, src | Reciprocal square root: 1/√src |
| ERF | dest, src | Error function (Gaussian integral) |
| ERFC | dest, src | Complementary error function: 1 - erf(src) |
| GAMMA | dest, src | Gamma function Γ(src) |
| LGAMMA | dest, src | Natural log of gamma function: ln(Γ(src)) |

### INT4 Inference Instructions (12)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| MATMULI4 | out, A, B, M, K, N | INT4 matrix multiplication: C = A × B (32-bit accumulate) |
| SOFTMAXI4 | dest, src | INT4 softmax (dequantize → FP16 softmax → quantize) |
| ATTENTIONI4 | out, Q, K, V, L, D | INT4 multi-head attention: softmax(Q×K^T/√d)×V |
| GELUI4 | dest, src | INT4 GELU activation using 16-entry lookup table |
| LAYERNORMI4 | out, in, params | INT4 layer normalization (mean, variance, scale, bias) |
| RESIDUALI4 | out, in, res | INT4 residual connection: out = in + res (FP16 addition) |
| MOVI4 | dest, src | Move packed INT4 data (4 values per 16-bit word) |
| PACKI4 | dest, src | Pack 8-bit integers to 4-bit with saturation |
| UNPACKI4 | dest, src | Unpack 4-bit to 8-bit with sign/zero extension |
| ADDI4 | dest, src1, src2 | INT4 vector addition with saturation |
| MULI4 | dest, src1, src2 | INT4 vector multiplication with saturation |
| DOTI4 | dest, src1, src2 | INT4 dot product with 32-bit accumulate |

### Probabilistic Inference Instructions (10)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| HMM_FORWARD | new, old, trans, emiss, scale | HMM forward algorithm step (sum over states) |
| HMM_VITERBI | new, old, trans, emiss, back | HMM Viterbi algorithm step (max over states) |
| HMM_BACKWARD | new, old, trans, emiss | HMM backward algorithm step |
| HMM_UPDATE | fwd, bwd, trans, emiss, acc | Baum-Welch expectation-maximization update |
| SOFTMAX | dest, src | Softmax function: e^x_i / Σ e^x_j |
| LOG_SUM_EXP | dest, src | Log of sum of exponentials: log(Σ e^x_i) |
| VECTOR_CONDITION | mask, src, cond | Test each vector element against condition, return mask |
| VECTOR_THRESHOLD | mask, src, thresh, cond | Compare vector to scalar threshold, return mask |
| LOG_SOFTMAX | dest, src | Log-softmax: log(e^x_i / Σ e^x_j) |
| SPARSE_DOT | dest, dense, idx, val | Sparse-dense dot product (non-zero elements only) |

### System Instructions (9)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| SYSENTER | (none) | Enter kernel mode (user→kernel, saves context) |
| SYSEXIT | (none) | Exit kernel mode (kernel→user, restores context) |
| IN | dest, port | Read byte/word/dword from I/O port |
| OUT | port, src | Write byte/word/dword to I/O port |
| CFG_VIDEO | tile, base, w, h, fmt, hz | Configure video output framebuffer |
| CFG_AUDIO | tile, buf, size, rate, bits, ch, map | Configure audio output circular buffer |
| RING_INIT | buf, seg, cnt, ctrl | Initialize hardware-managed circular buffer |
| RING_WRITE | ring, data, len | Write data to circular buffer |
| RING_SWAP | ring | Atomically swap read/write pointers (double-buffering) |

### Interconnect Instructions (9)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| MAP_STORAGE | chip, block, addr, size | Map NAND flash to memory address space |
| EXPORT_MEMORY | local, size, blade, remote, perm | Export local memory to remote blades |
| REMOTE_CALL | blade, func, argc, args, result | Execute function on remote blade |
| LINK_STATUS | blade, buffer | Query optical link health (signal, errors, bandwidth) |
| RACK_UNIFY | start, end, base, interleave | Unify rack blades into single shared memory |
| WARP_SYNC | warp | Synchronize 32 cores in a warp |
| REMOTE_ALLOC | blade, size, align | Allocate memory on remote blade |
| BROADCAST | (none) | Send instruction stream to all blades |
| BARRIER_SYNC | (none) | Global barrier synchronization (all cores, all blades) |

### Memory Management Instructions (7)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| SEGMENT_CREATE | parent, base, size, owner, perm, buf | Create new segment in segment tree |
| SEGMENT_DELETE | seg | Delete segment and all children |
| SEGMENT_MODIFY | seg, value, flag | Change segment permissions or owner |
| CAPABILITY_GRANT | seg, target, perm, exp, buf | Create cryptographically signed capability token |
| CAPABILITY_ACCEPT | token, name, buf | Import capability token, create local segment |
| SEGMENT_LOOKUP | addr/buf | Return segment descriptor for address or ID |
| TLB_INVALIDATE | addr/seg | Invalidate TLB entry (page, range, or all) |

### Protection Instructions (6)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| OWNER_GET | owner_buf, anc_buf | Get current owner ID and ancestor chain |
| OWNER_SET_PARENT | owner, parent | Set parent of owner in hierarchy (root only) |
| RING_SET | ring, owner | Map x86 ring number (0-3) to owner ID |
| IRQ_SET | irq, owner | Assign interrupt request line to owner |
| IO_MAP | phys, size, seg, perm | Map I/O device into segment tree |
| SEGMENT_WALK | addr, buf, max | Walk segment tree, return full path of descriptors |

### Register Type Mapping Instructions (4)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| SET_REG_MAP | bank, type, len, round | Set default register type and vector length |
| SET_REG_TYPE | reg, type | Set type for individual register (overrides default) |
| GET_REG_TYPE | reg, dest | Get current type of register |
| RESET_REG_MAP | bank | Reset register bank to default configuration |

### INT4 Memory Instructions (6) - From Addendum

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| MOVI4 | dest, src | Move packed INT4 data (4 values per 16-bit word) |
| PACKI4 | dest, src | Pack 8-bit integers to 4-bit with saturation |
| UNPACKI4 | dest, src | Unpack 4-bit to 8-bit with sign/zero extension |
| ADDI4 | dest, src1, src2 | INT4 vector addition with saturation |
| MULI4 | dest, src1, src2 | INT4 vector multiplication with saturation |
| DOTI4 | dest, src1, src2 | INT4 dot product with 32-bit accumulate |

### ROMB Instructions (4) - From Addendum

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| ROMB_INSERT | romb_addr, cache_line | Insert ROMB data directly into L1 cache |
| ROMB_IRQ | romb_addr, len, vector | Configure interrupt when ROMB data ready |
| ROMB_PRIORITY | module, priority | Set ROMB module priority for overlay system |
| ROMB_SELECT | module, base, size | Select ROMB module for address range |

### Transactional Memory Instructions (4)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| XBEGIN | handler | Start transaction, set fallback handler address |
| XEND | (none) | Commit transaction, make all writes visible |
| XABORT | code | Abort transaction, jump to handler with error code |
| XTEST | (none) | Test if currently in transaction (sets zero flag) |

### Variable Precision Vector Instructions (4)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| SET_PRECISION | vec, mask | Set precision mask for vector (per-element precision) |
| VADDP.VP | dest, src1, src2 | Vector add with variable precision (from mask) |
| VMULP.VP | dest, src1, src2 | Vector multiply with variable precision |
| VFMA.VP | dest, a, b, c | Vector FMA with variable precision |

### In-Memory Compute Instructions (4)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| MEM_SCAN | base, size, pattern, result | Scan memory region for pattern (executed in memory controller) |
| MEM_FILTER | base, size, pred, result | Filter records by predicate (executed in memory controller) |
| MEM_AGGREGATE | base, size, op, result | Aggregate (sum, count, min, max) in memory controller |
| MEM_BITMAP | base, size, pred, bitmap | Create bitmap of matching records |

### Compression Instructions (7)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| MEM_COMPRESS | src, dst, size | Compress memory region (predictor + entropy encoding) |
| MEM_DECOMPRESS | src, dst, size | Decompress memory region |
| DME_COPY_COMP | src, dst, size, mode | Copy and compress using DME |
| MEM_COMPRESS_STATS | base, size, buf | Get compression statistics (ratio, encoder used) |
| MEM_COMPRESS_ADAPT | src, dst, size | Adaptive compression with learned parameters |
| MEM_TRAIN_COMPRESS | data, size | Train compression neural network on representative data |
| MEM_ALLOC_COMPRESS_AWARE | size, ptr | Allocate memory optimized for compression |

### Parsing Instructions (HGPE) (7)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| PARSE | grammar, input, size, output | Parse input with BNF grammar, produce AST |
| PARSE_STREAM | grammar, stream, output | Streaming parse (continuous input) |
| PARSE_DEFINE_GRAMMAR | source, dest | Compile BNF grammar to hardware representation |
| PARSE_MATCH | pattern, input, size, result | Test pattern match (regex or literal) |
| AST_WALK | root, visitor, context | Traverse AST, call visitor function for each node |
| AST_QUERY | root, path, result | Query AST with JSONPath-style expression |
| AST_TRANSFORM | root, rules, output | Apply transformation rules to AST |

### Miscellaneous Instructions (4)

| Instruction | Parameters | Brief Function |
|-------------|------------|----------------|
| NOP | (none) | No operation (consumes 1 cycle) |
| CPUID | leaf | Return processor identification and feature info |
| RDTSC | (none) | Read 128-bit time-stamp counter (cycles since reset) |
| HLT | (none) | Halt core until interrupt |

---

## Summary Table

| Category | Number of Instructions |
|----------|------------------------|
| Data Movement | 5 |
| Arithmetic | 9 |
| Logic and Bit | 9 |
| Control Flow | 4 |
| Vector and SIMD | 5 |
| Advanced Math | 16 |
| INT4 Inference | 12 |
| Probabilistic Inference | 10 |
| System | 9 |
| Interconnect | 9 |
| Memory Management | 7 |
| Protection | 6 |
| Register Type Mapping | 4 |
| INT4 Memory (Addendum) | 6 |
| ROMB (Addendum) | 4 |
| Transactional Memory | 4 |
| Variable Precision Vectors | 4 |
| In-Memory Compute | 4 |
| Compression | 7 |
| Parsing (HGPE) | 7 |
| Miscellaneous | 4 |
| **Total** | **132** |

---

### Full Encoding, Assembly Examples, and Operand Specifications

This volume provides the complete instruction set specification for the Sirius NEXUS AI Processor Gen5. Each instruction is documented with its encoding across all three core types (Math, Logic, System), assembly syntax, operand types, numerical formats, and multiple usage examples. The instruction set is organized into 20 functional categories, with 132 instructions total.

---

# Section 1: Instruction Encoding Overview

The Sirius NEXUS instruction set uses variable-length encoding that differs by core type. Math cores use 8-bit opcodes with 20-bit headers and support vector operands. Logic cores use 7-bit opcodes with 12-bit headers and support only scalar operands. System cores use 6-bit opcodes with 8-bit headers and support only the most frequently used operations. The table below summarizes the encoding differences.

| Core Type | Opcode Bits | Header Bits | Max Operands | Avg Instruction Size | L1 I-cache Capacity |
|-----------|-------------|-------------|--------------|---------------------|---------------------|
| Math Core | 8 bits (0x00-0xFF) | 20 bits | 8 | 48 bits (6 bytes) | 5,461 instructions |
| Logic Core | 7 bits (0x00-0x7F) | 12 bits | 4 | 32 bits (4 bytes) | 16,384 instructions |
| System Core | 6 bits (0x00-0x3F) | 8 bits | 2 | 24 bits (3 bytes) | 10,922 instructions |

**Common Header Format (Math Core - 20 bits)**

| Bit Range | Field | Description |
|-----------|-------|-------------|
| 0-7 | Opcode | 8-bit operation code |
| 8-15 | Flags | Vector mode, saturation, rounding, etc. |
| 16-19 | Operand Count | Number of operands (0-15) |

**Common Header Format (Logic Core - 12 bits)**

| Bit Range | Field | Description |
|-----------|-------|-------------|
| 0-6 | Opcode | 7-bit operation code |
| 7-9 | Flags | Branch condition, etc. |
| 10-11 | Operand Count | Number of operands (0-3) |

**Common Header Format (System Core - 8 bits)**

| Bit Range | Field | Description |
|-----------|-------|-------------|
| 0-5 | Opcode | 6-bit operation code |
| 6-7 | Flags | Special operation flags |

**Operand Descriptor Format (16 bits - Math and Logic Cores)**

| Bit Range | Field | Values |
|-----------|-------|--------|
| 0-2 | Type | 0=register, 1=memory, 2=immediate, 3=remote, 4=vector |
| 3-5 | Size | 0=8-bit, 1=16-bit, 2=32-bit, 3=64-bit, 4=128-bit, 5=256-bit, 6=512-bit |
| 6-8 | Behavior | 0=input, 1=output, 2=input/output |
| 9-15 | Value | Register number, address mode, or immediate indicator |

**Operand Descriptor Format (8 bits - System Core)**

| Bit Range | Field | Values |
|-----------|-------|--------|
| 0-1 | Type | 0=register, 1=memory, 2=immediate |
| 2-4 | Size | 0=8-bit, 1=16-bit, 2=32-bit, 3=64-bit |
| 5-7 | Register | Register number (0-7) |

**Register Names by Core Type**

| Core Type | Registers | Names |
|-----------|-----------|-------|
| Math Core | 64 vector registers (512-bit) | V0-V63 |
| Math Core | 32 scalar registers (64-bit) | R0-R31 |
| Logic Core | 32 scalar registers (64-bit) | R0-R31 |
| System Core | 16 scalar registers (64-bit) | R0-R15 |

**Numerical Formats Supported**

| Format | Encoding | Bits | Range | Precision |
|--------|----------|------|-------|-----------|
| INT4 | Signed 4-bit integer | 4 | -8 to 7 | 1 bit |
| UINT4 | Unsigned 4-bit integer | 4 | 0 to 15 | 1 bit |
| INT8 | Signed 8-bit integer | 8 | -128 to 127 | 1 bit |
| UINT8 | Unsigned 8-bit integer | 8 | 0 to 255 | 1 bit |
| INT16 | Signed 16-bit integer | 16 | -32,768 to 32,767 | 1 bit |
| UINT16 | Unsigned 16-bit integer | 16 | 0 to 65,535 | 1 bit |
| INT32 | Signed 32-bit integer | 32 | -2.1e9 to 2.1e9 | 1 bit |
| UINT32 | Unsigned 32-bit integer | 32 | 0 to 4.3e9 | 1 bit |
| INT64 | Signed 64-bit integer | 64 | -9.2e18 to 9.2e18 | 1 bit |
| FP16 | IEEE 754 half-precision | 16 | ±65,504 | ~3.3 decimal digits |
| BF16 | Brain floating-point | 16 | ±3.4e38 | ~2.3 decimal digits |
| FP32 | IEEE 754 single-precision | 32 | ±3.4e38 | ~7.2 decimal digits |
| FP64 | IEEE 754 double-precision | 64 | ±1.8e308 | ~15.9 decimal digits |
| POSIT16 | Posit Type-III 16-bit | 16 | ±1.2e10 | ~4 decimal digits |
| POSIT32 | Posit Type-III 32-bit | 32 | ±1.0e76 | ~8 decimal digits |

---

# Section 2: Data Movement Instructions

## 2.1 MOV - Move Data

**Description:** Copies data from source to destination without modifying the source. Supports register-to-register, memory-to-register, register-to-memory, and immediate-to-register transfers.

**Math Core Encoding:** Opcode 0x01, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register or Memory | 8-512 bits | Destination location |
| Src | Register, Memory, or Immediate | 8-512 bits | Source location |

**Logic Core Encoding:** Opcode 0x01 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Opcode 0x01 (6-bit), 8-bit header, 2 operand descriptors

**Assembly Syntax:**
```
MOV destination, source
MOV.NT destination, source    ; Non-temporal (bypass cache)
MOV.REMOTE @blade:addr, source ; Move to remote blade
```

**Examples:**
```assembly
; Register to register
MOV R1, R2          ; Copy R2 to R1 (Math/Logic core)
MOV V1, V2          ; Copy vector V2 to V1 (Math core only)

; Immediate to register
MOV R1, #42         ; Load 42 into R1
MOV V1, #1.0        ; Load 1.0 into all elements of vector V1

; Memory to register
MOV R1, [R2]        ; Load from address in R2
MOV R1, [R2 + 64]   ; Load from address R2 + 64
MOV R1, [R2 + R3*8] ; Load from address R2 + R3*8

; Register to memory
MOV [R1], R2        ; Store R2 to address in R1
MOV.NT [R1], R2     ; Non-temporal store (bypass cache)

; Remote memory
MOV R1, @4:0x10000  ; Load from blade 4, address 0x10000
MOV @4:0x10000, R1  ; Store to blade 4, address 0x10000

; Memory-mapped flash
MOV R1, [0x100000000] ; Load from flash address
```

---

## 2.2 MOVSX - Move with Sign Extension

**Description:** Moves a smaller signed integer into a larger register, preserving the sign by replicating the most significant bit of the source across the upper bits of the destination.

**Math Core Encoding:** Opcode 0x02, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register | 16-512 bits | Destination must be larger than source |
| Src | Register, Memory, or Immediate | 8-128 bits | Source must be smaller than destination |

**Logic Core Encoding:** Opcode 0x02 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Assembly Syntax:**
```
MOVSX destination, source
MOVSX.S destination, source   ; Saturating sign extension
```

**Examples:**
```assembly
; Sign extend 8-bit to 32-bit
MOVSX R1, R2        ; R2 contains 8-bit signed value, R1 gets sign-extended 32-bit

; Sign extend from memory
MOVSX R1, [R2]      ; Load byte from address R2, sign extend to 32-bit

; Sign extend 16-bit to 64-bit
MOVSX R1, R2        ; R2 contains 16-bit signed value, R1 gets sign-extended 64-bit

; Saturating sign extension
MOVSX.S R1, R2      ; Clamp to min/max if overflow would occur

; Sign extend from immediate
MOVSX R1, #-42      ; Sign extend immediate -42 to 32-bit
```

---

## 2.3 MOVZX - Move with Zero Extension

**Description:** Moves a smaller unsigned integer into a larger register, filling the upper bits with zeros.

**Math Core Encoding:** Opcode 0x03, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register | 16-512 bits | Destination must be larger than source |
| Src | Register, Memory, or Immediate | 8-128 bits | Source must be smaller than destination |

**Logic Core Encoding:** Opcode 0x03 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Assembly Syntax:**
```
MOVZX destination, source
```

**Examples:**
```assembly
; Zero extend 8-bit to 32-bit
MOVZX R1, R2        ; R2 contains 8-bit value, R1 gets zero-extended 32-bit

; Zero extend from memory
MOVZX R1, [R2]      ; Load byte from address R2, zero extend to 32-bit

; Zero extend 16-bit to 64-bit
MOVZX R1, R2        ; R2 contains 16-bit value, R1 gets zero-extended 64-bit

; Zero extend from immediate
MOVZX R1, #255      ; Zero extend immediate 255 to 32-bit
```

---

## 2.4 LEA - Load Effective Address

**Description:** Computes a memory address without accessing memory and stores the address in a register. Can perform addition and scaling in a single instruction.

**Math Core Encoding:** Opcode 0x04, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register | 64-bit | Destination for computed address |
| Src | Memory expression | N/A | Address expression (evaluated, not accessed) |

**Logic Core Encoding:** Opcode 0x04 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Opcode 0x02 (6-bit), 8-bit header, 2 operand descriptors

**Assembly Syntax:**
```
LEA destination, [address expression]
LEA destination, @blade:address   ; Remote address descriptor
```

**Examples:**
```assembly
; Simple address copy
LEA R1, [R2]        ; R1 = R2

; Add constant to register
LEA R1, [R2 + 64]   ; R1 = R2 + 64

; Add two registers
LEA R1, [R2 + R3]   ; R1 = R2 + R3

; Add with scaling (array indexing)
LEA R1, [R2 + R3*8] ; R1 = R2 + (R3 * 8)

; Three-operand addition
LEA R1, [R2 + R3 + 64]  ; R1 = R2 + R3 + 64

; Address of array element
LEA R1, [array_base + R2*4]  ; R1 = array_base + (R2 * 4)

; Remote address descriptor
LEA R1, @4:0x10000  ; R1 = remote address descriptor for blade 4
```

---

## 2.5 XCHG - Exchange Data

**Description:** Atomically exchanges the contents of two operands. The exchange is indivisible with respect to other cores and DMA devices.

**Math Core Encoding:** Opcode 0x05, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register or Memory | 8-512 bits | First operand (receives second's value) |
| Src | Register or Memory | 8-512 bits | Second operand (receives first's value) |

**Logic Core Encoding:** Opcode 0x05 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Opcode 0x03 (6-bit), 8-bit header, 2 operand descriptors

**Assembly Syntax:**
```
XCHG operand1, operand2
XCHG.A operand1, operand2    ; Acquire-release semantics
XCHG.R operand1, operand2    ; Relaxed semantics
XCHG.B operand1, operand2    ; Byte exchange (size override)
```

**Examples:**
```assembly
; Exchange register with memory (spinlock acquire)
XCHG R1, [lock]     ; Atomically exchange R1 with lock variable

; Exchange two registers
XCHG R1, R2         ; Swap R1 and R2

; Exchange with acquire-release semantics
XCHG.A R1, [lock]   ; All previous memory ops complete before exchange

; Byte exchange
XCHG.B R1, [R2]     ; Exchange single byte

; Double-word exchange
XCHG R1, [R2]       ; Exchange 64-bit value

; Remote memory exchange
XCHG R1, @4:0x10000 ; Exchange with memory on blade 4
```

---

# Section 3: Arithmetic Instructions

## 3.1 ADD - Add Operands

**Description:** Performs binary addition of two operands and stores the result in the destination. Supports scalar, vector, and saturating modes.

**Math Core Encoding:** Opcode 0x10, 20-bit header, 2-3 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register or Memory | 8-512 bits | Destination (receives sum) |
| Src | Register, Memory, or Immediate | 8-512 bits | Source to add |
| Optional Src2 | Register, Memory, or Immediate | 8-512 bits | Second source (vector mode) |

**Logic Core Encoding:** Opcode 0x10 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Opcode 0x04 (6-bit), 8-bit header, 2 operand descriptors

**Flags Updated:** ZF (zero), SF (sign), CF (carry), OF (overflow)

**Assembly Syntax:**
```
ADD dest, src
ADD.V dest, src1, src2    ; Vector element-wise add
ADD.S dest, src           ; Saturating add
ADD.C dest, src           ; Add with carry (from previous operation)
```

**Examples:**
```assembly
; Simple integer addition
ADD R1, R2          ; R1 = R1 + R2

; Addition with immediate
ADD R1, #42         ; R1 = R1 + 42

; Addition from memory
ADD R1, [R2]        ; R1 = R1 + value at address R2

; Vector addition
ADD.V V1, V2, V3    ; V1[i] = V2[i] + V3[i] for all i

; Broadcast scalar to vector
ADD.V V1, V2, #1    ; V1[i] = V2[i] + 1 for all i

; Saturating addition (clamps on overflow)
ADD.S R1, R2        ; R1 = saturate(R1 + R2)

; Add with carry (multi-precision)
ADD R1, R2          ; Add low 64 bits, sets carry flag
ADD.C R3, R4        ; Add high 64 bits with carry

; Remote memory addition
ADD R1, @4:0x10000  ; R1 = R1 + value at remote address
```

---

## 3.2 SUB - Subtract Operands

**Description:** Performs binary subtraction (dest - src) and stores the result in the destination.

**Math Core Encoding:** Opcode 0x11, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register or Memory | 8-512 bits | Destination (receives difference) |
| Src | Register, Memory, or Immediate | 8-512 bits | Source to subtract |

**Logic Core Encoding:** Opcode 0x11 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Opcode 0x05 (6-bit), 8-bit header, 2 operand descriptors

**Flags Updated:** ZF (zero), SF (sign), CF (borrow), OF (overflow)

**Assembly Syntax:**
```
SUB dest, src
SUB.V dest, src1, src2    ; Vector element-wise subtract
SUB.S dest, src           ; Saturating subtract
SUB.C dest, src           ; Subtract with borrow
```

**Examples:**
```assembly
; Simple integer subtraction
SUB R1, R2          ; R1 = R1 - R2

; Subtraction with immediate
SUB R1, #42         ; R1 = R1 - 42

; Pointer subtraction (difference in bytes)
SUB R1, R2          ; R1 = R1 - R2 (distance between pointers)

; Vector subtraction (image differencing)
SUB.V V1, V2, V3    ; V1[i] = V2[i] - V3[i]

; Saturating subtraction (clamps on underflow)
SUB.S R1, R2        ; R1 = saturate(R1 - R2)

; Subtract with borrow (multi-precision)
SUB R1, R2          ; Subtract low 64 bits, sets borrow flag
SUB.C R3, R4        ; Subtract high 64 bits with borrow
```

---

## 3.3 MUL - Multiply Unsigned

**Description:** Performs unsigned multiplication of two operands. The product is stored in a destination that must be twice the width of the operands.

**Math Core Encoding:** Opcode 0x12, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register | 2× operand width | Destination for product |
| Src | Register, Memory, or Immediate | 8-256 bits | Multiplier |

**Logic Core Encoding:** Opcode 0x12 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Flags Updated:** ZF (zero), SF (sign of high word), CF (if product exceeds dest width)

**Assembly Syntax:**
```
MUL dest, src
MUL.V dest, src1, src2    ; Vector element-wise multiply
```

**Examples:**
```assembly
; Simple unsigned multiplication
MUL R1, R2          ; R1 = R1 * R2 (unsigned)

; Multiplication with immediate
MUL R1, #10         ; R1 = R1 * 10

; Multiplication with memory operand
MUL R1, [R2]        ; R1 = R1 * value at address R2

; Vector multiplication (element-wise)
MUL.V V1, V2, V3    ; V1[i] = V2[i] * V3[i]

; Square calculation
MUL R1, R1          ; R1 = R1 * R1 (square)

; Scaling for fixed-point arithmetic
MUL R1, #65536      ; Scale by 2^16
SHR R1, R1, #16     ; Extract high 16 bits

; Remote multiplication
MUL R1, @4:0x10000  ; R1 = R1 * remote value
```

---

## 3.4 IMUL - Multiply Signed

**Description:** Performs signed multiplication of two operands using two's complement arithmetic.

**Math Core Encoding:** Opcode 0x13, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register | 2× operand width | Destination for product |
| Src | Register, Memory, or Immediate | 8-256 bits | Multiplier (signed) |

**Logic Core Encoding:** Opcode 0x13 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Flags Updated:** ZF (zero), SF (sign of high word), CF (if product exceeds dest width), OF (signed overflow)

**Assembly Syntax:**
```
IMUL dest, src
IMUL.V dest, src1, src2   ; Vector element-wise signed multiply
```

**Examples:**
```assembly
; Simple signed multiplication
IMUL R1, R2         ; R1 = R1 * R2 (signed)

; Multiplication with negative immediate
IMUL R1, #-10       ; R1 = R1 * (-10)

; Vector signed multiplication
IMUL.V V1, V2, V3   ; V1[i] = V2[i] * V3[i] (signed)
```

---

## 3.5 DIV - Divide Unsigned

**Description:** Performs unsigned division of a 64-bit dividend by a 32-bit divisor, producing a 32-bit quotient and a 32-bit remainder.

**Math Core Encoding:** Opcode 0x14, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dividend | Register pair | 64-bit | High word in R1, low word in R0 |
| Divisor | Register or Memory | 32-bit | Divisor |

**Logic Core Encoding:** Opcode 0x14 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Flags Updated:** ZF (zero quotient), CF (division by zero)

**Assembly Syntax:**
```
DIV dividend_high, divisor    ; Quotient in dividend_high, remainder in R0
```

**Examples:**
```assembly
; Simple unsigned division
DIV R1, R2          ; Divide (R1,R0) by R2, quotient in R1, remainder in R0

; Division of 32-bit value
MOVZX R1, R3        ; Zero-extend 32-bit to 64-bit in (R1,R0)
DIV R1, R2          ; Divide by 32-bit divisor

; Division with memory operand
DIV R1, [R2]        ; Divide by divisor at address R2

; Check divisibility
DIV R1, R2          ; Divide
CMP R0, #0          ; Check remainder
BRANCH EQ, divisible ; Branch if remainder is zero

; Convert seconds to minutes and seconds
MOV R1, seconds     ; Dividend in (R1,R0)
MOV R2, #60         ; Divisor = 60
DIV R1, R2          ; Quotient = minutes, remainder = seconds
```

---

## 3.6 IDIV - Divide Signed

**Description:** Performs signed division using two's complement arithmetic.

**Math Core Encoding:** Opcode 0x15, 20-bit header, 2 operand descriptors

**Logic Core Encoding:** Opcode 0x15 (7-bit), 12-bit header, 2 operand descriptors

**Assembly Syntax:**
```
IDIV dividend_high, divisor   ; Quotient in dividend_high, remainder in R0
```

**Examples:**
```assembly
; Signed division
IDIV R1, R2         ; Divide signed (R1,R0) by signed R2

; Check for negative remainder
IDIV R1, R2
CMP R0, #0
BRANCH LT, negative_remainder
```

---

## 3.7 INC - Increment

**Description:** Increments the operand by one.

**Math Core Encoding:** Opcode 0x16, 20-bit header, 1 operand descriptor

**Logic Core Encoding:** Opcode 0x16 (7-bit), 12-bit header, 1 operand descriptor

**System Core Encoding:** Opcode 0x06 (6-bit), 8-bit header, 1 operand descriptor

**Flags Updated:** ZF, SF, OF (carry flag unchanged)

**Assembly Syntax:**
```
INC operand
```

**Examples:**
```assembly
; Increment register
INC R1              ; R1 = R1 + 1

; Increment memory
INC [R1]            ; Increment value at address R1

; Loop counter
MOV R1, #0
loop:
    INC R1
    CMP R1, #100
    BRANCH LT, loop
```

---

## 3.8 DEC - Decrement

**Description:** Decrements the operand by one.

**Math Core Encoding:** Opcode 0x17, 20-bit header, 1 operand descriptor

**Logic Core Encoding:** Opcode 0x17 (7-bit), 12-bit header, 1 operand descriptor

**System Core Encoding:** Opcode 0x07 (6-bit), 8-bit header, 1 operand descriptor

**Flags Updated:** ZF, SF, OF (carry flag unchanged)

**Assembly Syntax:**
```
DEC operand
```

**Examples:**
```assembly
; Decrement register
DEC R1              ; R1 = R1 - 1

; Decrement memory
DEC [R1]            ; Decrement value at address R1

; Loop counter (count down)
MOV R1, #100
loop:
    DEC R1
    BRANCH NE, loop
```

---

## 3.9 FMA - Fused Multiply-Add

**Description:** Performs fused multiply-add: dest = (a × b) + c with a single rounding. This is more accurate than separate multiply and add instructions.

**Math Core Encoding:** Opcode 0x18, 20-bit header, 4 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register | 16-512 bits | Destination for result |
| A | Register, Memory, or Immediate | 16-512 bits | Multiplier |
| B | Register, Memory, or Immediate | 16-512 bits | Multiplicand |
| C | Register, Memory, or Immediate | 16-512 bits | Addend |

**Logic Core Encoding:** Not available

**System Core Encoding:** Not available

**Flags Updated:** ZF, SF, OF

**Assembly Syntax:**
```
FMA dest, a, b, c
FMA.V dest, a, b, c    ; Vector element-wise FMA
FMA.RZ dest, a, b, c   ; Round toward zero
FMA.RU dest, a, b, c   ; Round up
FMA.RD dest, a, b, c   ; Round down
```

**Examples:**
```assembly
; Simple FMA
FMA R1, R2, R3, R4   ; R1 = (R2 * R3) + R4

; FMA with immediate addend
FMA R1, R2, R3, #1.0 ; R1 = (R2 * R3) + 1.0

; Dot product using FMA in a loop
MOV R1, #0           ; Initialize accumulator
MOV R2, #0           ; Initialize index
loop:
    FMA R1, [R3+R2], [R4+R2], R1   ; accumulator += a[i] * b[i]
    ADD R2, #8
    CMP R2, #size
    BRANCH LT, loop

; Polynomial evaluation (Horner's method)
FMA R1, x, a, b      ; R1 = a*x + b
FMA R1, R1, x, c     ; R1 = (a*x + b)*x + c
FMA R1, R1, x, d     ; R1 = (a*x^2 + b*x + c)*x + d

; Vector FMA for neural network layer
FMA.V V1, V2, V3, V4 ; V1[i] = (V2[i] * V3[i]) + V4[i] for all i

; Complex multiplication using FMA
; Multiply (a + i*b) by (c + i*d) = (a*c - b*d) + i*(a*d + b*c)
FMA real, a, c, neg_b_d    ; real = a*c + (-b*d)
FMA imag, a, d, b_c        ; imag = a*d + b*c
```

---

# Section 4: Logic and Bit Instructions

## 4.1 AND - Bitwise Logical AND

**Description:** Performs bitwise AND between two operands. Each result bit is 1 only if both corresponding source bits are 1.

**Math Core Encoding:** Opcode 0x20, 20-bit header, 2 operand descriptors

**Logic Core Encoding:** Opcode 0x20 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Opcode 0x08 (6-bit), 8-bit header, 2 operand descriptors

**Flags Updated:** ZF, SF (CF and OF cleared)

**Assembly Syntax:**
```
AND dest, src
AND.V dest, src1, src2    ; Vector element-wise AND
```

**Examples:**
```assembly
; Simple bitwise AND
AND R1, R2          ; R1 = R1 & R2

; Masking with immediate (keep low 8 bits)
AND R1, #0xFF       ; R1 = R1 & 0xFF

; Clearing specific bits
AND R1, #0xFFFFFF00 ; Clear low 8 bits of R1

; Test if value is zero (without modifying)
AND R1, R1          ; Sets flags, R1 unchanged

; Aligning memory addresses to 16-byte boundary
AND R1, #0xFFFFFFF0 ; Round down to multiple of 16

; Vector bitwise AND
AND.V V1, V2, V3    ; V1[i] = V2[i] & V3[i] for all i
```

---

## 4.2 OR - Bitwise Logical OR

**Description:** Performs bitwise OR between two operands. Each result bit is 1 if at least one corresponding source bit is 1.

**Math Core Encoding:** Opcode 0x21, 20-bit header, 2 operand descriptors

**Logic Core Encoding:** Opcode 0x21 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Opcode 0x09 (6-bit), 8-bit header, 2 operand descriptors

**Flags Updated:** ZF, SF (CF and OF cleared)

**Assembly Syntax:**
```
OR dest, src
OR.V dest, src1, src2     ; Vector element-wise OR
```

**Examples:**
```assembly
; Simple bitwise OR
OR R1, R2           ; R1 = R1 | R2

; Setting specific bits (set low 4 bits to 1)
OR R1, #0x0F        ; R1 = R1 | 0x0F

; Combining flag registers
OR R1, R2           ; Combine error flags

; Convert binary digit to ASCII
OR R1, #0x30        ; Convert 0-9 to '0'-'9'

; Force value to be odd
OR R1, #1           ; R1 = R1 | 1 (set low bit)

; Vector bitwise OR
OR.V V1, V2, V3     ; V1[i] = V2[i] | V3[i] for all i
```

---

## 4.3 XOR - Bitwise Exclusive OR

**Description:** Performs bitwise XOR between two operands. Each result bit is 1 if the corresponding source bits are different.

**Math Core Encoding:** Opcode 0x22, 20-bit header, 2 operand descriptors

**Logic Core Encoding:** Opcode 0x22 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Opcode 0x0A (6-bit), 8-bit header, 2 operand descriptors

**Flags Updated:** ZF, SF (CF and OF cleared)

**Assembly Syntax:**
```
XOR dest, src
XOR.V dest, src1, src2    ; Vector element-wise XOR
```

**Examples:**
```assembly
; Simple bitwise XOR
XOR R1, R2          ; R1 = R1 ^ R2

; Zero a register (fastest method)
XOR R1, R1          ; R1 = 0

; Toggle specific bits
XOR R1, #0x0F       ; Toggle low 4 bits of R1

; Simple XOR encryption/decryption
XOR R1, key         ; Encrypt
; ... later ...
XOR R1, key         ; Decrypt back to original

; Swap registers without temporary
XOR R1, R2          ; R1 = R1 ^ R2
XOR R2, R1          ; R2 = R2 ^ R1 (now R2 holds original R1)
XOR R1, R2          ; R1 = R1 ^ R2 (now R1 holds original R2)

; Check if two values are equal
XOR R1, R2
BRANCH EQ, equal    ; Branch if R1 == R2

; Gray code conversion
; gray = binary ^ (binary >> 1)
MOV R2, R1
SHR R2, R2, #1
XOR R1, R2          ; R1 now contains Gray code
```

---

## 4.4 NOT - Bitwise Logical NOT

**Description:** Performs bitwise NOT (one's complement) on a single operand, inverting every bit.

**Math Core Encoding:** Opcode 0x23, 20-bit header, 1 operand descriptor

**Logic Core Encoding:** Opcode 0x23 (7-bit), 12-bit header, 1 operand descriptor

**System Core Encoding:** Not available

**Flags Updated:** ZF, SF (CF and OF cleared)

**Assembly Syntax:**
```
NOT operand
NOT.V dest, src         ; Vector element-wise NOT
```

**Examples:**
```assembly
; Simple bitwise NOT
NOT R1              ; R1 = ~R1

; Two's complement negation
NOT R1
ADD R1, #1          ; R1 = -R1 (two's complement)

; Create mask of all ones
XOR R1, R1          ; R1 = 0
NOT R1              ; R1 = all ones

; Invert vector element-wise
NOT.V V1, V2        ; V1[i] = ~V2[i] for all i

; Compute NAND (NOT AND)
AND R1, R2
NOT R1              ; R1 = ~(R1 & R2)
```

---

## 4.5 TEST - Test Bits

**Description:** Performs bitwise AND between two operands but does not store the result; only updates condition flags.

**Math Core Encoding:** Opcode 0x24, 20-bit header, 2 operand descriptors

**Logic Core Encoding:** Opcode 0x24 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Flags Updated:** ZF, SF (CF and OF cleared)

**Assembly Syntax:**
```
TEST operand1, operand2
```

**Examples:**
```assembly
; Test a single bit
TEST R1, #0x04      ; Test bit 2 of R1
BRANCH NE, bit_set   ; Branch if bit is set

; Test multiple bits (any set)
TEST R1, #0x0F      ; Test low 4 bits
BRANCH Z, none_set   ; Branch if none are set

; Test sign bit
TEST R1, #0x80000000 ; Test most significant bit
BRANCH NE, negative  ; Branch if negative

; Test for even/odd
TEST R1, #1         ; Test low bit
BRANCH Z, even      ; Branch if even

; Test memory value
TEST [R1], #0x80    ; Test high bit of byte at address R1
BRANCH NE, high_bit_set

; Test using register mask
TEST R1, R2         ; Test bits in R1 specified by mask in R2
BRANCH Z, no_bits_set
```

---

## 4.6 BSF - Bit Scan Forward

**Description:** Finds the index of the least significant set bit (lowest bit position containing a 1).

**Math Core Encoding:** Opcode 0x30, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Register | 64-bit | Receives bit index (0 = LSB) |
| Src | Register or Memory | 16-512 bits | Value to scan |

**Logic Core Encoding:** Opcode 0x30 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Flags Updated:** ZF (set if source is zero)

**Assembly Syntax:**
```
BSF destination, source
BSF.P1 destination, source   ; Return index + 1
```

**Examples:**
```assembly
; Find lowest set bit
BSF R1, R2          ; R1 = index of lowest set bit in R2
BRANCH Z, no_bits   ; Branch if R2 was zero

; Iterate over set bits
loop:
    BSF R1, R2
    BRANCH Z, done
    ; Process bit at position R1
    XOR R2, #1<<R1  ; Clear that bit
    JMP loop

; Count trailing zeros (ctz) - same as BSF
BSF R1, R2          ; R1 = number of trailing zeros

; Find first free bit in bitmap
BSF R1, [bitmap]    ; Find first free bit (if 0=free, 1=allocated)
```

---

## 4.7 BSR - Bit Scan Reverse

**Description:** Finds the index of the most significant set bit (highest bit position containing a 1).

**Math Core Encoding:** Opcode 0x31, 20-bit header, 2 operand descriptors

**Logic Core Encoding:** Opcode 0x31 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Flags Updated:** ZF (set if source is zero)

**Assembly Syntax:**
```
BSR destination, source
```

**Examples:**
```assembly
; Find highest set bit
BSR R1, R2          ; R1 = index of highest set bit in R2

; Compute floor of binary logarithm (log2)
BSR R1, R2          ; R1 = floor(log2(R2))

; Find next power of two
BSR R1, R2
ADD R1, #1
MOV R3, #1
SHL R3, R3, R1      ; R3 = 2^(floor(log2(R2))+1)

; Normalize floating-point mantissa
BSR R1, R2          ; Find highest set bit in mantissa
SUB R1, #23         ; Subtract mantissa width
SHL R2, R2, R1      ; Shift to normalize

; Count leading zeros
BSR R1, R2
SUB R1, #31, R1     ; Leading zeros = 31 - floor(log2(R2))
```

---

## 4.8 SHL - Shift Left

**Description:** Shifts bits left; zeros are shifted into LSB positions.

**Math Core Encoding:** Opcode 0x36, 20-bit header, 2 operand descriptors

**Logic Core Encoding:** Opcode 0x36 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Flags Updated:** ZF, SF, CF (last bit shifted out), OF

**Assembly Syntax:**
```
SHL dest, count
SHL.V dest, src, count    ; Vector shift left
SHL.S dest, count         ; Saturating shift left
```

**Examples:**
```assembly
; Simple shift left (multiply by power of two)
SHL R1, #3          ; R1 = R1 << 3 = R1 * 8

; Shift left by variable amount
SHL R1, R2          ; R1 = R1 << (R2 & 0x3F)

; Extract bit field (shift to top, then shift back)
SHL R1, #16         ; Shift field to top
SHR R1, #16         ; Shift back to bottom

; Build value from fields
SHL R1, #16         ; Shift field 1 to high word
OR R1, R2           ; OR in field 2 (low word)

; Vector shift left
SHL.V V1, V2, #2    ; Each element of V1 = element of V2 << 2

; Power-of-two multiplication (much faster than MUL)
SHL R1, #10         ; R1 = R1 * 1024

; Shift left with carry detection
SHL R1, #1
BRANCH CS, overflow ; Branch if high bit was set before shift
```

---

## 4.9 SHR - Shift Right

**Description:** Shifts bits right; zeros are shifted into MSB positions (logical shift).

**Math Core Encoding:** Opcode 0x37, 20-bit header, 2 operand descriptors

**Logic Core Encoding:** Opcode 0x37 (7-bit), 12-bit header, 2 operand descriptors

**System Core Encoding:** Not available

**Flags Updated:** ZF, SF (cleared), CF (last bit shifted out)

**Assembly Syntax:**
```
SHR dest, count
SHR.V dest, src, count    ; Vector shift right
```

**Examples:**
```assembly
; Simple shift right (unsigned division by power of two)
SHR R1, #3          ; R1 = R1 >> 3 = R1 / 8 (unsigned)

; Extract high 16 bits
SHR R1, #16         ; Shift high bits to low position

; Unsigned division by power of two
SHR R1, #10         ; R1 = R1 / 1024 (unsigned)

; Align pointer to cache line (round down)
SHR R1, #6          ; Divide by 64
SHL R1, #6          ; Multiply by 64

; Vector shift right
SHR.V V1, V2, #2    ; Each element of V1 = element of V2 >> 2

; Extract bit field from the right
SHR R1, #3          ; Shift field to low bits
AND R1, #0x1F       ; Mask to 5 bits

; Convert fixed-point to integer (discard fractional part)
SHR R1, #16         ; R1 = R1 / 65536 (integer part only)

; Shift right with carry detection (test low bit)
SHR R1, #1
BRANCH CS, odd      ; Branch if low bit was set
```

---

# Section 5: Control Flow Instructions

## 5.1 JMP - Unconditional Jump

**Description:** Transfers execution control to a specified address unconditionally.

**Math Core Encoding:** Opcode 0x40, 20-bit header, 1 operand descriptor

**Logic Core Encoding:** Opcode 0x40 (7-bit), 12-bit header, 1 operand descriptor

**System Core Encoding:** Opcode 0x10 (6-bit), 8-bit header, 1 operand descriptor

**Assembly Syntax:**
```
JMP target
JMP.S target        ; Short jump (8-bit offset)
JMP.N target        ; Near jump (32-bit offset)
JMP.FAR segment:offset ; Far jump (segment change)
JMP R1              ; Jump through register
JMP [R1]            ; Jump through memory
JMP @4:0x10000      ; Remote jump to blade 4
```

**Examples:**
```assembly
; Direct jump to label
JMP target_label

; Infinite loop
loop:
    JMP loop

; Jump through register (function pointer)
JMP R1              ; Jump to address in R1

; Jump through memory (virtual function table)
JMP [R1]            ; Load target from memory at R1, then jump

; Short jump (2 bytes, limited range)
JMP.S short_target

; Far jump to different code segment
JMP.FAR 0x08:0x10000

; Remote jump
JMP @4:0x10000      ; Jump to code on blade 4
```

---

## 5.2 CALL - Call Subroutine

**Description:** Transfers control to a subroutine while saving the return address on the hardware return stack.

**Math Core Encoding:** Opcode 0x41, 20-bit header, 1 operand descriptor

**Logic Core Encoding:** Opcode 0x41 (7-bit), 12-bit header, 1 operand descriptor

**System Core Encoding:** Opcode 0x11 (6-bit), 8-bit header, 1 operand descriptor

**Assembly Syntax:**
```
CALL target
CALL R1             ; Call through register
CALL [R1]           ; Call through memory
CALL.FAR segment:offset ; Far call
CALL @4:0x10000     ; Remote call
```

**Examples:**
```assembly
; Simple subroutine call
CALL subroutine
; Returns here after subroutine completes

; Call through register (function pointer)
CALL R1             ; Call function at address in R1

; Call through memory (virtual function)
CALL [R1]           ; Load address from memory at R1, then call

; Nested calls (return stack handles them)
CALL outer
; ... returns here after outer and inner complete
outer:
    CALL inner
    RET
inner:
    RET

; Tail call optimization (replace CALL+RET with JMP)
; Instead of:
CALL subroutine
RET
; Use:
JMP subroutine

; Remote procedure call
CALL @4:0x10000     ; Call function on blade 4
```

---

## 5.3 RET - Return from Subroutine

**Description:** Returns control from a subroutine by popping the return address from the hardware return stack.

**Math Core Encoding:** Opcode 0x42, 20-bit header, 0 operand descriptors

**Logic Core Encoding:** Opcode 0x42 (7-bit), 12-bit header, 0 operand descriptors

**System Core Encoding:** Opcode 0x12 (6-bit), 8-bit header, 0 operand descriptors

**Assembly Syntax:**
```
RET
RET.FAR             ; Far return (segment change)
RET #8              ; Return and pop 8 bytes from stack
RET.I               ; Return from interrupt
```

**Examples:**
```assembly
; Simple return
subroutine:
    ; ... do work ...
    RET

; Far return (kernel to user)
kernel_entry:
    ; ... kernel code ...
    RET.FAR

; Return with argument cleanup (callee cleans stack)
subroutine:
    ; ... uses 8 bytes of stack arguments ...
    RET #8          ; Return and pop 8 argument bytes

; Return from interrupt handler
interrupt_handler:
    ; ... save context, handle interrupt, restore context ...
    RET.I           ; Restores saved flags

; Leaf function return (no nested calls)
leaf_function:
    ADD R1, R1, #1
    RET
```

---

## 5.4 BRANCH - Conditional Branch

**Description:** Transfers control to a target address if a specified condition is true based on the condition flags.

**Math Core Encoding:** Opcode 0x43, 20-bit header, 1 operand descriptor

**Logic Core Encoding:** Opcode 0x43 (7-bit), 12-bit header, 1 operand descriptor

**System Core Encoding:** Not available

**Condition Codes:**

| Code | Mnemonic | Condition | Flags Tested |
|------|----------|-----------|--------------|
| 0x0 | EQ | Equal | ZF = 1 |
| 0x1 | NE | Not equal | ZF = 0 |
| 0x2 | LT | Signed less than | SF != OF |
| 0x3 | LE | Signed less or equal | ZF = 1 or SF != OF |
| 0x4 | GT | Signed greater than | ZF = 0 and SF = OF |
| 0x5 | GE | Signed greater or equal | SF = OF |
| 0x6 | LO | Unsigned lower | CF = 1 |
| 0x7 | LS | Unsigned lower or same | CF = 1 or ZF = 1 |
| 0x8 | HI | Unsigned higher | CF = 0 and ZF = 0 |
| 0x9 | HS | Unsigned higher or same | CF = 0 |
| 0xA | CS | Carry set | CF = 1 |
| 0xB | CC | Carry clear | CF = 0 |
| 0xC | VS | Overflow set | OF = 1 |
| 0xD | VC | Overflow clear | OF = 0 |
| 0xE | MI | Negative (minus) | SF = 1 |
| 0xF | PL | Positive or zero (plus) | SF = 0 |

**Assembly Syntax:**
```
BRANCH condition, target
BRANCH.PT condition, target  ; Predict taken
BRANCH.PN condition, target  ; Predict not taken
```

**Examples:**
```assembly
; Branch if equal
CMP R1, R2
BRANCH EQ, equal_label

; Branch if greater than (signed)
CMP R1, R2
BRANCH GT, greater_label

; Branch if less than (unsigned)
CMP R1, R2
BRANCH LO, lower_label

; Loop with conditional branch
MOV R1, #0
loop:
    ADD R1, #1
    CMP R1, #100
    BRANCH LT, loop

; If-then-else structure
CMP R1, R2
BRANCH EQ, then_case
else_case:
    ; ... else code ...
    JMP end_if
then_case:
    ; ... then code ...
end_if:

; Short-circuit evaluation
CMP R1, #0
BRANCH EQ, short_circuit
CMP R2, #0
BRANCH EQ, short_circuit
; both non-zero

; Branch with prediction hints
BRANCH.PT EQ, likely_taken   ; Hint: predict taken
BRANCH.PN EQ, unlikely_taken ; Hint: predict not taken
```

---

# Section 6: Vector and SIMD Instructions

## 6.1 ADDPS - Add Packed Single-Precision

**Description:** Performs element-wise addition of packed single-precision floating-point values.

**Math Core Encoding:** Opcode 0x50, 20-bit header, 3 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Vector register | 128-1024 bits | Destination for results |
| Src1 | Vector register or memory | 128-1024 bits | First source vector |
| Src2 | Vector register or memory | 128-1024 bits | Second source vector |

**Assembly Syntax:**
```
ADDPS dest, src1, src2
ADDPS.Y dest, src1, src2   ; 256-bit (8 floats)
ADDPS.Z dest, src1, src2   ; 512-bit (16 floats)
ADDPS.K dest, src1, src2, mask ; Masked addition
```

**Examples:**
```assembly
; Add two 128-bit vectors (4 floats)
ADDPS XMM1, XMM2, XMM3   ; XMM1 = XMM2 + XMM3

; Add 256-bit vectors (8 floats)
ADDPS.Y YMM1, YMM2, YMM3

; Add 512-bit vectors (16 floats)
ADDPS.Z ZMM1, ZMM2, ZMM3

; Add vector from memory
ADDPS XMM1, XMM2, [R1]   ; XMM1 = XMM2 + memory at R1

; Add broadcast scalar to vector
ADDPS XMM1, XMM2, XMM3_S ; Broadcast XMM3[0] to all lanes

; Masked vector addition (mask in K1 register)
ADDPS.K ZMM1, ZMM2, ZMM3, K1
```

---

## 6.2 MULPS - Multiply Packed Single-Precision

**Description:** Performs element-wise multiplication of packed single-precision floating-point values.

**Math Core Encoding:** Opcode 0x51, 20-bit header, 3 operand descriptors

**Assembly Syntax:**
```
MULPS dest, src1, src2
MULPS.Y dest, src1, src2   ; 256-bit
MULPS.Z dest, src1, src2   ; 512-bit
MULPS.K dest, src1, src2, mask ; Masked
```

**Examples:**
```assembly
; Multiply two 128-bit vectors
MULPS XMM1, XMM2, XMM3   ; XMM1 = XMM2 * XMM3

; Scale vector by scalar
MULPS XMM1, XMM2, XMM3_S ; XMM1 = XMM2 * XMM3[0]

; Square vector elements
MULPS XMM1, XMM2, XMM2   ; XMM1 = XMM2 * XMM2 (squares)

; 4x4 matrix multiplication row by vector
MULPS XMM5, YMM0, XMM4_S ; Row0 * vector (broadcast)
HADDPS XMM5, XMM5, XMM5  ; Horizontal sum

; Vector multiplication with memory operand
MULPS XMM1, XMM2, [R1]   ; XMM1 = XMM2 * memory at R1
```

---

## 6.3 DOT - Vector Dot Product

**Description:** Computes the dot product (scalar product) of two vectors.

**Math Core Encoding:** Opcode 0x52, 20-bit header, 3 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Scalar register | 32-64 bits | Result of dot product |
| Src1 | Vector register or memory | 128-1024 bits | First vector |
| Src2 | Vector register or memory | 128-1024 bits | Second vector |

**Assembly Syntax:**
```
DOT dest, src1, src2
DOT.MP dest, src1, src2    ; Mixed precision (float multiply, double accumulate)
```

**Examples:**
```assembly
; Simple dot product of two 4-element vectors
DOT R1, XMM2, XMM3     ; R1 = XMM2 · XMM3

; Squared length of vector
DOT R1, XMM2, XMM2     ; R1 = |XMM2|^2

; Cosine similarity
DOT R1, XMM2, XMM3     ; dot product
SQRT R2, R2            ; length of first vector
SQRT R3, R3            ; length of second vector
MUL R4, R2, R3         ; product of lengths
DIV R5, R1, R4         ; cosine = dot / (len1 * len2)

; Mixed-precision dot product (reduces rounding error)
DOT.MP R1, ZMM2, ZMM3

; Convolution using sliding dot product
DOT R1, XMM2, XMM3     ; kernel · input window

; Attention mechanism dot product
DOT R1, XMM_query, XMM_key   ; query · key
```

---

## 6.4 CONV - 2D Convolution

**Description:** Performs 2D convolution in constant time using a systolic array.

**Math Core Encoding:** Opcode 0x53, 20-bit header, 5 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Output | Memory | Variable | Output buffer address |
| Input | Memory | Variable | Input buffer address |
| Kernel | Memory | Variable | Kernel buffer address |
| Dimensions | Immediate | 32 bits | Height in bits 0-15, width in bits 16-31 |
| Stride | Immediate | 16 bits | Vertical stride bits 0-7, horizontal bits 8-15 |

**Assembly Syntax:**
```
CONV output, input, kernel, dimensions, stride
CONV.K5 output, input, kernel, dims, stride   ; 5x5 kernel
CONV.PAD_SAME output, input, kernel, dims, stride  ; Same padding
CONV.DEPTH output, input, kernel, dims, stride ; Depthwise
CONV.TRANS output, input, kernel, dims, stride ; Transposed
```

**Examples:**
```assembly
; 3x3 convolution on 224x224 image
CONV R3, R1, R2, #0xE0E0, #1   ; 224=0xE0, stride=1

; Same padding (output same size as input)
CONV.PAD_SAME R3, R1, R2, #0xE0E0, #1

; 5x5 convolution with stride 2
CONV.K5 R3, R1, R2, #0xE0E0, #0x0202

; Depthwise convolution (each channel has own kernel)
CONV.DEPTH R3, R1, R2, dimensions, stride

; 1x1 convolution (pointwise)
CONV.K1 R3, R1, R2, dimensions, #1

; 8-bit integer convolution (quantized networks)
CONV.I8 R3, R1, R2, dimensions, stride

; Transposed convolution (upsampling)
CONV.TRANS R3, R1, R2, dimensions, stride

; Dilated convolution with dilation rate 2
CONV.DILATE R3, R1, R2, dimensions, #0x0202, #2
```

---

## 6.5 SHUFPS - Shuffle Packed Single-Precision

**Description:** Reorders elements within a vector by selecting elements from two source vectors.

**Math Core Encoding:** Opcode 0x54, 20-bit header, 4 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Vector register | 128-512 bits | Destination for shuffled result |
| Src1 | Vector register | 128-512 bits | First source vector |
| Src2 | Vector register | 128-512 bits | Second source vector |
| Mask | Immediate | 8 bits | Shuffle pattern (2 bits per element) |

**Assembly Syntax:**
```
SHUFPS dest, src1, src2, mask
```

**Examples:**
```assembly
; Basic shuffle of 4 elements
SHUFPS XMM1, XMM2, XMM3, #0x1B
; XMM1 = {XMM2[1], XMM2[0], XMM3[3], XMM3[2]}

; Broadcast a single element to all positions
SHUFPS XMM1, XMM2, XMM2, #0x00   ; Broadcast XMM2[0]

; Reverse vector order
SHUFPS XMM1, XMM2, XMM2, #0x1B   ; Reverse 4 elements

; Interleave two vectors (for complex numbers)
SHUFPS XMM1, XMM2, XMM3, #0x88   ; {r0,i0,r1,i1}

; Unpack low and high halves
UNPCKLPS XMM1, XMM2, XMM3   ; {XMM2[0],XMM3[0],XMM2[1],XMM3[1]}
UNPCKHPS XMM1, XMM2, XMM3   ; {XMM2[2],XMM3[2],XMM2[3],XMM3[3]}

; Extract and broadcast element 2
SHUFPS XMM1, XMM2, XMM2, #0xAA   ; 0xAA = 10 10 10 10 (binary)
```

---

# Section 7: INT4 Inference Instructions

## 7.1 MATMULI4 - INT4 Matrix Multiplication

**Description:** Performs matrix multiplication of two INT4 matrices, accumulating results in 32-bit integers.

**Math Core Encoding:** Opcode 0x90, 20-bit header, 5 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Output | Memory | Variable | Output accumulator matrix address |
| A | Memory | Variable | First INT4 matrix |
| B | Memory | Variable | Second INT4 matrix |
| M | Immediate | 32 bits | Rows of A |
| K | Immediate | 32 bits | Columns of A / rows of B |
| N | Immediate | 32 bits | Columns of B |

**Assembly Syntax:**
```
MATMULI4 output, A, B, M, K, N
MATMULI4.T1 output, A, B, M, K, N   ; Transpose first matrix
MATMULI4.T2 output, A, B, M, K, N   ; Transpose second matrix
MATMULI4.R output, A, B, M, K, N, bias ; With ReLU activation
MATMULI4.G output, A, B, M, K, N, bias ; With GELU activation
```

**Examples:**
```assembly
; Basic INT4 matrix multiplication
MATMULI4 C, A, B, #1024, #1024, #1024

; With transpose
MATMULI4.T1 C, A, B, #1024, #1024, #1024  ; C = A^T × B

; With bias and ReLU activation
MATMULI4.R C, A, B, #1024, #1024, #1024, bias

; With GELU activation (transformer FFN)
MATMULI4.G C, A, B, #1024, #1024, #1024, bias
```

---

## 7.2 SOFTMAXI4 - INT4 Softmax

**Description:** Computes softmax on INT4 logits using FP16 for intermediate computation.

**Math Core Encoding:** Opcode 0x91, 20-bit header, 2 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Dest | Vector register or memory | Variable | Output probabilities (INT4) |
| Src | Vector register or memory | Variable | Input logits (INT4) |

**Assembly Syntax:**
```
SOFTMAXI4 dest, src
SOFTMAXI4.T dest, src, temp   ; Temperature-scaled
SOFTMAXI4.L dest, src         ; Log-softmax
```

**Examples:**
```assembly
; Softmax on INT4 logits
SOFTMAXI4 V1, V2

; Temperature-scaled softmax (T=0.7)
SOFTMAXI4.T V1, V2, #0.7

; Log-softmax (for cross-entropy loss)
SOFTMAXI4.L V1, V2
```

---

## 7.3 ATTENTIONI4 - INT4 Multi-Head Attention

**Description:** Computes scaled dot-product attention entirely in INT4 with FP16 softmax.

**Math Core Encoding:** Opcode 0x92, 20-bit header, 6 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Output | Memory | Variable | Output attention matrix |
| Q | Memory | Variable | Query matrix (INT4) |
| K | Memory | Variable | Key matrix (INT4) |
| V | Memory | Variable | Value matrix (INT4) |
| SeqLen | Immediate | 32 bits | Sequence length |
| HeadDim | Immediate | 32 bits | Head dimension |

**Assembly Syntax:**
```
ATTENTIONI4 output, Q, K, V, seq_len, head_dim
ATTENTIONI4.C output, Q, K, V, seq_len, head_dim  ; Causal masking
ATTENTIONI4.F output, Q, K, V, seq_len, head_dim  ; Flash attention
```

**Examples:**
```assembly
; Standard attention
ATTENTIONI4 output, Q, K, V, #2048, #64

; Causal masking (autoregressive)
ATTENTIONI4.C output, Q, K, V, #2048, #64

; Flash attention (memory-optimized)
ATTENTIONI4.F output, Q, K, V, #2048, #64
```

---

## 7.4 GELUI4 - INT4 GELU Activation

**Description:** Computes GELU activation on INT4 values using a lookup table.

**Math Core Encoding:** Opcode 0x93, 20-bit header, 2 operand descriptors

**Assembly Syntax:**
```
GELUI4 dest, src
GELUI4.F dest, src   ; Fast approximate (2x speed, 2% accuracy loss)
```

**Examples:**
```assembly
; Apply GELU to INT4 vector
GELUI4 V1, V2

; Fast approximate GELU
GELUI4.F V1, V2
```

---

## 7.5 LAYERNORMI4 - INT4 Layer Normalization

**Description:** Computes layer normalization on INT4 tensors.

**Math Core Encoding:** Opcode 0x94, 20-bit header, 3 operand descriptors

| Operand | Type | Size | Description |
|---------|------|------|-------------|
| Output | Memory | Variable | Output tensor (INT4) |
| Input | Memory | Variable | Input tensor (INT4) |
| Params | Memory | 2×32 bits | Scale and bias (FP16) |

**Assembly Syntax:**
```
LAYERNORMI4 output, input, params
```

**Examples:**
```assembly
; Normalize INT4 vector using learned scale and bias
LAYERNORMI4 output, input, params
```

---

## 7.6 RESIDUALI4 - INT4 Residual Connection

**Description:** Adds residual connection between two INT4 tensors using FP16 for addition.

**Math Core Encoding:** Opcode 0x95, 20-bit header, 3 operand descriptors

**Assembly Syntax:**
```
RESIDUALI4 output, input, residual
```

**Examples:**
```assembly
; Residual connection: output = input + residual
RESIDUALI4 output, input, residual
```

---

# Section 8: System Instructions

## 8.1 SYSENTER - Enter Kernel Mode

**Description:** Transfers control from user code to operating system kernel.

**System Core Encoding:** Opcode 0x20 (6-bit), 8-bit header, 0 operand descriptors

**Assembly Syntax:**
```
SYSENTER
SYSENTER.ASYNC   ; Asynchronous (returns immediately)
SYSENTER.REMOTE  ; Execute on remote blade
```

**Examples:**
```assembly
; Standard system call
MOV R1, #1        ; System call number (write)
MOV R2, fd        ; File descriptor
MOV R3, buffer    ; Buffer address
MOV R4, count     ; Byte count
SYSENTER

; Asynchronous system call
SYSENTER.ASYNC
; Continue execution while kernel processes request
```

---

## 8.2 SYSEXIT - Exit Kernel Mode

**Description:** Returns from kernel mode to user code.

**System Core Encoding:** Opcode 0x21 (6-bit), 8-bit header, 0 operand descriptors

**Assembly Syntax:**
```
SYSEXIT
SYSEXIT.SP        ; Return with modified stack pointer
SYSEXIT.REMOTE    ; Return to remote blade
```

**Examples:**
```assembly
; Return from system call
SYSEXIT

; Return with new stack pointer (for thread creation)
SYSEXIT.SP
```

---

## 8.3 IN - Input from Port

**Description:** Reads a byte, word, or doubleword from an I/O port.

**System Core Encoding:** Opcode 0x22 (6-bit), 8-bit header, 2 operand descriptors

**Assembly Syntax:**
```
IN dest, port
IN.W dest, port    ; Word (16-bit)
IN.D dest, port    ; Doubleword (32-bit)
IN.S dest, port    ; String input (repeated)
```

**Examples:**
```assembly
; Read byte from keyboard controller
IN R1, #0x60

; Read word from COM1 serial port
IN.W R1, #0x3F8

; Read 32 bytes from port into buffer
MOV R2, #32
IN.S R1, #0x3F8

; Read from port using register port number
MOV R2, #0x3F8
IN R1, R2
```

---

## 8.4 OUT - Output to Port

**Description:** Writes a byte, word, or doubleword to an I/O port.

**System Core Encoding:** Opcode 0x23 (6-bit), 8-bit header, 2 operand descriptors

**Assembly Syntax:**
```
OUT port, src
OUT.W port, src    ; Word (16-bit)
OUT.D port, src    ; Doubleword (32-bit)
OUT.S port, src    ; String output (repeated)
```

**Examples:**
```assembly
; Write byte to keyboard controller
OUT #0x60, R1

; Write word to COM1 serial port
OUT.W #0x3F8, R1

; Write 32 bytes from buffer to port
OUT.S #0x3F8, R1

; Write immediate value to POST port
OUT #0x80, #0x12
```

---

## 8.5 CFG_VIDEO - Configure Video Output

**Description:** Configures a video output tile to read a memory region as a framebuffer.

**System Core Encoding:** Opcode 0x24 (6-bit), 8-bit header, 5 operand descriptors

**Assembly Syntax:**
```
CFG_VIDEO tile, base, width, height, format, refresh
CFG_VIDEO.DB tile, base0, width, height, format, refresh  ; Double-buffered
CFG_VIDEO.SWAP tile, new_base   ; Swap buffer
CFG_VIDEO.OFF tile               ; Disable output
```

**Examples:**
```assembly
; Configure 1920x1080 RGB output at 60 Hz
CFG_VIDEO #0, framebuffer, #1920, #1080, #0x01, #60000

; 4K output with double buffering
CFG_VIDEO.DB #0, framebuffer0, #3840, #2160, #0x03, #60000

; Swap buffers (page flip)
CFG_VIDEO.SWAP #0, new_framebuffer

; DisplayPort output at 144 Hz
CFG_VIDEO.DP #1, framebuffer, #2560, #1440, #0x01, #144000

; Disable video output
CFG_VIDEO.OFF #0
```

---

## 8.6 CFG_AUDIO - Configure Audio Output

**Description:** Configures an audio output tile to read a circular buffer from memory.

**System Core Encoding:** Opcode 0x25 (6-bit), 8-bit header, 6 operand descriptors

**Assembly Syntax:**
```
CFG_AUDIO tile, buffer, size, rate, bits, channels, map
CFG_AUDIO.MIX tile, buffer, size, rate, bits, channels, map  ; Hardware mixing
```

**Examples:**
```assembly
; Configure stereo audio at 48 kHz
CFG_AUDIO #0, audio_buffer, #65536, #48000, #16, #2, channel_map

; 5.1 surround sound at 96 kHz
CFG_AUDIO #0, audio_buffer, #131072, #96000, #24, #6, surround_map

; HDMI audio output
CFG_AUDIO.HDMI #0, audio_buffer, #65536, #48000, #16, #2, channel_map

; Hardware mixing
CFG_AUDIO.MIX #0, master_buffer, #65536, #48000, #16, #2, map
```

---

## 8.7 RING_INIT - Initialize Circular Buffer

**Description:** Initializes a hardware-managed circular buffer.

**System Core Encoding:** Opcode 0x26 (6-bit), 8-bit header, 4 operand descriptors

**Assembly Syntax:**
```
RING_INIT buffer, segment_size, segment_count, control
RING_INIT.INT buffer, segment_size, segment_count, control  ; With interrupts
```

**Examples:**
```assembly
; Initialize audio ring buffer
RING_INIT audio_buffer, #4096, #16, ring_ctrl

; Initialize network receive ring
RING_INIT net_rx_buffer, #2048, #32, net_rx_ctrl

; Initialize with interrupts enabled
RING_INIT.INT audio_buffer, #4096, #16, ring_ctrl

; Remote ring buffer (shared between blades)
RING_INIT.REMOTE shared_buffer, #4096, #16, @4:ring_ctrl
```

---

## 8.8 RING_WRITE - Write to Ring Buffer

**Description:** Writes data to a hardware-managed circular buffer.

**System Core Encoding:** Opcode 0x27 (6-bit), 8-bit header, 3 operand descriptors

**Assembly Syntax:**
```
RING_WRITE ring, data, length
RING_WRITE.NB ring, data, length   ; Non-blocking
RING_WRITE.SG ring, list, count    ; Scatter-gather
```

**Examples:**
```assembly
; Write audio samples
RING_WRITE #0, audio_samples, #1024

; Non-blocking write
RING_WRITE.NB #0, audio_samples, #1024
BRANCH CS, buffer_full

; Scatter-gather write from multiple buffers
RING_WRITE.SG #0, sg_list, #3
```

---

## 8.9 RING_SWAP - Swap Ring Buffer Pointers

**Description:** Atomically swaps read and write pointers of a ring buffer.

**System Core Encoding:** Opcode 0x28 (6-bit), 8-bit header, 1 operand descriptor

**Assembly Syntax:**
```
RING_SWAP ring
RING_SWAP.BLOCK ring   ; Block until consumer finishes
RING_SWAP.COND ring    ; Conditional (non-blocking)
```

**Examples:**
```assembly
; Double-buffered audio
RING_WRITE #0, audio_samples, #4096
RING_SWAP #0
RING_WRITE #0, audio_samples2, #4096

; Video page flip
RENDER next_frame
RING_SWAP #0

; Conditional swap
RING_SWAP.COND #0
BRANCH CS, consumer_busy
```

---
# Sirius NEXUS AI Processor Gen5

## Rack Assembly and Task Startup Examples

This document provides comprehensive examples of rack assembly, system initialization, task startup, and distributed computation across multiple blades in a Sirius NEXUS cluster. The examples demonstrate the complete workflow from physical rack assembly to running parallel AI inference workloads.

---

# Section 1: Rack Assembly Specifications

## 1.1 Rack Chassis Specifications

The Sirius NEXUS rack chassis is designed to hold 20 blade servers in a standard 19-inch, 42U form factor. The chassis measures 600mm wide, 1000mm deep, and 1867mm tall (42U). Each blade slot is 40mm tall (1U) and 500mm deep. The chassis is constructed from 1.5mm thick steel with a powder-coated finish for durability and electromagnetic shielding.

**Physical Layout:**

| Component | Position | Dimensions | Quantity |
|-----------|----------|------------|----------|
| Blade slots | Front, vertical | 200mm × 500mm × 40mm each | 20 |
| Backplane | Rear, full height | 600mm × 1867mm × 5mm | 1 |
| Power distribution unit | Bottom rear | 600mm × 200mm × 200mm | 2 (redundant) |
| Management board | Top rear | 300mm × 100mm × 40mm | 1 |
| Liquid cooling manifold | Rear, horizontal | 600mm × 100mm × 100mm | 1 |
| Fan array | Rear, behind blades | 600mm × 1867mm × 50mm | 6 modules, 12 fans each |
| Optical backplane | Rear, internal | 600mm × 1867mm × 10mm | 1 |

**Blade Slot Numbering:**

```
Rack Front View (42U chassis, 20 blades)
┌─────────────────────────────────────────┐
│  Slot 20 │ Slot 19 │ Slot 18 │ Slot 17 │  Top (U42)
├─────────────────────────────────────────┤
│  Slot 16 │ Slot 15 │ Slot 14 │ Slot 13 │
├─────────────────────────────────────────┤
│  Slot 12 │ Slot 11 │ Slot 10 │ Slot 09 │
├─────────────────────────────────────────┤
│  Slot 08 │ Slot 07 │ Slot 06 │ Slot 05 │
├─────────────────────────────────────────┤
│  Slot 04 │ Slot 03 │ Slot 02 │ Slot 01 │  Bottom (U1)
└─────────────────────────────────────────┘
```

## 1.2 Physical Assembly Instructions

**Step 1: Rack Positioning and Leveling**

Position the rack chassis on a level concrete floor capable of supporting 1,000 kg. The rack must be within 1 degree of level in both X and Y axes. Use a laser level to verify. Extend the four leveling feet until they contact the floor and the casters are off the ground. Tighten the locking nuts to secure the feet. The rack should not wobble when pushed.

**Step 2: Power Distribution Unit Installation**

Slide the two Power Distribution Units (PDUs) into the bottom rear of the rack. Each PDU provides 48V DC at 10kW, with 20 output connectors (one per blade) plus 2 spare. Connect each PDU to separate building power circuits (208V AC, 30A, 3-phase). The PDUs are hot-swappable; if one fails, the other continues to supply power to all blades. The PDUs communicate with the management board via dedicated management Ethernet.

**Step 3: Management Board Installation**

Install the management board in the top rear of the rack. Connect the management board to the backplane via the 100-pin management connector. Connect the management board to the facility network via the RJ45 Ethernet port. The management board runs its own Linux-based operating system and provides a web interface at https://rack-mgmt.local. Default credentials are admin/admin (must be changed on first login).

**Step 4: Liquid Cooling Manifold Installation**

Connect the liquid cooling manifold to the backplane at the rear of the rack. The manifold has 20 pairs of quick-disconnect fittings (supply and return) that mate with each blade's cold plate when inserted. Connect the manifold to the facility chilled water supply (20°C, 50 GPM, 100 PSI max). The manifold includes temperature sensors and flow meters that report to the management board. The facility chiller must be capable of removing 20kW per rack (1kW per blade average).

**Step 5: Blade Insertion**

Insert blades from the front of the rack, one at a time. Align the blade with the slot rails. Push the blade fully into the slot until the edge connector seats in the backplane and the optical transceivers mate with the backplane waveguides. You will feel a distinct click when the blade is fully seated. Rotate the ejector handles to the locked position. The blade should be flush with the front of the rack (±1mm). Repeat for all 20 blades.

**Step 6: Optical Backplane Verification**

After all blades are inserted, verify the optical connections. On the management board web interface, navigate to Diagnostics → Optical Links. Each blade should show "Link Up" for all 12 optical channels. Signal strength should be between -5 dBm and -15 dBm. Bit error rate should be less than 10^-15. If any link shows errors, remove and reinsert the blade, ensuring proper alignment.

**Step 7: Power On Sequence**

Apply power to the PDUs. The management board boots first (approx. 30 seconds). The management board then sequentially powers on the blades, starting with Slot 1 and proceeding to Slot 20, with a 1-second delay between blades to prevent inrush current spikes. Each blade takes approximately 2.5 minutes for power-on self-test. The management board web interface shows the status of each blade (Power On, POST Running, Online, Fault).

**Step 8: Network Configuration**

Configure the management network. Connect the management board to your facility network. Assign static IP addresses to each blade (or configure DHCP). The default IP range is 10.0.0.1-10.0.0.20 for blades 1-20. Configure the data network for the optical fabric; the optical interconnects use a separate network that does not require IP configuration.

---

# Section 2: Rack Unification and Initialization

## 2.1 Single Rack Unification

After all blades are powered on and have passed POST, unify the rack into a single shared memory space using the RACK_UNIFY instruction. This instruction must be executed from the management board or from a dedicated System core on any blade with sufficient privileges.

**Assembly Code for Rack Unification:**

```assembly
; Rack unification program executed on management board
; Unified memory space: 20 blades, 64GB each = 1.28TB total

    ; Step 1: Check all blades are online
    MOV R1, #1               ; Blade counter
check_loop:
    LINK_STATUS R1, status_buffer
    LD.B R2, [status_buffer] ; Status byte: 0=offline, 1=online, 2=post, 3=fault
    CMP R2, #1               ; Check if online
    BRANCH NE, blade_offline
    ADD R1, #1
    CMP R1, #20
    BRANCH LE, check_loop

    ; Step 2: Export each blade's local memory
    MOV R1, #1               ; Blade counter
export_loop:
    ; Export 64GB of local memory from blade R1 to global address space
    ; Local base 0x00000000, size 64GB, appears at global base calculated from blade number
    MUL R2, R1, #0x100000000 ; Global base = blade_number * 64GB
    EXPORT_MEMORY #0x00000000, #0x100000000, R1, R2, #0x03  ; Read-write
    ADD R1, #1
    CMP R1, #20
    BRANCH LE, export_loop

    ; Step 3: Unify all blades with round-robin interleaving
    ; Addresses interleaved across blades at 64-byte granularity
    RACK_UNIFY #1, #20, #0x00000000, #64

    ; Step 4: Verify unification
    ; Test access to memory on blade 10 from blade 1
    REMOTE_CALL #10, verify_address, #1, @0x200000000, result
    CMP result, #0
    BRANCH EQ, unification_failed

    ; Step 5: Broadcast configuration to all blades
    BROADCAST.WAIT
        ; Each blade configures its local settings
        SET_REG_MAP #MATH, #FP16, #V512, #NEAREST
        SET_REG_MAP #ACU, #INT4, #V512, #NEAREST
    BROADCAST_END

blade_offline:
    ; Handle offline blade
    CALL report_offline_blade
    HLT

unification_failed:
    CALL report_unification_failure
    HLT
```

## 2.2 Multi-Rack Unification

For a multi-rack configuration (up to 256 racks), the process is similar but requires coordination between rack management boards.

```assembly
; Multi-rack unification (256 racks, 5,120 blades)
; Each rack has its own management board; primary rack coordinates

    ; Primary rack (Rack 0) management board code:

    ; Step 1: Discover all racks
    MOV R1, #1               ; Rack counter
rack_loop:
    ; Send discovery packet to rack R1
    REMOTE_CALL @rack:R1, discover_function, #0, #0, result
    CMP result, #0
    BRANCH EQ, rack_offline
    ADD R1, #1
    CMP R1, #256
    BRANCH LE, rack_loop

    ; Step 2: Assign global address ranges
    ; Each rack gets 512TB of address space (256 racks × 512TB = 128PB total)
    MOV R1, #1
assign_loop:
    MUL R2, R1, #0x80000000000   ; Rack base = rack_number * 512TB
    REMOTE_CALL @rack:R1, assign_address_range, #2, R2, #0x80000000000, result
    ADD R1, #1
    CMP R1, #256
    BRANCH LE, assign_loop

    ; Step 3: Enable cross-rack coherence
    ; Each rack's directory exports its local directory to global directory
    MOV R1, #1
coherence_loop:
    REMOTE_CALL @rack:R1, enable_global_directory, #0, #0, result
    ADD R1, #1
    CMP R1, #256
    BRANCH LE, coherence_loop

    ; Step 4: Unify all racks
    RACK_UNIFY.GLOBAL #1, #256, #0x00000000, #4096   ; 4KB interleaving
```

---

# Section 3: Task Startup and Scheduling

## 3.1 Hardware Task Scheduler Initialization

The Hardware Task Scheduler (HTS) manages task queues across all cores on a blade. Initialize the scheduler during system boot.

```assembly
; Hardware Task Scheduler initialization
; Run on System core 0 of each blade

    ; Step 1: Configure task queue memory
    ; Allocate 1MB for task queue (64K entries × 16 bytes)
    SEGMENT_CREATE #0, #0x10000000, #20, owner_0, #0x03, queue_desc
    LD.W queue_base, [queue_desc + #8]   ; Get allocated base address

    ; Step 2: Initialize scheduler registers
    ; SCHED_BASE - base address of task queue
    ; SCHED_HEAD - head pointer (next task to execute)
    ; SCHED_TAIL - tail pointer (next free slot)
    ; SCHED_COUNT - number of pending tasks
    MOV SCHED_BASE, queue_base
    MOV SCHED_HEAD, #0
    MOV SCHED_TAIL, #0
    MOV SCHED_COUNT, #0

    ; Step 3: Configure core assignment
    ; Core 0-7: Math cores
    ; Core 8-15: Logic cores
    ; Core 16-19: System cores
    ; Core 20-255: ACU cores
    CFG_SCHED_MASK #0xFF, #MATH_CORES      ; Math cores 0-7
    CFG_SCHED_MASK #0xFF00, #LOGIC_CORES   ; Logic cores 8-15
    CFG_SCHED_MASK #0xF0000, #SYSTEM_CORES ; System cores 16-19
    CFG_SCHED_MASK #0xFFF00000, #ACU_CORES ; ACU cores 20-255

    ; Step 4: Enable scheduler
    CFG_SCHED_ENABLE #1
```

## 3.2 Task Submission Example

Submit tasks to the hardware scheduler using the TASK_SUBMIT instruction.

```assembly
; Task submission example: Matrix multiplication on multiple cores
; Task function: multiply two 1024x1024 matrices

    ; Define task structure
    ; Each task: function pointer + up to 3 arguments
task_structure:
    DQ matmul_function     ; Function address
    DQ A_matrix_base       ; Argument 0: matrix A
    DQ B_matrix_base       ; Argument 1: matrix B
    DQ result_base         ; Argument 2: result matrix
    DQ 1024                ; Argument 3: dimension (optional)

    ; Submit 64 tasks (each processes 128x128 tile)
    MOV R1, #0             ; Task counter
submit_loop:
    ; Calculate tile address for this task
    ; Each tile is 128x128 = 16K elements = 64KB (if FP16)
    MUL R2, R1, #65536     ; Tile offset
    ADD R3, A_matrix_base, R2
    ADD R4, B_matrix_base, R2
    ADD R5, result_base, R2

    ; Build task descriptor in memory
    ST.D [task_buffer], matmul_tile_function
    ST.D [task_buffer+8], R3
    ST.D [task_buffer+16], R4
    ST.D [task_buffer+24], R5

    ; Submit task
    TASK_SUBMIT task_buffer, #MATH_CORE   ; Execute on any Math core

    ADD R1, #1
    CMP R1, #64
    BRANCH LT, submit_loop

    ; Wait for all tasks to complete
    TASK_WAIT #0           ; Wait for task queue to empty

    ; All tasks complete, result matrix is ready
```

## 3.3 Task Function Example (Matrix Multiplication Tile)

```assembly
; Task function: multiply a 128x128 tile
; Input: R1 = A tile address, R2 = B tile address, R3 = result tile address

matmul_tile_function:
    ; Configure register types
    SET_REG_MAP #MATH, #FP16, #V512, #NEAREST

    ; Allocate local registers
    ; V0-V15: row of A
    ; V16-V31: column of B
    ; V32: accumulator

    MOV R4, #0             ; i loop counter (rows)
row_loop:
    ; Load row i from A tile (128 elements = 16 vectors of 8 floats each)
    LEA R5, [R1 + R4*256]  ; Each row is 128 elements × 2 bytes = 256 bytes
    MOV R6, #0             ; j loop counter (columns)
col_loop:
    ; Initialize accumulator to zero
    XOR V32, V32

    ; Load column j from B tile (128 elements)
    LEA R7, [R2 + R6*2]    ; Each column element is 2 bytes (FP16)

    ; Dot product using vector FMA
    MOV R8, #0             ; k counter
dot_loop:
    ; Load 8 elements from row (V0)
    LD.V V0, [R5 + R8*16]  ; 8 FP16 values = 16 bytes

    ; Load 8 elements from column (V16)
    LD.V V16, [R7 + R8*16]

    ; FMA: accumulate += row[k] * column[k]
    FMA.V V32, V0, V16, V32

    ADD R8, #8
    CMP R8, #128
    BRANCH LT, dot_loop

    ; Horizontal sum of V32 to get single value
    HADDPS V32, V32, V32
    HADDPS V32, V32, V32
    HADDPS V32, V32, V32

    ; Store result
    MOV R9, [R3 + R4*256 + R6*2]
    ST.H [R9], V32

    ADD R6, #1
    CMP R6, #128
    BRANCH LT, col_loop

    ADD R4, #1
    CMP R4, #128
    BRANCH LT, row_loop

    ; Task complete
    TASK_EXIT
```

---

# Section 4: Distributed AI Inference Example

## 4.1 Loading a Large Language Model Across Multiple Blades

This example demonstrates loading a 1.8 trillion parameter model across 20 blades using memory-mapped ROMB Gen2 storage.

```assembly
; Load LLM across all blades in a rack
; Model: 1.8T parameters at INT4 = 900GB
; Each blade has 1.5TB ROMB, so model fits on one blade, but we distribute for throughput

    ; Step 1: Map ROMB Gen2 on each blade
    ; Assume model is pre-loaded on ROMB at manufacturing
    BROADCAST.WAIT
        ; Map ROMB Gen2 stack 0 to memory address 0x200000000 on each blade
        MAP_STORAGE.ROMB2 #0, #0, #0x200000000, #0x17C00000000  ; 1.5TB
    BROADCAST_END

    ; Step 2: Partition model across blades
    ; Blade 1: layers 0-9
    ; Blade 2: layers 10-19
    ; ... Blade 20: layers 190-199 (assuming 200-layer model)
    MOV R1, #1
partition_loop:
    MUL R2, R1, #10        ; Start layer = (blade-1)*10
    SUB R3, R2, #10        ; End layer = start layer + 9
    REMOTE_CALL R1, load_model_layers, #2, R2, R3, result
    ADD R1, #1
    CMP R1, #20
    BRANCH LE, partition_loop

    ; Step 3: Load tokenizer and embedding table on all blades
    BROADCAST.WAIT
        ; Embedding table: 100,000 tokens × 4096 dimensions × 2 bytes = 819MB
        DME_COPY #0x200000000, embedding_buffer, #0x33300000
    BROADCAST_END
```

## 4.2 Distributed Inference Execution

```assembly
; Distributed inference on 20 blades
; Each blade processes a different batch

    ; Step 1: Configure inference parameters
    MOV batch_size, #100       ; 100 sequences per blade
    MOV seq_length, #2048      ; 2048 tokens per sequence
    MOV total_batches, #1000   ; Total batches to process

    ; Step 2: Launch inference tasks on all blades
batch_loop:
    MOV R1, #1                 ; Blade counter
    MOV R2, current_batch      ; Batch ID

launch_loop:
    ; Submit inference task to blade R1
    ; Task processes one batch on that blade
    REMOTE_CALL.ASYNC R1, inference_task, #3, R2, batch_size, seq_length, result

    ADD R1, #1
    CMP R1, #20
    BRANCH LE, launch_loop

    ; Step 3: Wait for all blades to complete
    BARRIER_SYNC

    ; Step 4: Collect results
    MOV R1, #1
collect_loop:
    REMOTE_CALL R1, get_results, #1, result_buffer, results
    ; Aggregate results from blade R1
    CALL aggregate_results
    ADD R1, #1
    CMP R1, #20
    BRANCH LE, collect_loop

    ADD current_batch, #1
    CMP current_batch, total_batches
    BRANCH LT, batch_loop

    ; Step 5: Output final results
    CALL output_predictions
```

## 4.3 Single Blade Inference Task

```assembly
; Inference task running on a single blade
; Processes one batch of sequences

inference_task:
    ; Arguments:
    ; R1 = batch_id
    ; R2 = batch_size
    ; R3 = seq_length

    ; Configure for INT4 inference
    SET_REG_MAP #ACU, #INT4, #V512, #NEAREST

    ; Load model layers from local ROMB
    ; Model stored at 0x200000000, each layer is 4.5GB
    MOV R4, #0                 ; Layer counter
layer_loop:
    ; Load layer weights from ROMB
    MUL R5, R4, #0x120000000  ; Layer offset = layer × 4.5GB
    ADD R6, R5, #0x200000000  ; Layer address

    ; Run attention for this layer
    ; Q, K, V tensors are in HBM at known locations
    ATTENTIONI4.C output, Q, K, V, seq_length, #64

    ; Run FFN for this layer
    MATMULI4.R ff_output, attn_output, weights1, #4096, #4096, #16384, bias1
    MATMULI4 ff_output2, ff_output, weights2, #4096, #16384, #4096
    RESIDUALI4 output, ff_output2, attn_output   ; Add residual

    ; Layer normalization
    LAYERNORMI4 output, output, layer_norm_params

    ADD R4, #1
    CMP R4, #200              ; 200 layers
    BRANCH LT, layer_loop

    ; Softmax over final logits
    SOFTMAXI4 predictions, logits

    ; Store results for this batch
    ST.V [result_buffer], predictions

    TASK_EXIT
```

---

# Section 5: Full System Boot Sequence

## 5.1 Blade Power-On Self-Test (POST) Sequence

```assembly
; Blade POST executed on System core 0 immediately after power-on

post_sequence:
    ; Step 1: Clock test - verify all PLLs locked
    MOV R1, #0
clock_test:
    RD_PLL_STATUS R1, status
    TEST status, #LOCK_BIT
    BRANCH Z, clock_failed
    ADD R1, #1
    CMP R1, #NUM_PLLS
    BRANCH LT, clock_test

    ; Step 2: Voltage test - verify all rails within tolerance
    RD_VOLTAGE_SENSOR #CORE_VOLTAGE, voltage
    CMP voltage, #0x780       ; 0.8V = 0x780 in sensor units
    BRANCH LO, voltage_failed
    CMP voltage, #0x820
    BRANCH HI, voltage_failed

    ; Step 3: Temperature test - verify all sensors below threshold
    MOV R1, #0
temp_test:
    RD_TEMP_SENSOR R1, temp
    CMP temp, #85             ; 85°C max
    BRANCH HI, temp_failed
    ADD R1, #1
    CMP R1, #NUM_SENSORS
    BRANCH LT, temp_test

    ; Step 4: Memory test - quick test of first 1GB HBM
    MEM_TEST #0x00000000, #0x40000000, #TEST_PATTERN

    ; Step 5: ROMB Gen2 test - verify signature
    MOV R1, [0x200000000]      ; Read first word from ROMB
    CMP R1, #ROMB_SIGNATURE
    BRANCH NE, romb_failed

    ; Step 6: Optical link test
    MOV R1, #0
link_test:
    LINK_STATUS R1, link_buffer
    LD.B R2, [link_buffer]     ; Link status
    CMP R2, #1                 ; 1 = up
    BRANCH NE, link_failed
    ADD R1, #1
    CMP R1, #12                ; 12 optical transceivers
    BRANCH LT, link_test

    ; Step 7: Core self-test
    ; Built-in self-test of each core type
    BIST_MATH
    BIST_LOGIC
    BIST_SYSTEM
    BIST_ACU

    ; Step 8: Notify management board
    SEND_MGMT_STATUS #POST_PASSED

    ; Step 9: Load bootloader from ROMB
    DME_COPY #0x200000000, bootloader_entry, #0x10000
    JMP bootloader_entry

clock_failed:
    SEND_MGMT_STATUS #CLOCK_FAIL
    HLT
voltage_failed:
    SEND_MGMT_STATUS #VOLTAGE_FAIL
    HLT
temp_failed:
    SEND_MGMT_STATUS #TEMP_FAIL
    HLT
romb_failed:
    SEND_MGMT_STATUS #ROMB_FAIL
    HLT
link_failed:
    SEND_MGMT_STATUS #LINK_FAIL
    HLT
```

## 5.2 Management Board Coordination

```assembly
; Management board code - coordinates all blades in the rack

management_main:
    ; Step 1: Initialize management interfaces
    CFG_NETWORK mgmt_ip, #255.255.255.0, #10.0.0.1
    CFG_WEB_INTERFACE #8080

    ; Step 2: Wait for all blades to complete POST
    MOV R1, #1
blade_wait:
    WAIT_FOR_BLADE_STATUS R1, #POST_PASSED, #30000  ; 30 second timeout
    CMP result, #0
    BRANCH EQ, blade_timeout
    ADD R1, #1
    CMP R1, #20
    BRANCH LE, blade_wait

    ; Step 3: Power on optical fabric
    CFG_OPTICAL_FABRIC #ENABLE

    ; Step 4: Unify rack memory
    CALL unify_rack

    ; Step 5: Load and start distributed operating system
    CALL load_distributed_os

    ; Step 6: Start workload manager
    CALL start_workload_manager

    ; Step 7: Enable external access
    CFG_EXTERNAL_ACCESS #ENABLE

    ; Step 8: Main management loop
management_loop:
    ; Monitor blade health
    CALL check_blade_health

    ; Monitor temperature and adjust cooling
    CALL thermal_management

    ; Handle blade failures
    CALL handle_blade_failures

    ; Process management requests
    CALL process_management_requests

    WAIT #1000                ; 1 second loop
    JMP management_loop

blade_timeout:
    ; Blade R1 failed to respond
    CALL report_blade_failure
    ; Continue with remaining blades
```

---

# Section 6: Example Configuration Files

## 6.1 Rack Configuration File (YAML)

```yaml
# Sirius NEXUS Rack Configuration
# File: /etc/sirius/rack_config.yaml

rack:
  id: 1
  name: "AI Training Rack A"
  location: "Data Center West, Row 3, Position 2"

  chassis:
    model: "SN-RACK-42U"
    serial: "SNR-2024-001"
    power: "208V AC, 30A, 3-phase"
    cooling: "Chilled water 20°C, 50 GPM"

  blades:
    - slot: 1
      type: "inference-optimized"
      cores: 149120
      memory: "64GB HBM2e"
      storage: "200TB NAND + 1.5TB ROMB"
      mac: "00:1A:2B:3C:4D:01"
      status: "online"

    - slot: 2
      type: "inference-optimized"
      cores: 149120
      memory: "64GB HBM2e"
      storage: "200TB NAND + 1.5TB ROMB"
      mac: "00:1A:2B:3C:4D:02"
      status: "online"

    # ... slots 3-19 similarly configured ...

    - slot: 20
      type: "storage-only"
      cores: 800
      memory: "32GB DDR4"
      storage: "200TB NAND"
      mac: "00:1A:2B:3C:4D:14"
      status: "online"

  network:
    management:
      subnet: "10.0.0.0/24"
      gateway: "10.0.0.1"
    data:
      type: "optical-fabric"
      bandwidth: "9.6 Tb/s per blade"
      topology: "full-mesh"

  cooling:
    supply_temp: 20
    return_temp: 30
    flow_rate: 50
    unit: "GPM"

  power:
    total_capacity: 20000
    current_load: 4800
    unit: "W"
```

## 6.2 Task Queue Configuration

```assembly
; Task queue configuration for workload manager
; File: /etc/sirius/task_queue.cfg

    ; Queue parameters
    QUEUE_SIZE = 65536        ; 64K task slots
    TASK_TIMEOUT = 60000      ; 60 second timeout (ms)
    MAX_RETRIES = 3

    ; Priority levels (0=highest, 7=lowest)
    PRIORITY_REALTIME = 0
    PRIORITY_HIGH = 2
    PRIORITY_NORMAL = 4
    PRIORITY_LOW = 6
    PRIORITY_BACKGROUND = 7

    ; Core assignment
    CORE_MATH = 0x000000FF    ; Cores 0-7
    CORE_LOGIC = 0x0000FF00   ; Cores 8-15
    CORE_SYSTEM = 0x000F0000  ; Cores 16-19
    CORE_ACU = 0xFFF00000     ; Cores 20-255

    ; Scheduling policy
    SCHED_POLICY = "round_robin"  ; Options: round_robin, fifo, priority
    LOAD_BALANCING = true
    PREEMPTION = true

    ; Power management
    POWER_GOVERNOR = "performance"  ; Options: performance, powersave, ondemand
    IDLE_CORE_PARK = true
    CORE_PARK_DELAY = 100    ; ms before parking idle core
```

---

# Section 7: Monitoring and Debugging

## 7.1 Rack Health Monitoring

```assembly
; Rack health monitoring loop
; Runs on management board every second

health_monitor:
    ; Check each blade
    MOV R1, #1
blade_check:
    ; Get blade status
    GET_BLADE_STATUS R1, status_buffer

    ; Check temperature
    LD.W temp, [status_buffer + #8]
    CMP temp, #80            ; Warning at 80°C
    BRANCH HI, temp_warning
    CMP temp, #85            ; Critical at 85°C
    BRANCH HI, temp_critical

    ; Check power consumption
    LD.W power, [status_buffer + #12]
    CMP power, #250          ; Blade rated at 240W
    BRANCH HI, power_warning

    ; Check memory errors
    LD.W mem_errors, [status_buffer + #16]
    CMP mem_errors, #100
    BRANCH HI, mem_warning

    ; Check optical link errors
    LD.W link_errors, [status_buffer + #20]
    CMP link_errors, #1000
    BRANCH HI, link_warning

    ADD R1, #1
    CMP R1, #20
    BRANCH LE, blade_check

    ; Log health status
    CALL log_health_metrics

    WAIT #1000               ; 1 second
    JMP health_monitor

temp_warning:
    CALL log_temp_warning
    ; Increase fan speed
    CFG_FAN_SPEED #HIGH
    JMP blade_check

temp_critical:
    CALL log_temp_critical
    ; Throttle blade or power off
    CFG_BLADE_POWER R1, #OFF
    JMP blade_check
```

## 7.2 Debug Console Commands

```assembly
; Management board debug console commands

debug_command_help:
    ; Commands available:
    ; status      - Show rack status
    ; blade N     - Show blade N status
    ; memory      - Show memory utilization
    ; tasks       - Show task queues
    ; power       - Show power consumption
    ; temp        - Show temperatures
    ; links       - Show optical link status
    ; reset N     - Reset blade N
    ; shutdown    - Shutdown entire rack
    ; unify       - Re-run rack unification
    ; diag        - Run diagnostics

debug_command_status:
    ; Show rack summary
    CALL get_rack_status
    PRINT "Rack ID: ", rack_id
    PRINT "Blades online: ", online_count, "/20"
    PRINT "Total cores: ", total_cores
    PRINT "Total memory: ", total_memory, "GB"
    PRINT "Total storage: ", total_storage, "TB"
    PRINT "Power: ", current_power, "/20000 W"
    PRINT "Temperature: ", avg_temp, "C"

debug_command_blade:
    ; Show blade N status
    ; R1 = blade number
    GET_BLADE_STATUS R1, status_buffer
    PRINT "Blade ", R1, ":"
    LD.B type, [status_buffer]
    PRINT "  Type: ", type
    LD.W temp, [status_buffer + #8]
    PRINT "  Temperature: ", temp, "C"
    LD.W power, [status_buffer + #12]
    PRINT "  Power: ", power, "W"
    LD.W tasks, [status_buffer + #24]
    PRINT "  Pending tasks: ", tasks
    LD.W ipc, [status_buffer + #28]
    PRINT "  IPC: ", ipc
```

---

# Section 8: Complete Rack Assembly Checklist

## 8.1 Pre-Assembly Checklist

| Item | Specification | Verified |
|------|---------------|----------|
| Floor load capacity | ≥1,000 kg per rack | ☐ |
| Power availability | 208V AC, 30A, 3-phase, 2 circuits | ☐ |
| Cooling availability | Chilled water 20°C, 50 GPM | ☐ |
| Network connectivity | 10GbE management network | ☐ |
| Physical space | 600mm width, 1200mm depth, 2000mm height | ☐ |
| Grounding | Earth ground connection | ☐ |
| ESD protection | Wrist strap, grounded mat | ☐ |
| Tools | Torque wrench, level, multimeter, fiber scope | ☐ |

## 8.2 Assembly Steps Checklist

| Step | Action | Verified |
|------|--------|----------|
| 1 | Position and level rack | ☐ |
| 2 | Install PDUs (2 units) | ☐ |
| 3 | Connect PDU power to building circuits | ☐ |
| 4 | Install management board | ☐ |
| 5 | Connect management board to network | ☐ |
| 6 | Install liquid cooling manifold | ☐ |
| 7 | Connect cooling to facility supply | ☐ |
| 8 | Insert blades in slots 1-20 | ☐ |
| 9 | Secure blades with ejector handles | ☐ |
| 10 | Connect management cables | ☐ |
| 11 | Power on PDUs | ☐ |
| 12 | Verify management board boot | ☐ |
| 13 | Monitor blade POST | ☐ |
| 14 | Verify optical links | ☐ |
| 15 | Run rack unification | ☐ |
| 16 | Load operating system | ☐ |
| 17 | Run validation tests | ☐ |
| 18 | Enable external access | ☐ |

## 8.3 Validation Tests

```assembly
; Post-assembly validation test suite
; Run from management board

validation_suite:
    ; Test 1: Memory bandwidth
    PRINT "Test 1: Memory bandwidth..."
    CALL test_memory_bandwidth
    CMP result, #3000        ; Should exceed 3 TB/s
    BRANCH LT, test_failed

    ; Test 2: Optical fabric latency
    PRINT "Test 2: Optical fabric latency..."
    CALL test_fabric_latency
    CMP result, #6000        ; Should be under 6 µs
    BRANCH HI, test_failed

    ; Test 3: Cross-blade coherence
    PRINT "Test 3: Cross-blade coherence..."
    CALL test_coherence
    CMP result, #0
    BRANCH NE, test_failed

    ; Test 4: AI inference throughput
    PRINT "Test 4: AI inference throughput..."
    CALL test_inference_throughput
    CMP result, #600000       ; Should exceed 600K tokens/sec
    BRANCH LT, test_failed

    ; Test 5: Thermal performance
    PRINT "Test 5: Thermal performance..."
    CALL test_thermal
    CALL get_max_temperature
    CMP temp, #85
    BRANCH HI, test_failed

    PRINT "All tests passed!"
    JMP validation_done

test_failed:
    PRINT "Test failed!"
    CALL report_failure
    HLT
```

---

This completes the rack assembly and task startup documentation for the Sirius NEXUS AI Processor Gen5. The examples cover physical rack assembly, electrical and cooling connections, blade insertion, system initialization, rack unification, task scheduling, distributed inference, and health monitoring. The assembly checklist and validation tests provide a complete workflow for deploying a production Sirius NEXUS cluster.

# Sirius NEXUS AI Processor Gen5

## Complete Operand Syntax and Data Block Documentation

This document provides comprehensive documentation of all operand syntax forms, addressing modes, data block definitions, and memory layout specifications for the Sirius NEXUS instruction set. Every possible operand type is described with syntax examples, encoding rules, and usage patterns.

---

# Section 1: Operand Types Overview

The Sirius NEXUS architecture supports six operand types, each with its own syntax and encoding. The type is determined by the operand descriptor in the instruction encoding.

| Type Code | Operand Type | Syntax Pattern | Example |
|-----------|--------------|----------------|---------|
| 0 | Register | `R[0-31]`, `V[0-63]`, `L[0-31]`, `S[0-15]` | `R1`, `V32`, `L5`, `S0` |
| 1 | Memory | `[expression]` | `[R1]`, `[R2 + 64]`, `[R3 + R4*8]` |
| 2 | Immediate | `#value` | `#42`, `#0xFF`, `#3.14159` |
| 3 | Remote Memory | `@blade:address` | `@4:0x10000`, `@0xFFF:0x200000000` |
| 4 | Vector | `vector[range]` | `V1[0:7]`, `V2[0:15:2]` |
| 5 | Register Type Map | `%register` | `%R1`, `%V32` |

---

# Section 2: Register Operands

## 2.1 Math Core Registers

| Register Class | Count | Size | Names | Syntax | Use |
|----------------|-------|------|-------|--------|-----|
| Vector Registers | 64 | 512-bit | V0-V63 | `Vn` | SIMD operations |
| Scalar Registers | 32 | 64-bit | R0-R31 | `Rn` | General purpose |
| Mask Registers | 8 | 64-bit | K0-K7 | `Kn` | Vector masking |
| Control Registers | 16 | 64-bit | CR0-CR15 | `CRn` | System control |
| Status Registers | 4 | 64-bit | SR0-SR3 | `SRn` | Status flags |

**Syntax Examples:**

```assembly
; Vector register operations
MOV V1, V2              ; Copy vector V2 to V1
ADDPS V1, V2, V3        ; V1 = V2 + V3 (element-wise)

; Scalar register operations
MOV R1, #42             ; Load immediate
ADD R1, R2              ; R1 = R1 + R2

; Mask register operations
AND K1, K2, K3          ; K1 = K2 & K3 (bitwise)
MOV K1, #0xFF00         ; Load mask pattern

; Control register operations (privileged)
MOV CR0, R1             ; Set control register
MOV R1, CR0             ; Read control register

; Status register operations (read-only)
MOV R1, SR0             ; Read status flags
```

## 2.2 Logic Core Registers

| Register Class | Count | Size | Names | Syntax | Use |
|----------------|-------|------|-------|--------|-----|
| General Registers | 32 | 64-bit | R0-R31 | `Rn` | General purpose |
| Program Counter | 1 | 64-bit | PC | `PC` | Instruction pointer |
| Stack Pointer | 1 | 64-bit | SP | `SP` | Software stack |
| Link Register | 1 | 64-bit | LR | `LR` | Return address |
| Condition Codes | 1 | 32-bit | CC | `CC` | Condition flags |

**Syntax Examples:**

```assembly
; General register operations
MOV R1, R2              ; Copy R2 to R1
ADD R1, #1              ; Increment R1

; Program counter access (read-only)
MOV R1, PC              ; Get current instruction address

; Stack pointer operations
SUB SP, #32             ; Allocate stack space
MOV [SP], R1            ; Push to stack
MOV R1, [SP]            ; Pop from stack

; Link register for function calls
CALL subroutine         ; LR set to return address
RET                     ; Returns to address in LR

; Condition codes
CMP R1, R2              ; Set condition codes
BRANCH EQ, equal_label  ; Branch if equal
```

## 2.3 System Core Registers

| Register Class | Count | Size | Names | Syntax | Use |
|----------------|-------|------|-------|--------|-----|
| General Registers | 16 | 64-bit | R0-R15 | `Rn` | General purpose |
| Model-Specific | 32 | 64-bit | MSR0-MSR31 | `MSRn` | System configuration |
| Interrupt Vector | 1 | 64-bit | IVT | `IVT` | Interrupt vector table |
| Page Table Base | 1 | 64-bit | PTBR | `PTBR` | Page table root |

**Syntax Examples:**

```assembly
; General register operations
MOV R1, R2              ; Copy R2 to R1
MOV R1, #0x1000         ; Load immediate

; Model-specific registers (privileged)
MOV MSR0, R1            ; Set MSR
MOV R1, MSR0            ; Read MSR

; Interrupt vector table
MOV IVT, R1             ; Set interrupt vector base

; Page table base register
MOV PTBR, R1            ; Set page table root
```

---

# Section 3: Memory Operands

## 3.1 Addressing Modes

| Mode | Syntax | Effective Address | Use Case |
|------|--------|-------------------|----------|
| Direct | `[address]` | `address` | Absolute addressing |
| Register Indirect | `[Rn]` | `Rn` | Pointer access |
| Base + Offset | `[Rn + offset]` | `Rn + offset` | Structure fields |
| Base + Index | `[Rn + Rm]` | `Rn + Rm` | Array access |
| Base + Index*Scale | `[Rn + Rm * scale]` | `Rn + (Rm × scale)` | Typed array access |
| Base + Offset + Index | `[Rn + offset + Rm]` | `Rn + offset + Rm` | Structure array access |
| PC-Relative | `[PC + offset]` | `PC + offset` | Position-independent code |
| Absolute 64-bit | `[0x...]` | `64-bit address` | Large memory access |

**Scale Factors:**

| Scale Value | Multiply Factor | Use |
|-------------|-----------------|-----|
| 1 | ×1 | 8-bit elements |
| 2 | ×2 | 16-bit elements |
| 4 | ×4 | 32-bit elements |
| 8 | ×8 | 64-bit elements |
| 16 | ×16 | 128-bit elements |
| 32 | ×32 | 256-bit elements |
| 64 | ×64 | 512-bit elements |

## 3.2 Memory Operand Syntax Examples

```assembly
; Direct addressing
MOV R1, [0x1000]        ; Load from absolute address 0x1000
MOV [0x2000], R1        ; Store to absolute address 0x2000

; Register indirect
MOV R1, [R2]            ; Load from address in R2
MOV [R3], R1            ; Store to address in R3

; Base + offset (displacement)
MOV R1, [R2 + 64]       ; Load from R2 + 64
MOV [R3 + 8], R1        ; Store to R3 + 8

; Base + index
MOV R1, [R2 + R3]       ; Load from R2 + R3
MOV [R4 + R5], R1       ; Store to R4 + R5

; Base + index × scale
MOV R1, [R2 + R3*8]     ; Load from R2 + (R3 × 8) for 64-bit array
MOV [R4 + R5*4], R1     ; Store to R4 + (R5 × 4) for 32-bit array

; Base + offset + index × scale
MOV R1, [R2 + 64 + R3*8] ; Load from array with header
MOV [R4 + 16 + R5*4], R1 ; Store to structure array

; PC-relative (for position-independent code)
LEA R1, [PC + 64]       ; Get address of data at PC+64
MOV R2, [PC + 128]      ; Load from data section

; Large absolute address (64-bit)
MOV R1, [0x100000000]   ; Load from address above 4GB
MOV [0x200000000], R1   ; Store to address above 4GB
```

## 3.3 Memory Operand Size Specifications

Size can be specified explicitly using suffixes when the operand size cannot be inferred from the instruction or registers.

| Suffix | Size (bits) | Size (bytes) | Syntax Example |
|--------|-------------|--------------|----------------|
| `.B` | 8 | 1 | `MOV.B [R1], #0xFF` |
| `.W` | 16 | 2 | `MOV.W [R1], #0xFFFF` |
| `.D` | 32 | 4 | `MOV.D [R1], #0xFFFFFFFF` |
| `.Q` | 64 | 8 | `MOV.Q [R1], #0xFFFFFFFFFFFFFFFF` |
| `.O` | 128 | 16 | `MOV.O [R1], V1` |
| `.Y` | 256 | 32 | `MOV.Y [R1], YMM1` |
| `.Z` | 512 | 64 | `MOV.Z [R1], ZMM1` |

**Examples:**

```assembly
; Explicit size specification
MOV.B [R1], #0xFF       ; Store byte
MOV.W [R1], #0xFFFF     ; Store word (16-bit)
MOV.D [R1], #0xFFFFFFFF ; Store doubleword (32-bit)
MOV.Q [R1], R2          ; Store quadword (64-bit)

; Implicit size from source
MOV [R1], R2            ; Size inferred from R2 (64-bit)
MOV [R1], V1            ; Size inferred from V1 (512-bit)
```

---

# Section 4: Immediate Operands

## 4.1 Integer Immediate Formats

| Format | Syntax | Example | Size Range |
|--------|--------|---------|------------|
| Decimal | `#number` | `#42` | -2^63 to 2^63-1 |
| Hexadecimal | `#0xhex` | `#0xFF` | 0 to 2^64-1 |
| Binary | `#0bbinary` | `#0b1010` | 0 to 2^64-1 |
| Octal | `#0ooctal` | `#0o777` | 0 to 2^64-1 |
| Character | `#'char'` | `#'A'` | ASCII (8-bit) |
| String | `#"string"` | `#"Hello"` | Multiple bytes |

**Syntax Examples:**

```assembly
; Decimal immediate
MOV R1, #42             ; 42 decimal
ADD R1, #-100           ; -100 decimal

; Hexadecimal immediate
MOV R1, #0xFF           ; 255 decimal
AND R1, #0xFFFFFF00     ; Mask for clearing low 8 bits

; Binary immediate
MOV R1, #0b10101010     ; 170 decimal
XOR R1, #0b11110000     ; Toggle high 4 bits

; Octal immediate
MOV R1, #0o777          ; 511 decimal
SHL R1, #0o10           ; Shift left by 8

; Character immediate
MOV R1, #'A'            ; 65 decimal (ASCII 'A')
CMP R1, #'\n'           ; Compare to newline (10)

; String immediate (multiple bytes)
DB #"Hello, World!\n"   ; String data in memory
```

## 4.2 Floating-Point Immediate Formats

| Format | Syntax | Example | Precision |
|--------|--------|---------|-----------|
| Decimal | `#number` | `#3.14159` | Double (FP64) |
| Scientific | `#valueeexp` | `#1.0e-10` | Double (FP64) |
| Hexadecimal Float | `#0xhexp` | `#0x1.0p0` | Binary representation |
| Single Precision | `#number.f` | `#3.14f` | Single (FP32) |
| Half Precision | `#number.h` | `#3.14h` | Half (FP16) |

**Syntax Examples:**

```assembly
; Double-precision floating-point
FMA R1, R2, R3, #1.0   ; Add 1.0
MOV R1, #3.141592653589793

; Single-precision floating-point
MOV R1, #3.14159f      ; Single precision (store in low 32 bits)
ADDPS XMM1, XMM2, #1.0f ; Add 1.0f to all elements

; Half-precision floating-point (for INT4 inference)
MOV R1, #1.0h          ; Half precision
MOVI4 V1, #0.5h        ; Load 0.5 into INT4 vector

; Scientific notation
MOV R1, #1.60217662e-19 ; Electron charge in coulombs
MOV R1, #2.99792458e8   ; Speed of light in m/s

; Hexadecimal floating-point (exact representation)
MOV R1, #0x1.0000000000000p0 ; 1.0
MOV R1, #0x1.8000000000000p1 ; 3.0
```

## 4.3 Special Immediate Values

| Value | Syntax | Description |
|-------|--------|-------------|
| True | `#TRUE` or `#1` | Boolean true |
| False | `#FALSE` or `#0` | Boolean false |
| Pi | `#PI` | π (3.14159...) |
| E | `#E` | e (2.71828...) |
| Infinity | `#INF` | Infinity |
| Not a Number | `#NAN` | Quiet NaN |
| Maximum | `#MAX` | Maximum representable value |
| Minimum | `#MIN` | Minimum representable value |

**Syntax Examples:**

```assembly
; Boolean values
CMP R1, #TRUE          ; Compare with true
MOV R2, #FALSE         ; Initialize flag to false

; Mathematical constants
MOV R1, #PI            ; Load π
MUL R2, R2, #E         ; Multiply by e

; Special floating-point values
MOV R1, #INF           ; Positive infinity
MOV R2, #NAN           ; Not a number (quiet)
```

---

# Section 5: Remote Memory Operands

## 5.1 Remote Memory Syntax

Remote memory operands access memory on a different blade in the rack or across the optical fabric.

| Syntax | Component | Description |
|--------|-----------|-------------|
| `@blade:address` | blade (0-4095), address (0-2^64-1) | Remote memory access |
| `@rack:blade:address` | rack (0-255), blade (0-19), address | Multi-rack access |
| `@blade` | blade | Remote address in register |

**Syntax Examples:**

```assembly
; Direct remote memory access
MOV R1, @4:0x10000      ; Load from blade 4, address 0x10000
MOV @4:0x20000, R1      ; Store to blade 4, address 0x20000

; Multi-rack access (256 racks, 20 blades each)
MOV R1, @1:5:0x10000    ; Rack 1, blade 5, address 0x10000

; Remote address in register
LEA R1, @4:0x10000      ; Load remote address into register
MOV R2, [R1]            ; Use register as remote address
MOV [R1], R2            ; Store using remote address register

; Remote memory with offset
MOV R1, @4:0x10000 + 64 ; Load from blade 4, address 0x10040
MOV R1, @4:[R2]         ; Address in R2, on blade 4

; Remote memory with indexing
MOV R1, @4:[R2 + R3*8]  ; Indexed remote access
```

## 5.2 Remote Memory Size Specifications

```assembly
; Size-specified remote memory
MOV.B R1, @4:0x10000    ; Load byte from remote
MOV.W R1, @4:0x10000    ; Load word (16-bit) from remote
MOV.D R1, @4:0x10000    ; Load doubleword (32-bit) from remote
MOV.Q R1, @4:0x10000    ; Load quadword (64-bit) from remote
```

---

# Section 6: Vector Operands

## 6.1 Vector Register Syntax

Vector operands are used with SIMD instructions and can include element range specifications.

| Syntax | Description | Example |
|--------|-------------|---------|
| `Vn` | Full vector (all elements) | `V1` |
| `Vn[start:end]` | Range of elements (inclusive) | `V1[0:7]` |
| `Vn[start:end:stride]` | Strided range | `V1[0:15:2]` |
| `Vn.scalar` | Broadcast scalar from element 0 | `V1.S` |
| `Vn[element]` | Single element (scalar) | `V1[3]` |

**Syntax Examples:**

```assembly
; Full vector operations
ADDPS V1, V2, V3        ; All elements: V1[i] = V2[i] + V3[i]

; Element range
ADDPS V1[0:7], V2[0:7], V3[0:7]  ; First 8 elements only

; Strided range (every other element)
ADDPS V1[0:15:2], V2[0:15:2], V3[0:15:2]

; Broadcast scalar (element 0 to all positions)
ADDPS V1, V2, V3.S      ; V1[i] = V2[i] + V3[0]

; Single element access (scalar)
MOV R1, V1[3]           ; Move element 3 to scalar register
MOV V2[5], R1           ; Move scalar to vector element

; Vector mask operations
ADDPS.K V1, V2, V3, K1  ; Only elements where K1 bit is 1
```

## 6.2 Vector Element Types

| Suffix | Element Type | Size | Syntax Example |
|--------|--------------|------|----------------|
| (none) | Default | Variable | `V1[0]` |
| `.B` | Byte (INT8) | 8-bit | `V1.B[0]` |
| `.H` | Half-word (INT16) | 16-bit | `V1.H[0]` |
| `.W` | Word (INT32) | 32-bit | `V1.W[0]` |
| `.D` | Double-word (INT64) | 64-bit | `V1.D[0]` |
| `.S` | Single-precision float | 32-bit | `V1.S[0]` |
| `.D` | Double-precision float | 64-bit | `V1.D[0]` |

**Examples:**

```assembly
; Type-specified element access
MOV R1, V1.B[0]         ; Load 8-bit element (zero-extended)
MOV R1, V1.H[1]         ; Load 16-bit element
MOV R1, V1.S[2]         ; Load 32-bit float (converted to int)
MOV R1, V1.D[3]         ; Load 64-bit element

; Mixed-type vector operations
ADDPS.V V1.S, V2.S, V3.S ; Single-precision vector add
```

---

# Section 7: Register Type Map Operands

## 7.1 Type Map Syntax

The Register Type Map (RDTM) allows setting data types for registers.

| Syntax | Description | Example |
|--------|-------------|---------|
| `%R` | Type map for scalar register | `%R1` |
| `%V` | Type map for vector register | `%V32` |
| `%ALL` | Type map for all registers | `%ALL` |

**Type Map Values:**

| Value | Type | Bits | Description |
|-------|------|------|-------------|
| `#INT4` | Signed 4-bit integer | 4 | -8 to 7 |
| `#UINT4` | Unsigned 4-bit integer | 4 | 0 to 15 |
| `#INT8` | Signed 8-bit integer | 8 | -128 to 127 |
| `#UINT8` | Unsigned 8-bit integer | 8 | 0 to 255 |
| `#INT16` | Signed 16-bit integer | 16 | -32,768 to 32,767 |
| `#UINT16` | Unsigned 16-bit integer | 16 | 0 to 65,535 |
| `#INT32` | Signed 32-bit integer | 32 | -2.1e9 to 2.1e9 |
| `#UINT32` | Unsigned 32-bit integer | 32 | 0 to 4.3e9 |
| `#INT64` | Signed 64-bit integer | 64 | -9.2e18 to 9.2e18 |
| `#FP16` | Half-precision float | 16 | IEEE 754 half |
| `#BF16` | Brain float | 16 | Google bfloat16 |
| `#FP32` | Single-precision float | 32 | IEEE 754 single |
| `#FP64` | Double-precision float | 64 | IEEE 754 double |
| `#POSIT16` | Posit 16-bit | 16 | Type-III posit |
| `#POSIT32` | Posit 32-bit | 32 | Type-III posit |

**Syntax Examples:**

```assembly
; Set type for a single register
SET_REG_TYPE R1, #INT32
SET_REG_TYPE V1, #FP32
SET_REG_TYPE V2, #INT4

; Set type for all registers (global default)
SET_REG_MAP #MATH, #FP32, #V512, #NEAREST

; Query register type
GET_REG_TYPE R1, type_buffer
CMP type_buffer, #INT32
BRANCH EQ, is_int32

; Type conversion (hardware accelerated)
CVT R1, #FP32, V1, #INT4   ; Convert INT4 vector to FP32 scalar
```

---

# Section 8: Data Block Directives

## 8.1 Data Definition Directives

Directives for defining data blocks in assembly source code.

| Directive | Description | Size per Element | Example |
|-----------|-------------|------------------|---------|
| `DB` | Define byte | 1 byte | `DB 0x12, 0x34, 0x56` |
| `DW` | Define word | 2 bytes | `DW 0x1234, 0x5678` |
| `DD` | Define doubleword | 4 bytes | `DD 0x12345678` |
| `DQ` | Define quadword | 8 bytes | `DQ 0x123456789ABCDEF0` |
| `DO` | Define octaword | 16 bytes | `DO 0x1234...` |
| `DY` | Define 256-bit | 32 bytes | `DY 0x1234...` |
| `DZ` | Define 512-bit | 64 bytes | `DZ 0x1234...` |
| `DF` | Define float | 4 bytes | `DF 3.14159` |
| `DD` (float) | Define double | 8 bytes | `DD 3.141592653589793` |
| `DH` | Define half-float | 2 bytes | `DH 3.14` |
| `DP` | Define posit | 2/4/8 bytes | `DP 3.14159` |
| `DS` | Define string | 1 byte per char | `DS "Hello"` |
| `DBZ` | Define block of zeros | Variable | `DBZ 1024` |
| `ALIGN` | Align to boundary | N/A | `ALIGN 16` |

## 8.2 Data Block Syntax Examples

```assembly
; Section .data (read-write)
.data

; Byte data
int8_values:
    DB 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    DB -1, -2, -3
    DB 0xFF, 0x80                    ; 255, 128

; Word data (16-bit)
int16_values:
    DW 1000, 2000, 3000, 4000
    DW -1000, -2000
    DW 0xFFFF, 0x8000

; Doubleword data (32-bit)
int32_values:
    DD 1000000, 2000000, 3000000
    DD -1000000
    DD 0xFFFFFFFF, 0x80000000

; Quadword data (64-bit)
int64_values:
    DQ 10000000000, 20000000000
    DQ -10000000000
    DQ 0xFFFFFFFFFFFFFFFF

; Floating-point data
float_values:
    DF 3.14159, 2.71828, 1.41421   ; Single precision
    DD 3.141592653589793            ; Double precision
    DH 1.0, 0.5, 0.25              ; Half precision

; Posit data (for Posit arithmetic unit)
posit_values:
    DP 3.14159, #POSIT32           ; 32-bit posit
    DP 3.14159, #POSIT16           ; 16-bit posit

; String data
message:
    DS "Hello, World!\n"
    DB 0                            ; Null terminator

; Zero-initialized buffer
buffer:
    DBZ 1024                        ; 1KB of zeros

; Aligned data
.align 16
aligned_data:
    DQ 0x1122334455667788
    DQ 0xAABBCCDDEEFF0011
```

## 8.3 Section Directives

| Directive | Description | Default Attributes |
|-----------|-------------|--------------------|
| `.text` | Code section | Read-only, executable |
| `.data` | Data section | Read-write |
| `.rodata` | Read-only data | Read-only |
| `.bss` | Zero-initialized data | Read-write, zero-initialized |
| `.romb` | ROMB Gen2 section | Read-only, stored in optical memory |
| `.romb2` | ROMB Gen2 section (alias) | Read-only, stored in optical memory |

**Syntax Examples:**

```assembly
; Code section
.text
_start:
    MOV R1, #42
    HLT

; Read-only data (stored in DRAM)
.rodata
constants:
    DD 3.14159, 2.71828, 1.41421

; Read-write data
.data
variables:
    DQ 0
    DBZ 4096

; Zero-initialized data (does not occupy file space)
.bss
buffer:
    DBZ 65536

; ROMB Gen2 section (1.5TB optical memory)
.romb
model_weights:
    DZ 0x...    ; Large model weights
    DZ 0x...    ; Stored in optical memory (0.95ns access)
```

## 8.4 Label and Equate Directives

| Directive | Syntax | Description |
|-----------|--------|-------------|
| Label | `name:` | Symbol definition |
| Equate | `name EQU value` | Constant definition |
| Set | `name SET value` | Re-definable constant |
| Macro | `MACRO name args` | Macro definition |
| Endm | `ENDM` | Macro end |

**Syntax Examples:**

```assembly
; Label definition
start_of_code:
    MOV R1, #42
    JMP start_of_code

; Equate (constant)
SIZE EQU 1024
BUFFER_SIZE EQU 4096
PI EQU 3.141592653589793

; Set (re-definable)
VERSION SET 1
VERSION SET 2               ; Can be changed

; Macro definition
MACRO SAVE_REGS reglist
    PUSH reglist
ENDM

; Macro usage
SAVE_REGS {R1,R2,R3,R4}
```

---

# Section 9: Memory Addressing Examples

## 9.1 Array Access Patterns

```assembly
; 1D array access (C: arr[i])
; arr base in R1, index in R2, element size 8 bytes
LEA R3, [R1 + R2*8]        ; Address of arr[i]
MOV R4, [R3]               ; Load arr[i]

; 2D array access (C: arr[i][j])
; arr base in R1, i in R2, j in R3, rows=100, columns=50, element size 4 bytes
MUL R4, R2, #200           ; i * (columns * element_size) = i * 200
MUL R5, R3, #4             ; j * element_size = j * 4
LEA R6, [R1 + R4 + R5]     ; Address of arr[i][j]
MOV R7, [R6]               ; Load arr[i][j]

; 3D array access (C: arr[i][j][k])
; dims: d1=10, d2=20, d3=30, element size=2 bytes
MUL R4, R1, #1200          ; i * (d2*d3*elem) = i * 1200
MUL R5, R2, #60            ; j * (d3*elem) = j * 60
MUL R6, R3, #2             ; k * elem = k * 2
LEA R7, [R0 + R4 + R5 + R6] ; Address of arr[i][j][k]
```

## 9.2 Structure Access Patterns

```assembly
; Structure definition
; struct Point { int x; int y; int z; };  // 12 bytes
POINT_X EQU 0
POINT_Y EQU 4
POINT_Z EQU 8

; Array of structures
; arr of Points, base in R1, index in R2
MUL R3, R2, #12            ; Index * structure size
LEA R4, [R1 + R3]          ; Base of structure
MOV R5, [R4 + POINT_X]     ; Load point.x
MOV R6, [R4 + POINT_Y]     ; Load point.y
MOV R7, [R4 + POINT_Z]     ; Load point.z

; Nested structure
; struct Rectangle { struct Point top_left; struct Point bottom_right; }
RECT_TL_X EQU 0
RECT_TL_Y EQU 4
RECT_TL_Z EQU 8
RECT_BR_X EQU 12
RECT_BR_Y EQU 16
RECT_BR_Z EQU 20

; Access rectangle fields
LEA R4, [R1]               ; Rectangle base
MOV R5, [R4 + RECT_TL_X]   ; top_left.x
MOV R6, [R4 + RECT_BR_X]   ; bottom_right.x
```

## 9.3 Bit Field Access Patterns

```assembly
; Bit field extraction
; Extract bits 4-7 from R1 (4-bit field)
MOV R2, R1
SHR R2, R2, #4             ; Shift right by 4
AND R2, R2, #0x0F          ; Mask to 4 bits

; Extract bit field using mask (bits 8-15)
MOV R2, R1
AND R2, R2, #0xFF00        ; Mask bits 8-15
SHR R2, R2, #8             ; Shift down

; Set bit field (bits 4-7 to value in R3)
MOV R2, R1
AND R2, R2, #0xFFFFFF0F    ; Clear bits 4-7
SHL R4, R3, #4             ; Shift value to bits 4-7
OR R1, R2, R4              ; Combine
```

---

# Section 10: Complete Assembly Example

## 10.1 Matrix Multiplication Program

```assembly
;=============================================================================
; Matrix Multiplication Program
; Computes C = A × B where A, B, C are 1024x1024 FP32 matrices
; Uses the MATMULI4 instruction with INT4 quantization for inference
;=============================================================================

;=============================================================================
; Data Section
;=============================================================================
.data

; Matrix dimensions
M EQU 1024
K EQU 1024
N EQU 1024
MATRIX_SIZE EQU M * K * 4      ; 4MB per matrix (1024×1024×4 bytes)

; Matrix buffers (allocated in HBM)
.align 64
matrix_A:
    DBZ MATRIX_SIZE
matrix_B:
    DBZ MATRIX_SIZE
matrix_C:
    DBZ MATRIX_SIZE

; Quantization parameters
.align 16
scale_A:   DF 0.0078           ; Scale factor for matrix A (INT4)
scale_B:   DF 0.0078           ; Scale factor for matrix B (INT4)
scale_C:   DF 0.0078           ; Scale factor for output (FP32)

; Bias for activation
bias:
    DBZ 4096                    ; 1024 elements × 4 bytes

;=============================================================================
; Code Section
;=============================================================================
.text

;=============================================================================
; Main entry point
;=============================================================================
_start:
    ; Initialize type map for INT4 inference
    SET_REG_MAP #ACU, #INT4, #V512, #NEAREST

    ; Load matrices from ROMB (simulated - actual data would be in ROMB)
    DME_COPY.ROMB2 #0x200000000, matrix_A, MATRIX_SIZE
    DME_COPY.ROMB2 #0x200400000, matrix_B, MATRIX_SIZE

    ; Set quantization scales
    MOV R1, #scale_A
    SET_QUANT_SCALE #0, [R1]    ; Scale for tensor 0 (A)
    SET_QUANT_SCALE #1, scale_B ; Scale for tensor 1 (B)

    ; Perform matrix multiplication: C = A × B
    ; Using MATMULI4 which operates on INT4 and accumulates in 32-bit
    MATMULI4 matrix_C, matrix_A, matrix_B, #M, #K, #N

    ; Apply bias and ReLU activation
    MATMULI4.R matrix_C, matrix_C, bias, #M, #N, #1

    ; Store result back to ROMB (if needed)
    DME_COPY matrix_C, #0x200800000, MATRIX_SIZE

    ; Halt
    HLT

;=============================================================================
; Matrix multiplication using explicit loops (fallback)
;=============================================================================
matmul_scalar:
    ; Input: R1 = A base, R2 = B base, R3 = C base
    ; R4 = M, R5 = K, R6 = N

    ; Configure for FP32
    SET_REG_MAP #MATH, #FP32, #V512, #NEAREST

    MOV R7, #0                  ; i = 0
outer_loop:
    MOV R8, #0                  ; j = 0
middle_loop:
    MOV R9, #0                  ; k = 0
    MOV V0, #0.0                ; accumulator = 0
inner_loop:
    ; Load A[i][k] and B[k][j]
    LEA R10, [R1 + R7*R5*4 + R9*4]  ; A[i][k] address
    LEA R11, [R2 + R9*R6*4 + R8*4]  ; B[k][j] address
    LD.S V1, [R10]                  ; Load A[i][k]
    LD.S V2, [R11]                  ; Load B[k][j]

    ; FMA: accumulator += A[i][k] * B[k][j]
    FMA V0, V1, V2, V0

    ADD R9, #1
    CMP R9, R5
    BRANCH LT, inner_loop

    ; Store result to C[i][j]
    LEA R10, [R3 + R7*R6*4 + R8*4]
    ST.S [R10], V0

    ADD R8, #1
    CMP R8, R6
    BRANCH LT, middle_loop

    ADD R7, #1
    CMP R7, R4
    BRANCH LT, outer_loop

    RET

;=============================================================================
; Optimized matrix multiplication using vector FMA
;=============================================================================
matmul_vector:
    ; Input: R1 = A base, R2 = B base, R3 = C base
    ; R4 = M, R5 = K, R6 = N

    ; Each iteration processes 8 columns of C (256 bits = 8 × FP32)
    MOV R7, #0                  ; i = 0
v_outer_loop:
    MOV R8, #0                  ; j = 0 (in blocks of 8)
v_middle_loop:
    MOV V0, #0.0                ; Initialize accumulators (8 lanes)
    MOV V1, #0.0
    MOV V2, #0.0
    MOV V3, #0.0
    MOV V4, #0.0
    MOV V5, #0.0
    MOV V6, #0.0
    MOV V7, #0.0

    MOV R9, #0                  ; k = 0
v_inner_loop:
    ; Load row from A (8 elements)
    LEA R10, [R1 + R7*R5*4 + R9*4]
    LDPS V8, [R10]              ; Load 8 elements from A[i][k:k+7]

    ; Load 8 columns from B
    LEA R11, [R2 + R9*R6*4 + R8*32]  ; B[k][j:j+7]
    LDPS V9, [R11]              ; Load 8 elements from B[k][j:j+7]

    ; Multiply-add
    FMA.V V0, V8, V9, V0

    ADD R9, #1
    CMP R9, R5
    BRANCH LT, v_inner_loop

    ; Store results
    LEA R10, [R3 + R7*R6*4 + R8*32]
    STPS [R10], V0

    ADD R8, #8
    CMP R8, R6
    BRANCH LT, v_middle_loop

    ADD R7, #1
    CMP R7, R4
    BRANCH LT, v_outer_loop

    RET

;=============================================================================
; END OF PROGRAM
;=============================================================================
```

---

This document provides complete syntax documentation for all operand types supported by the Sirius NEXUS instruction set, including register operands, memory operands with all addressing modes, immediate operands in various formats, remote memory operands for distributed computing, vector operands with range specifications, register type map operands for mixed-precision computation, and data block directives for defining memory contents. The examples demonstrate practical usage patterns for arrays, structures, and complete programs.

This concludes Volume 1 of the Sirius NEXUS AI Processor Gen5 documentation. The complete instruction set comprises 132 instructions across 20 functional categories, with full encoding specifications for Math, Logic, and System cores. Each instruction is documented with assembly syntax, operand types, numerical formats, and multiple usage examples.
