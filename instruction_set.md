# Sirius NEXUS AI Processor Gen5

## Volume 1: Complete Instruction Set Reference

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

This concludes Volume 1 of the Sirius NEXUS AI Processor Gen5 documentation. The complete instruction set comprises 132 instructions across 20 functional categories, with full encoding specifications for Math, Logic, and System cores. Each instruction is documented with assembly syntax, operand types, numerical formats, and multiple usage examples.
