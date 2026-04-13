import time

def send_welcome_email(user_email: str):
    print(f"[Background Task] Starting to send welcome email to: {user_email}")

    # This simulates the time it takes to connect to a Gmail/SMTP server
    time.sleep(5)  # Simulate time-consuming email sending
    print(f"[Background Task] Success! Welcome email sent to: {user_email}")
