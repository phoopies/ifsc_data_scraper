import pandas as pd

df = pd.read_csv('athletes_w_gender.csv', sep='\t')
df.count()

# Valid age, country and gender
df1 = df.dropna(subset=['age', 'country', 'gender'])
df1 = df1[df1.gender != 0]
df1.to_csv("athletes_filtered_age_country_gender.csv", sep="\t", index=False)
print(len(df1))

# As above but also valid height
df2 = df1.dropna(subset=['height'])
df2 = df2[(df2.height >= 140) & (df2.height <= 220)]
df2.to_csv("athletes_filtered_age_country_gender_height.csv", sep="\t", index=False)
print(len(df2))

# As above but also valid arm span
df3 = df2.dropna(subset=['arm_span'])
# Ape index to arm span
df3.loc[(df3.arm_span >= -20) & (df3.arm_span <= 20), 'arm_span'] = df3.height + df3.arm_span
df3 = df3[(df3.arm_span >= 120) & (df3.arm_span <= 240)]
df3.to_csv("athletes_filtered_all.csv", sep="\t", index=False)
print(len(df3))