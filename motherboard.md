# Volume 2: Motherboard Design Specification

## Complete Physical Implementation Guide

Volume 2 provides the complete manufacturing specification for the Sirius NEXUS AI Processor blade, including substrate materials, layer stack, silicon interposer design, chiplet specifications, memory integration, optical transceivers, thermal management, power distribution, and assembly procedures. This volume is intended for TSMC manufacturing engineers, packaging specialists, and quality assurance teams. The design has been optimized for manufacturability while maintaining the performance required for 5th-generation AI computing.

The Sirius NEXUS AI Processor is available in three form factors optimized for different deployment scenarios. The desktop workstation variant measures 305mm by 305mm, conforming to the Extended ATX standard, and fits in standard full-tower computer cases with standard power supplies. This variant includes two optical transceivers for optional peer-to-peer linking, air cooling with a copper heat spreader and three 120mm fans, and storage options of 10TB, 20TB, or 100TB. The professional workstation variant measures 400mm by 350mm and includes six optical transceivers, liquid cooling with dual 360mm radiators, and storage up to 200TB. The blade server variant measures 200mm by 500mm by 40mm and includes twelve optical transceivers, liquid cooling via a rack manifold, and is designed for high-density data center deployment.

---

## Section 1: Motherboard Substrate

The motherboard substrate begins with an aluminum nitride (AlN) ceramic core measuring 1.6mm thick, selected for its thermal conductivity of 180 W/mK and coefficient of thermal expansion of 4.5 ppm/°C, closely matching the 3.5 ppm/°C of the silicon interposer. The close matching prevents mechanical stress during thermal cycling that would otherwise break connections between the substrate and interposer. The core can withstand 1000 cycles from -40°C to +125°C without failure. For desktop variants, the core measures 305mm by 305mm; for professional variants, 400mm by 350mm; for blade variants, 200mm by 500mm.

On top of the ceramic core, twelve alternating layers of copper and low-dielectric polymer are deposited using a sequential buildup process. The low-dielectric polymer has a dielectric constant of 2.8 at 10 GHz, reducing signal propagation delay compared to standard FR-4, and is applied by spin coating at 1000 RPM to achieve 10-micron thickness after spinning. Each polymer layer is cured at 200°C, and the copper layers are electroplated to 18 microns for signal layers and 35 microns for power planes. The ground plane covers the entire substrate surface, providing electromagnetic shielding for the signals above it and serving as a return path for high-frequency currents.

The layer stack from bottom to top consists of a ground plane, four signal routing layers with 10-micron traces at 10-micron spacing and 50-ohm controlled impedance, two power planes for core logic (0.8V) and memory (1.2V), four more signal layers for high-speed differential pairs with 15-micron traces and 15-micron spacing forming 100-ohm differential impedance, two more power planes for flash storage (3.3V) and I/O (1.8V), and a top layer containing solder pads for interposer attachment and NAND flash chips arranged in a 200-micron pitch grid with 100-micron diameter pads. The total thickness is approximately 1.92mm uniform to within 50 microns.

Laser-drilled vias of 50-micron diameter connect the bottom ground plane to the top pads, filled with copper by electroplating. The vias are drilled through the 1.6mm thickness using a carbon dioxide laser with 100-nanosecond pulses at 10 kHz, requiring approximately 100 pulses per hole. The buildup layers are added sequentially with each layer's vias aligned to the layer below using infrared alignment marks with 1-micron accuracy. The final structure is planarized by chemical mechanical polishing to ensure a flat surface for interposer attachment, with a flatness specification of 25 microns across the entire 150mm by 150mm interposer area.

---

## Section 2: Silicon Interposer

The silicon interposer measures 150mm by 150mm and is manufactured on a 65nm CMOS process with nine layers of copper interconnect. The interposer contains no active transistors, only the passives, waveguides, and through-silicon vias that connect the chiplets to each other and to the substrate below. The 200-micron thick silicon wafer serves as the mechanical substrate, with deep reactive ion etching creating 10-micron diameter holes through the wafer at 50-micron pitch. These holes are lined with a 0.5-micron layer of silicon dioxide for insulation, then filled with copper using electroplating to form the through-silicon vias.

