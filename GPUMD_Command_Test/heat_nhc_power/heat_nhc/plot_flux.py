#!/usr/bin/env python3
"""
Thermal transport analysis from compute.out
- Temperature profile (last 30%, fixed groups removed, sorted by z)
- Cumulative energy + flux fit → κ (Nature style)
ΔT is taken from the source and sink groups (read from run.in),
excluding any fixed groups.
"""

import argparse, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- Nature‑like style (sans‑serif) ----------
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.linewidth": 1.0,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "lines.linewidth": 1.2,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

try:
    from ase.io import read as ase_read
except ImportError:
    ase_read = None
    print("Warning: ASE not installed; cross‑sectional area unavailable.",
          file=sys.stderr)


def parse_args():
    p = argparse.ArgumentParser(description="Thermal transport analysis from compute.out")
    p.add_argument("path", help="run directory or compute.out file")
    p.add_argument("--sample", type=int, default=None)
    p.add_argument("--output", type=int, default=None)
    p.add_argument("--dt", type=float, default=None, help="time step in fs")
    p.add_argument("--out", default=None, help="output figure name")
    return p.parse_args()


def read_run_in(run_in):
    """
    Parse run.in and return:
      dt, sample_interval, output_interval, source_group, sink_group, set(fixed_groups)
    If not found, returns None for missing values.
    """
    dt = sample = output = None
    source = sink = None
    fixed = set()
    if not os.path.isfile(run_in):
        return dt, sample, output, source, sink, fixed
    for line in open(run_in):
        line = line.split("#")[0]               # remove comment
        tok = line.split()
        if not tok:
            continue
        if tok[0] == "time_step" and len(tok) >= 2:
            try:
                dt = float(tok[1])
            except ValueError:
                pass
        elif tok[0] == "compute":
            ints = []
            for t in tok[1:]:
                try:
                    ints.append(int(t))
                except ValueError:
                    break
            if len(ints) >= 3:                   # compute grouping_method sample_interval output_interval ...
                sample = ints[1]
                output = ints[2]
            elif len(ints) == 2 and sample is None:  # only source & sink
                source = ints[0]
                sink   = ints[1]
        elif tok[0] == "fix":
            for t in tok[1:]:
                try:
                    fixed.add(int(t))
                except ValueError:
                    pass
    return dt, sample, output, source, sink, fixed


def read_model_xyz(fname):
    """Return sorted z‑centers, sort index, cross‑sectional area (Å²),
       number of groups, box length in z (Å)."""
    if not os.path.isfile(fname) or ase_read is None:
        return None, None, None, None, None
    atoms = ase_read(fname)
    cell = atoms.get_cell()
    if cell is not None and cell.rank == 3:
        A = np.linalg.norm(np.cross(cell[0], cell[1]))
        Lz = np.linalg.norm(cell[2])
    else:
        A, Lz = None, None
    zsum, zcnt = {}, {}
    with open(fname) as f:
        n_at = int(f.readline())
        f.readline()   # header
        for i, line in enumerate(f):
            if i >= len(atoms):
                break
            tok = line.split()
            if len(tok) < 5:
                continue
            g = int(tok[-1])
            z = atoms.positions[i, 2]
            zsum[g] = zsum.get(g, 0.0) + z
            zcnt[g] = zcnt.get(g, 0) + 1
    ng = max(zsum) + 1
    z_raw = np.array([zsum[g] / zcnt[g] for g in range(ng)])
    sort_idx = np.argsort(z_raw)
    z_sorted = z_raw[sort_idx]
    return z_sorted, sort_idx, A, ng, Lz


