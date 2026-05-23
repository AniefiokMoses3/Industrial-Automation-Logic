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


---

##  Infrastructure Automation Subsystem (Python)

To support the deployment and integrity of our industrial control environment, this repository includes an automated, network-aware workspace monitor (`work_space_monitor.py`).

###  System Monitoring & Metrics Engine
The script interfaces directly with the host operating system file layers to audit engineering assets, track repository growth, and enforce storage safety parameters.

* **Multi-Asset Filtering:** Programmatically screens the workspace directory to catalog critical industrial project binaries (`.project`), documentation (`.md`), script logic (`.py`), and visual HMI layouts (`.png`).
* **Deterministic I/O Logging:** Appends continuous operational histories to a localized log (`Work_Space_Report.txt`) stamped with compliant ISO-8601 data tokens (`YYYY-MM-DD HH:MM:SS`) to prevent tracking data overwrites.
* **Automated Alarm Matrix:** Features a conditional safety switch that acts exactly like a PLC physical high-limit alarm. If the total storage footprint crosses a setpoint threshold ($1000\text{ KB}$), it initializes the network alerting sequence.

###  Secure SMTP Alert Transmission Pipeline
When triggered by a threshold overrun, the script establishes an encrypted communication tunnel to dispatch emergency notifications straight to the production engineering team.

DATA ENVELOPE GENERATION & ROUTING PIPELINE

```text
          DATA ENVELOPE GENERATION & ROUTING PIPELINE
+-------------------------------------------------------------+
| 1. COMPILE PAYLOAD (email.mime.text.MIMEText Object)         |
|    - Serialize metadata headers (Subject, From, To)          |
+-------------------------------------------------------------+
                              |
                              v  Passes stream to...
+-------------------------------------------------------------+
| 2. SECURE CARRIER TRANSPORT (smtplib.SMTP Engine)           |
|    - Dial Gateway (Port 587)                                |
|    - Upgrade line to TLS Encryption (server.starttls)        |
|    - Authenticate via Secure App Passwords                  |
+-------------------------------------------------------------+
                              |
                              v
                      [ DISPATCH INBOX ALERT ]
```

* **Defensive Exception Handling:** Encapsulates network operations inside resilient `try/except` interlocking blocks to ensure network or DNS drops fail gracefully without crashing core logging operations.
* **Low-Level Socket Architecture:** Utilizes direct routing vectors to maintain high-availability data dispatches across isolated network interfaces.

###  Execution & Deployment Instructions
To run a manual workspace infrastructure audit from your terminal, execute:
```powershell
python work_space_monitor.py