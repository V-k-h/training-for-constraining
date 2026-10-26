# Training for Constraining

**How to Prevent Circuit-Level Bugs** — educational companion repository for a 50-minute Devcon workshop by Levi Katyal Sledd and Vijay Singh. Example models use \(\mathbb F_{11}\) unless otherwise stated.

> **Security scope:** These are purpose-built mathematical *constraint models*, not deployed Circom/Noir/gnark circuits or production exploit reproductions. The fake-GLV example is an intentionally simplified algebraic illustration, not a confirmed reproduction of any specific gnark CVE. A successful Lean theorem for the model does not imply compiled-circuit security.

## Quick start — no dependencies

Python 3.10+ is sufficient:

```bash
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
lake update
lake exe cache get
lake build
```

It includes:

- `Workshop/Selector.lean`: concrete bad selector witness; corrected soundness over **any field**; false instance rejected.
- `Workshop/Quotient.lean`: free quotient in a native field; scalar cancellation over a vector space with explicit nonzero and equality hypotheses.

**Verification note:** Lean and Mathlib are not installed in the environment in which this archive was assembled. The Lean files were prepared but **not compiler-checked** here. Validate with a pinned toolchain locally before public presentation, and fix API differences if the upstream package has changed. Python checks were executed here.

## LLZK (optional)

[`llzk/`](llzk/) contains two genuine LLZK-syntax IR source examples for missing public-output binding: `and_vulnerable.llzk` and `and_fixed.llzk`. Their structure follows the official [LLZK AND example](https://github.com/project-llzk/llzk-lib/blob/main/doc/doxygen/03_syntax.md).

With a compatible [LLZK](https://github.com/project-llzk/llzk-lib) toolchain:

```bash
make llzk-check
```

`llzk-opt` was **not available in the packaging environment**, so the examples need parser verification before being used live. Running `llzk-opt` merely verifies/parses IR: it is **not** a soundness proof. See [`llzk/README.md`](llzk/README.md) for the distinction.

## Slides

[`slides/workshop.pdf`](slides/workshop.pdf) and [`slides/workshop.tex`](slides/workshop.tex) are the current workshop deck. If `openzeppelin-logo.png` is not available, the LaTeX source uses a text fallback.

## Suggested live sequence (3–5 minutes)

1. Show a false selector statement accepted by the broken relation: `make demo`.
2. Explain the repair: `s(s-1)=0`.
3. Display the universal theorem in `lean/Workshop/Selector.lean` (run `lake build` beforehand).
4. Compare `llzk/and_vulnerable.llzk` with `llzk/and_fixed.llzk`: witness computation is not enforcement.
5. Return to the gnark dependency story: this same separation can occur inside a third-party gadget.

## Sources and acknowledgments

- [LLZK project](https://github.com/project-llzk/llzk-lib) and [IR specification](https://github.com/project-llzk/llzk-lib/blob/main/doc/doxygen/03_syntax.md) — open source, developed by Veridise with Ethereum Foundation support.
- [Lean 4](https://lean-lang.org/) and [Mathlib](https://github.com/leanprover-community/mathlib4).
- The workshop case study of fake GLV should always be paired with the exact published affected versions and repair when discussing real implementations.

The educational repository's MIT license applies to this repository's original examples and notes; it does not relicense the upstream LLZK or Lean/Mathlib projects. Review use of names and logos before publishing under an organization's branding.
