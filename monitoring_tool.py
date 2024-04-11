import psutil
import csv
import curses
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Email configuration
SMTP_SERVER = 'your_smtp_server'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email_username'
SMTP_PASSWORD = 'your_email_password'
RECIPIENT_EMAIL = 'recipient@example.com'

# Monitoring thresholds
MEMORY_THRESHOLD = 90  # Percent
CPU_THRESHOLD = 80  # Percent

# Function to collect system metrics
def collect_system_metrics():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_io = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

    return cpu_percent, memory_percent, disk_usage, network_io

# Function to write metrics to CSV file
def write_to_csv(metrics):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Current timestamp with microseconds
    metrics.insert(0, timestamp)  # Insert timestamp at the beginning of the metrics list

    with open('metrics.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(metrics)

# Function to send email notification
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, msg.as_string())
    server.quit()

# Function to display interactive dashboard using curses
def display_dashboard(stdscr):
    stdscr.clear()
    curses.curs_set(0)  # Hide cursor

    # Define colors
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        stdscr.clear()

        # Get system metrics
        cpu_percent, memory_percent, disk_percent, network_io = collect_system_metrics()

        # Print header
        stdscr.addstr(1, 1, "System Metrics", curses.A_BOLD | curses.color_pair(1))

        # Print CPU usage
        stdscr.addstr(3, 1, "CPU Usage:", curses.A_BOLD)
        stdscr.addstr(3, 15, f"{cpu_percent}%", curses.color_pair(2) if cpu_percent < 80 else curses.color_pair(3))

        # Print Memory usage
        stdscr.addstr(5, 1, "Memory Usage:", curses.A_BOLD)
        stdscr.addstr(5, 17, f"{memory_percent}%", curses.color_pair(2) if memory_percent < 90 else curses.color_pair(3))

        # Print Disk usage
        stdscr.addstr(7, 1, "Disk Usage:", curses.A_BOLD)
        stdscr.addstr(7, 14, f"{disk_percent}%", curses.color_pair(2) if disk_percent < 80 else curses.color_pair(3))

        # Print Network I/O
        stdscr.addstr(9, 1, "Network I/O:", curses.A_BOLD)
        stdscr.addstr(9, 15, f"{network_io} bytes", curses.A_DIM)

        # Print timestamp
        stdscr.addstr(12, 1, "Last Updated: " + time.strftime("%Y-%m-%d %H:%M:%S"), curses.A_BOLD | curses.A_DIM)

        stdscr.refresh()
        time.sleep(1)  # Update every 1 second

        # Write metrics to CSV
        metrics = [cpu_percent, memory_percent, disk_percent, network_io]
        write_to_csv(metrics)

        # Check for critical states and send email alert
        if memory_percent > MEMORY_THRESHOLD:
            send_email("Critical: High Memory Usage", f"Memory Usage is at {memory_percent}%")

        if cpu_percent > CPU_THRESHOLD:
            send_email("Critical: High CPU Usage", f"CPU Usage is at {cpu_percent}%")

        # Listen for user input (q to quit)
        key = stdscr.getch()
        if key == ord('q'):
            break

def main():
    # Initialize curses and display interactive dashboard
    curses.wrapper(display_dashboard)

if __name__ == "__main__":
    main()