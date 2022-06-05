# Safecracker

---

## Story - The Safe on the Property

My friend bought a property to avoid the pandemic.  The property came with a large safe in an old garage.
My goal is to build a device to open the safe, non-destructively, with bonus points for style.

---

## Problem - The Safe

The safe is basically a large heavy steel box featuring a "Sargent & Greenleaf Inc" dial with 100 numbers about its circumference and a handle.

### Typical Operation

Mechanical dial locks typically require entering multiple numbers to unlock them, but the exact steps often differ.  With some googling, it seems this specific type of dial lock unlocks as follows:

* Dial left 3 revolutions.
* Dial left again, stopping on the first number.
* Dial right 2 revolutions.
* Dial right again, stopping on the second number.
* Dial left 1 revolution.
* Dial left again, stopping on the third number.
* Dial right.  If the combination has been entered correctly, the dial will catch and refuse to turn further, indicating the latch has been withdrawn.
* Now you can turn the large lever to retract the large bolts across the door.
* Pull open the door.

### Dial Lock Internals

The mechanical dial lock operates using internal wheels with a notch in them.  In theory a person could carefully feel a lever rub against the notches as they turn the dial, to determine the combination.

---

## Possible (Non-Destructive) Solutions

* ~~Looking into the safe using an XRAY/Radiation machine.~~ Expensive and unfun.
* Attempting every combination, aka Combinatorial Brute Force.
* Attempting to detect the notches in the disc as it turns, but this requires a *lot* of precision.

## Design

### Requirements

* Turning the dial slowly and precisely.
* Detecting the position.
* Detecting vibration.

### Hardware

* Stepper Motor - NEMA23
* Stepper Motor Driver - A4988 Module
* Photointerrupter Module
* MPU6050 Accelerometer and Gyroscope
* Power Supply for it all. 5V10A
* 3d Printed Frame

### Software

* A4988 Motor Class
* 

---