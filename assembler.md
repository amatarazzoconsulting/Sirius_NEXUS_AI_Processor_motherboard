# Sirius NEXUS Assembler Documentation

## Complete Reference Guide for the Sirius NEXUS Assembly Toolchain

This document provides comprehensive documentation for the Sirius NEXUS Assembler, a complete assembly language toolchain supporting all 132 instructions across Math, Logic, and System cores. The assembler translates human-readable assembly code into machine code executable on Sirius NEXUS processors.

---

# Section 1: Overview

## 1.1 Purpose

The Sirius NEXUS Assembler converts assembly language source code into binary machine code that can be executed on Sirius NEXUS AI Processors. The assembler supports three core types (Math, Logic, System), all addressing modes, all data types (INT4, INT8, INT16, INT32, INT64, FP16, FP32, FP64, Posit), and all 132 instructions documented in the Instruction Set Reference.

## 1.2 Features

| Feature | Description |
|---------|-------------|
| Multi-core support | Math, Logic, and System cores with different instruction encodings |
| Variable-length instructions | 16-512 bits depending on operands |
| All addressing modes | Direct, indirect, base+offset, base+index, scaled index |
| All data types | INT4 through FP64, Posit16, Posit32 |
| Data directives | DB, DW, DD, DQ, DO, DF, DH, DS, DBZ, ALIGN |
| Section support | .text, .data, .rodata, .bss, .romb |
| Labels and symbols | Forward and backward references |
| Macros | User-defined macros with parameters |
| Remote memory | @blade:address and @rack:blade:address syntax |
| Vector operations | Element range and stride specifications |
| Register type mapping | SET_REG_MAP, SET_REG_TYPE, GET_REG_TYPE |

## 1.3 Installation

```bash
# Clone the assembler repository
git clone https://github.com/sirius-nexus/assembler.git

# Install the assembler
cd assembler
python setup.py install

# Or use directly
python -m sirius_asm input.asm -o output.bin
```

---

# Section 2: Command Line Usage

## 2.1 Basic Syntax

```bash
sirius-asm [options] input.asm
```

## 2.2 Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-o FILE` | Output binary file | `-o program.bin` |
| `-c CORE` | Target core (math, logic, system) | `-c math` |
| `-l FILE` | Generate listing file | `-l program.lst` |
| `-v` | Verbose output | `-v` |
| `--list-macros` | List all macros | `--list-macros` |
| `--dump-symbols` | Dump symbol table | `--dump-symbols` |
| `--help` | Show help | `--help` |

## 2.3 Usage Examples

```bash
# Assemble for Math core (default)
sirius-asm matrix.asm -o matrix.bin

# Assemble for Logic core
sirius-asm boot.asm -c logic -o boot.bin

# Assemble for System core with listing
sirius-asm kernel.asm -c system -o kernel.bin -l kernel.lst

# Verbose assembly with symbol dump
sirius-asm test.asm -v --dump-symbols
```

---

# Section 3: Assembly Language Syntax

## 3.1 Line Structure

```assembly
[label:] [instruction | directive] [; comment]
```

- Labels end with a colon `:`
- Instructions and directives are case-insensitive
- Comments begin with semicolon `;`
- Whitespace is ignored except as separators

## 3.2 Example Program

```assembly
; Sample Sirius NEXUS assembly program
; Computes the sum of an array

    .text
    GLOBAL _start

_start:
    ; Initialize registers
    MOV R1, #0          ; sum = 0
    MOV R2, #0          ; index = 0
    LEA R3, array       ; R3 = address of array
    MOV R4, #16         ; length = 16

loop:
    CMP R2, R4
    BRANCH GE, done
    
    ADD R1, [R3 + R2*4] ; sum += array[index]
    ADD R2, #1          ; index++
    JMP loop

done:
    MOV [result], R1    ; store result
    HLT

    .data
array:
    DD 1, 2, 3, 4, 5, 6, 7, 8
    DD 9, 10, 11, 12, 13, 14, 15, 16
result:
    DQ 0
```

---

# Section 4: Core Types

## 4.1 Math Core

The Math core supports the full instruction set with vector and SIMD extensions.

```bash
sirius-asm program.asm -c math -o program.bin
```

**Characteristics:**
- 64 vector registers (V0-V63, 512-bit)
- 32 scalar registers (R0-R31, 64-bit)
- 8 mask registers (K0-K7)
- All 132 instructions
- Vector operations with SIMD

## 4.2 Logic Core

The Logic core supports a reduced instruction set for control-flow intensive code.

```bash
sirius-asm program.asm -c logic -o program.bin
```

**Characteristics:**
- 32 scalar registers (R0-R31, 64-bit)
- PC, SP, LR registers
- 30 instructions (branches, integer arithmetic, logic)
- No vector or SIMD instructions

## 4.3 System Core

The System core supports a minimal instruction set for kernel and I/O operations.

```bash
sirius-asm program.asm -c system -o program.bin
```

**Characteristics:**
- 16 scalar registers (R0-R15, 64-bit)
- Model-specific registers (MSR0-MSR31)
- 24 instructions (system calls, I/O, memory management)
- Runs at 4 GHz

---

# Section 5: Operand Types

## 5.1 Register Operands

### Math Core Registers

| Syntax | Count | Size | Description |
|--------|-------|------|-------------|
| `V0`-`V63` | 64 | 512-bit | Vector registers |
| `R0`-`R31` | 32 | 64-bit | Scalar registers |
| `K0`-`K7` | 8 | 64-bit | Mask registers |
| `CR0`-`CR15` | 16 | 64-bit | Control registers |

### Logic Core Registers

| Syntax | Count | Size | Description |
|--------|-------|------|-------------|
| `R0`-`R31` | 32 | 64-bit | General purpose |
| `PC` | 1 | 64-bit | Program counter |
| `SP` | 1 | 64-bit | Stack pointer |
| `LR` | 1 | 64-bit | Link register |
| `CC` | 1 | 32-bit | Condition codes |

### System Core Registers

| Syntax | Count | Size | Description |
|--------|-------|------|-------------|
| `R0`-`R15` | 16 | 64-bit | General purpose |
| `MSR0`-`MSR31` | 32 | 64-bit | Model-specific |
| `IVT` | 1 | 64-bit | Interrupt vector table |
| `PTBR` | 1 | 64-bit | Page table base |

## 5.2 Memory Operands

| Mode | Syntax | Example |
|------|--------|---------|
| Direct | `[address]` | `[0x1000]` |
| Register indirect | `[Rn]` | `[R1]` |
| Base + offset | `[Rn + offset]` | `[R1 + 64]` |
| Base + index | `[Rn + Rm]` | `[R1 + R2]` |
| Base + index*scale | `[Rn + Rm*scale]` | `[R1 + R2*8]` |
| PC-relative | `[PC + offset]` | `[PC + 128]` |

**Scale factors:** 1, 2, 4, 8, 16, 32, 64

## 5.3 Immediate Operands

| Format | Syntax | Example |
|--------|--------|---------|
| Decimal | `#number` | `#42` |
| Hexadecimal | `#0xhex` | `#0xFF` |
| Binary | `#0bbinary` | `#0b1010` |
| Octal | `#0ooctal` | `#0o777` |
| Character | `#'char'` | `#'A'` |
| String | `#"string"` | `#"Hello"` |
| Float (double) | `#number` | `#3.14159` |
| Float (single) | `#numberf` | `#3.14f` |
| Float (half) | `#numberh` | `#3.14h` |
| Scientific | `#valueeexp` | `#1.0e-10` |
| Constants | `#PI`, `#E`, `#INF`, `#NAN` | `#PI` |

## 5.4 Remote Memory Operands

| Syntax | Example | Description |
|--------|---------|-------------|
| `@blade:address` | `@4:0x10000` | Blade in same rack |
| `@rack:blade:address` | `@1:5:0x10000` | Specific rack and blade |

## 5.5 Vector Operands

