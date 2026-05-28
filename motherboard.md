# PIP CISC Unified Compute Platform
## Motherboard Design & Manufacturing Specification

**Volume 2: Physical Implementation**
**Production Version 2.0**

---


## Chapter 1: Introduction to the Unified Motherboard Architecture

The PIP CISC motherboard represents a fundamental departure from every computer motherboard that preceded it. Traditional motherboards are collections of discrete components—CPU socket, memory slots, chipset, storage connectors, expansion slots—connected by traces that create signal integrity problems, bandwidth limitations, and power delivery challenges. This design eliminates those separations entirely, integrating all functions onto a single unified substrate where every component communicates through a silicon interposer that acts as a computational fabric.

The central insight of this architecture is that the traditional separation between processor, memory controller, and I/O hub is an artifact of manufacturing limitations that no longer apply. In the 1980s and 1990s, it was impossible to integrate all these functions onto a single die because of die size limitations, yield problems, and thermal constraints. Today, advanced packaging technologies like silicon interposers, through-silicon vias, and hybrid bonding make integration not only possible but economically advantageous.

The unified motherboard measures either 305mm by 305mm for desktop workstations, 400mm by 350mm for professional workstations, or 200mm by 500mm for blade servers. These dimensions were chosen to fit standard enclosures while providing sufficient area for the core chiplets, memory stacks, and storage chips. The desktop variant fits in standard full-tower computer cases with standard power supplies, requiring no special enclosures.

The substrate is a twelve-layer ceramic structure with embedded copper power planes. Ceramic was chosen over standard FR-4 fiberglass because ceramic has a coefficient of thermal expansion that closely matches silicon, preventing mechanical stress during thermal cycling. FR-4 expands at 17 parts per million per degree Celsius, while silicon expands at 3.5 parts per million. This mismatch would cause the interposer connections to fail after a few hundred thermal cycles. Ceramic expands at 4.5 parts per million, close enough to silicon to ensure reliability.

On top of this substrate sits a silicon interposer measuring 150mm by 150mm. The interposer is manufactured on a 65nm process and contains the PIP-Fabric crossbar switch, the global address routing logic, and the directory cache for coherency tracking. The interposer contains no active transistors in the traditional sense—it has no ALUs or control logic—but it does contain 1.2 billion passive components: vias, waveguides, and routing channels that connect the chiplets to each other and to the substrate below.

The interposer is the central nervous system of the motherboard. Every communication between cores, between cores and memory, between cores and storage, and between blades passes through the interposer's crossbar. The crossbar has 128 input ports and 128 output ports, each 512 bits wide, operating at 2 GHz. The total switching capacity is 131 terabits per second, sufficient to handle the bandwidth demands of ten thousand Math cores simultaneously.

Attached to the interposer are the core chiplets. One thousand Math core chiplets are arranged in a 100x100 grid across the central region. Each Math core chiplet measures 2mm by 2mm and contains thirty-two arithmetic logic units, sixty-four vector registers of 512 bits each, and 512 kilobytes of L1 cache. The chiplets are manufactured on a 3nm process and are attached to the interposer using hybrid bonding with 9-micron pitch connections.

The Math core chiplets are arranged in a grid with 2.1mm spacing between chiplet centers, leaving 100 microns of space for the bonding pads and routing channels. The grid covers an area of 200mm by 200mm on the interposer, centered on the die. The outer edges of the interposer are reserved for the memory stacks and the System core chiplets.

The Logic core chiplets are two hundred fifty-six in number, each measuring 1.5mm by 1.5mm, arranged in a 16x16 grid to the left of the Math complex. Each Logic core chiplet contains eight arithmetic logic units optimized for branching and searching, 32 scalar registers of 64 bits each, and 256 kilobytes of L1 cache. The Logic cores handle the irregular, unpredictable parts of workloads that the Math cores handle poorly.

The System core chiplets are forty in number, each measuring 2mm by 2.5mm, arranged in an 8x5 grid to the right of the Math complex. Each System core chiplet contains four high-performance ALUs running at 4 GHz, 64 scalar registers, and 512 kilobytes of L1 cache. The System cores handle I/O, memory management, interrupt handling, and the optical fabric communication.

The HBM3e memory stacks are attached to the interposer around the perimeter of the core complex. Eight stacks are used, each containing eight DRAM dies vertically interconnected with through-silicon vias. Each stack provides 8 gigabytes of memory and 512 gigabytes per second of bandwidth. The total capacity is 64 gigabytes, and the total bandwidth is 4 terabytes per second.

The memory stacks are arranged in two rows of four stacks each. One row is placed above the Math core grid, and one row below. This placement minimizes the distance between the Math cores and the memory, reducing access latency. The distance from the center of the Math grid to the nearest memory stack is 25mm, which at the speed of light in silicon corresponds to a round-trip delay of approximately 250 picoseconds.

The NAND flash chips are soldered directly to the motherboard substrate, not to the interposer. This allows configurable storage capacity without redesigning the interposer layout. The 10TB configuration uses twenty 512GB chips arranged in two rows along the bottom edge of the board. The 20TB configuration uses forty 512GB chips. The 100TB configuration uses eighty 1.28TB chips, occupying both sides of the substrate.

The flash chips are attached to the substrate using standard reflow soldering. The chips are placed by a pick-and-place machine with 25-micron accuracy, then reflowed at 260 degrees Celsius for 60 seconds. The solder is a lead-free tin-silver-copper alloy that forms reliable connections between the chip pads and the substrate pads.

The optical transceivers are mounted along the rear edge of the blade for blade variants, or along the top edge for desktop variants. Twelve transceivers are provided, each capable of 800 gigabits per second over a single fiber. The total off-board bandwidth is 9.6 terabits per second, sufficient to connect the blade to a rack backplane or to other blades in a cluster.

The thermal encasement is a critical component that enables the motherboard to operate at full performance without throttling. Two layers of pyrolytic graphite sheet sandwich the motherboard, spreading heat uniformly across the board. The graphite has a thermal conductivity of 1500 W/mK in the plane of the sheet, ten times that of copper. A liquid cold plate contacts the encasement for blade variants, while a copper heat spreader with fins provides air cooling for desktop variants.

The power distribution network is integrated into the substrate. Twelve power planes provide the core logic voltage of 0.8 volts, the memory voltage of 1.2 volts, the I/O voltage of 1.8 volts, and the flash voltage of 3.3 volts. The power planes are 35 microns thick and are perforated with thermal vias that allow heat to flow from the interposer to the ceramic core.

The entire assembly is designed for manufacturability. Each component can be tested individually before assembly, and defective components can be replaced without discarding the entire board. The interposer includes built-in self-test circuits that can exercise every core, every memory stack, and every optical transceiver in less than one minute.

The desktop variant fits in a standard full-tower case measuring 220mm wide, 590mm tall, and 560mm deep. The case requires a 600-watt power supply with a 12-volt rail capable of delivering 50 amps. The case includes three 120mm fans for airflow across the motherboard, plus a 140mm cold plate that contacts the copper heat spreader.

The professional workstation variant requires a larger case measuring 250mm wide, 650mm tall, and 600mm deep. The case must accommodate dual power supplies delivering 1000 watts total, plus dual 360mm radiators for liquid cooling. The professional variant is intended for continuous operation at full load, such as in rendering farms or AI training clusters.

The blade variant measures 200mm wide, 500mm deep, and 40mm tall. It slides into a 19-inch rack chassis that holds up to twenty blades. The rack provides power, cooling, and optical backplane connections. The blade has no external connectors other than the optical transceivers and the power edge connector; all I/O is handled through the backplane.

The storage-only blade variant contains no Math or Logic cores. It includes only enough System cores to run the address translation and flash management logic. The entire board is populated with NAND flash chips, providing 100TB or 200TB of memory-mapped storage. The storage blade can be mixed with compute blades in the same rack, allowing independent scaling of compute and storage.

The rack chassis holds up to twenty blades in a 42U rack. The chassis includes a management board that boots first and configures the optical crossbar. The management board then powers the blades in sequence, monitoring current draw and temperature. After all blades report readiness, the management board executes RACK_UNIFY to create the global memory space.

The optical backplane is a passive structure containing embedded waveguides that route signals between blades. The backplane has no active components, which improves reliability and reduces cost. The waveguides are fabricated from polymer materials with a refractive index contrast of 0.02, providing low loss over distances up to 1 meter.

The unified architecture eliminates the concept of "local" and "remote" memory from the programmer's perspective. A load instruction does not care whether the target address is on the same blade or on a blade four racks away. The hardware directory cache tracks the location of each memory page and routes the request accordingly. The programmer sees a single, flat address space spanning the entire installation.

The performance advantages of the unified architecture are substantial. A traditional GPU cluster with 1000 nodes has 1000 separate memory spaces; moving data between nodes requires explicit communication through a network stack with latency measured in microseconds. The PIP CISC system with 1000 blades has one memory space; moving data between blades is just a load instruction with latency measured in nanoseconds.

The power efficiency of the unified architecture exceeds traditional systems by a factor of two to three. The elimination of separate controller chips removes their power consumption. The direct attachment of memory to the interposer reduces the power required to drive signals across the memory bus. The optical interconnects consume less power than copper for distances over 10 centimeters.

The reliability of the unified architecture exceeds traditional systems because there are fewer connectors, fewer solder joints, and fewer components that can fail. The interposer has no moving parts and no components that wear out. The flash storage has a limited number of write cycles, but the wear leveling algorithms in the helper cores ensure that all chips wear evenly.

The security of the unified architecture exceeds traditional systems because the capability-based protection model prevents unauthorized access to memory. A buffer overflow vulnerability cannot be exploited to access memory outside the segment because the hardware checks permissions on every access. The cryptographic signatures on capability tokens prevent forgery.

The scalability of the unified architecture is limited only by the optical fabric and the directory cache. The directory cache scales to 65,536 blades using a hashed scheme. Beyond that, the directory overflows to memory, increasing latency but maintaining correctness. The optical fabric can be extended with active optical switches, allowing up to 1,048,576 blades in a single address space.

The manufacturing of this motherboard requires TSMC's most advanced packaging technologies. The hybrid bonding process for attaching chiplets to the interposer has been demonstrated in TSMC's 3D Fabric line. The through-silicon vias in the HBM stacks are standard in TSMC's memory packaging. The optical transceivers use TSMC's silicon photonics process. No other foundry possesses all of these capabilities.

The remainder of this document provides the detailed specifications required to manufacture the motherboard. Chapter 2 describes the substrate materials and layer stack in detail. Subsequent chapters cover the design of each component, the assembly process, the test procedures, and the form factor variants. The appendices provide pinouts, timing diagrams, mechanical drawings, and test vectors.

---

## Chapter 2: Substrate Materials and Layer Stack

The motherboard substrate is the foundation upon which all other components are built. It must provide mechanical support for the interposer and the attached components, electrical connectivity between the interposer and the flash chips, power distribution to all components, and thermal conductivity to remove heat. The substrate achieves these conflicting requirements through a carefully designed stack of ceramic core, copper planes, and low-dielectric polymer layers.

The core of the substrate is manufactured from aluminum nitride (AlN), a ceramic material with exceptional thermal conductivity. AlN has a thermal conductivity of 180 W/mK, compared to 1.5 W/mK for standard FR-4 fiberglass and 400 W/mK for copper. This high thermal conductivity allows heat to flow from the interposer, through the substrate, and into the thermal encasement without creating hot spots. The AlN core also has a coefficient of thermal expansion of 4.5 ppm/°C, closely matching the 3.5 ppm/°C of the silicon interposer.

The AlN core is fabricated by hot pressing aluminum nitride powder at 1800 degrees Celsius under 50 megapascals of pressure. The resulting ceramic billet is sliced into wafers 1.6mm thick using a diamond wire saw. The wafers are lapped to a flatness of 10 microns and polished to a surface roughness of 0.5 microns. The edges are chamfered to prevent chipping during handling.

The desktop variant of the substrate measures 305mm by 305mm, the professional variant 400mm by 350mm, and the blade variant 200mm by 500mm. All variants use the same 1.6mm core thickness and the same twelve-layer buildup structure. The differences are only in the outer dimensions and the number of components placed.

The first step in substrate fabrication is drilling the laser vias through the AlN core. A carbon dioxide laser drills holes of 50 microns diameter at locations determined by the design database. The laser fires 100 nanosecond pulses with a repetition rate of 10 kHz, drilling through the 1.6mm thickness in 100 pulses per hole. A typical desktop substrate requires 100,000 laser vias, taking 10 seconds to drill all holes.

The laser-drilled vias are cleaned in a plasma etcher to remove debris from the drilling process. The plasma etcher uses oxygen and argon gases at 200 millitorr pressure and 500 watts of RF power. The plasma removes 1 micron of material from the via walls, ensuring a clean surface for subsequent metallization. The cleaning process takes 5 minutes per batch of 10 substrates.

The vias are then metallized with copper using electroless plating. The substrates are immersed in a palladium catalyst solution that nucleates copper deposition on the via walls. They are then transferred to an electroless copper bath containing copper sulfate, formaldehyde, and sodium hydroxide at 50 degrees Celsius. Copper deposits at a rate of 1 micron per hour until a 5-micron thick layer covers the via walls.

After electroless plating, the vias are filled with copper by electroplating. The substrates are mounted in a plating fixture that contacts the seed layer on both sides of the core. They are immersed in an acid copper sulfate bath with 50 grams per liter of copper sulfate and 200 grams per liter of sulfuric acid. A current density of 20 milliamperes per square centimeter deposits copper at 1 micron per minute until the vias are completely filled.

The filled vias are planarized by chemical mechanical polishing. The substrates are mounted on a rotating platen and pressed against a polishing pad with a slurry of alumina particles in deionized water. The polishing removes the excess copper from the surface while leaving the copper plugs flush with the AlN surface. The polishing removes 10 microns of material, leaving a surface roughness of 50 nanometers.

The buildup layers are now added to both sides of the core using a sequential process. Each buildup layer consists of a polymer dielectric deposited by spin coating, followed by copper traces patterned by photolithography and electroplating. The process is repeated twelve times, six layers on each side of the core.

The polymer dielectric is a photosensitive polyimide with a dielectric constant of 2.8 at 10 GHz. The polyimide is dissolved in a solvent at 30 percent solids and spin coated onto the substrate at 1000 RPM. The resulting film is 10 microns thick after spinning. The film is soft baked at 100 degrees Celsius for 2 minutes to remove the solvent.

The dielectric is exposed to ultraviolet light through a photomask that defines the trace pattern. The photomask is a quartz plate with chrome patterns that block the UV light. The exposure tool uses a mercury lamp with a wavelength of 365 nanometers, delivering 200 millijoules per square centimeter to the substrate. The exposed regions become insoluble in the developer.

The unexposed regions are dissolved in a developer solution of tetramethylammonium hydroxide at 0.26 normal concentration. The development takes 60 seconds and leaves behind the patterned dielectric. The developed substrate is rinsed in deionized water and dried with nitrogen. The remaining dielectric has openings where the copper traces will be deposited.

A seed layer of titanium and copper is deposited by sputtering. The titanium layer is 50 nanometers thick and serves as an adhesion promoter. The copper layer is 200 nanometers thick and provides a conductive seed for electroplating. The sputtering is performed at 5 millitorr argon pressure with a DC power of 5 kilowatts.

The copper traces are built up by electroplating through the dielectric openings. The substrates are immersed in the same acid copper sulfate bath used for via filling. The current density is 10 milliamperes per square centimeter, depositing copper at 0.5 microns per minute. The deposition continues until the copper reaches a thickness of 18 microns for signal layers or 35 microns for power planes.

After copper deposition, the photoresist that defined the pattern is stripped in a solvent bath. The solvent is N-methylpyrrolidone heated to 80 degrees Celsius, which dissolves the resist without attacking the copper or dielectric. The stripping takes 10 minutes, followed by a rinse in deionized water.

The exposed seed layer between the copper traces is removed by flash etching. The substrate is dipped in an etchant of ammonium persulfate at 100 grams per liter for 60 seconds. The etchant removes the 200-nanometer copper seed layer without significantly attacking the 18-micron traces. The titanium seed layer is removed by a separate etch in dilute hydrofluoric acid.

The surface is planarized by chemical mechanical polishing before the next buildup layer is applied. The polishing removes the topography caused by the copper traces, leaving a flat surface for the next dielectric layer. The polishing removes 5 microns of material, enough to level the surface but not enough to expose the copper traces.

This process is repeated for each of the twelve buildup layers. The bottom side of the core receives six layers, and the top side receives six layers. The layers are built in alternating directions to maintain flatness: layer 1 on the top side, then layer 1 on the bottom side, then layer 2 on the top side, and so on.

The ground plane is the first layer on both sides of the core. The ground plane is a continuous sheet of copper with no breaks, providing electromagnetic shielding for the signals above it. The ground plane is 35 microns thick and covers the entire substrate area except for the thermal via openings. The thermal vias are 100-micron diameter holes through the ground plane that allow heat to flow to the core.

The four signal routing layers are built above the ground plane on each side. These layers contain the traces that connect the interposer to the flash chips and to the edge connectors. The traces are 10 microns wide and spaced 10 microns apart, providing a trace density of 50 traces per millimeter. The trace impedance is controlled to 50 ohms by adjusting the trace width and the dielectric thickness.

The signal layers use differential pairs for high-speed signals. A differential pair consists of two traces that carry equal and opposite signals. The receiver detects the difference between the two signals, canceling common-mode noise. The differential traces are 10 microns wide with 10 micron spacing between the pair, and 20 micron spacing between pairs. The differential impedance is 100 ohms.

The two power planes are built above the signal layers. The core logic power plane carries 0.8 volts to the interposer and the core chiplets. The memory power plane carries 1.2 volts to the HBM stacks. Both power planes are 35 microns thick and are perforated with thermal vias at 500-micron pitch. The perforations occupy 20 percent of the plane area but are arranged in a pattern that does not degrade current delivery.

The top two signal layers are built above the power planes. These layers carry the highest-speed signals: the optical transceiver links at 800 gigabits per second and the memory interface at 6.4 gigatransfers per second. The traces on these layers are 15 microns wide with 15 micron spacing, forming 100-ohm differential impedance.

The topmost layer of the substrate contains the solder pads for attaching the interposer and the flash chips. The interposer pads are 50 microns in diameter at 100-micron pitch, arranged in a 150mm by 150mm grid. There are 2.25 million interposer pads on the desktop substrate. The flash chip pads are 0.5mm in diameter at 1mm pitch, arranged in rows according to the storage configuration.

The bottommost layer of the substrate contains the pads for the edge connector on blade variants, or the pads for the power connectors and I/O ports on desktop variants. The edge connector has 200 gold-plated contacts, each 1mm wide with 2mm pitch. The power connectors have multiple pins for carrying 50 amps of current at 12 volts.

The completed substrate is inspected by automated optical inspection. A camera system with 5-micron resolution scans the entire substrate, comparing the pattern of traces and pads to the design database. Any defect larger than 10 microns is flagged for repair or rejection. The inspection takes 2 minutes per substrate.

The substrate is tested electrically for continuity and isolation. A flying probe tester uses two moving probes to contact each pad and measure resistance. The tester checks that each trace has continuity from its source to its destination, and that adjacent traces are not shorted together. The test takes 5 minutes for the desktop substrate with 2.25 million pads.

The substrate is then baked at 125 degrees Celsius for 2 hours to remove any moisture absorbed during processing. Moisture in the dielectric can cause delamination during the high-temperature soldering processes. The baked substrates are stored in a dry nitrogen cabinet until assembly.

The final substrate thickness is 1.6mm plus the buildup layers. The twelve buildup layers add 120 microns of dielectric and 200 microns of copper, for a total thickness of approximately 1.92mm. The thickness is uniform to within 50 microns across the substrate, ensuring flatness for the component attachment processes.

The coefficient of thermal expansion of the completed substrate is 4.5 ppm/°C in the plane of the board and 50 ppm/°C through the thickness. The in-plane expansion matches the silicon interposer, while the through-thickness expansion is accommodated by the compliance of the solder joints and the thermal interface material.

The thermal conductivity of the substrate is 180 W/mK in the plane of the core, but only 2 W/mK through the thickness because of the polymer dielectric layers. The thermal vias provide a low-resistance path through the thickness, with a thermal resistance of 5 degrees Celsius per watt for the entire substrate.

The electrical performance of the substrate is characterized by the propagation delay, the characteristic impedance, and the crosstalk. The propagation delay is 6 picoseconds per millimeter for the signal traces. The characteristic impedance is 50 ohms plus or minus 5 percent. The crosstalk between adjacent traces is -40 decibels at 10 GHz.

The reliability of the substrate is verified by thermal cycling from -40 to +125 degrees Celsius for 1000 cycles. After cycling, the substrates are inspected for cracks in the dielectric, delamination between layers, and opens in the traces. The acceptance criterion is zero defects after 1000 cycles.

The substrates are manufactured in lots of 100 at a time. The cycle time for a lot is 2 weeks from raw AlN wafer to finished substrate. The yield is 90 percent for the desktop substrate, 85 percent for the professional substrate, and 95 percent for the blade substrate. The lower yield for the professional substrate is due to its larger area and higher defect probability.

The cost of the substrate is dominated by the AlN core material and the photomasks. The AlN core costs $200 per substrate in volume production. The photomasks cost $50,000 per set and are reused for all substrates of the same design. The processing cost is $300 per substrate, for a total of $500 per desktop substrate in volume.

The substrate design is captured in a Gerber file format that specifies the geometry of every trace, pad, and via. The Gerber files are sent to the substrate manufacturer along with a drill file for the laser vias and a netlist for electrical test. The manufacturer uses these files to generate the photomasks and the NC programs for the drilling and plating equipment.

The substrate is the most complex component of the motherboard after the interposer. Its fabrication requires a sophisticated supply chain and tight process control. However, the substrate is also the most mature technology in the design; similar substrates are used in high-performance computing and telecommunications equipment today. The extension to larger sizes and finer pitches is within the capabilities of leading substrate manufacturers.

The substrate provides the mechanical foundation for the entire motherboard. Its flatness, thermal conductivity, and electrical performance determine the yield and reliability of the final assembly. A well-designed substrate enables the high-density interconnections required by the PIP CISC architecture while maintaining signal integrity and power delivery.

The interaction between the substrate and the interposer is critical. The interposer is attached to the substrate by 2.25 million solder joints, each 50 microns in diameter. The substrate must be flat to within 25 microns across the entire 150mm by 150mm area to ensure that all joints make contact. The coefficient of thermal expansion must match the interposer to within 1 ppm/°C to prevent joint failure during thermal cycling.

The interaction between the substrate and the flash chips is also important. The flash chips are attached by 0.5mm solder balls that are more compliant than the interposer joints. The substrate can have a flatness of 100 microns in the flash chip areas without affecting reliability. The coefficient of thermal expansion mismatch between the silicon flash chips and the AlN substrate is 1 ppm/°C, which is acceptable for the 500-micron solder balls.

The power delivery network is integrated into the substrate. The 0.8-volt core logic power plane must deliver 500 amps of current to the interposer with an IR drop of less than 50 millivolts. The power plane has a resistance of 0.1 milliohms per square, so the IR drop from the edge of the plane to the center is 25 millivolts at full current. The remaining 25 millivolts of budget is allocated to the interposer and the chiplet power distribution.

The decoupling capacitors are mounted on the substrate near the interposer. One hundred capacitors of 10 microfarads each are placed around the perimeter of the interposer to filter high-frequency noise. Another 100 capacitors of 100 microfarads each are placed on the back side of the substrate for bulk energy storage. The total capacitance is 11 millifarads, sufficient to hold the core logic voltage stable during current transients.

The signal integrity of the substrate is verified by time-domain reflectometry. A fast edge is launched into each trace, and the reflections are measured. Any impedance discontinuity greater than 10 percent is flagged for redesign. The reflections from vias, pad transitions, and layer changes are minimized by careful design of the trace geometry.

The substrate passes a battery of qualification tests before production release. These tests include thermal cycling, humidity exposure, vibration, and mechanical shock. The substrate must survive 1000 thermal cycles without failure, 1000 hours at 85 degrees Celsius and 85 percent relative humidity without corrosion, and 10 G of vibration without opens or shorts.

The substrate is the unsung hero of the PIP CISC platform. It is invisible to the user and to the programmer, but its quality determines the reliability of the entire system. The design and manufacturing processes described in this chapter ensure that the substrate meets the demanding requirements of the PIP CISC architecture.
# Chapter 3: Silicon Interposer Design

The silicon interposer is the central nervous system of the PIP CISC motherboard. It is a 150mm by 150mm chip fabricated on a 65nm CMOS process that contains no active transistors but instead provides the passive wiring, through-silicon vias, and optical waveguides that connect the core chiplets to each other and to the substrate below. Every communication between cores, between cores and memory, and between cores and the optical fabric passes through the interposer's routing network. The interposer is manufactured on a dedicated line at TSMC's Fab 14, using a process that has been optimized for high-density passive interconnects.

The interposer begins as a 200-micron thick silicon wafer sliced from a single-crystal ingot grown by the Czochralski method. The wafers are 300mm in diameter, allowing four 150mm by 150mm interposers to be fabricated on each wafer. The silicon is p-type with a resistivity of 10 ohm-centimeters, chosen for its compatibility with the through-silicon via etching process. The wafers are lapped to a thickness uniformity of plus or minus 5 microns and polished to a surface roughness of 0.5 nanometers.

The first step in interposer fabrication is the deposition of the isolation layer. A 2-micron thick layer of silicon dioxide is grown on both sides of the wafer by thermal oxidation at 1100 degrees Celsius in a steam atmosphere. The oxide serves as an electrical insulator between the through-silicon vias and the silicon substrate. The oxide is also a stress-relief layer that prevents cracking during the via filling process.

The through-silicon vias are etched using the Bosch deep reactive ion etching process. A photoresist mask is patterned with 10-micron diameter holes at 50-micron pitch across the entire wafer. The wafer is placed in an inductively coupled plasma etcher with alternating cycles of etching and passivation. The etching cycle uses sulfur hexafluoride gas to etch silicon isotropically, while the passivation cycle uses octafluorocyclobutane to deposit a fluorocarbon polymer on the sidewalls. After 2000 cycles, the vias are 200 microns deep, reaching completely through the wafer.

The Bosch process creates vias with scalloped sidewalls caused by the alternating etch and passivation cycles. The scallops are 100 nanometers deep and 500 nanometers wide, which is acceptable for the subsequent copper filling process. The vias are cleaned in a piranha solution of sulfuric acid and hydrogen peroxide to remove the fluorocarbon polymer and any silicon debris. The cleaning is followed by a rinse in deionized water and a spin-dry cycle.

A liner of titanium nitride is deposited on the via sidewalls by atomic layer deposition. The wafer is placed in a reaction chamber at 350 degrees Celsius, and alternating pulses of tetrakis(dimethylamino)titanium and ammonia are introduced. Each pulse deposits a monolayer of titanium nitride, and 100 pulses are required to achieve a 10-nanometer thick liner. The liner serves as a diffusion barrier that prevents copper from migrating into the silicon.

A seed layer of copper is deposited on top of the titanium nitride liner by physical vapor deposition. The wafer is sputtered in an argon plasma with a copper target at 5 kilowatts of DC power. The deposition continues until a 200-nanometer thick copper layer covers all via sidewalls and the top surface of the wafer. The seed layer provides a conductive path for the electroplating current.

The vias are filled with copper by electroplating. The wafer is immersed in an acid copper sulfate bath identical to the one used for substrate via filling. A current density of 10 milliamperes per square centimeter deposits copper at 0.5 microns per minute. The deposition continues for 400 minutes, filling the 200-micron deep vias completely. The copper overburden on the wafer surface is 50 microns thick at the end of the plating process.

The overburden is removed by chemical mechanical polishing. The wafer is mounted on a rotating platen and pressed against a polishing pad with a slurry of alumina particles in an oxidizing solution. The polishing removes the 50-micron copper overburden and planarizes the surface to within 50 nanometers of flatness. The polishing stops when the silicon dioxide isolation layer is exposed, leaving the copper via plugs flush with the oxide surface.

The redistribution layers are now built on the front side of the wafer. Nine layers of copper interconnect are deposited using a dual-damascene process similar to standard CMOS back-end-of-line. Each layer consists of trenches etched in a low-k dielectric, filled with copper, and planarized by chemical mechanical polishing. The process is repeated nine times to build the complete redistribution network.

The first redistribution layer is a ground plane that provides electromagnetic shielding for the signals above it. The ground plane is a continuous sheet of copper covering the entire wafer except for the via landing pads. The copper is 1 micron thick and is deposited by electroplating into trenches etched in a 2-micron thick silicon dioxide layer. The ground plane is connected to the silicon substrate through the through-silicon vias at 1mm pitch.

The second through fifth redistribution layers are the signal routing layers. These layers contain the traces that connect the chiplet bonding pads to each other and to the through-silicon vias. The traces are 1 micron wide with 1 micron spacing, providing a trace density of 500 traces per millimeter. The trace impedance is 50 ohms for single-ended signals and 85 ohms for differential pairs.

The signal traces are routed using a grid of orthogonal channels. The horizontal channels are in the even-numbered layers, and the vertical channels are in the odd-numbered layers. This orthogonal routing minimizes crosstalk and simplifies the design automation. The traces are connected between layers by vias that are 0.5 microns in diameter at 1-micron pitch.

The sixth and seventh redistribution layers are the power distribution layers. The sixth layer carries the core logic voltage of 0.8 volts, and the seventh layer carries the memory voltage of 1.2 volts. Both layers are 5 microns thick and are patterned with a mesh that provides low resistance while allowing thermal vias to pass through. The mesh has 90 percent metal coverage, resulting in a sheet resistance of 1 milliohm per square.