def linear_fit(x, y):
    """Return slope, intercept, R²."""
    p = np.polyfit(x, y, 1)
    y_pred = np.polyval(p, x)
    ss_res = ((y - y_pred) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return p[0], p[1], r2


def main():
    args = parse_args()
    fpath = args.path if os.path.isfile(args.path) else os.path.join(args.path, "compute.out")
    dirname = os.path.dirname(os.path.abspath(fpath))
    if not os.path.isfile(fpath):
        sys.exit(f"File not found: {fpath}")

    # 1. Parse run.in
    dt_r, sample_r, output_r, src_grp, snk_grp, fixed_groups = read_run_in(
        os.path.join(dirname, "run.in"))
    dt   = args.dt    if args.dt    is not None else (dt_r   or 1.0)
    smp  = args.sample if args.sample is not None else (sample_r or 100)
    outv = args.output if args.output is not None else (output_r or 20)
    row_ps = smp * outv * dt / 1000.0

    # 2. Read compute.out
    data = np.loadtxt(fpath)
    if data.ndim == 1:
        data = data[None, :]
    n_rows = data.shape[0]
    e_src = data[:, -2]   # cumulative energy hot source (eV)
    e_snk = data[:, -1]   # cumulative energy cold sink  (eV)
    time_ps = np.arange(n_rows) * row_ps

    # 3. Geometry info
    z_pos, sort_idx, area_A2, ng, Lz = read_model_xyz(os.path.join(dirname, "model.xyz"))
    if z_pos is None:
        ng = data.shape[1] - 2
        z_pos = np.arange(ng)
        sort_idx = np.arange(ng)
        xlabel = "Group index"
        Lz = None
    else:
        xlabel = r"$z$ (Å)"

    # 4. Temperature profile (last 30 %)
    temp_arr = data[:, :ng]
    i_start = int(n_rows * 0.7)
    T_profile = temp_arr[i_start:].mean(axis=0)        # original group order
    T_sorted_all = T_profile[sort_idx]                 # sorted by z

    # Fixed‑group mask
    fixed_mask_orig = np.zeros(ng, dtype=bool)
    for g in fixed_groups:
        if 0 <= g < ng:
            fixed_mask_orig[g] = True
    fixed_mask_sorted = fixed_mask_orig[sort_idx]
    keep = ~fixed_mask_sorted                           # groups to show / use

    z_plot = z_pos[keep]
    T_plot = T_sorted_all[keep]

    # y‑limits
    all_T = temp_arr.flatten()
    all_T = all_T[all_T > 1e-6]
    if len(all_T) > 0:
        T_min, T_max = all_T.min(), all_T.max()
        span = T_max - T_min
        ylim = (T_min - 0.05 * span, T_max + 0.05 * span)
    else:
        ylim = (0, 1)

    # 5. ΔT from source & sink groups (must not be fixed)
    if src_grp is not None and snk_grp is not None:
        if src_grp in fixed_groups or snk_grp in fixed_groups:
            print(f"Warning: source ({src_grp}) or sink ({snk_grp}) is a fixed group.",
                  "Using min/max temperature of non‑fixed groups.", file=sys.stderr)
            src_grp = snk_grp = None   # fallback

    if src_grp is not None and snk_grp is not None and src_grp < ng and snk_grp < ng:
        T_hot  = T_profile[src_grp]
        T_cold = T_profile[snk_grp]
        delta_T = abs(T_hot - T_cold)
    else:
        # Fallback: use min/max of non‑fixed groups
        if len(T_plot) >= 2:
            T_hot  = T_plot[0]   # lowest z
            T_cold = T_plot[-1]  # highest z
            delta_T = abs(T_hot - T_cold)
            src_grp = "auto (min z)"
            snk_grp = "auto (max z)"
        else:
            delta_T = 0.0
            T_hot = T_cold = 0.0

    # Effective length and gradient
    if len(z_plot) >= 2:
        L_eff = z_plot[-1] - z_plot[0]
        grad_T = delta_T / L_eff if L_eff > 0 else None
    else:
        L_eff = None
        grad_T = None

    # 6. Heat flux from energy accumulation (fit last 30 %)
    n_fit = max(int(n_rows * 0.3), 10)
    t_fit = time_ps[-n_fit:]
    e_src_fit = e_src[-n_fit:]
    e_snk_fit = e_snk[-n_fit:]

    J_src_ps, _, r2_src = linear_fit(t_fit, e_src_fit)
    J_snk_ps, _, r2_snk = linear_fit(t_fit, e_snk_fit)
    J_src = abs(J_src_ps) / 1000.0   # eV/fs
    J_snk = abs(J_snk_ps) / 1000.0
    J_avg = 0.5 * (J_src + J_snk)

    # 7. Thermal coefficients
    G = J_avg / delta_T if delta_T > 0 else 0.0
    if area_A2 is not None and grad_T is not None and grad_T > 0:
        kappa_raw = J_avg / (area_A2 * grad_T)
        kappa_SI  = kappa_raw * 1.602176634e6      # W/(m·K)
    else:
        kappa_SI = None

    # 8. Plot
    fig, (axT, axE) = plt.subplots(1, 2, figsize=(10, 4.2))

    # Left: temperature (sorted, fixed groups excluded)
    axT.plot(z_plot, T_plot, "o-", ms=4, color="C0")
    axT.set_xlabel(xlabel)
    axT.set_ylabel("Temperature (K)")
    axT.set_ylim(ylim)
    axT.set_title("Temperature profile (last 30 %)")
    axT.grid(alpha=0.25)
    textstr = f"ΔT = {delta_T:.1f} K"
    if grad_T is not None:
        textstr += f"\ndT/dz = {grad_T:.4f} K/Å"
    axT.text(0.05, 0.95, textstr, transform=axT.transAxes, fontsize=8,
             verticalalignment="top",
             bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.7))

    # Right: cumulative energy + flux fit
    axE.plot(time_ps, e_src, lw=0.8, alpha=0.7, label="Source energy")
    axE.plot(time_ps, e_snk, lw=0.8, alpha=0.7, label="Sink energy")
    axE.axvspan(t_fit[0], t_fit[-1], color="gray", alpha=0.1,
                label="fit region (last 30 %)")
    t_ext = np.array([t_fit[0], t_fit[-1]])
    axE.plot(t_ext, J_src_ps * t_ext + (e_src_fit.mean() - J_src_ps * t_fit.mean()),
             "C0--", lw=1.2, label=f"fit src: {J_src:.5f} eV/fs")
    axE.plot(t_ext, J_snk_ps * t_ext + (e_snk_fit.mean() - J_snk_ps * t_fit.mean()),
             "C1--", lw=1.2, label=f"fit snk: {J_snk:.5f} eV/fs")
    axE.set_xlabel("Time (ps)")
    axE.set_ylabel("Cumulative energy (eV)")
    axE.set_title("Energy accumulation")
    axE.legend(fontsize=7)
    axE.grid(alpha=0.25)

    coeff_str = f"J = {J_avg:.5f} eV/fs\nG = {G:.5f} eV/(fs·K)"
    if kappa_SI is not None:
        coeff_str += f"\nκ = {kappa_SI:.2f} W/(m·K)"
    else:
        coeff_str += "\nκ = N/A"
    axE.text(0.05, 0.95, coeff_str, transform=axE.transAxes, fontsize=8,
             verticalalignment="top",
             bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.7))

    fig.tight_layout()
    out_name = args.out or f"{os.path.basename(dirname)}_analysis.png"
    fig.savefig(out_name, dpi=300)
    print(f"Figure saved to {out_name}")

    # 9. Console summary
    print(f"\n{'='*50}")
    print(f"System: {os.path.basename(dirname)}  |  rows = {n_rows}  |  dt_row = {row_ps:.2f} ps")
    print(f"Source group: {src_grp}  |  Sink group: {snk_grp}")
    print(f"Heat flux (fit last 30 %): {J_avg:.6f} eV/fs")
    print(f"  source fit: {J_src:.6f} eV/fs  R²={r2_src:.6f}")
    print(f"  sink fit:   {J_snk:.6f} eV/fs  R²={r2_snk:.6f}")
    print(f"Temperature difference: ΔT = {delta_T:.1f} K")
    if grad_T is not None:
        print(f"Effective length L_eff = {L_eff:.3f} Å, dT/dz = {grad_T:.6f} K/Å")
    else:
        print("Temperature gradient not available.")
    print(f"Thermal conductance: G = {G:.6f} eV/(fs·K)")
    if kappa_SI is not None:
        print(f"Thermal conductivity: κ = {kappa_SI:.2f} W/(m·K)")
    else:
        print("Thermal conductivity: insufficient data.")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
