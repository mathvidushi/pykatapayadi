# pykatapayadi

**A Unicode-aware Python library for the Kaṭapayādi numeral system and Sanskrit corpus analysis.**

> 🚧 **Status:** This project is under active development. The API may evolve before the first stable (v1.0) release.

## Overview

**pykatapayadi** is an open-source Python library for working with the traditional **Kaṭapayādi** numeral system. It provides accurate Unicode-aware encoding of Sanskrit words and is being developed as a research tool for computational Sanskrit, Indian Knowledge Systems (IKS), and Digital Humanities.

The long-term goal is to build a reliable, extensible library that supports encoding, decoding, corpus analysis, and research on Sanskrit texts using the Kaṭapayādi system.

---

## Current Features (v0.1)

* Unicode-aware Sanskrit processing
* NFC Unicode normalization
* Kaṭapayādi encoder
* Implements the traditional **Upāntya** interpretation of the Kaṭapayādi rule
* Detailed trace of the encoding process
* DDMM date validation
* Pandas DataFrame generation
* Batch processing of word lists
* Excel export
* Unit tests

---

## Planned Features

* Kaṭapayādi decoder
* Sanskrit corpus analysis
* Viṣṇu Sahasranāma analyser
* Ādityahṛdayam analyser
* Lalitā Sahasranāma analyser
* Birthday search
* Corpus statistics
* PDF and text readers
* Command-line interface (CLI)
* Graphical user interface (GUI)

---

## Rule Implemented

The current implementation follows the traditional rule:

> मिश्रे तूपान्त्यहल्संख्या ।
> न च चिन्त्यो हलस्वरः ॥

### Interpretation

* Only consonants carrying a vowel are counted.
* A consonant immediately followed by a halant (्) is ignored.
* Digits are read in reverse order according to the Kaṭapayādi convention.

This implementation is referred to within the library as the **Upāntya** scheme.

---

## Example

```python
from pykatapayadi import Katapayadi

kp = Katapayadi()

result = kp.encode("विनायक")

print(result.number)
```

Output

```text
1104
```

---

## Design Philosophy

The project is guided by the following principles:

* Correctness over cleverness
* Readability over brevity
* Transparent algorithms
* Unicode-first implementation
* Comprehensive testing
* Extensible architecture
* Clear documentation

---

## Planned Project Structure

```text
pykatapayadi/
│
├── README.md
├── LICENSE
├── requirements.txt
├── pykatapayadi/
│   ├── __init__.py
│   ├── encoder.py
│   ├── models.py
│   ├── constants.py
│   └── utils.py
├── examples/
│   └── Katapayadi.ipynb
├── tests/
│   └── test_encoder.py
└── corpus/
```

---

## Requirements

* Python 3.10 or later
* pandas

Additional dependencies may be added as the project evolves.

---

## Roadmap

### v0.1

* Core encoder
* Unicode normalization
* Date validation
* DataFrame support

### v0.2

* Corpus reader
* Excel reports
* Batch processing improvements

### v0.3

* Decoder
* Birthday search
* Corpus statistics

### v0.4

* Support for additional Kaṭapayādi parsing schemes

### v1.0

* Stable public release
* Complete documentation
* Full test coverage

---

## Contributing

Contributions are welcome.

If you would like to contribute, please open an issue first to discuss new features or significant changes before submitting a pull request.

---

## License

The license will be selected before the first public release.

---

## Acknowledgements

This project is inspired by the mathematical, astronomical, and linguistic traditions of India. Its goal is to make the Kaṭapayādi system accessible through modern, open-source software while remaining faithful to the traditional sources.

---

## Vision

The long-term vision for **pykatapayadi** is to become a comprehensive open-source toolkit for studying and analysing Sanskrit numerical encoding systems. Beginning with Kaṭapayādi, the project aims to provide researchers, educators, students, and developers with reliable computational tools for exploring Sanskrit texts and the rich mathematical heritage of the Indian Knowledge Systems.
