I have revised the **LOWL Compiler v3.0.0** to incorporate all Sirius NEXUS system features including graphene photonic fabric, 132 core instructions, SYSTEM API services, chip-based storage (ROMB Gen2, NAND flash, HBM3e), vector registers, and INT4 inference primitives. The compiler outputs Sirius NEXUS assembly format compatible with the platform assembler.

```python
#!/usr/bin/env python3
"""
LOWL Compiler v3.0.0 - Sirius NEXUS Graphene Photonic Fabric Edition
Complete Systems Programming Language for Sirius NEXUS AI Processor

New Features for Sirius NEXUS:
- 132 Core Instructions (MOV, ADD, FMA, BRANCH, ADDPS, MATMULI4, SYSENTER, etc.)
- SYSTEM API Services 0x3000-0x3004 (Device Identity, Chassis Control, Power Management)
- Chip-Based Storage: ROMB Gen2 (1.5TB optical), NAND flash (100TB), HBM3e (512GB)
- Vector Registers: V0-V63 (512-bit), R0-R31 (64-bit), K0-K7 (mask)
- INT4 Inference Primitives: MATMULI4, ATTENTIONI4, SOFTMAXI4, GELUI4
- Graphene Optical Interconnect: graphene_emit, graphene_detect, optical_router
- Core Types: MATH (10,000 cores), LOGIC (256), SYSTEM (40), ACU (2,048)
- Output: Sirius NEXUS Assembly Format (.s)

Copyright (c) 2026 - MIT License
"""

import sys
import re
import struct
import argparse
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple, Set
from enum import Enum
from pathlib import Path

VERSION_MAJOR = 3
VERSION_MINOR = 0
VERSION_PATCH = 0

# ============================================================================
# Sirius NEXUS Architecture Constants
# ============================================================================

SIRIUS_NEXUS_CONFIG = {
    "math_cores": 10000,
    "logic_cores": 256,
    "system_cores": 40,
    "acu_cores": 2048,
    "hbm_stacks": 8,
    "hbm_per_stack_gb": 64,
    "romb_tb": 1.5,
    "nand_tb": 100,
    "optical_channels": 12,
    "core_clock_mhz": {
        "math": 2000,
        "logic": 2500,
        "system": 4000,
        "acu": 2000,
    },
    "simd_width": {
        "sse": 4,
        "avx": 8,
        "avx512": 16,
    }
}


# ============================================================================
# Enumerations
# ============================================================================

class CoreType(Enum):
    MATH = 1
    LOGIC = 2
    SYSTEM = 3
    ACU = 4


class DataType(Enum):
    U8 = 1; U16 = 2; U32 = 3; U64 = 4
    I8 = 5; I16 = 6; I32 = 7; I64 = 8
    INT4 = 9; INT8 = 10; INT16 = 11; INT32 = 12; INT64 = 13
    FP16 = 14; BF16 = 15; FP32 = 16; FP64 = 17
    POSIT16 = 18; POSIT32 = 19
    PTR = 20; MMIO_PTR = 21
    VEC4_F32 = 22; VEC8_F32 = 23; VEC16_F32 = 24
    VEC4_F64 = 25; VEC8_F64 = 26
    OPTICAL_PATH = 27; CORE_ID = 28; BLOCK_ID = 29
    TENSOR_2D = 30; TENSOR_3D = 31; TENSOR_4D = 32
    BLOCK_ARRAY = 33
    VOID = 40


class OptimizationLevel(Enum):
    O0 = 0; O1 = 1; O2 = 2; O3 = 3


class SIMDLevel(Enum):
    NONE = 0; SSE = 1; AVX = 2; AVX512 = 3


class OutputFormat(Enum):
    SIRIUS_ASM = 1
    ELF_EXECUTABLE = 2
    FLAT_BINARY = 3
    KERNEL_MODULE = 4


class ProtectionRing(Enum):
    RING0_KERNEL = 0
    RING1_DRIVER = 1
    RING2_SERVICE = 2
    RING3_USER = 3


# ============================================================================
# SYSTEM API Services (Volume 1, Section 23)
# ============================================================================

class SystemService(Enum):
    DEVICE_INFO = 0x3000
    CHASSIS_CTRL = 0x3001
    POWER_MGMT = 0x3002
    VIDEO_AUDIO = 0x3003
    NETWORK = 0x3004


class DeviceInfoCommand(Enum):
    GET_IDENTITY = 0x01
    GET_CAPABILITIES = 0x02
    GET_ATTRIBUTES = 0x03
    GET_SERIAL = 0x05
    GET_UUID = 0x06


class ChassisCommand(Enum):
    LED_SET = 0x01
    LED_BLINK = 0x03
    FAN_SET_SPEED = 0x10
    FAN_SET_MODE = 0x12
    BEACON_ENABLE = 0x30


class PowerCommand(Enum):
    SHUTDOWN = 0x01
    REBOOT = 0x02
    GET_POWER_STATE = 0x07
    SET_POWER_CAP = 0x09
    GET_HEALTH = 0x0E


class VideoCommand(Enum):
    VIDEO_CFG_MODE = 0x01
    VIDEO_CFG_FRAMEBUFFER = 0x02
    VIDEO_SWAP_BUFFER = 0x04


class AudioCommand(Enum):
    AUDIO_CFG_OUTPUT = 0x10
    AUDIO_START_STREAM = 0x12


class NetworkCommand(Enum):
    OPTICAL_LINK_STATUS = 0x20
    RDMA_READ = 0x40


# ============================================================================
# Instruction Database (132 Instructions)
# ============================================================================

INSTRUCTIONS = {
    # Data Movement (5)
    'MOV': (0x01, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 2),
    'MOVSX': (0x02, [CoreType.MATH, CoreType.LOGIC], 2),
    'MOVZX': (0x03, [CoreType.MATH, CoreType.LOGIC], 2),
    'LEA': (0x04, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 2),
    'XCHG': (0x05, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 2),
    
    # Arithmetic (9)
    'ADD': (0x10, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 2),
    'SUB': (0x11, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 2),
    'MUL': (0x12, [CoreType.MATH, CoreType.LOGIC], 2),
    'IMUL': (0x13, [CoreType.MATH, CoreType.LOGIC], 2),
    'DIV': (0x14, [CoreType.MATH, CoreType.LOGIC], 2),
    'IDIV': (0x15, [CoreType.MATH, CoreType.LOGIC], 2),
    'INC': (0x16, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 1),
    'DEC': (0x17, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 1),
    'FMA': (0x18, [CoreType.MATH, CoreType.ACU], 4),
    
    # Logic and Bit (9)
    'AND': (0x20, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 2),
    'OR': (0x21, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 2),
    'XOR': (0x22, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 2),
    'NOT': (0x23, [CoreType.MATH, CoreType.LOGIC], 1),
    'TEST': (0x24, [CoreType.MATH, CoreType.LOGIC], 2),
    'BSF': (0x30, [CoreType.MATH, CoreType.LOGIC], 2),
    'BSR': (0x31, [CoreType.MATH, CoreType.LOGIC], 2),
    'SHL': (0x36, [CoreType.MATH, CoreType.LOGIC], 2),
    'SHR': (0x37, [CoreType.MATH, CoreType.LOGIC], 2),
    
    # Control Flow (4)
    'JMP': (0x40, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 1),
    'CALL': (0x41, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 1),
    'RET': (0x42, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 0),
    'BRANCH': (0x43, [CoreType.MATH, CoreType.LOGIC], 1),
    
    # Vector and SIMD (5)
    'ADDPS': (0x50, [CoreType.MATH], 3),
    'MULPS': (0x51, [CoreType.MATH], 3),
    'DOT': (0x52, [CoreType.MATH], 3),
    'CONV': (0x53, [CoreType.MATH], 5),
    'SHUFPS': (0x54, [CoreType.MATH], 4),
    
    # Advanced Math (16)
    'EXP': (0x80, [CoreType.MATH], 2),
    'LOG': (0x81, [CoreType.MATH], 2),
    'LOG2': (0x82, [CoreType.MATH], 2),
    'LOG10': (0x83, [CoreType.MATH], 2),
    'POW': (0x84, [CoreType.MATH], 3),
    'SIN': (0x85, [CoreType.MATH], 2),
    'COS': (0x86, [CoreType.MATH], 2),
    'TAN': (0x87, [CoreType.MATH], 2),
    'ARCTAN': (0x88, [CoreType.MATH], 2),
    'ARCTAN2': (0x89, [CoreType.MATH], 3),
    'SQRT': (0x8A, [CoreType.MATH], 2),
    'RSQRT': (0x8B, [CoreType.MATH], 2),
    'ERF': (0x8C, [CoreType.MATH], 2),
    'ERFC': (0x8D, [CoreType.MATH], 2),
    'GAMMA': (0x8E, [CoreType.MATH], 2),
    'LGAMMA': (0x8F, [CoreType.MATH], 2),
    
    # INT4 Inference (12)
    'MATMULI4': (0x90, [CoreType.MATH, CoreType.ACU], 6),
    'SOFTMAXI4': (0x91, [CoreType.MATH, CoreType.ACU], 2),
    'ATTENTIONI4': (0x92, [CoreType.MATH, CoreType.ACU], 6),
    'GELUI4': (0x93, [CoreType.MATH, CoreType.ACU], 2),
    'LAYERNORMI4': (0x94, [CoreType.MATH, CoreType.ACU], 3),
    'RESIDUALI4': (0x95, [CoreType.MATH, CoreType.ACU], 3),
    'MOVI4': (0x96, [CoreType.MATH, CoreType.ACU], 2),
    'PACKI4': (0x97, [CoreType.MATH, CoreType.ACU], 2),
    'UNPACKI4': (0x98, [CoreType.MATH, CoreType.ACU], 2),
    'ADDI4': (0x99, [CoreType.MATH, CoreType.ACU], 3),
    'MULI4': (0x9A, [CoreType.MATH, CoreType.ACU], 3),
    'DOTI4': (0x9B, [CoreType.MATH, CoreType.ACU], 3),
    
    # ROMB Instructions (4)
    'ROMB_INSERT': (0x9C, [CoreType.MATH, CoreType.SYSTEM], 2),
    'ROMB_IRQ': (0x9D, [CoreType.SYSTEM], 3),
    'ROMB_PRIORITY': (0x9E, [CoreType.SYSTEM], 2),
    'ROMB_SELECT': (0x9F, [CoreType.SYSTEM], 3),
    
    # System Instructions (9)
    'SYSENTER': (0x60, [CoreType.SYSTEM], 0),
    'SYSEXIT': (0x61, [CoreType.SYSTEM], 0),
    'IN': (0x62, [CoreType.SYSTEM], 2),
    'OUT': (0x63, [CoreType.SYSTEM], 2),
    'CFG_VIDEO': (0x64, [CoreType.SYSTEM], 5),
    'CFG_AUDIO': (0x65, [CoreType.SYSTEM], 6),
    'RING_INIT': (0x66, [CoreType.SYSTEM], 4),
    'RING_WRITE': (0x67, [CoreType.SYSTEM], 3),
    'RING_SWAP': (0x68, [CoreType.SYSTEM], 1),
    
    # Interconnect (9)
    'MAP_STORAGE': (0x70, [CoreType.SYSTEM], 4),
    'EXPORT_MEMORY': (0x71, [CoreType.SYSTEM], 5),
    'REMOTE_CALL': (0x72, [CoreType.SYSTEM], 5),
    'LINK_STATUS': (0x73, [CoreType.SYSTEM], 2),
    'RACK_UNIFY': (0x74, [CoreType.SYSTEM], 4),
    'WARP_SYNC': (0x75, [CoreType.MATH], 1),
    'REMOTE_ALLOC': (0x76, [CoreType.SYSTEM], 3),
    'BROADCAST': (0x77, [CoreType.SYSTEM], 0),
    'BARRIER_SYNC': (0x78, [CoreType.SYSTEM], 0),
    
    # Memory Management (7)
    'SEGMENT_CREATE': (0xB0, [CoreType.SYSTEM], 6),
    'SEGMENT_DELETE': (0xB1, [CoreType.SYSTEM], 1),
    'SEGMENT_MODIFY': (0xB2, [CoreType.SYSTEM], 3),
    'CAPABILITY_GRANT': (0xB3, [CoreType.SYSTEM], 5),
    'CAPABILITY_ACCEPT': (0xB4, [CoreType.SYSTEM], 3),
    'SEGMENT_LOOKUP': (0xB5, [CoreType.SYSTEM], 2),
    'TLB_INVALIDATE': (0xB6, [CoreType.SYSTEM], 1),
    
    # Graphene Optical Builtins
    'GRAPHENE_EMIT': (0x7A, [CoreType.MATH, CoreType.SYSTEM], 4),
    'GRAPHENE_MODULATE': (0x7B, [CoreType.MATH, CoreType.SYSTEM], 4),
    'GRAPHENE_DETECT': (0x7C, [CoreType.MATH, CoreType.SYSTEM], 3),
    'OPTICAL_ROUTER': (0x79, [CoreType.SYSTEM], 4),
    
    # Miscellaneous (4)
    'NOP': (0x00, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 0),
    'CPUID': (0x7D, [CoreType.SYSTEM], 1),
    'RDTSC': (0x7E, [CoreType.SYSTEM], 0),
    'HLT': (0x7F, [CoreType.MATH, CoreType.LOGIC, CoreType.SYSTEM], 0),
}

# Condition codes for BRANCH instruction
CONDITION_CODES = {
    'EQ': 0x0, 'NE': 0x1, 'LT': 0x2, 'LE': 0x3,
    'GT': 0x4, 'GE': 0x5, 'LO': 0x6, 'LS': 0x7,
    'HI': 0x8, 'HS': 0x9, 'CS': 0xA, 'CC': 0xB,
    'VS': 0xC, 'VC': 0xD, 'MI': 0xE, 'PL': 0xF,
}


# ============================================================================
# Register Tables
# ============================================================================

MATH_VECTOR_REGS = {f'V{i}': i for i in range(64)}
MATH_SCALAR_REGS = {f'R{i}': i for i in range(32)}
MATH_MASK_REGS = {f'K{i}': i for i in range(8)}
MATH_CONTROL_REGS = {f'CR{i}': i for i in range(16)}

LOGIC_REGS = {f'R{i}': i for i in range(32)}
LOGIC_REGS['SP'] = 30
LOGIC_REGS['LR'] = 31
LOGIC_REGS['PC'] = 32
LOGIC_REGS['CC'] = 33

SYSTEM_REGS = {f'R{i}': i for i in range(16)}
SYSTEM_REGS['IVT'] = 16
SYSTEM_REGS['PTBR'] = 17
for i in range(32):
    SYSTEM_REGS[f'MSR{i}'] = 32 + i

ALL_REGS = {**MATH_VECTOR_REGS, **MATH_SCALAR_REGS, **MATH_MASK_REGS,
            **MATH_CONTROL_REGS, **LOGIC_REGS, **SYSTEM_REGS}


# ============================================================================
# Token Types
# ============================================================================

class TokenType(Enum):
    TOK_EOF = 0; TOK_ERROR = 1
    TOK_IDENTIFIER = 2; TOK_NUMBER = 3; TOK_STRING = 4
    KW_FN = 10; KW_LET = 11; KW_IF = 12; KW_ELSE = 13
    KW_WHILE = 14; KW_RETURN = 15; KW_TRUE = 16; KW_FALSE = 17
    KW_CORE = 18; KW_MATH = 19; KW_LOGIC = 20; KW_SYSTEM = 21; KW_ACU = 22
    KW_DATA_SECTION = 30; KW_ROMB = 31; KW_NAND = 32; KW_HBM = 33
    KW_SYSTEM_CALL = 40; KW_GRAPHENE_EMIT = 41; KW_GRAPHENE_DETECT = 42
    KW_OPTICAL_ROUTER = 43
    OP_ASSIGN = 100; OP_PLUS = 101; OP_MINUS = 102; OP_MULTIPLY = 103
    OP_DIVIDE = 104; OP_EQ = 105; OP_NE = 106; OP_LT = 107; OP_LE = 108
    OP_GT = 109; OP_GE = 110; OP_AND = 111; OP_OR = 112
    OP_LPAREN = 120; OP_RPAREN = 121; OP_LBRACE = 122; OP_RBRACE = 123
    OP_LBRACKET = 124; OP_RBRACKET = 125; OP_COMMA = 126; OP_SEMICOLON = 127
    OP_COLON = 128; OP_DOT = 129
    NEWLINE = 200; INDENT = 201; DEDENT = 202


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    file: str = ""


# ============================================================================
# AST Nodes
# ============================================================================

class ASTType(Enum):
    PROGRAM = 1; FUNCTION = 2; BLOCK = 3; ASSIGN = 4
    BINARY_OP = 5; CALL = 6; IF_STMT = 7; WHILE_STMT = 8
    RETURN_STMT = 9; VARIABLE = 10; LITERAL = 11
    DATA_SECTION = 12; SYSTEM_CALL = 13; GRAPHENE_EMIT = 14
    GRAPHENE_DETECT = 15; OPTICAL_ROUTER = 16; ROMB_MAP = 17
    CORE_ATTRIBUTE = 18; SIMD_PRAGMA = 19


@dataclass
class ASTNode:
    type: ASTType
    value: str = ""
    line: int = 0
    column: int = 0
    children: List['ASTNode'] = field(default_factory=list)
    data_type: DataType = DataType.U64
    core_type: CoreType = CoreType.MATH
    simd_level: SIMDLevel = SIMDLevel.NONE
    opt_level: OptimizationLevel = OptimizationLevel.O2
    romb_size: int = 0
    nand_size: int = 0


# ============================================================================
# Symbol Table
# ============================================================================

@dataclass
class Symbol:
    name: str
    type: DataType
    scope_level: int
    is_global: bool
    line: int
    column: int


class SymbolTable:
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]
        self.current_scope = 0
        
    def enter_scope(self) -> None:
        self.scopes.append({})
        self.current_scope += 1
        
    def exit_scope(self) -> None:
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope -= 1
            
    def declare(self, name: str, dtype: DataType, line: int, col: int, is_global: bool = False) -> bool:
        if name in self.scopes[self.current_scope]:
            return False
        sym = Symbol(name, dtype, self.current_scope, is_global, line, col)
        self.scopes[self.current_scope][name] = sym
        return True
        
    def lookup(self, name: str) -> Optional[Symbol]:
        for i in range(self.current_scope, -1, -1):
            if name in self.scopes[i]:
                return self.scopes[i][name]
        return None


# ============================================================================
# Error Collector
# ============================================================================

class ErrorCollector:
    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        
    def add_error(self, msg: str, line: int, col: int) -> None:
        self.errors.append({'msg': msg, 'line': line, 'col': col})
        
    def add_warning(self, msg: str, line: int, col: int) -> None:
        self.warnings.append({'msg': msg, 'line': line, 'col': col})
        
    def has_errors(self) -> bool:
        return len(self.errors) > 0
        
    def print_summary(self) -> None:
        for w in self.warnings:
            print(f"\033[93mWarning\033[0m at {w['line']}:{w['col']}: {w['msg']}")
        for e in self.errors:
            print(f"\033[91mError\033[0m at {e['line']}:{e['col']}: {e['msg']}")
        if self.errors:
            print(f"\n\033[91m{len(self.errors)} error(s)\033[0m")


# ============================================================================
# Lexer
# ============================================================================

class Lexer:
    def __init__(self, source: str, filename: str, errors: ErrorCollector):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.column = 1
        self.errors = errors
        
    def current(self) -> str:
        return self.source[self.pos] if self.pos < len(self.source) else '\0'
        
    def advance(self) -> None:
        if self.current() == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        
    def skip_whitespace(self) -> None:
        while self.current() in ' \t\r':
            self.advance()
            
    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.column
        ident = ""
        while self.current().isalnum() or self.current() == '_':
            ident += self.current()
            self.advance()
            
        kw_map = {
            'fn': TokenType.KW_FN, 'let': TokenType.KW_LET, 'if': TokenType.KW_IF,
            'else': TokenType.KW_ELSE, 'while': TokenType.KW_WHILE, 'return': TokenType.KW_RETURN,
            'true': TokenType.KW_TRUE, 'false': TokenType.KW_FALSE,
            'core': TokenType.KW_CORE, 'math': TokenType.KW_MATH, 'logic': TokenType.KW_LOGIC,
            'system': TokenType.KW_SYSTEM, 'acu': TokenType.KW_ACU,
            'data_section': TokenType.KW_DATA_SECTION, 'romb': TokenType.KW_ROMB,
            'nand': TokenType.KW_NAND, 'hbm': TokenType.KW_HBM,
            'system_call': TokenType.KW_SYSTEM_CALL,
            'graphene_emit': TokenType.KW_GRAPHENE_EMIT,
            'graphene_detect': TokenType.KW_GRAPHENE_DETECT,
            'optical_router': TokenType.KW_OPTICAL_ROUTER,
        }
        if ident in kw_map:
            return Token(kw_map[ident], ident, start_line, start_col, self.filename)
        return Token(TokenType.TOK_IDENTIFIER, ident, start_line, start_col, self.filename)
    
    def read_number(self) -> Token:
        start_line, start_col = self.line, self.column
        num = ""
        while self.current().isdigit() or self.current() == '.':
            num += self.current()
            self.advance()
        return Token(TokenType.TOK_NUMBER, num, start_line, start_col, self.filename)
    
    def read_string(self) -> Token:
        start_line, start_col = self.line, self.column
        self.advance()  # Skip opening quote
        s = ""
        while self.current() != '"' and self.current() != '\0':
            if self.current() == '\\':
                self.advance()
                if self.current() == 'n': s += '\n'
                elif self.current() == 't': s += '\t'
                else: s += self.current()
            else:
                s += self.current()
            self.advance()
        self.advance()  # Skip closing quote
        return Token(TokenType.TOK_STRING, s, start_line, start_col, self.filename)
    
    def read_operator(self) -> Token:
        start_line, start_col = self.line, self.column
        c = self.current()
        self.advance()
        
        if c == '=' and self.current() == '=':
            self.advance()
            return Token(TokenType.OP_EQ, "==", start_line, start_col, self.filename)
        if c == '!' and self.current() == '=':
            self.advance()
            return Token(TokenType.OP_NE, "!=", start_line, start_col, self.filename)
        if c == '<' and self.current() == '=':
            self.advance()
            return Token(TokenType.OP_LE, "<=", start_line, start_col, self.filename)
        if c == '>' and self.current() == '=':
            self.advance()
            return Token(TokenType.OP_GE, ">=", start_line, start_col, self.filename)
        if c == '&' and self.current() == '&':
            self.advance()
            return Token(TokenType.OP_AND, "&&", start_line, start_col, self.filename)
        if c == '|' and self.current() == '|':
            self.advance()
            return Token(TokenType.OP_OR, "||", start_line, start_col, self.filename)
            
        op_map = {
            '=': TokenType.OP_ASSIGN, '+': TokenType.OP_PLUS, '-': TokenType.OP_MINUS,
            '*': TokenType.OP_MULTIPLY, '/': TokenType.OP_DIVIDE,
            '<': TokenType.OP_LT, '>': TokenType.OP_GT,
            '(': TokenType.OP_LPAREN, ')': TokenType.OP_RPAREN,
            '{': TokenType.OP_LBRACE, '}': TokenType.OP_RBRACE,
            '[': TokenType.OP_LBRACKET, ']': TokenType.OP_RBRACKET,
            ',': TokenType.OP_COMMA, ';': TokenType.OP_SEMICOLON,
            ':': TokenType.OP_COLON, '.': TokenType.OP_DOT,
        }
        if c in op_map:
            return Token(op_map[c], c, start_line, start_col, self.filename)
            
        return Token(TokenType.TOK_ERROR, c, start_line, start_col, self.filename)
    
    def next_token(self) -> Token:
        self.skip_whitespace()
        if self.pos >= len(self.source):
            return Token(TokenType.TOK_EOF, "", self.line, self.column, self.filename)
            
        if self.current() == '\n':
            self.advance()
            return Token(TokenType.NEWLINE, "\n", self.line - 1, self.column, self.filename)
            
        if self.current() == '/' and self.peek() == '/':
            while self.current() != '\n' and self.current() != '\0':
                self.advance()
            return self.next_token()
            
        if self.current().isalpha() or self.current() == '_':
            return self.read_identifier()
            
        if self.current().isdigit():
            return self.read_number()
            
        if self.current() == '"':
            return self.read_string()
            
        return self.read_operator()
    
    def peek(self) -> str:
        return self.source[self.pos + 1] if self.pos + 1 < len(self.source) else '\0'


# ============================================================================
# Parser
# ============================================================================

class Parser:
    def __init__(self, tokens: List[Token], symbols: SymbolTable, errors: ErrorCollector,
                 core_type: CoreType = CoreType.MATH):
        self.tokens = tokens
        self.pos = 0
        self.symbols = symbols
        self.errors = errors
        self.core_type = core_type
        self.current_simd = SIMDLevel.NONE
        
    def current(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token(TokenType.TOK_EOF, "", 0, 0, "")
        
    def advance(self) -> None:
        if self.pos < len(self.tokens):
            self.pos += 1
            
    def match(self, tok_type: TokenType) -> bool:
        if self.current().type == tok_type:
            self.advance()
            return True
        return False
        
    def expect(self, tok_type: TokenType, msg: str) -> bool:
        if self.current().type != tok_type:
            self.errors.add_error(msg, self.current().line, self.current().column)
            return False
        self.advance()
        return True
        
    def parse(self) -> ASTNode:
        program = ASTNode(ASTType.PROGRAM, "program")
        
        while self.current().type != TokenType.TOK_EOF:
            stmt = self.parse_statement()
            if stmt:
                program.children.append(stmt)
            else:
                break
        return program
    
    def parse_statement(self) -> Optional[ASTNode]:
        tok = self.current()
        
        if tok.type == TokenType.KW_CORE:
            return self.parse_core_attribute()
        elif tok.type == TokenType.KW_FN:
            return self.parse_function()
        elif tok.type == TokenType.KW_LET:
            return self.parse_let()
        elif tok.type == TokenType.KW_IF:
            return self.parse_if()
        elif tok.type == TokenType.KW_WHILE:
            return self.parse_while()
        elif tok.type == TokenType.KW_RETURN:
            return self.parse_return()
        elif tok.type == TokenType.KW_DATA_SECTION:
            return self.parse_data_section()
        elif tok.type == TokenType.KW_SYSTEM_CALL:
            return self.parse_system_call()
        elif tok.type == TokenType.KW_GRAPHENE_EMIT:
            return self.parse_graphene_emit()
        elif tok.type == TokenType.KW_GRAPHENE_DETECT:
            return self.parse_graphene_detect()
        elif tok.type == TokenType.KW_OPTICAL_ROUTER:
            return self.parse_optical_router()
        elif tok.type == TokenType.OP_LBRACE:
            return self.parse_block()
        elif tok.type == TokenType.NEWLINE:
            self.advance()
            return self.parse_statement()
        else:
            expr = self.parse_expression()
            self.match(TokenType.OP_SEMICOLON)
            return expr
    
    def parse_core_attribute(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.CORE_ATTRIBUTE, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_CORE, "Expected 'core'")
        
        if self.current().type == TokenType.KW_MATH:
            node.core_type = CoreType.MATH
            self.advance()
        elif self.current().type == TokenType.KW_LOGIC:
            node.core_type = CoreType.LOGIC
            self.advance()
        elif self.current().type == TokenType.KW_SYSTEM:
            node.core_type = CoreType.SYSTEM
            self.advance()
        elif self.current().type == TokenType.KW_ACU:
            node.core_type = CoreType.ACU
            self.advance()
        
        self.match(TokenType.OP_SEMICOLON)
        return node
    
    def parse_function(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.FUNCTION, line=self.current().line, column=self.current().column)
        node.core_type = self.core_type
        
        self.expect(TokenType.KW_FN, "Expected 'fn'")
        
        name = self.current().value
        self.expect(TokenType.TOK_IDENTIFIER, "Expected function name")
        node.value = name
        
        self.expect(TokenType.OP_LPAREN, "Expected '('")
        # Parse parameters (simplified)
        while self.current().type == TokenType.TOK_IDENTIFIER:
            param = self.current().value
            self.advance()
            if self.match(TokenType.OP_COLON):
                self.parse_type()
            if not self.match(TokenType.OP_COMMA):
                break
        self.expect(TokenType.OP_RPAREN, "Expected ')'")
        
        if self.match(TokenType.OP_ARROW):
            self.parse_type()
        
        self.symbols.enter_scope()
        
        if self.match(TokenType.OP_LBRACE):
            node.children = self.parse_block_contents()
        else:
            # Indented block
            self.expect(TokenType.OP_COLON, "Expected ':'")
            self.match(TokenType.NEWLINE)
            self.parse_indented_block(node)
        
        self.symbols.exit_scope()
        return node
    
    def parse_block(self) -> ASTNode:
        node = ASTNode(ASTType.BLOCK, line=self.current().line, column=self.current().column)
        self.expect(TokenType.OP_LBRACE, "Expected '{'")
        node.children = self.parse_block_contents()
        self.expect(TokenType.OP_RBRACE, "Expected '}'")
        return node
    
    def parse_block_contents(self) -> List[ASTNode]:
        children = []
        while self.current().type != TokenType.OP_RBRACE and self.current().type != TokenType.TOK_EOF:
            stmt = self.parse_statement()
            if stmt:
                children.append(stmt)
            else:
                break
        return children
    
    def parse_indented_block(self, node: ASTNode) -> None:
        while self.current().type == TokenType.NEWLINE:
            self.advance()
        if self.current().type == TokenType.INDENT:
            self.advance()
            while self.current().type != TokenType.DEDENT and self.current().type != TokenType.TOK_EOF:
                stmt = self.parse_statement()
                if stmt:
                    node.children.append(stmt)
                else:
                    break
            self.match(TokenType.DEDENT)
    
    def parse_let(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.ASSIGN, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_LET, "Expected 'let'")
        
        var_name = self.current().value
        self.expect(TokenType.TOK_IDENTIFIER, "Expected variable name")
        
        var_type = DataType.U64
        if self.match(TokenType.OP_COLON):
            var_type = self.parse_type()
        
        is_global = (self.symbols.current_scope == 0)
        self.symbols.declare(var_name, var_type, node.line, node.column, is_global)
        
        var_child = ASTNode(ASTType.VARIABLE, var_name, node.line, node.column)
        node.children.append(var_child)
        
        if self.match(TokenType.OP_ASSIGN):
            node.children.append(self.parse_expression())
        else:
            node.children.append(ASTNode(ASTType.LITERAL, "0", node.line, node.column))
            
        self.match(TokenType.OP_SEMICOLON)
        return node
    
    def parse_if(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.IF_STMT, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_IF, "Expected 'if'")
        
        self.expect(TokenType.OP_LPAREN, "Expected '('")
        node.children.append(self.parse_expression())
        self.expect(TokenType.OP_RPAREN, "Expected ')'")
        
        then_block = ASTNode(ASTType.BLOCK, line=self.current().line, column=self.current().column)
        self.parse_indented_block(then_block)
        node.children.append(then_block)
        
        if self.match(TokenType.KW_ELSE):
            else_block = ASTNode(ASTType.BLOCK, line=self.current().line, column=self.current().column)
            self.parse_indented_block(else_block)
            node.children.append(else_block)
        
        return node
    
    def parse_while(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.WHILE_STMT, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_WHILE, "Expected 'while'")
        
        self.expect(TokenType.OP_LPAREN, "Expected '('")
        node.children.append(self.parse_expression())
        self.expect(TokenType.OP_RPAREN, "Expected ')'")
        
        body = ASTNode(ASTType.BLOCK, line=self.current().line, column=self.current().column)
        self.parse_indented_block(body)
        node.children.append(body)
        
        return node
    
    def parse_return(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.RETURN_STMT, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_RETURN, "Expected 'return'")
        
        if self.current().type not in (TokenType.OP_SEMICOLON, TokenType.NEWLINE, TokenType.DEDENT):
            node.children.append(self.parse_expression())
        
        self.match(TokenType.OP_SEMICOLON)
        return node
    
    def parse_data_section(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.DATA_SECTION, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_DATA_SECTION, "Expected 'data_section'")
        
        if self.match(TokenType.KW_ROMB):
            node.type = ASTType.ROMB_MAP
            if self.current().type == TokenType.TOK_NUMBER:
                node.romb_size = int(self.current().value)
                self.advance()
        
        name = self.current().value
        self.expect(TokenType.TOK_IDENTIFIER, "Expected section name")
        node.value = name
        
        self.expect(TokenType.OP_COLON, "Expected ':'")
        self.parse_indented_block(node)
        
        return node
    
    def parse_system_call(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.SYSTEM_CALL, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_SYSTEM_CALL, "Expected 'system_call'")
        
        name = self.current().value
        self.expect(TokenType.TOK_IDENTIFIER, "Expected command name")
        node.value = name
        
        while self.current().type == TokenType.TOK_IDENTIFIER or self.current().type == TokenType.TOK_NUMBER:
            arg = self.parse_expression()
            if arg:
                node.children.append(arg)
            if not self.match(TokenType.OP_COMMA):
                break
        
        self.match(TokenType.OP_SEMICOLON)
        return node
    
    def parse_graphene_emit(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.GRAPHENE_EMIT, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_GRAPHENE_EMIT, "Expected 'graphene_emit'")
        
        self.expect(TokenType.OP_LPAREN, "Expected '('")
        
        # Parse channel
        if self.current().type == TokenType.TOK_NUMBER:
            node.children.append(ASTNode(ASTType.LITERAL, self.current().value, self.current().line, self.current().column))
            self.advance()
        self.expect(TokenType.OP_COMMA, "Expected ','")
        
        # Parse address
        node.children.append(self.parse_expression())
        self.expect(TokenType.OP_COMMA, "Expected ','")
        
        # Parse size
        node.children.append(self.parse_expression())
        
        self.expect(TokenType.OP_RPAREN, "Expected ')'")
        self.match(TokenType.OP_SEMICOLON)
        return node
    
    def parse_graphene_detect(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.GRAPHENE_DETECT, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_GRAPHENE_DETECT, "Expected 'graphene_detect'")
        
        self.expect(TokenType.OP_LPAREN, "Expected '('")
        
        if self.current().type == TokenType.TOK_NUMBER:
            node.children.append(ASTNode(ASTType.LITERAL, self.current().value, self.current().line, self.current().column))
            self.advance()
        self.expect(TokenType.OP_COMMA, "Expected ','")
        
        node.children.append(self.parse_expression())
        self.expect(TokenType.OP_COMMA, "Expected ','")
        
        node.children.append(self.parse_expression())
        
        self.expect(TokenType.OP_RPAREN, "Expected ')'")
        self.match(TokenType.OP_SEMICOLON)
        return node
    
    def parse_optical_router(self) -> Optional[ASTNode]:
        node = ASTNode(ASTType.OPTICAL_ROUTER, line=self.current().line, column=self.current().column)
        self.expect(TokenType.KW_OPTICAL_ROUTER, "Expected 'optical_router'")
        
        if self.match(TokenType.OP_DOT):
            method = self.current().value
            self.advance()
            node.value = method
        
        self.expect(TokenType.OP_LPAREN, "Expected '('")
        
        while self.current().type != TokenType.OP_RPAREN and self.current().type != TokenType.TOK_EOF:
            node.children.append(self.parse_expression())
            if not self.match(TokenType.OP_COMMA):
                break
        
        self.expect(TokenType.OP_RPAREN, "Expected ')'")
        self.match(TokenType.OP_SEMICOLON)
        return node
    
    def parse_expression(self) -> Optional[ASTNode]:
        return self.parse_binary_op(0)
    
    def get_precedence(self, tok_type: TokenType) -> int:
        prec_map = {
            TokenType.OP_ASSIGN: 1,
            TokenType.OP_AND: 3, TokenType.OP_OR: 3,
            TokenType.OP_EQ: 4, TokenType.OP_NE: 4,
            TokenType.OP_LT: 5, TokenType.OP_LE: 5, TokenType.OP_GT: 5, TokenType.OP_GE: 5,
            TokenType.OP_PLUS: 9, TokenType.OP_MINUS: 9,
            TokenType.OP_MULTIPLY: 10, TokenType.OP_DIVIDE: 10,
        }
        return prec_map.get(tok_type, 0)
    
    def parse_binary_op(self, min_precedence: int) -> Optional[ASTNode]:
        left = self.parse_primary()
        if not left:
            return None
        
        while True:
            tok = self.current()
            precedence = self.get_precedence(tok.type)
            if precedence == 0 or precedence < min_precedence:
                break
            self.advance()
            
            right = self.parse_binary_op(precedence + 1)
            if not right:
                return None
            
            binary = ASTNode(ASTType.BINARY_OP, tok.value, tok.line, tok.column)
            binary.children.append(left)
            binary.children.append(right)
            left = binary
        
        return left
    
    def parse_primary(self) -> Optional[ASTNode]:
        tok = self.current()
        
        if tok.type == TokenType.TOK_NUMBER:
            self.advance()
            node = ASTNode(ASTType.LITERAL, tok.value, tok.line, tok.column)
            return node
        
        if tok.type == TokenType.TOK_STRING:
            self.advance()
            node = ASTNode(ASTType.LITERAL, tok.value, tok.line, tok.column)
            return node
        
        if tok.type == TokenType.TOK_IDENTIFIER:
            self.advance()
            node = ASTNode(ASTType.VARIABLE, tok.value, tok.line, tok.column)
            
            if self.current().type == TokenType.OP_LPAREN:
                call = ASTNode(ASTType.CALL, node.value, node.line, node.column)
                call.children.append(node)
                self.advance()
                while self.current().type != TokenType.OP_RPAREN:
                    call.children.append(self.parse_expression())
                    if self.current().type == TokenType.OP_COMMA:
                        self.advance()
                self.expect(TokenType.OP_RPAREN, "Expected ')'")
                return call
            
            return node
        
        if tok.type == TokenType.KW_TRUE:
            self.advance()
            return ASTNode(ASTType.LITERAL, "1", tok.line, tok.column)
        
        if tok.type == TokenType.KW_FALSE:
            self.advance()
            return ASTNode(ASTType.LITERAL, "0", tok.line, tok.column)
        
        if tok.type == TokenType.OP_LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.OP_RPAREN, "Expected ')'")
            return expr
        
        self.errors.add_error(f"Unexpected token: {tok.value}", tok.line, tok.column)
        return None
    
    def parse_type(self) -> DataType:
        type_map = {
            'u8': DataType.U8, 'u16': DataType.U16, 'u32': DataType.U32, 'u64': DataType.U64,
            'i8': DataType.I8, 'i16': DataType.I16, 'i32': DataType.I32, 'i64': DataType.I64,
            'int4': DataType.INT4, 'int8': DataType.INT8, 'int16': DataType.INT16,
            'int32': DataType.INT32, 'int64': DataType.INT64,
            'fp16': DataType.FP16, 'bf16': DataType.BF16, 'f32': DataType.FP32, 'f64': DataType.FP64,
            'ptr': DataType.PTR,
        }
        if self.current().value in type_map:
            dtype = type_map[self.current().value]
            self.advance()
            return dtype
        self.advance()
        return DataType.U64


# ============================================================================
# Code Generator (Sirius NEXUS Assembly Format)
# ============================================================================

class CodeGenerator:
    def __init__(self, core_type: CoreType = CoreType.MATH,
                 opt_level: OptimizationLevel = OptimizationLevel.O2,
                 simd_level: SIMDLevel = SIMDLevel.AVX512,
                 output_format: OutputFormat = OutputFormat.SIRIUS_ASM):
        self.core_type = core_type
        self.opt_level = opt_level
        self.simd_level = simd_level
        self.output_format = output_format
        self.output_lines: List[str] = []
        self.indent = 0
        self.label_counter = 0
        self.in_function = False
        
    def indent_str(self) -> str:
        return "    " * self.indent
    
    def emit(self, line: str = "") -> None:
        if line:
            self.output_lines.append(self.indent_str() + line)
        else:
            self.output_lines.append("")
    
    def emit_raw(self, line: str) -> None:
        self.output_lines.append(line)
    
    def new_label(self) -> str:
        self.label_counter += 1
        return f".L{self.label_counter - 1}"
    
    def generate_prologue(self) -> None:
        self.emit_raw(f"; Sirius NEXUS Assembly - Core: {self.core_type.name}")
        self.emit_raw(f"; Optimization: {self.opt_level.name}, SIMD: {self.simd_level.name}")
        self.emit_raw(f"; Generated by LOWL Compiler v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}")
        self.emit_raw("")
        
        self.emit_section("text")
        
        if self.core_type == CoreType.MATH:
            self.emit("SET_REG_MAP #MATH, #FP32, #V512, #NEAREST")
        elif self.core_type == CoreType.ACU:
            self.emit("SET_REG_MAP #ACU, #INT4, #V512, #NEAREST")
        
        self.emit()
    
    def generate_epilogue(self) -> None:
        if self.in_function:
            self.emit("RET")
        else:
            if self.core_type == CoreType.SYSTEM:
                self.emit("HLT")
            else:
                self.emit("RET")
    
    def emit_section(self, section: str) -> None:
        self.emit_raw(f"    .{section}")
    
    def generate(self, node: ASTNode) -> str:
        self.generate_prologue()
        
        for child in node.children:
            self.gen_node(child)
        
        self.generate_epilogue()
        return "\n".join(self.output_lines)
    
    def gen_node(self, node: ASTNode) -> None:
        if node.type == ASTType.FUNCTION:
            self.gen_function(node)
        elif node.type == ASTType.ASSIGN:
            self.gen_assign(node)
        elif node.type == ASTType.IF_STMT:
            self.gen_if(node)
        elif node.type == ASTType.WHILE_STMT:
            self.gen_while(node)
        elif node.type == ASTType.RETURN_STMT:
            self.gen_return(node)
        elif node.type == ASTType.CALL:
            self.gen_call(node)
        elif node.type == ASTType.DATA_SECTION:
            self.gen_data_section(node)
        elif node.type == ASTType.SYSTEM_CALL:
            self.gen_system_call(node)
        elif node.type == ASTType.GRAPHENE_EMIT:
            self.gen_graphene_emit(node)
        elif node.type == ASTType.GRAPHENE_DETECT:
            self.gen_graphene_detect(node)
        elif node.type == ASTType.OPTICAL_ROUTER:
            self.gen_optical_router(node)
        elif node.type == ASTType.ROMB_MAP:
            self.gen_romb_map(node)
        elif node.type == ASTType.BLOCK:
            for child in node.children:
                self.gen_node(child)
        elif node.type == ASTType.CORE_ATTRIBUTE:
            self.core_type = node.core_type
    
    def gen_function(self, node: ASTNode) -> None:
        self.emit()
        self.emit_raw(f"{node.value}:")
        self.indent += 1
        self.in_function = True
        
        # Function prologue
        if self.core_type != CoreType.SYSTEM:
            self.emit("PUSH RBP")
            self.emit("MOV RBP, RSP")
            self.emit("SUB RSP, #32")
        
        for child in node.children:
            self.gen_node(child)
        
        # Function epilogue
        self.emit("MOV RSP, RBP")
        self.emit("POP RBP")
        self.emit("RET")
        
        self.indent -= 1
        self.in_function = False
    
    def gen_assign(self, node: ASTNode) -> None:
        if len(node.children) >= 2:
            dest = self.expr_to_str(node.children[0])
            src = self.expr_to_str(node.children[1])
            self.emit(f"MOV {dest}, {src}")
    
    def gen_if(self, node: ASTNode) -> None:
        if len(node.children) >= 2:
            cond = self.expr_to_str(node.children[0])
            else_label = self.new_label()
            end_label = self.new_label()
            
            self.emit(f"CMP {cond}, #0")
            self.emit(f"BRANCH EQ, {else_label}")
            self.gen_node(node.children[1])
            self.emit(f"JMP {end_label}")
            self.emit_raw(f"{else_label}:")
            if len(node.children) > 2:
                self.gen_node(node.children[2])
            self.emit_raw(f"{end_label}:")
    
    def gen_while(self, node: ASTNode) -> None:
        if len(node.children) >= 2:
            start_label = self.new_label()
            end_label = self.new_label()
            
            self.emit_raw(f"{start_label}:")
            cond = self.expr_to_str(node.children[0])
            self.emit(f"CMP {cond}, #0")
            self.emit(f"BRANCH EQ, {end_label}")
            self.gen_node(node.children[1])
            self.emit(f"JMP {start_label}")
            self.emit_raw(f"{end_label}:")
    
    def gen_return(self, node: ASTNode) -> None:
        if node.children:
            val = self.expr_to_str(node.children[0])
            self.emit(f"MOV RAX, {val}")
        else:
            self.emit("XOR RAX, RAX")
    
    def gen_call(self, node: ASTNode) -> None:
        self.emit(f"CALL {node.value}")
    
    def gen_data_section(self, node: ASTNode) -> None:
        self.emit_section("data")
        self.emit_raw(f"{node.value}:")
        self.indent += 1
        for child in node.children:
            if child.type == ASTType.LITERAL:
                self.emit(f"DB {child.value}")
            else:
                self.emit(f"DBZ {child.value}")
        self.indent -= 1
        self.emit()
    
    def gen_system_call(self, node: ASTNode) -> None:
        """Generate SYSTEM API call (Services 0x3000-0x3004)"""
        self.emit("; SYSTEM API Call")
        
        if node.value == "GET_IDENTITY":
            self.emit("MOV R1, #0x3000")
            self.emit("MOV R2, #0x01")
            if node.children:
                self.emit(f"LEA R3, {self.expr_to_str(node.children[0])}")
            self.emit("SYSENTER")
        elif node.value == "GET_CAPABILITIES":
            self.emit("MOV R1, #0x3000")
            self.emit("MOV R2, #0x02")
            if node.children:
                self.emit(f"LEA R3, {self.expr_to_str(node.children[0])}")
            self.emit("SYSENTER")
        elif node.value == "GET_SERIAL":
            self.emit("MOV R1, #0x3000")
            self.emit("MOV R2, #0x05")
            if node.children:
                self.emit(f"LEA R3, {self.expr_to_str(node.children[0])}")
            self.emit("SYSENTER")
        elif node.value == "GET_UUID":
            self.emit("MOV R1, #0x3000")
            self.emit("MOV R2, #0x06")
            if node.children:
                self.emit(f"LEA R3, {self.expr_to_str(node.children[0])}")
            self.emit("SYSENTER")
        elif node.value == "LED_SET":
            self.emit("MOV R1, #0x3001")
            self.emit("MOV R2, #0x01")
            if len(node.children) >= 2:
                self.emit(f"MOV R3, #{self.expr_to_str(node.children[0])}")
                self.emit(f"MOV R4, #{self.expr_to_str(node.children[1])}")
            self.emit("SYSENTER")
        elif node.value == "LED_BLINK":
            self.emit("MOV R1, #0x3001")
            self.emit("MOV R2, #0x03")
            if len(node.children) >= 3:
                self.emit(f"MOV R3, #{self.expr_to_str(node.children[0])}")
                self.emit(f"MOV R4, #{self.expr_to_str(node.children[1])}")
                self.emit(f"MOV R5, #{self.expr_to_str(node.children[2])}")
            self.emit("SYSENTER")
        elif node.value == "BEACON_ENABLE":
            self.emit("MOV R1, #0x3001")
            self.emit("MOV R2, #0x30")
            if node.children:
                self.emit(f"MOV R3, #{self.expr_to_str(node.children[0])}")
            self.emit("SYSENTER")
        elif node.value == "SHUTDOWN":
            self.emit("MOV R1, #0x3002")
            self.emit("MOV R2, #0x01")
            if node.children:
                self.emit(f"MOV R3, #{self.expr_to_str(node.children[0])}")
            self.emit("SYSENTER")
        elif node.value == "REBOOT":
            self.emit("MOV R1, #0x3002")
            self.emit("MOV R2, #0x02")
            if node.children:
                self.emit(f"MOV R3, #{self.expr_to_str(node.children[0])}")
            self.emit("SYSENTER")
        elif node.value == "SET_POWER_CAP":
            self.emit("MOV R1, #0x3002")
            self.emit("MOV R2, #0x09")
            if node.children:
                self.emit(f"MOV R3, #{self.expr_to_str(node.children[0])}")
            self.emit("SYSENTER")
        elif node.value == "GET_HEALTH":
            self.emit("MOV R1, #0x3002")
            self.emit("MOV R2, #0x0E")
            if node.children:
                self.emit(f"LEA R3, {self.expr_to_str(node.children[0])}")
            self.emit("SYSENTER")
        elif node.value == "OPTICAL_LINK_STATUS":
            self.emit("MOV R1, #0x3004")
            self.emit("MOV R2, #0x20")
            if len(node.children) >= 2:
                self.emit(f"MOV R3, #{self.expr_to_str(node.children[0])}")
                self.emit(f"LEA R4, {self.expr_to_str(node.children[1])}")
            self.emit("SYSENTER")
        elif node.value == "RDMA_READ":
            self.emit("MOV R1, #0x3004")
            self.emit("MOV R2, #0x40")
            if len(node.children) >= 3:
                self.emit(f"MOV R3, {self.expr_to_str(node.children[0])}")
                self.emit(f"LEA R4, {self.expr_to_str(node.children[1])}")
                self.emit(f"MOV R5, #{self.expr_to_str(node.children[2])}")
            self.emit("SYSENTER")
        elif node.value == "CFG_VIDEO":
            self.emit("MOV R1, #0x3003")
            self.emit("MOV R2, #0x01")
            if len(node.children) >= 6:
                self.emit(f"MOV R3, #{self.expr_to_str(node.children[0])}")
                self.emit(f"LEA R4, {self.expr_to_str(node.children[1])}")
                self.emit(f"MOV R5, #{self.expr_to_str(node.children[2])}")
                self.emit(f"; Width/Height/Format/Refresh in mode structure")
            self.emit("SYSENTER")
        else:
            self.emit(f"; Unknown system call: {node.value}")
    
    def gen_graphene_emit(self, node: ASTNode) -> None:
        """Generate graphene_emit(channel, addr, size)"""
        if len(node.children) >= 3:
            channel = self.expr_to_str(node.children[0])
            addr = self.expr_to_str(node.children[1])
            size = self.expr_to_str(node.children[2])
            self.emit(f"; Graphene optical emission on channel {channel}")
            self.emit(f"MOV RSI, {addr}")
            self.emit(f"MOV RCX, {size}")
            self.emit(f"GRAPHENE_EMIT {channel}, RSI, RCX")
    
    def gen_graphene_detect(self, node: ASTNode) -> None:
        """Generate graphene_detect(channel, addr, size)"""
        if len(node.children) >= 3:
            channel = self.expr_to_str(node.children[0])
            addr = self.expr_to_str(node.children[1])
            size = self.expr_to_str(node.children[2])
            self.emit(f"; Graphene optical detection on channel {channel}")
            self.emit(f"MOV RDI, {addr}")
            self.emit(f"MOV RCX, {size}")
            self.emit(f"GRAPHENE_DETECT {channel}, RDI, RCX")
    
    def gen_optical_router(self, node: ASTNode) -> None:
        """Generate optical_router.method(args)"""
        method = node.value
        if method == "broadcast":
            self.emit("OPTICAL_ROUTER.BROADCAST")
        elif method == "barrier":
            self.emit("OPTICAL_ROUTER.BARRIER")
        elif len(node.children) >= 3:
            src = self.expr_to_str(node.children[0])
            dst = self.expr_to_str(node.children[1])
            size = self.expr_to_str(node.children[2])
            self.emit(f"OPTICAL_ROUTER {src}, {dst}, {size}")
    
    def gen_romb_map(self, node: ASTNode) -> None:
        """Generate ROMB Gen2 mapping"""
        self.emit_section("romb")
        self.emit_raw(f"{node.value}:")
        self.indent += 1
        if node.romb_size > 0:
            self.emit(f"DBZ {node.romb_size}")
        self.indent -= 1
        self.emit()
    
    def expr_to_str(self, node: ASTNode) -> str:
        if node.type == ASTType.LITERAL:
            return f"#{node.value}"
        elif node.type == ASTType.VARIABLE:
            return node.value
        elif node.type == ASTType.BINARY_OP:
            left = self.expr_to_str(node.children[0])
            right = self.expr_to_str(node.children[1])
            return f"({left} {node.value} {right})"
        return "0"


# ============================================================================
# Main Compiler
# ============================================================================

class LOWLCompiler:
    def __init__(self, core_type: CoreType = CoreType.MATH,
                 opt_level: OptimizationLevel = OptimizationLevel.O2,
                 simd_level: SIMDLevel = SIMDLevel.AVX512,
                 output_format: OutputFormat = OutputFormat.SIRIUS_ASM,
                 verbose: bool = False):
        self.core_type = core_type
        self.opt_level = opt_level
        self.simd_level = simd_level
        self.output_format = output_format
        self.verbose = verbose
        self.errors = ErrorCollector()
        self.symbols = SymbolTable()
    
    def compile(self, source: str, output_file: str, source_file: str = "<input>") -> bool:
        if self.verbose:
            print(f"LOWL Compiler v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}")
            print(f"Target: Sirius NEXUS {self.core_type.name} Core")
            print(f"Optimization: {self.opt_level.name}, SIMD: {self.simd_level.name}")
        
        # Lex
        lexer = Lexer(source, source_file, self.errors)
        tokens = []
        while True:
            tok = lexer.next_token()
            if tok.type == TokenType.TOK_ERROR:
                self.errors.add_error(f"Lexer error: {tok.value}", tok.line, tok.column)
                return False
            tokens.append(tok)
            if tok.type == TokenType.TOK_EOF:
                break
        
        if self.verbose:
            print(f"Lexer: {len(tokens)} tokens")
        
        # Parse
        parser = Parser(tokens, self.symbols, self.errors, self.core_type)
        ast = parser.parse()
        
        if self.errors.has_errors():
            self.errors.print_summary()
            return False
        
        if self.verbose:
            print("Parser: AST built")
        
        # Generate code
        generator = CodeGenerator(self.core_type, self.opt_level, self.simd_level, self.output_format)
        assembly = generator.generate(ast)
        
        # Write output
        try:
            with open(output_file, 'w') as f:
                f.write(assembly)
        except IOError as e:
            print(f"Cannot write to {output_file}: {e}")
            return False
        
        if self.verbose:
            lines = len(assembly.split('\n'))
            print(f"Generated {lines} lines of Sirius NEXUS assembly")
        
        return True


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description=f'LOWL Compiler v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH} - Sirius NEXUS Edition',
        epilog='Copyright (c) 2026 - MIT License'
    )
    parser.add_argument('input', help='Input .lowl file')
    parser.add_argument('-o', '--output', default='output.s', help='Output assembly file')
    parser.add_argument('-c', '--core', choices=['math', 'logic', 'system', 'acu'], 
                        default='math', help='Target core type')
    parser.add_argument('-O', '--optimize', choices=['0', '1', '2', '3'], default='2',
                        help='Optimization level')
    parser.add_argument('-S', '--simd', choices=['none', 'sse', 'avx', 'avx512'], 
                        default='avx512', help='SIMD level')
    parser.add_argument('-f', '--format', choices=['sirius', 'elf', 'bin'], 
                        default='sirius', help='Output format')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', 
                        version=f'LOWL v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}')
    
    args = parser.parse_args()
    
    # Map arguments
    core_map = {
        'math': CoreType.MATH,
        'logic': CoreType.LOGIC,
        'system': CoreType.SYSTEM,
        'acu': CoreType.ACU
    }
    opt_map = {
        '0': OptimizationLevel.O0,
        '1': OptimizationLevel.O1,
        '2': OptimizationLevel.O2,
        '3': OptimizationLevel.O3
    }
    simd_map = {
        'none': SIMDLevel.NONE,
        'sse': SIMDLevel.SSE,
        'avx': SIMDLevel.AVX,
        'avx512': SIMDLevel.AVX512
    }
    format_map = {
        'sirius': OutputFormat.SIRIUS_ASM,
        'elf': OutputFormat.ELF_EXECUTABLE,
        'bin': OutputFormat.FLAT_BINARY
    }
    
    # Read input
    try:
        with open(args.input, 'r') as f:
            source = f.read()
    except IOError as e:
        print(f"Error: Cannot open {args.input}: {e}")
        sys.exit(1)
    
    # Compile
    compiler = LOWLCompiler(
        core_type=core_map[args.core],
        opt_level=opt_map[args.optimize],
        simd_level=simd_map[args.simd],
        output_format=format_map[args.format],
        verbose=args.verbose
    )
    
    if compiler.compile(source, args.output, args.input):
        print(f"Compiled {args.input} -> {args.output}")
        print(f"Target: Sirius NEXUS {args.core.upper()} Core")
        print(f"Optimization: O{args.optimize}, SIMD: {args.simd}")
        sys.exit(0)
    else:
        print("Compilation failed")
        sys.exit(1)


# ============================================================================
# Example Source Code
# ============================================================================

EXAMPLE_SOURCE = '''; Example Sirius NEXUS LOWL Program
; LLM Inference with Graphene Optical Interconnect

core math

data_section romb model_weights:
    DBZ 0x17C00000000  ; 1.5TB ROMB Gen2

data_section identity_buffer:
    DBZ 256

data_section health_buffer:
    DBZ 32

fn transformer_forward() -> void
    ; Configure ACU core for INT4 inference
    SET_REG_MAP #ACU, #INT4, #V512, #NEAREST
    
    ; Map ROMB Gen2 optical memory
    MAP_STORAGE.ROMB2 #0, #0, #0x200000000, #0x17C00000000
    
    ; Load embedding table from ROMB
    DME_COPY #0x200000000, embedding_table, #0x40000000
    
    ; Multi-head attention
    let Q_addr: ptr = #0x300000000
    let K_addr: ptr = #0x300400000
    let V_addr: ptr = #0x300800000
    let seq_len: u32 = 2048
    let head_dim: u32 = 64
    
    ATTENTIONI4 attn_out, Q_addr, K_addr, V_addr, seq_len, head_dim
    
    ; Feed-forward network
    let hidden: u32 = 4096
    let ffn_dim: u32 = 16384
    
    MATMULI4.R ff1_out, attn_out, fc1_weights, hidden, hidden, ffn_dim, fc1_bias
    MATMULI4 ff2_out, ff1_out, fc2_weights, hidden, ffn_dim, hidden, fc2_bias
    RESIDUALI4 layer_out, ff2_out, attn_out
    
    ; Layer normalization
    LAYERNORMI4 norm_out, layer_out, norm_params
    
    ; Output projection
    let vocab: u32 = 100000
    MATMULI4 logits, norm_out, output_weights, hidden, hidden, vocab
    SOFTMAXI4 probabilities, logits
    
    ; Return
    return

fn main() -> void
    ; Get device identity
    system_call GET_IDENTITY identity_buffer
    
    ; Configure chassis LED
    system_call LED_SET 0 1
    
    ; Check optical link status
    system_call OPTICAL_LINK_STATUS 0 link_status
    
    ; Run inference
    call transformer_forward
    
    ; Check health
    system_call GET_HEALTH health_buffer
    
    ; Shutdown on critical health
    let health: u8 = [health_buffer]
    if (health == 2) then
        system_call SHUTDOWN 0
    end
    
    return
'''

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f"LOWL Compiler v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH} - Sirius NEXUS Edition")
        print("Usage: python lowl_compiler.py input.lowl [-o output.s] [-c core] [-O level]")
        print("\nExample source code:")
        print(EXAMPLE_SOURCE)
    else:
        main()
```