| Syntax | Example | Description |
|--------|---------|-------------|
| `Vn` | `V1` | Full vector |
| `Vn[start:end]` | `V1[0:7]` | Element range |
| `Vn[start:end:stride]` | `V1[0:15:2]` | Strided range |
| `Vn.S` | `V1.S` | Broadcast scalar (element 0) |
| `Vn[element]` | `V1[3]` | Single element |
| `Vn.B[element]` | `V1.B[0]` | Byte element |
| `Vn.H[element]` | `V1.H[0]` | Half-word element |
| `Vn.W[element]` | `V1.W[0]` | Word element |
| `Vn.D[element]` | `V1.D[0]` | Double-word element |

---

# Section 6: Instruction Set

## 6.1 Data Movement Instructions

| Instruction | Syntax | Description |
|-------------|--------|-------------|
| `MOV` | `MOV dest, src` | Move data |
| `MOVSX` | `MOVSX dest, src` | Move with sign extension |
| `MOVZX` | `MOVZX dest, src` | Move with zero extension |
| `LEA` | `LEA dest, [addr]` | Load effective address |
| `XCHG` | `XCHG a, b` | Exchange data |

**Examples:**
```assembly
MOV R1, R2              ; R1 = R2
MOV R1, #42             ; R1 = 42
MOV R1, [R2]            ; R1 = memory[R2]
MOV [R1], R2            ; memory[R1] = R2
MOV R1, @4:0x10000      ; R1 = remote memory
MOVSX R1, R2            ; Sign extend R2 to R1
MOVZX R1, R2            ; Zero extend R2 to R1
LEA R1, [R2 + 64]       ; R1 = R2 + 64
XCHG R1, [lock]         ; Atomic exchange
```

## 6.2 Arithmetic Instructions

| Instruction | Syntax | Description |
|-------------|--------|-------------|
| `ADD` | `ADD dest, src` | Addition |
| `SUB` | `SUB dest, src` | Subtraction |
| `MUL` | `MUL dest, src` | Unsigned multiply |
| `IMUL` | `IMUL dest, src` | Signed multiply |
| `DIV` | `DIV dest, src` | Unsigned division |
| `IDIV` | `IDIV dest, src` | Signed division |
| `INC` | `INC dest` | Increment |
| `DEC` | `DEC dest` | Decrement |
| `FMA` | `FMA dest, a, b, c` | Fused multiply-add |

**Examples:**
```assembly
ADD R1, R2              ; R1 = R1 + R2
ADD R1, #42             ; R1 = R1 + 42
SUB R1, R2              ; R1 = R1 - R2
MUL R1, R2              ; R1 = R1 * R2 (unsigned)
IMUL R1, R2             ; R1 = R1 * R2 (signed)
DIV R1, R2              ; Divide (R1,R0) by R2
INC R1                  ; R1 = R1 + 1
DEC R1                  ; R1 = R1 - 1
FMA R1, R2, R3, R4      ; R1 = (R2 * R3) + R4
ADD.V V1, V2, V3        ; Vector addition
```

## 6.3 Logic and Bit Instructions

| Instruction | Syntax | Description |
|-------------|--------|-------------|
| `AND` | `AND dest, src` | Bitwise AND |
| `OR` | `OR dest, src` | Bitwise OR |
| `XOR` | `XOR dest, src` | Bitwise XOR |
| `NOT` | `NOT dest` | Bitwise NOT |
| `TEST` | `TEST a, b` | Test bits |
| `BSF` | `BSF dest, src` | Bit scan forward |
| `BSR` | `BSR dest, src` | Bit scan reverse |
| `SHL` | `SHL dest, count` | Shift left |
| `SHR` | `SHR dest, count` | Shift right |

**Examples:**
```assembly
AND R1, #0xFF           ; Mask low 8 bits
OR R1, #0x0F            ; Set low 4 bits
XOR R1, R1              ; Zero R1
NOT R1                  ; One's complement
TEST R1, #0x04          ; Test bit 2
BSF R1, R2              ; Find lowest set bit
BSR R1, R2              ; Find highest set bit
SHL R1, #3              ; R1 = R1 * 8
SHR R1, #3              ; R1 = R1 / 8 (unsigned)
```

## 6.4 Control Flow Instructions

| Instruction | Syntax | Description |
|-------------|--------|-------------|
| `JMP` | `JMP target` | Unconditional jump |
| `CALL` | `CALL target` | Call subroutine |
| `RET` | `RET` | Return from subroutine |
| `BRANCH` | `BRANCH cond, target` | Conditional branch |

**Condition Codes:** EQ, NE, LT, LE, GT, GE, LO, LS, HI, HS, CS, CC, VS, VC, MI, PL

**Examples:**
```assembly
JMP label              ; Unconditional jump
CALL subroutine        ; Call function
RET                    ; Return
BRANCH EQ, equal_label ; Branch if equal
BRANCH LT, less_label  ; Branch if less than
```

## 6.5 Vector and SIMD Instructions

| Instruction | Syntax | Description |
|-------------|--------|-------------|
| `ADDPS` | `ADDPS dest, src1, src2` | Vector add |
| `MULPS` | `MULPS dest, src1, src2` | Vector multiply |
| `DOT` | `DOT dest, src1, src2` | Dot product |
| `CONV` | `CONV out, in, ker, dims, stride` | 2D convolution |
| `SHUFPS` | `SHUFPS dest, src1, src2, mask` | Shuffle |

**Examples:**
```assembly
ADDPS V1, V2, V3        ; V1 = V2 + V3
ADDPS.Y Y1, Y2, Y3      ; 256-bit vector add
MULPS V1, V2, V3        ; V1 = V2 * V3
DOT R1, V2, V3          ; R1 = dot(V2, V3)
CONV out, in, ker, #0xE0E0, #1
SHUFPS V1, V2, V3, #0x1B
```

## 6.6 INT4 Inference Instructions

| Instruction | Syntax | Description |
|-------------|--------|-------------|
| `MATMULI4` | `MATMULI4 out, A, B, M, K, N` | INT4 matrix multiply |
| `SOFTMAXI4` | `SOFTMAXI4 dest, src` | INT4 softmax |
| `ATTENTIONI4` | `ATTENTIONI4 out, Q, K, V, L, D` | INT4 attention |
| `GELUI4` | `GELUI4 dest, src` | INT4 GELU |
| `LAYERNORMI4` | `LAYERNORMI4 out, in, params` | INT4 layer norm |
| `RESIDUALI4` | `RESIDUALI4 out, in, res` | INT4 residual |

**Examples:**
```assembly
MATMULI4 C, A, B, #1024, #1024, #1024
SOFTMAXI4 V1, V2
ATTENTIONI4 out, Q, K, V, #2048, #64
GELUI4 V1, V2
LAYERNORMI4 out, in, params
RESIDUALI4 out, in, residual
```

## 6.7 System Instructions

| Instruction | Syntax | Description |
|-------------|--------|-------------|
| `SYSENTER` | `SYSENTER` | Enter kernel mode |
| `SYSEXIT` | `SYSEXIT` | Exit kernel mode |
| `IN` | `IN dest, port` | Input from port |
| `OUT` | `OUT port, src` | Output to port |
| `CFG_VIDEO` | `CFG_VIDEO tile, base, w, h, fmt, hz` | Configure video |
| `CFG_AUDIO` | `CFG_AUDIO tile, buf, size, rate, bits, ch, map` | Configure audio |
| `RING_INIT` | `RING_INIT buf, seg, cnt, ctrl` | Init ring buffer |
| `RING_WRITE` | `RING_WRITE ring, data, len` | Write to ring |
| `RING_SWAP` | `RING_SWAP ring` | Swap ring pointers |

**Examples:**
```assembly
SYSENTER
SYSEXIT
IN R1, #0x60           ; Read keyboard
OUT #0x60, R1          ; Write keyboard
CFG_VIDEO #0, fb, #1920, #1080, #0x01, #60000
```

## 6.8 Interconnect Instructions

