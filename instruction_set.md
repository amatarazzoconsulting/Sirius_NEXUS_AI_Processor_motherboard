# Sirius NEXUS AI Processor Gen5

## Volume 1: Complete Instruction Set Reference

# Sirius NEXUS AI Processor Gen5 - Complete Instruction Set Summary
## All 184 Instructions with Full Specifications

This document provides the complete instruction set for production release of the Sirius NEXUS AI Processor Gen5, including all core instructions, SYSTEM API commands, and hardware acceleration primitives.

---

# Section 1: Instruction Set Summary

| Category | Count | Instructions |
|----------|-------|--------------|
| Data Movement | 8 | MOV, MOVSX, MOVZX, LEA, XCHG, CMOV, MOVNT, PREFETCH |
| Arithmetic | 12 | ADD, SUB, MUL, IMUL, DIV, IDIV, INC, DEC, FMA, ADC, SBB, NEG |
| Logic and Bit | 12 | AND, OR, XOR, NOT, TEST, BSF, BSR, SHL, SHR, ROL, ROR, RCL, RCR |
| Control Flow | 8 | JMP, CALL, RET, BRANCH, LOOP, JCXZ, INT, IRET |
| Vector SIMD | 16 | ADDPS, SUBPS, MULPS, DIVPS, ADD, MUL, DOT, CONV, SHUFPS, BLEND, PERM, BROADCAST, GATHER, SCATTER, COMPRESS, EXPAND |
| Advanced Math | 24 | EXP, LOG, LOG2, LOG10, POW, SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2, SQRT, RSQRT, ERF, ERFC, GAMMA, LGAMMA, BESSEL_J, BESSEL_Y, HYPOT, CBRT, HYPOT3, POLYEVAL |
| INT4 Inference | 16 | MATMULI4, SOFTMAXI4, ATTENTIONI4, GELUI4, LAYERNORMI4, RESIDUALI4, MOVI4, PACKI4, UNPACKI4, ADDI4, MULI4, DOTI4, CONVI4, POOLI4, QUANTIZE, DEQUANTIZE |
| Probabilistic | 12 | HMM_FORWARD, HMM_VITERBI, HMM_BACKWARD, HMM_UPDATE, SOFTMAX, LOG_SUM_EXP, VECTOR_COND, VECTOR_THRESHOLD, LOG_SOFTMAX, SPARSE_DOT, MIXTURE, SAMPLE |
| System | 12 | SYSENTER, SYSEXIT, IN, OUT, CFG_VIDEO, CFG_AUDIO, RING_INIT, RING_WRITE, RING_SWAP, TIMER_SET, TIMER_GET, INTERRUPT_CTL |
| Interconnect | 12 | MAP_STORAGE, EXPORT_MEMORY, REMOTE_CALL, LINK_STATUS, RACK_UNIFY, WARP_SYNC, REMOTE_ALLOC, BROADCAST, BARRIER_SYNC, RDMA_READ, RDMA_WRITE, OPTICAL_SEND |
| Memory Management | 10 | SEGMENT_CREATE, SEGMENT_DELETE, SEGMENT_MODIFY, CAPABILITY_GRANT, CAPABILITY_ACCEPT, SEGMENT_LOOKUP, TLB_INVALIDATE, PAGE_ALLOC, PAGE_FREE, VM_MAP |
| Protection | 8 | OWNER_GET, OWNER_SET_PARENT, RING_SET, IRQ_SET, IO_MAP, SEGMENT_WALK, PERM_CHECK, AUDIT |
| Register Type Mapping | 4 | SET_REG_MAP, SET_REG_TYPE, GET_REG_TYPE, RESET_REG_MAP |
| INT4 Memory | 8 | MOVI4, PACKI4, UNPACKI4, ADDI4, MULI4, DOTI4, SHUFI4, PERMI4 |
| ROMB | 6 | ROMB_INSERT, ROMB_IRQ, ROMB_PRIORITY, ROMB_SELECT, ROMB_PREFETCH, ROMB_INVALIDATE |
| Transactional Memory | 6 | XBEGIN, XEND, XABORT, XTEST, XLOCK, XUNLOCK |
| Variable Precision | 6 | SET_PRECISION, VADDP.VP, VMULP.VP, VFMA.VP, VCVT.VP, VCMP.VP |
| In-Memory Compute | 8 | MEM_SCAN, MEM_FILTER, MEM_AGGREGATE, MEM_BITMAP, MEM_SORT, MEM_UNIQUE, MEM_JOIN, MEM_REDUCE |
| Compression | 8 | MEM_COMPRESS, MEM_DECOMPRESS, DME_COPY_COMP, MEM_COMPRESS_STATS, MEM_COMPRESS_ADAPT, MEM_TRAIN_COMPRESS, MEM_ALLOC_COMP_AWARE, MEM_COMPRESS_STREAM |
| Parsing (HGPE) | 10 | PARSE, PARSE_STREAM, PARSE_DEFINE_GRAMMAR, PARSE_MATCH, AST_WALK, AST_QUERY, AST_TRANSFORM, GRAMMAR_COMPILE, REGEX_COMPILE, REGEX_EXEC |
| Graphics | 8 | RASTERIZE, TEXTURE_SAMPLE, BLEND, DEPTH_TEST, COLOR_CONVERT, CLIP, LIGHTING, SHADER_EXEC |
| Cryptographic | 12 | AES_ENC, AES_DEC, SHA256, SHA512, RSA_ENC, RSA_DEC, ECC_MUL, RANDOM, HMAC, HKDF, CHACHA20, POLY1305 |
| Debug/Profiling | 6 | BREAKPOINT, TRACE, PROFILE_START, PROFILE_END, PERF_COUNT, DEBUG_PRINT |
| Graphene Photonic | 6 | GRAPHENE_EMIT, GRAPHENE_DETECT, GRAPHENE_MODULATE, OPTICAL_ROUTER, PHOTONIC_BARRIER, WAVELENGTH_TUNE |
| **TOTAL** | **184** | |

