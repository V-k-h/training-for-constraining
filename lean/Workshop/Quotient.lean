import Mathlib

namespace Workshop

-- Over the native field, a prover-controlled quotient is vacuous.
-- This is a theorem over any field, not merely an F_11 test.
theorem free_quotient {F : Type*} [Field F]
    (u s v ell : F) (hell : ell ≠ 0) :
    ∃ k : F, u - s * v = k * ell := by
  refine ⟨(u - s * v) / ell, ?_⟩
  field_simp

-- A toy algebraic version of the scalar cancellation argument.
-- V is a vector space over F; actual elliptic curve subgroup
-- membership and scalar representation must be justified separately.
theorem scalar_cancellation
    {F : Type*} {V : Type*}
    [Field F] [AddCommGroup V] [Module F V]
    (s u v : F) (P Q : V)
    (hv : v ≠ 0)
    (hscalar : u = s * v)
    (hcurve : u • P = v • Q) :
    Q = s • P := by
  have h : v • Q = v • (s • P) := by
    calc
      v • Q = u • P := hcurve.symm
      _ = (s * v) • P := by rw [hscalar]
      _ = v • (s • P) := by rw [mul_comm s v, mul_smul]
  have h' := congrArg (fun R : V => (v⁻¹) • R) h
  simpa [smul_smul, inv_mul_cancel₀ hv] using h'

end Workshop