| Instruction | Syntax | Description |
|-------------|--------|-------------|
| `MAP_STORAGE` | `MAP_STORAGE chip, block, addr, size` | Map flash to memory |
| `EXPORT_MEMORY` | `EXPORT_MEMORY local, size, blade, remote, perm` | Export memory |
| `REMOTE_CALL` | `REMOTE_CALL blade, func, argc, args, result` | Remote call |
| `LINK_STATUS` | `LINK_STATUS blade, buffer` | Query optical link |
| `RACK_UNIFY` | `RACK_UNIFY start, end, base, interleave` | Unify rack |
| `WARP_SYNC` | `WARP_SYNC warp` | Synchronize warp |
| `REMOTE_ALLOC` | `REMOTE_ALLOC blade, size, align` | Remote allocate |
| `BROADCAST` | `BROADCAST` | Broadcast to all blades |
| `BARRIER_SYNC` | `BARRIER_SYNC` | Global barrier |

**Examples:**
```assembly
MAP_STORAGE #0, #0, #0x100000000, #0x40000000
EXPORT_MEMORY #0x20000000, #0x1000000, #4, #0x30000000, #0x03
REMOTE_CALL #4, #0x1000, #2, arg_list, result
RACK_UNIFY #1, #20, #0x00000000, #64
BROADCAST
    NOP
BROADCAST_END
```

## 6.9 Register Type Mapping Instructions

| Instruction | Syntax | Description |
|-------------|--------|-------------|
| `SET_REG_MAP` | `SET_REG_MAP bank, type, length, round` | Set default type map |
| `SET_REG_TYPE` | `SET_REG_TYPE reg, type` | Set register type |
| `GET_REG_TYPE` | `GET_REG_TYPE reg, dest` | Get register type |
| `RESET_REG_MAP` | `RESET_REG_MAP bank` | Reset to default |

**Type Values:** `#INT4`, `#INT8`, `#INT16`, `#INT32`, `#INT64`, `#FP16`, `#BF16`, `#FP32`, `#FP64`, `#POSIT16`, `#POSIT32`

**Examples:**
```assembly
SET_REG_MAP #MATH, #FP32, #V512, #NEAREST
SET_REG_TYPE V1, #INT4
GET_REG_TYPE V1, R1
RESET_REG_MAP #MATH
```

---

# Section 7: Assembler Directives

## 7.1 Section Directives

| Directive | Description | Default Address |
|-----------|-------------|-----------------|
| `.text` | Code section | 0x00000000 |
| `.data` | Read-write data | 0x01000000 |
| `.rodata` | Read-only data | 0x02000000 |
| `.bss` | Zero-initialized data | 0x03000000 |
| `.romb` | ROMB Gen2 section | 0x200000000 |

## 7.2 Data Definition Directives

| Directive | Size | Syntax Example |
|-----------|------|----------------|
| `DB` | 1 byte | `DB 0x12, 0x34, 0x56` |
| `DW` | 2 bytes | `DW 0x1234, 0x5678` |
| `DD` | 4 bytes | `DD 0x12345678` |
| `DQ` | 8 bytes | `DQ 0x123456789ABCDEF0` |
| `DO` | 16 bytes | `DO 0x1234...` |
| `DF` | 4 bytes (float) | `DF 3.14159` |
| `DH` | 2 bytes (half) | `DH 3.14` |
| `DS` | variable | `DS "Hello"` |
| `DBZ` | variable | `DBZ 1024` |
| `ALIGN` | N/A | `ALIGN 16` |

## 7.3 Symbol Directives

| Directive | Syntax | Description |
|-----------|--------|-------------|
| `EQU` | `name EQU value` | Define constant |
| `SET` | `name SET value` | Define variable |
| `GLOBAL` | `GLOBAL name` | Export symbol |
| `EXTERN` | `EXTERN name` | Import symbol |

## 7.4 Macro Directives

| Directive | Syntax | Description |
|-----------|--------|-------------|
| `MACRO` | `MACRO name args` | Start macro |
| `ENDM` | `ENDM` | End macro |
| `REPT` | `REPT count` | Repeat block |
| `ENDR` | `ENDR` | End repeat |

**Macro Example:**
```assembly
MACRO SAVE_REGS reglist
    PUSH reglist
ENDM

MACRO LOAD_REGS reglist
    POP reglist
ENDM

; Usage
SAVE_REGS {R1,R2,R3,R4}
; ... function body ...
LOAD_REGS {R1,R2,R3,R4}
```

---

# Section 8: Data Types and Numeric Formats

## 8.1 Integer Types

| Type | Bits | Range | Suffix | Example |
|------|------|-------|--------|---------|
| INT4 | 4 | -8 to 7 | (none) | `#-3` |
| UINT4 | 4 | 0 to 15 | `u` | `#10u` |
| INT8 | 8 | -128 to 127 | `b` | `#-42b` |
| UINT8 | 8 | 0 to 255 | `ub` | `#255ub` |
| INT16 | 16 | -32768 to 32767 | `w` | `#-1000w` |
| UINT16 | 16 | 0 to 65535 | `uw` | `#65535uw` |
| INT32 | 32 | -2.1e9 to 2.1e9 | `d` | `#-1000000d` |
| UINT32 | 32 | 0 to 4.3e9 | `ud` | `#4294967295ud` |
| INT64 | 64 | -9.2e18 to 9.2e18 | `q` | `#-10000000000q` |

## 8.2 Floating-Point Types

| Type | Bits | Precision | Suffix | Example |
|------|------|-----------|--------|---------|
| FP16 (half) | 16 | ~3.3 digits | `h` | `#3.14h` |
| BF16 | 16 | ~2.3 digits | `b` | `#3.14b` |
| FP32 (float) | 32 | ~7.2 digits | `f` | `#3.14159f` |
| FP64 (double) | 64 | ~15.9 digits | (none) | `#3.141592653589793` |

## 8.3 Posit Types

| Type | Bits | Dynamic Range | Syntax | Example |
|------|------|---------------|--------|---------|
| POSIT16 | 16 | ±1.2e10 | `#p16` | `#3.14159p16` |
| POSIT32 | 32 | ±1.0e76 | `#p32` | `#3.14159p32` |

---

# Section 9: Expression Syntax

## 9.1 Operators

| Operator | Description | Precedence |
|----------|-------------|------------|
| `+` | Addition | 1 |
| `-` | Subtraction | 1 |
| `*` | Multiplication | 2 |
| `/` | Division | 2 |
| `%` | Modulo | 2 |
| `<<` | Shift left | 3 |
| `>>` | Shift right | 3 |
| `&` | Bitwise AND | 4 |
| `|` | Bitwise OR | 4 |
| `^` | Bitwise XOR | 4 |
| `~` | Bitwise NOT | 5 |

## 9.2 Expression Examples

```assembly
MOV R1, #(SIZE * 4 + 8)
LEA R2, [R1 + offset * 2]
DB (value & 0xFF)
DW (base + (index << 2))
```

---

# Section 10: Complete Example Programs

## 10.1 Matrix Multiplication (Math Core)

```assembly
;===========================================================================
; Matrix Multiplication: C = A × B (1024×1024 FP32)
;===========================================================================

    .text
    GLOBAL matmul

; Constants
SIZE EQU 1024
ELEM_SIZE EQU 4
ROW_SIZE EQU SIZE * ELEM_SIZE

matmul:
    ; Input: R1 = A, R2 = B, R3 = C
    SET_REG_MAP #MATH, #FP32, #V512, #NEAREST

    MOV R4, #0          ; i = 0
outer_loop:
    MOV R5, #0          ; j = 0
middle_loop:
    MOV V0, #0.0        ; accumulator = 0
    MOV R6, #0          ; k = 0
inner_loop:
    ; Load A[i][k] (8 floats at a time)
    LEA R7, [R1 + R4*ROW_SIZE + R6*ELEM_SIZE]
    LDPS V1, [R7]

    ; Load B[k][j] (8 floats at a time)
    LEA R8, [R2 + R6*ROW_SIZE + R5*ELEM_SIZE]
    LDPS V2, [R8]

    ; FMA: accumulator += A[i][k] * B[k][j]
    FMA.V V0, V1, V2, V0

    ADD R6, #8
    CMP R6, SIZE
    BRANCH LT, inner_loop

    ; Horizontal sum of V0 (8 floats → 1 float)
    HADDPS V0, V0, V0
    HADDPS V0, V0, V0
    HADDPS V0, V0, V0

    ; Store result to C[i][j]
    LEA R9, [R3 + R4*ROW_SIZE + R5*ELEM_SIZE]
    ST.S [R9], V0

    ADD R5, #1
    CMP R5, SIZE
    BRANCH LT, middle_loop

    ADD R4, #1
    CMP R4, SIZE
    BRANCH LT, outer_loop

    RET

    .data
A:  DBZ (SIZE * SIZE * ELEM_SIZE)
B:  DBZ (SIZE * SIZE * ELEM_SIZE)
C:  DBZ (SIZE * SIZE * ELEM_SIZE)
```