The eighth redistribution layer is an additional signal layer for the most critical high-speed signals. These signals include the clock distribution network and the optical transceiver links. The traces on this layer are 0.5 microns wide with 0.5 micron spacing, achieving a trace density of 1000 traces per millimeter. The tight pitch requires extreme ultraviolet lithography for patterning.

The ninth redistribution layer is the top metal layer that contains the bonding pads for chiplet attachment. The pads are arranged in a 9-micron pitch grid, matching the pitch of the hybrid bonding connections on the chiplets. Each pad is 5 microns in diameter and is surrounded by a ring of silicon dioxide that provides mechanical support during bonding. The pads are recessed 1 micron below the surface to protect them during handling.

The bonding pads are coated with a layer of copper that is 1 micron thick, followed by a layer of nickel that is 0.3 microns thick, followed by a layer of gold that is 0.1 microns thick. The gold layer prevents oxidation and provides a low-resistance contact for the hybrid bonding process. The nickel layer serves as a diffusion barrier between the copper and the gold.

The back side of the wafer is now processed. The wafer is flipped and mounted on a temporary carrier using a heat-release adhesive. The carrier protects the front side during the back side processing. The back side of the wafer is thinned to 100 microns by grinding with a diamond wheel, then polished to remove the grinding damage. The final thickness is 100 microns plus or minus 2 microns.

The back side redistribution layer is built using the same dual-damascene process as the front side. The back side layer contains the pads for attachment to the motherboard substrate. The pads are 50 microns in diameter at 100-micron pitch, matching the substrate pads. The pads are arranged in a 150mm by 150mm grid, with a total of 2.25 million pads.

The back side pads are connected to the front side pads through the through-silicon vias. Each via connects one front side pad to one back side pad, providing a direct electrical path from the chiplets to the substrate. The via resistance is 10 milliohms, and the via capacitance is 50 femtofarads.

The optical waveguides are fabricated in the silicon dioxide layers between the redistribution layers. The waveguides are made of silicon nitride with a refractive index of 2.0, surrounded by silicon dioxide cladding with a refractive index of 1.45. The waveguides are 0.5 microns wide and 0.5 microns tall, forming a square cross-section that supports a single optical mode at 850 nanometers wavelength.

The waveguides are patterned by photolithography and etched by reactive ion etching. A photoresist mask defines the waveguide pattern, and the silicon nitride is etched in a fluorocarbon plasma. The etch produces vertical sidewalls with a roughness of 5 nanometers, which is acceptable for low-loss waveguides. The waveguide loss is 2 decibels per centimeter.

The waveguides are integrated with the redistribution layers through vertical couplers. A vertical coupler is a grating etched into the waveguide that scatters light upward toward a photodetector or downward toward a laser. The grating period is 500 nanometers, and the etch depth is 100 nanometers. The coupling efficiency is 70 percent for the input coupler and 80 percent for the output coupler.

The optical waveguides are used for high-speed communication between chiplets that are physically distant. The waveguides have a bandwidth of 100 terahertz, limited only by the dispersion of the silicon nitride material. The propagation delay in the waveguides is 5 picoseconds per millimeter, compared to 6 picoseconds per millimeter for the electrical traces. The waveguides consume no power and generate no electromagnetic interference.

The completed interposer is tested on a wafer prober before singulation. A probe card with 10,000 needles contacts the bonding pads on the front side. The tester measures the resistance of each through-silicon via, the continuity of each signal trace, and the isolation between adjacent traces. The test takes 30 seconds per interposer.

The optical waveguides are tested by coupling light from an external laser into the input grating and measuring the output power at the far end. The test uses a 850-nanometer vertical-cavity surface-emitting laser and a germanium photodetector. The insertion loss of each waveguide is measured and compared to the design value. Waveguides with loss greater than 5 decibels are flagged as defective.

The interposers are singulated by dicing the wafer with a diamond blade. The blade is 50 microns thick and rotates at 30,000 revolutions per minute. The wafer is mounted on a dicing tape that holds the die in place after cutting. The dicing process separates the wafer into four interposers, each 150mm by 150mm.

The singulated interposers are picked from the dicing tape by a vacuum collet and placed into shipping trays. The trays are designed to protect the delicate bonding pads during transport. The interposers are shipped to the assembly facility in nitrogen-purged bags to prevent oxidation of the copper pads.

The interposer is the most complex component of the PIP CISC motherboard after the core chiplets. Its fabrication requires a combination of processes not typically found in a standard CMOS line: deep silicon etching, high-aspect-ratio copper plating, and silicon nitride waveguide deposition. TSMC's integrated device manufacturing model makes this combination possible.

The design of the interposer is captured in a GDSII file that specifies the geometry of every via, trace, pad, and waveguide. The GDSII file contains 50 gigabytes of data for the 150mm by 150mm interposer. The file is sent to TSMC along with a netlist for electrical test and a mask specification for the photomasks.

The interposer masks are 13 layers of quartz with chrome patterns. The masks are written by an electron beam writer with a 50-nanometer spot size. The writing time is 2 hours per mask layer, for a total of 26 hours for the entire mask set. The masks are inspected for defects and shipped to TSMC's mask shop.

The interposer fabrication line at TSMC is dedicated to this product. The line includes a deep silicon etcher, an atomic layer deposition system, an electroplating tool, and a chemical mechanical polisher. The line operates 24 hours per day, 7 days per week, producing 1000 interposers per day. The yield is 85 percent, meaning 850 good interposers per day.

The interposer cost is dominated by the fabrication time and the mask cost. The fabrication time is 2 weeks per batch of 100 wafers (400 interposers). The mask cost is amortized over the production volume. At full production, the interposer cost is $200 per unit.

The interposer is the enabling technology for the PIP CISC architecture. Without the interposer, the 10,000 Math cores could not communicate efficiently because the distance between chiplets would be too large for electrical signals. The interposer reduces the distance between chiplets to 100 microns, allowing communication at 2 GHz with low power.

The interposer also enables the optical waveguides that connect distant regions of the chip. The waveguides have lower loss and higher bandwidth than electrical traces for distances longer than 1 millimeter. The interposer contains 1,000 waveguides, each 10 centimeters long, providing a total optical bandwidth of 100 petabits per second.

The interposer is the substrate upon which the entire PIP CISC architecture is built. Its quality determines the performance and reliability of the final product. The design and manufacturing processes described in this chapter ensure that the interposer meets the demanding requirements of the PIP CISC platform.

The interaction between the interposer and the core chiplets is critical. The chiplets are attached to the interposer by hybrid bonding, with 9-micron pitch connections. The interposer must be flat to within 100 nanometers across the bonding area to ensure that all connections make contact. The coefficient of thermal expansion must match the chiplets to within 1 part per million per degree Celsius to prevent joint failure.

The interposer also interacts with the motherboard substrate. The interposer is attached to the substrate by 2.25 million solder joints, each 50 microns in diameter. The interposer must be flat to within 25 microns across its entire area to ensure that all solder joints make contact. The coefficient of thermal expansion must match the substrate to within 0.5 parts per million per degree Celsius.

The power delivery network in the interposer must deliver 500 amps of current to the core chiplets with an IR drop of less than 50 millivolts. The power distribution layers have a resistance of 1 milliohm per square, so the IR drop from the edge of the interposer to the center is 25 millivolts at full current. The remaining 25 millivolts is allocated to the substrate and the chiplet power distribution.

The signal integrity of the interposer is verified by electromagnetic simulation. The simulation uses a finite-element method to solve Maxwell's equations for the entire interposer geometry. The simulation computes the S-parameters of every signal path and verifies that the return loss is less than -20 decibels and the insertion loss is less than -1 decibel up to 10 gigahertz.

The thermal performance of the interposer is verified by finite-element simulation. The simulation models the heat generation in the chiplets and the heat flow through the interposer and the substrate. The simulation shows that the maximum temperature rise in the interposer is 10 degrees Celsius above the substrate temperature, which is acceptable for reliability.

The reliability of the interposer is verified by accelerated life testing. Interposers are subjected to thermal cycling from -40 to +125 degrees Celsius for 1000 cycles, followed by electrical test. The interposers are also subjected to 1000 hours of operation at 125 degrees Celsius with 5 volts bias. The acceptance criterion is zero failures after these tests.

The interposer is the most advanced passive component ever manufactured for a commercial computer. It combines through-silicon vias, high-density redistribution layers, and optical waveguides on a single 150mm by 150mm die. The interposer is a testament to the capability of TSMC's manufacturing technology and the vision of the PIP CISC architecture.

The interposer design described in this chapter is ready for mask generation and pilot production. The design files have been verified by design rule checking, layout versus schematic, and electromagnetic simulation. The masks are being written, and the process tooling is being qualified. The first engineering samples are expected within six months.

The interposer is the foundation of the PIP CISC platform. Its successful manufacture is the critical path to bringing the product to market. TSMC's experience with through-silicon vias, redistribution layers, and silicon photonics makes them the ideal partner for this challenging manufacturing project.

The interposer represents a new category of semiconductor product: the passive active interposer. It is passive in that it contains no transistors, but active in that it routes signals and power between chiplets. The interposer blurs the line between packaging and silicon, enabling the dense integration that defines the PIP CISC architecture.

The future of the interposer includes the integration of active devices such as voltage regulators and optical drivers. These active components can be embedded in the interposer using TSMC's deep-trench capacitor technology and silicon photonics processes. The next generation of the interposer will include 1,000 voltage regulators, one for each Math core chiplet, providing dynamic voltage scaling at the chiplet level.

The interposer is the silent workhorse of the PIP CISC motherboard. The user never sees it, and the programmer never addresses it directly. But without the interposer, the ten thousand cores would be isolated islands unable to communicate. The interposer transforms a collection of chiplets into a unified computational fabric.

The design of the interposer was the most challenging part of the PIP CISC project. The routing of 2.25 million signals between 1,300 chiplets required new electronic design automation algorithms that could handle the scale and complexity. The development of these algorithms took three years and involved a team of 50 engineers.

The interposer routing is organized as a hierarchical grid. The top level of the hierarchy routes signals between regions of the interposer. The middle level routes signals within each region. The bottom level routes signals from the region to the individual chiplet bonding pads. The hierarchical approach reduces the routing complexity from quadratic to linear in the number of chiplets.

The interposer clock distribution is a symmetric tree that delivers the 2 GHz clock to every chiplet with less than 10 picoseconds of skew. The clock tree is implemented in the eighth redistribution layer, which has the finest pitch and the tightest impedance control. The clock tree is terminated at each chiplet by a programmable delay line that compensates for manufacturing variations.

The interposer reset distribution is a separate network that can reset individual chiplets or groups of chiplets. The reset network is implemented in the first redistribution layer, which has the coarsest pitch and the highest drive strength. The reset network can reset any chiplet in less than 1 nanosecond.

The interposer test features include a boundary scan chain that can test the connectivity between chiplets. The boundary scan chain is implemented in the second redistribution layer and is accessible through a dedicated test port. The boundary scan can detect opens and shorts in the interposer routing with 100 percent coverage.

The interposer repair features include redundant traces that can replace defective traces. The redundant traces are implemented in the third redistribution layer and are selected by antifuses that can be programmed during test. The repair can replace up to 1 percent of the traces, improving yield by 10 percentage points.

The interposer is a masterpiece of engineering and manufacturing. It pushes the limits of what is possible with silicon processing, but it stays within the capabilities that TSMC has already demonstrated in production. The interposer is the bridge between the 3nm chiplets and the 65nm substrate, between the optical waveguides and the copper traces, between the ten thousand cores and the single memory space.

This concludes Chapter 3 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Math Core Chiplet CMOS Design in similar detail, covering the arithmetic logic units, the vector register file, the L1 cache, and the mesh network that connects the cores on the chiplet.
# Chapter 4: Math Core Chiplet CMOS Design

The Math core chiplet is the computational engine of the PIP CISC platform. Each chiplet contains 32 physical Math cores, each capable of executing 512-bit vector instructions at 2 GHz. The chiplets are manufactured on TSMC's 3nm process, which provides the transistor density required to pack 32 cores into a 2mm by 2mm die. One thousand such chiplets are arranged in a 100x100 grid on the interposer, providing a total of 10,000 Math cores.

The 3nm process used for the Math core chiplet is TSMC's N3E variant, optimized for high-performance computing. The process features a contacted poly pitch of 45 nanometers and a minimum metal pitch of 28 nanometers. The transistor density is 250 million transistors per square millimeter, allowing each 2mm by 2mm chiplet to contain 1 billion transistors. The 32 Math cores share these 1 billion transistors, along with the mesh network and the chiplet-level cache.

The chiplet is designed as a tile of 32 cores arranged in an 8x4 grid. Each core occupies an area of 250 micrometers by 250 micrometers. The cores are placed on a 260-micrometer pitch, leaving 10 micrometers between cores for the routing channels. The chiplet measures 2.08mm by 1.04mm for the core array, plus 0.5mm on each side for the I/O ring, for a total die size of 3.08mm by 2.04mm. The actual die is 2mm by 2mm after trimming the I/O ring to the minimum required width.

The core is partitioned into several functional blocks. The instruction fetch unit occupies the top-left corner of the core and is responsible for fetching instructions from the L1 instruction cache. The decode unit is adjacent to the fetch unit and decodes the variable-length PIP CISC instructions into micro-operations. The rename unit follows the decode unit and renames the architectural registers to physical registers. The dispatch unit sends renamed instructions to the appropriate execution units.

The integer ALU block contains 16 parallel 32-bit ALUs that can be combined to form 8 64-bit ALUs, 4 128-bit ALUs, 2 256-bit ALUs, or 1 512-bit ALU. The ALUs are implemented as 32-bit slices that share carry chains. Each slice contains a 32-bit adder with carry-lookahead, a 32-bit multiplier with Booth encoding, a 32-bit shifter, and a 32-bit logical unit. The slices are connected by a programmable interconnect that routes carries between slices for wider operations.

The floating-point ALU block contains 16 parallel 32-bit FPUs that can be combined for wider precision. Each FPU implements single-precision operations as defined by IEEE 754. The FPUs use a 24-bit mantissa multiplier and an 8-bit exponent adder. For double-precision operations, two FPUs are combined to form a 53-bit mantissa multiplier and an 11-bit exponent adder. For the FMA instruction, the mantissa multiplier and the exponent adder are fused into a single operation.

The vector register file contains 64 registers, each 512 bits wide, for a total of 4 kilobytes of register storage. The register file is implemented as a 64x512-bit SRAM array with 10 read ports and 5 write ports. The read ports are organized into two banks: 5 ports feed the integer ALUs, and 5 ports feed the floating-point ALUs. The write ports accept results from the ALUs and from the load-store unit. The register file can sustain 10 reads and 5 writes per cycle.

The vector register file uses a multi-banked architecture to achieve the required port count. The 512-bit registers are divided into 16 32-bit banks. Each bank is a 64x32-bit SRAM with 1 read port and 1 write port. The 10 read ports are distributed across the banks, with each bank providing 1 read port to each of 10 global read buses. The 5 write ports are similarly distributed. The banked architecture reduces the area and power of the register file compared to a fully multiported design.

The L1 instruction cache is 32 kilobytes of 4-way set-associative SRAM with a 64-byte cache line. The cache is implemented as 4 banks of 8 kilobytes each. The tag array stores 20-bit tags for 1024 sets, plus 4 bits of state per tag. The data array stores 64-byte lines divided into 8 8-byte words. The cache can deliver one 512-bit instruction bundle per cycle, which contains up to 16 instructions depending on their lengths.

The L1 data cache is 32 kilobytes of 4-way set-associative SRAM with a 64-byte cache line. The cache is implemented identically to the instruction cache but with a different replacement policy. The data cache uses a write-back write-allocate policy with a pseudo-LRU replacement algorithm. The cache has 2 read ports and 1 write port, allowing one load and one store per cycle, or two loads per cycle if no store is performed.

The L1 data cache includes a store buffer that holds pending writes. The store buffer has 16 entries, each holding a 64-byte cache line. The store buffer coalesces writes to the same cache line, reducing the number of writes to the cache array. When the store buffer fills, it drains to the L1 cache, which may evict a dirty line to the L2 cache if necessary.

The load-store unit handles all memory accesses. It computes virtual addresses from the base and index registers, translates them to physical addresses using the TLB, and sends requests to the L1 data cache. The load-store unit can execute one load and one store per cycle, or two loads if no store is pending. The unit also handles misaligned accesses by splitting them into multiple aligned accesses.

The TLB has 64 entries and is fully associative. Each entry maps a 4KB virtual page to a 4KB physical page, plus 4 bits of permission. The TLB is accessed in parallel with the L1 data cache tag lookup. A TLB miss triggers a hardware walk of the segment tree, which takes up to 12 cycles. The TLB miss handler also updates the TLB with the new mapping.

The branch predictor is a 4K-entry tournament predictor. The tournament predictor combines a local predictor that tracks the history of each branch individually with a global predictor that tracks the history of all branches. The local predictor uses a 10-bit history for each branch, indexed by the branch address. The global predictor uses a 12-bit global history register that is updated after every branch. The tournament predictor selects the better predictor for each branch based on the past performance.

The branch target buffer has 256 entries and is 4-way set-associative. Each entry stores the address of a previously executed branch and the target address taken. The buffer is accessed in the fetch stage and returns the predicted target in the same cycle. The target is validated in the execute stage. A misprediction flushes the pipeline and updates the branch predictor and the branch target buffer.

The return address stack has 16 entries and is used to predict the return address for subroutine returns. The stack is pushed when a call instruction is executed and popped when a return instruction is executed. The stack is shadowed by a second stack that is used for speculative execution. The speculative stack is committed when the call is committed and rolled back when the call is mispredicted.

The instruction fetch unit fetches 32 bytes of instruction data from the L1 instruction cache each cycle. The fetch unit aligns the 32-byte block to the current instruction pointer and sends it to the decode unit. The fetch unit also includes a branch predictor that provides the next instruction pointer. The fetch unit can fetch from a new target in the cycle after a branch is predicted.

The decode unit receives 32 bytes of instruction data from the fetch unit. The decode unit scans the instruction stream to find instruction boundaries. Because the PIP CISC instruction set uses variable-length encoding, finding the boundaries requires examining the opcode and operand count fields. The decode unit can decode up to 8 instructions per cycle, but the average is 4 instructions per cycle.

The decode unit also translates the variable-length PIP CISC instructions into fixed-length micro-operations. Each micro-operation is a simple operation that can be executed by one of the ALUs. A single PIP CISC instruction may translate into 1 to 4 micro-operations. The FMA instruction translates into a single micro-operation because the hardware directly supports it. A complex instruction like HMM_FORWARD translates into many micro-operations that are stored in the microcode ROM.

The rename unit maps the architectural registers specified in the PIP CISC instruction to physical registers in the register file. The rename unit uses a register alias table that tracks the mapping of each architectural register to the most recent physical register. The rename unit renames up to 8 registers per cycle. The rename unit also detects WAW and WAR hazards and inserts the necessary dependencies.

The dispatch unit receives renamed micro-operations from the rename unit and sends them to the appropriate execution units. The dispatch unit has 5 issue ports: port 0 for integer ALUs, port 1 for floating-point ALUs, port 2 for loads, port 3 for stores, and port 4 for branches. Each issue port has a reservation station that holds pending micro-operations waiting for their operands.

The integer ALU execution units are 16 in number, organized as 2 clusters of 8 ALUs each. The ALUs are 32 bits wide but can be combined for wider operations. The integer ALUs execute addition, subtraction, multiplication, division, and logical operations. The multiplication is pipelined with a latency of 3 cycles. The division is not pipelined and has a latency of 32 cycles.

The floating-point ALU execution units are 16 in number, organized identically to the integer ALUs. The floating-point ALUs execute addition, subtraction, multiplication, division, square root, and FMA operations. The FMA operation is the most important for the Math core, and it is optimized to have a latency of 4 cycles and a throughput of 1 per cycle. The division and square root operations have latencies of 16 and 32 cycles, respectively.

The vector execution units are integrated into the ALUs. A 512-bit vector operation uses all 16 ALUs in parallel, with each ALU processing a 32-bit lane. The vector control unit distributes the vector elements to the ALUs and collects the results. The vector control unit also handles vector reductions by combining the results from the ALUs in a tree.

The load-store unit has 2 load ports and 1 store port. Each load port can load a 512-bit vector from the L1 data cache in a single cycle if the data is aligned. Misaligned loads are split into two 256-bit loads. The store port can store a 512-bit vector in a single cycle, but the store is written to the store buffer and may take multiple cycles to reach the cache.

The L2 cache is shared among all 32 cores on the chiplet. The L2 cache is 4 megabytes of 16-way set-associative SRAM with a 64-byte cache line. The cache is partitioned into 16 banks of 256 kilobytes each. The cache uses a write-back write-allocate policy with a pseudo-LRU replacement algorithm. The L2 cache has 32 read ports and 16 write ports, one for each core, but the banks are interleaved to reduce contention.

The L2 cache is connected to the cores through a mesh network. The mesh network has 8 rows and 4 columns, matching the 8x4 core grid. Each core is connected to its four neighbors through 128-bit bidirectional links. The mesh network uses wormhole switching with 5 virtual channels to avoid deadlock. The mesh operates at 2 GHz, matching the core clock speed.

The mesh network router at each core has 5 input ports and 5 output ports: north, south, east, west, and local. The router uses a deterministic X-Y routing algorithm: packets are routed first in the X direction, then in the Y direction. The router also implements flow control using credits that track available buffer space in the downstream router.

The L2 cache controller implements the MESI cache coherence protocol. Each cache line has a 2-bit coherence state. The controller listens to snoop requests from the mesh network and responds with the cache line state and data if required. The controller also initiates snoop requests when a core writes to a cache line that may be shared with other cores.

The chiplet also includes a built-in self-test controller that can test all 32 cores in parallel. The self-test controller generates test patterns for the ALUs, the register file, the caches, and the mesh network. The test patterns are applied at the full clock speed, and the results are compared to the expected values. The self-test completes in 1 second and can detect 99 percent of manufacturing defects.

The chiplet is attached to the interposer using hybrid bonding. The bonding pads are 5 microns in diameter at 9-micron pitch, arranged in a 200x200 grid around the perimeter of the chiplet. The pads are recessed 1 micron below the chiplet surface and are surrounded by a ring of copper that provides mechanical support. The bonding process uses thermal compression at 400 degrees Celsius under 50 Newtons of force.

The chiplet is manufactured on TSMC's 3nm process line at Fab 18 in Tainan. The line produces 10,000 wafers per month, each wafer containing 1,000 chiplets. The yield is 80 percent for the Math core chiplet, meaning 800 good chiplets per wafer. The chiplet cost is $10 per unit in volume production.

The Math core chiplet is the most complex of the three chiplet types. Its 1 billion transistors include 32 cores, 4 megabytes of L2 cache, and a mesh network. The chiplet operates at 2 GHz and consumes 2 watts of power, for a total of 2 kilowatts for the 1,000 chiplets on a blade.

The chiplet design is verified by simulation at the RTL, gate, and transistor levels. The RTL simulation verifies the functional correctness of the core. The gate-level simulation verifies the timing and the power consumption. The transistor-level simulation verifies the signal integrity and the noise margins. The chiplet passes all simulations before being released for manufacturing.

The chiplet is the heart of the PIP CISC platform. Its design is the result of three years of engineering effort by a team of 100 designers. The chiplet pushes the limits of what is possible with 3nm CMOS, but it stays within the design rules established by TSMC. The chiplet is ready for mask generation and pilot production.

The interaction between the Math core chiplet and the interposer is critical. The hybrid bonding pads must align with the interposer pads to within 1 micron. The thermal expansion of the chiplet and the interposer must be matched to within 1 part per million per degree Celsius. The power supply voltage must be delivered to the chiplet with less than 10 millivolts of IR drop.

The chiplet includes on-die decoupling capacitors that filter high-frequency noise on the power supply. The decoupling capacitors are implemented as metal-insulator-metal capacitors in the upper metal layers. The total capacitance on the chiplet is 100 nanofarads, enough to hold the voltage stable during current transients of 10 amps per nanosecond.

The chiplet also includes temperature sensors that monitor the die temperature. The sensors are implemented as diode-connected transistors that have a temperature-dependent voltage. The sensors are distributed across the chiplet at 1mm spacing. The temperature readings are used by the power management unit to adjust the clock frequency and the supply voltage.

The chiplet includes a power management unit that controls the clock frequency and the supply voltage of each core independently. The power management unit uses a phase-locked loop to generate the 2 GHz clock from a 100 MHz reference. The phase-locked loop has a lock time of 100 microseconds and a jitter of 5 picoseconds.

The chiplet includes a thermal management unit that monitors the temperature sensors and throttles the cores when the temperature exceeds 85 degrees Celsius. Throttling reduces the clock frequency by 50 percent until the temperature drops below 80 degrees Celsius. The thermal management unit also controls the fan speed through a dedicated output pin.

The chiplet includes a security unit that implements the cryptographic functions required for capability tokens. The security unit contains a hardware random number generator, an AES-256 engine, and an ECDSA engine. The security unit also stores the chiplet's private key, which is unique to each chiplet and is programmed during manufacturing.

The chiplet includes a test access port that conforms to the IEEE 1149.1 JTAG standard. The test access port provides access to the boundary scan chain and to the internal test registers. The test access port is used during manufacturing to test the chiplet and during system bring-up to debug the hardware.

The Math core chiplet is a marvel of modern semiconductor engineering. Its 1 billion transistors are arranged in a regular grid of 32 cores, each core a sophisticated superscalar processor. The chiplet delivers 32 gigaflops of FP32 performance at 2 watts, an efficiency of 16 gigaflops per watt. This efficiency is what makes the 10,000-core system possible within a 2 kilowatt power budget.

The future of the Math core chiplet includes integration of the L3 cache onto the chiplet. The L3 cache is currently on the interposer, but moving it to the chiplet would reduce latency and increase bandwidth. The next generation of the chiplet will include 16 megabytes of L3 cache, bringing the total cache on the chiplet to 20 megabytes. The next generation will also support 1024-bit vectors, doubling the peak performance.
# Chapter 5: Logic Core Chiplet CMOS Design

The Logic core chiplet is the branch-intensive engine of the PIP CISC platform. Unlike the Math cores that excel at vector and matrix operations, the Logic cores are optimized for irregular computations: tree traversal, hash table lookups, recursive algorithms, and decision trees. Each Logic core chiplet contains 8 physical cores, each capable of executing 128-bit scalar and SIMD instructions at 2.5 GHz. The chiplets are manufactured on TSMC's 3nm process, the same process used for the Math cores, but with different design optimizations. Two hundred fifty-six such chiplets are arranged in a 16x16 grid on the interposer, providing a total of 2,048 Logic cores.

The Logic core is a dual-issue, out-of-order processor with a 10-stage pipeline. The pipeline stages are fetch, decode, rename, dispatch, issue, register read, execute, memory access, write back, and commit. The 10-stage pipeline allows a clock speed of 2.5 GHz, 25 percent higher than the Math cores, because the Logic core does not require the wide vector datapaths that limit the Math core's maximum frequency.

The instruction fetch unit fetches 32 bytes of instruction data from the L1 instruction cache each cycle. The fetch unit includes a sophisticated branch predictor with 95 percent accuracy for integer workloads. The branch predictor combines a 4K-entry bimodal predictor, a 4K-entry global history predictor, and a 256-entry loop predictor. The loop predictor is particularly important for the Logic core because integer code often contains tight loops that the other predictors handle poorly.

The decode unit receives the 32-byte instruction block and extracts up to 4 instructions per cycle. The decode unit also performs macro-op fusion, combining common sequences of instructions into a single micro-operation. For example, a compare followed by a conditional branch is fused into a single compare-and-branch micro-operation. Macro-op fusion reduces the number of micro-operations in the pipeline and improves performance.

The rename unit maps the 32 architectural registers to 128 physical registers. The extra physical registers enable out-of-order execution by allowing the processor to speculatively execute instructions without overwriting architectural state. The rename unit can rename up to 4 registers per cycle and includes a register alias table with 32 entries and 4 read ports and 4 write ports.

The dispatch unit sends renamed micro-operations to the reservation stations. The Logic core has 3 issue ports: port 0 for ALU operations, port 1 for load-store operations, and port 2 for branch operations. Each issue port has a reservation station that holds up to 16 pending micro-operations. The reservation stations are implemented as content-addressable memories that wake up micro-operations when their operands become ready.

The integer ALU is 64 bits wide and can execute one ALU operation per cycle. The ALU contains a 64-bit adder with carry-lookahead that completes in 4 gate delays, a 64-bit shifter that can shift by any amount in 1 cycle, and a logical unit that computes AND, OR, XOR, and NOT in parallel. The ALU also contains a multiplier that produces a 64-bit product from two 32-bit operands in 2 cycles, or a 64-bit product from two 64-bit operands in 3 cycles.

The branch execution unit handles all branch instructions. The branch unit evaluates the condition using the condition flags and compares the target address to the predicted address. If the prediction was correct, the branch unit commits the branch and continues. If the prediction was incorrect, the branch unit flushes the pipeline and redirects the fetch unit to the correct target. The branch misprediction penalty is 10 cycles, which is relatively low for a 2.5 GHz processor.

The load-store unit handles all memory accesses. The load-store unit has a 32-entry load buffer and a 16-entry store buffer. The load buffer holds pending loads that are waiting for data from the cache or from memory. The store buffer holds pending stores that are waiting to be written to the cache. The load-store unit can execute one load and one store per cycle, or two loads if no store is pending.

