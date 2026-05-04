

import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================
# 🔐 EMAIL CONFIG
# =========================

MY_EMAIL = "swapstersupport@gmail.com"
MY_PASSWORD = "zuou voaw uzzy otlb"

# 👉 JIS EMAIL PAR SAB SEND KARNA HAI
RECEIVER_EMAIL = "muhammadmeesam90@gmail.com"   # same ya koi aur

# =========================
# 📅 TODAY
# =========================
today = datetime.datetime.now()
today_day = today.day

# =========================
# 📂 LOAD CSV
# =========================
data = pd.read_csv("payment.csv")

# =========================
# 🔁 LOOP
# =========================
for index, row in data.iterrows():

    if row["due_day"] == today_day:

        msg = MIMEMultipart("alternative")
        msg["From"] = MY_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = f"Payment Reminder - {row['name']}"

        html = f"""
        <html>
        <body style="font-family: Arial; background:#f6f6f6; padding:20px;">
            <div style="max-width:600px; margin:auto; background:white; padding:20px; border-radius:10px;">

                <h2 style="text-align:center;">Payment Invoice</h2>
                <hr>

                <p><strong>Name:</strong> {row['name']}</p>
                <p><strong>Service:</strong> {row['service']}</p>

                <table style="width:100%; border-collapse:collapse; margin-top:20px;">
                    <tr style="background:#eee;">
                        <th style="padding:10px; border:1px solid #ddd;">Description</th>
                        <th style="padding:10px; border:1px solid #ddd;">Amount</th>
                    </tr>
                    <tr>
                        <td style="padding:10px; border:1px solid #ddd;">
                            {row['service']} Subscription
                        </td>
                        <td style="padding:10px; border:1px solid #ddd;">
                            Rs {row['price']}
                        </td>
                    </tr>
                </table>

                <p style="margin-top:20px;">
                    Reminder: {row['name']} ka payment due hai.
                </p>

            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.send_message(msg)

            print(f"✅ Reminder sent for {row['name']}")

        except Exception as e:
            print(f"❌ Error: {e}")

print("🚀 Done")