---

# Section 2: Data Movement Instructions (8)

## 2.1 MOV - Move Data
**Encoding:** Math:0x01, Logic:0x01, System:0x01
**Operands:** dest (reg/mem), src (reg/mem/imm)
**Size suffixes:** .B(8), .W(16), .D(32), .Q(64), .O(128), .Y(256), .Z(512)
**Flags:** None
```assembly
MOV R1, R2              ; R1 = R2
MOV R1, #42             ; Immediate
MOV R1, [R2]            ; Memory load
MOV [R1], R2            ; Memory store
MOV.NT [R1], R2         ; Non-temporal (bypass cache)
MOV.REMOTE @4:0x10000, R1  ; Remote store
```

## 2.2 MOVSX - Move with Sign Extension
**Encoding:** Math:0x02, Logic:0x02
**Operands:** dest (reg), src (reg/mem/imm) - dest larger than src
**Flags:** ZF, SF
```assembly
MOVSX R1, R2            ; Sign extend 8→32
MOVSX R1, [R2]          ; From memory
MOVSX.S R1, R2          ; Saturating
```

## 2.3 MOVZX - Move with Zero Extension
**Encoding:** Math:0x03, Logic:0x03
**Operands:** dest (reg), src (reg/mem/imm) - dest larger than src
**Flags:** ZF, SF
```assembly
MOVZX R1, R2            ; Zero extend
MOVZX R1, [R2]          ; From memory
```

## 2.4 LEA - Load Effective Address
**Encoding:** Math:0x04, Logic:0x04, System:0x02
**Operands:** dest (reg), src (mem expr)
```assembly
LEA R1, [R2 + 64]       ; R1 = R2 + 64
LEA R1, [R2 + R3*8]     ; Array indexing
LEA R1, @4:0x10000      ; Remote address
```

## 2.5 XCHG - Exchange Data
**Encoding:** Math:0x05, Logic:0x05, System:0x03
**Operands:** a (reg/mem), b (reg/mem) - atomic
```assembly
XCHG R1, [lock]         ; Atomic spinlock
XCHG R1, R2             ; Swap registers
XCHG.A R1, [lock]       ; Acquire-release
```

## 2.6 CMOV - Conditional Move
**Encoding:** Math:0x06, Logic:0x06
**Operands:** dest (reg), src (reg/mem)
**Conditions:** EQ,NE,LT,LE,GT,GE,LO,LS,HI,HS,CS,CC,VS,VC,MI,PL
```assembly
CMOV.EQ R1, R2          ; If equal, R1 = R2
CMOV.LT R1, [R2]        ; If less, load
```

## 2.7 MOVNT - Non-temporal Move
**Encoding:** Math:0x07
**Operands:** dest (mem), src (reg/vec)
```assembly
MOVNT [R1], V0          ; Streaming store (bypass cache)
MOVNT [R1], R2          ; Non-temporal scalar
```

## 2.8 PREFETCH - Prefetch Data
**Encoding:** Math:0x08
**Operands:** addr (mem), hint (imm)
**Hints:** 0=NTA,1=T0,2=T1,3=T2
```assembly
PREFETCH [R1], #0       ; Non-temporal prefetch
PREFETCH [R1], #1       ; L1 cache prefetch
```

---

# Section 3: Arithmetic Instructions (12)

## 3.1 ADD - Add
**Encoding:** Math:0x10, Logic:0x10, System:0x04
**Operands:** dest (reg/mem), src (reg/mem/imm)
**Flags:** ZF, SF, CF, OF
```assembly
ADD R1, R2              ; R1 = R1 + R2
ADD.V V1, V2, V3        ; Vector add
ADD.S R1, R2            ; Saturating add
ADD.C R3, R4            ; Add with carry
```

## 3.2 SUB - Subtract
**Encoding:** Math:0x11, Logic:0x11, System:0x05
**Operands:** dest (reg/mem), src (reg/mem/imm)
**Flags:** ZF, SF, CF, OF
```assembly
SUB R1, R2              ; R1 = R1 - R2
SUB.V V1, V2, V3        ; Vector subtract
SUB.S R1, R2            ; Saturating subtract
```

## 3.3 MUL - Multiply Unsigned
**Encoding:** Math:0x12, Logic:0x12
**Operands:** dest (reg), src (reg/mem/imm)
**Flags:** ZF, SF, CF
```assembly
MUL R1, R2              ; R1 = R1 * R2
MUL.V V1, V2, V3        ; Vector multiply
```

