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

print(email)
print(sku)

"""
SAP,160007622,HREW RECT 1008/10 2 X 1 X .120W X 288   ,2042.0,CARBON TUBE RECTANGLE HREW    ,CARBON,TUBE,RECTANGLE,1008/1010,EXACT,,,,103400130799.0,11.0,11,288.0,IN,,,,,,,0.12,IN,2.0,IN,1.0,IN,,HR/EW-MECHANICAL,,NOT A SHORT,
SAP,100016705,HREW RECT 1008/10 PO 2 X 1 X .120W X 288,2042.0,CARBON TUBE RECTANGLE HREW P&O,CARBON,TUBE,RECTANGLE,1008/1010,EXACT,,PO,,103400131193.0,11.0,11,288.0,IN,,,,,,,0.12,IN,2.0,IN,1.0,IN,PO,HR/EW-MECHANICAL,,NOT A SHORT,
"""