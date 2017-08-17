# poly-date
Homogenous three-variable polynomial equations for dates. Using Mosek.

# Content

Apparently the day 15/8/17 was a *Pythagorean date* because 15^2+8^2=17^2. However, other dates can satisfy other interesting polynomial equations, not just `d^2+m^2=y^2`. 

# Usage

For fours arguments ``d m y maxDeg`` the script searches for a minimum degree, shortest homogenous polynomial equation with all coefficients equal to 1 satisfied by ``d m y`` and of degree at most ``maxDeg``. The rest should be self-explanatory.

An installation and license for Mosek are required. Solutions are verified in integer arithmetic, but there is no guarantee that the some solution is not missed if the numbers get too large, as always with floating-point arithmetic. An alternative is to implement subset sum.

# Example

```
python2 poly.py 8 11 15 5
my^2 + m^2y + dm^2 + d^2y + d^3 = y^3 + m^3 + dmy + d^2m
```