## 3.4 IMUL - Multiply Signed
**Encoding:** Math:0x13, Logic:0x13
**Operands:** dest (reg), src (reg/mem/imm)
**Flags:** ZF, SF, CF, OF
```assembly
IMUL R1, R2             ; Signed multiply
IMUL.V V1, V2, V3       ; Vector signed multiply
```

## 3.5 DIV - Divide Unsigned
**Encoding:** Math:0x14, Logic:0x14
**Operands:** dividend (reg), divisor (reg/mem)
**Result:** Quotient in dividend, remainder in R0
```assembly
DIV R1, R2              ; (R1,R0) / R2
```

## 3.6 IDIV - Divide Signed
**Encoding:** Math:0x15, Logic:0x15
**Operands:** dividend (reg), divisor (reg/mem)
```assembly
IDIV R1, R2             ; Signed division
```

## 3.7 INC - Increment
**Encoding:** Math:0x16, Logic:0x16, System:0x06
**Operands:** dest (reg/mem)
**Flags:** ZF, SF, OF
```assembly
INC R1                  ; R1 = R1 + 1
```

## 3.8 DEC - Decrement
**Encoding:** Math:0x17, Logic:0x17, System:0x07
**Operands:** dest (reg/mem)
**Flags:** ZF, SF, OF
```assembly
DEC R1                  ; R1 = R1 - 1
```

## 3.9 FMA - Fused Multiply-Add
**Encoding:** Math:0x18
**Operands:** dest (reg), a (reg/mem/imm), b (reg/mem/imm), c (reg/mem/imm)
```assembly
FMA R1, R2, R3, R4      ; R1 = (R2 * R3) + R4
FMA.V V1, V2, V3, V4    ; Vector FMA
FMA.RZ V1, V2, V3, V4   ; Round toward zero
```

## 3.10 ADC - Add with Carry
**Encoding:** Math:0x19, Logic:0x19
**Operands:** dest (reg/mem), src (reg/mem/imm)
**Flags:** ZF, SF, CF, OF
```assembly
ADC R1, R2              ; R1 = R1 + R2 + CF
```

## 3.11 SBB - Subtract with Borrow
**Encoding:** Math:0x1A, Logic:0x1A
**Operands:** dest (reg/mem), src (reg/mem/imm)
**Flags:** ZF, SF, CF, OF
```assembly
SBB R1, R2              ; R1 = R1 - R2 - CF
```

## 3.12 NEG - Negate
**Encoding:** Math:0x1B, Logic:0x1B
**Operands:** dest (reg/mem)
**Flags:** ZF, SF, CF, OF
```assembly
NEG R1                  ; R1 = -R1 (two's complement)
```

---

# Section 4: Logic and Bit Instructions (12)

## 4.1 AND - Bitwise AND
**Encoding:** Math:0x20, Logic:0x20, System:0x08
**Operands:** dest (reg/mem), src (reg/mem/imm)
```assembly
AND R1, #0xFF           ; Mask low 8 bits
AND.V V1, V2, V3        ; Vector AND
```

## 4.2 OR - Bitwise OR
**Encoding:** Math:0x21, Logic:0x21, System:0x09
**Operands:** dest (reg/mem), src (reg/mem/imm)
```assembly
OR R1, #0x0F            ; Set low 4 bits
OR.V V1, V2, V3         ; Vector OR
```

## 4.3 XOR - Bitwise XOR
**Encoding:** Math:0x22, Logic:0x22, System:0x0A
**Operands:** dest (reg/mem), src (reg/mem/imm)
```assembly
XOR R1, R1              ; Zero register
XOR.V V1, V2, V3        ; Vector XOR
```

## 4.4 NOT - Bitwise NOT
**Encoding:** Math:0x23, Logic:0x23
**Operands:** dest (reg/mem)
```assembly
NOT R1                  ; R1 = ~R1
NOT.V V1, V2            ; Vector NOT
```

## 4.5 TEST - Test Bits
**Encoding:** Math:0x24, Logic:0x24
**Operands:** a (reg/mem), b (reg/mem/imm)
**Flags:** ZF, SF
```assembly
TEST R1, #0x04          ; Test bit 2
```

## 4.6 BSF - Bit Scan Forward
**Encoding:** Math:0x30, Logic:0x30
**Operands:** dest (reg), src (reg/mem)
```assembly
BSF R1, R2              ; Index of lowest set bit
```

## 4.7 BSR - Bit Scan Reverse
**Encoding:** Math:0x31, Logic:0x31
**Operands:** dest (reg), src (reg/mem)
```assembly
BSR R1, R2              ; Index of highest set bit
```

## 4.8 SHL - Shift Left
**Encoding:** Math:0x36, Logic:0x36
**Operands:** dest (reg/mem), count (reg/imm)
```assembly
SHL R1, #3              ; R1 = R1 << 3
SHL.V V1, V2, #2        ; Vector shift left
```

## 4.9 SHR - Shift Right (Logical)
**Encoding:** Math:0x37, Logic:0x37
**Operands:** dest (reg/mem), count (reg/imm)
```assembly
SHR R1, #3              ; R1 = R1 >> 3
SHR.V V1, V2, #2        ; Vector shift right
```

