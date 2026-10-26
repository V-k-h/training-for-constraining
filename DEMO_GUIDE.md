# Live demo guide (about 4 minutes)

## 0. Before the session

Run `make all` locally and confirm all 7 tests succeed. Install Lean and LLZK separately if you intend to run their optional commands; preflight them **on the same laptop used for presenting**. Keep the Python demo as an offline fallback.

## 1. Produce counterexamples — 45 seconds

```sh
make demo
```

Point to the `non-Boolean selector` witness `(x,y,z;s)=(3,7,5;6)` over `F_11`:

- Intended: `z = x` or `z = y`.
- Enforced: `z = s*x + (1-s)*y`.
- Prover supplies `s=6`; arithmetic yields `z=5`, which is neither input.

## 2. Repair — 30 seconds

Add `s*(s-1)=0`. In a field this forces `s=0` or `s=1`, so the gadget produces `y` or `x`.

## 3. Show a universal Lean theorem — 60 seconds

Open `lean/Workshop/Selector.lean` and point at `selector_sound`. Explain `mul_eq_zero.mp` and the two cases. If preflight succeeded, run `make lean` or `cd lean && lake build` (the former also updates dependencies). Be clear that a proof of the mathematical model is not a compiler validation result.

## 4. Show LLZK IR — 60 seconds

```sh
diff -u llzk/and_vulnerable.llzk llzk/and_fixed.llzk
```

The honest `@compute` function is unchanged, while only the repaired `@constrain` binds the public output. The LLZK example intentionally demonstrates a different bug from the selector to make the general principle clear.

If `llzk-opt` was independently installed and preflighted, run `make llzk-check`. Parsing **is not formal verification**.

## 5. Takeaway — 20 seconds

> A prover can replace every private witness and hint. Only enforced constraints bind the public claim. Verify the exact assumptions of dependencies and compilers, not only the application source.
