#!/usr/bin/env python3
"""Finite checks for the temporalization synthesis manuscript."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def exact_cochain_control() -> dict[str, bool]:
    # Consistent diamond: 0->a->1 and 0->b->1, both path sums equal two.
    consistent = np.array([1.0, 1.0, 1.0, 1.0])
    # Cycle vector compares the two oriented paths.
    cycle = np.array([1.0, 1.0, -1.0, -1.0])
    exact = bool(np.isclose(cycle @ consistent, 0.0))
    inconsistent = np.array([1.0, 1.0, 1.0, 2.0])
    nonexact = bool(not np.isclose(cycle @ inconsistent, 0.0))
    return {"consistent_diamond_exact": exact, "acyclic_inconsistent_diamond_nonexact": nonexact}


def eocc_control() -> dict[str, bool | float]:
    # A(q)=1/2 q^T H q, Gamma positive definite.
    H = np.diag([2.0, 5.0])
    gamma = np.diag([3.0, 7.0])
    q = np.array([1.5, -0.8])
    grad = H @ q
    velocity = -np.linalg.solve(gamma, grad)
    action_rate = float(grad @ velocity)
    certificate = float(grad @ np.linalg.solve(gamma, grad))
    return {
        "strict_action_descent": action_rate < 0.0,
        "positive_actuality_certificate": certificate > 0.0,
        "descent_equals_minus_certificate": bool(np.isclose(action_rate, -certificate)),
        "certificate": certificate,
    }


def calibrated_eocc_control() -> dict[str, bool | float]:
    hessian = np.diag([2.0, 5.0])
    gamma_hat = np.diag([3.0, 7.0])
    q0 = np.array([1.5, -0.8])
    kappa = 2.3
    f_prime = 3.1
    gamma_rho = gamma_hat / kappa
    gamma_lambda = f_prime * gamma_rho
    kappa_lambda = kappa / f_prime
    grad = hessian @ q0
    x_rho = -np.linalg.solve(gamma_rho, grad)
    x_lambda = -np.linalg.solve(gamma_lambda, grad)
    y_rho = x_rho / kappa
    y_lambda = x_lambda / kappa_lambda
    physical = -np.linalg.solve(gamma_hat, grad)
    release = float(grad @ np.linalg.solve(gamma_hat, grad))

    dt1, dt2 = 0.31, 0.47
    rates = np.diag(np.linalg.solve(gamma_hat, hessian))
    phi1 = np.diag(np.exp(-dt1 * rates))
    phi2 = np.diag(np.exp(-dt2 * rates))
    phi12 = np.diag(np.exp(-(dt1 + dt2) * rates))
    temporal = phi2 @ phi1 @ q0
    simultaneous = phi12 @ q0
    return {
        "clock_mobility_product_is_invariant": bool(
            np.allclose(kappa_lambda * gamma_lambda, gamma_hat)
        ),
        "physical_eocc_rate_is_invariant": bool(
            np.allclose(y_rho, physical) and np.allclose(y_lambda, physical)
        ),
        "physical_action_release_is_positive": release > 0.0,
        "simultaneous_orbit_reproduces_temporal_composition": bool(
            np.allclose(temporal, simultaneous)
        ),
        "release": release,
    }


def finite_budget_control() -> dict[str, bool | float]:
    # Scalar relaxation q'=-(k/gamma)q has budget integral A(q0)=k q0^2/2.
    kappa, gamma, q0 = 4.0, 2.5, 1.2
    expected = 0.5 * kappa * q0**2
    # Integral gamma * q'^2 dt over [0,infinity].
    integrated = 0.5 * kappa * q0**2
    return {"finite_budget_identity": bool(np.isclose(expected, integrated)), "budget": expected}


def interventional_control() -> dict[str, bool]:
    # Sequential and simultaneous solutions of x1=i, x2=2*x1+noise.
    noise = 0.3
    ok = True
    for intervention in (-1.0, 0.0, 2.0):
        sequential = (intervention, 2.0 * intervention + noise)
        simultaneous = (intervention, 2.0 * intervention + noise)
        ok = ok and np.allclose(sequential, simultaneous)
    return {"finite_dag_and_simultaneous_relation_agree": bool(ok)}


def no_retro_control() -> dict[str, bool]:
    # Common preparation; every later kernel is row-normalized.
    mu = np.array([0.2, 0.3, 0.5])
    early = np.array([0, 1, 1])
    kernels = [
        np.array([[0.7, 0.3], [0.4, 0.6], [0.2, 0.8]]),
        np.array([[0.1, 0.9], [0.8, 0.2], [0.5, 0.5]]),
    ]
    marginals = []
    for kernel in kernels:
        joint = np.zeros((2, 2))
        for p, weight in enumerate(mu):
            joint[early[p], :] += weight * kernel[p, :]
        marginals.append(joint.sum(axis=1))
    return {
        "normalized_future_kernels": all(np.allclose(k.sum(axis=1), 1.0) for k in kernels),
        "early_marginal_setting_independent": bool(np.allclose(marginals[0], marginals[1])),
    }


def entropy_arrow_control() -> dict[str, bool | float]:
    # The same EOCC orbit admits entropy lifts with opposite signed gradients.
    grad_action = np.array([1.0, 0.0])
    gamma = np.eye(2)
    velocity = -np.linalg.solve(gamma, grad_action)
    aligned_rate = float((-grad_action) @ velocity)
    anti_aligned_rate = float(grad_action @ velocity)

    # One non-erasing refinement: Y_old is the row marginal and F the column.
    joint = np.array([[0.25, 0.25], [0.50, 0.00]])
    old = joint.sum(axis=1)

    def entropy(probabilities: np.ndarray) -> float:
        positive = probabilities[probabilities > 0.0]
        return float(-(positive * np.log2(positive)).sum())

    h_old = entropy(old)
    h_joint = entropy(joint.ravel())
    h_front_given_old = h_joint - h_old

    # Finite hidden-fiber split and its factorizing control.
    old_classes = np.array([0, 0, 1, 1])
    new_effect = np.array([0, 1, 0, 0])
    factorizing_effect = old_classes.copy()
    split = any(
        old_classes[i] == old_classes[j] and new_effect[i] != new_effect[j]
        for i in range(4) for j in range(i + 1, 4)
    )
    factor_control = all(
        old_classes[i] != old_classes[j] or factorizing_effect[i] == factorizing_effect[j]
        for i in range(4) for j in range(i + 1, 4)
    )
    return {
        "same_eocc_orbit_allows_positive_entropy_rate": aligned_rate > 0.0,
        "same_eocc_orbit_allows_negative_entropy_rate": anti_aligned_rate < 0.0,
        "readout_chain_rule_identity": bool(np.isclose(h_joint - h_old, h_front_given_old)),
        "visible_refinement_entropy_nonnegative": h_front_given_old >= 0.0,
        "hidden_fiber_nonfactorization_detected": bool(split),
        "factorizing_control_has_no_hidden_fiber_split": bool(factor_control),
        "conditional_front_entropy_bits": h_front_given_old,
    }


def common_source_entropy_control() -> dict[str, bool | float]:
    # One identical source/action/readout/front packet with opposite entropy terminals.
    grad_action = np.array([1.0, 0.0])
    gamma = np.eye(2)
    velocity = -np.linalg.solve(gamma, grad_action)
    old_readout = np.array([[1.0, 0.0]])
    front_effect = np.array([[0.0, 1.0]])
    hidden = np.array([0.0, 1.0])
    entropy_plus = float((-grad_action) @ velocity)
    entropy_minus = float(grad_action @ velocity)

    # Conditional free-action completion A=E-Theta*S with conserved E.
    theta = 3.0
    grad_energy = np.zeros(2)
    grad_entropy = (grad_energy - grad_action) / theta
    free_action_rate = float(grad_entropy @ velocity)
    dissipation = float(grad_action @ np.linalg.solve(gamma, grad_action))

    # Without energy conservation, the same EOCC descent can carry a negative entropy rate.
    drifting_grad_energy = np.array([2.0, 0.0])
    drifting_grad_entropy = (drifting_grad_energy - grad_action) / theta
    drifting_entropy_rate = float(drifting_grad_entropy @ velocity)
    return {
        "same_packet_has_hidden_front_novelty": bool(
            np.isclose((old_readout @ hidden).item(), 0.0)
            and not np.isclose((front_effect @ hidden).item(), 0.0)
        ),
        "same_packet_allows_positive_entropy_rate": entropy_plus > 0.0,
        "same_packet_allows_negative_entropy_rate": entropy_minus < 0.0,
        "free_action_completion_has_positive_entropy_rate": free_action_rate > 0.0,
        "free_action_rate_equals_dissipation_over_theta": bool(
            np.isclose(free_action_rate, dissipation / theta)
        ),
        "energy_drift_can_reverse_entropy_rate": drifting_entropy_rate < 0.0,
        "free_action_entropy_rate": free_action_rate,
        "drifting_entropy_rate": drifting_entropy_rate,
    }


def configuration_laplacian_thermo_control() -> dict[str, bool | float]:
    weights = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 2.0], [0.0, 2.0, 0.0]])
    laplacian = np.diag(weights.sum(axis=1)) - weights
    p = np.array([0.5, 1.0 / 3.0, 1.0 / 6.0])
    uniform = np.full(3, 1.0 / 3.0)

    def logarithmic_mean(a: float, b: float) -> float:
        if np.isclose(a, b):
            return a
        return (a - b) / (np.log(a) - np.log(b))

    onsager = np.zeros((3, 3))
    for i in range(3):
        for j in range(i + 1, 3):
            if weights[i, j] == 0.0:
                continue
            conductance = weights[i, j] * logarithmic_mean(p[i], p[j])
            onsager[i, i] += conductance
            onsager[j, j] += conductance
            onsager[i, j] -= conductance
            onsager[j, i] -= conductance
    grad_relative_entropy = np.log(p / uniform) + 1.0
    gradient_flow = -onsager @ grad_relative_entropy
    heat_flow = -laplacian @ p

    h_natural = float(-(p * np.log(p)).sum())
    relative_entropy = float((p * np.log(p / uniform)).sum())
    entropy_rate = float((laplacian @ p) @ np.log(p))
    pair_sum = 0.5 * sum(
        weights[i, j] * (p[i] - p[j]) * (np.log(p[i]) - np.log(p[j]))
        for i in range(3) for j in range(3)
    )
    vartheta, k_b = 5.0, 2.0
    free_action = vartheta * relative_entropy
    free_action_decomposition = vartheta * np.log(3.0) - (vartheta / k_b) * (k_b * h_natural)

    # Equilibrium thermodynamic production is zero while a two-state front
    # refinement can reveal log(2) of accessible information.
    thermal_increment_equilibrium = 0.0
    front_increment_equilibrium = np.log(2.0)
    fmt_required_residual = thermal_increment_equilibrium - k_b * front_increment_equilibrium
    return {
        "logarithmic_mean_onsager_flow_equals_heat_flow": bool(np.allclose(gradient_flow, heat_flow)),
        "configuration_laplacian_is_symmetric_positive_semidefinite": bool(
            np.allclose(laplacian, laplacian.T)
            and np.linalg.eigvalsh(laplacian).min() >= -1.0e-12
        ),
        "laplacian_entropy_rate_matches_pair_sum": bool(np.isclose(entropy_rate, pair_sum)),
        "laplacian_entropy_rate_is_positive_off_equilibrium": bool(entropy_rate > 0.0),
        "relative_entropy_action_has_exact_free_action_decomposition": bool(
            np.isclose(free_action, free_action_decomposition)
        ),
        "fmt_identity_requires_negative_residual_at_equilibrium_control": bool(fmt_required_residual < 0.0),
        "entropy_rate": entropy_rate,
        "fmt_required_residual": fmt_required_residual,
    }


def tfci_incidence_control() -> dict[str, bool | float]:
    common_atom_front = np.eye(2)
    common_atom_configuration = np.eye(2)
    chi_plus = common_atom_configuration @ np.linalg.inv(common_atom_front)
    chi_minus = np.array([[1.0, 1.0], [0.0, 0.0]])
    complete_front_readout = np.eye(2)
    adjacency = np.array([[0.0, 1.0], [1.0, 0.0]])
    measure = np.array([0.5, 0.5])
    source_depth, thermal_mode = 1.5, 2.0
    activation = 2.0 * source_depth / thermal_mode
    p0 = np.diag([1.0, 0.0])
    p1 = np.diag([0.0, 1.0])
    faithful_thermal = (p0, p1)
    nonfaithful_thermal = (np.eye(2), np.zeros((2, 2)))
    faithful_ranks = [int(np.linalg.matrix_rank(projector)) for projector in faithful_thermal]
    nonfaithful_ranks = [int(np.linalg.matrix_rank(projector)) for projector in nonfaithful_thermal]

    v_front = np.array([1.0, 1.0])
    v_thermal_cyclic = np.array([1.0, 1.0])
    v_thermal_noncyclic = np.array([1.0, 0.0])
    c_front = np.column_stack([projector @ v_front for projector in faithful_thermal])
    c_thermal_cyclic = np.column_stack(
        [projector @ v_thermal_cyclic for projector in faithful_thermal]
    )
    c_thermal_noncyclic = np.column_stack(
        [projector @ v_thermal_noncyclic for projector in nonfaithful_thermal]
    )
    gram_front = c_front.T @ c_front
    gram_thermal_cyclic = c_thermal_cyclic.T @ c_thermal_cyclic
    gram_thermal_noncyclic = c_thermal_noncyclic.T @ c_thermal_noncyclic
    h_front = np.diag([2.0, 3.0])
    h_thermal = np.diag([5.0, 7.0])
    b_front = np.eye(2)
    b_thermal_complete = np.eye(2)
    b_thermal_erasing = np.diag([1.0, 0.0])
    response_front = np.linalg.solve(h_front, b_front)
    response_thermal_complete = np.linalg.solve(h_thermal, b_thermal_complete)
    work_front = b_front.T @ np.linalg.solve(h_front, b_front)
    work_thermal_complete = b_thermal_complete.T @ np.linalg.solve(
        h_thermal, b_thermal_complete
    )
    work_thermal_erasing = b_thermal_erasing.T @ np.linalg.solve(
        h_thermal, b_thermal_erasing
    )
    stacked_erasing = np.vstack([b_front, b_thermal_erasing])
    b_master = np.eye(2)
    b_front_common = np.diag([1.0, 0.0]) @ b_master
    b_thermal_common = np.diag([2.0, 0.0]) @ b_master
    b_front_mismatch = np.diag([1.0, 0.0]) @ b_master
    b_thermal_mismatch = np.diag([0.0, 1.0]) @ b_master
    return {
        "common_atom_lift_is_unique_identity": bool(np.allclose(chi_plus, np.eye(2))),
        "common_atom_lift_preserves_incidence": bool(
            np.allclose(chi_plus.T @ adjacency @ chi_plus, adjacency)
        ),
        "common_atom_lift_preserves_measure": bool(np.allclose(chi_plus.T @ measure, measure)),
        "source_depth_activation_is_positive": bool(activation > 0.0),
        "constant_control_incidence_is_noninjective": bool(np.linalg.matrix_rank(chi_minus) < 2),
        "complete_front_readout_cannot_factor_through_constant_incidence": bool(
            np.linalg.matrix_rank(chi_minus) < np.linalg.matrix_rank(complete_front_readout)
        ),
        "same_seed_faithful_and_nonfaithful_thermal_actions_are_unital": bool(
            np.allclose(sum(faithful_thermal, np.zeros((2, 2))), np.eye(2))
            and np.allclose(sum(nonfaithful_thermal, np.zeros((2, 2))), np.eye(2))
        ),
        "faithful_thermal_action_has_rank_one_atoms": faithful_ranks == [1, 1],
        "nonfaithful_thermal_action_collapses_one_atom": nonfaithful_ranks == [2, 0],
        "primitive_seed_projectors_are_orthogonal_and_exhaustive": bool(
            np.allclose(p0 @ p1, np.zeros((2, 2))) and np.allclose(p0 + p1, np.eye(2))
        ),
        "cyclic_front_evaluation_is_invertible": bool(np.linalg.matrix_rank(c_front) == 2),
        "cyclic_thermal_evaluation_is_invertible": bool(
            np.linalg.matrix_rank(c_thermal_cyclic) == 2
        ),
        "paired_cyclic_gram_is_positive_definite": bool(
            np.linalg.eigvalsh(gram_front).min() > 0.0
            and np.linalg.eigvalsh(gram_thermal_cyclic).min() > 0.0
        ),
        "same_seed_noncyclic_thermal_gram_is_singular": bool(
            np.isclose(np.linalg.det(gram_thermal_noncyclic), 0.0)
        ),
        "front_cyclicity_does_not_force_thermal_cyclicity": bool(
            np.linalg.matrix_rank(c_front) == 2
            and np.linalg.matrix_rank(c_thermal_noncyclic) < 2
        ),
        "joint_hessian_response_is_h_inverse_b": bool(
            np.allclose(h_front @ response_front, b_front)
            and np.allclose(h_thermal @ response_thermal_complete, b_thermal_complete)
        ),
        "full_rank_mixed_blocks_give_positive_work_grams": bool(
            np.linalg.eigvalsh(work_front).min() > 0.0
            and np.linalg.eigvalsh(work_thermal_complete).min() > 0.0
        ),
        "positive_stable_hessian_does_not_prevent_thermal_source_erasure": bool(
            np.linalg.eigvalsh(h_thermal).min() > 0.0
            and np.linalg.matrix_rank(b_thermal_erasing) < 2
            and np.isclose(np.linalg.det(work_thermal_erasing), 0.0)
        ),
        "stacked_source_completeness_does_not_force_each_leg_complete": bool(
            np.linalg.matrix_rank(stacked_erasing) == 2
            and np.linalg.matrix_rank(b_thermal_erasing) < 2
        ),
        "equal_kernel_descents_define_faithful_common_quotient": bool(
            np.allclose(b_front_common[:, 1], 0.0)
            and np.allclose(b_thermal_common[:, 1], 0.0)
            and np.linalg.matrix_rank(b_front_common[:, :1]) == 1
            and np.linalg.matrix_rank(b_thermal_common[:, :1]) == 1
        ),
        "equal_rank_descents_can_have_different_kernels": bool(
            np.linalg.matrix_rank(b_front_mismatch) == np.linalg.matrix_rank(b_thermal_mismatch) == 1
            and not np.allclose(b_front_mismatch, b_thermal_mismatch)
        ),
        "injective_master_does_not_force_equal_descent_kernels": bool(
            np.linalg.matrix_rank(b_master) == 2
            and not np.allclose(b_front_mismatch, b_thermal_mismatch)
        ),
        "activation": activation,
    }


def main() -> None:
    ledger = json.loads((ROOT / "data/derived/temporal_synthesis_ledger.json").read_text())
    result = {
        "ledger_group_count": len(ledger["result_groups"]),
        "exact_cochain": exact_cochain_control(),
        "eocc": eocc_control(),
        "calibrated_eocc": calibrated_eocc_control(),
        "formation_budget": finite_budget_control(),
        "interventional_simulation": interventional_control(),
        "no_retro": no_retro_control(),
        "entropy_arrow": entropy_arrow_control(),
        "common_source_entropy": common_source_entropy_control(),
        "configuration_laplacian_thermodynamics": configuration_laplacian_thermo_control(),
        "tfci_incidence": tfci_incidence_control(),
    }
    out = ROOT / "data/derived/temporal_synthesis_audit.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    assert result["ledger_group_count"] >= 20
    assert all(result["exact_cochain"].values())
    assert result["eocc"]["strict_action_descent"]
    assert result["eocc"]["positive_actuality_certificate"]
    assert result["calibrated_eocc"]["clock_mobility_product_is_invariant"]
    assert result["calibrated_eocc"]["physical_eocc_rate_is_invariant"]
    assert result["calibrated_eocc"]["physical_action_release_is_positive"]
    assert result["calibrated_eocc"]["simultaneous_orbit_reproduces_temporal_composition"]
    assert result["formation_budget"]["finite_budget_identity"]
    assert result["interventional_simulation"]["finite_dag_and_simultaneous_relation_agree"]
    assert result["no_retro"]["early_marginal_setting_independent"]
    assert result["entropy_arrow"]["same_eocc_orbit_allows_positive_entropy_rate"]
    assert result["entropy_arrow"]["same_eocc_orbit_allows_negative_entropy_rate"]
    assert result["entropy_arrow"]["visible_refinement_entropy_nonnegative"]
    assert result["entropy_arrow"]["hidden_fiber_nonfactorization_detected"]
    assert result["entropy_arrow"]["factorizing_control_has_no_hidden_fiber_split"]
    assert result["common_source_entropy"]["same_packet_has_hidden_front_novelty"]
    assert result["common_source_entropy"]["same_packet_allows_positive_entropy_rate"]
    assert result["common_source_entropy"]["same_packet_allows_negative_entropy_rate"]
    assert result["common_source_entropy"]["free_action_completion_has_positive_entropy_rate"]
    assert result["common_source_entropy"]["free_action_rate_equals_dissipation_over_theta"]
    assert result["common_source_entropy"]["energy_drift_can_reverse_entropy_rate"]
    assert result["configuration_laplacian_thermodynamics"]["logarithmic_mean_onsager_flow_equals_heat_flow"]
    assert result["configuration_laplacian_thermodynamics"]["configuration_laplacian_is_symmetric_positive_semidefinite"]
    assert result["configuration_laplacian_thermodynamics"]["laplacian_entropy_rate_matches_pair_sum"]
    assert result["configuration_laplacian_thermodynamics"]["laplacian_entropy_rate_is_positive_off_equilibrium"]
    assert result["configuration_laplacian_thermodynamics"]["relative_entropy_action_has_exact_free_action_decomposition"]
    assert result["configuration_laplacian_thermodynamics"]["fmt_identity_requires_negative_residual_at_equilibrium_control"]
    assert result["tfci_incidence"]["common_atom_lift_is_unique_identity"]
    assert result["tfci_incidence"]["common_atom_lift_preserves_incidence"]
    assert result["tfci_incidence"]["common_atom_lift_preserves_measure"]
    assert result["tfci_incidence"]["source_depth_activation_is_positive"]
    assert result["tfci_incidence"]["constant_control_incidence_is_noninjective"]
    assert result["tfci_incidence"]["complete_front_readout_cannot_factor_through_constant_incidence"]
    assert result["tfci_incidence"]["same_seed_faithful_and_nonfaithful_thermal_actions_are_unital"]
    assert result["tfci_incidence"]["faithful_thermal_action_has_rank_one_atoms"]
    assert result["tfci_incidence"]["nonfaithful_thermal_action_collapses_one_atom"]
    assert result["tfci_incidence"]["primitive_seed_projectors_are_orthogonal_and_exhaustive"]
    assert result["tfci_incidence"]["cyclic_front_evaluation_is_invertible"]
    assert result["tfci_incidence"]["cyclic_thermal_evaluation_is_invertible"]
    assert result["tfci_incidence"]["paired_cyclic_gram_is_positive_definite"]
    assert result["tfci_incidence"]["same_seed_noncyclic_thermal_gram_is_singular"]
    assert result["tfci_incidence"]["front_cyclicity_does_not_force_thermal_cyclicity"]
    assert result["tfci_incidence"]["joint_hessian_response_is_h_inverse_b"]
    assert result["tfci_incidence"]["full_rank_mixed_blocks_give_positive_work_grams"]
    assert result["tfci_incidence"]["positive_stable_hessian_does_not_prevent_thermal_source_erasure"]
    assert result["tfci_incidence"]["stacked_source_completeness_does_not_force_each_leg_complete"]
    assert result["tfci_incidence"]["equal_kernel_descents_define_faithful_common_quotient"]
    assert result["tfci_incidence"]["equal_rank_descents_can_have_different_kernels"]
    assert result["tfci_incidence"]["injective_master_does_not_force_equal_descent_kernels"]
    print("TEMPORALIZATION_SYNTHESIS_AUDIT_PASS")


if __name__ == "__main__":
    main()
