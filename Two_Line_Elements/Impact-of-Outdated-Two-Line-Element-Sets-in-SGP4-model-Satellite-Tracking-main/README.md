#  Impact of Outdated Two Line Element Sets in SGP4 model Satellite Tracking

This project demonstrates how the accuracy of a satellite orbit prediction degrades as the **TLE (Two-Line Element set) becomes older**.

We propagate multiple TLEs of different ages using the **SGP4 propagator** and compare their predicted positions against the newest (reference) TLE.

<img src="https://github.com/Girinath-NU/Impact-of-Outdated-Two-Line-Element-Sets-in-SGP4-model-Satellite-Tracking/blob/main/Earth%20View.png" width="75%" />
---

## Objective

To visualize and quantify **orbital prediction error growth** caused by TLE ageing.

We compare:

* 1-day old TLE
* 3-day old TLE
* 6-day old TLE
  against the newest available TLE.

---

## Concept

TLEs are generated from tracking observations.
As time passes:

Atmospheric drag + gravitational perturbations + solar radiation pressure
➡ causes orbit prediction to drift

Therefore:

Older TLE → Larger Position Error

This project demonstrates that behavior graphically.

---

## Requirements

* MATLAB R2021a or later
* Aerospace Toolbox
* Satellite Communications Toolbox

---

## Project Structure

```
project/
│── tle_1hr.tle      # Newest TLE (reference)
│── tle_1day.tle     # 1 day old
│── tle_3day.tle     # 3 day old
│── tle_6day.tle     # 6 day old
│── tle_error.m      # Main MATLAB script
│── README.md
```

---

## How to Run

1. Update file paths inside the script:

```matlab
f1 = "path/to/tle_1hr.tle";
f2 = "path/to/tle_1day.tle";
f3 = "path/to/tle_3day.tle";
f4 = "path/to/tle_6day.tle";
```

2. Run the script:

```matlab
tle_error
```

---

## What the Code Does

### 1. Create Satellite Scenario

Defines simulation start time close to newest TLE epoch.

### 2. Load Satellites using SGP4

Each TLE is propagated independently using the SGP4 model.

### 3. Visualize Orbits

Color coded:

* Green → Latest TLE (reference)
* Blue → 1 day old
* Magenta → 3 day old
* Red → 6 day old

### 4. Compute Position Error

We compute 3D distance error:

[
Error = || P_{old} - P_{new} ||
]

### 5. Plot Error Growth

Graph shows prediction divergence over time.

---

## 📊 Output

### Orbit Viewer

3D Earth visualization showing orbital divergence.

### Error Graph

Position error vs time.

### Console Output

```
Final Position Errors:
1 Day TLE error  : XX km
3 Day TLE error  : XX km
6 Day TLE error  : XX km
```

---

## 📈 Expected Result

Error increases approximately exponentially:

| TLE Age | Typical Error  |
| ------- | -------------- |
| 1 Day   | Few km         |
| 3 Days  | Tens of km     |
| 6 Days  | Hundreds of km |

(Depends on satellite altitude — LEO diverges faster)

---

## 🛰️ Key Learning

TLE is **not a permanent orbit definition**.

It is a short-term prediction model.

For LEO satellites:

* Valid for ~1–3 days
* Beyond 5 days → unreliable for pointing/tracking

---