The L1 instruction cache is 64 kilobytes of 4-way set-associative SRAM with a 64-byte cache line. The Logic core has a larger instruction cache than the Math core because integer code tends to have larger instruction footprints than vector code. The cache is implemented as 4 banks of 16 kilobytes each, with a tag array that stores 20-bit tags for 1024 sets.

The L1 data cache is 64 kilobytes of 4-way set-associative SRAM with a 64-byte cache line. The data cache uses a write-through policy because integer code often involves shared memory that must be visible to other cores immediately. The write-through policy ensures that writes are written to the L2 cache in the same cycle, making them visible to other cores.

The TLB has 128 entries and is 4-way set-associative. The larger TLB reflects the fact that integer workloads often have larger working sets than vector workloads. Each entry maps a 4KB virtual page to a 4KB physical page, plus 4 bits of permission. The TLB supports two page sizes: 4KB and 2MB. The 2MB pages are used for code and data that are accessed frequently.

The branch target buffer has 512 entries and is 4-way set-associative. The larger branch target buffer improves the prediction accuracy for indirect branches and virtual function calls. The branch target buffer is accessed in the fetch stage and returns the predicted target in the same cycle. The target is validated in the execute stage.

The return address stack has 32 entries, twice the size of the Math core's return stack. The larger return stack is needed because integer code often has deeper call stacks than vector code. The return stack is pushed when a call instruction is executed and popped when a return instruction is executed.

The L2 cache is shared among all 8 cores on the chiplet. The L2 cache is 2 megabytes of 8-way set-associative SRAM with a 64-byte cache line. The cache is partitioned into 8 banks of 256 kilobytes each. The L2 cache uses a write-back policy for lines that are not shared, and a write-through policy for lines that are shared with other cores. The cache coherence protocol is MESI, the same as the Math core.

The L2 cache is connected to the cores through a ring network. The ring network has 8 nodes, one for each core, connected in a bidirectional ring. The ring operates at 2.5 GHz, matching the core clock speed. The ring uses credit-based flow control to prevent packet loss. Each node has 2 input ports and 2 output ports, one for each direction on the ring.

The ring network uses a simple routing algorithm: packets are sent in the direction that minimizes the distance to the destination. If the distance is equal in both directions, the packet is sent clockwise. The ring has a maximum latency of 4 cycles from any core to any other core, which is sufficient for the coherence protocol.

The chiplet also includes a built-in self-test controller that can test all 8 cores in parallel. The self-test controller generates test patterns for the ALU, the cache, the TLB, and the ring network. The test patterns are applied at the full clock speed, and the results are compared to the expected values. The self-test completes in 0.5 seconds, half the time of the Math core because there are fewer cores.

The Logic core chiplet is attached to the interposer using the same hybrid bonding process as the Math core. The bonding pads are 5 microns in diameter at 9-micron pitch, arranged in a 150x150 grid around the perimeter of the chiplet. The chiplet measures 1.5mm by 1.5mm, smaller than the Math core chiplet because it contains fewer cores.

The chiplet is manufactured on TSMC's 3nm process line at Fab 18. The line produces 10,000 wafers per month, each wafer containing 2,000 chiplets. The yield is 85 percent for the Logic core chiplet, higher than the Math core because the chiplet is smaller and has fewer transistors. The chiplet cost is $5 per unit in volume production.

The Logic core chiplet consumes 0.5 watts per core, for a total of 4 watts per chiplet. The 256 chiplets on a blade consume 1 kilowatt, half the power of the Math cores. The lower power consumption is due to the lower transistor count and the simpler execution units.

The chiplet is optimized for branch-intensive workloads. A branch predictor with 95 percent accuracy means that only 5 percent of branches are mispredicted, incurring a 10-cycle penalty. The effective branch penalty is 0.5 cycles per branch, which is acceptable for most integer workloads.

The chiplet includes a hardware performance monitor that tracks the number of instructions executed, the number of cycles, the number of cache misses, the number of TLB misses, and the number of branch mispredictions. The performance monitor is accessible through the test access port and can be used to tune the software for the Logic core.

The chiplet includes a power management unit that can independently control the clock frequency and supply voltage of each core. The power management unit uses a phase-locked loop to generate the 2.5 GHz clock from a 100 MHz reference. The power management unit also includes a voltage regulator that can adjust the supply voltage from 0.6 volts to 1.0 volts in 10 millivolt steps.

The chiplet includes a temperature sensor at the center of the die. The temperature sensor is used by the power management unit to throttle the cores when the temperature exceeds 85 degrees Celsius. Throttling reduces the clock frequency by 25 percent until the temperature drops below 80 degrees Celsius.

The Logic core chiplet is the workhorse for control-intensive workloads. Its 2,048 cores handle the branching, searching, and decision-making that the Math cores cannot handle efficiently. The combination of 10,000 Math cores and 2,048 Logic cores creates a balanced system that can handle both data-parallel and control-parallel workloads.

The chiplet design is verified by simulation at the RTL, gate, and transistor levels. The RTL simulation verifies the functional correctness of the core. The gate-level simulation verifies the timing and the power consumption. The transistor-level simulation verifies the signal integrity and the noise margins. The chiplet passes all simulations before being released for manufacturing.

The interaction between the Logic core chiplet and the interposer is critical. The hybrid bonding pads must align with the interposer pads to within 1 micron. The thermal expansion of the chiplet and the interposer must be matched to within 1 part per million per degree Celsius. The power supply voltage must be delivered to the chiplet with less than 10 millivolts of IR drop.

The chiplet includes on-die decoupling capacitors that filter high-frequency noise on the power supply. The decoupling capacitors are implemented as metal-insulator-metal capacitors in the upper metal layers. The total capacitance on the chiplet is 50 nanofarads, enough to hold the voltage stable during current transients of 5 amps per nanosecond.

The chiplet includes a security unit that implements the cryptographic functions required for capability tokens. The security unit is simpler than the Math core's security unit because the Logic cores do not handle capability tokens directly. The security unit contains a hardware random number generator and an AES-128 engine.

The chiplet includes a test access port that conforms to the IEEE 1149.1 JTAG standard. The test access port provides access to the boundary scan chain and to the internal test registers. The test access port is used during manufacturing to test the chiplet and during system bring-up to debug the hardware.

The Logic core chiplet is a balanced design that prioritizes branch prediction and cache performance over raw arithmetic throughput. Its 8 cores are sufficient for the control-plane workloads that complement the Math cores. The chiplet's small size and low power consumption allow 256 chiplets to be placed on a single blade.

The future of the Logic core chiplet includes support for transactional memory, which would allow the Logic cores to execute critical sections in parallel without locks. Transactional memory is particularly useful for data structures like hash tables and trees, where fine-grained locking is difficult. The next generation of the Logic core will include hardware support for transactional memory with 16-entry transactional buffers.

The Logic core chiplet is the glue that holds the PIP CISC platform together. It runs the operating system scheduler, the memory manager, the interrupt handlers, and the device drivers. It also executes the parts of the application that are not vectorizable: the setup code, the cleanup code, and the error handling code. Without the Logic cores, the Math cores would be unable to run any program.

# Chapter 6: System Core Chiplet CMOS Design

The System core chiplet is the master controller of the PIP CISC platform. Unlike the Math cores that excel at vector processing and the Logic cores that handle branching, the System cores are optimized for I/O, memory management, interrupt handling, and optical fabric communication. Each System core chiplet contains 4 physical cores, each capable of executing 64-bit scalar instructions at 4 GHz. The chiplets are manufactured on TSMC's 3nm process, but with design optimizations for high clock speed rather than high transistor density. Forty such chiplets are arranged in an 8x5 grid on the interposer, providing a total of 160 System cores.

The System core is a single-issue, in-order processor with a 15-stage pipeline. The pipeline is deeper than the Logic core's pipeline because the System core must achieve a higher clock speed of 4 GHz. The pipeline stages are fetch, fetch2, decode, decode2, decode3, rename, dispatch, issue, regread, exec1, exec2, exec3, mem, writeback, and commit. The 15-stage pipeline allows a clock speed of 4 GHz, but incurs a 15-cycle penalty for branch mispredictions.

The instruction fetch unit fetches 16 bytes of instruction data from the L1 instruction cache each cycle. The fetch unit includes a simple branch predictor with 85 percent accuracy. The System core does not require a sophisticated branch predictor because its code is mostly straight-line with few branches. The branch predictor uses a 1K-entry bimodal predictor that is sufficient for the System core's workload.

The decode unit receives 16 bytes of instruction data and extracts up to 2 instructions per cycle. The decode unit also performs microcode expansion for complex system instructions. The microcode ROM stores 2,048 entries, each 128 bits wide, containing sequences of micro-operations for instructions like SYSENTER, SYSEXIT, and the memory management instructions. The microcode ROM is implemented as a read-only memory in the metal layers, not as a programmable ROM.

The rename unit is simpler than the Logic core's rename unit because the System core is in-order. The rename unit maps the 64 architectural registers to 128 physical registers, but the mapping is static rather than dynamic. The rename unit also includes a register alias table that is updated only on context switches, not on every instruction.

The dispatch unit sends decoded instructions to the execution units. The System core has 4 issue ports: port 0 for ALU operations, port 1 for load-store operations, port 2 for branch operations, and port 3 for system operations. The system operations include SYSENTER, SYSEXIT, and the memory management instructions that are not handled by the microcode ROM.

The integer ALU is 64 bits wide and can execute one ALU operation per cycle. The ALU contains a 64-bit adder, a 64-bit shifter, and a logical unit. The ALU also contains a multiplier that produces a 128-bit product from two 64-bit operands in 3 cycles. The multiplier is used for address translation and for the cryptographic operations required for capability tokens.

The cryptographic unit is a dedicated accelerator for AES, SHA-1, and SHA-256. The cryptographic unit can encrypt or decrypt a 256-bit block in 10 cycles, and can compute a SHA-256 hash of a 512-byte block in 100 cycles. The cryptographic unit is used to verify capability tokens and to secure the optical fabric communication. The unit includes a hardware random number generator that produces 256 bits of entropy every 100 cycles.

The load-store unit handles all memory accesses. The load-store unit has a 64-entry load buffer and a 32-entry store buffer. The load-store unit also includes a hardware prefetcher that predicts future memory accesses and loads them into the cache before they are needed. The prefetcher is particularly important for the System core because it handles streaming I/O and memory-mapped flash.

The L1 instruction cache is 32 kilobytes of 2-way set-associative SRAM with a 64-byte cache line. The smaller associativity is acceptable because the System core's instruction footprint is small. The cache is implemented as 2 banks of 16 kilobytes each, with a tag array that stores 20-bit tags for 512 sets.

The L1 data cache is 32 kilobytes of 2-way set-associative SRAM with a 64-byte cache line. The data cache uses a write-through policy for all accesses because the System core's data must be visible to the other cores immediately. The write-through policy ensures that the L2 cache is always up to date.

The TLB has 256 entries and is 8-way set-associative. The large TLB reflects the fact that the System core handles address translation for the entire system. Each entry maps a 4KB virtual page to a 4KB physical page, plus 4 bits of permission. The TLB also supports 2MB and 1GB pages for mapping large I/O regions and memory-mapped flash.

The TLB miss handler is implemented in hardware, not in microcode. The hardware walker traverses the segment tree to find the physical address for a virtual address. The segment tree walk takes up to 12 cycles for a tree of depth 6. The TLB miss handler also updates the TLB with the new mapping.

The L2 cache is shared among all 4 cores on the chiplet. The L2 cache is 1 megabyte of 4-way set-associative SRAM with a 64-byte cache line. The cache is partitioned into 4 banks of 256 kilobytes each. The L2 cache uses a write-back policy for lines that are not shared, and a write-through policy for lines that are shared with other cores.

The L2 cache is connected to the cores through a crossbar switch. The crossbar provides full connectivity between the 4 cores and the L2 cache banks. The crossbar has 4 input ports and 4 output ports, each 128 bits wide, operating at 4 GHz. The crossbar uses a simple round-robin arbitration scheme.

The System core also includes an interrupt controller that can handle 256 interrupt sources. The interrupt controller is integrated into the core and is accessible through the system instructions. The interrupt controller has a programmable priority scheme with 16 priority levels. The interrupt controller also includes a timer that can generate periodic interrupts for the operating system scheduler.

The interrupt controller is connected to the optical fabric through a dedicated interface. The interface allows interrupts to be sent from one blade to another. When a remote interrupt is received, the interrupt controller treats it as a local interrupt and delivers it to the appropriate core. The remote interrupt latency is 5 microseconds, dominated by the optical fabric round trip.

The System core includes a memory management unit that controls the segment tree. The MMU has a dedicated 128-entry cache for segment descriptors. The segment descriptor cache is fully associative and uses a least-recently-used replacement policy. The MMU also includes the hardware for walking the segment tree on a TLB miss.

The System core includes a power management unit that controls the clock frequency and supply voltage of all cores on the blade. The power management unit communicates with the rack management controller through the optical fabric. The power management unit can put individual cores into a low-power sleep state, or shut them down completely.

The chiplet also includes a built-in self-test controller that can test all 4 cores in parallel. The self-test controller generates test patterns for the ALU, the cache, the TLB, the crossbar, and the interrupt controller. The test patterns are applied at the full clock speed, and the results are compared to the expected values. The self-test completes in 0.2 seconds.

The System core chiplet is attached to the interposer using the same hybrid bonding process as the Math and Logic cores. The bonding pads are 5 microns in diameter at 9-micron pitch, arranged in a 100x100 grid around the perimeter of the chiplet. The chiplet measures 2mm by 2.5mm, larger than the Logic core chiplet because it contains additional logic for memory management and interrupt handling.

The chiplet is manufactured on TSMC's 3nm process line at Fab 18. The line produces 10,000 wafers per month, each wafer containing 1,000 chiplets. The yield is 80 percent for the System core chiplet, the same as the Math core. The chiplet cost is $12 per unit in volume production.

The System core chiplet consumes 1 watt per core, for a total of 4 watts per chiplet. The 40 chiplets on a blade consume 160 watts, much less than the Math and Logic cores. The lower power consumption is due to the lower transistor count and the in-order design.

The System core is designed for high clock speed and low latency. The 4 GHz clock speed allows the System core to respond to interrupts quickly and to process memory management requests with minimal delay. The 15-stage pipeline is optimized for frequency, not for instruction-level parallelism.

The System core includes a hardware performance monitor that tracks the number of instructions executed, the number of cycles, the number of cache misses, the number of TLB misses, and the number of interrupts. The performance monitor is accessible through the test access port and can be used to tune the operating system for the System core.

The System core includes a temperature sensor at the center of the die. The temperature sensor is used by the power management unit to throttle the core when the temperature exceeds 85 degrees Celsius. Throttling reduces the clock frequency by 25 percent until the temperature drops below 80 degrees Celsius.

The System core chiplet is the master of the PIP CISC platform. Its 160 cores run the operating system, manage the memory, handle the interrupts, and control the optical fabric. Without the System cores, the Math and Logic cores would be unable to communicate with the outside world.

The chiplet design is verified by simulation at the RTL, gate, and transistor levels. The RTL simulation verifies the functional correctness of the core. The gate-level simulation verifies the timing and the power consumption. The transistor-level simulation verifies the signal integrity and the noise margins. The chiplet passes all simulations before being released for manufacturing.

The interaction between the System core chiplet and the interposer is critical. The hybrid bonding pads must align with the interposer pads to within 1 micron. The thermal expansion of the chiplet and the interposer must be matched to within 1 part per million per degree Celsius. The power supply voltage must be delivered to the chiplet with less than 10 millivolts of IR drop.

The chiplet includes on-die decoupling capacitors that filter high-frequency noise on the power supply. The decoupling capacitors are implemented as metal-insulator-metal capacitors in the upper metal layers. The total capacitance on the chiplet is 25 nanofarads, enough to hold the voltage stable during current transients of 2.5 amps per nanosecond.

The chiplet includes a security unit that implements the cryptographic functions required for capability tokens and for secure boot. The security unit contains a hardware random number generator, an AES-256 engine, an ECDSA engine, and a SHA-256 engine. The security unit also stores the blade's private key, which is unique to each blade and is programmed during manufacturing.

The chiplet includes a test access port that conforms to the IEEE 1149.1 JTAG standard. The test access port provides access to the boundary scan chain and to the internal test registers. The test access port is used during manufacturing to test the chiplet and during system bring-up to debug the hardware.

The System core chiplet is the smallest of the three chiplet types in terms of core count, but the largest in terms of functionality. Its 160 cores handle all of the system-level tasks that the other cores cannot. The chiplet's high clock speed and low latency are essential for the responsiveness of the PIP CISC platform.

The future of the System core chiplet includes integration of the optical transceiver controllers onto the chiplet. The optical transceiver controllers are currently implemented in the interposer, but moving them to the System core chiplet would reduce latency and improve performance. The next generation of the System core will include 12 optical transceiver controllers, one for each fiber on the blade.

The System core chiplet is the brain of the PIP CISC platform. It boots the system, loads the operating system, manages the memory, handles the interrupts, and controls the optical fabric. The System cores are the first to start and the last to stop. They are the only cores that have direct access to the I/O devices and to the optical transceivers. Without the System cores, the PIP CISC platform would be a collection of dumb compute engines with no way to communicate with the outside world.

# Chapter 7: HBM3e Memory Stack Integration

The HBM3e memory stacks provide the main memory for the PIP CISC platform. Unlike traditional systems where memory is installed in DIMM slots separate from the processor, the HBM3e stacks are attached directly to the interposer, just millimeters away from the core chiplets. This proximity reduces memory access latency from tens of nanoseconds to a few nanoseconds and increases bandwidth from tens of gigabytes per second to terabytes per second. Eight HBM3e stacks are attached to the interposer around the perimeter of the core complex, providing a total capacity of 64 gigabytes and a total bandwidth of 4 terabytes per second.

Each HBM3e stack contains eight DRAM dies vertically interconnected with through-silicon vias, plus a base logic die at the bottom that contains the memory controller and the helper cores. The stack measures 10mm by 8mm and is 720 microns tall. The eight DRAM dies are each 80 microns thick, and the base logic die is 80 microns thick, for a total stack height of 720 microns including the solder bumps. The stack is attached to the interposer using thermal compression bonding with 20-micron pitch solder bumps.

The DRAM dies are manufactured on a 10nm DRAM process optimized for density rather than speed. Each DRAM die contains 8 independent memory banks, each 512 megabytes in capacity, for a total of 4 gigabytes per die. The eight dies in a stack provide 32 gigabytes per stack, but the PIP CISC platform uses only 8 gigabytes per stack because the remaining capacity is reserved for error correction and redundancy. The 8 gigabytes per stack times 8 stacks equals 64 gigabytes of usable memory.

Each DRAM die is organized as 64,000 rows of 8,192 bytes each, for a total of 512 megabytes per bank. The row access time is 15 nanoseconds, the column access time is 2.5 nanoseconds, and the cycle time is 20 nanoseconds. The DRAM uses a bank-group architecture that allows different banks to be accessed in parallel. The eight banks in a die are divided into two bank groups of four banks each.

The through-silicon vias in the DRAM dies are 5 microns in diameter at 10-micron pitch. The vias are arranged in two rows along the center of the die, leaving the edges for the memory banks. The vias carry data, address, command, and power signals between the dies. A total of 2,048 vias per die provide 1,024 data signals (64 bytes per access times 16 bits per byte) and 1,024 control signals.

The base logic die is manufactured on a 28nm logic process optimized for low power. The die contains the memory controller, the PHY interface, and the 32 helper cores. The memory controller translates requests from the PIP-Fabric into DRAM commands: activate, read, write, precharge, and refresh. The controller also handles the timing requirements of the DRAM, inserting the necessary delays between commands.

The memory controller includes a 32-entry command queue that reorders requests to maximize row hits. A row hit occurs when a request accesses a row that is already open in a bank. Row hits have a latency of 10 nanoseconds, while row misses have a latency of 30 nanoseconds because the open row must be closed and a new row opened. The reorder queue can improve the row hit rate from 50 percent to 80 percent, reducing the average latency from 20 nanoseconds to 14 nanoseconds.

The PHY interface connects the memory stack to the interposer. The PHY contains 1,024 data pins operating at 6.4 gigabits per second, for a total bandwidth of 6.4 terabits per second per stack. The PHY uses differential signaling with a voltage swing of 200 millivolts. The pins are arranged in 4 rows of 256 pins along the long edge of the die. The PHY also includes delay-locked loops that align the data signals with the clock.

The 32 helper cores are small 32-bit RISC processors that run at 1 GHz. Each helper core has 16 kilobytes of instruction memory and 16 kilobytes of data memory. The helper cores execute firmware that handles error correction, wear leveling for the flash storage, and address translation for memory-mapped I/O. The helper cores communicate with the main memory controller through a mailbox interface.

The error correction firmware uses a Reed-Solomon code that can correct up to 8 bit errors per 256-byte block. The helper cores read the error correction codes from a reserved area of the DRAM, compute the syndromes, and correct any errors. The error correction adds 10 microseconds of latency to reads that encounter errors, but errors are rare (one per 10^15 bits read) so the average impact is negligible.

The wear leveling firmware manages the NAND flash storage. The helper cores maintain a mapping from logical block addresses to physical block addresses, and they move data between blocks to ensure that all blocks wear evenly. The wear leveling algorithm is a modified version of the greedy algorithm that selects the block with the fewest erase cycles for new writes.

The address translation firmware handles the memory-mapped I/O. The helper cores maintain a translation table that maps physical addresses to I/O device addresses. When a load or store instruction accesses an I/O address, the memory controller traps to a helper core, which translates the address and forwards the request to the appropriate device.

The HBM3e stacks are attached to the interposer using thermal compression bonding. The bonding pads on the bottom of the base logic die are 20 microns in diameter at 40-micron pitch, matching the pads on the interposer. The bonding process uses a temperature of 350 degrees Celsius and a force of 20 Newtons per stack. The process takes 10 seconds per stack, for a total of 80 seconds per blade.

The memory stacks are tested before attachment to the interposer. Each stack is tested at speed using a dedicated tester that simulates the PIP-Fabric. The tester applies a pattern of reads and writes to all addresses in the stack, checking for stuck bits, coupling faults, and row hammer vulnerabilities. The test takes 10 seconds per stack.

The memory stacks are also tested after attachment to the interposer. The interposer includes test access points that allow the System cores to access each stack individually. The System cores run a memory test that verifies the connectivity between the interposer and the stacks, and that tests the stacks at the full 6.4 gigabits per second data rate.

The HBM3e stack is the highest-bandwidth component in the PIP CISC platform. Its 4 terabytes per second bandwidth is sufficient to feed all 10,000 Math cores simultaneously, assuming each core consumes 400 megabytes per second. The bandwidth is achieved through the 1,024 data pins operating at 6.4 gigabits per second, for a total of 6.4 terabits per second per stack, or 51.2 terabits per second for 8 stacks.

The latency of the HBM3e stack is dominated by the DRAM access time, not by the interposer or the PHY. The DRAM row access time is 15 nanoseconds, the column access time is 2.5 nanoseconds, and the interposer adds 1 nanosecond of propagation delay. The total latency from a Math core to the HBM3e stack is approximately 20 nanoseconds for a row hit, and 40 nanoseconds for a row miss.

The HBM3e stack is the most expensive component in the PIP CISC platform after the core chiplets. Each stack costs $200 in volume production, for a total of $1,600 per blade. The cost is driven by the 28nm base logic die, which is expensive to manufacture, and by the assembly process, which requires precise alignment and bonding.

The future of the HBM3e stack includes stacking more DRAM dies. The current stack has 8 dies, but the technology supports up to 16 dies. A 16-die stack would provide 16 gigabytes per stack, for a total of 128 gigabytes per blade. The next generation of the PIP CISC platform will use 16-die stacks, doubling the memory capacity.

The HBM3e stack is the memory backbone of the PIP CISC platform. Its high bandwidth and low latency are essential for feeding the 10,000 Math cores. Without the HBM3e stacks, the Math cores would starve for data, and the platform would not achieve its performance potential. The integration of the memory stacks directly onto the interposer is a key innovation that enables the PIP CISC architecture.

The memory stacks also include temperature sensors that monitor the die temperature. The sensors are implemented as diode-connected transistors that have a temperature-dependent voltage. The sensors are distributed across the stack at 2mm spacing. The temperature readings are used by the power management unit to adjust the refresh rate of the DRAM. Higher temperatures require more frequent refresh to prevent data loss.

The memory stacks include a built-in self-test controller that can test all banks in parallel. The self-test controller generates a pattern of read and write operations that exercises every memory cell. The pattern is based on the March C- algorithm, which detects stuck-at faults, coupling faults, and neighborhood pattern sensitive faults. The self-test completes in 100 milliseconds per stack.

The memory stacks include a redundancy repair unit that can replace defective rows and columns. The repair unit has 16 spare rows and 16 spare columns per bank. When a defect is detected during test, the repair unit remaps the defective row or column to a spare. The repair information is stored in non-volatile memory on the base logic die.

The memory stacks include a row hammer mitigation unit that prevents the row hammer vulnerability. The row hammer vulnerability occurs when a row is accessed repeatedly, causing charge leakage in adjacent rows. The mitigation unit counts the number of accesses to each row and refreshes adjacent rows when the count exceeds a threshold.

The HBM3e stack is a masterpiece of 3D integration. Its eight DRAM dies are stacked with through-silicon vias, creating a single memory device with 32 times the density of a single die. The base logic die integrates the memory controller and the helper cores, offloading these tasks from the System cores. The HBM3e stack is the enabling technology for the unified memory architecture of the PIP CISC platform.

# Chapter 8: NAND Flash Storage Array

The NAND flash storage array provides non-volatile memory for the PIP CISC platform. Unlike traditional systems where storage is accessed through a controller and a block I/O interface, the PIP CISC platform maps flash chips directly into the memory address space. A load instruction to a flash address triggers a hardware flash read, and a store instruction to a flash address triggers a hardware flash write. The operating system is not involved in storage access; the hardware handles everything. This eliminates the system call overhead, the interrupt latency, and the data copying that plague traditional storage systems.

The flash chips are soldered directly to the motherboard substrate, not to the interposer. This allows configurable storage capacity without redesigning the interposer layout. Three capacity options are offered: 10TB using twenty 512GB chips arranged in two rows along the bottom edge of the board, 20TB using forty 512GB chips, or 100TB using eighty 1.28TB chips occupying both sides of the substrate. The flash chips are arranged in a grid with 1mm spacing between chips, allowing for airflow and access for rework.

Each flash chip measures 12mm by 18mm and contains 8 planes of 256 gigabytes each. The planes can be accessed in parallel, providing a raw bandwidth of 1.6 gigabytes per second per chip. The read latency is 50 microseconds, the write latency is 500 microseconds, and the erase latency is 5 milliseconds. The chips use 3D NAND technology with 128 layers of floating-gate transistors, providing a storage density of 10 gigabits per square millimeter.

The 3D NAND structure consists of alternating layers of polysilicon and silicon dioxide etched with vertical channels. The channels are filled with polysilicon to form the channel of the floating-gate transistors, and the word lines are formed by the polysilicon layers. Each vertical channel serves 128 transistors, one per layer. The structure is manufactured by depositing the layers, etching the channels, and then depositing the channel polysilicon. The process is repeated 128 times to build the full stack.

The flash chips communicate with the PIP-Fabric through a simplified ONFi interface implemented in the substrate. Each chip has 8 data lanes operating at 5 gigabits per second, for a total bandwidth of 5 gigabytes per second per chip. The interface uses 1.2 volt signaling with 100-ohm differential impedance. The pins are arranged along the long edge of the chip in two rows of 64 pins each.

The ONFi interface implements a subset of the full ONFi 5.0 specification. The supported commands include page read, page program, block erase, read status, and reset. The interface does not support the more advanced features like interleaved addressing or multi-plane operations because the PIP-Fabric provides those capabilities at a higher level.

The memory controller in the System cores manages the flash address translation. A translation table in DRAM maps 4KB memory pages to flash block addresses. The table uses a log-structured merge tree to optimize for the write-once nature of flash. The log-structured merge tree has three levels: a small write buffer in DRAM, a medium-sized cache in the HBM3e memory, and the main table in flash.

When a write instruction targets a flash address, the following occurs. The System core checks the translation table in the DRAM cache. If the page is found, the System core updates the mapping to point to a new location and writes the data to the new location. The old location is marked as invalid and will be garbage collected later. If the page is not found in the cache, the System core loads the relevant portion of the translation table from flash into the cache, then proceeds with the write.

The helper cores in the HBM3e stacks assist with the flash management. There are 32 helper cores per memory stack, for a total of 256 helper cores on a blade. The helper cores run firmware that handles garbage collection, wear leveling, and bad block management. The helper cores communicate with the System cores through a mailbox interface.

The garbage collection firmware reclaims space occupied by invalid pages. The firmware selects a block with a high number of invalid pages, copies the valid pages to a new block, and erases the old block. The garbage collection runs continuously in the background, using idle cycles of the helper cores. The garbage collection bandwidth is 500 megabytes per second, sufficient to keep up with the write traffic from the System cores.

The wear leveling firmware ensures that all flash blocks are erased approximately the same number of times. Flash blocks can be erased only 3,000 to 10,000 times before they become unreliable. The wear leveling algorithm maintains an erase count for each block and selects blocks with low erase counts for new writes. The algorithm also periodically moves data from blocks with high erase counts to blocks with low erase counts.

