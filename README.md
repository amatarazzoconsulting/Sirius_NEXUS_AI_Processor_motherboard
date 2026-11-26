# Sirius NEXUS Gen6 — Architecture, Simulation & Engineering Package

**Status:** Conceptual engineering baseline / simulation package  
**Revision:** Gen6 concept, 26 November 2026  
**Owner/project:** Sirius NEXUS AI Processor  
**Important:** This package describes a proposed design. It is not a TSMC-approved design, tape-out package, verified RTL implementation, measured silicon benchmark, or manufacturing quotation.

## What is included

- `architecture/gen6_architecture.md` — system architecture and subsystem targets.
- `architecture/optical_fabric_tsmc_coupe.md` — proposed TSMC COUPE / co-packaged optics integration.
- `architecture/memory_and_compute.md` — HBM, SRAM, tensor, attention, and KV-cache design.
- `simulation/gen6_roofline_sim.py` — reproducible bandwidth/compute/optical-fabric model.
- `simulation/assumptions.json` — all editable assumptions in machine-readable form.
- `simulation/results.csv` and `simulation/results.json` — generated simulation output.
- `benchmarks/benchmark_plan.md` — fair benchmark protocol against commercial accelerators.
- `verification/verification_plan.md` — RTL, firmware, compiler, and system verification.
- `manufacturing/manufacturing_and_risk.md` — packaging, thermal, power, supply-chain, and foundry engagement plan.
- `references/sources.md` — public technical references and evidence classification.

## Run the simulation

Requires Python 3.9+; standard library only.

```bash
python3 simulation/gen6_roofline_sim.py
```

The script writes updated CSV and JSON results in the same directory.

## Critical modeling rules

1. Local HBM bandwidth and optical fabric bandwidth are different resources. The model never adds them together.
2. TSMC COUPE is treated as an optical I/O / interconnect technology, not as a memory technology.
3. The 12.8 Tb/s optical number is a Gen6 design target informed by publicly reported TSMC roadmap discussion; it is not a confirmed product guarantee or current Sirius implementation.
4. The 8 TB/s HBM target is an engineering assumption requiring memory-stack, controller, package, power, and thermal validation.
5. All performance values are analytical estimates. No hardware was built or benchmarked.
6. Roofline estimates omit real-world effects unless explicitly modeled. Actual throughput will be lower.

## Gen6 headline targets

| Item | Gen6 target | Evidence status |
|---|---:|---|
| HBM capacity | 192 GB | Proposed |
| Sustained local HBM bandwidth | 8 TB/s | Proposed target; validate |
| Aggregate on-package SRAM | 512 MB | Proposed target; costly/area-sensitive |
| FP16 peak | 2 PFLOP/s | Proposed; requires detailed datapath definition |
| FP8 peak | 4 PFLOP/s | Proposed |
| INT8 peak | 8 POP/s | Proposed |
| Optical fabric | 12.8 Tb/s aggregate | Proposed topology target; TSMC path subject to engagement |
| Power envelope | 1,000 W | Proposed accelerator module/system envelope; not package guarantee |

These are deliberately separated from commercial reference products' published specifications.
