"""Pedagogical finite-field constraint models. NOT a SNARK or production exploit."""

P = 11

def eq(a: int, b: int, modulus: int = P) -> bool:
    return (a - b) % modulus == 0


def binding_weak(x: int, w0: int, w1: int, w2: int, w3: int) -> bool:
    """x is public; w0..w3 are private; x is deliberately unbound."""
    return eq(w1, w0*w0) and eq(w2, w1*w1) and eq(w3, w2+5)


def binding_fixed(x: int, w0: int, w1: int, w2: int, w3: int) -> bool:
    return binding_weak(x, w0, w1, w2, w3) and eq(w3, x)


def selector_weak(x: int, y: int, z: int, s: int) -> bool:
    """x,y,z public, selector s private, all arithmetic in F_11."""
    return eq(z, s*x + (1-s)*y)


def selector_fixed(x: int, y: int, z: int, s: int) -> bool:
    return selector_weak(x, y, z, s) and eq(s*(s-1), 0)


def iszero_weak(a: int, out: int, hint: int) -> bool:
    """a,out public; inverse hint private."""
    return eq(out, 1-a*hint)


def iszero_fixed(a: int, out: int, hint: int) -> bool:
    return iszero_weak(a, out, hint) and eq(a*out, 0)


def foreign_weak(x: int, y: int, z: int, quotient: int) -> bool:
    """A quotient equation in native F_11 for claimed multiplication mod 3."""
    return eq(x*y-z, 3*quotient)


def foreign_fixed(x: int, y: int, z: int, quotient: int) -> bool:
    return (all(v in range(3) for v in (x,y,z))
            and quotient in (0,1)
            and foreign_weak(x,y,z,quotient))


def fake_glv_weak(s: int, u: int, v: int, point: int, result: int, k: int) -> bool:
    """Toy model: prime-order subgroup as additive Z/5; scalar check in F_11.

    `point` and `result` are elements of the order-five group; NOT actual EC points.
    """
    return ((u*point - v*result) % 5 == 0
            and eq(u-s*v, 5*k))


def fake_glv_fixed(s: int, u: int, v: int, point: int, result: int) -> bool:
    return (v%5 != 0 and (u-s*v)%5 == 0
            and (u*point-v*result)%5 == 0)


def attack_examples() -> list[tuple[str, bool, bool, str]]:
    """name, vulnerable accepted, repaired accepted, explanatory witness."""
    return [
        ("missing public binding", binding_weak(7,1,1,1,6), binding_fixed(7,1,1,1,6),
         "x=7; w=(1,1,1,6); no fourth root of 2 in F_11"),
        ("non-Boolean selector", selector_weak(3,7,5,6), selector_fixed(3,7,5,6),
         "(x,y,z;s)=(3,7,5;6)"),
        ("unvalidated inverse hint", iszero_weak(3,1,0), iszero_fixed(3,1,0),
         "public (a,out)=(3,1); private hint=0"),
        ("unbounded foreign-field quotient", foreign_weak(2,2,0,5), foreign_fixed(2,2,0,5),
         "mod 3: 2*2 != 0; native F_11 quotient k=5"),
        ("free quotient in toy fake GLV", fake_glv_weak(2,0,1,1,0,4),
         fake_glv_fixed(2,0,1,1,0), "s=2,u=0,v=1,P=1,Q=0,k=4; Q != sP in Z/5"),
    ]


def main() -> None:
    for name, vulnerable, repaired, witness in attack_examples():
        assert vulnerable and not repaired, (name, vulnerable, repaired)
        print(f"[{name}]\n  witness: {witness}\n  vulnerable: ACCEPT\n  repaired:   REJECT\n")
    print("All five educational counterexamples reproduced.")

if __name__ == "__main__":
    main()