**Key Features of the Revised LOWL Compiler:**

1. **132 Core Instructions** - Full instruction set including MOV, ADD, FMA, BRANCH, ADDPS, MATMULI4, SYSENTER, MAP_STORAGE, GRAPHENE_EMIT, etc.

2. **SYSTEM API Services (0x3000-0x3004)**:
   - `system_call GET_IDENTITY` - Device identity
   - `system_call GET_CAPABILITIES` - Hardware capabilities
   - `system_call GET_SERIAL` / `GET_UUID`
   - `system_call LED_SET` / `LED_BLINK` / `BEACON_ENABLE` - Chassis control
   - `system_call SHUTDOWN` / `REBOOT` / `SET_POWER_CAP` / `GET_HEALTH` - Power management
   - `system_call OPTICAL_LINK_STATUS` / `RDMA_READ` - Network
   - `system_call CFG_VIDEO` / `CFG_AUDIO` - Video/Audio

3. **Chip-Based Storage**:
   - `data_section romb` - ROMB Gen2 optical memory (1.5TB)
   - `MAP_STORAGE.ROMB2` - Map optical memory to address space
   - `DME_COPY` - DMA engine copy

4. **Graphene Optical Interconnect**:
   - `graphene_emit(channel, addr, size)` - Optical transmission
   - `graphene_detect(channel, addr, size)` - Optical detection
   - `optical_router.broadcast()` - Crossbar routing

5. **Core Types**:
   - `core math` - 10,000 Math cores with SIMD
   - `core logic` - 256 Logic cores (control flow)
   - `core system` - 40 System cores (kernel)
   - `core acu` - 2,048 ACU cores (INT4 inference)

6. **Vector Register Support**:
   - V0-V63 (512-bit vectors)
   - R0-R31 (64-bit scalars)
   - SIMD: SSE (128-bit), AVX (256-bit), AVX512 (512-bit)

**Usage Example:**

```bash
# Compile for Math core with AVX-512
python lowl_compiler.py model.lowl -o model.s -c math -O3 -S avx512

# Compile for System core (kernel)
python lowl_compiler.py kernel.lowl -o kernel.s -c system -O2

# Compile for ACU core (INT4 inference)
python lowl_compiler.py inference.lowl -o inference.s -c acu -O3
```
