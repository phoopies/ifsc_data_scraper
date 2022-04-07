import pandas as pd
import gender_guesser.detector as gd

df = pd.read_csv('athletes.csv', sep='\t')

d = gd.Detector()
genders = []
for name in df.name:
    firstname = name.split(' ')[0]
    gender = d.get_gender(firstname)

    if 'female' in gender:
        genders.append(-1)
    elif "male" in gender:
        genders.append(1)
    else:
        genders.append(0)
    print(f"{firstname} is {gender} = {genders[-1]}")

df['gender'] = genders
df.to_csv("athletes_w_gender.csv", sep="\t", index=False)