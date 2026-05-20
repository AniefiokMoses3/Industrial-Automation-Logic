# Industrial Automation & Control Logic Library

Welcome to my professional portfolio repository. This space serves as an engineering showcase combining industrial automation logic with modern documentation standards.

## Active Project: Project Aries (Sequential Motor Control)

### Overview
This project features a two-stage sequential motor control circuit built using IEC 61131-3 Ladder Logic. It implements a critical safety-on delay sequence designed to protect heavy rotating machinery and plant personnel before system activation.

### Technical Implementation
Software Environment: CODESYS V3.5 SP22 Patch 1
Latching Logic: Developed an interlocking start/stop network to maintain state using momentary inputs.
Timing Subsystem: Configured a TON (Timer On Delay) function block (`T#5s`) to act as a deterministic safety window.
HMI Dashboard: Integrated a graphical Human-Machine Interface containing custom-mapped operational push-buttons and a dynamic status indicator lamp.

### Logic Design Architecture
Network 1: Handles primary system ignition and latching memory state.
Network 2: Monitors runtime constraints and triggers the 5-second accumulation parameter before validating the system-ready status.
