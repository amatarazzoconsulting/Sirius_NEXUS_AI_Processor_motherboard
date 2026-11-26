# Gen6 Memory, Tensor and AI Compute Design

## 1. Memory hierarchy

| Tier | Proposed role | Latency/bandwidth treatment |
|---|---|---|
| Register files | Immediate operands | Per-pipeline implementation |
| L1/L2 SRAM | Tile-local reuse | Characterize in RTL and synthesis |
| Shared SRAM | Cross-tile staging, KV metadata | 512 MB aggregate target is aspirational |
| HBM | Weights, active tensors, KV pages | 8 TB/s proposed sustained target |
| Host DRAM | Oversubscription and staging | PCIe/CXL or platform-specific |
| NVMe | Checkpoints, model library, datasets | Storage; never model as HBM |

The 512 MB SRAM target is large and expensive. Treat it as an aggregate distributed SRAM budget, not a single monolithic cache. Validate area, porting, banking, wire delay, leakage and yield before freezing it.

## 2. HBM bandwidth sizing

For \(N\) stacks, effective data rate per pin \(r\), and data width \(w\):

\[
BW_{raw} = N \times r \times w / 8
\]

The usable bandwidth is:

\[
BW_{usable} = BW_{raw} \times efficiency
\]

The 8 TB/s Gen6 target must be backed by a concrete HBM generation, number of stacks, stack interface width, pin rate, controller count and sustained efficiency. The simulator currently treats 8 TB/s as an already-sustained bandwidth input.

## 3. Tensor engines

Implement dedicated matrix engines supporting:
- FP16 and BF16.
- FP8 with explicit E4M3/E5M2 semantics.
- INT8.
- INT4 with defined packing and accumulation.
- Wider accumulators where required.
- Explicit rounding, saturation, NaN and denormal behavior.

Peak throughput must be derived from:
- Number of MAC units.
- Operations per MAC (usually two FLOPs per multiply-accumulate).
- Clock frequency.
- Number of operations issued per cycle.
- Utilization and pipeline stalls.

Do not infer peak throughput from vector width alone.

## 4. Attention engine

Recommended operations:
- Fused scaled dot-product attention.
- Online softmax.
- Blocked/tiled attention.
- RoPE.
- Reduction and normalization support.
- KV cache read/write and page management.

Correctness requirements:
- Match reference outputs within declared tolerances.
- Handle causal and non-causal masks.
- Handle variable sequence lengths and padding.
- Avoid race conditions on shared cache pages.
- Validate long-context numerical stability.

## 5. KV cache

Provide:
- Page-based allocation.
- Per-layer metadata.
- Optional INT8/INT4 cache quantization with quality validation.
- Eviction and prefetch policy.
- Multi-tenant isolation.
- Telemetry for hit rate, fragmentation and bytes moved.

KV cache traffic depends on sequence length, head count, head dimension, precision and batching. The simple roofline simulator does not yet model this traffic; results are therefore optimistic.

## 6. Workload performance model

For a dense \(P\)-parameter model at batch size \(b\), approximate weight traffic per generated token across the batch as \(P \times q\), where \(q\) is bytes per parameter. With ideal weight reuse across the batch:

\[
T_{memory,total} \le \frac{BW_{HBM} \times b}{Pq}
\]

This gives aggregate tokens/s, not per-user tokens/s. It is a simplified upper bound. For batch 1, it reduces to the usual weight-streaming roofline.

Approximate dense compute per token is \(2P\) operations per sequence. Aggregate compute ceiling for batch \(b\):

\[
T_{compute,total} \le \frac{PeakOps}{2P}
\]

The model takes the minimum of memory and compute ceilings. It excludes attention/KV traffic, runtime overhead, context-dependent work and communication unless modeled separately.