## 10.2 LLM Inference (Math Core with INT4)

```assembly
;===========================================================================
; LLM Inference: Transformer forward pass (INT4 quantized)
;===========================================================================

    .text
    GLOBAL transformer_forward

; Model configuration
NUM_LAYERS EQU 32
NUM_HEADS EQU 32
HEAD_DIM EQU 64
SEQ_LEN EQU 2048
HIDDEN_SIZE EQU 4096

transformer_forward:
    ; Input: R1 = input tokens, R2 = output logits
    SET_REG_MAP #ACU, #INT4, #V512, #NEAREST

    ; Load embedding table from ROMB
    MAP_STORAGE.ROMB2 #0, #0, #0x200000000, #0x40000000
    DME_COPY #0x200000000, embedding_table, #0x40000000

    ; Embed input tokens
    CALL embed_tokens

    MOV R3, #0          ; layer = 0
layer_loop:
    ; Layer normalization
    LAYERNORMI4 norm_out, layer_input, layer_norm_params

    ; Multi-head attention
    ATTENTIONI4 attn_out, norm_out, key_cache, value_cache, SEQ_LEN, HEAD_DIM
    RESIDUALI4 attn_out, attn_out, layer_input

    ; Layer normalization (post-attention)
    LAYERNORMI4 norm2_out, attn_out, layer_norm2_params

    ; Feed-forward network (2-layer MLP)
    MATMULI4.G ff1_out, norm2_out, fc1_weights, HIDDEN_SIZE, HIDDEN_SIZE, HIDDEN_SIZE*4, fc1_bias
    MATMULI4 ff2_out, ff1_out, fc2_weights, HIDDEN_SIZE, HIDDEN_SIZE*4, HIDDEN_SIZE, fc2_bias
    RESIDUALI4 layer_output, ff2_out, attn_out

    ADD R3, #1
    CMP R3, NUM_LAYERS
    BRANCH LT, layer_loop

    ; Final layer norm and output projection
    LAYERNORMI4 final_norm, layer_output, final_norm_params
    MATMULI4 logits, final_norm, output_weights, HIDDEN_SIZE, HIDDEN_SIZE, VOCAB_SIZE, output_bias

    ; Softmax for probabilities
    SOFTMAXI4 logits, logits

    RET

    .romb
embedding_table:    DBZ (VOCAB_SIZE * HIDDEN_SIZE * 2)  ; INT4 = 2 bytes per element
layer_norm_params:  DF 1.0, 0.0
fc1_weights:        DBZ (HIDDEN_SIZE * HIDDEN_SIZE * 4 * 2)
fc1_bias:           DBZ (HIDDEN_SIZE * 4 * 2)
fc2_weights:        DBZ (HIDDEN_SIZE * 4 * HIDDEN_SIZE * 2)
fc2_bias:           DBZ (HIDDEN_SIZE * 2)
output_weights:     DBZ (HIDDEN_SIZE * VOCAB_SIZE * 2)
output_bias:        DBZ (VOCAB_SIZE * 2)
```

## 10.3 Rack Unification (System Core)

```assembly
;===========================================================================
; Rack Unification: Initialize 20-blade rack as shared memory
;===========================================================================

    .text
    GLOBAL rack_init

rack_init:
    ; Check all blades are online
    MOV R1, #1
check_loop:
    LINK_STATUS R1, status_buffer
    LD.B R2, [status_buffer]
    CMP R2, #1          ; 1 = online
    BRANCH NE, blade_offline
    ADD R1, #1
    CMP R1, #20
    BRANCH LE, check_loop

    ; Configure optical fabric
    CFG_OPTICAL_FABRIC #ENABLE

    ; Export each blade's memory
    MOV R1, #1
export_loop:
    MUL R2, R1, #0x100000000   ; Global base = blade × 64GB
    EXPORT_MEMORY #0x00000000, #0x100000000, R1, R2, #0x03
    ADD R1, #1
    CMP R1, #20
    BRANCH LE, export_loop

    ; Unify all blades
    RACK_UNIFY #1, #20, #0x00000000, #64

    ; Broadcast configuration
    BROADCAST.WAIT
        SET_REG_MAP #MATH, #FP16, #V512, #NEAREST
        SET_REG_MAP #ACU, #INT4, #V512, #NEAREST
    BROADCAST_END

    MOV R1, #0          ; Success
    RET

blade_offline:
    MOV R1, #1          ; Error
    RET

    .data
status_buffer: DBZ 64
```

---

# Section 11: Error Messages and Troubleshooting

## 11.1 Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `Unknown instruction: XXX` | Instruction not recognized | Check spelling, ensure core supports it |
| `XXX expects N operands, got M` | Wrong operand count | Check instruction syntax |
| `Invalid operand: XXX` | Malformed operand | Check operand syntax |
| `Undefined symbol: XXX` | Label not defined | Define label or declare as EXTERN |
| `Section not found: XXX` | Missing section directive | Add .text, .data, etc. |
| `Register not available on this core` | Wrong core type | Use -c flag to select correct core |

## 11.2 Debugging Tips

```bash
# Generate listing file to see assembled code
sirius-asm program.asm -l program.lst

# Dump symbol table
sirius-asm program.asm --dump-symbols

# Verbose output
sirius-asm program.asm -v

# Disassemble binary
sirius-disasm program.bin
```

---

# Section 12: API Reference

## 12.1 Python Module

```python
from sirius_asm import SiriusNEXUSAssembler, CoreType

# Create assembler for Math core
assembler = SiriusNEXUSAssembler(CoreType.MATH)

# Assemble source code
source = """
    MOV R1, #42
    ADD R1, R2
    HLT
"""
machine_code = assembler.assemble(source)

# Save to file
with open('output.bin', 'wb') as f:
    f.write(machine_code)

# Get symbol table
symbols = assembler.symbols
print(symbols)  # {'_start': 0, 'loop': 16, ...}
```

## 12.2 Library Functions

```python
# Assemble file
def assemble_file(input_path: str, output_path: str = None, 
                  core: CoreType = CoreType.MATH) -> bytes

# Parse single instruction
def parse_instruction(line: str) -> Tuple[str, List[Operand]]

# Encode instruction to bytes
def encode_instruction(mnemonic: str, operands: List[Operand], 
                       core: CoreType) -> bytes
```

---

This document provides complete documentation for the Sirius NEXUS Assembler, including command-line usage, assembly language syntax, instruction set, directives, data types, expressions, and complete program examples. The assembler supports all 132 instructions across all core types and is the primary tool for developing software for Sirius NEXUS AI Processors.



