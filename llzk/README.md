# LLZK: missing public-output binding

Two LLZK IR examples model an honest `AND`/multiplication gate. The `@compute` function is identical in both examples and produces `out = a*b`. Only `@constrain` differs:

- `and_vulnerable.llzk`: computes the multiplication but **does not constrain the public `out` member**.
- `and_fixed.llzk`: enforces `out = a*b` via `constrain.eq`.

This makes the central workshop distinction visible at IR level: *witness generation is not a constraint*. The example closely follows the upstream LLZK language-specification AND gate: https://github.com/project-llzk/llzk-lib/blob/main/doc/doxygen/03_syntax.md .

## Optional LLZK parser check

Requires an independently installed version of upstream `llzk-opt` compatible with the dialect syntax:

```sh
llzk-opt llzk/and_vulnerable.llzk -o /dev/null
llzk-opt llzk/and_fixed.llzk -o /dev/null
```

You can also run `make llzk-check`, which checks both with `llzk-opt` and errors if the executable is absent. The scripts **do not** claim these files were automatically proven unsound/sound by the LLZK compiler; `llzk-opt` parsing/IR verification is different from semantic verification.

### Real formal verification backend

Upstream LLZK supports analysis/translation routes, including SMT and zkLean, but using them requires backend-specific lowering and specifications. This repository intentionally does **not** claim to provide an end-to-end configured LLZK-to-SMT or LLZK-to-Lean proof pipeline. Compare [LLZK tool guides](https://github.com/project-llzk/llzk-lib/blob/main/doc/doxygen/02_tools.md). The standalone Lean theorems formalize the same *mathematical security properties*, not a mechanically linked proof of these LLZK files.

Upstream LLZK is under active development. Test against a pinned `llzk-lib` release/commit before a public live demonstration.
