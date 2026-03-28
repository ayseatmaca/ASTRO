# NORAD-TLE-two-line-element-set-format

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/topics/python)

## NORAD TLE Parser and Structured Orbital Data Export

Python-based parser for reading, interpreting, and exporting NORAD Two-Line Element (TLE) orbital data into structured JSON format.

---

## Overview

This project provides a structured TLE reader and parser for extracting orbital parameters from NORAD Two-Line Element sets.

TLEs are standardized orbital data formats widely used to describe the mean orbital elements of Earth-orbiting objects.

The script:

- Detects satellite name headers (if present)
- Parses Line 1 and Line 2 according to official NORAD field definitions
- Extracts orbital parameters into structured dictionaries
- Exports parsed data to `output.json` for integration with analytical pipelines

---

## Example TLE Format

```text
STARLINK-34935
1 51049U 22002AZ  23344.50972222  .00000319  00000-0  15287-4 0  9993
2 51049  53.2170 352.5403 0001660  59.5515 300.5766 15.08875454 99462
```

---

## Functional Capabilities

- Automatic satellite name detection  
- Field-level parsing based on NORAD positional specifications  
- Extraction of:
  - Inclination  
  - RAAN  
  - Eccentricity  
  - Argument of Perigee  
  - Mean Anomaly  
  - Mean Motion  
  - BSTAR drag term  
  - Epoch  
- JSON export for downstream processing  

---

## Processing Workflow

1. Opens a specified TLE file (default: `STARLINK-34935.txt`)  
2. Identifies optional satellite name header  
3. Separates Line 1 and Line 2  
4. Applies field slicing based on NORAD documentation  
5. Outputs parsed parameters to terminal  
6. Exports structured dataset to `output.json`  

---

## Parsed Field Structure

### Line 1

| Field | Description |
|-------|------------|
| Satellite Catalog Number | NORAD ID |
| Classification | Object classification |
| International Designator | Launch identifier |
| Epoch | Reference epoch |
| 1st Derivative of Mean Motion | Drag-related term |
| 2nd Derivative of Mean Motion | Higher-order term |
| BSTAR | Atmospheric drag coefficient |
| Element Set Number | TLE version number |
| Checksum | Data integrity validation |

### Line 2

| Field | Description |
|-------|------------|
| Inclination (deg) | Orbital inclination |
| RAAN (deg) | Right Ascension of Ascending Node |
| Eccentricity | Decimal implied format |
| Argument of Perigee (deg) | Argument of perigee |
| Mean Anomaly (deg) | Position at epoch |
| Mean Motion (rev/day) | Orbital frequency |
| Revolution Number | Orbit count at epoch |
| Checksum | Data integrity validation |

---

## Requirements

- Python 3.x

---

## References

- CelesTrak TLE Documentation: https://celestrak.org/NORAD/documentation/tle-fmt.php  
- Space-Track.org (Official TLE source)  
- NASA – What is a TLE?  

---

## Application Context

This parser supports:

- Orbit propagation workflows  
- SGP4 integration  
- Debris tracking systems  
- Space Domain Awareness (SDA) pipelines  
- Orbital risk modeling frameworks  

---

For collaborations, feel free to connect via LinkedIn or email.