The bad block management firmware identifies blocks that have become unreliable and removes them from use. The firmware tests blocks after each erase, checking for bits that cannot be programmed or erased. If a block fails the test, it is marked as bad and added to a bad block list. The firmware also periodically retires blocks that have high error rates, even if they have not failed completely.

The flash chips are attached to the substrate using reflow soldering. The pads on the substrate are 0.5mm in diameter at 1mm pitch. The chips are placed by a pick-and-place machine with an accuracy of 25 microns, then reflowed at 260 degrees Celsius for 60 seconds. The solder is a lead-free tin-silver-copper alloy that forms reliable connections between the chip pads and the substrate pads.

The flash chips are tested before attachment to the substrate. Each chip is tested at speed using a dedicated tester that simulates the ONFi interface. The tester writes a pattern to all pages in the chip, reads it back, and checks for errors. The tester also erases all blocks and checks that the erase succeeded. The test takes 10 seconds per chip, which is acceptable for production volumes.

The flash chips are also tested after attachment to the substrate. The System cores run a flash test that verifies the connectivity between the substrate and the chips, and that tests the chips at the full 5 gigabits per second data rate. The test takes 1 second per chip, for a total of 20 seconds for a 20-chip configuration.

The flash array is organized as a single logical address space. The 10TB configuration has 2.5 billion 4KB pages, each with a unique address. The 20TB configuration has 5 billion pages, and the 100TB configuration has 25 billion pages. The address space is linear, meaning that a program can access any page using a single 64-bit address.

The performance of the flash array is limited by the flash chips themselves, not by the interface or the translation table. The read latency is 50 microseconds, the write latency is 500 microseconds, and the erase latency is 5 milliseconds. These latencies are high compared to DRAM (50 nanoseconds), but they are low compared to traditional storage (10 milliseconds for a hard drive, 100 microseconds for an NVMe drive with software overhead).

The bandwidth of the flash array scales with the number of chips. The 10TB configuration has 20 chips, each with 5 gigabytes per second of bandwidth, for a total of 100 gigabytes per second. The 20TB configuration has 200 gigabytes per second, and the 100TB configuration has 400 gigabytes per second. This bandwidth is sufficient to stream data from flash to the Math cores at full speed.

The reliability of the flash array is enhanced by the error correction and wear leveling. The error correction can correct up to 8 bit errors per 1KB page, which is sufficient for the lifetime of the flash. The wear leveling ensures that all blocks are erased approximately the same number of times, preventing premature failure of heavily used blocks. The expected lifetime of the flash array is 5 years with continuous writing at 100 gigabytes per second.

The flash array is the largest component on the motherboard after the interposer. The 100TB configuration uses eighty 1.28TB chips, each 12mm by 18mm, for a total area of 17,280 square millimeters. The chips are mounted on both sides of the substrate, with 40 chips on the top side and 40 chips on the bottom side. The chips are arranged in a grid with 1mm spacing, covering most of the substrate area.

The power consumption of the flash array is significant. Each flash chip consumes 2 watts when reading, 5 watts when writing, and 0.1 watts when idle. The 100TB configuration consumes 400 watts when writing at full speed, 160 watts when reading at full speed, and 8 watts when idle. The power consumption is managed by the power management unit, which can put idle chips into a low-power state.

The flash array generates heat that must be removed by the thermal encasement. The flash chips are in direct contact with the pyrolytic graphite sheet that encases the motherboard. The graphite sheet spreads the heat from the flash chips across the entire board, preventing hot spots. The liquid cold plate or copper heat spreader then removes the heat from the graphite sheet.

The flash array is the storage backbone of the PIP CISC platform. Its 100TB capacity can store entire datasets that would otherwise require a separate storage server. Its 400 gigabytes per second bandwidth can stream data to the Math cores as fast as they can consume it. Its memory-mapped interface eliminates the software overhead of traditional storage, allowing programs to access flash as if it were DRAM.

The future of the flash array includes the use of QLC (quad-level cell) flash, which stores 4 bits per cell instead of 3. QLC flash has a capacity of 2.56TB per chip, doubling the capacity of the 100TB configuration to 200TB without increasing the chip count. The write latency of QLC flash is higher (1 millisecond), but the read latency is the same (50 microseconds). The next generation of the PIP CISC platform will use QLC flash for cost-effective capacity.

The flash array is the persistent memory of the PIP CISC platform. It stores the operating system, the applications, and the user data. It is also used as swap space when the DRAM is full. The memory-mapped interface allows the operating system to treat flash as just another level of the memory hierarchy, with the hardware managing the movement of data between DRAM and flash.

This concludes Chapter 8 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Optical Transceiver Assembly, covering the silicon photonic integrated circuits, the fiber array attachment, and the interface to the PIP-Fabric.
# Chapter 9: Optical Transceiver Assembly

The optical transceivers are the gateway between the PIP CISC blade and the outside world. They provide communication to other blades in the same rack, to other racks in the same cluster, and to the external network. Each transceiver converts electrical signals from the PIP-Fabric into optical signals carried on single-mode fiber, and vice versa. Twelve transceivers are mounted along the rear edge of each blade, providing a total off-board bandwidth of 9.6 terabits per second. The transceivers are the only components on the blade that interface with the external environment, making them critical for system integration.

Each optical transceiver is a silicon photonic integrated circuit measuring 5mm by 5mm, manufactured on TSMC's 130nm photonic process. The photonic process includes both electronic transistors for the control circuitry and optical components for the light generation, modulation, and detection. The chip contains four micro-ring modulators, four germanium photodetectors, a wavelength-division multiplexer, a demultiplexer, and the associated driver and receiver electronics.

The laser source is external to the photonic chip. A continuous-wave laser module mounted on the substrate next to the photonic chip emits light at four wavelengths: 1270, 1290, 1310, and 1330 nanometers. The laser module produces 100 milliwatts of power at each wavelength, for a total of 400 milliwatts. The light is coupled into the photonic chip through a grating coupler with an efficiency of 70 percent. The 30 percent loss is dissipated as heat in the coupler.

The four wavelengths are generated by four separate laser diodes, each with its own temperature controller. The temperature controllers maintain the laser diodes at a precise temperature to stabilize the wavelength. The temperature controllers are implemented as thermoelectric coolers that can adjust the temperature by 10 degrees Celsius in either direction. The temperature control consumes 500 milliwatts per laser diode, for a total of 2 watts per transceiver.

The micro-ring modulators are the key active components in the transmit path. Each modulator is a ring-shaped waveguide with a diameter of 10 microns. The ring is designed to resonate at a specific wavelength; when a voltage is applied, the refractive index of the ring changes, shifting the resonance away from the laser wavelength. This modulation changes the amount of light coupled from the laser into the output waveguide, creating a 200 gigabit per second optical signal.

The modulators are driven by differential driver circuits that produce a 1-volt peak-to-peak signal at 200 gigabits per second. The drivers are implemented in the electronic part of the photonic chip and consume 500 milliwatts each, for a total of 2 watts per transceiver. The drivers are matched to the modulators to minimize reflections and maximize the modulation depth.

The four modulated signals are combined by a wavelength-division multiplexer. The multiplexer is an arrayed waveguide grating that combines the four wavelengths into a single waveguide. The multiplexer has an insertion loss of 3 decibels, meaning half the power is lost. The loss is acceptable because the laser power is high and the photodetectors are sensitive.

The combined signal is coupled into a single-mode fiber through an edge coupler. The edge coupler is a tapered waveguide that expands the mode from the 0.5-micron wide waveguide to the 9-micron diameter fiber core. The coupling efficiency is 80 percent, for a total loss of 1 decibel. The fiber is glued into a V-groove etched in the photonic chip, with the core aligned to the edge coupler within 1 micron.

The receive path is symmetric to the transmit path. The incoming optical signal from the fiber is coupled into the photonic chip through an edge coupler. The signal is then demultiplexed by another arrayed waveguide grating into the four wavelengths. Each wavelength is directed to a germanium photodetector.

The germanium photodetectors convert the optical signal back into an electrical current. The photodetectors are 20 microns in diameter and have a bandwidth of 50 GHz. The responsivity is 0.8 amperes per watt, meaning that 1 milliwatt of optical power produces 0.8 milliamperes of current. The dark current is 10 nanoamperes, which is negligible.

The photodetector current is amplified by a transimpedance amplifier that converts the current to a voltage. The transimpedance amplifier has a gain of 1,000 ohms and a bandwidth of 50 GHz. The output voltage is 0.8 volts for a 1 milliwatt input. The amplifier consumes 500 milliwatts per channel, for a total of 2 watts per transceiver.

The amplified signals are then processed by a clock and data recovery circuit that extracts the clock from the data and retimes the data. The clock and data recovery circuit uses a phase-locked loop that locks to the incoming data stream. The circuit consumes 500 milliwatts per channel, for a total of 2 watts per transceiver.

The recovered data is then sent to the PIP-Fabric through a SerDes interface. The SerDes converts the parallel data from the PIP-Fabric (128 bits at 1.56 GHz) to the serial data for the optical link (1 bit at 200 GHz). The SerDes consumes 500 milliwatts per transceiver.

The optical transceivers are attached to the substrate using flip-chip bonding. The bonding pads on the photonic chip are 50 microns in diameter at 100-micron pitch. The chip is aligned to the substrate using fiducial marks with an accuracy of 1 micron. The alignment is critical because the fiber array must be positioned precisely over the edge couplers.

The fiber array contains 12 single-mode fibers, one for each transceiver. The fibers are glued into a V-groove array etched in a silicon interposer. The V-grooves are 125 microns wide and 62.5 microns deep, matching the diameter of the fiber cladding. The fibers are stripped of their coating and placed in the V-grooves, then glued with epoxy. The fiber ends are polished at an 8-degree angle to prevent back-reflection.

The fiber array is aligned to the photonic chips by a robotic alignment system. The system uses a camera to locate the edge couplers on each photonic chip, then moves the fiber array until the fibers are centered over the couplers. The alignment accuracy is 1 micron, which is achievable with modern robotics. The fiber array is then glued to the substrate with UV-cured epoxy.

The optical transceivers are tested before attachment to the substrate. Each transceiver is tested at speed using a dedicated tester that simulates the PIP-Fabric and the fiber link. The tester measures the transmitter output power, the extinction ratio, the jitter, and the bit error rate. The tester also measures the receiver sensitivity and the input dynamic range. The test takes 1 second per transceiver.

The transceivers are also tested after attachment to the substrate. The System cores run a link test that sends a pattern of data through each transceiver and verifies that the pattern is received correctly. The test also measures the bit error rate by counting errors over a long period. The test takes 1 minute per transceiver, for a total of 12 minutes per blade.

The optical transceivers consume significant power. Each transceiver consumes 2 watts for the laser, 2 watts for the modulators, 2 watts for the photodetectors, 2 watts for the clock and data recovery, and 0.5 watts for the SerDes, for a total of 8.5 watts per transceiver. The 12 transceivers on a blade consume 102 watts, which is a significant portion of the blade's 700-watt power budget.

The optical transceivers generate heat that must be removed by the thermal encasement. The transceivers are in direct contact with the pyrolytic graphite sheet that encases the motherboard. The graphite sheet spreads the heat from the transceivers across the entire board, preventing hot spots. The liquid cold plate then removes the heat from the graphite sheet.

The optical transceivers are the highest-bandwidth components in the PIP CISC platform. Their 9.6 terabits per second of off-board bandwidth allows the blade to communicate with other blades at speeds that approach the bandwidth of the on-board memory. The low latency of the optical link (5 microseconds round trip) allows the blades to be tightly coupled into a single shared-memory system.

The optical transceivers also include diagnostic features that monitor the health of the link. The transceivers measure the received optical power, the laser bias current, the temperature, and the supply voltage. These measurements are accessible to the System cores through a management interface. The System cores use this information to detect failing transceivers before they cause errors.

The optical transceivers include a laser safety feature that shuts off the laser if the fiber is disconnected. The safety feature uses a photodetector that monitors the back-reflection from the fiber. If the back-reflection drops below a threshold, the laser is shut off within 1 microsecond. This prevents eye damage and complies with laser safety regulations.

The optical transceivers are the gateway to the outside world for the PIP CISC blade. They connect the blade to the rack backplane, which provides communication to other blades and to the external network. The rack backplane contains embedded optical waveguides that route signals between the blades, eliminating the need for external fiber cables within the rack.

The future of the optical transceivers includes integration of the laser source onto the photonic chip. Hybrid integration of a III-V laser on a silicon photonic chip is an active area of research, and TSMC has demonstrated prototype devices. Integrating the laser would reduce the transceiver power consumption by 2 watts and simplify the assembly.

The optical transceivers are the only moving parts on the PIP CISC blade. The fibers are flexible and can vibrate, but the photonic chips themselves have no moving parts. The reliability of the optical transceivers is determined by the laser lifetime, which is 10 years at the operating temperature. The transceivers are expected to outlast the useful life of the blade.

This concludes Chapter 9 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Thermal Encasement and Cooling System, covering the pyrolytic graphite sheets, the liquid cold plates, and the rack-level cooling infrastructure.
# Chapter 9: Optical Transceiver Assembly

The optical transceivers are the gateway between the PIP CISC blade and the outside world. They provide communication to other blades in the same rack, to other racks in the same cluster, and to the external network. Each transceiver converts electrical signals from the PIP-Fabric into optical signals carried on single-mode fiber, and vice versa. Twelve transceivers are mounted along the rear edge of each blade, providing a total off-board bandwidth of 9.6 terabits per second. The transceivers are the only components on the blade that interface with the external environment, making them critical for system integration.

Each optical transceiver is a silicon photonic integrated circuit measuring 5mm by 5mm, manufactured on TSMC's 130nm photonic process. The photonic process includes both electronic transistors for the control circuitry and optical components for the light generation, modulation, and detection. The chip contains four micro-ring modulators, four germanium photodetectors, a wavelength-division multiplexer, a demultiplexer, and the associated driver and receiver electronics.

The laser source is external to the photonic chip. A continuous-wave laser module mounted on the substrate next to the photonic chip emits light at four wavelengths: 1270, 1290, 1310, and 1330 nanometers. The laser module produces 100 milliwatts of power at each wavelength, for a total of 400 milliwatts. The light is coupled into the photonic chip through a grating coupler with an efficiency of 70 percent. The 30 percent loss is dissipated as heat in the coupler.

The four wavelengths are generated by four separate laser diodes, each with its own temperature controller. The temperature controllers maintain the laser diodes at a precise temperature to stabilize the wavelength. The temperature controllers are implemented as thermoelectric coolers that can adjust the temperature by 10 degrees Celsius in either direction. The temperature control consumes 500 milliwatts per laser diode, for a total of 2 watts per transceiver.

The micro-ring modulators are the key active components in the transmit path. Each modulator is a ring-shaped waveguide with a diameter of 10 microns. The ring is designed to resonate at a specific wavelength; when a voltage is applied, the refractive index of the ring changes, shifting the resonance away from the laser wavelength. This modulation changes the amount of light coupled from the laser into the output waveguide, creating a 200 gigabit per second optical signal.

The modulators are driven by differential driver circuits that produce a 1-volt peak-to-peak signal at 200 gigabits per second. The drivers are implemented in the electronic part of the photonic chip and consume 500 milliwatts each, for a total of 2 watts per transceiver. The drivers are matched to the modulators to minimize reflections and maximize the modulation depth.

The four modulated signals are combined by a wavelength-division multiplexer. The multiplexer is an arrayed waveguide grating that combines the four wavelengths into a single waveguide. The multiplexer has an insertion loss of 3 decibels, meaning half the power is lost. The loss is acceptable because the laser power is high and the photodetectors are sensitive.

The combined signal is coupled into a single-mode fiber through an edge coupler. The edge coupler is a tapered waveguide that expands the mode from the 0.5-micron wide waveguide to the 9-micron diameter fiber core. The coupling efficiency is 80 percent, for a total loss of 1 decibel. The fiber is glued into a V-groove etched in the photonic chip, with the core aligned to the edge coupler within 1 micron.

The receive path is symmetric to the transmit path. The incoming optical signal from the fiber is coupled into the photonic chip through an edge coupler. The signal is then demultiplexed by another arrayed waveguide grating into the four wavelengths. Each wavelength is directed to a germanium photodetector.

The germanium photodetectors convert the optical signal back into an electrical current. The photodetectors are 20 microns in diameter and have a bandwidth of 50 GHz. The responsivity is 0.8 amperes per watt, meaning that 1 milliwatt of optical power produces 0.8 milliamperes of current. The dark current is 10 nanoamperes, which is negligible.

The photodetector current is amplified by a transimpedance amplifier that converts the current to a voltage. The transimpedance amplifier has a gain of 1,000 ohms and a bandwidth of 50 GHz. The output voltage is 0.8 volts for a 1 milliwatt input. The amplifier consumes 500 milliwatts per channel, for a total of 2 watts per transceiver.

The amplified signals are then processed by a clock and data recovery circuit that extracts the clock from the data and retimes the data. The clock and data recovery circuit uses a phase-locked loop that locks to the incoming data stream. The circuit consumes 500 milliwatts per channel, for a total of 2 watts per transceiver.

The recovered data is then sent to the PIP-Fabric through a SerDes interface. The SerDes converts the parallel data from the PIP-Fabric (128 bits at 1.56 GHz) to the serial data for the optical link (1 bit at 200 GHz). The SerDes consumes 500 milliwatts per transceiver.

The optical transceivers are attached to the substrate using flip-chip bonding. The bonding pads on the photonic chip are 50 microns in diameter at 100-micron pitch. The chip is aligned to the substrate using fiducial marks with an accuracy of 1 micron. The alignment is critical because the fiber array must be positioned precisely over the edge couplers.

The fiber array contains 12 single-mode fibers, one for each transceiver. The fibers are glued into a V-groove array etched in a silicon interposer. The V-grooves are 125 microns wide and 62.5 microns deep, matching the diameter of the fiber cladding. The fibers are stripped of their coating and placed in the V-grooves, then glued with epoxy. The fiber ends are polished at an 8-degree angle to prevent back-reflection.

The fiber array is aligned to the photonic chips by a robotic alignment system. The system uses a camera to locate the edge couplers on each photonic chip, then moves the fiber array until the fibers are centered over the couplers. The alignment accuracy is 1 micron, which is achievable with modern robotics. The fiber array is then glued to the substrate with UV-cured epoxy.

The optical transceivers are tested before attachment to the substrate. Each transceiver is tested at speed using a dedicated tester that simulates the PIP-Fabric and the fiber link. The tester measures the transmitter output power, the extinction ratio, the jitter, and the bit error rate. The tester also measures the receiver sensitivity and the input dynamic range. The test takes 1 second per transceiver.

The transceivers are also tested after attachment to the substrate. The System cores run a link test that sends a pattern of data through each transceiver and verifies that the pattern is received correctly. The test also measures the bit error rate by counting errors over a long period. The test takes 1 minute per transceiver, for a total of 12 minutes per blade.

The optical transceivers consume significant power. Each transceiver consumes 2 watts for the laser, 2 watts for the modulators, 2 watts for the photodetectors, 2 watts for the clock and data recovery, and 0.5 watts for the SerDes, for a total of 8.5 watts per transceiver. The 12 transceivers on a blade consume 102 watts, which is a significant portion of the blade's 700-watt power budget.

The optical transceivers generate heat that must be removed by the thermal encasement. The transceivers are in direct contact with the pyrolytic graphite sheet that encases the motherboard. The graphite sheet spreads the heat from the transceivers across the entire board, preventing hot spots. The liquid cold plate then removes the heat from the graphite sheet.

The optical transceivers are the highest-bandwidth components in the PIP CISC platform. Their 9.6 terabits per second of off-board bandwidth allows the blade to communicate with other blades at speeds that approach the bandwidth of the on-board memory. The low latency of the optical link (5 microseconds round trip) allows the blades to be tightly coupled into a single shared-memory system.

The optical transceivers also include diagnostic features that monitor the health of the link. The transceivers measure the received optical power, the laser bias current, the temperature, and the supply voltage. These measurements are accessible to the System cores through a management interface. The System cores use this information to detect failing transceivers before they cause errors.

The optical transceivers include a laser safety feature that shuts off the laser if the fiber is disconnected. The safety feature uses a photodetector that monitors the back-reflection from the fiber. If the back-reflection drops below a threshold, the laser is shut off within 1 microsecond. This prevents eye damage and complies with laser safety regulations.

The optical transceivers are the gateway to the outside world for the PIP CISC blade. They connect the blade to the rack backplane, which provides communication to other blades and to the external network. The rack backplane contains embedded optical waveguides that route signals between the blades, eliminating the need for external fiber cables within the rack.

The future of the optical transceivers includes integration of the laser source onto the photonic chip. Hybrid integration of a III-V laser on a silicon photonic chip is an active area of research, and TSMC has demonstrated prototype devices. Integrating the laser would reduce the transceiver power consumption by 2 watts and simplify the assembly.

The optical transceivers are the only moving parts on the PIP CISC blade. The fibers are flexible and can vibrate, but the photonic chips themselves have no moving parts. The reliability of the optical transceivers is determined by the laser lifetime, which is 10 years at the operating temperature. The transceivers are expected to outlast the useful life of the blade.

This concludes Chapter 9 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Thermal Encasement and Cooling System, covering the pyrolytic graphite sheets, the liquid cold plates, and the rack-level cooling infrastructure.
# Chapter 11: Power Distribution Network

The power distribution network is the circulatory system of the PIP CISC motherboard. It delivers electrical current from the power supply to every transistor on every chiplet, every DRAM cell in every HBM stack, and every flash cell in every NAND chip. The network must deliver 700 amperes of current at 0.8 volts to the Math cores, 200 amperes at 0.8 volts to the Logic cores, 40 amperes at 0.8 volts to the System cores, 30 amperes at 1.2 volts to the HBM stacks, 20 amperes at 3.3 volts to the NAND flash, and 10 amperes at 1.8 volts to the optical transceivers. The total power delivered to the blade is 700 watts, with the remaining 200 watts dissipated as heat in the power distribution network itself.

The power distribution network is implemented in the twelve copper planes embedded in the motherboard substrate. Four planes are dedicated to the core logic voltage of 0.8 volts, four planes to the memory voltage of 1.2 volts, two planes to the I/O voltage of 1.8 volts, and two planes to the flash voltage of 3.3 volts. The planes are 35 microns thick and are perforated with thermal vias that allow heat to flow from the interposer to the ceramic core. The perforations occupy 20 percent of the plane area but are arranged in a pattern that does not degrade current delivery.

The 0.8-volt core logic planes are the most critical. They must deliver 700 amperes of current to the interposer with an IR drop of less than 50 millivolts. The resistance of the four planes in parallel is 0.1 milliohms per square, and the distance from the power connector to the farthest chiplet is 150mm. The IR drop from the connector to the far edge of the interposer is 10 millivolts at full current, leaving 40 millivolts for the interposer and chiplet power distribution.

The power is delivered to the blade through a single edge connector at the rear of the blade. The edge connector has 200 gold-plated contacts, each rated for 5 amperes. The 700 amperes of core logic current requires 140 contacts, the 200 amperes of Logic core current requires 40 contacts, and the remaining 20 contacts are used for the other voltages and for ground. The edge connector is keyed to prevent incorrect insertion.

The edge connector is mated to the rack backplane, which distributes power from the rack power distribution unit to all blades. The backplane has a 48-volt DC bus that carries power from the rack PDU to the blades. Each blade has a DC-DC converter that converts the 48 volts to the required voltages. The DC-DC converter is located on the blade near the edge connector, minimizing the length of the low-voltage high-current traces.

The DC-DC converter is a multi-phase synchronous buck converter with 16 phases. Each phase uses a pair of power MOSFETs and an inductor to convert 48 volts to 0.8 volts. The phases are interleaved to reduce the ripple current in the input and output capacitors. The converter operates at a switching frequency of 1 MHz, which is high enough to keep the inductors small but low enough to keep the switching losses manageable.

The input to the DC-DC converter is filtered by a bank of 100 microfarad ceramic capacitors. The capacitors are placed in parallel to reduce the equivalent series resistance and inductance. The input filter prevents the switching noise from the converter from propagating back to the rack backplane and disturbing other blades. The input filter also provides bulk energy storage for the converter during load transients.

The output of the DC-DC converter is filtered by a bank of 1,000 microfarad ceramic capacitors. The capacitors are placed close to the edge connector to minimize the inductance of the output traces. The output filter has a total capacitance of 10 millifarads, which is sufficient to hold the output voltage stable during current transients of 100 amps per microsecond.

The DC-DC converter is controlled by a dedicated microcontroller that monitors the output voltage and current. The microcontroller adjusts the duty cycle of the phases to maintain the output voltage at 0.8 volts plus or minus 1 percent. The microcontroller also monitors the temperature of the MOSFETs and the inductors, and shuts down the converter if the temperature exceeds 125 degrees Celsius.

The power distribution network includes decoupling capacitors at every level of the hierarchy. The motherboard substrate has 1,000 decoupling capacitors of 10 microfarads each, distributed across the area under the interposer. These capacitors filter high-frequency noise that could couple between the power planes and the signal traces. The capacitors are placed in vias that connect the power planes to the ground plane.

The interposer has its own decoupling capacitors. The interposer is manufactured on a 65nm process that includes metal-insulator-metal capacitors in the upper metal layers. The interposer has 10 microfarads of decoupling capacitance distributed across its area. The interposer also has deep trench capacitors that provide an additional 100 microfarads of capacitance with very low inductance.

Each chiplet has on-die decoupling capacitors. The Math cores have 100 nanofarads of decoupling capacitance per core, for a total of 3.2 microfarads per chiplet. The Logic cores have 50 nanofarads per core, for a total of 0.4 microfarads per chiplet. The System cores have 25 nanofarads per core, for a total of 0.1 microfarads per chiplet. The on-die capacitance is implemented as metal-insulator-metal capacitors in the upper metal layers.

The total decoupling capacitance on the blade is 10 millifarads from the motherboard capacitors, 100 microfarads from the interposer capacitors, 3.2 microfarads from the Math chiplets, 0.4 microfarads from the Logic chiplets, 0.1 microfarads from the System chiplets, and 10 millifarads from the DC-DC converter output filter. The total capacitance is 20 millifarads, which is sufficient to hold the voltage stable during the fastest current transients.

The power distribution network is modeled and simulated using a finite-element electromagnetic solver. The solver computes the resistance, inductance, and capacitance of every trace and via in the network. The simulation shows that the IR drop from the edge connector to the farthest chiplet is 40 millivolts, well within the 50-millivolt budget. The simulation also shows that the impedance of the network is less than 1 milliohm up to 10 MHz, and less than 10 milliohms up to 100 MHz.

The power distribution network is tested by injecting a current step and measuring the voltage droop. A test fixture injects a 100-ampere step with a rise time of 1 nanosecond into the power planes. An oscilloscope measures the voltage at the edge connector and at the far side of the interposer. The voltage droop at the far side is 50 millivolts, which decays to 10 millivolts within 1 microsecond. The 50-millivolt droop is acceptable because the chiplets can tolerate a 10 percent variation in supply voltage.

The power distribution network is the largest and heaviest component of the motherboard after the substrate itself. The copper planes weigh 500 grams, and the decoupling capacitors weigh 200 grams. The total weight of the power distribution network is 700 grams, which is 30 percent of the blade's total weight of 2.3 kilograms.

The power distribution network is also the most reliable component of the motherboard. The copper planes have no moving parts and no failure mechanisms. The decoupling capacitors have a lifetime of 10,000 hours at 105 degrees Celsius, which is 10 years at the blade's operating temperature of 60 degrees Celsius. The DC-DC converter has a lifetime of 100,000 hours, limited by the wear-out of the MOSFETs and the capacitors.

The power distribution network is the foundation upon which the entire PIP CISC platform is built. Without a clean, stable power supply, the 10,000 cores would not function correctly. The power distribution network is designed to deliver the required current with low noise and low loss, ensuring that the chiplets receive the power they need to operate at full speed.

This concludes Chapter 11 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Clock Distribution and Synchronization network, covering the phase-locked loops, the clock trees, and the synchronization of chiplets across the interposer.
# Chapter 12: Clock Distribution and Synchronization

The clock distribution network is the heartbeat of the PIP CISC platform. It delivers a synchronized clock signal to every sequential logic element on every chiplet, every HBM stack, every flash chip, and every optical transceiver. The network must distribute the clock with less than 10 picoseconds of skew across the entire 150mm by 150mm interposer, and less than 50 picoseconds of skew across the entire blade. The clock frequency is 2 GHz for the Math cores, 2.5 GHz for the Logic cores, 4 GHz for the System cores, and variable frequencies for the other components. The clock distribution network consumes 50 watts of power, which is 7 percent of the blade's total power budget.

The master clock for the blade is generated by a temperature-compensated crystal oscillator mounted on the substrate near the edge connector. The crystal oscillator produces a 100 MHz sine wave with a stability of plus or minus 10 parts per million over temperature. The 100 MHz signal is buffered and distributed to the phase-locked loops on each chiplet and each HBM stack. The crystal oscillator consumes 100 milliwatts of power and has a lifetime of 10 years.

The 100 MHz reference clock is distributed to the chiplets through a tree of differential buffers. The tree begins at the crystal oscillator and fans out to 1,000 Math chiplets, 256 Logic chiplets, and 40 System chiplets. The tree has 5 levels: level 0 drives 8 buffers, level 1 drives 64 buffers, level 2 drives 512 buffers, level 3 drives 4,096 buffers, and level 4 drives the 1,296 chiplets. The tree is implemented in the signal layers of the interposer, using 100-ohm differential pairs.

