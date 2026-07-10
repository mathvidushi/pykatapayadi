"""katapayadi.py - single file research script"""
from dataclasses import dataclass, field
import unicodedata, calendar, re
from typing import List
import pandas as pd

HALANT="्"
CONSONANTS=set("कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह")
MAP={"क":1,"ख":2,"ग":3,"घ":4,"ङ":5,"च":6,"छ":7,"ज":8,"झ":9,"ञ":0,
"ट":1,"ठ":2,"ड":3,"ढ":4,"ण":5,"त":6,"थ":7,"द":8,"ध":9,"न":0,
"प":1,"फ":2,"ब":3,"भ":4,"म":5,"य":1,"र":2,"ल":3,"व":4,"श":5,"ष":6,"स":7,"ह":8}
DAYS={1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

@dataclass
class Result:
    word:str
    counted:List[str]=field(default_factory=list)
    digits:List[int]=field(default_factory=list)
    number:int|None=None
    valid:bool=False
    date:str=""
    trace:List[str]=field(default_factory=list)

def date_from_number(n):
    s=str(n)
    if len(s)!=4:return False,""
    dd=int(s[:2]); mm=int(s[2:])
    if mm<1 or mm>12:return False,""
    if dd<1 or dd>DAYS[mm]:return False,""
    return True,f"{dd:02d}-{calendar.month_name[mm]}"

def encode(word):
    word=unicodedata.normalize("NFC",word)
    r=Result(word)
    for i,ch in enumerate(word):
        if ch not in CONSONANTS:continue
        if i+1<len(word) and word[i+1]==HALANT:
            r.trace.append(f"{ch} ignored");continue
        r.counted.append(ch)
        d=MAP[ch]
        r.digits.append(d)
        r.trace.append(f"{ch}->{d}")
    if r.digits:
        r.number=int("".join(map(str,r.digits[::-1])))
        r.valid,r.date=date_from_number(r.number)
    return r

def extract_words(text):
    text=unicodedata.normalize("NFC",text)
    return [w for w in re.findall(r"[ऀ-ॿ]+",text) if w]

def analyse_words(words):
    rows=[]
    for w in words:
        r=encode(w)
        rows.append({"Word":w,"Counted":" ".join(r.counted),"Digits":" ".join(map(str,r.digits)),
        "Number":r.number,"ValidDate":r.valid,"Date":r.date})
    return pd.DataFrame(rows)

def analyse_text(text):
    return analyse_words(extract_words(text))

def analyse_text_file(path):
    with open(path,encoding="utf-8") as f:
        return analyse_text(f.read())

def save_excel(df,path):
    df.to_excel(path,index=False)
