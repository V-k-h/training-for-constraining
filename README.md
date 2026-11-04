# Training for Constraining

**How to Prevent Circuit-Level Bugs** — educational companion repository for a 50-minute Devcon workshop by Levi Katyal Sledd and Vijay Singh. Example models use $\mathbb{F}_{11}$ unless otherwise stated.

> **Security scope:** These are purpose-built mathematical *constraint models*, not deployed Circom/Noir/gnark circuits or production exploit reproductions. The fake-GLV example is an intentionally simplified algebraic illustration, not a confirmed reproduction of any specific gnark CVE. A successful Lean theorem for the model does not imply compiled-circuit security.

## Quick start — no dependencies

Python 3.10+ is sufficient:

```bash
git clone https://github.com/V-k-h/training-for-constraining
cd training-for-constraining
make demo
make test
```

Demonstrations produce counterexamples accepted by intentionally vulnerable models but rejected after repair:

| Example | Vulnerability | Added requirement |
|---|---|---|
| Missing public binding | Witness output not tied to public input | `out = x` |
| Non-Boolean selector | `s` may be arbitrary field element | `s(s-1) = 0` |
| Unvalidated hint | Prover controls inverse hint | `a*out = 0` |
| Foreign-field quotient | Free quotient satisfies native equation | All domains/quotient range constrained |
| Fake-GLV **toy** | Quotient absorbs scalar mismatch | Scalar congruence and nonzero cancellation scalar |

## Lean 4 proofs (optional)

A standalone Lean/mathlib project lives in [`lean/`](lean/):

```bash
cd lean
lake exe cache get   # downloads prebuilt Mathlib, several GB on first run
lake build
```

or simply `make lean` from the repository root. Dependencies are pinned in `lean/lean-toolchain` and `lean/lake-manifest.json`, so `lake update` is not needed.

It includes:

- `Workshop/Selector.lean`: concrete bad selector witness; corrected soundness over **any field**; false instance rejected.
- `Workshop/Quotient.lean`: free quotient in a native field; scalar cancellation over a vector space with explicit nonzero and equality hypotheses.

**Verification note:** All five theorems compile with Lean 4.24.0 and Mathlib v4.24.0 and depend only on the standard axioms (`propext`, `Classical.choice`, `Quot.sound`); no `sorry` is used. The `Lean proofs` GitHub Actions workflow rebuilds them on every change under `lean/`. A theorem about the algebraic model is a statement about that model only, not about any compiled circuit.

## LLZK (optional)

[`llzk/`](llzk/) contains two genuine LLZK-syntax IR source examples for missing public-output binding: `and_vulnerable.llzk` and `and_fixed.llzk`. Their structure follows the official [LLZK AND example](https://github.com/project-llzk/llzk-lib/blob/main/doc/doxygen/03_syntax.md).

With a compatible [LLZK](https://github.com/project-llzk/llzk-lib) toolchain:

```bash
make llzk-check
```

The two files match the official AND example in the upstream syntax document operation for operation; they have not yet been run through `llzk-opt`. To check them, build `llzk-opt` from a pinned `llzk-lib` release and run `make llzk-check`. Parsing verifies the IR only: it is **not** a soundness proof. See [`llzk/README.md`](llzk/README.md) for the distinction.

## Slides

[`slides/workshop.pdf`](slides/workshop.pdf) is the current workshop deck, built from [`slides/workshop.tex`](slides/workshop.tex). Presenter notes are in [`slides/speaker-notes.pdf`](slides/speaker-notes.pdf), and a three-page note on how SMT solvers decide these queries, and where Lean takes over, is in [`notes/smt-ring-theory.pdf`](notes/smt-ring-theory.pdf).

To rebuild with [tectonic](https://tectonic-typesetting.github.io/):

```bash
make slides          # deck
make speaker-notes   # deck, then notes
```

If you build with `pdflatex` instead, run it twice: the title-slide QR code is placed on the second pass.

## Explore further

1. Run `make demo` and find the non-Boolean selector: the vulnerable relation accepts $z = 5$ although it is neither input, and adding $s(s-1)=0$ rejects it.
2. Read `selector_sound` in [`lean/Workshop/Selector.lean`](lean/Workshop/Selector.lean): the same repair, proved for every field.
3. Run `diff -u llzk/and_vulnerable.llzk llzk/and_fixed.llzk`: both compute `out = a*b`, but only one constrains it. Witness computation is not enforcement.
4. Read [`notes/smt-ring-theory.pdf`](notes/smt-ring-theory.pdf) for how SMT solvers decide these soundness queries, and where Lean proofs take over.

## Sources and acknowledgments

- [LLZK project](https://github.com/project-llzk/llzk-lib) and [IR specification](https://github.com/project-llzk/llzk-lib/blob/main/doc/doxygen/03_syntax.md) — open source, developed by Veridise with Ethereum Foundation support.
- [Lean 4](https://lean-lang.org/) and [Mathlib](https://github.com/leanprover-community/mathlib4).
- gnark fake GLV, the workshop's case study: the [vulnerable `scalarMulFakeGLV` in v0.15.0](https://github.com/Consensys-Incorporated/gnark/blob/v0.15.0/std/algebra/native/twistededwards/point.go#L129-L182), with an unbounded quotient, and the [repair in v0.16.0](https://github.com/Consensys-Incorporated/gnark/blob/v0.16.0/std/algebra/native/twistededwards/scalar_decomp.go), which checks the scalar decomposition in emulated arithmetic and constrains the result to the prime-order subgroup. See also [PR #1765](https://github.com/Consensys-Incorporated/gnark/pull/1765).

The MIT license applies to this repository's original examples and notes. It does not relicense the upstream LLZK or Lean/Mathlib projects, and it does not cover the OpenZeppelin name or logo.