Each differential buffer is a current-mode logic amplifier that converts the differential input to a differential output with a gain of 10. The buffer has a propagation delay of 100 picoseconds and a jitter of 1 picosecond. The buffers are distributed across the interposer to minimize the length of the clock traces. The longest trace from the crystal oscillator to a chiplet is 200mm, which at the speed of light in silicon corresponds to a delay of 1 nanosecond.

Each chiplet has its own phase-locked loop that multiplies the 100 MHz reference to the core clock frequency. The Math core PLL multiplies by 20 to generate 2 GHz, the Logic core PLL multiplies by 25 to generate 2.5 GHz, and the System core PLL multiplies by 40 to generate 4 GHz. The PLLs are implemented as charge-pump PLLs with a voltage-controlled oscillator. The PLLs have a lock time of 100 microseconds and a jitter of 5 picoseconds.

The voltage-controlled oscillator in each PLL is a ring oscillator with 16 delay stages. The ring oscillator has a tuning range of 1 to 5 GHz, which covers the required frequencies. The control voltage for the ring oscillator is generated by a charge pump that compares the divided clock to the reference clock. The charge pump uses a 1 MHz loop filter to suppress high-frequency noise.

The PLLs also include a phase adjustment circuit that can advance or retard the clock by up to 50 picoseconds in 1-picosecond steps. The phase adjustment is controlled by the System cores, which measure the skew between chiplets using a dedicated skew measurement circuit. The System cores adjust the phase of each chiplet's clock to minimize the skew across the interposer.

The skew measurement circuit uses a time-to-digital converter that measures the time difference between the rising edges of two clocks. The time-to-digital converter is implemented as a delay line of 100 inverters, each with a delay of 1 picosecond. The time-to-digital converter has a resolution of 1 picosecond and a range of 100 picoseconds. The System cores use the time-to-digital converter to measure the skew between each pair of chiplets.

The measured skews are used to calculate the optimal phase adjustment for each chiplet. The System cores solve a linear programming problem that minimizes the maximum skew across all chiplets. The solution is a set of phase adjustments that bring all chiplets within 10 picoseconds of each other. The System cores program the phase adjustments into the PLLs, and the skew measurement is repeated to verify the result.

The clock distribution network within each chiplet is a tree of buffers that fans out the clock to all sequential elements. The Math core chiplet has 32 cores, each with 10,000 sequential elements, for a total of 320,000 sequential elements. The clock tree has 10 levels and consumes 100 milliwatts per chiplet, for a total of 100 watts for all Math chiplets. The clock tree is implemented in the upper metal layers of the chiplet, using thick wires to minimize resistance.

The Logic core chiplet has 8 cores, each with 20,000 sequential elements, for a total of 160,000 sequential elements. The clock tree has 8 levels and consumes 50 milliwatts per chiplet, for a total of 12.8 watts for all Logic chiplets. The System core chiplet has 4 cores, each with 30,000 sequential elements, for a total of 120,000 sequential elements. The clock tree has 8 levels and consumes 50 milliwatts per chiplet, for a total of 2 watts for all System chiplets.

The HBM stacks have their own clock distribution networks. Each HBM stack contains 8 DRAM dies, each with 10,000 sequential elements, for a total of 80,000 sequential elements per stack. The clock tree in the HBM stack has 8 levels and consumes 50 milliwatts per stack, for a total of 400 milliwatts for all 8 stacks. The HBM stacks receive their reference clock from the interposer and multiply it to 1.6 GHz using an internal PLL.

The NAND flash chips have simple clock distribution networks. Each flash chip has a ring oscillator that generates the internal clock for the state machine and the data path. The ring oscillator is not synchronized to the system clock; the flash chips are asynchronous. The flash chips communicate with the System cores using a source-synchronous interface where the data is accompanied by a strobe signal.

The optical transceivers have their own clock distribution networks. Each transceiver has a phase-locked loop that recovers the clock from the incoming data stream. The recovered clock is used to retime the data and to generate the transmit clock. The PLLs in the transceivers have a lock time of 1 microsecond and a jitter of 1 picosecond.

The clock distribution network is simulated using a transient simulation that models the propagation of the clock edges through the tree. The simulation includes the parasitics of the traces, the nonlinear behavior of the buffers, and the loading of the sequential elements. The simulation shows that the skew across the interposer is 8 picoseconds, well within the 10-picosecond budget. The simulation also shows that the jitter at the sequential elements is 10 picoseconds, which is acceptable for a 2 GHz clock.

The clock distribution network is tested by measuring the skew between chiplets using a dedicated test mode. The System cores put the blade into test mode, where each chiplet outputs its clock on a dedicated test pin. A high-speed oscilloscope measures the time difference between the test pins, and the System cores adjust the phase of each PLL to minimize the skew. The test takes 1 second per blade and is performed during manufacturing and after each power-on.

The clock distribution network is critical for the correct operation of the PIP CISC platform. If the skew between chiplets exceeds the setup time of the flip-flops, the data will be corrupted. The clock distribution network is designed to meet the skew requirement across all process corners and all temperatures, ensuring reliable operation for the life of the product.

The clock distribution network consumes 50 watts of power, which is significant but necessary. The power is dissipated in the buffers, the PLLs, and the clock trees. The power consumption is proportional to the clock frequency and the number of sequential elements, so future generations with higher frequencies will consume more power. The clock distribution network is optimized for low power by using low-swing differential signaling and by gating the clocks to idle chiplets.

The clock distribution network is the heartbeat of the PIP CISC platform. It synchronizes the operation of 10,000 Math cores, 2,048 Logic cores, 160 System cores, 64 gigabytes of HBM3e memory, 100 terabytes of NAND flash, and 12 optical transceivers. Without the clock distribution network, the chiplets would operate independently and the system would not function. The clock distribution network is the unsung hero of the PIP CISC platform.

This concludes Chapter 12 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Signal Integrity and EMI Mitigation techniques, covering the transmission line design, the crosstalk reduction, and the shielding of the optical transceivers.

# Chapter 13: Signal Integrity and EMI Mitigation

Signal integrity is the measure of how faithfully an electrical signal is transmitted from a driver to a receiver. In the PIP CISC platform, signals travel over distances of up to 200mm on the interposer and up to 500mm on the substrate, at data rates of up to 10.4 gigatransfers per second. At these speeds, the signals behave as waves, not as simple currents. The signal integrity engineer must consider reflection, crosstalk, attenuation, and dispersion, all of which can corrupt the signal and cause errors. The PIP CISC platform addresses these challenges through careful transmission line design, termination, shielding, and equalization.

The transmission lines on the interposer are microstrip and stripline structures. A microstrip is a trace on the top layer of the interposer with a ground plane below it. A stripline is a trace embedded between two ground planes in the middle layers. Both structures have a characteristic impedance determined by the trace width, the thickness of the dielectric, and the dielectric constant. The PIP CISC platform uses 50-ohm single-ended microstrips and 100-ohm differential striplines for all high-speed signals.

The characteristic impedance is controlled by adjusting the trace width and the dielectric thickness. The target impedance is 50 ohms for single-ended signals and 100 ohms for differential signals. The fabrication process can achieve plus or minus 5 percent tolerance on the trace width, resulting in an impedance tolerance of plus or minus 10 percent. This tolerance is acceptable for the PIP CISC platform because the drivers and receivers can tolerate a 10 percent impedance mismatch.

The reflection coefficient is the fraction of a signal that is reflected back when it encounters an impedance mismatch. A reflection coefficient of 0 means no reflection, and a reflection coefficient of 1 means total reflection. The PIP CISC platform requires a reflection coefficient of less than 0.1 for all high-speed signals, which corresponds to an impedance mismatch of less than 10 percent. This requirement is met by the fabrication tolerance of the transmission lines.

The termination of the transmission lines is critical for preventing reflections. The PIP CISC platform uses on-chip termination for all high-speed signals. The driver has a programmable output impedance that can be set to match the characteristic impedance of the transmission line. The receiver has a programmable input impedance that can be set to the same value. The termination is calibrated at power-on by measuring the impedance of a reference transmission line.

The crosstalk between adjacent transmission lines is another source of signal corruption. Crosstalk occurs when the electromagnetic field of one signal couples into an adjacent signal. The crosstalk is proportional to the mutual capacitance and mutual inductance between the traces. The PIP CISC platform reduces crosstalk by increasing the spacing between traces, by using differential signaling, and by placing ground traces between signals.

The spacing between traces is determined by the crosstalk requirement. The PIP CISC platform requires a crosstalk of less than -40 decibels, which means that the interfering signal is 100 times smaller than the desired signal. This requirement is met by spacing the traces at least 2 trace widths apart. For 1-micron wide traces, the spacing is 2 microns. For 0.5-micron wide traces, the spacing is 1 micron.

Differential signaling is inherently immune to crosstalk. In a differential pair, the two signals are equal and opposite. The crosstalk from an adjacent signal couples equally into both signals, so the difference between the signals is unchanged. The PIP CISC platform uses differential signaling for all high-speed signals that are not constrained by pin count, including the memory interface and the optical transceiver links.

Ground traces placed between signals provide additional isolation. A ground trace acts as a shield, absorbing the electromagnetic field from the adjacent signals. The ground trace is connected to the ground plane at regular intervals through vias. The vias are spaced at one-tenth of the wavelength, which for a 10 GHz signal is 3mm on the interposer. The ground traces are 0.5 microns wide and are placed between every pair of signal traces.

The attenuation of the signal as it travels along the transmission line is caused by the resistance of the copper trace and the loss of the dielectric. The copper loss is proportional to the square root of the frequency, because of the skin effect. At 10 GHz, the skin depth in copper is 0.6 microns, so the effective resistance of a 1-micron wide trace is 10 times the DC resistance. The dielectric loss is proportional to the frequency, because of the dipole relaxation in the dielectric. The PIP CISC platform uses a low-loss dielectric with a loss tangent of 0.01 at 10 GHz.

The total attenuation of a 200mm trace at 10 GHz is 10 decibels, which is acceptable for the PIP CISC platform. The drivers have a output swing of 1 volt, and the receivers have a sensitivity of 100 millivolts, so a 10 decibel loss is within the budget. The receivers also have equalizers that boost the high-frequency components of the signal, compensating for the attenuation.

The dispersion of the signal is caused by the frequency dependence of the propagation velocity. In a transmission line, the propagation velocity is determined by the dielectric constant, which varies with frequency. The variation in propagation velocity causes the different frequency components of a signal to arrive at different times, spreading the signal in time. The dispersion is measured in picoseconds per gigahertz per meter, and for the PIP CISC platform it is 1 picosecond per gigahertz per meter.

The dispersion for a 200mm trace at 10 GHz is 2 picoseconds, which is less than the rise time of the signal (50 picoseconds). The dispersion is therefore negligible for the PIP CISC platform. For longer traces or higher frequencies, the dispersion could become significant, and equalizers would be needed to compensate.

The equalizers in the receivers are adaptive finite-impulse response filters that boost the high-frequency components of the signal. The filter coefficients are adjusted by a least-mean-squares algorithm that minimizes the error between the received signal and a reference. The equalizer can compensate for up to 20 decibels of attenuation and 10 picoseconds of dispersion, which is sufficient for the PIP CISC platform.

The electromagnetic interference from the PIP CISC platform is a concern for the other equipment in the rack. The high-speed signals on the interposer and the substrate radiate electromagnetic waves that can interfere with the operation of other blades. The PIP CISC platform includes several features to reduce EMI: the ground planes provide shielding, the differential signaling cancels the radiation, and the optical transceivers do not radiate at all.

The ground planes in the substrate and the interposer act as shields that contain the electromagnetic fields. The fields from a microstrip trace are confined between the trace and the ground plane. The fields from a stripline trace are confined between the two ground planes. The ground planes are connected together by vias at regular intervals, forming a Faraday cage that prevents radiation from escaping.

The differential signaling cancels the radiation because the fields from the two signals are equal and opposite. The net field at a distance from the pair is the difference between the fields, which is small. The cancellation is perfect if the two signals are perfectly balanced, but in practice there is some imbalance. The imbalance is less than 1 percent, so the cancellation is 40 decibels.

The optical transceivers do not radiate at all because they use light instead of electricity. The light is confined to the optical fiber, which is surrounded by a cladding that prevents the light from escaping. The only radiation from the optical transceivers is the 60 Hz hum from the power supply, which is negligible.

The EMI from the PIP CISC platform is measured in a certified laboratory. The blade is placed in an anechoic chamber, and an antenna measures the radiated power at frequencies from 30 MHz to 40 GHz. The measured radiation is below the FCC Class A limit for industrial equipment by 10 decibels, and below the Class B limit for residential equipment by 3 decibels. The PIP CISC platform is therefore compliant with all applicable EMI regulations.

The signal integrity of the PIP CISC platform is verified by bit error rate testing. A test pattern generator sends a pseudorandom bit sequence through a signal path, and a receiver counts the number of errors. The bit error rate is the number of errors divided by the number of bits. The PIP CISC platform requires a bit error rate of less than 10^-15, which is one error per 10^15 bits. At 10.4 gigabits per second, this is one error per 100,000 seconds, or about one error per day.

The bit error rate test is performed on every signal path during manufacturing. The test takes 1 second per path, and there are 100,000 signal paths on a blade, so the total test time is 100,000 seconds, or 28 hours. The test is performed in parallel on multiple blades to reduce the time per blade. The test is also performed after the blade is installed in the rack, as part of the system bring-up.

The eye diagram is a graphical representation of the signal quality. An oscilloscope captures many cycles of the signal and overlays them on top of each other. The resulting image looks like an eye, with the eye opening representing the time and voltage margins. A healthy signal has a wide eye opening, while a marginal signal has a narrow eye opening. The PIP CISC platform requires an eye opening of at least 50 percent of the unit interval and 50 percent of the voltage swing.

The eye diagram for the PIP CISC platform is measured during manufacturing and during system bring-up. The eye opening is typically 80 percent of the unit interval and 80 percent of the voltage swing, indicating excellent signal quality. The margin is sufficient to absorb variations in temperature, voltage, and process.

The signal integrity of the PIP CISC platform is the result of careful design and rigorous testing. The transmission lines are designed to have the correct impedance, the termination is matched, the crosstalk is minimized, and the equalizers compensate for the attenuation. The EMI is reduced by shielding, differential signaling, and optical fibers. The result is a platform that can reliably transmit 10.4 gigabits per second over distances of 200mm, with a bit error rate of less than 10^-15.

The signal integrity of the PIP CISC platform is also affected by the power distribution network. The noise on the power supply couples into the signal through the driver and receiver circuits. The power distribution network is designed to have a low impedance at high frequencies, so the supply noise is small. The supply noise is less than 10 millivolts peak-to-peak, which is 1 percent of the signal swing.

The signal integrity of the PIP CISC platform is also affected by the clock distribution network. The jitter on the clock is transferred to the data through the sampling process. The clock jitter is 10 picoseconds, which is 1 percent of the unit interval at 10.4 gigabits per second (96 picoseconds). The jitter is small enough that it does not significantly affect the bit error rate.

The signal integrity of the PIP CISC platform is also affected by the temperature. The propagation velocity of the transmission line changes with temperature, because the dielectric constant changes. The change is 0.1 percent per degree Celsius, so a 60 degree Celsius temperature change causes a 6 percent change in propagation delay. The skew between signals can change by 60 picoseconds over a 200mm trace, which is acceptable because the skew budget is 100 picoseconds.

The signal integrity of the PIP CISC platform is also affected by the aging of the materials. The dielectric constant of the interposer changes over time as the material absorbs moisture and as the polymer chains relax. The change is 1 percent over 10 years, which is acceptable. The copper traces oxidize over time, increasing the resistance. The increase is 10 percent over 10 years, which is also acceptable.

The signal integrity of the PIP CISC platform is a testament to the expertise of the design team. The team has decades of experience in high-speed digital design, and they have applied that experience to the PIP CISC platform. The result is a platform that can reliably transmit data at 10.4 gigabits per second, over distances of 200mm, with a bit error rate of less than 10^-15.

The signal integrity of the PIP CISC platform is also a testament to the manufacturing capability of TSMC. The interposer traces have a width tolerance of plus or minus 0.1 microns, which is essential for controlling the impedance. The vias have a diameter tolerance of plus or minus 0.5 microns, which is essential for controlling the reflection. The dielectric thickness has a tolerance of plus or minus 0.5 microns, which is essential for controlling the propagation velocity.

The signal integrity of the PIP CISC platform is the foundation upon which the entire system is built. Without reliable signal transmission, the 10,000 cores would not be able to communicate with each other, and the system would not function. The signal integrity is ensured by the careful design of the transmission lines, the termination, the shielding, and the equalization. The result is a platform that is both fast and reliable.

The signal integrity of the PIP CISC platform is also a key enabler of the optical interconnects. The electrical signals from the PIP-Fabric are converted to optical signals by the transceivers, transmitted over the fiber, and converted back to electrical signals at the other end. The quality of the electrical signals determines the quality of the optical signals, so the signal integrity of the electrical domain directly affects the performance of the optical domain.

The signal integrity of the PIP CISC platform is continuously monitored by the System cores. The System cores measure the bit error rate of each link and adjust the equalizer coefficients to compensate for changes in temperature, voltage, and aging. The System cores also monitor the eye opening and report any degradation to the management controller. The management controller can then schedule maintenance before the link fails.

The signal integrity of the PIP CISC platform is the result of a holistic approach that considers the entire system. The design of the chiplets, the interposer, the substrate, and the optical transceivers is coordinated to ensure that the signals are transmitted reliably. The manufacturing process is controlled to ensure that the physical parameters are within the required tolerances. The testing is rigorous to ensure that any defects are caught before the product is shipped.

The signal integrity of the PIP CISC platform is a competitive advantage. No other platform can transmit 10.4 gigabits per second over 200mm with a bit error rate of 10^-15. This capability allows the PIP CISC platform to scale to 1,000 blades in a single shared-memory system, something that is impossible with traditional electrical interconnects. The signal integrity of the PIP CISC platform is the key to its scalability.

The signal integrity of the PIP CISC platform is also a source of pride for the design team. They have created a platform that is both fast and reliable, and they have done so within the constraints of cost, power, and area. The signal integrity of the PIP CISC platform is a testament to their skill and dedication.

The signal integrity of the PIP CISC platform is the unsung hero of the system. The user never sees it, and the programmer never thinks about it. But without it, the system would not work. The signal integrity is the invisible foundation upon which the entire PIP CISC platform is built.

This concludes Chapter 13 of the Motherboard Design & Manufacturing Specification. The remaining chapters will cover the PIP-Fabric Crossbar Switch Design, the Directory Cache Coherency Logic, the Address Translation and Segment Walk Hardware, and the remaining topics listed in the chapter index.

# Chapter 14: PIP-Fabric Crossbar Switch Design

The PIP-Fabric crossbar switch is the central communication hub of the PIP CISC platform. It connects every core, every memory stack, every flash chip, and every optical transceiver to every other component on the blade. The crossbar has 128 input ports and 128 output ports, each 512 bits wide, operating at 2 GHz. The total switching capacity is 131 terabits per second, sufficient to handle the bandwidth demands of ten thousand Math cores simultaneously. The crossbar is implemented in the silicon interposer, using the top five metal layers for the switch matrix and the control logic.

The crossbar is organized as a 128x128 matrix of crosspoints. Each crosspoint is a transmission gate that connects an input port to an output port when enabled. The transmission gate is implemented as a pair of transistors: an NMOS and a PMOS in parallel. The transmission gate has a resistance of 100 ohms when on, and an infinite resistance when off. The crosspoint also includes a buffer that regenerates the signal, compensating for the attenuation of the transmission gate.

The crossbar uses a centralized arbitration scheme. A central arbiter receives requests from all input ports and grants access to the output ports. The arbiter uses a round-robin algorithm that ensures fairness among the input ports. The arbiter can grant up to 128 simultaneous transfers, one per output port. The arbitration takes 1 cycle, so the crossbar has a latency of 2 cycles: one for arbitration and one for the data transfer.

The input ports have queues that hold data while they wait for arbitration. Each input port has a 16-entry queue, each entry 512 bits wide. The queue is implemented as a FIFO memory with 16 words of 512 bits. The queue can hold up to 16 packets, which is sufficient to cover the arbitration latency. The queue also provides backpressure to the transmitting component when it is full.

The output ports have queues that hold data while they wait to be transmitted. Each output port has a 16-entry queue, identical to the input queues. The output queue is necessary because multiple input ports may send data to the same output port in consecutive cycles. The output queue smoothes the traffic, preventing the loss of data.

The crossbar also supports multicast and broadcast operations. A multicast operation sends a packet from one input port to multiple output ports. The central arbiter replicates the packet and sends it to all the requested output ports. A broadcast operation sends a packet from one input port to all output ports. The broadcast is implemented as a multicast with all output ports selected.

The crossbar includes error detection and correction circuitry. Each packet has a 32-bit cyclic redundancy check code appended to the end. The CRC code is computed by the transmitting component and checked by the receiving component. If the CRC check fails, the receiving component sends a negative acknowledgment to the transmitting component, which retransmits the packet. The retransmission is handled by the hardware, transparent to the software.

The crossbar also includes a performance monitoring unit that counts the number of packets sent, the number of packets received, the number of CRC errors, and the number of retransmissions. The performance counters are accessible to the System cores through a dedicated management interface. The System cores use the counters to detect congestion and to balance the traffic across the crossbar.

The crossbar is implemented in the silicon interposer using 65nm CMOS technology. The 128x128 matrix of crosspoints contains 16,384 transmission gates. Each transmission gate has an area of 100 square microns, for a total area of 1.6 square millimeters. The control logic for the arbiter and the queues occupies an additional 0.4 square millimeters, for a total area of 2 square millimeters. The crossbar is a small fraction of the interposer area.

The crossbar consumes 10 watts of power. The power is dissipated in the transmission gates, the buffers, and the control logic. The transmission gates dissipate power when they are on, because they have resistance. The buffers dissipate power when they switch, because they charge and discharge the capacitance of the output traces. The control logic dissipates power because it switches at 2 GHz.

The crossbar is designed for low latency and high throughput. The latency is 2 cycles (1 nanosecond), which is negligible compared to the memory access time. The throughput is 131 terabits per second, which is sufficient for the peak bandwidth of the Math cores. The crossbar is not a bottleneck for the PIP CISC platform.

The crossbar is tested during manufacturing by a built-in self-test. The self-test sends packets from every input port to every output port and verifies that they are received correctly. The self-test also tests the multicast and broadcast operations. The self-test takes 1 second and detects any defects in the crossbar.

The crossbar is the heart of the PIP-Fabric. It enables the tight coupling of the 10,000 cores, the 64 gigabytes of memory, the 100 terabytes of flash, and the 9.6 terabits per second of optical bandwidth. Without the crossbar, the components would be isolated and the system would not function. The crossbar is the unsung hero of the PIP CISC platform.

This concludes Chapter 14 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Directory Cache Coherency Logic, which maintains a consistent view of memory across all cores and blades. The directory is essential for the shared-memory programming model of the PIP CISC platform.

# Chapter 14: Directory Cache Coherency Logic

The directory cache coherency logic is the traffic cop of the PIP CISC platform. It ensures that every core on every blade sees a consistent view of memory, even when multiple cores are reading and writing the same locations simultaneously. Without coherency, one core might read stale data that another core has updated, leading to incorrect results. The directory protocol tracks the location of each cache line and the state of each copy, allowing the hardware to invalidate stale copies before a write occurs. The directory is implemented in the silicon interposer, using dedicated logic and memory arrays.

The directory is organized as a sparse directory, meaning that it only tracks cache lines that are currently in use. The directory has 1 million entries, enough to track 1 million cache lines. Each cache line is 64 bytes, so the directory can track 64 megabytes of cached data. This is sufficient for the 64 megabytes of L3 cache on the blade. The directory entry for a cache line contains the physical address, the state, and a vector of sharers.

The physical address is 64 bits, which is enough to address the entire memory space of the blade. The state is 3 bits, encoding the coherence state of the cache line. The vector of sharers is 128 bits, one bit per core on the blade. The vector indicates which cores have a copy of the cache line. A 128-bit vector is sufficient for the 10,000 Math cores, 2,048 Logic cores, and 160 System cores on a blade.

The coherence states are MESI: Modified, Exclusive, Shared, and Invalid. The Modified state means that the cache line is present in exactly one cache and has been modified. The Exclusive state means that the cache line is present in exactly one cache and has not been modified. The Shared state means that the cache line is present in multiple caches and has not been modified. The Invalid state means that the cache line is not present in any cache.

The directory also tracks the location of cache lines that are on other blades. For remote cache lines, the directory entry contains the blade identifier instead of the vector of sharers. The blade identifier is 12 bits, enough to address 4,096 blades. The directory also contains a flag indicating whether the cache line is local or remote. The remote entries are stored in a separate table with 64,000 entries.

The directory protocol is implemented as a finite-state machine. The state machine receives requests from the cores and from the optical fabric, and it sends commands to the cores and to the optical fabric. The state machine has 16 states, corresponding to the combinations of the MESI states and the pending operations. The state machine is implemented in logic gates, not in microcode, for speed.

The directory also includes a directory cache that stores recently used directory entries. The directory cache has 64,000 entries, enough to cover the 64 megabytes of L3 cache. The directory cache is implemented as a 16-way set-associative SRAM with a 64-byte cache line. The directory cache reduces the latency of directory lookups from 10 cycles to 2 cycles, which is critical for performance.

The directory is designed for low latency. A directory lookup takes 2 cycles when the entry is in the directory cache, and 10 cycles when the entry is not in the cache. The directory update takes 1 cycle after the lookup. The total latency for a coherence operation is 3 to 11 cycles, which is acceptable for a 2 GHz processor.

The directory is also designed for high throughput. The directory can process 1,000 coherence operations per cycle, which is sufficient for the peak bandwidth of the Math cores. The directory is pipelined, so it can start a new operation every cycle. The pipeline has 4 stages: request, lookup, update, and response.

The directory is integrated with the crossbar switch. When a core sends a request to the memory controller, the request is intercepted by the directory. The directory checks the coherence state of the cache line and determines whether the request can proceed. If the request can proceed, the directory forwards the request to the memory controller. If the request cannot proceed, the directory sends a message to the cores that have copies of the cache line, ordering them to invalidate or write back their copies.

The directory also handles remote requests from other blades. When a remote blade sends a request, the request is received by the optical transceiver and forwarded to the directory. The directory processes the request as if it came from a local core, but the response is sent back over the optical fabric. The remote request adds 5 microseconds of latency for the optical round trip.

The directory is the most complex logic in the interposer. It contains 10 million logic gates and 100 million bits of SRAM. The directory occupies 10 square millimeters of the interposer area, which is 5 percent of the total area. The directory consumes 5 watts of power, which is 1 percent of the blade's power budget.

The directory is designed for correctness and performance. The state machine is formally verified to ensure that it implements the MESI protocol correctly. The directory cache is tuned to have a hit rate of 99 percent, which is sufficient for the working set of the applications. The directory is the unsung hero of the PIP CISC platform.

The directory is also designed for scalability. The directory can be extended to track 4,096 blades by adding more entries to the remote table. The remote table has 64,000 entries, which is enough for 64,000 remote cache lines. This is sufficient for the coherence traffic between 4,096 blades, because the remote working set is limited by the optical bandwidth.

The directory is also designed for fault tolerance. The directory entries are protected by error-correcting codes that can correct single-bit errors and detect double-bit errors. If an uncorrectable error is detected, the directory entry is marked as invalid and the cache line is flushed from all caches. The error is reported to the System cores, which can take corrective action.

The directory is tested during manufacturing by a built-in self-test. The self-test exercises all states of the state machine and all entries of the directory cache. The self-test also injects errors to test the error-correcting codes. The self-test takes 1 second and detects any defects in the directory.

The directory is the key to the shared-memory programming model of the PIP CISC platform. It allows the programmer to write parallel code without worrying about where the data is located or which core is accessing it. The directory automatically keeps the caches coherent, ensuring that the program sees a consistent view of memory.

The directory also enables the scaling of the PIP CISC platform to thousands of blades. The directory tracks the location of cache lines across blades, allowing the hardware to maintain coherence across the optical fabric. The programmer does not need to use message passing or other explicit communication mechanisms; the hardware handles everything.

The directory is a masterpiece of computer architecture. It implements the MESI protocol in hardware, with low latency and high throughput. It scales to thousands of blades and terabytes of memory. It is transparent to the programmer and to the compiler. The directory is the unsung hero of the PIP CISC platform.

The directory works in concert with the crossbar switch. The crossbar provides the communication paths, and the directory controls the traffic. Together, they form the PIP-Fabric, the backbone of the PIP CISC platform. The PIP-Fabric is what makes the platform unique; no other system has a fabric that can connect thousands of cores and terabytes of memory with low latency and high bandwidth.

The directory is also aware of the memory hierarchy. The directory knows which cache lines are in the L1 caches, which are in the L2 caches, and which are in the L3 cache. The directory uses this information to optimize the coherence operations. For example, if a cache line is only in the L3 cache, the directory can service a read request from the L3 cache without involving the core caches.

The directory also includes a prediction mechanism that anticipates future coherence operations. The predictor uses the history of past operations to guess which cache lines will be needed next. The predictor can prefetch cache lines into the directory cache, reducing the latency of future lookups. The predictor is implemented as a neural network with 1,000 neurons, which is trained by the hardware.

The predictor is a novel feature of the PIP CISC platform. Traditional directory protocols do not include prediction; they react to requests as they arrive. The predictor allows the directory to anticipate requests and to prepare the coherence state in advance. The predictor reduces the average latency of a directory lookup from 2 cycles to 1.5 cycles, a 25 percent improvement.

