from time import sleep
from typing import List
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

url = lambda id: f"https://www.ifsc-climbing.org/index.php?option=com_ifsc&task=athlete.display&id={id}"
filename = "athletes.csv"

class Athlete:
    def __init__(self, id: int, name: str, age: int, country: str, hometown: str = None, height_cm: int = None, arm_span_cm: int = None) -> None:
        self.id = id
        self.name = name
        self.age = age
        self.country = country
        self.hometown = hometown
        self.height = height_cm
        self.arm_span = arm_span_cm
    
    def __str__(self) -> str:
        return f"{self.name} {self.age} {self.country}"
    
    def to_dict(self) -> dict:
        return self.__dict__
    
# How long to wait until going to next athlete. Longer is nicer to the server :)
timeout_ms = 1500
id = 1

athletes: List[Athlete] = []

# Break when x consecutive invalid pages are encountered
max_consecutive_invalids = 20
invalid_counter = 0

while True:
    page = requests.get(url(id))
    soup = bs(page.text, 'html.parser')

    athlete_div = soup.find("div", class_="athlete")

    name = athlete_div.find("h1", class_="name").get_text(strip=True)
    if not name:
        invalid_counter += 1
        print(f"Invalid climber encountered at {id}")
        if invalid_counter >= max_consecutive_invalids:
            print(f"{max_consecutive_invalids} consecutive invalids encountered. Stopping scrape...")
            break
        id += 1
        continue

    invalid_counter = 0

    age = athlete_div.find("span", class_="age").find("strong").get_text(strip=True)
    country = athlete_div.find("div", class_="country").find("span").get_text(strip=True)
    hometown = athlete_div.find("span", class_="hometown").find("strong").get_text(strip=True)

    info = {}
    personal_info_div = soup.find("div", class_="personal-info")
    paragraphs = personal_info_div.find_all("p")
    paragraphs_it = iter(paragraphs)
    for (subtitle, paragraph) in zip(paragraphs_it, paragraphs_it):
        info[subtitle.get_text(strip=True)] = paragraph.get_text(strip=True)
        
    height = info["HEIGHT"] if "HEIGHT" in info else None
    arm_span = info["ARM SPAN"] if "ARM SPAN" in info else None

    athlete = Athlete(id, name, age, country, hometown, height, arm_span)
    print(athlete)

    athletes.append(athlete)

    id += 1
    sleep(timeout_ms / 1000)

df = pd.DataFrame.from_records([athlete.to_dict() for athlete in athletes])
df.to_csv(filename, sep="\t", index=False)