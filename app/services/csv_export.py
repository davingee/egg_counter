import csv
import smtplib
from email.message import EmailMessage
from pathlib import Path
from app.clients import db
from shared import helper
from app.schemas import DateSelection


def send_csv_email(
    smtp_server,
    port,
    sender_email,
    sender_password,
    recipient_email,
    file_path,
    content,
    subject="Eggs Report CSV",
):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(content)

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(), maintype="text", subtype="csv", filename=Path(file_path).name
        )

    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)


async def export_eggs_to_csv(selection: DateSelection):
    query = """
    SELECT * FROM eggs
    WHERE date >= :start
    ORDER BY date ASC
    """
    rows = await db.fetch_all(query=query, values={"start": selection.date})
    csv_path = helper.csv_name(selection.date)
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        if rows:
            writer.writerow(rows[0].keys())
            for row in rows:
                writer.writerow(row.values())
        else:
            print("No rows found.")
    return csv_path


def cleanup_egg_csvs(directory="."):
    base_path = Path(directory)
    for file in base_path.glob("eggs_today_*.csv"):
        try:
            file.unlink()
        except Exception:
            pass