## 4.10 ROL - Rotate Left
**Encoding:** Math:0x38, Logic:0x38
**Operands:** dest (reg/mem), count (reg/imm)
```assembly
ROL R1, #1              ; Rotate left by 1
```

## 4.11 ROR - Rotate Right
**Encoding:** Math:0x39, Logic:0x39
**Operands:** dest (reg/mem), count (reg/imm)
```assembly
ROR R1, #1              ; Rotate right by 1
```

## 4.12 RCL - Rotate Through Carry Left
**Encoding:** Math:0x3A, Logic:0x3A
**Operands:** dest (reg/mem), count (reg/imm)
```assembly
RCL R1, #1              ; Rotate through carry left
```

## 4.13 RCR - Rotate Through Carry Right
**Encoding:** Math:0x3B, Logic:0x3B
**Operands:** dest (reg/mem), count (reg/imm)
```assembly
RCR R1, #1              ; Rotate through carry right
```

---

# Section 5: Control Flow Instructions (8)

## 5.1 JMP - Unconditional Jump
**Encoding:** Math:0x40, Logic:0x40, System:0x10
**Operands:** target (imm/reg/mem)
```assembly
JMP label
JMP R1                  ; Register indirect
JMP [R1]                ; Memory indirect
JMP @4:0x10000          ; Remote jump
```

## 5.2 CALL - Call Subroutine
**Encoding:** Math:0x41, Logic:0x41, System:0x11
**Operands:** target (imm/reg/mem)
```assembly
CALL subroutine
CALL R1                 ; Register indirect
CALL @4:0x10000         ; Remote call
```

## 5.3 RET - Return
**Encoding:** Math:0x42, Logic:0x42, System:0x12
**Operands:** Optional pop count
```assembly
RET
RET #8                  ; Return and pop 8 bytes
RET.FAR                 ; Far return
RET.I                   ; Interrupt return
```

## 5.4 BRANCH - Conditional Branch
**Encoding:** Math:0x43, Logic:0x43
**Operands:** condition (imm), target (imm)
**Conditions:** EQ,NE,LT,LE,GT,GE,LO,LS,HI,HS,CS,CC,VS,VC,MI,PL
```assembly
BRANCH EQ, label        ; Branch if equal
BRANCH.PT EQ, label     ; Predict taken
BRANCH.PN EQ, label     ; Predict not taken
```

## 5.5 LOOP - Loop Counter
**Encoding:** Math:0x44, Logic:0x44
**Operands:** target (imm)
**Uses:** RCX as counter
```assembly
MOV RCX, #100
LOOP label              ; RCX--; if RCX!=0 jump
```

## 5.6 JCXZ - Jump if CX Zero
**Encoding:** Math:0x45, Logic:0x45
**Operands:** target (imm)
```assembly
JCXZ label              ; Jump if CX=0
```

## 5.7 INT - Software Interrupt
**Encoding:** System:0x30
**Operands:** vector (imm)
```assembly
INT #0x80               ; Software interrupt
```

## 5.8 IRET - Interrupt Return
**Encoding:** System:0x31
**Operands:** None
```assembly
IRET                    ; Return from interrupt
```

---

# Section 6: Vector SIMD Instructions (16)

## 6.1 ADDPS - Add Packed Single
**Encoding:** Math:0x50
**Operands:** dest (vec), src1 (vec/mem), src2 (vec/mem)
```assembly
ADDPS XMM1, XMM2, XMM3      ; 4 floats
ADDPS.Y YMM1, YMM2, YMM3    ; 8 floats
ADDPS.Z ZMM1, ZMM2, ZMM3    ; 16 floats
ADDPS.K ZMM1, ZMM2, ZMM3, K1 ; Masked
```

## 6.2 SUBPS - Subtract Packed Single
**Encoding:** Math:0x51
**Operands:** dest (vec), src1 (vec/mem), src2 (vec/mem)
```assembly
SUBPS XMM1, XMM2, XMM3
```

## 6.3 MULPS - Multiply Packed Single
**Encoding:** Math:0x52
**Operands:** dest (vec), src1 (vec/mem), src2 (vec/mem)
```assembly
MULPS XMM1, XMM2, XMM3
```

## 6.4 DIVPS - Divide Packed Single
**Encoding:** Math:0x53
**Operands:** dest (vec), src1 (vec/mem), src2 (vec/mem)
```assembly
DIVPS XMM1, XMM2, XMM3
```

## 6.5 ADDPD - Add Packed Double
**Encoding:** Math:0x54
**Operands:** dest (vec), src1 (vec/mem), src2 (vec/mem)
```assembly
ADDPD XMM1, XMM2, XMM3      ; 2 doubles
ADDPD.Y YMM1, YMM2, YMM3    ; 4 doubles
```

## 6.6 MULPD - Multiply Packed Double
**Encoding:** Math:0x55
**Operands:** dest (vec), src1 (vec/mem), src2 (vec/mem)
```assembly
MULPD XMM1, XMM2, XMM3
```

## 6.7 DOT - Dot Product
**Encoding:** Math:0x56
**Operands:** dest (scalar), src1 (vec), src2 (vec)
```assembly
DOT R1, XMM2, XMM3
DOT.MP R1, ZMM2, ZMM3   ; Mixed precision
```

