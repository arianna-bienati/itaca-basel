#!/usr/bin/env python

import pandas as pd
import json
import re

def reversed_values(value):
    return abs(value - 3)  # substract the max value from all values and change negative to positive values to reverse order
def extract_numeric(column_name):
  matches = re.findall(r'\d+', column_name)
  return ''.join(matches)
RATINGS_SOURCE_PATH = "source/answers_20230904T0946.csv"

df = pd.read_csv(RATINGS_SOURCE_PATH)

COL_RECODING = {
    "Informazioni cronologiche": "timestamp",
    "ID valutatore": "rater_id",
    "ID testo": "text_id",
}

likert_colnames = []
for col in df.columns:
  if col not in list(COL_RECODING.keys()):
    likert_colnames.append(col)

LIKERT_COL_RECODING = {col: f"likert_{extract_numeric(col)}" for col in likert_colnames}

LIKERT_VAL_RECODING = {
    "3 - Del tutto d'accordo": 3,
    "2 - Un po’ d’accordo": 2,
    "1 - Un po’ in disaccordo": 1,
    "0 - Del tutto in disaccordo": 0,
    "Del tutto d'accordo": 3,
    "Un po’ d’accordo": 2,
    "Un po’ in disaccordo": 1,
    "Del tutto in disaccordo": 0,
}

REVERSED_VAL = ["likert_001", 
                "likert_005", 
                "likert_008", 
                "likert_009", 
                "likert_012", 
                "likert_015", 
                "likert_016", 
                "likert_018", 
                "likert_019", 
                "likert_025", 
                "likert_028", 
                "likert_029", 
                "likert_030", 
                "likert_032", 
                "likert_035", 
                "likert_036", 
                "likert_037", 
                "likert_039", 
                "likert_041", 
                "likert_042"]

with open("output/ratings_doc.md", "w", encoding="UTF-8") as f:
    items = {v: k[91:-1].strip() for k, v in LIKERT_COL_RECODING.items()} # k[91:-1] refers to the part of column name that contains the description of the item
    # marking reversed items in the description
    for key in items.keys():
      if key in REVERSED_VAL:
        items[key] = items[key] + "[REVERSED ITEM]"
    scale = {v: k for k, v in LIKERT_VAL_RECODING.items()}
    rev_scale = {reversed_values(v): k for k, v in LIKERT_VAL_RECODING.items()}
    f.write(
        f"""# `ratings.csv` legend

## Likert questions

Questions were administered with the following request:
```json
"Indica, per favore, il tuo grado di accordo o disaccordo con ciascuna affermazione."
```

The items to rate are recoded as:
```json
{json.dumps(items, indent=True, ensure_ascii=False)}
```

The rating scale is recoded as:
```json
{json.dumps(scale, indent=True, ensure_ascii=False)}
```
The rating scale for reversed items is recoded as:
```json
{json.dumps(rev_scale, indent=True, ensure_ascii=False)}
```

"""
    )

df.rename(columns=COL_RECODING, inplace=True)
df.rename(columns=LIKERT_COL_RECODING, inplace=True)
df.replace(LIKERT_VAL_RECODING, inplace=True)

# TODO: check correctness of IDs

# Of course we have duplicates...
dups = df.duplicated(subset=["rater_id", "text_id"], keep=False)
# ... but at least it's just 12 rows duplicated once and nothing worse.
assert 24 == dups.sum()
assert df[dups][["rater_id", "text_id"]].value_counts().eq(2).all()
# Of these, 10 are full duplicates and 14 have different ratings.
fubar = ~df[dups].drop(columns=["timestamp"]).duplicated(keep=False)
assert {False: 12, True: 12} == fubar.value_counts().to_dict()
# Regardless, our strategy is to keep the last one and cross our fingers.
# Note we're not checking the timestamp and using the ingestion order instead.
df.drop(columns=["timestamp"], inplace=True)
df.drop_duplicates(subset=["rater_id", "text_id"], keep="last", inplace=True)

# remove rater "BiA" from the raters_ids because she was not in the raters' team. Just contributed with 1 test rating at the beginning.
df = df[df["rater_id"] != "BiA"]
# remove rating with empty text_id because we cannot link it back to any text
df = df[df["text_id"] != " "]

# apply reversed values according to the changes in answer formulation
df[REVERSED_VAL] = df[REVERSED_VAL].map(reversed_values)

print("How many ratings did we get from each rater? (Should be approx. evenly split)")
print(df["rater_id"].value_counts())

print("""
      How many texts have N ratings?
        * Most texts should have two ratings.
        * Some of the texts were rated by only 1 rater, because one of the raters decided they were too short to be rated
        * 10 texts were rated in a pilot by 6 raters
        * 1 text (CA31TO_LAR14V) has 4 ratings, because it was one of three (next to ST23TO_PER21M and GR25ME_NAR22A) that has been used for the training of the raters. Each text of the training texts has at least two ratings. 
      """)
print(df["text_id"].value_counts().value_counts())

df.to_csv("output/ratings.csv", index=False)