On the front side of the wafer, the redistribution layer is constructed with nine metal layers separated by silicon dioxide dielectric. The bottom metal layer M1 is a ground plane providing shielding for the signals above. M2 through M5 are signal routing layers with 1-micron wide traces at 1-micron pitch carrying signals between chiplets at speeds up to 10.4 gigatransfers per second. M6 and M7 are power distribution layers carrying core logic voltage (0.8V) and memory voltage (1.2V), patterned with a mesh that provides 90 percent metal coverage and 5 milliohms per square sheet resistance.

M8 is an additional signal layer for the most critical high-speed signals including optical transceiver links and the memory interface, using 0.5-micron wide traces with 0.5-micron spacing to achieve the required density. M9 is the top metal layer containing the bonding pads for chiplet attachment, arranged in a 9-micron pitch grid with 5-micron diameter pads recessed 1 micron below the surface and surrounded by a ring of copper for mechanical support. The back side of the interposer contains pads for attachment to the substrate, 50 microns in diameter at 100-micron pitch, with through-silicon vias connecting the back side pads to the redistribution layer.

The interposer also contains optical waveguides for communication between distant chiplets, fabricated in the silicon dioxide layers using a silicon nitride core with refractive index 2.0 surrounded by silicon dioxide cladding with refractive index 1.45. The waveguides are 0.5 microns wide and support a single optical mode at 850 nanometers wavelength, with a loss of 2 decibels per centimeter. Vertical couplers using gratings etched into the waveguide scatter light upward toward photodetectors or downward toward lasers, with coupling efficiency of 70 percent for input couplers and 80 percent for output couplers.

---

## Section 3: Core Chiplets

The Math core chiplet measures 2mm by 2mm and contains 32 Math cores, each with 16 ALUs, 64 vector registers of 512 bits each, and 512KB of L1 cache. The chiplet contains 1 billion transistors manufactured on TSMC's N3E 3nm process, with 32 cores arranged in an 8x4 grid on 260-micron pitch. Each Math core can execute 2, 4, or 8 operations per cycle depending on configuration, with the 4-operation (quad-issue) configuration used in the standard blade. The chiplet is attached to the interposer using hybrid bonding with 9-micron pitch connections, with bonding pads recessed 1 micron below the chiplet surface.

The Logic core chiplet measures 1.5mm by 1.5mm and contains 32 Logic cores, each with 8 ALUs optimized for integer operations, 32 scalar registers of 64 bits each, and 256KB of L1 cache. The chiplet contains 500 million transistors manufactured on TSMC's N3E 3nm process, with 32 cores arranged in a 4x8 grid. The Logic core uses a 10-stage pipeline to achieve 2.5 GHz clock speed, with a branch predictor combining bimodal, global history, and loop predictors achieving 95 percent accuracy for integer workloads.

The System core chiplet measures 2mm by 2.5mm and contains 20 System cores, each with 4 high-performance ALUs, 64 scalar registers of 64 bits each, and 512KB of L1 cache. The chiplet contains 1.2 billion transistors manufactured on TSMC's N3E 3nm process, with 20 cores arranged in a 5x4 grid. The System core uses a 15-stage pipeline to achieve 4 GHz clock speed, with a 2,048-entry microcode ROM for complex system instructions like SYSENTER and SYSEXIT.

The Approximate Compute Unit (ACU) chiplet measures 2mm by 2mm and contains 256 ACU cores, each with 8 approximate ALUs that skip carry propagation for multiplication. The chiplet contains 800 million transistors manufactured on TSMC's N3E 3nm process, with 256 cores arranged in a 16x16 grid. The ACU implements four approximation modes: Exact (0% error, 1x speed), Approx-1 (0.1% error, 2x speed), Approx-2 (1% error, 4x speed), and Approx-3 (5% error, 8x speed). The ACU is used for inference workloads where small accuracy losses are acceptable.

---

## Section 4: Memory Integration

