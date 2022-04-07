import pandas as pd
# TODO Data by categories, i.e. tallest woman from Finland

df = pd.read_csv('athletes_w_gender.csv', sep='\t')
filtered_df = df[ (df['height'] > 100) & (df['height'] < 230) & (df['arm_span'] > 100) & (df['arm_span'] < 230)]

print(filtered_df)

data = {}

data["max_height"] = filtered_df.loc[filtered_df.height.idxmax()]
data["min_height"] = filtered_df.loc[filtered_df.height.idxmin()]

data["max_armspan"] = filtered_df.loc[filtered_df.arm_span.idxmax()]
data["min_armspan"] = filtered_df.loc[filtered_df.arm_span.idxmin()]

ape_index =  filtered_df.arm_span - filtered_df.height
data["max_ape_index"] = filtered_df.loc[ape_index.idxmax()]
data["min_ape_index"] = filtered_df.loc[ape_index.idxmin()]

for (attribute, athlete) in data.items():
    print(attribute)
    print(athlete)
    print('*' * 75)