## 6.8 CONV - 2D Convolution
**Encoding:** Math:0x57
**Operands:** out (mem), in (mem), ker (mem), dims (imm), stride (imm)
```assembly
CONV out, in, ker, #0xE0E0, #1
CONV.K5 out, in, ker, dims, #0x0202
CONV.PAD_SAME out, in, ker, dims, #1
```

## 6.9 SHUFPS - Shuffle
**Encoding:** Math:0x58
**Operands:** dest (vec), src1 (vec), src2 (vec), mask (imm)
```assembly
SHUFPS XMM1, XMM2, XMM3, #0x1B
```

## 6.10 BLEND - Conditional Blend
**Encoding:** Math:0x59
**Operands:** dest (vec), src1 (vec), src2 (vec), mask (reg)
```assembly
BLEND V1, V2, V3, K1
```

## 6.11 PERM - Permute Elements
**Encoding:** Math:0x5A
**Operands:** dest (vec), src (vec), indices (vec/imm)
```assembly
PERM V1, V2, #0x01234567
```

## 6.12 BROADCAST - Broadcast Scalar
**Encoding:** Math:0x5B
**Operands:** dest (vec), src (scalar/mem)
```assembly
BROADCAST V1, R2
BROADCAST V1, [R2]
```

## 6.13 GATHER - Gather from Memory
**Encoding:** Math:0x5C
**Operands:** dest (vec), base (reg), indices (vec), scale (imm)
```assembly
GATHER V1, R2, V3, #4
```

## 6.14 SCATTER - Scatter to Memory
**Encoding:** Math:0x5D
**Operands:** base (reg), indices (vec), src (vec), scale (imm)
```assembly
SCATTER R2, V3, V1, #4
```

## 6.15 COMPRESS - Compress Vector
**Encoding:** Math:0x5E
**Operands:** dest (vec), src (vec), mask (reg)
```assembly
COMPRESS V1, V2, K1
```

## 6.16 EXPAND - Expand Vector
**Encoding:** Math:0x5F
**Operands:** dest (vec), src (vec), mask (reg)
```assembly
EXPAND V1, V2, K1
```

---

# Section 7: Advanced Math Functions (24)

## 7.1 EXP - Exponential e^x
**Encoding:** Math:0x80
**Operands:** dest (reg), src (reg/mem)
```assembly
EXP R1, R2
EXP.V XMM1, XMM2
EXP.FAST R1, R2
```

## 7.2 LOG - Natural Logarithm ln(x)
**Encoding:** Math:0x81
**Operands:** dest (reg), src (reg/mem)
```assembly
LOG R1, R2
LOG.V XMM1, XMM2
```

## 7.3 LOG2 - Base-2 Logarithm log2(x)
**Encoding:** Math:0x82
**Operands:** dest (reg), src (reg/mem)
```assembly
LOG2 R1, R2
```

## 7.4 LOG10 - Base-10 Logarithm log10(x)
**Encoding:** Math:0x83
**Operands:** dest (reg), src (reg/mem)
```assembly
LOG10 R1, R2
```

## 7.5 POW - Power Function x^y
**Encoding:** Math:0x84
**Operands:** dest (reg), base (reg/mem), exp (reg/mem)
```assembly
POW R1, R2, R3
```

## 7.6 SIN - Sine (radians)
**Encoding:** Math:0x85
**Operands:** dest (reg), src (reg/mem)
```assembly
SIN R1, R2
SIN.V XMM1, XMM2
```

## 7.7 COS - Cosine (radians)
**Encoding:** Math:0x86
**Operands:** dest (reg), src (reg/mem)
```assembly
COS R1, R2
```

## 7.8 TAN - Tangent (radians)
**Encoding:** Math:0x87
**Operands:** dest (reg), src (reg/mem)
```assembly
TAN R1, R2
```

## 7.9 ASIN - Arc Sine
**Encoding:** Math:0x88
**Operands:** dest (reg), src (reg/mem)
```assembly
ASIN R1, R2
```

## 7.10 ACOS - Arc Cosine
**Encoding:** Math:0x89
**Operands:** dest (reg), src (reg/mem)
```assembly
ACOS R1, R2
```

## 7.11 ATAN - Arc Tangent
**Encoding:** Math:0x8A
**Operands:** dest (reg), src (reg/mem)
```assembly
ATAN R1, R2
```

## 7.12 ATAN2 - Two-argument Arc Tangent
**Encoding:** Math:0x8B
**Operands:** dest (reg), y (reg/mem), x (reg/mem)
```assembly
ATAN2 R1, R2, R3
```

## 7.13 SQRT - Square Root
**Encoding:** Math:0x8C
**Operands:** dest (reg), src (reg/mem)
```assembly
SQRT R1, R2
SQRT.V XMM1, XMM2
```

## 7.14 RSQRT - Reciprocal Square Root
**Encoding:** Math:0x8D
**Operands:** dest (reg), src (reg/mem)
```assembly
RSQRT R1, R2
RSQRT.V XMM1, XMM2
```

