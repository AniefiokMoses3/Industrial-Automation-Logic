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

##  Infrastructure Automation Subsystem (Python & Docker v2)

To support the deployment and integrity of our industrial control environment, this repository includes an automated, network-aware workspace monitor running as a persistent background daemon (`work_space_monitor.py`).

###  Core Architecture & Features
- **Continuous Worker Loop:** Upgraded from a transient script to a persistent background service using an infinite execution engine with a managed 1-hour hibernation throttle (`time.sleep(3600)`).
- **Targeted Asset Auditing:** Explicitly tracks critical industrial files (`.project`, `.py`, `.md`, `.png`) while filtering out background storage noise.
- **Persistent Ledger Logging:** Automatically generates and appends system telemetry to a historical file (`Work_Space_Report.txt`) for audit compliance.
- **Automated Alarm Matrix:** Features a conditional safety switch that acts exactly like a PLC physical high-limit alarm. If the total storage footprint crosses a setpoint threshold ($1000\text{ KB}$), it initializes the network alerting sequence.

###  Secure SMTP Alert Transmission Pipeline
When triggered by a threshold overrun, the script establishes an encrypted communication tunnel to dispatch emergency notifications straight to the production engineering team.

```text
          DATA ENVELOPE GENERATION & ROUTING PIPELINE
+-------------------------------------------------------------+
| 1. COMPILE PAYLOAD (email.mime.text.MIMEText Object)        |
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

 **Defensive Exception Handling:** Encapsulates network operations inside resilient `try/except` interlocking blocks to ensure network or DNS drops fail gracefully without crashing core logging operations.
 **Low-Level Socket Architecture:** Utilizes direct routing vectors to maintain high-availability data dispatches across isolated network interfaces.

###  Execution & Deployment Guide (Dockerized Background Daemon)
To deploy this monitoring agent seamlessly as an isolated, persistent service on any infrastructure, follow these steps:
```bash
docker build -t work-space-monitor:v2 .

Run the container in Detached Mode (-d) so it runs permanently in the background, injecting secure environment credentials and mapping a local storage volume to allow the ledger logs to persist on your host machine:

docker run -d --name workspace-agent `
  -e EMAIL_USER="your_authenticated_sender@gmail.com" `
  -e EMAIL_PASS="your_16_character_app_password" `
  -e EMAIL_RECEIVER="production_manager@email.com" `
  -v "${PWD}:/app" `
  work-space-monitor:v2

  To inspect the real-time runtime tracking logs of your background daemon:

  docker logs workspace-agent

  ### System Ledger Sample Output (`Work_Space_Report.txt`)
The daemon maintains a physical running file on the host machine containing historical audit logs formatted as follows:
```text
[2026-05-29 15:40:12] Asset Checked: 6 | Total Footprint: 1107.14 KB 
[2026-05-29 16:40:12] Asset Checked: 6 | Total Footprint: 1107.14 KB