The predictor is also used for power management. The predictor can detect when a cache line is unlikely to be accessed again, and it can instruct the directory to evict the line from the directory cache. The eviction frees up space for other cache lines and reduces the power consumption of the directory cache.

The predictor is implemented in the same logic as the directory. The predictor uses the same SRAM arrays as the directory cache, but with different read and write ports. The predictor is trained on the fly, using the actual coherence operations as training data. The predictor adapts to the workload, improving its accuracy over time.

The directory is a critical component of the PIP CISC platform. It is responsible for maintaining the illusion of a single shared memory, even as the system scales to thousands of blades and millions of cores. The directory is the reason that the PIP CISC platform can support a shared-memory programming model, while other large-scale systems require explicit message passing.

The directory is also a source of performance. By tracking the location of cache lines, the directory can service requests from the local cache, avoiding the need to go to memory. The directory can also forward requests to the core that has the data, avoiding the need to write back and then read. These optimizations reduce the latency and bandwidth consumption of memory operations.

The directory is also a source of power consumption. The directory cache consumes 5 watts, which is 1 percent of the blade's power budget. The predictor consumes an additional 1 watt. The directory is a small but significant contributor to the overall power consumption of the PIP CISC platform.

The directory is designed to be scalable to future generations of the PIP CISC platform. The directory can be extended to track 4,096 blades by adding more entries to the remote table. The directory can also be extended to track larger caches by adding more entries to the directory cache. The directory is implemented in the interposer, which can be scaled to larger sizes as the interposer technology improves.

The directory is a key differentiator of the PIP CISC platform. No other system has a directory that can track 1 million cache lines and 4,096 blades with low latency and high throughput. The directory is the result of years of research and development, and it is protected by dozens of patents.

The directory is a testament to the skill of the architecture team. They have created a directory protocol that is both correct and efficient, and they have implemented it in a way that is scalable and power-efficient. The directory is a work of art, as elegant as it is functional.

The directory is also a testament to the manufacturing capability of TSMC. The directory requires dense SRAM arrays and fast logic gates, both of which are provided by TSMC's 65nm process. The directory also requires precise timing, which is enabled by TSMC's process control. Without TSMC, the directory could not be built.

The directory is the heart of the PIP-Fabric. It beats at 2 GHz, coordinating the activities of 10,000 cores. It is invisible to the programmer, but it is essential for the operation of the system. The directory is the unsung hero of the PIP CISC platform.

The directory is also a source of reliability. The error-correcting codes in the directory cache protect against soft errors caused by cosmic rays. The directory state machine is designed to be resilient to transient faults, with redundant state bits and voting logic. The directory can detect and correct most faults, ensuring that the system continues to operate correctly.

The directory is also a source of security. The directory enforces the memory protection rules of the segment tree. If a core attempts to access a cache line that it does not have permission to access, the directory will block the access and raise an exception. The directory is the first line of defense against buffer overflows and other memory attacks.

The directory is a complex piece of hardware, but it is well understood by the design team. The team has simulated the directory at the RTL, gate, and transistor levels, verifying that it meets the performance, power, and reliability requirements. The team has also built a prototype of the directory in a field-programmable gate array, and they have tested it with real software. The prototype has been running for six months without a single coherence error.

The directory is ready for production. The design has been reviewed by independent experts, and it has passed all design reviews. The layout has been checked for design rule violations, and it has passed all physical verification. The directory is ready to be taped out and manufactured.

The directory is the culmination of a decade of research. The architects have studied the coherence protocols of the past and have learned from their mistakes. They have incorporated the best ideas from academia and industry, and they have added their own innovations. The directory is a state-of-the-art design that will serve as the foundation for the PIP CISC platform for years to come.

The directory is also a platform for future innovation. The architects have left room in the design for new features, such as support for transactional memory and for hardware-assisted debugging. The directory can be extended without changing the core protocol, allowing the PIP CISC platform to evolve over time.

The directory is the brain of the PIP-Fabric. It makes the decisions that keep the system coherent. It is the traffic cop that directs the flow of data. The directory is the most important component of the interposer, and it is the key to the success of the PIP CISC platform.

The directory is also the most challenging component to design. The architects had to balance competing requirements: performance vs. power, scalability vs. area, correctness vs. complexity. They had to make trade-offs that would satisfy all stakeholders. The final design is a compromise, but it is a good compromise.

The directory is a credit to the PIP CISC project. It demonstrates that the team has the technical expertise to design a world-class coherence protocol. It also demonstrates that the team has the discipline to implement that protocol in a way that is manufacturable and reliable. The directory is a testament to the team's skill and dedication.

The directory is the unsung hero of the PIP CISC platform. It works silently in the background, keeping the caches coherent. It never complains, it never asks for recognition. It just does its job, day after day, year after year. The directory is the epitome of the reliable component.

The directory is the subject of this chapter. We have described its organization, its protocol, its performance, its power, its reliability, its security, and its scalability. We have explained how it works and why it is important. We have given the reader a deep understanding of the directory, so that they can appreciate the complexity and elegance of the PIP CISC platform.

The directory is the last component we will describe in detail. The remaining components are either less complex or less critical. The directory is the capstone of the PIP CISC platform, the component that ties everything together. The directory is the reason that the PIP CISC platform can scale to thousands of blades and millions of cores. The directory is the future of computing.

# Chapter 15: Address Translation and Segment Walk Hardware

The address translation and segment walk hardware is the memory management unit of the PIP CISC platform. It translates virtual addresses used by software into physical addresses used by the memory system, while also checking permissions and enforcing protection. Unlike traditional processors that use page tables, the PIP CISC platform uses a segment tree, a hierarchical structure that maps virtual addresses to physical memory regions with arbitrary granularity. The segment walk hardware is implemented in the System cores, with a dedicated accelerator that traverses the segment tree in hardware.

The segment tree is a hierarchical data structure stored in a reserved region of physical memory. The root of the tree is a segment descriptor stored in a dedicated register that can only be written by the highest privilege level. The root descriptor points to a segment table, which is an array of segment descriptors. Each segment descriptor contains the base address, size, owner, permissions, and a pointer to the next level of the tree. The tree can have up to 6 levels, allowing the addressing of up to 2^60 bytes of virtual address space.

The segment descriptor is 128 bits wide and has the following fields. The type field occupies bits 0 through 3 and indicates the type of segment: data, code, page table, capability, remote, or I/O. The size field occupies bits 4 through 11 and encodes the segment size as a power of two from 2^12 (4KB) to 2^60 (1 exabyte). The base address field occupies bits 12 through 75 and provides 64 bits of physical address. The owner field occupies bits 76 through 107 and provides 32 bits of owner identifier. The permission field occupies bits 108 through 115 and encodes read, write, execute, create child, delegate, and seal permissions. The child pointer field occupies bits 116 through 127 and indexes into the segment table to locate the first child segment of this node.

The segment table is a hardware-managed structure stored in a reserved region of physical memory. The table contains up to 4,096 entries, each 128 bits wide. The root segment occupies entry zero and is initialized during system boot. The segment table is cached in a dedicated hardware translation lookaside buffer with 128 entries. Each TLB entry caches a complete segment descriptor and is tagged with the owner identifier of the process that performed the translation.

The address translation hardware walks the segment tree when a TLB miss occurs. The walk begins at the root segment descriptor. The hardware extracts the appropriate number of bits from the virtual address to index into the segment table. The number of bits per level is determined by the size of the segment table at that level. For a 4,096-entry table, 12 bits are used. The hardware loads the segment descriptor from the table, checks the permissions, and then proceeds to the next level. The walk continues until a leaf segment is reached.

The segment walk hardware is implemented as a finite-state machine. The state machine has 12 states: root, level1, level2, level3, level4, level5, leaf, fault, and the corresponding wait states for memory accesses. The state machine is clocked at 2 GHz, the same frequency as the System cores. Each level of the walk takes 1 cycle to compute the index and 1 cycle to wait for the memory access, for a total of 2 cycles per level. A 6-level walk takes 12 cycles.

The segment walk hardware includes a dedicated cache for segment descriptors. The segment descriptor cache has 128 entries and is fully associative. The cache is tagged with the virtual address and the owner identifier. The cache reduces the latency of a TLB miss from 12 cycles to 2 cycles when the descriptor is in the cache. The hit rate of the cache is 95 percent for typical workloads, so the average TLB miss latency is 2.5 cycles.

The segment walk hardware also checks permissions at each level of the walk. The permission check verifies that the current owner has the required access rights for the segment. The current owner is stored in a dedicated register that is updated on every context switch. The permission check also verifies that the segment has not been sealed. If any check fails, the hardware raises a protection fault and traps to the operating system.

The segment walk hardware is integrated with the TLB. When a walk completes, the hardware loads the leaf segment descriptor into the TLB. The TLB entry is tagged with the virtual page number and the owner identifier. The TLB also stores the permissions and the physical page number. The TLB can be invalidated by the operating system when the segment tree is modified.

The segment walk hardware also supports superpages. A superpage is a large page that is mapped by a single segment descriptor. For example, a 1GB superpage can be mapped by a segment descriptor with a size of 1GB. The segment walk hardware detects superpages by checking the size field of the segment descriptor. If the size field indicates a page larger than the current level, the walk terminates early, and the remaining bits of the virtual address are used as the offset within the superpage.

The segment walk hardware is designed for low latency and high throughput. The latency is 12 cycles for a full walk, which is acceptable for a TLB miss. The throughput is one walk per cycle, because the state machine is pipelined. The pipeline has 6 stages, one for each level of the walk. The pipeline can process multiple walks in parallel, as long as they do not conflict for the same memory resources.

The segment walk hardware also includes a performance monitor that counts the number of walks, the number of cache hits, the number of cache misses, and the number of protection faults. The performance counters are accessible to the operating system through a dedicated management interface. The operating system uses the counters to tune the segment tree and to detect abnormal behavior.

The segment walk hardware is tested during manufacturing by a built-in self-test. The self-test creates a segment tree in memory and then walks the tree using random virtual addresses. The self-test verifies that the hardware returns the correct physical addresses and permissions. The self-test takes 1 second and detects any defects in the segment walk hardware.

The address translation and segment walk hardware is the key to the protection model of the PIP CISC platform. It enforces the capability-based security that isolates processes and virtual machines from each other. It also enables the efficient implementation of shared memory and inter-process communication.

This concludes Chapter 15 of the Motherboard Design & Manufacturing Specification. The final chapters will cover the remaining topics: the Hybrid Bonding Assembly Process, the Through-Silicon Via Fabrication, the Reflow Soldering and Surface Mount Technology, the Mechanical Enclosure and Rack Integration, the Power-On Self-Test and Built-In Self-Test, the Manufacturing Test Flows and Fault Coverage, the Reliability, Burn-In, and Stress Testing, the Desktop Workstation Form Factor, the Professional Workstation Form Factor, the Blade Server Form Factor, the Storage-Only Blade Configuration, the Rack Backplane and Optical Waveguide Design, the Multi-Rack Fabric Extension, the Bill of Materials and Component Sourcing, the Assembly Sequence and Process Control, the Quality Assurance and Yield Management, the Firmware Boot ROM and Initialization Microcode, the Debugging and Diagnostic Interfaces, the Field Upgrade and Repair Procedures, the Environmental Compliance and Certification, the Security Features and Tamper Resistance, the Performance Characterization and Benchmarks, the Design Rules and Layout Guidelines for Partners, and the Future Scalability and Next-Generation Roadmap.

# Chapter 16: Hybrid Bonding Assembly Process

The hybrid bonding assembly process is the most critical manufacturing step for the PIP CISC platform. It attaches the 1,296 chiplets—1,000 Math cores, 256 Logic cores, and 40 System cores—to the silicon interposer with 9-micron pitch connections. Hybrid bonding differs from traditional solder bump bonding in that it creates a direct copper-to-copper connection between the chiplet and the interposer, without any intervening solder. The result is a connection that has 10 times lower resistance, 10 times lower capacitance, and 100 times higher density than solder bumps. The hybrid bonding process is performed at TSMC's advanced packaging facility in Hsinchu.

The hybrid bonding process begins with the preparation of the chiplet surfaces. The chiplets are manufactured on 300mm wafers at TSMC's Fab 18. After the final metal layer is deposited, a layer of silicon dioxide is deposited on top of the metal. The silicon dioxide is then polished by chemical mechanical polishing to a flatness of 1 nanometer. The polishing removes the topography of the metal layers, creating a perfectly flat surface for bonding.

The bonding pads are then etched into the silicon dioxide. A photoresist mask is patterned with 5-micron diameter holes at 9-micron pitch. The holes are etched through the silicon dioxide using a reactive ion etching process with a fluorocarbon plasma. The etching stops on the top metal layer of the chiplet, exposing the copper pads. The etching process creates holes that are 5 microns in diameter and 1 micron deep.

The exposed copper pads are cleaned to remove any native oxide. The cleaning process uses a dilute solution of citric acid that dissolves the copper oxide without attacking the underlying copper. The citric acid is applied by a spin coater, then rinsed with deionized water. The cleaning is followed by a plasma treatment with hydrogen gas that reduces any remaining oxide. The treated copper pads are pure copper, ready for bonding.

The interposer is prepared in the same way as the chiplets. The interposer wafer has bonding pads on both the front side (for the chiplets) and the back side (for the substrate). The front side pads are 5 microns in diameter at 9-micron pitch, matching the chiplets. The back side pads are 50 microns in diameter at 100-micron pitch, matching the substrate. Both sides are planarized and cleaned using the same processes as the chiplets.

The chiplets are aligned to the interposer using a wafer-to-wafer bonder. The bonder has a camera system that locates alignment marks on the chiplet wafer and on the interposer wafer. The alignment marks are etched into the silicon at the corners of each chiplet. The bonder moves the chiplet wafer until the alignment marks are within 0.5 microns of the interposer marks. The alignment is performed at room temperature to prevent thermal expansion from distorting the alignment.

The wafers are then brought into contact. The bonder lowers the chiplet wafer onto the interposer wafer until the silicon dioxide surfaces touch. The silicon dioxide surfaces are hydrophilic, meaning they attract each other through hydrogen bonding. The attraction is strong enough to hold the wafers together without any external force. The wafers are aligned to within 0.5 microns, which is sufficient for the 9-micron pitch.

The wafers are then annealed at 400 degrees Celsius for 1 hour. The annealing causes the copper pads to expand and to diffuse into each other. The copper atoms migrate across the interface, forming a continuous copper connection. The silicon dioxide surfaces also bond together, forming a strong mechanical bond. The annealing is performed in a forming gas atmosphere (95 percent nitrogen, 5 percent hydrogen) to prevent oxidation of the copper.

The bonded wafer stack is then thinned from the back side. The chiplet wafer is ground from 775 microns to 100 microns using a diamond grinder. The grinding is followed by chemical mechanical polishing to remove the damage layer and to create a smooth surface. The thinning exposes the through-silicon vias that connect the chiplets to the interposer.

The back side of the chiplet wafer is then patterned with redistribution layers. The redistribution layers route the signals from the chiplet vias to the hybrid bonding pads on the interposer. The redistribution layers are deposited using the same dual-damascene process used for the interposer. The redistribution layers have 2 metal layers, each 1 micron thick.

The bonded wafer stack is then diced into individual blades. A diamond blade saw cuts through the chiplet wafer, the interposer, and the substrate wafer simultaneously. The blade is 50 microns thick and rotates at 30,000 revolutions per minute. The dicing process separates the wafer stack into individual blades, each measuring 200mm by 500mm.

The hybrid bonding process is inspected by scanning acoustic microscopy. The inspection uses high-frequency ultrasound to detect voids in the bonded interface. A void appears as a bright spot in the acoustic image because the ultrasound reflects off the air-solid interface. The inspection can detect voids as small as 1 micron in diameter. The acceptance criterion is fewer than 10 voids per square millimeter.

The hybrid bonding process is also inspected by cross-sectioning. A sample blade is cut in half, and the cut surface is polished and etched. The etched surface is examined under a scanning electron microscope. The microscope reveals the copper-to-copper connection and the silicon dioxide-to-silicon dioxide bond. The connection should be continuous, with no gaps or voids.

The hybrid bonding process has a yield of 95 percent per connection. The 1,296 chiplets have a total of 1.3 million connections (1,296 chiplets times 1,000 pads per chiplet). The overall yield is 0.95^1,300,000, which is effectively zero. To achieve a reasonable overall yield, the hybrid bonding process must be defect-free, or the design must include redundancy. The PIP CISC platform includes redundancy: each chiplet has 10 percent spare pads that can be used to replace defective pads. The redundancy improves the yield to 90 percent per blade.

The hybrid bonding process is the most expensive step in the assembly of the PIP CISC platform. The bonder costs $10 million, and each blade takes 10 minutes to bond. The cost per blade is $1,000 for the bonding step. The cost is justified by the performance benefits: the hybrid bonding connections have 10 times lower resistance and 10 times lower capacitance than solder bumps, enabling the high-speed signaling required by the PIP-Fabric.

The hybrid bonding process is a key differentiator of the PIP CISC platform. No other platform uses hybrid bonding to connect chiplets to an interposer at 9-micron pitch. The hybrid bonding process is the result of years of research and development by TSMC, and it is protected by dozens of patents. The hybrid bonding process is the reason that the PIP CISC platform can integrate 1,296 chiplets on a single blade.

This concludes Chapter 16 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Through-Silicon Via Fabrication process, which creates the vertical connections through the interposer. The through-silicon vias are essential for connecting the chiplets to the substrate.

# Chapter 17: Through-Silicon Via Fabrication

The through-silicon vias are the vertical connections that pass through the silicon interposer, connecting the chiplets on the front side to the substrate on the back side. Each via is a 10-micron diameter hole filled with copper that provides a low-resistance path from the chiplet bonding pads to the substrate bonding pads. The interposer has 2.25 million vias, one for each bonding pad. The vias are fabricated using a via-first process, meaning the vias are etched and filled before the redistribution layers are deposited.

The through-silicon via fabrication begins with a 200-micron thick silicon wafer. The wafer is first coated with a layer of silicon dioxide that is 2 microns thick. The oxide is deposited by plasma-enhanced chemical vapor deposition at 350 degrees Celsius. The oxide serves as an electrical insulator between the vias and the silicon substrate. The oxide also acts as an etch stop layer for the subsequent etching process.

The via locations are patterned using photolithography. A photoresist mask is deposited and exposed with a stepper that projects the via pattern onto the wafer. The pattern has 10-micron diameter circles at 50-micron pitch across the entire wafer. The exposed photoresist is developed, leaving holes in the resist at the via locations. The resist is then hard-baked at 120 degrees Celsius to improve its etch resistance.

The vias are etched using the Bosch deep reactive ion etching process. The wafer is placed in an inductively coupled plasma etcher with alternating cycles of etching and passivation. The etching cycle uses sulfur hexafluoride gas to etch silicon isotropically. The passivation cycle uses octafluorocyclobutane to deposit a fluorocarbon polymer on the sidewalls. After 2,000 cycles, the vias are 200 microns deep, reaching completely through the wafer.

The Bosch process creates vias with scalloped sidewalls caused by the alternating etch and passivation cycles. The scallops are 100 nanometers deep and 500 nanometers wide. The scallops are acceptable for the subsequent copper filling process because the copper will conform to the sidewalls. The scallops also improve the adhesion of the barrier layer because they create mechanical interlocking.

The vias are cleaned after etching to remove the fluorocarbon polymer and any silicon debris. The cleaning uses a piranha solution of sulfuric acid and hydrogen peroxide at 120 degrees Celsius. The piranha solution attacks organic materials but does not attack silicon or silicon dioxide. The cleaning is followed by a rinse in deionized water and a spin-dry cycle.

A liner of titanium nitride is deposited on the via sidewalls by atomic layer deposition. The wafer is placed in a reaction chamber at 350 degrees Celsius, and alternating pulses of tetrakis(dimethylamino)titanium and ammonia are introduced. Each pulse deposits a monolayer of titanium nitride, and 100 pulses are required to achieve a 10-nanometer thick liner. The liner serves as a diffusion barrier that prevents copper from migrating into the silicon.

A seed layer of copper is deposited on top of the titanium nitride liner by physical vapor deposition. The wafer is sputtered in an argon plasma with a copper target at 5 kilowatts of DC power. The deposition continues until a 200-nanometer thick copper layer covers all via sidewalls and the top surface of the wafer. The seed layer provides a conductive path for the electroplating current.

The vias are filled with copper by electroplating. The wafer is immersed in an acid copper sulfate bath with 50 grams per liter of copper sulfate and 200 grams per liter of sulfuric acid. A current density of 10 milliamperes per square centimeter deposits copper at 0.5 microns per minute. The deposition continues for 400 minutes, filling the 200-micron deep vias completely. The copper overburden on the wafer surface is 50 microns thick at the end of the plating process.

The overburden is removed by chemical mechanical polishing. The wafer is mounted on a rotating platen and pressed against a polishing pad with a slurry of alumina particles in an oxidizing solution. The polishing removes the 50-micron copper overburden and planarizes the surface to within 50 nanometers of flatness. The polishing stops when the silicon dioxide layer is exposed, leaving the copper via plugs flush with the oxide surface.

The through-silicon vias are then tested for continuity. A probe card contacts the top of each via and measures the resistance to a probe on the bottom of the wafer. The resistance should be less than 100 milliohms. The test is performed at wafer level before the redistribution layers are deposited. Vias that fail the test are marked as defective and will be bypassed using the redundancy in the redistribution layers.

The through-silicon vias are also tested for leakage. A voltage of 10 volts is applied between the via and the silicon substrate. The leakage current should be less than 1 nanoampere. The test detects any pinholes in the titanium nitride liner or any contamination in the via. The test is performed at wafer level before the redistribution layers are deposited.

The through-silicon vias are the vertical backbone of the interposer. They connect the front side to the back side, allowing signals and power to flow from the chiplets to the substrate. The vias have a resistance of 10 milliohms and a capacitance of 50 femtofarads. The resistance is low enough that the IR drop is negligible. The capacitance is low enough that the signal integrity is not compromised.

The through-silicon vias are also a source of stress. The copper in the vias expands more than the silicon when heated, creating mechanical stress around the vias. The stress can cause the silicon to crack if the vias are too close together. The minimum distance between vias is 50 microns, which is sufficient to prevent cracking. The stress is also mitigated by the titanium nitride liner, which absorbs some of the expansion.

The through-silicon vias are a key enabler of the PIP CISC platform. They allow the chiplets to be connected to the substrate without wire bonds or solder bumps. The vias are the reason that the interposer can have 2.25 million connections to the substrate. The vias are the unsung heroes of the PIP CISC platform.

This concludes Chapter 17 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Reflow Soldering and Surface Mount Technology used to attach the NAND flash chips and other components to the substrate.

# Chapter 18: Reflow Soldering and Surface Mount Technology

The reflow soldering and surface mount technology process attaches the NAND flash chips, passive components, and connectors to the motherboard substrate. Unlike the hybrid bonding used for the chiplets, which creates direct copper-to-copper connections, reflow soldering uses solder to create mechanical and electrical connections. The process is mature and well-understood, with decades of manufacturing experience behind it. The PIP CISC platform uses reflow soldering for all components that are not attached by hybrid bonding, including the 80 NAND flash chips in the 100TB configuration, the 1,000 decoupling capacitors, the power connectors, and the edge connector.

The reflow soldering process begins with the application of solder paste to the substrate. The solder paste is a suspension of solder particles in a flux vehicle. The solder particles are a tin-silver-copper alloy with a melting point of 217 degrees Celsius. The flux vehicle cleans the surfaces of the pads and the components, removes oxides, and promotes wetting. The solder paste is applied by a stencil printer, which squeezes the paste through a stainless steel stencil onto the pads.

The stencil is a 100-micron thick sheet of stainless steel with laser-cut apertures at the pad locations. The apertures are slightly smaller than the pads to prevent solder bridging. For a 0.5mm pad, the aperture is 0.45mm. The stencil is aligned to the substrate using fiducial marks, and a squeegee pushes the solder paste across the stencil, filling the apertures. The substrate is then separated from the stencil, leaving deposits of solder paste on the pads.

The thickness of the solder paste deposit is controlled by the stencil thickness and the aperture size. The target deposit volume is 0.1 cubic millimeters per pad, which provides enough solder to form a reliable joint. The solder paste is inspected by a laser profilometer that measures the height and volume of each deposit. Deposits that are too high or too low are flagged for rework.

The components are then placed onto the substrate by a pick-and-place machine. The machine has a bank of feeders that supply the components on tape and reel. A vacuum nozzle picks each component from the feeder, aligns it using a vision system, and places it onto the solder paste deposits. The placement accuracy is 25 microns, which is sufficient for the 0.5mm pads.

The pick-and-place machine places the NAND flash chips first, because they are the largest components. The flash chips are placed in a grid pattern with 1mm spacing between chips. The machine then places the decoupling capacitors, which are 0402-size (1mm by 0.5mm) components. The machine finally places the connectors, which are the largest components on the board.

The placed components are held in place by the tackiness of the solder paste. The board is then transferred to the reflow oven, which melts the solder and forms the permanent connections. The reflow oven has multiple zones that heat the board gradually to prevent thermal shock. The board enters the oven at room temperature and passes through preheat, soak, reflow, and cooling zones.

The preheat zone raises the temperature of the board from 25 degrees Celsius to 150 degrees Celsius over 60 seconds. The heating rate is 2 degrees Celsius per second, which is slow enough to prevent cracking of the components. The preheat zone also activates the flux in the solder paste, which begins to clean the pads and the component leads.

The soak zone holds the board at 150 degrees Celsius for 60 seconds. The soak zone allows the temperature to equalize across the board, so that all components reach the same temperature. The soak zone also completes the activation of the flux, removing any remaining oxides. The soak zone is critical for preventing tombstoning, a defect where one end of a component lifts off the board due to uneven heating.

The reflow zone raises the temperature from 150 degrees Celsius to 245 degrees Celsius over 30 seconds. The heating rate is 3 degrees Celsius per second. The peak temperature is 245 degrees Celsius, which is 28 degrees above the melting point of the solder. The reflow zone lasts for 30 seconds, during which the solder melts and wets the pads and the component leads.

The cooling zone lowers the temperature from 245 degrees Celsius to 25 degrees Celsius over 60 seconds. The cooling rate is 4 degrees Celsius per second. The cooling zone solidifies the solder, forming the permanent connections. The cooling rate is controlled to prevent the formation of brittle intermetallic compounds.

After reflow, the board is inspected by automated optical inspection. A camera system with 10-micron resolution scans the entire board, comparing the image to a golden board. The inspection detects missing components, misaligned components, solder bridges, and insufficient solder. The inspection takes 1 minute per board.

The board is also inspected by X-ray. The X-ray system penetrates the components and reveals the solder joints underneath. The X-ray detects voids in the solder, which are bubbles that reduce the strength of the joint. The acceptance criterion is less than 20 percent voiding per joint.

The reflow soldering process is well-controlled and has a high yield. The yield for the NAND flash chips is 99.9 percent per joint, which is excellent for a 0.5mm pitch component. The yield for the decoupling capacitors is 99.99 percent per joint. The overall board yield is 95 percent, which is acceptable for volume production.

The reflow soldering process is also used for rework. A defective component can be removed by heating it with a hot air pencil while the board is supported on a hot plate. The molten solder is wicked away with solder wick, and a new component is placed with a pick-and-place tool. The rework takes 5 minutes per component and has a success rate of 90 percent.

The reflow soldering process is the last major assembly step for the PIP CISC blade. After the components are attached, the blade is cleaned to remove flux residues. The cleaning uses a saponifier solution that emulsifies the flux, followed by a deionized water rinse. The blade is then dried with hot air and inspected for cleanliness.

This concludes Chapter 18 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Mechanical Enclosure and Rack Integration, covering the chassis design for the desktop, professional, and blade variants.

# Chapter 19: Mechanical Enclosure and Rack Integration

The mechanical enclosure protects the PIP CISC blade from physical damage, provides electromagnetic shielding, and manages airflow for cooling. The enclosure also provides the mechanical interface to the rack or to the desktop case. The blade variant has a different enclosure than the desktop variant, because the blade must slide into a rack while the desktop must sit on a desk. The professional workstation variant has an enclosure that is intermediate between the two.

The blade enclosure is a sheet metal box that measures 200mm wide, 500mm deep, and 40mm tall. The enclosure is made of 1mm thick aluminum sheet, which is lightweight and has good thermal conductivity. The aluminum is coated with a nickel-plated finish that resists corrosion and provides electromagnetic shielding. The enclosure has a removable top cover that allows access to the motherboard for service.

The front of the blade enclosure has a faceplate with a handle for insertion and removal. The handle is spring-loaded and engages with the rack to secure the blade. The faceplate also has status LEDs that indicate power, activity, and fault conditions. The LEDs are visible through a transparent window in the faceplate.

The rear of the blade enclosure has the edge connector that plugs into the rack backplane. The edge connector is a 200-pin connector with gold-plated contacts. The connector is mounted directly to the motherboard and protrudes through an opening in the rear of the enclosure. The enclosure also has cutouts for the optical transceivers, which are accessible from the rear.

The bottom of the blade enclosure has a cold plate that contacts the thermal encasement of the motherboard. The cold plate is made of copper with internal channels for the cooling liquid. The cold plate is spring-loaded to ensure good contact with the thermal encasement. The cold plate is connected to the rack manifold through quick-disconnect fittings on the rear of the blade.

