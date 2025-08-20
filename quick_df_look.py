import pandas as pd
from rich.pretty import pprint

df = pd.read_excel("./to_invoice_before_sorting.xlsx")
pprint(df)

pprint(df.describe())

pprint(df.dtypes)

pprint(df.columns)