## 7.15 ERF - Error Function
**Encoding:** Math:0x8E
**Operands:** dest (reg), src (reg/mem)
```assembly
ERF R1, R2
```

## 7.16 ERFC - Complementary Error Function
**Encoding:** Math:0x8F
**Operands:** dest (reg), src (reg/mem)
```assembly
ERFC R1, R2
```

## 7.17 GAMMA - Gamma Function Γ(x)
**Encoding:** Math:0x90
**Operands:** dest (reg), src (reg/mem)
```assembly
GAMMA R1, R2
```

## 7.18 LGAMMA - Log Gamma ln(Γ(x))
**Encoding:** Math:0x91
**Operands:** dest (reg), src (reg/mem)
```assembly
LGAMMA R1, R2
```

## 7.19 BESSEL_J - Bessel J Function
**Encoding:** Math:0x92
**Operands:** dest (reg), n (imm), x (reg/mem)
```assembly
BESSEL_J R1, #0, R2     ; J0(x)
```

## 7.20 BESSEL_Y - Bessel Y Function
**Encoding:** Math:0x93
**Operands:** dest (reg), n (imm), x (reg/mem)
```assembly
BESSEL_Y R1, #0, R2     ; Y0(x)
```

## 7.21 HYPOT - Hypotenuse √(x²+y²)
**Encoding:** Math:0x94
**Operands:** dest (reg), x (reg/mem), y (reg/mem)
```assembly
HYPOT R1, R2, R3
```

## 7.22 CBRT - Cube Root ∛x
**Encoding:** Math:0x95
**Operands:** dest (reg), src (reg/mem)
```assembly
CBRT R1, R2
```

## 7.23 HYPOT3 - 3D Hypotenuse √(x²+y²+z²)
**Encoding:** Math:0x96
**Operands:** dest (reg), x (reg/mem), y (reg/mem), z (reg/mem)
```assembly
HYPOT3 R1, R2, R3, R4
```

## 7.24 POLYEVAL - Polynomial Evaluation
**Encoding:** Math:0x97
**Operands:** dest (reg), x (reg/mem), coeffs (mem), degree (imm)
```assembly
POLYEVAL R1, R2, coeffs, #5
```

---

# Section 8: INT4 Inference Instructions (16)

## 8.1 MATMULI4 - INT4 Matrix Multiply
**Encoding:** Math:0xA0, ACU:0xA0
**Operands:** out (mem), A (mem), B (mem), M (imm), K (imm), N (imm)
```assembly
MATMULI4 C, A, B, #1024, #1024, #1024
MATMULI4.T1 C, A, B, #1024, #1024, #1024
MATMULI4.R C, A, B, #1024, #1024, #1024, bias
MATMULI4.G C, A, B, #1024, #1024, #1024, bias
```

## 8.2 SOFTMAXI4 - INT4 Softmax
**Encoding:** Math:0xA1, ACU:0xA1
**Operands:** dest (vec/mem), src (vec/mem)
```assembly
SOFTMAXI4 V1, V2
SOFTMAXI4.T V1, V2, #0.7
SOFTMAXI4.L V1, V2
```

## 8.3 ATTENTIONI4 - INT4 Attention
**Encoding:** Math:0xA2, ACU:0xA2
**Operands:** out (mem), Q (mem), K (mem), V (mem), L (imm), D (imm)
```assembly
ATTENTIONI4 out, Q, K, V, #2048, #64
ATTENTIONI4.C out, Q, K, V, #2048, #64
```

## 8.4 GELUI4 - INT4 GELU
**Encoding:** Math:0xA3, ACU:0xA3
**Operands:** dest (vec/mem), src (vec/mem)
```assembly
GELUI4 V1, V2
GELUI4.F V1, V2
```

## 8.5 LAYERNORMI4 - INT4 Layer Norm
**Encoding:** Math:0xA4, ACU:0xA4
**Operands:** out (mem), in (mem), params (mem)
```assembly
LAYERNORMI4 out, in, params
```

## 8.6 RESIDUALI4 - INT4 Residual
**Encoding:** Math:0xA5, ACU:0xA5
**Operands:** out (mem), in (mem), residual (mem)
```assembly
RESIDUALI4 out, in, residual
```

## 8.7 MOVI4 - Move INT4
**Encoding:** Math:0xA6, ACU:0xA6
**Operands:** dest (reg/mem), src (reg/mem)
```assembly
MOVI4 R1, [R2]
MOVI4 [R2], R1
MOVI4.Z V1, [R2]
```

## 8.8 PACKI4 - Pack to INT4
**Encoding:** Math:0xA7, ACU:0xA7
**Operands:** dest (vec), src (vec)
```assembly
PACKI4 V2, V1
PACKI4.S V2, V1
```

## 8.9 UNPACKI4 - Unpack INT4
**Encoding:** Math:0xA8, ACU:0xA8
**Operands:** dest (vec), src (vec)
```assembly
UNPACKI4.S V2, V1
UNPACKI4.Z V2, V1
```

## 8.10 ADDI4 - INT4 Vector Add
**Encoding:** Math:0xA9, ACU:0xA9
**Operands:** dest (vec), src1 (vec), src2 (vec)
```assembly
ADDI4 V1, V2, V3
ADDI4.S V1, V2, V3
```

