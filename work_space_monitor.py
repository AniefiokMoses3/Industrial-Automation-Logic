import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

# ==========================================================
# MODULE: NETWORK ALERT SYSTEM
# ==========================================================
def trigger_production_alert(current_size):
    smtp_server = "64.233.184.108"
    smtp_port = 587

    # SYSTEM ACCESS CREDENTIALS
    sender_email = "your_authenticated_sender_email@gmail.com"
    receiver_email = "production_manager_or_your_recipient@email.com"
    sender_password = "your_16_character_app_password_here"

    # LET'S COMPILE THE MINE ENVELOP METADATA
    subject = "Alert! Workspace Storage Threshold Exceeded."
    body = (
        f"INDUSTRIAL INFASTRUCTURE MONITORING REPORT\n"
        f"------------------------------------------------\n"
        f"TIMESTAMP:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Detected Footprint: {current_size:.2f}\n"
        f"Operational Budget: 1000.00 KB \n\n"
        f"Action Required: Please audit the local repository for oversized footprints."
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # LET'S EXECUTE NETWORK LOGIC TRANSMISSION PIPELINE
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() # Let's upgrade line to secure TLS encription
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("[ALARM SYSTEM] Production alert email successfully dispatched.")
    except Exception as network_error:
        print(f"[ALARM SYSTEM CRITICAL FAILURE] Transmission blocked: {network_error}")

# =======================================================================================
# MAIN AUTOMATION EXECUTION ENGINE
# =======================================================================================
            
folder_path = os.getcwd() 
file_path = os.listdir(folder_path)

total_assets_count = 0
total_work_space_size_kb = 0.0

critical_extentions = (".png", ".project", ".md", ".py")
print("SCANNING WORK SPACE FOR CRITICAL ASSETS...\n")
print("-" * 50)

for file in file_path:
    if file.endswith(critical_extentions):
        full_path = os.path.join(folder_path, file)

        file_size_kb = os.path.getsize(full_path) / 1024

        print(f"Assets: {file:<35} | size: {file_size_kb: .2f} KB")

        total_assets_count += 1
        total_work_space_size_kb += file_size_kb
#Log metrics to our running append file
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("Work_Space_Report.txt", "a") as report:
    report.write(f"[{current_time}] Asset Checked: {total_assets_count} | Total Footprint: {total_work_space_size_kb: .2F} KB \n")

print("-" * 50)
print(f"Audit Complete! Total Workspace Footprint: {total_work_space_size_kb: .2f} KB")  

# --------- COMPARATIVE AUTOMATION SWITCH ---------------
if total_work_space_size_kb > 1000.00:
    print("\n[WARNING] Storage budget exceeded! initializing alert network...")
    trigger_production_alert(total_work_space_size_kb)
else:
    print("\n[STATUS] Workspace operations within safe threshold limits.")    