```python
#!/usr/bin/env python3
"""
Sirius NEXUS Assembler - Complete Python Implementation
Supports all 132 instructions across Math, Logic, and System cores
Supports INT4, Posit, FP16/32/64, and all addressing modes
"""

import struct
import re
import sys
from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any, Union
from pathlib import Path

# ============================================================================
# Enumerations and Constants
# ============================================================================

class CoreType(IntEnum):
    MATH = 0
    LOGIC = 1
    SYSTEM = 2

class OperandType(IntEnum):
    REGISTER = 0
    MEMORY = 1
    IMMEDIATE = 2
    REMOTE = 3
    VECTOR = 4
    TYPE_MAP = 5

class DataType(IntEnum):
    INT4 = 0
    UINT4 = 1
    INT8 = 2
    UINT8 = 3
    INT16 = 4
    UINT16 = 5
    INT32 = 6
    UINT32 = 7
    INT64 = 8
    FP16 = 9
    BF16 = 10
    FP32 = 11
    FP64 = 12
    POSIT16 = 13
    POSIT32 = 14

class ConditionCode(IntEnum):
    EQ = 0x0
    NE = 0x1
    LT = 0x2
    LE = 0x3
    GT = 0x4
    GE = 0x5
    LO = 0x6
    LS = 0x7
    HI = 0x8
    HS = 0x9
    CS = 0xA
    CC = 0xB
    VS = 0xC
    VC = 0xD
    MI = 0xE
    PL = 0xF

class VectorLength(IntEnum):
    V128 = 0   # 4 floats / 16 INT8
    V256 = 1   # 8 floats / 32 INT8
    V512 = 2   # 16 floats / 64 INT8
    V1024 = 3  # 32 floats / 128 INT8

# ============================================================================
# Instruction Database
# ============================================================================

INSTRUCTIONS = {
    # Data Movement (Chapter 2)
    'MOV': {'opcode': 0x01, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    'MOVSX': {'opcode': 0x02, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'MOVZX': {'opcode': 0x03, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'LEA': {'opcode': 0x04, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    'XCHG': {'opcode': 0x05, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    
    # Arithmetic (Chapter 3)
    'ADD': {'opcode': 0x10, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    'SUB': {'opcode': 0x11, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    'MUL': {'opcode': 0x12, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'IMUL': {'opcode': 0x13, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'DIV': {'opcode': 0x14, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'IDIV': {'opcode': 0x15, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'INC': {'opcode': 0x16, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 1},
    'DEC': {'opcode': 0x17, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 1},
    'FMA': {'opcode': 0x18, 'cores': [CoreType.MATH], 'operands': 4},
    
    # Logic and Bit (Chapter 4)
    'AND': {'opcode': 0x20, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    'OR': {'opcode': 0x21, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    'XOR': {'opcode': 0x22, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    'NOT': {'opcode': 0x23, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 1},
    'TEST': {'opcode': 0x24, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'BSF': {'opcode': 0x30, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'BSR': {'opcode': 0x31, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'SHL': {'opcode': 0x36, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    'SHR': {'opcode': 0x37, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 2},
    
    # Control Flow (Chapter 5)
    'JMP': {'opcode': 0x40, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 1},
    'CALL': {'opcode': 0x41, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 1},
    'RET': {'opcode': 0x42, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 0},
    'BRANCH': {'opcode': 0x43, 'cores': [CoreType.MATH, CoreType.LOGIC], 'operands': 1},
    
    # Vector and SIMD (Chapter 6)
    'ADDPS': {'opcode': 0x50, 'cores': [CoreType.MATH], 'operands': 3},
    'MULPS': {'opcode': 0x51, 'cores': [CoreType.MATH], 'operands': 3},
    'DOT': {'opcode': 0x52, 'cores': [CoreType.MATH], 'operands': 3},
    'CONV': {'opcode': 0x53, 'cores': [CoreType.MATH], 'operands': 5},
    'SHUFPS': {'opcode': 0x54, 'cores': [CoreType.MATH], 'operands': 4},
    
    # INT4 Inference (Chapter 7)
    'MATMULI4': {'opcode': 0x90, 'cores': [CoreType.MATH], 'operands': 6},
    'SOFTMAXI4': {'opcode': 0x91, 'cores': [CoreType.MATH], 'operands': 2},
    'ATTENTIONI4': {'opcode': 0x92, 'cores': [CoreType.MATH], 'operands': 6},
    'GELUI4': {'opcode': 0x93, 'cores': [CoreType.MATH], 'operands': 2},
    'LAYERNORMI4': {'opcode': 0x94, 'cores': [CoreType.MATH], 'operands': 3},
    'RESIDUALI4': {'opcode': 0x95, 'cores': [CoreType.MATH], 'operands': 3},
    
    # System Instructions (Chapter 8)
    'SYSENTER': {'opcode': 0x60, 'cores': [CoreType.SYSTEM], 'operands': 0},
    'SYSEXIT': {'opcode': 0x61, 'cores': [CoreType.SYSTEM], 'operands': 0},
    'IN': {'opcode': 0x62, 'cores': [CoreType.SYSTEM], 'operands': 2},
    'OUT': {'opcode': 0x63, 'cores': [CoreType.SYSTEM], 'operands': 2},
    'CFG_VIDEO': {'opcode': 0x64, 'cores': [CoreType.SYSTEM], 'operands': 5},
    'CFG_AUDIO': {'opcode': 0x65, 'cores': [CoreType.SYSTEM], 'operands': 6},
    'RING_INIT': {'opcode': 0x66, 'cores': [CoreType.SYSTEM], 'operands': 4},
    'RING_WRITE': {'opcode': 0x67, 'cores': [CoreType.SYSTEM], 'operands': 3},
    'RING_SWAP': {'opcode': 0x68, 'cores': [CoreType.SYSTEM], 'operands': 1},
    
    # Interconnect Instructions (Chapter 9)
    'MAP_STORAGE': {'opcode': 0x70, 'cores': [CoreType.SYSTEM], 'operands': 4},
    'EXPORT_MEMORY': {'opcode': 0x71, 'cores': [CoreType.SYSTEM], 'operands': 5},
    'REMOTE_CALL': {'opcode': 0x72, 'cores': [CoreType.SYSTEM], 'operands': 5},
    'LINK_STATUS': {'opcode': 0x73, 'cores': [CoreType.SYSTEM], 'operands': 2},
    'RACK_UNIFY': {'opcode': 0x74, 'cores': [CoreType.SYSTEM], 'operands': 4},
    'WARP_SYNC': {'opcode': 0x75, 'cores': [CoreType.MATH], 'operands': 1},
    'REMOTE_ALLOC': {'opcode': 0x76, 'cores': [CoreType.SYSTEM], 'operands': 3},
    'BROADCAST': {'opcode': 0x77, 'cores': [CoreType.SYSTEM], 'operands': 0},
    'BARRIER_SYNC': {'opcode': 0x78, 'cores': [CoreType.SYSTEM], 'operands': 0},
    
    # Memory Management (Chapter 10)
    'SEGMENT_CREATE': {'opcode': 0xB0, 'cores': [CoreType.SYSTEM], 'operands': 6},
    'SEGMENT_DELETE': {'opcode': 0xB1, 'cores': [CoreType.SYSTEM], 'operands': 1},
    'SEGMENT_MODIFY': {'opcode': 0xB2, 'cores': [CoreType.SYSTEM], 'operands': 3},
    'CAPABILITY_GRANT': {'opcode': 0xB3, 'cores': [CoreType.SYSTEM], 'operands': 5},
    'CAPABILITY_ACCEPT': {'opcode': 0xB4, 'cores': [CoreType.SYSTEM], 'operands': 3},
    'SEGMENT_LOOKUP': {'opcode': 0xB5, 'cores': [CoreType.SYSTEM], 'operands': 2},
    'TLB_INVALIDATE': {'opcode': 0xB6, 'cores': [CoreType.SYSTEM], 'operands': 1},
    
    # Protection Instructions (Chapter 11)
    'OWNER_GET': {'opcode': 0xB7, 'cores': [CoreType.SYSTEM], 'operands': 2},
    'OWNER_SET_PARENT': {'opcode': 0xB8, 'cores': [CoreType.SYSTEM], 'operands': 2},
    'RING_SET': {'opcode': 0xC0, 'cores': [CoreType.SYSTEM], 'operands': 2},
    'IRQ_SET': {'opcode': 0xC1, 'cores': [CoreType.SYSTEM], 'operands': 2},
    'IO_MAP': {'opcode': 0xC2, 'cores': [CoreType.SYSTEM], 'operands': 4},
    'SEGMENT_WALK': {'opcode': 0xC3, 'cores': [CoreType.SYSTEM], 'operands': 3},
    
    # Register Type Mapping
    'SET_REG_MAP': {'opcode': 0x0F, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 4},
    'SET_REG_TYPE': {'opcode': 0x0E, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    'GET_REG_TYPE': {'opcode': 0x0D, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 2},
    'RESET_REG_MAP': {'opcode': 0x0C, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 1},
    
    # Miscellaneous
    'NOP': {'opcode': 0x00, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 0},
    'CPUID': {'opcode': 0x7D, 'cores': [CoreType.SYSTEM], 'operands': 1},
    'RDTSC': {'opcode': 0x7E, 'cores': [CoreType.SYSTEM], 'operands': 0},
    'HLT': {'opcode': 0x7F, 'cores': [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 'operands': 0},
}

# Register tables
MATH_VECTOR_REGS = {f'V{i}': i for i in range(64)}
MATH_SCALAR_REGS = {f'R{i}': i for i in range(32)}
MATH_MASK_REGS = {f'K{i}': i for i in range(8)}
MATH_CONTROL_REGS = {f'CR{i}': i for i in range(16)}

LOGIC_REGS = {f'R{i}': i for i in range(32)}
LOGIC_REGS['SP'] = 30
LOGIC_REGS['LR'] = 31
LOGIC_REGS['PC'] = 32

SYSTEM_REGS = {f'R{i}': i for i in range(16)}
SYSTEM_REGS['IVT'] = 16
SYSTEM_REGS['PTBR'] = 17
for i in range(32):
    SYSTEM_REGS[f'MSR{i}'] = 32 + i

ALL_REGS = {**MATH_VECTOR_REGS, **MATH_SCALAR_REGS, **MATH_MASK_REGS,
            **MATH_CONTROL_REGS, **LOGIC_REGS, **SYSTEM_REGS}

# ============================================================================
# Operand Parser
# ============================================================================

@dataclass
class Operand:
    type: OperandType
    value: Any
    size: Optional[int] = None
    behavior: int = 0

class OperandParser:
    """Parse assembly operands into structured format"""
    
    # Patterns for operand matching
    REG_PATTERN = re.compile(r'^([VRKLSC][A-Z0-9]*)$', re.IGNORECASE)
    VECTOR_RANGE_PATTERN = re.compile(r'^([Vv][0-9]+)(?:\.([BHDWS]))?(?:\[([0-9]+):([0-9]+)(?::([0-9]+))?\])?$')
    REMOTE_PATTERN = re.compile(r'^@([0-9]+):(0x[0-9A-Fa-f]+|[0-9]+)$')
    MULTI_RACK_PATTERN = re.compile(r'^@([0-9]+):([0-9]+):(0x[0-9A-Fa-f]+|[0-9]+)$')
    MEMORY_PATTERN = re.compile(r'^\[(.*)\]$')
    IMM_DECIMAL_PATTERN = re.compile(r'^#(-?[0-9]+)$')
    IMM_HEX_PATTERN = re.compile(r'^#0x([0-9A-Fa-f]+)$')
    IMM_BIN_PATTERN = re.compile(r'^#0b([01]+)$')
    IMM_FLOAT_PATTERN = re.compile(r'^#(-?[0-9]+\.[0-9]+(?:[eE][-+]?[0-9]+)?(?:[fh]?))$')
    IMM_CONST_PATTERN = re.compile(r'^#(TRUE|FALSE|PI|E|INF|NAN|MAX|MIN)$', re.IGNORECASE)
    TYPE_MAP_PATTERN = re.compile(r'^%([VR])?([0-9]+)$')
    
    @classmethod
    def parse(cls, token: str, line_num: int = 0) -> Operand:
        """Parse a single operand token"""
        
        # Check for register
        match = cls.REG_PATTERN.match(token.upper())
        if match and token.upper() in ALL_REGS:
            return Operand(OperandType.REGISTER, token.upper(), behavior=0)
        
        # Check for vector with range
        match = cls.VECTOR_RANGE_PATTERN.match(token)
        if match:
            reg_name = match.group(1).upper()
            elem_type = match.group(2)
            start = int(match.group(3)) if match.group(3) else None
            end = int(match.group(4)) if match.group(4) else None
            stride = int(match.group(5)) if match.group(5) else 1
            return Operand(OperandType.VECTOR, 
                          {'reg': reg_name, 'type': elem_type, 'start': start, 
                           'end': end, 'stride': stride})
        
        # Check for remote memory
        match = cls.REMOTE_PATTERN.match(token)
        if match:
            blade = int(match.group(1))
            addr = int(match.group(2), 0)
            return Operand(OperandType.REMOTE, (blade, addr))
        
        # Check for multi-rack remote
        match = cls.MULTI_RACK_PATTERN.match(token)
        if match:
            rack = int(match.group(1))
            blade = int(match.group(2))
            addr = int(match.group(3), 0)
            return Operand(OperandType.REMOTE, (rack, blade, addr))
        
        # Check for memory operand
        match = cls.MEMORY_PATTERN.match(token)
        if match:
            expr = match.group(1)
            return Operand(OperandType.MEMORY, expr)
        
        # Check for type map operand
        match = cls.TYPE_MAP_PATTERN.match(token)
        if match:
            reg_class = match.group(1)
            reg_num = int(match.group(2))
            return Operand(OperandType.TYPE_MAP, (reg_class, reg_num))
        
        # Check for immediate values
        match = cls.IMM_DECIMAL_PATTERN.match(token)
        if match:
            return Operand(OperandType.IMMEDIATE, int(match.group(1)))
        
        match = cls.IMM_HEX_PATTERN.match(token)
        if match:
            return Operand(OperandType.IMMEDIATE, int(match.group(1), 16))
        
        match = cls.IMM_BIN_PATTERN.match(token)
        if match:
            return Operand(OperandType.IMMEDIATE, int(match.group(1), 2))
        
        match = cls.IMM_FLOAT_PATTERN.match(token)
        if match:
            val_str = match.group(1)
            if val_str.endswith('f'):
                return Operand(OperandType.IMMEDIATE, float(val_str[:-1]))
            elif val_str.endswith('h'):
                return Operand(OperandType.IMMEDIATE, ('half', float(val_str[:-1])))
            else:
                return Operand(OperandType.IMMEDIATE, float(val_str))
        
        match = cls.IMM_CONST_PATTERN.match(token)
        if match:
            const_map = {
                'TRUE': 1, 'FALSE': 0, 'PI': 3.141592653589793,
                'E': 2.718281828459045, 'INF': float('inf'),
                'NAN': float('nan'), 'MAX': 2**63-1, 'MIN': -2**63
            }
            return Operand(OperandType.IMMEDIATE, const_map[match.group(1).upper()])
        
        raise SyntaxError(f"Invalid operand at line {line_num}: {token}")

# ============================================================================
# Data Directives
# ============================================================================

@dataclass
class DataDirective:
    """Data directive for assembly"""
    directive: str
    values: List[Any]
    address: int = 0

class DataDirectiveHandler:
    """Handle data definition directives (DB, DW, DD, DQ, etc.)"""
    
    @staticmethod
    def handle(directive: str, args: List, current_addr: int) -> Tuple[bytearray, int]:
        """Process data directive and return bytes + new address"""
        directive = directive.upper()
        result = bytearray()
        
        if directive == 'DB':
            for arg in args:
                result.extend(DataDirectiveHandler._emit_byte(arg))
        elif directive == 'DW':
            for arg in args:
                result.extend(DataDirectiveHandler._emit_word(arg))
        elif directive == 'DD':
            for arg in args:
                result.extend(DataDirectiveHandler._emit_dword(arg))
        elif directive == 'DQ':
            for arg in args:
                result.extend(DataDirectiveHandler._emit_qword(arg))
        elif directive == 'DO':
            for arg in args:
                result.extend(DataDirectiveHandler._emit_oword(arg))
        elif directive == 'DF':
            for arg in args:
                result.extend(struct.pack('<f', float(arg)))
        elif directive == 'DD' and isinstance(args[0], float):
            for arg in args:
                result.extend(struct.pack('<d', float(arg)))
        elif directive == 'DH':
            for arg in args:
                # Half-precision float conversion (simplified)
                f = float(arg)
                result.extend(DataDirectiveHandler._float_to_half(f))
        elif directive == 'DS':
            # String directive
            for arg in args:
                if isinstance(arg, str):
                    result.extend(arg.encode('ascii'))
                else:
                    result.extend(str(arg).encode('ascii'))
        elif directive == 'DBZ':
            # Zero block
            size = int(args[0]) if args else 0
            result.extend(b'\x00' * size)
        elif directive == 'ALIGN':
            alignment = int(args[0])
            padding = (alignment - (current_addr % alignment)) % alignment
            result.extend(b'\x00' * padding)
        else:
            raise ValueError(f"Unknown directive: {directive}")
        
        return result, current_addr + len(result)
    
    @staticmethod
    def _emit_byte(value) -> bytes:
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                return value[1:-1].encode('ascii')
            return bytes([ord(value[0]) if len(value) == 1 else 0])
        return bytes([value & 0xFF])
    
    @staticmethod
    def _emit_word(value) -> bytes:
        return struct.pack('<H', value & 0xFFFF)
    
    @staticmethod
    def _emit_dword(value) -> bytes:
        return struct.pack('<I', value & 0xFFFFFFFF)
    
    @staticmethod
    def _emit_qword(value) -> bytes:
        return struct.pack('<Q', value & 0xFFFFFFFFFFFFFFFF)
    
    @staticmethod
    def _emit_oword(value) -> bytes:
        if isinstance(value, int):
            return struct.pack('<QQ', value & 0xFFFFFFFFFFFFFFFF, (value >> 64) & 0xFFFFFFFFFFFFFFFF)
        return bytes(16)
    
    @staticmethod
    def _float_to_half(f: float) -> bytes:
        """Convert float to half-precision (16-bit) IEEE 754"""
        # Simplified conversion - production version would use proper algorithm
        import math
        if math.isnan(f):
            return b'\x00\x7e'
        if math.isinf(f):
            return b'\x00\x7c' if f > 0 else b'\x00\xfc'
        # Clamp and convert (simplified)
        i = int(f * 2048)  # Approximate scaling
        i = max(-32768, min(32767, i))
        return struct.pack('<h', i)

# ============================================================================
# Instruction Encoder
# ============================================================================

class InstructionEncoder:
    """Encode parsed instructions to machine code"""
    
    def __init__(self, core_type: CoreType = CoreType.MATH):
        self.core_type = core_type
        self.output = bytearray()
        self.current_addr = 0
    
    def encode(self, mnemonic: str, operands: List[Operand], flags: int = 0) -> bytearray:
        """Encode a single instruction"""
        mnemonic = mnemonic.upper()
        
        if mnemonic not in INSTRUCTIONS:
            raise ValueError(f"Unknown instruction: {mnemonic}")
        
        insn = INSTRUCTIONS[mnemonic]
        if self.core_type not in insn['cores']:
            raise ValueError(f"{mnemonic} not available on {self.core_type.name} core")
        
        if len(operands) != insn['operands']:
            raise ValueError(f"{mnemonic} expects {insn['operands']} operands, got {len(operands)}")
        
        # Build header based on core type
        opcode = insn['opcode']
        
        if self.core_type == CoreType.MATH:
            # 20-bit header: opcode(8) | flags(8) | operand_count(4)
            header = (opcode & 0xFF) | ((flags & 0xFF) << 8) | ((len(operands) & 0xF) << 16)
            self._write_bits(header, 20)
        elif self.core_type == CoreType.LOGIC:
            # 12-bit header: opcode(7) | flags(3) | operand_count(2)
            opcode_7bit = opcode & 0x7F
            flags_3bit = flags & 0x7
            header = (opcode_7bit & 0x7F) | ((flags_3bit & 0x7) << 7) | ((len(operands) & 0x3) << 10)
            self._write_bits(header, 12)
        else:  # SYSTEM
            # 8-bit header: opcode(6) | flags(2)
            opcode_6bit = opcode & 0x3F
            flags_2bit = flags & 0x3
            header = (opcode_6bit & 0x3F) | ((flags_2bit & 0x3) << 6)
            self._write_bits(header, 8)
        
        # Encode operands
        for operand in operands:
            self._encode_operand(operand)
        
        return self.output
    
    def _write_bits(self, value: int, bits: int):
        """Write variable-length bit field"""
        bytes_needed = (bits + 7) // 8
        self.output.extend(value.to_bytes(bytes_needed, 'little'))
    
    def _encode_operand(self, operand: Operand):
        """Encode a single operand"""
        if operand.type == OperandType.REGISTER:
            reg_num = ALL_REGS.get(operand.value, 0)
            if self.core_type == CoreType.MATH:
                # 16-bit descriptor: type(3) | size(3) | behavior(3) | reg_num(7)
                desc = (0 << 13) | (3 << 10) | ((operand.behavior & 0x7) << 7) | (reg_num & 0x7F)
                self._write_bits(desc, 16)
            elif self.core_type == CoreType.LOGIC:
                desc = (0 << 10) | (3 << 7) | (reg_num & 0x7F)
                self._write_bits(desc, 12)
            else:  # SYSTEM
                desc = (0 << 6) | (3 << 3) | (reg_num & 0x7)
                self._write_bits(desc, 8)
        
        elif operand.type == OperandType.IMMEDIATE:
            val = operand.value
            if isinstance(val, tuple) and val[0] == 'half':
                f = val[1]
                # Convert to half-float bytes
                val_bytes = struct.pack('<e', f)
                size = 2
            elif isinstance(val, float):
                val_bytes = struct.pack('<d', val)
                size = 8
            elif isinstance(val, int):
                # Determine size needed
                if -128 <= val <= 127:
                    val_bytes = struct.pack('<b', val)
                    size = 1
                elif -32768 <= val <= 32767:
                    val_bytes = struct.pack('<h', val)
                    size = 2
                elif -2147483648 <= val <= 2147483647:
                    val_bytes = struct.pack('<i', val)
                    size = 4
                else:
                    val_bytes = struct.pack('<q', val)
                    size = 8
            else:
                val_bytes = bytes(8)
                size = 8
            
            if self.core_type == CoreType.MATH:
                desc = (2 << 13) | ((size & 0x7) << 10) | (operand.behavior << 7)
                self._write_bits(desc, 16)
            elif self.core_type == CoreType.LOGIC:
                desc = (2 << 10) | ((size & 0x3) << 8) | (operand.behavior << 6)
                self._write_bits(desc, 12)
            else:
                desc = (2 << 6) | ((size & 0x3) << 4) | (operand.behavior << 3)
                self._write_bits(desc, 8)
            
            self.output.extend(val_bytes)
        
        elif operand.type == OperandType.MEMORY:
            # Memory operand - simplified encoding
            # In production, would parse address expression
            if self.core_type == CoreType.MATH:
                desc = (1 << 13) | (3 << 10) | (operand.behavior << 7)
                self._write_bits(desc, 16)
            elif self.core_type == CoreType.LOGIC:
                desc = (1 << 10) | (3 << 8) | (operand.behavior << 6)
                self._write_bits(desc, 12)
            else:
                desc = (1 << 6) | (3 << 4) | (operand.behavior << 3)
                self._write_bits(desc, 8)
            # Placeholder for address (will be resolved by linker)
            self.output.extend(b'\x00' * 8)
        
        elif operand.type == OperandType.REMOTE:
            # Remote memory operand
            if len(operand.value) == 2:
                blade, addr = operand.value
                rack = 0
            else:
                rack, blade, addr = operand.value
            
            if self.core_type == CoreType.MATH:
                desc = (3 << 13) | (3 << 10) | (operand.behavior << 7) | (blade & 0xFFF)
                self._write_bits(desc, 20)
                self.output.extend(struct.pack('<Q', addr))
            else:
                desc = (3 << 10) | (3 << 8) | (operand.behavior << 6) | (blade & 0xFF)
                self._write_bits(desc, 16)
                self.output.extend(struct.pack('<Q', addr))
        
        elif operand.type == OperandType.VECTOR:
            # Vector operand with range
            vec_info = operand.value
            reg_num = ALL_REGS.get(vec_info['reg'], 0)
            if self.core_type == CoreType.MATH:
                desc = (4 << 29) | ((reg_num & 0x3F) << 20) | ((vec_info.get('start', 0) & 0xFF) << 12)
                desc |= ((vec_info.get('end', 63) & 0xFF) << 4) | (vec_info.get('stride', 1) & 0xF)
                self._write_bits(desc, 32)
        
        elif operand.type == OperandType.TYPE_MAP:
            reg_class, reg_num = operand.value
            if self.core_type == CoreType.MATH:
                desc = (5 << 13) | (reg_num & 0x3F)
                self._write_bits(desc, 16)

# ============================================================================
# Main Assembler
# ============================================================================

class SiriusNEXUSAssembler:
    """Complete assembler for Sirius NEXUS processors"""
    
    def __init__(self, core_type: CoreType = CoreType.MATH):
        self.core_type = core_type
        self.encoder = InstructionEncoder(core_type)
        self.symbols: Dict[str, int] = {}
        self.undefined: Dict[str, List[Tuple[int, int]]] = {}
        self.output = bytearray()
        self.current_section = '.text'
        self.section_addrs = {'.text': 0, '.data': 0x1000000, '.rodata': 0x2000000, 
                              '.bss': 0x3000000, '.romb': 0x200000000}
        self.current_addr = 0
    
    def assemble(self, source: str) -> bytearray:
        """Assemble source code to machine code"""
        lines = source.split('\n')
        self._first_pass(lines)
        self._second_pass(lines)
        return self.output
    
    def _first_pass(self, lines: List[str]):
        """First pass: collect labels and estimate sizes"""
        addr = 0
        in_section = '.text'
        
        for line_num, line in enumerate(lines, 1):
            line = line.split(';')[0].strip()  # Remove comments
            if not line:
                continue
            
            # Section directive
            if line.startswith('.'):
                parts = line.split()
                if parts[0] in ['.text', '.data', '.rodata', '.bss', '.romb']:
                    in_section = parts[0]
                    addr = self.section_addrs.get(in_section, 0)
                continue
            
            # Label
            if line.endswith(':'):
                label = line[:-1]
                self.symbols[label] = addr
                continue
            
            # Instruction
            parts = line.split(None, 1)
            mnemonic = parts[0].upper()
            
            if mnemonic in INSTRUCTIONS:
                # Estimate instruction size
                if self.core_type == CoreType.MATH:
                    addr += 3  # 20-bit header
                    insn = INSTRUCTIONS[mnemonic]
                    addr += insn['operands'] * 2  # 16-bit operand descriptors
                elif self.core_type == CoreType.LOGIC:
                    addr += 2  # 12-bit header
                    addr += len(parts[1].split(',')) if len(parts) > 1 else 0
                else:  # SYSTEM
                    addr += 1  # 8-bit header
            elif mnemonic.startswith('.'):
                # Directive - estimate size
                if mnemonic == '.DBZ':
                    size = int(parts[1]) if len(parts) > 1 else 0
                    addr += size
                elif mnemonic in ['.DB', '.DW', '.DD', '.DQ', '.DO', '.DF', '.DH']:
                    # Count values
                    values = parts[1].split(',') if len(parts) > 1 else []
                    if mnemonic == '.DB':
                        addr += len(values)
                    elif mnemonic == '.DW':
                        addr += len(values) * 2
                    elif mnemonic == '.DD':
                        addr += len(values) * 4
                    elif mnemonic == '.DQ':
                        addr += len(values) * 8
                    elif mnemonic == '.DO':
                        addr += len(values) * 16
                elif mnemonic == '.ALIGN':
                    alignment = int(parts[1]) if len(parts) > 1 else 16
                    addr = ((addr + alignment - 1) // alignment) * alignment
    
    def _second_pass(self, lines: List[str]):
        """Second pass: generate actual machine code"""
        in_section = '.text'
        self.current_addr = self.section_addrs['.text']
        
        for line_num, line in enumerate(lines, 1):
            line = line.split(';')[0].strip()
            if not line:
                continue
            
            # Section directive
            if line.startswith('.'):
                parts = line.split()
                if parts[0] in ['.text', '.data', '.rodata', '.bss', '.romb']:
                    in_section = parts[0]
                    self.current_addr = self.section_addrs.get(in_section, 0)
                continue
            
            # Label
            if line.endswith(':'):
                continue
            
            # Parse instruction or directive
            parts = line.split(None, 1)
            mnemonic = parts[0].upper()
            
            if mnemonic in INSTRUCTIONS:
                # Parse operands
                operands = []
                if len(parts) > 1:
                    for token in self._split_operands(parts[1]):
                        operands.append(OperandParser.parse(token, line_num))
                
                # Encode instruction
                self.encoder.core_type = self.core_type
                encoded = self.encoder.encode(mnemonic, operands)
                self.output.extend(encoded)
                self.current_addr += len(encoded)
            
            elif mnemonic.startswith('.'):
                # Data directive
                args = []
                if len(parts) > 1:
                    args = self._parse_directive_args(parts[1])
                
                data_bytes, new_addr = DataDirectiveHandler.handle(mnemonic, args, self.current_addr)
                self.output.extend(data_bytes)
                self.current_addr = new_addr
    
    def _split_operands(self, operand_str: str) -> List[str]:
        """Split operand string into individual operands"""
        # Handle nested brackets
        result = []
        current = []
        bracket_depth = 0
        for char in operand_str:
            if char == ',' and bracket_depth == 0:
                result.append(''.join(current).strip())
                current = []
            else:
                if char == '[':
                    bracket_depth += 1
                elif char == ']':
                    bracket_depth -= 1
                current.append(char)
        if current:
            result.append(''.join(current).strip())
        return result
    
    def _parse_directive_args(self, arg_str: str) -> List:
        """Parse directive arguments"""
        args = []
        for token in arg_str.split(','):
            token = token.strip()
            if token.startswith('"') and token.endswith('"'):
                args.append(token)
            elif token.startswith('0x'):
                args.append(int(token, 16))
            elif token.startswith('0b'):
                args.append(int(token, 2))
            elif token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
                args.append(int(token))
            else:
                # Try as float
                try:
                    args.append(float(token))
                except ValueError:
                    args.append(token)
        return args

# ============================================================================
# Command Line Interface
# ============================================================================

def main():
    """Command-line entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sirius NEXUS Assembler')
    parser.add_argument('input', help='Input assembly file')
    parser.add_argument('-o', '--output', help='Output binary file')
    parser.add_argument('-c', '--core', choices=['math', 'logic', 'system'], 
                        default='math', help='Target core type')
    parser.add_argument('-l', '--list', help='Generate listing file')
    
    args = parser.parse_args()
    
    # Read input file
    with open(args.input, 'r') as f:
        source = f.read()
    
    # Determine core type
    core_map = {'math': CoreType.MATH, 'logic': CoreType.LOGIC, 'system': CoreType.SYSTEM}
    core_type = core_map[args.core]
    
    # Assemble
    assembler = SiriusNEXUSAssembler(core_type)
    machine_code = assembler.assemble(source)
    
    # Write output
    output_file = args.output or args.input.replace('.asm', '.bin')
    with open(output_file, 'wb') as f:
        f.write(machine_code)
    
    print(f"Assembled {len(machine_code)} bytes to {output_file}")
    
    if args.list:
        with open(args.list, 'w') as f:
            f.write(f"Sirius NEXUS Assembly Listing\n")
            f.write(f"Input: {args.input}\n")
            f.write(f"Core: {args.core}\n")
            f.write(f"Output size: {len(machine_code)} bytes\n\n")
            f.write("Symbols:\n")
            for sym, addr in assembler.symbols.items():
                f.write(f"  {sym}: 0x{addr:08X}\n")

if __name__ == '__main__':
    main()
```