The blade enclosure is designed to slide into a 19-inch rack chassis. The rack chassis holds up to 20 blades in a 42U rack. The chassis has guide rails that align the blade as it is inserted. The guide rails also support the weight of the blade, which is 5 kilograms for a fully populated blade. The chassis has a backplane that mates with the edge connector and the optical transceivers.

The rack backplane is a passive printed circuit board that distributes power and signals between the blades. The backplane has 20 slots for the blades, each with a 200-pin edge connector and 12 optical connectors. The backplane also has connectors for the management board, the power distribution unit, and the external network. The backplane is 19 inches wide and 1U (44mm) tall.

The rack backplane is manufactured from FR-4 material with 20 layers of copper. The backplane has power planes that distribute 48 volts to the blades, and signal layers that distribute management and synchronization signals. The backplane also has embedded optical waveguides that route the optical signals between the blades. The waveguides are fabricated from polymer materials and have a loss of 0.5 decibels per meter.

The rack chassis also includes a management board that controls the power and cooling for the rack. The management board is a small computer with its own processor and memory. The management board communicates with the blades through a dedicated management network on the backplane. The management board also monitors the temperature and power consumption of the rack and adjusts the cooling accordingly.

The rack chassis also includes a power distribution unit that converts 208-volt AC power to 48-volt DC power. The power distribution unit has a capacity of 10 kilowatts, which is sufficient for 20 blades at 700 watts each. The power distribution unit also has a battery backup that provides 5 minutes of power in case of an AC outage.

The desktop enclosure is a traditional tower case that measures 220mm wide, 590mm tall, and 560mm deep. The case is made of 1mm thick steel with a powder-coated finish. The case has a removable side panel that allows access to the motherboard. The front of the case has a power button, reset button, and status LEDs.

The desktop case has a copper heat spreader that contacts the thermal encasement of the motherboard. The heat spreader has fins that are 10mm tall and spaced 2mm apart. Three 120mm fans blow air across the fins, removing up to 600 watts of heat. The fans are controlled by the System cores based on the temperature readings from the chiplets.

The desktop case also has drive bays for additional storage. The drive bays are located in the front of the case and can hold up to four 3.5-inch hard drives or eight 2.5-inch SSDs. The drives are connected to the motherboard through SATA cables.

The professional workstation enclosure is larger than the desktop case, measuring 250mm wide, 650mm tall, and 600mm deep. The case is made of 1.5mm thick aluminum with a brushed finish. The case has a liquid cooling system with dual 360mm radiators and a pump. The liquid cooling system removes up to 1,000 watts of heat.

The professional case also has a window in the side panel that allows the user to see the motherboard. The window is made of tempered glass and is tinted to reduce glare. The case also has RGB lighting that can be controlled by the software.

The mechanical enclosure is the final piece of the PIP CISC platform. It protects the delicate electronics, provides cooling, and gives the product a professional appearance. The enclosure is designed to be both functional and attractive, meeting the needs of data center operators and individual users alike.

This concludes Chapter 19 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Power-On Self-Test and Built-In Self-Test, covering the diagnostic routines that verify the integrity of the blade before it is allowed to boot.

# Chapter 20: Power-On Self-Test and Built-In Self-Test

The power-on self-test and built-in self-test are the diagnostic routines that verify the integrity of the PIP CISC blade before it is allowed to boot. The power-on self-test runs every time the blade is powered on, while the built-in self-test runs during manufacturing and on demand. The tests cover the core chiplets, the memory stacks, the flash chips, the optical transceivers, and the interconnects.

The power-on self-test begins as soon as the blade receives power. The System core that is designated as the primary boot core starts executing code from a read-only memory embedded in the chiplet. The boot ROM contains the first-stage bootloader, which initializes the minimal hardware required to load the second-stage bootloader from flash.

The first test is the clock test. The System core checks that all phase-locked loops have locked to the reference clock. The core reads the lock status registers of each PLL and verifies that the lock bit is set. If any PLL fails to lock, the core retries the lock sequence up to 10 times. If the PLL still fails to lock, the core reports a fatal error and halts.

The second test is the voltage test. The System core reads the voltage monitoring registers of the power management unit. The core verifies that the core voltage is within 0.8 volts plus or minus 5 percent, the memory voltage is within 1.2 volts plus or minus 5 percent, and the I/O voltage is within 1.8 volts plus or minus 5 percent. If any voltage is out of tolerance, the core reports a fatal error and halts.

The third test is the temperature test. The System core reads the temperature sensors distributed across the blade. The core verifies that all temperatures are below 85 degrees Celsius. If any temperature is above 85 degrees, the core activates the cooling system and waits for the temperature to drop. If the temperature does not drop within 60 seconds, the core reports a fatal error and halts.

The fourth test is the memory test. The System core writes a pattern to every location in the HBM3e memory stacks and then reads it back. The pattern is a walking ones pattern that tests each bit individually. The test also checks for stuck-at faults, coupling faults, and neighborhood pattern sensitive faults. The memory test takes 1 second per gigabyte, so the 64-gigabyte memory takes 64 seconds.

The fifth test is the flash test. The System core reads the identification page of each NAND flash chip and verifies that the chip is present and responding. The core then performs a quick erase test on a small portion of each chip. The flash test takes 1 second per chip, so the 80 chips in the 100TB configuration take 80 seconds.

The sixth test is the optical transceiver test. The System core sends a test pattern through each transceiver and verifies that the pattern is received correctly. The test pattern is a pseudorandom bit sequence that exercises all possible bit transitions. The test also measures the bit error rate and the signal strength. The optical test takes 1 second per transceiver, so the 12 transceivers take 12 seconds.

The seventh test is the interconnect test. The System core sends a test packet from every core to every other core and verifies that the packet is received correctly. The test also measures the latency of each path and checks for congestion. The interconnect test takes 1 second per core, but because the test is parallelized across all cores, the total time is 1 second.

The eighth test is the built-in self-test of the Math cores. Each Math core has a built-in self-test controller that can test the core without external intervention. The self-test runs a sequence of instructions that exercise the ALU, the register file, and the caches. The self-test also tests the vector units by performing vector add, multiply, and FMA operations. The Math core self-test takes 10 milliseconds per core, and because the test is parallelized across all 10,000 cores, the total time is 10 milliseconds.

The ninth test is the built-in self-test of the Logic cores. The Logic core self-test is similar to the Math core self-test but focuses on branch prediction and integer operations. The self-test runs a sequence of branches, calls, and returns that exercise the branch predictor and the return stack. The Logic core self-test takes 5 milliseconds per core, and because the test is parallelized across all 2,048 cores, the total time is 5 milliseconds.

The tenth test is the built-in self-test of the System cores. The System core self-test tests the memory management unit, the interrupt controller, and the I/O interfaces. The self-test also tests the cryptographic unit by encrypting and decrypting a test pattern. The System core self-test takes 10 milliseconds per core, and because the test is parallelized across all 40 cores, the total time is 10 milliseconds.

The eleventh test is the crossbar test. The System core sends test packets through every path in the crossbar and verifies that the packets are received correctly. The test also tests the multicast and broadcast capabilities. The crossbar test takes 100 milliseconds.

The twelfth test is the directory test. The System core exercises the directory cache by creating, modifying, and invalidating cache lines. The test verifies that the directory state machine transitions correctly through all MESI states. The directory test takes 100 milliseconds.

The power-on self-test takes approximately 2.5 minutes to complete. Most of the time is consumed by the memory test (64 seconds) and the flash test (80 seconds). The remaining tests take less than 1 second each. The power-on self-test is performed every time the blade is powered on, but the user can skip some tests to reduce boot time.

The built-in self-test is a more comprehensive test that is performed during manufacturing. The built-in self-test includes additional tests for the hybrid bonding connections, the through-silicon vias, and the solder joints. The built-in self-test takes 1 hour to complete and is only performed at the factory.

The built-in self-test includes a thermal stress test that cycles the blade between -40 and 125 degrees Celsius while running the diagnostic routines. The thermal stress test detects any intermittent failures that might occur only at temperature extremes. The thermal stress test takes 10 hours to complete.

The built-in self-test also includes a voltage stress test that varies the core voltage from 0.6 to 1.0 volts while running the diagnostic routines. The voltage stress test detects any circuits that are sensitive to voltage variations. The voltage stress test takes 1 hour to complete.

The built-in self-test also includes a frequency stress test that varies the core frequency from 1 to 3 GHz while running the diagnostic routines. The frequency stress test detects any circuits that are sensitive to timing variations. The frequency stress test takes 1 hour to complete.

The power-on self-test and built-in self-test are essential for the reliability of the PIP CISC platform. They detect defects before the blade is shipped to the customer, and they detect failures before the blade is allowed to boot in the field. The self-tests are the first line of defense against hardware failures.

This concludes Chapter 20 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Manufacturing Test Flows and Fault Coverage, covering the statistical methods used to ensure that the blades meet quality and reliability targets.

# Chapter 21: Manufacturing Test Flows and Fault Coverage

The manufacturing test flow is the sequence of tests that every PIP CISC blade must pass before it is shipped to a customer. The test flow is designed to detect manufacturing defects such as shorts, opens, incorrect component placement, and process variations. The test flow also screens for early-life failures that would otherwise occur in the field. The test flow is developed by the manufacturing engineering team in collaboration with the design team, and it is implemented on automated test equipment at TSMC's packaging and test facility.

The test flow begins with an incoming inspection of the motherboard substrate. The substrate is inspected for cosmetic defects such as scratches, dents, and discoloration. The substrate is also measured for flatness, thickness, and warpage. Substrates that fail the incoming inspection are rejected and returned to the substrate manufacturer. The incoming inspection has a fault coverage of 90 percent for cosmetic defects and 100 percent for dimensional defects.

The second step is the solder paste inspection. The solder paste is inspected after the stencil printing step and before component placement. The inspection measures the height, volume, and area of each solder paste deposit. Deposits that are too high or too low are flagged for rework. The solder paste inspection has a fault coverage of 99 percent for missing solder and 95 percent for insufficient solder.

The third step is the automated optical inspection after component placement but before reflow. The inspection verifies that all components are present and correctly oriented. The inspection also checks for tombstoning, where one end of a component lifts off the board. The automated optical inspection has a fault coverage of 98 percent for missing components and 95 percent for misoriented components.

The fourth step is the automated optical inspection after reflow. The inspection checks for solder bridges, insufficient solder, and other reflow defects. The inspection also verifies that the components have not moved during reflow. The post-reflow optical inspection has a fault coverage of 99 percent for solder bridges and 95 percent for insufficient solder.

The fifth step is the X-ray inspection. The X-ray system penetrates the components and reveals the solder joints underneath. The X-ray inspection detects voids in the solder, which are bubbles that reduce the strength of the joint. The X-ray inspection also detects head-in-pillow defects, where the component lead does not wet to the solder. The X-ray inspection has a fault coverage of 95 percent for voids larger than 20 percent of the joint volume.

The sixth step is the in-circuit test. The in-circuit tester contacts test points on the board and measures the resistance, capacitance, and inductance of the components. The in-circuit tester can detect opens, shorts, and incorrect component values. The in-circuit test has a fault coverage of 90 percent for opens and 85 percent for shorts.

The seventh step is the boundary scan test. The boundary scan test uses the JTAG interface to test the interconnections between the chiplets and the interposer. The boundary scan test can detect opens and shorts in the hybrid bonding connections. The boundary scan test has a fault coverage of 99 percent for opens and 98 percent for shorts.

The eighth step is the built-in self-test of the chiplets. The built-in self-test is run on each chiplet individually, with the other chiplets held in reset. The built-in self-test exercises the ALUs, the register files, the caches, and the mesh network. The built-in self-test has a fault coverage of 95 percent for the Math cores, 95 percent for the Logic cores, and 98 percent for the System cores.

The ninth step is the memory built-in self-test of the HBM3e stacks. The memory built-in self-test writes patterns to every memory cell and reads them back. The test detects stuck-at faults, coupling faults, and neighborhood pattern sensitive faults. The memory built-in self-test has a fault coverage of 99 percent for the HBM3e stacks.

The tenth step is the flash test. The flash test writes patterns to a small portion of each NAND flash chip and reads them back. The test also checks the wear leveling and bad block management logic. The flash test has a fault coverage of 90 percent for the flash chips, which is acceptable because the flash chips have built-in error correction.

The eleventh step is the optical transceiver test. The optical transceiver test sends patterns through each transceiver and measures the bit error rate. The test also measures the transmit power, the receive sensitivity, and the eye opening. The optical transceiver test has a fault coverage of 99 percent for the transceivers.

The twelfth step is the system test. The system test runs a full operating system on the blade and executes a suite of diagnostic applications. The system test verifies that the blade can boot, that all cores are functional, and that the memory and storage are accessible. The system test has a fault coverage of 95 percent for system-level defects.

The manufacturing test flow has an overall fault coverage of 95 percent, meaning that 95 percent of defects are detected by the tests. The remaining 5 percent of defects are latent defects that will cause failures in the field. The fault coverage is validated by injecting known defects into sample blades and verifying that the tests detect them.

The manufacturing test flow also includes a burn-in step. The burn-in step runs the blade at elevated temperature and voltage for 24 hours while running the built-in self-test in a loop. The burn-in step accelerates the aging of the blade, causing latent defects to fail early. Blades that survive the burn-in step are much less likely to fail in the field.

The burn-in step is performed in a burn-in oven that can hold 100 blades at a time. The oven heats the blades to 125 degrees Celsius while the test equipment applies 1.1 volts to the core logic. The burn-in step consumes 10 kilowatts of power and generates 10 kilowatts of heat. The burn-in step is the most expensive step in the manufacturing test flow.

The manufacturing test flow is designed to achieve a shipped product quality level of 100 parts per million, meaning that no more than 100 blades per million shipped will fail in the first year of operation. This quality level is typical for high-end server products and is acceptable for the PIP CISC platform.

This concludes Chapter 21 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Reliability, Burn-In, and Stress Testing, covering the methods used to ensure that the blades meet the reliability targets.

# Chapter 22: Reliability, Burn-In, and Stress Testing

Reliability is the probability that a blade will function without failure for a specified period of time. The PIP CISC platform has a reliability target of 10 years of continuous operation, which is typical for server products. The reliability target is achieved through a combination of design margin, component selection, and stress testing. The stress testing includes burn-in, thermal cycling, voltage cycling, and mechanical shock testing.

The burn-in test is the most important stress test for reliability. The burn-in test runs the blade at elevated temperature and voltage for 24 hours while running the built-in self-test in a loop. The elevated temperature accelerates the chemical reactions that cause failure, such as electromigration and corrosion. The elevated voltage accelerates the electrical stress that causes failure, such as gate oxide breakdown. Blades that survive the burn-in test are much less likely to fail in the field.

The burn-in test is performed at 125 degrees Celsius, which is 40 degrees above the maximum operating temperature of 85 degrees Celsius. The core voltage is increased to 1.1 volts, which is 30 percent above the nominal 0.8 volts. The frequency is reduced to 1 GHz to prevent the blade from exceeding its thermal limit. The burn-in test consumes 10 kilowatts of power per 100 blades and generates 10 kilowatts of heat.

The thermal cycling test is performed on a sample of blades from each production lot. The thermal cycling test cycles the blade between -40 and 125 degrees Celsius for 1,000 cycles. The test is performed with the power off, so the only stress is from the thermal expansion mismatch between the materials. The thermal cycling test detects defects in the hybrid bonding connections, the solder joints, and the interposer vias.

The thermal cycling test is performed in a thermal chamber that can hold 10 blades at a time. The chamber heats the blades to 125 degrees Celsius over 10 minutes, holds them at temperature for 10 minutes, then cools them to -40 degrees Celsius over 10 minutes. The cycle is repeated 1,000 times, for a total test time of 500 hours. Blades that survive the thermal cycling test have no defects in the interconnects.

The voltage cycling test is performed on a sample of blades from each production lot. The voltage cycling test cycles the core voltage between 0.6 and 1.0 volts for 10,000 cycles. The test is performed at room temperature, with the blade running the built-in self-test. The voltage cycling test detects defects in the power distribution network and in the voltage regulators.

The voltage cycling test is performed on a test fixture that can hold 10 blades at a time. The fixture cycles the voltage from 0.6 to 1.0 volts over 1 millisecond, holds at 1.0 volts for 1 millisecond, then cycles back to 0.6 volts. The cycle is repeated 10,000 times, for a total test time of 20 seconds. Blades that survive the voltage cycling test have no defects in the power distribution network.

The mechanical shock test is performed on a sample of blades from each production lot. The mechanical shock test subjects the blade to a 50 G shock for 10 milliseconds in each of the three axes. The shock is applied by a drop table that drops the blade onto a steel plate. The mechanical shock test detects defects in the solder joints and in the connectors.

The mechanical shock test is performed on a test fixture that can hold one blade at a time. The blade is mounted on a drop table that is raised to a height of 1 meter and then dropped onto a steel plate. The impact generates a 50 G shock for 10 milliseconds. The blade is inspected for damage after the test. Blades that survive the mechanical shock test have no defects in the solder joints or connectors.

The vibration test is performed on a sample of blades from each production lot. The vibration test subjects the blade to 10 G of vibration at frequencies from 10 to 500 Hz for 1 hour in each of the three axes. The vibration is applied by a shaker table that oscillates the blade. The vibration test detects defects in the connectors and in the optical transceivers.

The vibration test is performed on a test fixture that can hold one blade at a time. The blade is mounted on a shaker table that oscillates at 10 G. The frequency is swept from 10 to 500 Hz over 1 hour. The blade is inspected for damage after the test. Blades that survive the vibration test have no defects in the connectors or optical transceivers.

The humidity test is performed on a sample of blades from each production lot. The humidity test subjects the blade to 85 percent relative humidity at 85 degrees Celsius for 1,000 hours. The test is performed with the power off. The humidity test detects defects in the corrosion protection of the solder joints and the connectors.

The humidity test is performed in a humidity chamber that can hold 10 blades at a time. The chamber maintains a temperature of 85 degrees Celsius and a relative humidity of 85 percent for 1,000 hours. The blades are inspected for corrosion after the test. Blades that survive the humidity test have no corrosion defects.

The reliability tests are destructive, meaning that the blades that are tested cannot be shipped to customers. The reliability tests are performed on a sample of blades from each production lot, typically 1 percent of the lot. The results of the reliability tests are used to adjust the manufacturing process if necessary.

The reliability of the PIP CISC platform is quantified by the mean time between failures. The MTBF is calculated by dividing the total operating time of a population of blades by the number of failures. The MTBF target for the PIP CISC platform is 1 million hours, which is 114 years. This is typical for server products and is acceptable for the PIP CISC platform.

The reliability of the PIP CISC platform is validated by accelerated life testing. A sample of 100 blades is subjected to accelerated stress for 1,000 hours, which is equivalent to 10 years of normal operation. The number of failures during the test is used to estimate the MTBF. The accelerated life test is performed once per year to validate the reliability of the manufacturing process.

This concludes Chapter 22 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Desktop Workstation Form Factor, covering the physical dimensions, thermal management, and power delivery for the desktop variant.

# Chapter 23: Desktop Workstation Form Factor

The desktop workstation variant of the PIP CISC platform is designed for use on a desk, under a desk, or in a standard computer case. The desktop variant has a lower power consumption than the blade variant, because it has fewer optical transceivers (2 instead of 12) and a smaller storage configuration (10TB instead of 100TB). The desktop variant is air-cooled rather than liquid-cooled, which makes it suitable for home and office environments.

The desktop motherboard measures 305mm by 305mm, which is the Extended ATX form factor. The motherboard has mounting holes in the standard ATX locations, so it can be installed in any ATX-compatible case. The motherboard has a 24-pin power connector for the main power, and an 8-pin power connector for the CPU power. The motherboard also has a 4-pin power connector for the fans.

The desktop motherboard has two optical transceivers, which provide up to 1.6 terabits per second of off-board bandwidth. The optical transceivers are mounted on the rear edge of the motherboard, next to the I/O panel. The optical transceivers are connected to the rack or to other workstations through standard fiber optic cables.

The desktop motherboard has two M.2 slots for NVMe SSDs, which provide additional storage. The M.2 slots support PCIe 5.0 x4 interfaces, providing up to 16 gigabytes per second of bandwidth. The M.2 slots are located on the front edge of the motherboard, where they are easily accessible.

The desktop motherboard has four DIMM slots for DDR5 memory, which provide up to 128 gigabytes of additional memory. The DIMM slots are located to the right of the CPU socket. The DIMM slots support dual-channel memory configurations.

The desktop motherboard has one PCIe 5.0 x16 slot for a graphics card, and two PCIe 5.0 x4 slots for other expansion cards. The PCIe slots are located below the CPU socket. The PCIe slots are connected to the PIP-Fabric through a PCIe bridge chip.

The desktop motherboard has a standard I/O panel with USB 4 ports, Ethernet ports, audio jacks, and video outputs. The I/O panel also has the connectors for the optical transceivers. The I/O panel is located on the rear edge of the motherboard.

The desktop workstation has a copper heat spreader that contacts the thermal encasement of the motherboard. The heat spreader has fins that are 10mm tall and spaced 2mm apart. Three 120mm fans blow air across the fins, removing up to 600 watts of heat. The fans are controlled by the System cores based on the temperature readings from the chiplets.

The desktop workstation is intended for use in a standard computer case. The case must have at least 600 watts of cooling capacity and at least 200mm of width to accommodate the 305mm by 305mm motherboard. The case must also have space for the 120mm fans and for the optical transceivers.

The desktop workstation is the most affordable variant of the PIP CISC platform. It is intended for software developers, researchers, and small businesses that need high-performance computing but do not have a data center. The desktop workstation delivers the same computational performance as the blade variant, but with lower storage capacity and lower off-board bandwidth.

This concludes Chapter 23 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Professional Workstation Form Factor, which has higher power and cooling capacity than the desktop variant.

# Chapter 24: Professional Workstation Form Factor

The professional workstation variant of the PIP CISC platform is designed for use in a laboratory, studio, or small server room. The professional variant has a higher power consumption than the desktop variant, because it has six optical transceivers and a larger storage configuration (20TB). The professional variant is liquid-cooled, which allows it to dissipate up to 1,000 watts of heat.

The professional motherboard measures 400mm by 350mm, which is larger than the Extended ATX form factor. The motherboard has custom mounting holes and requires a special case. The motherboard has a 24-pin power connector for the main power, and two 8-pin power connectors for the CPU power. The motherboard also has a 6-pin power connector for the liquid cooling pump.

The professional motherboard has six optical transceivers, which provide up to 4.8 terabits per second of off-board bandwidth. The optical transceivers are mounted on the rear edge of the motherboard. The optical transceivers are connected to the rack or to other workstations through standard fiber optic cables.

The professional motherboard has four M.2 slots for NVMe SSDs, which provide additional storage. The M.2 slots support PCIe 5.0 x4 interfaces, providing up to 16 gigabytes per second of bandwidth. The M.2 slots are located on the front edge of the motherboard.

The professional motherboard has eight DIMM slots for DDR5 memory, which provide up to 256 gigabytes of additional memory. The DIMM slots are located to the right of the CPU socket. The DIMM slots support quad-channel memory configurations.

The professional motherboard has two PCIe 5.0 x16 slots for graphics cards, and two PCIe 5.0 x8 slots for other expansion cards. The PCIe slots are located below the CPU socket. The PCIe slots are connected to the PIP-Fabric through a PCIe bridge chip.

The professional motherboard has a standard I/O panel with USB 4 ports, Ethernet ports, audio jacks, and video outputs. The I/O panel also has the connectors for the optical transceivers. The I/O panel is located on the rear edge of the motherboard.

The professional workstation has a liquid cooling system with dual 360mm radiators and a pump. The liquid cooling system removes up to 1,000 watts of heat. The radiators are mounted on the top and front of the case. The pump is mounted on the bottom of the case.

The professional workstation is intended for use in a custom case. The case must have at least 1,000 watts of cooling capacity and must be large enough to accommodate the 400mm by 350mm motherboard. The case must also have space for the radiators and the pump.

The professional workstation is the highest-performance variant of the PIP CISC platform. It is intended for video editors, 3D animators, and scientists who need the maximum possible performance from a single workstation. The professional workstation delivers the same computational performance as the blade variant, but with higher storage capacity and higher off-board bandwidth.

This concludes Chapter 24 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Blade Server Form Factor, which is designed for high-density deployment in data centers.

# Chapter 25: Blade Server Form Factor

The blade server variant of the PIP CISC platform is designed for high-density deployment in data centers. The blade variant has the highest power consumption of the three variants, because it has twelve optical transceivers and the largest storage configuration (100TB). The blade variant is liquid-cooled, which allows it to dissipate up to 700 watts of heat in a 40mm thick enclosure.

The blade motherboard measures 200mm by 500mm, which is the blade form factor. The motherboard has an edge connector on the rear edge that plugs into the rack backplane. The motherboard has no other connectors; all power and I/O are provided through the backplane.

The blade has twelve optical transceivers, which provide up to 9.6 terabits per second of off-board bandwidth. The optical transceivers are mounted on the rear edge of the motherboard and mate with optical connectors on the backplane. The blade has no fiber optic cables; the optical signals are routed through the backplane.

The blade has 100TB of NAND flash storage, which is soldered directly to the motherboard. The flash chips are mounted on both sides of the motherboard, with 40 chips on the top side and 40 chips on the bottom side. The flash chips are covered by the thermal encasement.

The blade has no DIMM slots; the memory is provided by the HBM3e stacks soldered to the interposer. The blade has 64GB of HBM3e memory, which is sufficient for most server workloads. The blade also has 1TB of DDR5 memory on the motherboard for workloads that need more memory.

The blade has no PCIe slots; all expansion is provided through the optical fabric. The blade can access PCIe devices on other blades through the optical fabric, using the remote memory access capabilities of the PIP-Fabric.

The blade has no I/O panel; all I/O is provided through the optical fabric. The blade can access USB, Ethernet, and audio devices on other blades or on the rack management controller.

The blade is cooled by a liquid cold plate that contacts the thermal encasement. The cold plate has internal channels for the cooling liquid. The cold plate is connected to the rack manifold through quick-disconnect fittings on the rear of the blade.

The blade slides into a 19-inch rack chassis that holds up to 20 blades. The rack chassis has a backplane that mates with the edge connector and the optical transceivers. The rack chassis also has a management board, a power distribution unit, and a liquid cooling manifold.

The blade server is intended for deployment in data centers. It is the most dense variant of the PIP CISC platform, with 10,000 Math cores, 2,048 Logic cores, and 160 System cores in a 40mm thick enclosure. The blade server is the variant that will be used for large-scale AI training and HPC clusters.

This concludes Chapter 25 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Storage-Only Blade Configuration, which is a blade with no compute cores, only NAND flash storage.

# Chapter 26: Storage-Only Blade Configuration

The storage-only blade configuration is a variant of the PIP CISC blade that has no Math cores, no Logic cores, and only a minimal number of System cores. The storage-only blade is populated entirely with NAND flash chips, providing up to 200TB of memory-mapped storage. The storage-only blade is designed to be mixed with compute blades in the same rack, providing a scalable storage system that can be accessed directly through the memory address space.

The storage-only blade has the same form factor as the compute blade: 200mm by 500mm by 40mm. The blade has the same edge connector and the same optical transceivers as the compute blade. The blade has a reduced power consumption of 300 watts, because it has no compute cores.

The storage-only blade has no Math cores and no Logic cores. The blade has only 8 System cores, which are sufficient to run the address translation and flash management logic. The System cores on the storage-only blade are the same as on the compute blade, but they are configured to run only storage-related firmware.

The storage-only blade has 200TB of NAND flash storage, arranged as 160 chips of 1.28TB each. The chips are mounted on both sides of the motherboard, with 80 chips on each side. The chips are covered by the thermal encasement.

The storage-only blade has no HBM3e memory. The blade uses a small amount of DDR4 memory for the translation tables and for the firmware. The DDR4 memory is soldered to the motherboard and is not user-upgradable.

The storage-only blade exports its flash storage as memory-mapped regions. The System cores on the compute blades can access the flash storage on the storage-only blade using standard load and store instructions. The address translation hardware on the compute blade directs the requests to the storage-only blade over the optical fabric.

The storage-only blade is managed by the same rack management controller as the compute blades. The management controller can power on and power off the storage-only blade independently of the compute blades. The management controller also monitors the health of the flash chips and reports any failures.

The storage-only blade is intended for use in data centers that need large amounts of memory-mapped storage. The storage-only blade can be combined with compute blades in any ratio, allowing the storage capacity to be scaled independently of the compute capacity. The storage-only blade is the key to the scalability of the PIP CISC platform.

This concludes Chapter 26 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Rack Backplane and Optical Waveguide Design, which connects the blades together into a unified system.

# Chapter 27: Rack Backplane and Optical Waveguide Design

The rack backplane is the passive printed circuit board that connects the blades together into a unified system. The backplane provides power, management signals, and optical communication between the blades. The backplane has no active components, which makes it highly reliable and easy to manufacture. The backplane is designed to fit into a 19-inch rack chassis and to accept up to 20 blades.

The backplane measures 19 inches (483mm) wide by 42U (1,867mm) tall by 5mm thick. The backplane is made of FR-4 material with 20 layers of copper. The backplane has 20 slots for the blades, arranged vertically. Each slot has a 200-pin edge connector and 12 optical connectors.

The power distribution on the backplane is implemented with heavy copper planes. The backplane has a 48-volt power plane that carries power from the power distribution unit to the blades. The power plane is 2 ounces (70 microns) thick and can carry 100 amperes per slot. The backplane also has a ground plane that provides the return path for the power.

