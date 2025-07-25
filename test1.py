# E = joint efficiency for, or the efficiency of, appropriate joint in cylindrical or spherical shells, or the efficiency of ligaments between openings, whichever is less. For welded vessels, use the efficiency specified in UW-12. For ligaments between openings, use the efficiency calculated by the rules given in UG-53.
# P = internal design pressure (see UG-21)
# R = insideradius of the shell course under consideration, For pipe, the inside radius R is determined by the nominal outside radius minus the nominal wall thickness.
# S = maximum allowable stress value (see UG-23 and the stress limitations specified in UG-24)
# t = minimum required thickness of shell

# UG-27 (c)(1)

def required_thickness_ug27(P, R, S, E):
    """
    Calculate required thickness using UG-27 (c)(1) for cylindrical shells.

    Parameters:
    P (float): Internal pressure (psi or MPa)
    R (float): Inside radius (in or mm)
    S (float): Allowable stress of material (psi or MPa)
    E (float): Weld joint efficiency (0 < E ≤ 1)

    Returns:
    float: Required wall thickness (same units as R)
    """
    if E <= 0 or E > 1:
        raise ValueError("Weld joint efficiency E must be between 0 and 1.")
    if SE := (S * E) - (0.6 * P) <= 0:
        raise ValueError("Invalid combination: denominator becomes zero or negative.")

    t = (P * R) / SE
    return t

# Example: P = 200 psi, R = 10 in, S = 15000 psi, E = 0.85
#t_required = required_thickness_ug27(P=200, R=10, S=15000, E=0.85)
#print(f"Required thickness: {t_required:.4f} in")

def required_thickness_cylinder(P, R, S, E):
    """UG-27 (c)(1): Required thickness for cylindrical shell."""
    denominator = (S * E) - (0.6 * P)
    if denominator <= 0:
        raise ValueError("Invalid parameters: denominator is zero or negative.")
    return (P * R) / denominator

def required_thickness_sphere(P, R, S, E):
    """UG-27 (c)(2): Required thickness for spherical shell."""
    denominator = 2 * ((S * E) - (0.2 * P))
    if denominator <= 0:
        raise ValueError("Invalid parameters: denominator is zero or negative.")
    return (P * R) / denominator

def allowable_pressure_cylinder(t, R, S, E):
    """Reverse UG-27 for cylinder: Compute max allowable pressure."""
    denominator = R + 0.6 * t
    if denominator == 0:
        raise ValueError("Invalid parameters: denominator is zero.")
    return (t * S * E) / denominator

def allowable_pressure_sphere(t, R, S, E):
    """Reverse UG-27 for sphere: Compute max allowable pressure."""
    denominator = R + 0.4 * t
    if denominator == 0:
        raise ValueError("Invalid parameters: denominator is zero.")
    return (2 * t * S * E) / denominator

EXAMPLE USAGE

# Inputs
P = 300     # psi
R = 12      # in
S = 20000   # psi
E = 0.85
t = 0.5     # in

# Required thickness for cylinder and sphere
t_cyl = required_thickness_cylinder(P, R, S, E)
t_sph = required_thickness_sphere(P, R, S, E)

# Allowable pressure for given thickness
P_cyl = allowable_pressure_cylinder(t, R, S, E)
P_sph = allowable_pressure_sphere(t, R, S, E)

print(f"Cylindrical Shell - Required Thickness: {t_cyl:.4f} in")
print(f"Spherical Shell  - Required Thickness: {t_sph:.4f} in")
print(f"Cylindrical Shell - Allowable Pressure: {P_cyl:.2f} psi")
print(f"Spherical Shell  - Allowable Pressure: {P_sph:.2f} psi")