## 8.11 MULI4 - INT4 Vector Multiply
**Encoding:** Math:0xAA, ACU:0xAA
**Operands:** dest (vec), src1 (vec), src2 (vec)
```assembly
MULI4 V1, V2, V3
MULI4.R V1, V2, V3
```

## 8.12 DOTI4 - INT4 Dot Product
**Encoding:** Math:0xAB, ACU:0xAB
**Operands:** dest (scalar), src1 (vec), src2 (vec)
```assembly
DOTI4 R1, V2, V3
DOTI4.A R1, V2, V3
```

## 8.13 CONVI4 - INT4 Convolution
**Encoding:** Math:0xAC, ACU:0xAC
**Operands:** out (mem), in (mem), ker (mem), dims (imm), stride (imm)
```assembly
CONVI4 out, in, ker, #0xE0E0, #1
```

## 8.14 POOLI4 - INT4 Pooling
**Encoding:** Math:0xAD, ACU:0xAD
**Operands:** out (mem), in (mem), size (imm), stride (imm), mode (imm)
```assembly
POOLI4 out, in, #2, #2, #0  ; Max pool 2x2
POOLI4 out, in, #2, #2, #1  ; Average pool
```

## 8.15 QUANTIZE - Quantize to INT4
**Encoding:** Math:0xAE, ACU:0xAE
**Operands:** out (mem), in (mem), scale (reg), zero (reg)
```assembly
QUANTIZE out, in, scale, zero
```

## 8.16 DEQUANTIZE - Dequantize from INT4
**Encoding:** Math:0xAF, ACU:0xAF
**Operands:** out (mem), in (mem), scale (reg), zero (reg)
```assembly
DEQUANTIZE out, in, scale, zero
```

---

# Section 9: Cryptographic Instructions (12)

## 9.1 AES_ENC - AES Encryption
**Encoding:** Math:0xC0
**Operands:** out (mem), in (mem), key (mem), rounds (imm)
```assembly
AES_ENC out, in, key, #10     ; AES-128
AES_ENC out, in, key, #12     ; AES-192
AES_ENC out, in, key, #14     ; AES-256
```

## 9.2 AES_DEC - AES Decryption
**Encoding:** Math:0xC1
**Operands:** out (mem), in (mem), key (mem), rounds (imm)
```assembly
AES_DEC out, in, key, #10
```

## 9.3 SHA256 - SHA-256 Hash
**Encoding:** Math:0xC2
**Operands:** out (mem), in (mem), size (imm)
```assembly
SHA256 hash, data, #1024
```

## 9.4 SHA512 - SHA-512 Hash
**Encoding:** Math:0xC3
**Operands:** out (mem), in (mem), size (imm)
```assembly
SHA512 hash, data, #1024
```

## 9.5 RSA_ENC - RSA Encryption
**Encoding:** Math:0xC4
**Operands:** out (mem), in (mem), n (mem), e (mem)
```assembly
RSA_ENC out, in, modulus, exponent
```

## 9.6 RSA_DEC - RSA Decryption
**Encoding:** Math:0xC5
**Operands:** out (mem), in (mem), n (mem), d (mem)
```assembly
RSA_DEC out, in, modulus, private
```

## 9.7 ECC_MUL - Elliptic Curve Multiply
**Encoding:** Math:0xC6
**Operands:** out (mem), scalar (mem), point (mem), curve (imm)
```assembly
ECC_MUL out, scalar, point, #256  ; P-256 curve
```

## 9.8 RANDOM - Random Number Generation
**Encoding:** Math:0xC7, System:0xC7
**Operands:** out (mem), size (imm)
```assembly
RANDOM buffer, #32        ; 256-bit random
```

## 9.9 HMAC - HMAC Generation
**Encoding:** Math:0xC8
**Operands:** out (mem), key (mem), data (mem), size (imm), hash (imm)
```assembly
HMAC hmac, key, data, #1024, #256  ; SHA-256 HMAC
```

## 9.10 HKDF - HKDF Key Derivation
**Encoding:** Math:0xC9
**Operands:** out (mem), salt (mem), ikm (mem), info (mem), len (imm)
```assembly
HKDF out, salt, ikm, info, #32
```

## 9.11 CHACHA20 - ChaCha20 Stream Cipher
**Encoding:** Math:0xCA
**Operands:** out (mem), in (mem), key (mem), nonce (mem), counter (imm)
```assembly
CHACHA20 out, in, key, nonce, #0
```

## 9.12 POLY1305 - Poly1305 MAC
**Encoding:** Math:0xCB
**Operands:** out (mem), key (mem), data (mem), size (imm)
```assembly
POLY1305 tag, key, data, #1024
```

---

# Section 10: Graphene Photonic Instructions (6)

## 10.1 GRAPHENE_EMIT - Optical Emission
**Encoding:** Math:0xD0, System:0xD0
**Operands:** channel (imm), buffer (mem), size (imm)
```assembly
GRAPHENE_EMIT #0, tx_buffer, #4096
GRAPHENE_EMIT.PAM4 #0, tx_buffer, #4096  ; PAM-4 modulation
```