The management signals on the backplane are implemented with differential pairs. The management signals include a 1-gigabit Ethernet network that connects the blades to the management board. The management signals also include a 100-megahertz clock that synchronizes the blades. The management signals are routed on the inner layers of the backplane.

The optical waveguides on the backplane are embedded in the FR-4 material. The waveguides are made of polymer materials with a refractive index contrast of 0.02. The waveguides are 50 microns wide and 50 microns tall, forming a square cross-section. The waveguides have a loss of 0.5 decibels per meter at 850 nanometers.

The optical waveguides are arranged in a crossbar topology. Each blade has 12 waveguides that connect to each of the other 19 blades, for a total of 228 waveguides per blade. The waveguides are routed through the backplane using a combination of horizontal and vertical channels. The routing is done by a computer algorithm that minimizes the length of the longest waveguide.

The optical waveguides are coupled to the optical transceivers on the blades through edge couplers. The edge couplers are located on the backplane at the slot positions. The edge couplers are aligned to the optical transceivers on the blades when the blade is inserted. The alignment is achieved by the guide rails on the chassis.

The rack backplane is manufactured by a specialized backplane manufacturer. The backplane is laminated from 20 layers of FR-4 with embedded waveguides. The waveguides are fabricated by laser direct writing, which creates the waveguide pattern in a photosensitive polymer. The waveguides are then overclad with a lower-index polymer.

The rack backplane is tested for continuity and loss. The continuity test checks that each waveguide is present and that the optical connectors are aligned. The loss test measures the insertion loss of each waveguide. The insertion loss should be less than 3 decibels for the longest waveguide.

This concludes Chapter 27 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Multi-Rack Fabric Extension, which allows multiple racks to be connected together into a single system.

# Chapter 28: Multi-Rack Fabric Extension

The multi-rack fabric extension allows multiple racks to be connected together into a single, unified system. The extension uses the same optical technology as the intra-rack backplane, but with longer fibers and active optical switches. The extension can connect up to 256 racks, providing a total of 5,120 blades and 51,200 Math cores in a single shared-memory system.

The multi-rack fabric extension uses standard single-mode fiber optic cables with MTP/MPO-12 connectors. The cables have 12 fibers each and can carry up to 800 gigabits per second per fiber. The cables are available in lengths up to 300 meters, which is sufficient for most data centers.

The multi-rack fabric extension uses active optical switches that route the optical signals between the racks. The switches are based on micro-electromechanical systems technology, which uses tiny mirrors to redirect the light. The switches have 256 input ports and 256 output ports, and can switch a signal in less than 1 microsecond.

The multi-rack fabric extension uses a directory-based coherence protocol that extends across the racks. The directory cache on each blade tracks the location of cache lines on other racks, as well as on other blades. The directory protocol uses the optical switches to communicate between racks.

The multi-rack fabric extension is managed by the same rack management controllers that manage the individual racks. The management controllers communicate with each other over the optical fabric to coordinate the power-on and power-off of the racks. The management controllers also monitor the health of the optical switches and the fiber cables.

The multi-rack fabric extension is the key to the scalability of the PIP CISC platform. It allows the platform to scale from a single blade to 5,120 blades without changing the programming model. The programmer sees a single shared memory, and the hardware handles all of the communication between racks.

This concludes Chapter 28 of the Motherboard Design & Manufacturing Specification. The remaining chapters will cover the Bill of Materials and Component Sourcing, the Assembly Sequence and Process Control, the Quality Assurance and Yield Management, the Firmware Boot ROM and Initialization Microcode, the Debugging and Diagnostic Interfaces, the Field Upgrade and Repair Procedures, the Environmental Compliance and Certification, the Security Features and Tamper Resistance, the Performance Characterization and Benchmarks, the Design Rules and Layout Guidelines for Partners, and the Future Scalability and Next-Generation Roadmap.

# Chapter 29: Bill of Materials and Component Sourcing

The bill of materials for the PIP CISC blade is a comprehensive list of every component required to assemble one blade. The BOM includes the part number, description, quantity, supplier, and cost for each component. The BOM is used by the procurement team to order components and by the manufacturing team to assemble the blades. The BOM is maintained in a database that is updated as components change or as suppliers change.

The most expensive component on the BOM is the silicon interposer. The interposer is manufactured by TSMC and costs $200 per unit in volume production. The interposer contains the PIP-Fabric crossbar, the directory cache, and the through-silicon vias. The interposer is the most complex component on the blade, and its cost reflects that complexity.

The second most expensive component is the Math core chiplets. The 1,000 Math core chiplets cost $10 each, for a total of $10,000 per blade. The Math core chiplets are manufactured by TSMC on the 3nm process. The cost per chiplet is driven by the die size and the yield.

The third most expensive component is the Logic core chiplets. The 256 Logic core chiplets cost $5 each, for a total of $1,280 per blade. The Logic core chiplets are smaller than the Math core chiplets, which reduces the cost per chiplet.

The fourth most expensive component is the System core chiplets. The 40 System core chiplets cost $12 each, for a total of $480 per blade. The System core chiplets are larger than the Logic core chiplets, but there are fewer of them.

The fifth most expensive component is the HBM3e memory stacks. The 8 HBM3e stacks cost $200 each, for a total of $1,600 per blade. The HBM3e stacks are manufactured by Samsung or SK Hynix, and the price is driven by the memory capacity and the bandwidth.

The sixth most expensive component is the NAND flash chips. The 80 NAND flash chips for the 100TB configuration cost $50 each, for a total of $4,000 per blade. The NAND flash chips are manufactured by Kioxia, Western Digital, or Micron. The price of NAND flash is volatile and depends on the supply and demand.

The seventh most expensive component is the optical transceivers. The 12 optical transceivers cost $100 each, for a total of $1,200 per blade. The optical transceivers are manufactured by TSMC on the 130nm photonic process. The cost per transceiver is driven by the laser diode and the packaging.

The eighth most expensive component is the motherboard substrate. The substrate costs $500 per blade in volume production. The substrate is manufactured by a specialized substrate supplier, such as Ibiden or Shinko. The cost of the substrate is driven by the number of layers and the via density.

The ninth most expensive component is the thermal encasement. The pyrolytic graphite sheets cost $200 per blade, and the cold plate costs $100 per blade. The thermal encasement is manufactured by a specialized materials company, such as Panasonic or GrafTech.

The tenth most expensive component is the edge connector. The 200-pin edge connector costs $50 per blade. The edge connector is manufactured by a connector supplier, such as Molex or TE Connectivity.

The total cost of the components for the 100TB blade configuration is $20,000. This cost does not include assembly, test, or overhead. The selling price of the blade will be determined by adding a markup to the cost. The target selling price is $40,000, which is comparable to other high-end server blades.

The BOM is reviewed quarterly by the cost reduction team. The team looks for opportunities to reduce cost by changing suppliers, negotiating better prices, or redesigning components. The goal is to reduce the cost of the blade by 10 percent per year for the first three years of production.

The BOM is also reviewed for obsolescence. The team tracks the lifecycle of each component and identifies components that are nearing end-of-life. When a component is obsoleted, the team works with the supplier to find a replacement or to buy a lifetime buy of the component.

This concludes Chapter 29 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Assembly Sequence and Process Control, which defines the order of assembly steps and the quality checks at each step.

# Chapter 30: Assembly Sequence and Process Control

The assembly sequence defines the order in which the components are attached to the motherboard substrate. The sequence is designed to minimize the risk of damage to the components and to maximize the yield. The sequence is validated by building pilot units and by running design of experiments to optimize the process parameters.

The first step in the assembly sequence is the attachment of the interposer to the substrate. The interposer is attached using thermocompression bonding with 50-micron pitch solder bumps. The bonding process uses a temperature of 350 degrees Celsius and a force of 50 Newtons per interposer. The process takes 10 seconds per interposer.

The second step is the attachment of the HBM3e memory stacks to the interposer. The memory stacks are attached using thermocompression bonding with 20-micron pitch solder bumps. The bonding process uses a temperature of 350 degrees Celsius and a force of 20 Newtons per stack. The process takes 10 seconds per stack, for a total of 80 seconds per blade.

The third step is the hybrid bonding of the chiplets to the interposer. The chiplets are attached using the hybrid bonding process described in Chapter 16. The bonding process uses a temperature of 400 degrees Celsius and a force of 50 Newtons per chiplet. The process takes 1 second per chiplet, for a total of 1,296 seconds (21.6 minutes) per blade.

The fourth step is the underfill of the chiplets. Underfill is a epoxy material that is injected under the chiplets to fill the gap between the chiplet and the interposer. The underfill strengthens the bond and protects the connections from moisture and contamination. The underfill is cured at 150 degrees Celsius for 1 hour.

The fifth step is the attachment of the NAND flash chips to the substrate. The flash chips are attached using reflow soldering, as described in Chapter 18. The reflow process takes 5 minutes per blade.

The sixth step is the attachment of the decoupling capacitors and other passive components. The passives are attached using reflow soldering, as described in Chapter 18. The reflow process takes 5 minutes per blade.

The seventh step is the attachment of the optical transceivers to the substrate. The transceivers are attached using flip-chip bonding with 50-micron pitch solder bumps. The bonding process uses a temperature of 260 degrees Celsius and a force of 10 Newtons per transceiver. The process takes 10 seconds per transceiver, for a total of 2 minutes per blade.

The eighth step is the attachment of the edge connector to the substrate. The edge connector is attached using through-hole soldering. The connector is inserted into plated through-holes and then wave-soldered. The process takes 1 minute per blade.

The ninth step is the application of the thermal encasement. The pyrolytic graphite sheets are laminated to the substrate using the process described in Chapter 10. The lamination takes 10 minutes per blade.

The tenth step is the attachment of the cold plate or heat spreader. The cold plate is attached to the thermal encasement using spring-loaded clamps. The attachment takes 1 minute per blade.

The assembly sequence is controlled by a manufacturing execution system that tracks every blade through every step. The MES records the serial number of each component, the process parameters, and the results of any tests. The MES also enforces the process flow, preventing operators from skipping steps.

The process control is maintained by statistical process control charts. The SPC charts track key process parameters, such as temperature, force, and alignment. When a parameter drifts outside the control limits, the process is stopped and the cause is investigated. The goal is to maintain the process in a state of statistical control.

The assembly sequence is validated by building pilot units. The pilot units are tested to ensure that they meet the performance and reliability requirements. The results of the pilot units are used to adjust the process parameters before volume production.

This concludes Chapter 30 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Quality Assurance and Yield Management, which ensures that the blades meet the quality targets.

# Chapter 31: Quality Assurance and Yield Management

Quality assurance is the set of activities that ensure that the blades meet the specified quality and reliability targets. Yield management is the set of activities that maximize the number of good blades produced from each manufacturing lot. The quality assurance and yield management teams work together to identify and correct defects in the manufacturing process.

The quality assurance team is responsible for incoming inspection, in-process inspection, and final test. The team uses statistical sampling plans to inspect components and assemblies. The team also maintains the quality management system, which is certified to ISO 9001.

The incoming inspection team inspects every component before it is released to the manufacturing floor. The inspection includes visual inspection, dimensional measurement, and electrical test. Components that fail the inspection are returned to the supplier. The incoming inspection has a target of zero defects.

The in-process inspection team inspects the blades at critical steps in the assembly sequence. The inspections include automated optical inspection after solder paste printing, after component placement, and after reflow. The inspections also include X-ray inspection of the solder joints. The in-process inspection has a target of 99 percent defect coverage.

The final test team tests every blade before it is shipped to the customer. The final test includes the power-on self-test and the built-in self-test described in Chapter 20. The final test also includes a 24-hour burn-in test. Blades that fail the final test are sent to the repair station for rework.

The yield management team tracks the yield at each step of the manufacturing process. The team uses Pareto charts to identify the most common defects and to prioritize improvement efforts. The team also uses design of experiments to optimize the process parameters.

The overall yield for the blade is the product of the yields at each step. The target overall yield is 80 percent for the 100TB configuration. This means that 80 percent of the blades that start the assembly process will pass the final test and be shipped to customers.

The yield is improved by a continuous improvement process. The team identifies the root cause of defects, implements corrective actions, and verifies that the corrective actions are effective. The team also works with the design team to improve the design for manufacturability.

The quality assurance and yield management teams are essential for the commercial success of the PIP CISC platform. They ensure that the blades are reliable and that the manufacturing cost is competitive. The teams are staffed by experienced engineers who have worked on similar high-end server products.

This concludes Chapter 31 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Firmware Boot ROM and Initialization Microcode, which is the first code to run on the blade.

# Chapter 32: Firmware Boot ROM and Initialization Microcode

The firmware boot ROM is the first code that executes on the PIP CISC blade. The boot ROM is stored in a read-only memory embedded in each System core chiplet. The boot ROM contains the first-stage bootloader, which initializes the minimal hardware required to load the second-stage bootloader from flash. The boot ROM is written in assembly language and is optimized for size and speed.

The boot ROM begins execution at power-on reset. The first instruction is a jump to the start of the boot ROM code. The boot ROM first initializes the stack pointer and the global pointer. The boot ROM then configures the clock generator to run at 100 MHz, which is the slowest stable frequency.

The boot ROM next initializes the memory controller. The boot ROM writes to the memory controller registers to set the timing parameters for the HBM3e memory stacks. The boot ROM then runs a quick memory test to verify that the memory is working. The memory test writes a pattern to the first megabyte of memory and reads it back.

The boot ROM next initializes the flash controller. The boot ROM reads the identification page of the first NAND flash chip to determine the type and capacity of the flash. The boot ROM then loads the second-stage bootloader from flash into memory.

The second-stage bootloader is a larger program that initializes the rest of the hardware and loads the operating system. The second-stage bootloader is written in C and is stored in a reserved area of the flash. The second-stage bootloader is signed with a digital signature to prevent tampering.

The boot ROM verifies the digital signature of the second-stage bootloader before executing it. The boot ROM contains a public key that is used to verify the signature. If the signature is valid, the boot ROM jumps to the second-stage bootloader. If the signature is invalid, the boot ROM halts and lights a red LED.

The second-stage bootloader initializes the optical transceivers and the PIP-Fabric. The second-stage bootloader also initializes the directory cache and the TLB. The second-stage bootloader then loads the operating system from the flash into memory.

The operating system is stored in a reserved area of the flash. The operating system is signed with a digital signature, and the second-stage bootloader verifies the signature before loading it. If the signature is valid, the second-stage bootloader jumps to the operating system entry point.

The initialization microcode is a set of micro-operations that implement the complex system instructions, such as SYSENTER and SYSEXIT. The microcode is stored in a read-only memory embedded in each System core chiplet. The microcode is written in a proprietary microcode language and is assembled by a microcode assembler.

The microcode is executed by the microcode sequencer when a complex instruction is decoded. The microcode sequencer fetches micro-operations from the microcode ROM and executes them one by one. The microcode sequencer can also branch and loop, allowing complex sequences of micro-operations.

The microcode is optimized for speed. The most common microcode routines, such as the SYSENTER handler, are placed in fast memory and are executed in a few cycles. The less common routines are placed in slower memory and may take many cycles to execute.

The boot ROM and initialization microcode are critical for the correct operation of the PIP CISC platform. They are thoroughly tested by simulation and by execution on prototype hardware. The boot ROM and microcode are stored in one-time programmable memory and cannot be changed after the blade is manufactured.

This concludes Chapter 32 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Debugging and Diagnostic Interfaces, which allow engineers to debug the hardware and software.

# Chapter 33: Debugging and Diagnostic Interfaces

The debugging and diagnostic interfaces allow engineers to debug the hardware and software of the PIP CISC platform. The interfaces include JTAG for debugging the chiplets, a serial console for debugging the firmware, and a network interface for remote debugging. The interfaces are accessible through the edge connector and through dedicated debug connectors on the motherboard.

The JTAG interface is the primary debug interface for the chiplets. Each chiplet has a JTAG port that is daisy-chained together. The JTAG chain allows an external debugger to access the internal registers of the chiplets and to control the execution of the cores. The JTAG interface is used during manufacturing to test the chiplets and during development to debug the hardware.

The JTAG interface uses the standard 20-pin connector defined by the IEEE 1149.1 standard. The connector has pins for TCK, TMS, TDI, TDO, and TRST. The JTAG interface operates at 10 MHz and can be driven by any standard JTAG debugger.

The serial console interface provides a text-based console for debugging the firmware. The serial console is implemented on a UART that is accessible through a dedicated connector on the edge connector. The serial console operates at 115,200 baud and uses 8-N-1 formatting. The serial console is used to print debug messages and to accept commands from the debugger.

The network interface provides a remote debug interface for the operating system. The network interface is implemented on the same Ethernet port that is used for normal network communication. The debug interface uses a proprietary protocol that allows the debugger to access the memory and registers of the blade remotely.

The diagnostic interfaces also include a set of test points on the motherboard. The test points are connected to critical signals, such as the clock, the reset, and the power good signals. The test points are used by engineers to measure the signals with an oscilloscope or a logic analyzer.

The debugging and diagnostic interfaces are essential for the development of the PIP CISC platform. They allow engineers to find and fix bugs quickly, reducing the time to market. The interfaces are also used by field service engineers to diagnose problems in the field.

This concludes Chapter 33 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Field Upgrade and Repair Procedures, which allow customers to upgrade and repair the blades in the field.

# Chapter 34: Field Upgrade and Repair Procedures

The field upgrade and repair procedures allow customers to upgrade the components of the PIP CISC blade and to replace failed components. The procedures are designed to be performed by trained field service engineers with standard tools. The procedures are documented in a service manual that is provided to customers.

The most common field upgrade is the replacement of the NAND flash chips. The flash chips are soldered to the motherboard and cannot be replaced in the field. However, the flash chips are rated for 5 years of continuous operation, which is longer than the expected life of the blade. If a flash chip fails, the entire blade must be replaced.

The second most common field upgrade is the replacement of the optical transceivers. The optical transceivers are attached to the motherboard with solder and cannot be replaced in the field. However, the optical transceivers are rated for 10 years of continuous operation, which is longer than the expected life of the blade. If a transceiver fails, the entire blade must be replaced.

The third most common field upgrade is the replacement of the decoupling capacitors. The decoupling capacitors are surface-mount components that can be replaced in the field with a hot air rework station. The service manual provides instructions for replacing the capacitors.

The fourth most common field upgrade is the replacement of the edge connector. The edge connector is a through-hole component that can be replaced in the field with a soldering iron. The service manual provides instructions for replacing the edge connector.

The field repair procedures are similar to the upgrade procedures. The failed component is removed and a new component is soldered in its place. The blade is then tested to verify that the repair was successful.

The field upgrade and repair procedures are designed to minimize the downtime of the blade. The average time to replace a component is 1 hour. The blade is powered off during the repair, so the downtime is the same as the repair time.

The field upgrade and repair procedures are essential for the maintainability of the PIP CISC platform. They allow customers to keep their blades operating for the full 10-year life of the product.

This concludes Chapter 34 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Environmental Compliance and Certification, which ensures that the blades meet environmental regulations.

# Chapter 35: Environmental Compliance and Certification

The PIP CISC platform must comply with environmental regulations around the world. The most important regulations are the Restriction of Hazardous Substances Directive (RoHS) and the Waste Electrical and Electronic Equipment Directive (WEEE) in Europe, and similar regulations in other countries. The platform must also comply with energy efficiency regulations, such as ENERGY STAR.

The RoHS directive restricts the use of lead, mercury, cadmium, hexavalent chromium, polybrominated biphenyls, and polybrominated diphenyl ethers in electrical and electronic equipment. The PIP CISC platform uses lead-free solder (tin-silver-copper) for all soldered connections. The platform also uses no other restricted substances. The platform is certified as RoHS compliant by an independent testing laboratory.

The WEEE directive requires manufacturers to take back and recycle their products at the end of life. The PIP CISC platform is designed for disassembly and recycling. The aluminum enclosure and the copper cold plate are easily separated from the motherboard. The motherboard is sent to a specialized recycler that recovers the precious metals and the silicon.

The ENERGY STAR program certifies products that meet energy efficiency guidelines. The PIP CISC platform meets the ENERGY STAR requirements for servers. The platform has a power management system that puts idle cores into low-power states and that reduces the clock frequency when the temperature is low. The platform also has a high-efficiency power supply that converts 48 volts to the core voltages with 95 percent efficiency.

The PIP CISC platform also complies with the Safety of Information Technology Equipment standard (IEC 62368-1). The platform is certified by a Nationally Recognized Testing Laboratory, such as Underwriters Laboratories. The certification verifies that the platform does not pose a fire, shock, or mechanical hazard.

The environmental compliance and certification are essential for selling the PIP CISC platform in global markets. The platform is designed with compliance in mind from the beginning, reducing the time and cost of certification.

This concludes Chapter 35 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Security Features and Tamper Resistance, which protect the platform from physical and logical attacks.

# Chapter 36: Security Features and Tamper Resistance

The PIP CISC platform includes security features that protect the hardware and software from physical and logical attacks. The security features include a hardware root of trust, secure boot, memory encryption, and tamper detection. The security features are designed to meet the requirements of high-security applications, such as government and financial services.

The hardware root of trust is a small, immutable circuit that generates and stores cryptographic keys. The root of trust is implemented in the System core chiplet and is isolated from the rest of the chip by a hardware firewall. The root of trust generates the keys for secure boot, memory encryption, and network encryption.

The secure boot feature ensures that only signed software can run on the blade. The boot ROM verifies the digital signature of the second-stage bootloader, and the second-stage bootloader verifies the signature of the operating system. If any signature is invalid, the blade halts and lights a red LED.

The memory encryption feature encrypts all data stored in the HBM3e memory and in the NAND flash. The encryption uses the Advanced Encryption Standard with 256-bit keys. The keys are stored in the root of trust and are never exposed to the software. The encryption hardware is integrated into the memory controller and operates at the full memory bandwidth with no performance penalty.

The tamper detection feature detects physical attempts to access the internal components of the blade. The blade has a mesh of thin wires on the top and bottom of the motherboard. If a wire is broken, the tamper detection circuit erases the encryption keys and disables the blade. The tamper detection circuit is powered by a battery that lasts for 10 years.

The security features are designed to be transparent to the user. The user does not need to enable or configure the security features; they are always active. The security features add 5 percent to the cost of the blade, which is acceptable for high-security applications.

This concludes Chapter 36 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Performance Characterization and Benchmarks, which measure the performance of the PIP CISC platform.

# Chapter 37: Performance Characterization and Benchmarks

The performance characterization and benchmarks measure the performance of the PIP CISC platform. The benchmarks include standard industry benchmarks, such as SPEC CPU, SPECrate, and LINPACK, as well as custom benchmarks that exercise the unique features of the platform. The performance results are used to validate the design and to market the product.

The SPEC CPU benchmark measures the integer and floating-point performance of a single core. The PIP CISC Math core achieves a SPECint score of 15 and a SPECfp score of 30 at 2 GHz. These scores are comparable to the best desktop processors on the market.

The SPECrate benchmark measures the throughput of all cores on a blade. The PIP CISC blade achieves a SPECint_rate score of 150,000 and a SPECfp_rate score of 300,000. These scores are 10 times higher than the best server processors on the market.

The LINPACK benchmark measures the performance of dense linear algebra. The PIP CISC blade achieves 10 teraflops of double-precision performance, which is comparable to a small supercomputer. The LINPACK performance is limited by the memory bandwidth, not by the compute cores.

The custom benchmarks include the HMM_FORWARD benchmark, which measures the performance of the HMM instructions. The HMM_FORWARD benchmark processes a 256-state HMM with 1,000 observations in 10 microseconds, which is 1,000 times faster than a software implementation.

The custom benchmarks also include the convolution benchmark, which measures the performance of the CONV instruction. The convolution benchmark processes a 224x224 image with a 3x3 kernel in 10 microseconds, which is 100 times faster than a software implementation.

The performance characterization is performed by the validation team using automated test scripts. The results are stored in a database and are used to track performance over time. The performance results are also used to tune the compiler and the operating system.

This concludes Chapter 37 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Design Rules and Layout Guidelines for Partners, which allow third parties to design components for the PIP CISC platform.

# Chapter 38: Design Rules and Layout Guidelines for Partners

The design rules and layout guidelines allow third parties to design components for the PIP CISC platform. The components include expansion cards, storage devices, and optical transceivers. The design rules specify the physical dimensions, the electrical characteristics, and the thermal requirements. The layout guidelines specify the placement of components on the board and the routing of traces.

The design rules for expansion cards are based on the PCIe standard. The expansion cards must be 167.65mm long and 111.15mm tall. The cards must have a PCIe x16 edge connector with 164 pins. The cards must comply with the PCIe 5.0 specification, which specifies the signaling and the power delivery.

The design rules for storage devices are based on the M.2 standard. The storage devices must be 22mm wide and 80mm long. The devices must have an M.2 M-key edge connector with 75 pins. The devices must comply with the NVMe 2.0 specification, which specifies the command set and the performance requirements.

The design rules for optical transceivers are based on the QSFP-DD standard. The transceivers must be 18.35mm wide and 89.4mm long. The transceivers must have a QSFP-DD edge connector with 76 pins. The transceivers must comply with the 800G-SR8 specification, which specifies the optical and electrical characteristics.

The layout guidelines specify the placement of components on the board. The guidelines recommend that high-speed components be placed near the edge connector to minimize trace lengths. The guidelines also recommend that decoupling capacitors be placed near the power pins of each component.

The layout guidelines also specify the routing of traces. The guidelines recommend that high-speed traces be routed as differential pairs with controlled impedance. The guidelines also recommend that traces be kept away from the edges of the board to reduce radiation.

The design rules and layout guidelines are documented in a reference manual that is provided to partners. The manual also includes a reference design that partners can use as a starting point for their own designs.

This concludes Chapter 38 of the Motherboard Design & Manufacturing Specification. The next chapter will describe the Future Scalability and Next-Generation Roadmap, which outlines the future direction of the PIP CISC platform.

# Chapter 39: Future Scalability and Next-Generation Roadmap

The future scalability and next-generation roadmap describe the planned improvements to the PIP CISC platform. The roadmap includes increases in core count, memory capacity, bandwidth, and power efficiency. The roadmap also includes new features, such as support for new data types and new algorithms.

The first generation of the PIP CISC platform has 10,000 Math cores, 64GB of memory, and 100TB of storage. The second generation will have 20,000 Math cores, 128GB of memory, and 200TB of storage. The second generation will be manufactured on TSMC's 2nm process, which will provide a 30 percent increase in transistor density and a 20 percent reduction in power consumption.

The second generation will also have support for new data types, such as 8-bit floating-point and 4-bit integer. The new data types will accelerate AI inference workloads, which can tolerate lower precision. The new data types will be implemented by extending the vector ALUs.

The second generation will also have support for new algorithms, such as spiking neural networks and probabilistic computing. The new algorithms will be implemented by adding new instructions to the ISA. The new instructions will be backward compatible with the first generation.

The third generation of the PIP CISC platform will have 40,000 Math cores, 256GB of memory, and 400TB of storage. The third generation will be manufactured on TSMC's 1.4nm process, which will provide another 30 percent increase in transistor density. The third generation will also have support for optical interconnects between chiplets, replacing the electrical interconnects on the interposer.

The roadmap is reviewed annually by the product management team. The team adjusts the roadmap based on customer feedback and on the progress of the technology. The goal is to release a new generation every two years.

This concludes Chapter 39 of the Motherboard Design & Manufacturing Specification. The appendices will provide additional technical details, including pinouts, timing diagrams, and mechanical drawings.

# Chapter 40: Appendices

The appendices provide additional technical details that are not covered in the main body of the specification. The appendices include pinout tables, timing diagrams, mechanical drawings, and test vectors.

Appendix A provides the pinout of the edge connector. The pinout table lists the signal name, the pin number, and the function for each pin. The table also indicates whether the pin is differential or single-ended, and whether it is powered by 0.8V, 1.2V, 1.8V, 3.3V, or 48V.

Appendix B provides the timing diagrams for the high-speed interfaces. The diagrams show the relationship between the clock and the data for the memory interface, the optical interface, and the PCIe interface. The diagrams also show the setup and hold times, the propagation delays, and the jitter requirements.

Appendix C provides the mechanical drawings of the blade, the rack, and the optical transceivers. The drawings include the dimensions, the tolerances, and the materials. The drawings are provided in DWG and PDF formats.

Appendix D provides the test vectors for the built-in self-test. The test vectors are patterns that are applied to the chiplets to verify their functionality. The test vectors are provided in a format that can be loaded into the automatic test equipment.

Appendix E provides the bill of materials in spreadsheet format. The spreadsheet includes the part number, description, quantity, supplier, and cost for each component. The spreadsheet is updated quarterly.

Appendix F provides the reliability prediction. The reliability prediction is calculated using the MIL-HDBK-217 standard. The prediction includes the failure rate for each component and the overall mean time between failures for the blade.

Appendix G provides the thermal model. The thermal model is a simulation of the temperature distribution on the blade. The model includes the power dissipation of each component and the thermal resistance of the cooling system.

Appendix H provides the signal integrity simulation results. The simulation results show the eye diagram for each high-speed interface. The results also show the crosstalk and the return loss.

Appendix I provides the power integrity simulation results. The simulation results show the impedance of the power distribution network and the voltage droop during transient events.

Appendix J provides the electromagnetic compatibility test results. The test results show the radiated and conducted emissions from the blade. The results also show the immunity of the blade to external interference.

This concludes the Motherboard Design & Manufacturing Specification for the PIP CISC Unified Compute Platform. The specification provides the complete technical details required to manufacture the motherboard, assemble the blades, and test the final product. The specification is intended for TSMC's manufacturing engineers and for the engineers at partner companies who will build components for the platform.

