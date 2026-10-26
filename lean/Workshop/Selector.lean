import Mathlib

/-! Public inputs x,y,z; private witness s. No auxiliary-witness category. -/
namespace Workshop

/-- `ZMod 11` is a field because 11 is prime; Mathlib needs this fact in scope. -/
instance : Fact (Nat.Prime 11) := ⟨by norm_num⟩

def selector {F : Type*} [Field F] (x y z s : F) : Prop :=
  z = s * x + (1 - s) * y

def selectorFixed {F : Type*} [Field F] (x y z s : F) : Prop :=
  selector x y z s ∧ s * (s - 1) = 0

-- An explicit counterexample over F_11: the broken relation accepts z = 5,
-- which is neither input, using the non-Boolean selector s = 6.
theorem selector_counterexample :
    selector (3 : ZMod 11) 7 5 6 ∧
      (5 : ZMod 11) ≠ 3 ∧ (5 : ZMod 11) ≠ 7 := by
  unfold selector
  decide

-- Once booleanity is enforced, the output is necessarily x or y.
theorem selector_sound {F : Type*} [Field F]
    (x y z s : F) (h : selectorFixed x y z s) :
    z = x ∨ z = y := by
  rcases h with ⟨heq, hbool⟩
  rcases mul_eq_zero.mp hbool with hs | hs
  · right
    simpa [selector, hs] using heq
  · have hs1 : s = 1 := sub_eq_zero.mp hs
    left
    simpa [selector, hs1] using heq

-- The repaired circuit cannot accept the malicious public instance.
theorem selector_repaired_rejects :
    ¬ ∃ s : ZMod 11, selectorFixed 3 7 5 s := by
  rintro ⟨s, h⟩
  rcases selector_sound 3 7 5 s h with hx | hy
  · exact absurd hx (by decide)
  · exact absurd hy (by decide)

end Workshop
