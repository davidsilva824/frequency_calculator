### to extract the sequences froma a list of words

import pandas as pd

# List of words to extract
words = ['fireman', 'firemen', 'farmer', 'farmers']  # edit this list

# Load Excel
df = pd.read_excel("SUBTLEX-UK.xlsx", sheet_name="Sheet1")

# Filter and get Zipf values
result = df[df['Spelling'].isin(words)][['Spelling', 'LogFreq(Zipf)']]
print(result)