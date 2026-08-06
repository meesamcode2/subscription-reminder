import datetime
import os
import smtplib
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


MY_EMAIL = os.getenv("EMAIL")
MY_PASSWORD = os.getenv("PASSWORD")
RECEIVER_EMAIL = "muhammadmeesam90@gmail.com"

if not MY_EMAIL:
    raise RuntimeError("GitHub secret EMAIL missing hai.")

if not MY_PASSWORD:
    raise RuntimeError("GitHub secret PASSWORD missing hai.")


# Manual testing mein TEST_DAY use hoga,
# scheduled run mein Pakistan ka current day.
test_day = os.getenv("TEST_DAY", "").strip()

if test_day:
    today_day = int(test_day)
    print(f"Test mode: due_day {today_day}")
else:
    pakistan_time = datetime.datetime.now(ZoneInfo("Asia/Karachi"))
    today_day = pakistan_time.day
    print(f"Pakistan date: {pakistan_time:%Y-%m-%d %H:%M}")


csv_path = Path(__file__).with_name("payment.csv")

if not csv_path.exists():
    raise FileNotFoundError(f"CSV file nahi mili: {csv_path}")

data = pd.read_csv(csv_path)
required_columns = {"name", "service", "due_day", "price"}

if not required_columns.issubset(data.columns):
    missing = required_columns - set(data.columns)
    raise ValueError(f"CSV columns missing hain: {missing}")


due_rows = data[data["due_day"].astype(int) == today_day]

if due_rows.empty:
    print(f"Due day {today_day} ke liye koi reminder nahi hai.")
else:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        connection.login(MY_EMAIL, MY_PASSWORD)

        for _, row in due_rows.iterrows():
            msg = MIMEMultipart("alternative")
            msg["From"] = MY_EMAIL
            msg["To"] = RECEIVER_EMAIL
            msg["Subject"] = f"Payment Reminder - {row['name']}"

            html = f"""
            <html>
            <body style="font-family:Arial; background:#f6f6f6; padding:20px;">
                <div style="
                    max-width:600px;
                    margin:auto;
                    background:white;
                    padding:20px;
                    border-radius:10px;
                ">
                    <h2 style="text-align:center;">Payment Invoice</h2>
                    <hr>

                    <p><strong>Name:</strong> {row['name']}</p>
                    <p><strong>Service:</strong> {row['service']}</p>

                    <table style="
                        width:100%;
                        border-collapse:collapse;
                        margin-top:20px;
                    ">
                        <tr style="background:#eeeeee;">
                            <th style="padding:10px; border:1px solid #dddddd;">
                                Description
                            </th>
                            <th style="padding:10px; border:1px solid #dddddd;">
                                Amount
                            </th>
                        </tr>

                        <tr>
                            <td style="padding:10px; border:1px solid #dddddd;">
                                {row['service']} Subscription
                            </td>
                            <td style="padding:10px; border:1px solid #dddddd;">
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
            connection.send_message(msg)

            print(f"Reminder sent successfully for {row['name']}")

print("Done")