The HBM3e memory stacks provide the main memory for the Sirius NEXUS processor, with eight stacks attached to the interposer around the perimeter of the core complex. Each stack contains eight DRAM dies vertically interconnected with through-silicon vias, plus a base logic die containing the memory controller and 32 helper cores. The stack measures 10mm by 8mm and is 720 microns tall, with total capacity 64 GB and total bandwidth 4 TB/s. The helper cores run at 1 GHz and handle error correction, refresh management, and address translation for memory-mapped I/O.

The ROMB Gen2 stack provides optical read-only memory, measuring 100mm by 100mm by 0.8mm and containing 1.5 TB of storage. The stack uses optical waveguides written by femtosecond laser in glass, with 0.95 ns access latency and 3.2 TB/s bandwidth. The ROMB Gen2 stack is attached to the substrate next to the interposer and is accessed via the same memory-mapped interface as DRAM. The stack consumes 5 watts when active and 0 watts when idle, with no refresh required.

The NAND flash chips are soldered directly to the motherboard substrate, providing 100 TB of memory-mapped storage. The 100TB configuration uses eighty 1.28TB chips arranged on both sides of the substrate, with 40 chips on each side. Each flash chip connects to the PIP-Fabric through dedicated lanes in the substrate, with read latency of 50 microseconds and write latency of 500 microseconds. The flash chips are attached using reflow soldering with lead-free tin-silver-copper alloy.

The memory hierarchy from fastest to slowest is: registers (0.5 ns), L1 cache (1 ns), L2 cache (4 ns), L3 cache (15 ns), ROMB Gen2 (0.95 ns), HBM3e DRAM (100 ns), and NAND flash (50 μs). The ROMB Gen2 is faster than DRAM despite being non-volatile, making it ideal for storing AI model weights and frequently accessed read-only data. The effective capacity with compression is 12 TB for ROMB Gen2 (8:1 compression ratio) and 800 TB for NAND flash (8:1 compression ratio).

---

## Section 5: Optical Interconnects

The Sirius NEXUS blade includes 12 optical transceivers mounted along the rear edge, each operating at 800 Gb/s over a single fiber using coarse wavelength-division multiplexing with four wavelengths (1270, 1290, 1310, and 1330 nanometers). The transceivers are silicon photonic integrated circuits manufactured on TSMC's 130nm photonic process, with micro-ring modulators for transmission and germanium photodetectors for reception. The laser source is external, mounted on the substrate next to the photonic chip.

The optical backplane in the rack chassis contains embedded waveguides that route signals between blades without active components. The backplane has 20 slots for blades, with each slot having 12 optical connectors that mate with the blade's transceivers. The waveguides are fabricated from polymer materials with a loss of 0.5 decibels per meter, with a maximum length of 1 meter within the rack. For inter-rack connections, active optical switches with 256 ports provide routing between racks with 1 microsecond of latency.

The optical fabric is cache-coherent, with directory-based coherence using wavelength-division multiplexing for broadcast messages. The directory is distributed across all blades using a hash of the memory address, with each blade tracking the location of pages for which it is the home. Coherence messages are sent over dedicated wavelengths, with the directory cache on each blade tracking up to 1 million cache lines locally and 64,000 remote cache lines.

The optical interconnect bandwidth per blade is 12 transceivers × 800 Gb/s = 9.6 Tb/s, enough to saturate the memory bandwidth of the blade. The latency for a remote access within the same rack is 5 microseconds, and for a remote access across racks is 10 microseconds. The system supports up to 256 racks (5,120 blades) in a single coherent shared memory space.

---

## Section 6: Thermal Management

The thermal encasement consists of two layers of pyrolytic graphite sheet (for general-purpose blades) or one layer (for inference-optimized blades), each 0.5mm thick with thermal conductivity of 1,500 W/mK in the plane of the sheet. The graphite sheets are applied by vacuum lamination using thermally conductive adhesive with 10 W/mK conductivity. A thermally conductive gap filler (silicone with ceramic particles, 5 W/mK) is applied to the tops of the chiplets before the graphite sheet is placed, compressing to 50 microns to accommodate height variations.

