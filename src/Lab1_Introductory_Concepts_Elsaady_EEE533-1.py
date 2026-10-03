"""
EEE533: Semiconductor Device and Process Modeling
Saif Elsaady
Lab 1: 10 points
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import base64
import io

# HTML Report Generator Class
class HTMLReportGenerator:
    def __init__(self, title="EEE533 Lab 1: Introductory Concepts", author="Saif Elsaady"):
        self.title = title
        self.author = author
        self.content = []
        self.plots = []
        
    def add_heading(self, text, level=1):
        self.content.append(f"<h{level}>{text}</h{level}>")
    
    def add_text(self, text):
        # Convert line breaks to HTML breaks
        formatted_text = text.replace('\n', '<br>')
        self.content.append(f"<p>{formatted_text}</p>")
    
    def add_code_block(self, code):
        self.content.append(f"<pre><code>{code}</code></pre>")
    
    def add_equation(self, latex_equation, display=True):
        """Add a LaTeX equation (display=True for block, False for inline)"""
        if display:
            self.content.append(f'<div class="equation-box">$${latex_equation}$$</div>')
        else:
            self.content.append(f"<p>${latex_equation}$</p>")
    
    def save_plot_as_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        return f"data:image/png;base64,{image_base64}"
    
    def add_plot(self, fig, caption=""):
        """Add matplotlib figure to report"""
        img_data = self.save_plot_as_base64(fig)
        self.content.append(f'<div class="plot-container">')
        self.content.append(f'<img src="{img_data}" alt="Plot" style="max-width: 100%; height: auto;">')
        if caption:
            self.content.append(f'<p class="caption"><em>{caption}</em></p>')
        self.content.append('</div>')
    
    def add_results_table(self, headers, rows):
        """Add a results table"""
        self.content.append('<table>')
        self.content.append('<tr>')
        for header in headers:
            self.content.append(f'<th>{header}</th>')
        self.content.append('</tr>')
        
        for row in rows:
            self.content.append('<tr>')
            for cell in row:
                self.content.append(f'<td>{cell}</td>')
            self.content.append('</tr>')
        self.content.append('</table>')
    
    def generate_html(self):
        """Generate complete HTML document"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    
    <!-- MathJax for LaTeX equation rendering -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }}
        }};
    </script>
    
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            color: #333333;
        }}
        
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #bdc3c7;
            padding-bottom: 5px;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
        
        h3 {{
            color: #7f8c8d;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        p {{
            text-align: justify;
            margin-bottom: 15px;
        }}
        
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            font-size: 14px;
            overflow-x: auto;
        }}
        
        code {{
            font-family: 'Courier New', monospace;
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        
        .plot-container {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            background-color: #f8f9fa;
        }}
        
        .caption {{
            font-style: italic;
            color: #6c757d;
            margin-top: 10px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th, td {{
            border: 1px solid #dee2e6;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        
        .author-info {{
            text-align: center;
            margin-bottom: 40px;
            color: #6c757d;
        }}
        
        .problem-section {{
            margin-bottom: 50px;
            padding: 20px;
            border-left: 4px solid #3498db;
            background-color: #f8f9fa;
        }}
        
        .result-box {{
            background-color: #e8f5e8;
            border: 1px solid #d4edda;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .equation-box {{
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>{self.title}</h1>
    <div class="author-info">
        <h3>{self.author}</h3>
        <p>EEE533: Semiconductor Device and Process Modeling</p>
    </div>
    
    {''.join(self.content)}
    
</body>
</html>
"""
        return html
    
    def save_to_file(self, filename="Lab1_Report.html"):
        """Save HTML report to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_html())
        print(f"HTML report saved as: {filename}")

# Initialize HTML report generator
report = HTMLReportGenerator()

# Physical constants you might need
# k_B = 8.617e-5  # Boltzmann constant in eV/K
# k_B_SI = 1.381e-23  # Boltzmann constant in J/K
# q = 1.602e-19  # Elementary charge in C

# =============================================================================
# Problem 1 (0.5 points)
# =============================================================================
# Add Problem 1 to HTML report
report.add_heading("Problem 1: Crystal Lattice Nearest Neighbors (0.5 points)", 2)
report.add_text("""
<strong>Problem Statement:</strong><br>
What is the number of nearest-neighbor atoms for simple cubic, FCC and BCC lattice?<br>
What is the number of the second nearest neighbors for simple cubic, FCC and BCC lattice?
""")

report.add_text("""
<strong>Questions to answer:</strong><br>
• How many atoms directly touch each atom in simple cubic structure?<br>
• How many atoms directly touch each atom in FCC structure?<br>
• How many atoms directly touch each atom in BCC structure?<br>
• What are the second nearest neighbors for each structure?
""")

# Nearest neighbors
nn_simple_cubic = 6  # 6 face-centered neighbors (±x, ±y, ±z directions)
nn_fcc = 12  # 12 corner atoms of the cuboctahedron
nn_bcc = 8  # 8 corner atoms of the cube

# Second nearest neighbors
snn_simple_cubic = 12  # 12 edge-sharing neighbors at distance a*sqrt(2)
snn_fcc = 6  # 6 face-centered atoms at distance a*sqrt(2)
snn_bcc = 6  # 6 face-centered atoms at distance a

# Print results and add to HTML
results_text = f"""
Simple Cubic: {nn_simple_cubic} nearest neighbors, {snn_simple_cubic} second nearest neighbors<br>
FCC: {nn_fcc} nearest neighbors, {snn_fcc} second nearest neighbors<br>
BCC: {nn_bcc} nearest neighbors, {snn_bcc} second nearest neighbors
"""

print("Problem 1 Results:")
print(f"Simple Cubic: {nn_simple_cubic} nearest neighbors, {snn_simple_cubic} second nearest neighbors")
print(f"FCC: {nn_fcc} nearest neighbors, {snn_fcc} second nearest neighbors")
print(f"BCC: {nn_bcc} nearest neighbors, {snn_bcc} second nearest neighbors")

# Add results to HTML
report.content.append('<div class="result-box">')
report.add_text(f"<strong>Results:</strong><br>{results_text}")
report.content.append('</div>')

# Add results table to HTML
report.add_results_table(
    ["Lattice Type", "Nearest Neighbors", "Second Nearest Neighbors"],
    [
        ["Simple Cubic", nn_simple_cubic, snn_simple_cubic],
        ["FCC", nn_fcc, snn_fcc],
        ["BCC", nn_bcc, snn_bcc]
    ]
)

# =============================================================================
# Problem 2 (0.5 points)
# =============================================================================
# Add Problem 2 to HTML report
report.add_heading("Problem 2: Primitive Cell Volumes (0.5 points)", 2)
report.add_text("""
<strong>Problem Statement:</strong><br>
Assume that a lattice constant a = 0.5 nm<br>
Find the volume of a primitive cell for simple cubic, FCC and BCC crystal structures
""")

report.add_text("""
<strong>Questions to answer:</strong><br>
• What is the relationship between lattice constant and primitive cell volume for simple cubic?<br>
• What is the relationship between lattice constant and primitive cell volume for FCC?<br>
• What is the relationship between lattice constant and primitive cell volume for BCC?<br>
• Calculate the actual volumes given a = 0.5 nm
""")

a = 0.5  # nm

# Primitive cell volumes
V_simple_cubic = a**3  # Simple cubic primitive cell = conventional cell
V_fcc = a**3 / 4  # FCC has 4 atoms per conventional cell, primitive cell has 1 atom
V_bcc = a**3 / 2  # BCC has 2 atoms per conventional cell, primitive cell has 1 atom

print("\nProblem 2 Results:")
print(f"Lattice constant a = {a} nm")
print(f"Simple Cubic primitive cell volume: {V_simple_cubic} nm³")
print(f"FCC primitive cell volume: {V_fcc} nm³")
print(f"BCC primitive cell volume: {V_bcc} nm³")

# Add results to HTML
results_text_2 = f"""
Lattice constant a = {a} nm<br>
Simple Cubic primitive cell volume: {V_simple_cubic} nm³<br>
FCC primitive cell volume: {V_fcc} nm³<br>
BCC primitive cell volume: {V_bcc} nm³
"""

report.content.append('<div class="result-box">')
report.add_text(f"<strong>Results:</strong><br>{results_text_2}")
report.content.append('</div>')

# Add results table to HTML
report.add_results_table(
    ["Lattice Type", "Volume Formula", "Volume (nm³)"],
    [
        ["Simple Cubic", "a³", f"{V_simple_cubic:.6f}"],
        ["FCC", "a³/4", f"{V_fcc:.6f}"],
        ["BCC", "a³/2", f"{V_bcc:.6f}"]
    ]
)

# =============================================================================
# Problem 3 (2.0 points)
# =============================================================================
# Consider bulk silicon material with donor doping ND=10^18 cm^-3
# The donor ionization energy is ED = 50 meV
# Plot the temperature dependence of the electron density
# On the same axes, plot the temperature dependence of intrinsic carrier concentration
# Include partial ionization (incomplete ionization) leading to carrier freeze-out at low temperatures
# Use bisection method to solve the transcendental equation

# Questions to answer:
# - What are the typical values for silicon bandgap energy Eg?
# - What are the effective density of states Nc and Nv for silicon?
# - What is the formula for intrinsic carrier concentration ni(T)?
# - What is the transcendental equation that describes electron density with donor freeze-out?
# - How do you implement the bisection method to solve f(x) = 0?
# - What should be the temperature range for the plot (consider freeze-out at low T)?
# - At what temperatures do you expect to see freeze-out effects?
# - At what temperatures does the material become intrinsic?

# Physics concepts to implement:
# - Intrinsic carrier concentration: ni = sqrt(Nc*Nv) * exp(-Eg/(2*k_B*T))
# - Charge neutrality with partial ionization
# - Fermi-Dirac statistics for donor ionization
# - Transcendental equation solving using bisection method
# - Temperature dependence from ~50K to 600K

# -----------------------------
# Physical constants (SI unless noted)
# -----------------------------
k_B_J = 1.380649e-23        # J/K
k_B_eV = 8.617333262145e-5  # eV/K
h = 6.62607015e-34          # J*s
m0 = 9.1093837015e-31       # kg
CM3_PER_M3 = 1e6            # 1 m^3 = 1e6 cm^3

# -----------------------------
# Silicon material parameters from the slides (300 K values)
# -----------------------------
Eg_eV = 1.12                 # bandgap at 300 K (eV)
me_dos = 1.08 * m0           # electron DOS effective mass
# The slide lists "0.57/0.8" for holes; common DOS value for Si is ~0.81 m0.
# We'll choose the higher (0.8 m0) entry to align with many device texts.
mh_dos = 0.80 * m0

# -----------------------------
# Donor parameters (given)
# -----------------------------
ND_cm3 = 1e18               # donors per cm^3
ED_eV = 0.050               # donor ionization energy (eV) below Ec
gD = 2.0                    # donor degeneracy factor

# -----------------------------
# Density-of-states prefactor for parabolic bands
# N_C = 2 * (2*pi*m_e*kT / h^2)^(3/2)
# N_V = 2 * (2*pi*m_h*kT / h^2)^(3/2)
# Returned in cm^-3
# -----------------------------
def Nc_cm3(T):
    val_m3 = 2.0 * ((2.0*np.pi*me_dos*k_B_J*T) / (h**2))**1.5
    return val_m3 / CM3_PER_M3

def Nv_cm3(T):
    val_m3 = 2.0 * ((2.0*np.pi*mh_dos*k_B_J*T) / (h**2))**1.5
    return val_m3 / CM3_PER_M3

def ni_cm3(T, Eg_eV_const=Eg_eV):
    # intrinsic concentration with constant Eg (parabolic bands)
    Nc = Nc_cm3(T)
    Nv = Nv_cm3(T)
    return np.sqrt(Nc*Nv) * np.exp(-Eg_eV_const/(2.0*k_B_eV*T))

# -----------------------------
# Charge neutrality with partial ionization:
# n = p + N_D^+
#
# Using nondegenerate (Boltzmann) statistics:
# n = N_C * exp(-(E_C - E_F)/kT)
# p = N_V * exp(-(E_F - E_V)/kT)
# Take E_C = 0, E_V = -Eg. Donor level E_D = -ED (below Ec).
# Donor ionized fraction: N_D^+ = N_D / (1 + (1/gD)*exp((E_F - E_D)/kT))
# -----------------------------
def charge_neutrality(EF_eV, T, ND_cm3, Eg_eV, ED_eV, gD):
    EC = 0.0
    EV = -Eg_eV
    ED_level = -ED_eV  # donor energy relative to Ec=0 (below Ec)
    Nc = Nc_cm3(T)
    Nv = Nv_cm3(T)
    n = Nc * np.exp(-(EC - EF_eV)/(k_B_eV*T))
    p = Nv * np.exp(-(EF_eV - EV)/(k_B_eV*T))
    ND_plus = ND_cm3 / (1.0 + (1.0/gD)*np.exp((EF_eV - ED_level)/(k_B_eV*T)))
    # f(EF) = n - (p + ND+); root at charge neutrality
    return n - (p + ND_plus)

# -----------------------------
# Robust bracketing + bisection (no canned solvers)
# -----------------------------
def find_bracket(func, T, ND_cm3, Eg_eV, ED_eV, gD, a=-2.0, b=+1.0, steps=200):
    """
    Scan EF in [a, b] eV to find sub-interval with a sign change for func(EF).
    Defaults: a below Ev by ~1 eV, b above Ec by ~1 eV since Ec=0, Ev=-Eg.
    """
    xs = np.linspace(a, b, steps+1)
    fs = [func(x, T, ND_cm3, Eg_eV, ED_eV, gD) for x in xs]
    for i in range(steps):
        if np.sign(fs[i]) == 0:
            return xs[i], xs[i]
        if np.sign(fs[i]) != np.sign(fs[i+1]):
            return xs[i], xs[i+1]
    # If no sign change, expand the search range a bit and retry (once)
    xs = np.linspace(a-2.0, b+2.0, steps+1)
    fs = [func(x, T, ND_cm3, Eg_eV, ED_eV, gD) for x in xs]
    for i in range(steps):
        if np.sign(fs[i]) == 0:
            return xs[i], xs[i]
        if np.sign(fs[i]) != np.sign(fs[i+1]):
            return xs[i], xs[i+1]
    # As a fallback, return a narrow bracket around midgap; caller can handle failure.
    return -Eg_eV/2 - 0.1, -Eg_eV/2 + 0.1

def bisection(func, a, b, T, ND_cm3, Eg_eV, ED_eV, gD, tol=1e-8, max_iter=200):
    """
    Classic bisection: assumes func(a)*func(b) <= 0 (root bracketed).
    All energies in eV.
    """
    fa = func(a, T, ND_cm3, Eg_eV, ED_eV, gD)
    fb = func(b, T, ND_cm3, Eg_eV, ED_eV, gD)
    if fa == 0.0: 
        return a
    if fb == 0.0: 
        return b
    if np.sign(fa) == np.sign(fb):
        raise ValueError("Bisection called without a valid sign-changing bracket.")
    for _ in range(max_iter):
        c = 0.5*(a+b)
        fc = func(c, T, ND_cm3, Eg_eV, ED_eV, gD)
        if abs(fc) < tol or 0.5*(b-a) < tol:
            return c
        if np.sign(fc) == np.sign(fa):
            a, fa = c, fc
        else:
            b, fb = c, fc
    return 0.5*(a+b)  # best estimate after max_iter

# -----------------------------
# Sweep temperature and compute n(T) with freeze-out, plus ni(T)
# -----------------------------
def solve_n_of_T(T_array, ND_cm3, Eg_eV, ED_eV, gD):
    n_vals = np.zeros_like(T_array, dtype=float)
    EF_vals = np.zeros_like(T_array, dtype=float)
    for i, T in enumerate(T_array):
        # bracket EF (try a modest window around the bandgap)
        a, b = find_bracket(charge_neutrality, T, ND_cm3, Eg_eV, ED_eV, gD,
                            a=-Eg_eV-0.5, b=+0.5, steps=300)
        try:
            EF = bisection(charge_neutrality, a, b, T, ND_cm3, Eg_eV, ED_eV, gD, tol=1e-10, max_iter=200)
        except ValueError:
            # As a fallback, just take midgap and continue
            EF = -Eg_eV/2.0
        EF_vals[i] = EF

        # once EF is known, compute n via Boltzmann relation
        EC = 0.0
        n_vals[i] = Nc_cm3(T) * np.exp(-(EC - EF)/(k_B_eV*T))
    return n_vals, EF_vals

# Temperature range (covers freeze-out, extrinsic, intrinsic)
Tmin, Tmax, nT = 5.0, 700.0, 400
T = np.linspace(Tmin, Tmax, nT)

# Solve
n_T, EF_T = solve_n_of_T(T, ND_cm3, Eg_eV, ED_eV, gD)
ni_T = ni_cm3(T, Eg_eV)

# Quick sanity check at 300 K
T300 = 300.0
n300 = np.interp(T300, T, n_T)
ni300 = ni_cm3(T300, Eg_eV)
print(f"At 300 K: n ≈ {n300:.3e} cm^-3,   ni ≈ {ni300:.3e} cm^-3")

# Add Problem 3 to HTML report
report.add_heading("Problem 3: Temperature Dependence of Electron Density (2.0 points)", 2)

problem3_description = """
<strong>Problem Statement:</strong><br>
Consider bulk silicon material with donor doping ND=10^18 cm^-3<br>
The donor ionization energy is ED = 50 meV<br>
Plot the temperature dependence of the electron density<br>
On the same axes, plot the temperature dependence of intrinsic carrier concentration<br>
Include partial ionization (incomplete ionization) leading to carrier freeze-out at low temperatures<br>
Use bisection method to solve the transcendental equation
"""
report.add_text(problem3_description)

# Add key physics concepts
physics_concepts = """
<strong>Key Physics Concepts Implemented:</strong><br>
• Intrinsic carrier concentration<br>
• Charge neutrality with partial ionization<br>
• Fermi-Dirac statistics for donor ionization<br>
• Transcendental equation solving using bisection method<br>
• Temperature dependence from ~5K to 700K
"""
report.add_text(physics_concepts)

# Add intrinsic carrier concentration equation
report.add_equation(r"n_i = \sqrt{N_c N_v} \exp\left(\frac{-E_g}{2k_BT}\right)")

# Add charge neutrality equation
report.add_text("<strong>Charge Neutrality:</strong>")
report.add_equation(r"n = p + N_D^+")

# Add Fermi-Dirac for donors
report.add_text("<strong>Donor Ionization (Fermi-Dirac):</strong>")
report.add_equation(r"N_D^+ = \frac{N_D}{1 + \frac{1}{g_D}\exp\left(\frac{E_F - E_D}{k_BT}\right)}")

# Add numerical results to HTML
results_text_3 = f"At 300 K: n ≈ {n300:.3e} cm^-3,   ni ≈ {ni300:.3e} cm^-3"
report.content.append('<div class="result-box">')
report.add_text(f"<strong>Results:</strong><br>{results_text_3}")
report.content.append('</div>')

# -----------------------------
# Plot
# -----------------------------
fig3 = plt.figure(figsize=(10,6))
plt.semilogy(T, n_T, 'b-', linewidth=2, label=r'$n(T)$ with partial donor ionization')
plt.semilogy(T, ni_T, 'r--', linewidth=2, label=r'$n_i(T)$ (parabolic bands, const $E_g$)')
plt.xlabel('Temperature T (K)', fontsize=12)
plt.ylabel('Concentration (cm$^{-3}$)', fontsize=12)
plt.title('Bulk Si (ND=1e18 cm$^{-3}$, ED=50 meV): $n(T)$ vs. $n_i(T)$', fontsize=14)
plt.grid(True, which='both', ls='--', alpha=0.5)
plt.legend(fontsize=11)
plt.tight_layout()

# Add plot to HTML report
report.add_plot(fig3, "Temperature dependence of electron density showing carrier freeze-out at low temperatures and approach to intrinsic behavior at high temperatures")

plt.show()

"""
EEE 533 — Problem 4 (3.0 points)

(a) Derive gc,2D(E) in a quasi-2D system.
    For parabolic bands, the conduction-band DOS in 2D is *constant* above each occupied
    subband edge and zero below it. Using the same approach as gc,3D(E),
        gc,3D(E) = (1/(2*pi**2)) * (2*m*/ħ^2)^(3/2) * sqrt(E - Ec) * θ(E - Ec)
    the 2D DOS per subband i is
        gc,2D_i(E) = (m*/(pi*ħ^2)) * θ(E - Ec - ε_i)
    so the total Q2D DOS is a stepwise sum over subbands:
        gc,2D(E) = Σ_i (m*/(pi*ħ^2)) θ(E - Ec - ε_i)
    (Formulas per the “Analytical Density of States” slide.)
    
(b) Plot the DOS for 3D, 2D, and 1D systems.
    Use ε(2D) = [50, 80, 95] meV and ε_i(1D) = [40, 75, 90, 95] meV.
    Use energy in eV and length in cm. Report units:
        3D: states / (eV·cm^3)
        2D: states / (eV·cm^2)
        1D: states / (eV·cm)
    The 1D DOS is (given in the problem statement):
        gc,1D(E) = Σ_i [ 2*m* / (π*ħ*sqrt(2*m*(E - Ec - ε_i))) ] θ(E - Ec - ε_i)
"""
# ---------- Physical constants ----------
hbar_Js = 1.054_571_817e-34     # J·s
eV_to_J = 1.602_176_634e-19     # J per eV
m0 = 9.109_383_7015e-31         # kg
cm_per_m = 100.0

# ---------- Silicon parameter from notes ----------
# Use the *DOS* effective mass for electrons in Si (consistent with Problem 5)
mstar = 1.18 * m0   # kg  (electron DOS mass for Si)

# ---------- Energy grid and subband data ----------
Ec = 0.0  # set conduction-band edge as reference (eV)
E = np.linspace(0.0, 0.6, 1500)  # eV
# 2D subband energies (eV)
eps_2D = np.array([0.050, 0.080, 0.095])
# 1D subband energies (eV)
eps_1D = np.array([0.040, 0.075, 0.090, 0.095])

# ---------- Helper: Heaviside θ ----------
theta = lambda x: (x > 0).astype(float)

# ---------- Unit conversion helpers ----------
# We compute in SI, then convert:
#   3D: per (J·m^3) -> per (eV·cm^3)
#   2D: per (J·m^2) -> per (eV·cm^2)
#   1D: per (J·m)   -> per (eV·cm)
m3_to_cm3 = (cm_per_m**3)
m2_to_cm2 = (cm_per_m**2)
m_to_cm   = (cm_per_m)

# ---------- (a) & (b): DOS formulas (parabolic bands) ----------
# Convert E to Joules for the SI expressions
E_J = E * eV_to_J
Ec_J = Ec * eV_to_J
eps_2D_J = eps_2D * eV_to_J
eps_1D_J = eps_1D * eV_to_J

# 3D DOS: gc,3D(E) = (1/(2*pi^2)) * (2*m*/ħ^2)^(3/2) * sqrt(E-Ec) * θ(E-Ec)
pref_3D_SI = (1.0 / (2.0*np.pi**2)) * (2.0*mstar / hbar_Js**2)**1.5
g3D_SI = pref_3D_SI * np.sqrt(np.maximum(E_J - Ec_J, 0.0))

# Convert to per (eV·cm^3)
g3D = g3D_SI * (eV_to_J) * (1.0 / m3_to_cm3)  # multiply by J/eV, divide by m^3/cm^3

# 2D DOS per subband: m*/(pi*ħ^2) * θ(E - Ec - ε_i)
pref_2D_SI = mstar / (np.pi * hbar_Js**2)  # per (J·m^2)
g2D_SI = np.zeros_like(E_J)
for ei in eps_2D_J:
    g2D_SI += pref_2D_SI * theta(E_J - (Ec_J + ei))

# Convert to per (eV·cm^2)
g2D = g2D_SI * (eV_to_J) * (1.0 / m2_to_cm2)

# 1D DOS given in the problem statement:
# gc,1D(E) = Σ_i [ 2*m* / (π*ħ*sqrt(2*m*(E - Ec - ε_i))) ] θ(…)
pref_1D_SI = 2.0*mstar / (np.pi * hbar_Js)    # numerator per sqrt(J)·m
g1D_SI = np.zeros_like(E_J)
for ei in eps_1D_J:
    inside = np.maximum(E_J - (Ec_J + ei), 0.0)
    # avoid division by zero cleanly
    term = np.zeros_like(E_J)
    mask = inside > 0
    term[mask] = pref_1D_SI / np.sqrt(2.0*mstar*inside[mask])
    g1D_SI += term

# Convert to per (eV·cm)
g1D = g1D_SI * (eV_to_J) * (1.0 / m_to_cm)

# Add Problem 4 to HTML report
report.add_heading("Problem 4: Density of States in Different Dimensions (3.0 points)", 2)

problem4_description = """
<strong>Problem Statement:</strong><br>
(a) Derive gc,2D(E) in a quasi-2D system.<br>
(b) Plot the DOS for 3D, 2D, and 1D systems.<br>
Use ε(2D) = [50, 80, 95] meV and ε_i(1D) = [40, 75, 90, 95] meV.<br>
Use energy in eV and length in cm.
"""
report.add_text(problem4_description)

# Add theoretical background
theory_text = """
<strong>Theoretical Background:</strong><br>
For parabolic bands, the conduction-band DOS in 2D is <em>constant</em> above each occupied
subband edge and zero below it. 
"""
report.add_text(theory_text)

# Add 3D DOS equation
report.add_text("<strong>3D Density of States:</strong>")
report.add_equation(r"g_{c,3D}(E) = \frac{1}{2\pi^2} \left(\frac{2m^*}{\hbar^2}\right)^{3/2} \sqrt{E - E_c} \cdot \theta(E - E_c)")

# Add 2D DOS equation
report.add_text("<strong>2D Density of States per subband:</strong>")
report.add_equation(r"g_{c,2D}^{(i)}(E) = \frac{m^*}{\pi\hbar^2} \theta(E - E_c - \varepsilon_i)")

# Add total 2D DOS
report.add_text("<strong>Total 2D DOS (sum over subbands):</strong>")
report.add_equation(r"g_{c,2D}(E) = \sum_i \frac{m^*}{\pi\hbar^2} \theta(E - E_c - \varepsilon_i)")

# Add 1D DOS equation
report.add_text("<strong>1D Density of States:</strong>")
report.add_equation(r"g_{c,1D}(E) = \sum_i \frac{2m^*}{\pi\hbar\sqrt{2m^*(E - E_c - \varepsilon_i)}} \theta(E - E_c - \varepsilon_i)")

report.add_text("<strong>Units:</strong> 3D [states/(eV·cm³)], 2D [states/(eV·cm²)], 1D [states/(eV·cm)]")

# Add normalization explanation
report.add_text("""
<strong>Visualization Note:</strong><br>
The plot shows normalized density of states to clearly visualize all three behaviors on the same scale.
The actual magnitudes differ significantly due to different dimensionalities and units.
Vertical dotted lines indicate subband energies for 2D (red) and 1D (green) systems.
""")

# ---------- Normalize for visualization ----------
# Find max values for normalization (avoiding infinities)
E_norm = np.linspace(0.05, 0.6, 1000)  # avoid singularities
g3D_norm = g3D[np.isfinite(g3D) & (g3D > 0)]
g2D_norm = g2D[np.isfinite(g2D) & (g2D > 0)]
g1D_norm = g1D[np.isfinite(g1D) & (g1D > 0)]

# Normalize each DOS to its maximum value
g3D_normalized = g3D / np.max(g3D_norm) if len(g3D_norm) > 0 else g3D
g2D_normalized = g2D / np.max(g2D_norm) if len(g2D_norm) > 0 else g2D
g1D_normalized = g1D / np.max(g1D_norm) if len(g1D_norm) > 0 else g1D

# ---------- Plot normalized versions ----------
fig4, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

# Plot normalized curves
l3d, = ax.plot(E, g3D_normalized, 'b-', linewidth=2, label=r'$g_{c,3D}(E)$ (√E behavior)')
l2d, = ax.step(E, g2D_normalized, 'r-', where='post', linewidth=2, label=r'$g_{c,2D}(E)$ (step function)')
l1d, = ax.plot(E, g1D_normalized, 'g-', linewidth=2, label=r'$g_{c,1D}(E)$ (1/√E behavior)')

# Mark subband edges for 2D and 1D
for ei in eps_2D:
    ax.axvline(x=ei, color='red', linestyle=':', alpha=0.3)
for ei in eps_1D:
    ax.axvline(x=ei, color='green', linestyle=':', alpha=0.3)

ax.set_xlim(0, 0.6)
ax.set_ylim(0, 1.1)
ax.set_xlabel('Energy E (eV) [with $E_c=0$]', fontsize=12)
ax.set_ylabel('Normalized Density of States (arb. units)', fontsize=12)
ax.set_title('Conduction-band DOS: 3D (√E), 2D (steps), 1D (1/√E) - Normalized', fontsize=14)
ax.grid(True, ls=':', alpha=0.7)

# Force the legend to use the exact handles we just made
leg = ax.legend(handles=[l3d, l2d, l1d], loc='upper left', fontsize=11, frameon=True)

# Quick sanity check to ensure curves aren't identically zero
print(f"Problem 4 sanity check - Non-zero values: g3D={np.any(g3D > 0)}, g2D={np.any(g2D > 0)}, g1D={np.any(g1D > 0)}")
print(f"Max values before normalization: g3D={np.max(g3D_norm):.2e}, g2D={np.max(g2D_norm):.2e}, g1D={np.max(g1D_norm):.2e}")

# Add plot to HTML report
report.add_plot(fig4, "Normalized density of states comparison showing characteristic behaviors: 3D (√E), 2D (step function), 1D (1/√E divergence). Vertical lines mark subband edges.")

plt.show()

"""
EEE 533 — Problem 5 (4.0 points)
Write a script (Python) to plot the number of electrons and holes per unit volume per unit
energy as a function of energy. For electrons n(E) = g_c(E) f(E), where g_c(E) is the 3D
conduction‑band DOS and f(E) is the Fermi–Dirac function. Total concentrations:
    n = ∫_{E_c}^{∞} n(E) dE,   p = ∫_{-∞}^{E_v} p(E) dE,   with  p(E) = g_v(E)[1 - f(E)].

(a) Plot electron AND hole energy densities vs. energy for E_F = E_C − 0.1 eV.
(b) Plot electron AND hole energy densities vs. energy for E_F = E_V + 0.1 eV.
(c) Compute electron densities for E_F1 = E_C − 0.1 eV and E_F2 = E_C − 0.01 eV via:
    (1) numerical integration, and (2) MB approximation n = N_C * exp((E_F − E_C)/(k_B T)).
(d) Repeat (c) for holes with E_F1 = E_V + 0.1 eV and E_F2 = E_V + 0.01 eV using
    p = N_V * exp((E_V − E_F)/(k_B T)).
(e) From (c)–(d), discuss when MB and Fermi–Dirac agree/differ (print a short note).

Notes:
• Energy in eV; length in cm. Units reported on plots: states/(eV·cm^3).
• 3D parabolic DOS:
    g_c(E) = (1/(2π^2)) * (2 m_e*/ħ^2)^(3/2) * sqrt(E − E_C) * θ(E − E_C)
    g_v(E) = (1/(2π^2)) * (2 m_h*/ħ^2)^(3/2) * sqrt(E_V − E) * θ(E_V − E)
• Use Si DOS masses from the problem statement: m_e* = 1.18 m0, m_h* = 0.81 m0.
"""

# ------------------ Physical constants (SI unless noted) ------------------
kB_eV = 8.617333262145e-5     # eV/K
kB_J  = 1.380649e-23           # J/K
eV_to_J = 1.602176634e-19      # J/eV
hbar = 1.054571817e-34         # J*s
h = 6.62607015e-34             # J*s
m0 = 9.1093837015e-31          # kg
cm_per_m = 100.0

# ------------------ Silicon parameters (given + slides context) ------------------
T = 300.0                      # K
Eg = 1.12                      # eV (Si, 300 K)
me_dos = 1.18 * m0             # kg (given)
mh_dos = 0.81 * m0             # kg (given)

# Place band edges: set E_V = 0, E_C = Eg for clarity when plotting both bands on one axis.
Ev = 0.0
Ec = Ev + Eg

# ------------------ 3D DOS (per eV·cm^3) for parabolic bands ------------------
def g3D_conduction(E):
    """3D conduction DOS g_c(E) in states/(eV·cm^3). E in eV."""
    xJ = np.maximum((E - Ec) * eV_to_J, 0.0)
    pref_SI = (1.0/(2.0*np.pi**2)) * (2.0*me_dos/hbar**2)**1.5  # per (J^(1/2)·m^3)
    g_SI = pref_SI * np.sqrt(xJ)                                # per (J·m^3)
    # convert: per (J·m^3) -> per (eV·cm^3)
    return g_SI * eV_to_J / (cm_per_m**3)

def g3D_valence(E):
    """3D valence DOS g_v(E) in states/(eV·cm^3). E in eV."""
    xJ = np.maximum((Ev - E) * eV_to_J, 0.0)
    pref_SI = (1.0/(2.0*np.pi**2)) * (2.0*mh_dos/hbar**2)**1.5
    g_SI = pref_SI * np.sqrt(xJ)
    return g_SI * eV_to_J / (cm_per_m**3)

# ------------------ Fermi–Dirac and MB helpers ------------------
def fermi(E, EF):
    return 1.0 / (1.0 + np.exp((E - EF)/(kB_eV*T)))

def Nc_cm3(TK=T):
    val_m3 = 2.0 * ((2.0*np.pi*me_dos*kB_J*TK)/(h**2))**1.5
    return val_m3 / 1e6

def Nv_cm3(TK=T):
    val_m3 = 2.0 * ((2.0*np.pi*mh_dos*kB_J*TK)/(h**2))**1.5
    return val_m3 / 1e6

# ------------------ Manual trapezoidal integration (no canned solver) ------------------
def trapz_manual(y, x):
    return np.sum(0.5*(y[1:]+y[:-1])*(x[1:]-x[:-1]))

# ------------------ Energy grids for plotting/integration ------------------
# Cover both valence and conduction with a gap in between for visual clarity.
E_left  = Ev - 0.6
E_right = Ec + 0.6
E = np.linspace(E_left, E_right, 4000)

# Split grids to integrate only where DOS is nonzero
Ec_to_max = np.linspace(Ec, E_right, 3000)    # conduction integration grid
min_to_Ev = np.linspace(E_left, Ev, 3000)     # valence integration grid

# ------------------ Part (a): EF = Ec - 0.1 eV ------------------
EF_a = Ec - 0.1
nE_a = g3D_conduction(E) * fermi(E, EF_a)                # electrons per energy (full axis; nonzero for E>=Ec)
pE_a = g3D_valence(E)   * (1.0 - fermi(E, EF_a))         # holes per energy (nonzero for E<=Ev)

# ------------------ Part (b): EF = Ev + 0.1 eV ------------------
EF_b = Ev + 0.1
nE_b = g3D_conduction(E) * fermi(E, EF_b)
pE_b = g3D_valence(E)   * (1.0 - fermi(E, EF_b))

# ------------------ Part (c): electron densities via integration and MB ------------------
EFc1 = Ec - 0.1
EFc2 = Ec - 0.01
# numerical (integrate only where g_c>0)
n_c1_num = trapz_manual(g3D_conduction(Ec_to_max)*fermi(Ec_to_max, EFc1), Ec_to_max)
n_c2_num = trapz_manual(g3D_conduction(Ec_to_max)*fermi(Ec_to_max, EFc2), Ec_to_max)
# MB approximations
Nc = Nc_cm3(T)
n_c1_MB = Nc*np.exp((EFc1 - Ec)/(kB_eV*T))
n_c2_MB = Nc*np.exp((EFc2 - Ec)/(kB_eV*T))

# ------------------ Part (d): hole densities via integration and MB ------------------
EFd1 = Ev + 0.1
EFd2 = Ev + 0.01
p_d1_num = trapz_manual(g3D_valence(min_to_Ev)*(1.0 - fermi(min_to_Ev, EFd1)), min_to_Ev)
p_d2_num = trapz_manual(g3D_valence(min_to_Ev)*(1.0 - fermi(min_to_Ev, EFd2)), min_to_Ev)
Nv = Nv_cm3(T)
p_d1_MB = Nv*np.exp((Ev - EFd1)/(kB_eV*T))
p_d2_MB = Nv*np.exp((Ev - EFd2)/(kB_eV*T))

# ------------------ Print numerical results (c) & (d) ------------------
print("=== Part (c): electrons at 300 K (states/cm^3) ===")
print(f"EF = Ec - 0.10 eV:   n_num = {n_c1_num:.3e},   n_MB = {n_c1_MB:.3e}")
print(f"EF = Ec - 0.01 eV:   n_num = {n_c2_num:.3e},   n_MB = {n_c2_MB:.3e}")
print("\n=== Part (d): holes at 300 K (states/cm^3) ===")
print(f"EF = Ev + 0.10 eV:   p_num = {p_d1_num:.3e},   p_MB = {p_d1_MB:.3e}")
print(f"EF = Ev + 0.01 eV:   p_num = {p_d2_num:.3e},   p_MB = {p_d2_MB:.3e}")

# Add Problem 5 to HTML report
report.add_heading("Problem 5: Electron and Hole Energy Densities (4.0 points)", 2)

problem5_description = """
<strong>Problem Statement:</strong><br>
Write a script (Python) to plot the number of electrons and holes per unit volume per unit
energy as a function of energy.<br><br>
<strong>Tasks:</strong><br>
(a) Plot electron AND hole energy densities vs. energy for E_F = E_C − 0.1 eV<br>
(b) Plot electron AND hole energy densities vs. energy for E_F = E_V + 0.1 eV<br>
(c) Compute electron densities for two Fermi levels via numerical integration and MB approximation<br>
(d) Repeat (c) for holes<br>
(e) Discuss when MB and Fermi–Dirac agree/differ
"""
report.add_text(problem5_description)

# Add key equations for Problem 5
report.add_text("<strong>Electron Energy Density:</strong>")
report.add_equation(r"n(E) = g_c(E) \cdot f(E)")

report.add_text("<strong>Hole Energy Density:</strong>") 
report.add_equation(r"p(E) = g_v(E) \cdot [1 - f(E)]")

report.add_text("<strong>Fermi-Dirac Distribution:</strong>")
report.add_equation(r"f(E) = \frac{1}{1 + \exp\left(\frac{E - E_F}{k_BT}\right)}")

report.add_text("<strong>Maxwell-Boltzmann Approximations:</strong>")
report.add_equation(r"n = N_C \exp\left(\frac{E_F - E_C}{k_BT}\right)")
report.add_equation(r"p = N_V \exp\left(\frac{E_V - E_F}{k_BT}\right)")

# Add numerical results to HTML
report.add_heading("Numerical Integration vs Maxwell-Boltzmann Comparison", 3)

# Format results for HTML
results_html = f"""
<strong>Part (c): Electrons at 300 K (states/cm³)</strong><br>
EF = Ec - 0.10 eV: n_numerical = {n_c1_num:.3e}, n_MB = {n_c1_MB:.3e}<br>
EF = Ec - 0.01 eV: n_numerical = {n_c2_num:.3e}, n_MB = {n_c2_MB:.3e}<br><br>
<strong>Part (d): Holes at 300 K (states/cm³)</strong><br>
EF = Ev + 0.10 eV: p_numerical = {p_d1_num:.3e}, p_MB = {p_d1_MB:.3e}<br>
EF = Ev + 0.01 eV: p_numerical = {p_d2_num:.3e}, p_MB = {p_d2_MB:.3e}
"""

report.content.append('<div class="result-box">')
report.add_text(results_html)
report.content.append('</div>')

# Add comparison table for better clarity
report.add_results_table(
    ["Fermi Level", "Method", "Electron Density (cm^-3)", "Hole Density (cm^-3)"],
    [
        ["EF = Ec - 0.10 eV", "Numerical", f"{n_c1_num:.3e}", "-"],
        ["EF = Ec - 0.10 eV", "Maxwell-Boltzmann", f"{n_c1_MB:.3e}", "-"],
        ["EF = Ec - 0.01 eV", "Numerical", f"{n_c2_num:.3e}", "-"],
        ["EF = Ec - 0.01 eV", "Maxwell-Boltzmann", f"{n_c2_MB:.3e}", "-"],
        ["EF = Ev + 0.10 eV", "Numerical", "-", f"{p_d1_num:.3e}"],
        ["EF = Ev + 0.10 eV", "Maxwell-Boltzmann", "-", f"{p_d1_MB:.3e}"],
        ["EF = Ev + 0.01 eV", "Numerical", "-", f"{p_d2_num:.3e}"],
        ["EF = Ev + 0.01 eV", "Maxwell-Boltzmann", "-", f"{p_d2_MB:.3e}"]
    ]
)

# ------------------ Part (e): brief comparison message ------------------
def comment_MB_vs_FD():
    msg = []
    msg.append("MB vs Fermi–Dirac: When |E_F - band edge| ≳ ~3–4 k_BT (non-degenerate),")
    msg.append("occupation is small (f << 1 or 1-f << 1), so MB agrees with FD;")
    msg.append("as E_F approaches a band edge within ~k_BT, degeneracy grows and MB deviates.")
    print("\n=== Part (e): Comment ===")
    print(" ".join(msg))
    
    # Add to HTML report
    comment_text = " ".join(msg)
    report.add_heading("Maxwell-Boltzmann vs Fermi-Dirac Analysis", 3)
    report.add_text(f"<strong>Part (e) Discussion:</strong><br>{comment_text}")

comment_MB_vs_FD()

# ------------------ Plotting (a) and (b) ------------------
def plot_case(EF, nE, pE, title_suffix, part_label):
    fig = plt.figure(figsize=(10,6))
    plt.plot(E, nE, 'b-', linewidth=2, label=r'$n(E)=g_c(E)\,f(E)$ (electrons)')
    plt.plot(E, pE, 'r-', linewidth=2, label=r'$p(E)=g_v(E)\,[1-f(E)]$ (holes)')
    # Mark band edges and EF
    plt.axvline(Ev, color='k', ls='--', lw=1, label=r'$E_V$')
    plt.axvline(Ec, color='k', ls='-.', lw=1, label=r'$E_C$')
    plt.axvline(EF, color='orange', ls=':', lw=2, label=r'$E_F$')
    plt.xlim(E_left, E_right)
    plt.ylim(bottom=0)
    plt.xlabel('Energy E (eV)', fontsize=12)
    plt.ylabel(r'Density per energy  [states/(eV·cm$^3$)]', fontsize=12)
    plt.title(f'Problem 5: n(E) & p(E) at T=300 K   ({title_suffix})', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, ls=':', alpha=0.7)
    plt.tight_layout()
    
    # Add to HTML report
    report.add_plot(fig, f"Part {part_label}: Energy density distributions showing {title_suffix}")
    
    plt.show()
    return fig

# Plots for parts (a) and (b)
fig5a = plot_case(EF_a, nE_a, pE_a, r'$E_F = E_C - 0.1\,\mathrm{eV}$', '(a)')
fig5b = plot_case(EF_b, nE_b, pE_b, r'$E_F = E_V + 0.1\,\mathrm{eV}$', '(b)')

# =============================================================================
# Generate HTML Report
# =============================================================================
print("\n" + "="*60)
print("GENERATING HTML REPORT...")
print("="*60)

# Summary section removed per user request

# Save the HTML report
report.save_to_file("Lab1_EEE533_Saif_Elsaady_Report.html")

print("="*60)