#!/usr/bin/env python3

import sys
import unicodedata
import pandas as pd
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
pd.set_option("display.max_rows", None)

from dataclasses import dataclass, field
from typing import List, Optional

from pykatapayadi.constants import MONTHS, DAYS_IN_MONTH

HALANT = "्"

CONSONANTS = set(
    "कखगघङ"
    "चछजझञ"
    "टठडढण"
    "तथदधन"
    "पफबभम"
    "यरलव"
    "शषसह"
)

KATAPAYADI_MAP = {
    "क":1, "ख":2, "ग":3, "घ":4, "ङ":5,
    "च":6, "छ":7, "ज":8, "झ":9, "ञ":0,
    "ट":1, "ठ":2, "ड":3, "ढ":4, "ण":5,
    "त":6, "थ":7, "द":8, "ध":9, "न":0,
    "प":1, "फ":2, "ब":3, "भ":4, "म":5,
    "य":1,
    "र":2,
    "ल":3,
    "व":4,
    "श":5,
    "ष":6,
    "स":7,
    "ह":8,
}
@dataclass
class KatapayadiResult:
    original_word: str
    devanagari: str
    counted_letters: List[str] = field(default_factory=list)
    ignored_letters: List[str] = field(default_factory=list)
    digits: List[int] = field(default_factory=list)
    reversed_digits: List[int] = field(default_factory=list)
    number: Optional[int] = None
    trace: List[str] = field(default_factory=list)
    valid_date: bool = False
    date_string: str = ""


class KatapayadiEncoder:
    """Encoder implementing the traditional Kaṭapayādi Upāntya interpretation.

    Rules implemented:
    - Count consonants that carry a vowel (i.e., consonant not followed by halant).
    - Ignore consonants immediately followed by halant (virama '्').
    """

    def __init__(self):
        self.map = KATAPAYADI_MAP
        self.halant = HALANT
        self.consonants = CONSONANTS

    def encode(self, word: str) -> KatapayadiResult:
        dev = transliterate(word, sanscript.IAST, sanscript.DEVANAGARI)
        dev = unicodedata.normalize("NFC", dev)
        # Remove characters that are not relevant to Kaṭapayādi
        dev = (
            dev.replace("ः", "")
            .replace("ं", "")
            .replace("ँ", "")
            .replace("ऽ", "")
        )

        counted: List[str] = []
        ignored: List[str] = []
        digits: List[int] = []
        trace: List[str] = [f"transliterated: {dev}"]

        i = 0
        n = len(dev)
        while i < n:
            ch = dev[i]
            # If consonant
            if ch in self.consonants:
                next_ch = dev[i + 1] if i + 1 < n else ""
                if next_ch == self.halant:
                    ignored.append(ch)
                    trace.append(f"ignored {ch} (followed by halant)")
                    i += 2
                    continue

                # consonant carries a vowel -> count it
                counted.append(ch)
                digit = self.map.get(ch)
                if digit is not None:
                    digits.append(digit)
                    trace.append(f"counted {ch} -> {digit}")
                else:
                    trace.append(f"counted {ch} -> (no mapping)")
                i += 1
                continue

            # otherwise skip
            i += 1

        reversed_digits = digits[::-1]
        number = int("".join(str(d) for d in reversed_digits)) if reversed_digits else None

        return KatapayadiResult(
            original_word=word,
            devanagari=dev,
            counted_letters=counted,
            ignored_letters=ignored,
            digits=digits,
            reversed_digits=reversed_digits,
            number=number,
            trace=trace,
        )


def main():
    if len(sys.argv) < 2:
        print("Usage: python katapayadi.py <names_file>")
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            names = [
                unicodedata.normalize("NFC", line.strip())
                for line in f
                if line.strip()
            ]
    except Exception as e:
        print(f"Error opening file {path}: {e}", file=sys.stderr)
        sys.exit(2)
    
    encoder = KatapayadiEncoder()

    results = [encoder.encode(name) for name in names]

    def date_from_number(number: Optional[int]):
        if number is None:
            return False, ""

        s = "".join(str(number)).zfill(4)

        # Only accept exactly four-digit Kaṭapayādi numbers
        if len(s) != 4:
            return False, ""

        day = int(s[:2])
        month = int(s[2:])

        if 1 <= month <= 12:
            max_day = DAYS_IN_MONTH.get(month, 31)
            if 1 <= day <= max_day:
                return True, f"{day:02d} {MONTHS[month]}"

        return False, ""
    rows = []
    for r in results:
        rev_digits = "".join(str(d) for d in (r.reversed_digits or [])).zfill(4)
        valid, date_str = date_from_number(r.number)
        rows.append(
            {
                "No": len(rows) + 1,
                "IAST": r.original_word,
                "Devanagari": r.devanagari,
                "Counted": " ".join(r.counted_letters),
                "Ignored": " ".join(r.ignored_letters),
                "Digits": " ".join(map(str, r.digits)),
                "ReversedDigits": rev_digits,
                "Number": r.number,
                "ValidDate": valid,
                "Date": date_str,
            }
        )

    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    print(f"Total names: {len(df)}")
    print(f"Valid dates: {df['ValidDate'].sum()}")
    print(f"Invalid dates: {len(df) - df['ValidDate'].sum()}")

    out_path = "Vishnusahasranama_Katapayadi_Analysis.xlsx"
    try:
        df.to_excel(out_path, index=False)
        print(f"Exported analysis to {out_path}")
    except Exception as e:
        print(f"Failed to export Excel file: {e}", file=sys.stderr)
    # =====================================================
    # TEMPORARY: Find names having the same Kaṭapayādi number
    # =====================================================

    print("\n" + "=" * 60)
    print("WORDS HAVING THE SAME KAṬAPAYĀDI NUMBER")
    print("=" * 60)

    duplicates = (
        df[df["Number"].notna()]
        .groupby("Number")
        .filter(lambda g: len(g) > 1)
        .sort_values("Number")
    )

    for number, group in duplicates.groupby("Number"):
        print(f"\nNumber = {number}")
        for _, row in group.iterrows():
            print(f"  {row['Devanagari']:<20} {row['IAST']}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()



