from flask import Flask
import datetime
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():

    today_day = datetime.datetime.now().day
    data = pd.read_csv("payment.csv")

    result = []

    for index, row in data.iterrows():
        if row["due_day"] == today_day:
            result.append(f"{row['name']} - Rs {row['price']} ({row['service']})")

    if result:
        return "<br>".join(result)
    else:
        return "No reminders today"

if __name__ == "__main__":
    app.run(debug=True)