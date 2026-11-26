# Sirius NEXUS Gen6 — System Architecture

## 1. Design intent

Gen6 evolves Sirius NEXUS from a broad unified-compute concept into a measurable heterogeneous AI accelerator. It retains general-purpose control and programmable vector execution while adding dedicated tensor engines, explicit memory hierarchy, high-bandwidth HBM, and an optical scale-up fabric.

The key design principle is **move data only as far as necessary**:
- Keep hot operands and metadata in SRAM.
- Keep active model weights and tensors in HBM.
- Keep cold models, datasets, and checkpoints in NVMe/storage.
- Use electrical links for short, dense intra-package connections where they are efficient.
- Use optical links for high-bandwidth package-to-package and board/rack scale-up traffic.

## 2. Proposed block-level organization

1. **Control complex**
   - Boot/security processors.
   - Command processor and workload scheduler.
   - Interrupt, telemetry, power and thermal management.
   - Memory protection and virtual address translation.

2. **Tensor compute complex**
   - Matrix engines for FP16, BF16, FP8, INT8 and INT4.
   - Accumulation modes with defined saturation and rounding.
   - Sparse execution only when sparsity metadata and numerical semantics are explicit.
   - Per-engine local operand SRAM and DMA.

3. **Vector and scalar complex**
   - General-purpose vector ALUs for normalization, activation, reductions, indexing and custom operators.
   - Scalar/control cores for branching, runtime services and irregular workloads.
   - This complex complements tensor engines; it is not expected to replace them for dense matrix multiplication.

4. **Attention and sequence complex**
   - Fused attention datapaths.
   - Online softmax and reduction support.
   - RoPE and common positional encoding operations.
   - KV-cache allocation, paging, quantization and eviction assistance.
   - Exact supported algorithms and numerical tolerances must be specified in RTL and compiler contracts.

5. **Memory complex**
   - HBM stacks and independent memory controllers.
   - Large shared SRAM target distributed across compute tiles.
   - Coherent or explicitly managed chiplet address spaces.
   - ECC, poison propagation, page retirement, scrubbing and telemetry.
   - NVMe remains storage, not a low-latency memory tier.

6. **Optical I/O complex**
   - Electrical-to-optical and optical-to-electrical control.
   - Silicon photonics engine(s) based on a TSMC COUPE integration path, subject to foundry/customer access and qualification.
   - Fiber attach units, laser strategy, wavelength/channel plan and optical monitoring.
   - Optical links serve scale-up traffic; they do not replace local HBM interfaces.

## 3. Gen6 target specification

| Subsystem | Proposed target | Validation required |
|---|---:|---|
| HBM capacity | 192 GB | Stack count, package footprint, yield, memory vendor |
| Local HBM bandwidth | 8 TB/s | HBM generation, stack count, pin rate, controller efficiency |
| SRAM | 512 MB aggregate | Macro area, banking, ports, leakage and yield |
| FP16 peak | 2 PFLOP/s | Number of MAC units, clock, operations/MAC |
| FP8 peak | 4 PFLOP/s | FP8 format, accumulation precision, throughput |
| INT8 peak | 8 POP/s | Signedness, accumulation width, saturation |
| Optical fabric | 12.8 Tb/s aggregate | Lane rate/count, directionality, FEC, topology |
| Power envelope | 1,000 W | Package/system boundary, regulator loss, optics, cooling |
| Host interface | PCIe/CXL-class concept | Exact generation, lane count and compliance |
| Scale-up | Optical multi-package fabric | Topology, routing, congestion and fault recovery |

All targets are design hypotheses, not achieved specifications.

## 4. Topology recommendation

Use a modular multi-chiplet package:
- Several compute chiplets around a central or distributed HBM interface complex.
- Local electrical links for short-distance die-to-die traffic.
- Optical engines placed at package edge, substrate or interposer according to foundry-supported integration options.
- Redundant optical paths between accelerator modules.
- Independent control plane for link training, routing, health monitoring and graceful degradation.

Avoid an architecture where all HBM traffic must cross the optical fabric. That would add conversion, routing, and protocol overhead to the most latency-sensitive data path.

## 5. Design trade-offs

### Performance
Higher HBM bandwidth improves batch-one decode only when model weights are the limiting traffic. Tensor compute, KV-cache traffic, attention, context length and kernel efficiency can become limiting factors.

### Scalability
Optical I/O improves scale-up bandwidth and potentially energy per bit over longer links. It introduces laser, coupling, thermal, packaging, test, repair and link-management complexity.

### Reliability
Use link redundancy, lane repair, CRC/FEC, ECC, optical power monitoring, temperature telemetry and failover.

### Software
A custom compiler and runtime are mandatory. Provide a supported path from PyTorch/ONNX or an equivalent graph IR to kernel scheduling, memory placement and collective communication.
