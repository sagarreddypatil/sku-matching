import polars as pl
from random import choice

pl.Config.set_fmt_str_lengths(99999)


def read_email(email_id: str) -> str:
    with open(f"data/emails/{email_id}.txt", "r") as f:
        return f.read()


ground_truth = pl.read_csv("data/ground_truth_df.csv")

email_ids = ground_truth["EmailId"].to_list()
email_texts = [read_email(eid) for eid in email_ids]

emails_df = pl.DataFrame({"EmailId": email_ids, "Email": email_texts})
ground_truth = ground_truth.join(emails_df, on="EmailId", how="left")

row = choice(ground_truth)
print(row)
email = row[0, "Email"]
sku = row[0, "Skus"]

open("email_input.txt", "w").write(email)
open("ground_truth.txt", "w").write(sku)

print(email)
print(sku)