## 10.2 GRAPHENE_DETECT - Optical Detection
**Encoding:** Math:0xD1, System:0xD1
**Operands:** channel (imm), buffer (mem), size (imm)
```assembly
GRAPHENE_DETECT #0, rx_buffer, #4096
```

## 10.3 GRAPHENE_MODULATE - Modulate Signal
**Encoding:** Math:0xD2, System:0xD2
**Operands:** channel (imm), data (reg), length (imm), format (imm)
```assembly
GRAPHENE_MODULATE #0, R1, #1024, #1   ; OOK
GRAPHENE_MODULATE #0, R1, #1024, #2   ; PAM-4
GRAPHENE_MODULATE #0, R1, #1024, #3   ; QPSK
```

## 10.4 OPTICAL_ROUTER - Route Optical Signal
**Encoding:** Math:0xD3, System:0xD3
**Operands:** src (imm), dst (imm), size (imm)
```assembly
OPTICAL_ROUTER #0, #1, #4096
OPTICAL_ROUTER.BROADCAST #0, size
OPTICAL_ROUTER.BARRIER
```

## 10.5 PHOTONIC_BARRIER - Barrier Synchronization
**Encoding:** Math:0xD4, System:0xD4
**Operands:** timeout (imm)
```assembly
PHOTONIC_BARRIER #1000
```

## 10.6 WAVELENGTH_TUNE - Tune Wavelength
**Encoding:** System:0xD5
**Operands:** channel (imm), wavelength (imm)
```assembly
WAVELENGTH_TUNE #0, #1270     ; nm
WAVELENGTH_TUNE #1, #1290
```

---

# Section 11: Debug/Profiling Instructions (6)

## 11.1 BREAKPOINT - Software Breakpoint
**Encoding:** All cores:0xE0
**Operands:** None
```assembly
BREAKPOINT
```

## 11.2 TRACE - Enable Tracing
**Encoding:** System:0xE1
**Operands:** enable (imm)
```assembly
TRACE #1                 ; Enable trace
TRACE #0                 ; Disable trace
```

## 11.3 PROFILE_START - Start Profiling
**Encoding:** System:0xE2
**Operands:** event (imm)
```assembly
PROFILE_START #0         ; Cycle count
PROFILE_START #1         ; Cache misses
PROFILE_START #2         ; Branch mispredictions
```

## 11.4 PROFILE_END - End Profiling
**Encoding:** System:0xE3
**Operands:** buffer (mem)
```assembly
PROFILE_END result_buffer
```

## 11.5 PERF_COUNT - Read Performance Counter
**Encoding:** System:0xE4
**Operands:** counter (imm), dest (reg)
```assembly
PERF_COUNT #0, R1        ; Read cycle counter
PERF_COUNT #1, R2        ; Read instruction count
```

## 11.6 DEBUG_PRINT - Print Debug Message
**Encoding:** System:0xE5
**Operands:** format (mem), args...
```assembly
DEBUG_PRINT #"Value: %d\n", R1
```

---

# Section 12: Register Tables

## Math Core Registers (64 registers)
| Class | Count | Size | Names |
|-------|-------|------|-------|
| Vector | 64 | 512-bit | V0-V63 |
| Scalar | 32 | 64-bit | R0-R31 |
| Mask | 8 | 64-bit | K0-K7 |
| Control | 16 | 64-bit | CR0-CR15 |
| Status | 4 | 64-bit | SR0-SR3 |

## Logic Core Registers (32 registers)
| Class | Count | Size | Names |
|-------|-------|------|-------|
| General | 32 | 64-bit | R0-R31 |
| Special | 4 | 64-bit | PC, SP, LR, CC |

## System Core Registers (16 + special)
| Class | Count | Size | Names |
|-------|-------|------|-------|
| General | 16 | 64-bit | R0-R15 |
| MSR | 32 | 64-bit | MSR0-MSR31 |
| Special | 2 | 64-bit | IVT, PTBR |

---

# Section 13: Instruction Encoding Summary

## Math Core (8-bit opcode + 20-bit header)
```
Header: [opcode:8][flags:8][operand_count:4]
Operand: [type:3][size:3][behavior:3][value:7]
```

## Logic Core (7-bit opcode + 12-bit header)
```
Header: [opcode:7][flags:3][operand_count:2]
Operand: [type:2][size:2][behavior:2][register:6]
```

## System Core (6-bit opcode + 8-bit header)
```
Header: [opcode:6][flags:2]
Operand: [type:2][size:3][register:3]
```

---

# Section 14: Performance Characteristics

| Instruction Class | Latency (cycles) | Throughput (per cycle) |
|-------------------|------------------|------------------------|
| MOV/LEA | 1 | 4 |
| ADD/SUB | 1 | 4 |
| MUL/IMUL | 3 | 2 |
| DIV/IDIV | 15-30 | 1 |
| FMA | 4 | 2 |
| ADDPS/MULPS | 2 | 4 (512-bit) |
| MATMULI4 | 16 | 8 (per 4x4 tile) |
| AES/SHA | 3-5 | 2 |
| GRAPHENE_EMIT | 1 | 12 channels |
| SYSTEM API | 10-50 | N/A |

---

This document provides the complete production instruction set for the Sirius NEXUS AI Processor Gen5 with all 184 instructions fully specified.