For desktop variants, a copper heat spreader with 10mm fins is attached to the graphite sheet, with three 120mm fans providing airflow across the fins. The desktop variant can dissipate 600 watts with fan speeds from 500 to 3,000 RPM, producing 20-45 dB of noise. For professional variants, liquid cooling with dual 360mm radiators and a pump dissipates 1,000 watts with fan speeds from 400 to 2,000 RPM, producing 15-35 dB of noise.

For blade variants, a liquid cold plate made of copper with internal channels contacts the thermal encasement. The cold plate measures 200mm by 500mm by 10mm, with internal channels 2mm wide and 2mm deep arranged in a serpentine pattern. The cooling liquid is deionized water with corrosion inhibitor, flowing at 1 liter per minute per blade, removing up to 700 watts with a temperature rise of 10°C. The rack manifold supplies water at 20°C and returns at 30°C, with a facility chiller removing the heat.

The thermal encasement is designed for a 10-year lifetime with continuous operation. The pyrolytic graphite sheets can be replaced in the field if damaged. The temperature sensors distributed across the blade monitor the temperature of each chiplet, with the System cores throttling the clock frequency if the temperature exceeds 85°C.

---

## Section 7: Power Distribution

The power distribution network uses twelve copper planes embedded in the motherboard substrate, with four planes for core logic (0.8V), four for memory (1.2V), two for I/O (1.8V), and two for flash (3.3V). The planes are 35 microns thick and perforated with thermal vias at 500-micron pitch, with the perforations occupying 20 percent of the plane area. The total decoupling capacitance on the blade is 20 millifarads, consisting of 10 millifarads from motherboard capacitors, 100 microfarads from interposer capacitors, and the remainder from on-die capacitance on the chiplets.

The DC-DC converter is a multi-phase synchronous buck converter with 16 phases for the general-purpose blade and 8 phases for the inference-optimized blade. The converter operates at a switching frequency of 1 MHz, with input from a 48V rack bus or 12V desktop power supply. The converter efficiency is 95 percent for the general-purpose blade and 96 percent for the inference-optimized blade.

The edge connector on the blade has 200 gold-plated contacts, each rated for 5 amperes. The 700 amperes of core logic current for the general-purpose blade requires 140 contacts, with the remaining 60 contacts used for other voltages and ground. The inference-optimized blade requires 200 amperes for core logic, using 40 contacts.

The power distribution network is simulated using a finite-element electromagnetic solver to verify that the IR drop from the edge connector to the farthest chiplet is less than 50 millivolts. The impedance of the network is less than 1 milliohm up to 10 MHz and less than 10 milliohms up to 100 MHz, with a voltage droop of 50 millivolts for a 100-ampere step with 1 nanosecond rise time.

---

## Section 8: Assembly Process

The hybrid bonding assembly process attaches the chiplets to the interposer with 9-micron pitch connections. The chiplets are prepared with 5-micron diameter bonding pads recessed 1 micron below the surface, with a layer of silicon dioxide polished to 1 nanometer flatness. The interposer is prepared similarly, and the wafers are aligned using a wafer-to-wafer bonder with 0.5-micron accuracy. The wafers are brought into contact, where silicon dioxide surfaces bond through hydrogen bonding, then annealed at 400°C for one hour to form copper-to-copper diffusion bonds.

The HBM3e stacks are attached to the interposer using thermal compression bonding with 20-micron pitch solder bumps, at 350°C with 20 Newtons of force per stack, taking 10 seconds per stack. The NAND flash chips are attached to the substrate using reflow soldering with lead-free tin-silver-copper alloy, at 260°C for 60 seconds. The optical transceivers are attached using flip-chip bonding with 50-micron pitch solder bumps, at 260°C with 10 Newtons of force per transceiver, taking 10 seconds per transceiver.

The underfill material (epoxy) is injected under the chiplets and cured at 150°C for one hour to strengthen the bonds and protect from moisture. The thermal encasement is applied by vacuum lamination, with the pyrolytic graphite sheets laminated using thermally conductive adhesive at 150°C for 30 minutes. The cold plate or heat spreader is attached using spring-loaded clamps with 10 pounds per square inch of pressure.

The assembly yield target is 80 percent for the general-purpose blade and 90 percent for the inference-optimized blade. The lower yield for the general-purpose blade is due to the higher number of chiplets (1,296 vs 1,168) and higher power dissipation (700W vs 200W). Defective chiplets can be disabled and replaced using the redundancy built into the design, with each chiplet having 10 percent spare pads that can replace defective pads.

---

## Section 9: Testing

The power-on self-test runs every time the blade is powered on, taking approximately 2.5 minutes to complete. The test includes clock test (all PLLs locked), voltage test (all voltages within tolerance), temperature test (all sensors below 85°C), memory test (64GB HBM3e), flash test (100TB NAND), optical transceiver test (12 transceivers at speed), interconnect test (all cores to all cores), built-in self-test of Math cores (10 milliseconds), built-in self-test of Logic cores (5 milliseconds), built-in self-test of System cores (10 milliseconds), crossbar test, and directory test.

The built-in self-test is a more comprehensive test performed during manufacturing, taking one hour to complete. The built-in self-test includes a thermal stress test cycling from -40°C to 125°C for 10 hours, a voltage stress test varying core voltage from 0.6V to 1.0V for one hour, and a frequency stress test varying core frequency from 1 GHz to 3 GHz for one hour. The built-in self-test detects 99 percent of manufacturing defects.

The manufacturing test flow includes incoming inspection of substrates (90% coverage), solder paste inspection (99% coverage), automated optical inspection before reflow (98% coverage), automated optical inspection after reflow (99% coverage), X-ray inspection (95% coverage), in-circuit test (90% coverage), boundary scan test (99% coverage), built-in self-test of chiplets (95% coverage), memory built-in self-test of HBM3e (99% coverage), flash test (90% coverage), optical transceiver test (99% coverage), system test (95% coverage), and burn-in (24 hours at 125°C). The overall fault coverage is 95 percent.

---

## Section 10: Blade Configurations

The general-purpose blade (high-throughput) contains 1,000 Math-4 chiplets (32 cores each, 4 ops/cycle, 2W each), 256 Logic-4 chiplets (32 cores each, 1W each), 40 System-4 chiplets (20 cores each, 8W each), and no ACU chiplets. Total cores: 32,000 Math + 8,192 Logic + 800 System = 40,992 cores. Peak FP32 performance: 20 TFLOPS. Peak INT4 performance: 320 TOPS. Memory: 64GB HBM3e + 100TB NAND + 1.5TB ROMB Gen2. Power: 700W. Cooling: Liquid. Price: $50,000.

The inference-optimized blade contains 1,000 Math-2 INT4 chiplets (64 cores each, 2 ops/cycle, 0.5W each), 256 Logic-2 chiplets (64 cores each, 0.5W each), 40 System-2 chiplets (80 cores each, 2W each), and 256 ACU chiplets (256 cores each, 0.5W each). Total cores: 64,000 Math + 16,384 Logic + 3,200 System + 65,536 ACU = 149,120 cores. Peak INT4 performance: 32,768 TOPS (32.8 POPS). Memory: 64GB HBM2e + 200TB NAND + 1.5TB ROMB Gen2. Power: 200W. Cooling: Air (rack). Price: $40,000.

The balanced blade contains 512 Math-8 chiplets (16 cores each, 8 ops/cycle, 4W each), 128 Logic-8 chiplets (16 cores each, 2W each), 20 System-8 chiplets (20 cores each, 8W each), and 256 ACU chiplets (256 cores each, 0.5W each). Total cores: 8,192 Math + 2,048 Logic + 400 System + 65,536 ACU = 76,176 cores. Peak INT4 performance: 32,768 TOPS. Memory: 64GB HBM3e + 100TB NAND + 1.5TB ROMB Gen2. Power: 400W. Cooling: Liquid. Price: $45,000.

---
