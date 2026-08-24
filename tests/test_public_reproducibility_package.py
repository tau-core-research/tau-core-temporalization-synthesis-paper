import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_publication_files_exist():
    for rel in [
        "LICENSE",
        "CITATION.cff",
        "DATA_NOTICE.md",
        "README.md",
        "temporalization_synthesis_submission_source/main.tex",
        "temporalization_synthesis_submission_source/refs.bib",
        "temporalization_synthesis_submission_source/main.pdf",
        "figures/fig_dependency_ownership_map.pdf",
        "figures/fig_temporalization_proof_spine.pdf",
        "data/derived/temporal_synthesis_ledger.json",
        "data/derived/temporal_synthesis_audit.json",
        "arxiv_submission_source.zip",
    ]:
        assert (ROOT / rel).exists(), rel


def test_manuscript_scope_and_nonredundancy_markers():
    tex = (ROOT / "temporalization_synthesis_submission_source/main.tex").read_text()
    for marker in [
        "Temporalization of an Atemporal Parent",
        "Nonredundancy and ownership",
        "Temporalization synthesis theorem",
        "Observer ticks do not identify Parent proto-rate",
        "Source-calibrated rate and the remaining ontological stop",
        "Finite interventional simulation no-go",
        "Formation budget, four-dimensional exchange and dark-sector limits",
        "Operational equivalence and the limit of finite experiments",
        "History refinement without a Parent history store",
        "Record persistence is not an entropy arrow",
        "Common ownership no-go and minimal free-action completion",
        "Configuration-Laplacian free action and the front-entropy no-go",
        "H(F_n\\mid Y_n)\\ge0",
        "Proof ladder, falsification and current status",
        "component results compose",
    ]:
        assert marker in tex, marker
    assert "Tau Core is proven" not in tex
    assert "dark matter is derived" not in tex
    assert "Nature selects the enriched temporal completion" not in tex


def test_result_ledger_claim_boundaries():
    data = json.loads((ROOT / "data/derived/temporal_synthesis_ledger.json").read_text())
    assert len(data["result_groups"]) == 32
    claims = data["synthesis_claims"]
    assert claims["temporal_completion_is_fibered_enhancement"] is True
    assert claims["eocc_actuality_is_derived_from_old_bare_tau"] is False
    assert claims["observer_tick_count_is_reparameterization_invariant_on_a_monotone_complete_path"] is True
    assert claims["observer_tick_intensity_identifies_parent_front_rate_without_independent_calibration"] is False
    assert claims["arbitrarily_many_uncalibrated_observers_identify_parent_front_rate"] is False
    assert claims["absolute_proto_rate_is_defined_without_parent_scale_anchor"] is False
    assert claims["source_calibrated_proto_rate_is_reparameterization_invariant"] is True
    assert claims["calibrated_order_proves_literal_parent_evolution"] is False
    assert claims["clock_mobility_product_is_reparameterization_invariant"] is True
    assert claims["calibrated_eocc_proves_literal_parent_evolution"] is False
    assert claims["eocc_and_record_persistence_force_entropy_arrow"] is False
    assert claims["visible_refinement_with_consistent_ensemble_has_nonnegative_readout_entropy_increment"] is True
    assert claims["accessible_readout_entropy_is_already_thermodynamic_entropy"] is False
    assert claims["common_source_ownership_with_front_novelty_forces_thermodynamic_entropy_arrow"] is False
    assert claims["free_action_identity_with_conserved_energy_and_positive_fixed_scale_forces_local_entropy_growth"] is True
    assert claims["free_action_and_front_macroterminal_laws_are_derived_from_current_tau_source"] is False
    assert claims["configuration_laplacian_has_exact_logarithmic_mean_eocc_free_action_form"] is True
    assert claims["front_conditional_entropy_generically_equals_thermodynamic_entropy_production"] is False
    assert claims["physical_front_to_thermodynamic_configuration_incidence_is_derived"] is False
    assert claims["sbmr_plus_heat_forces_front_configuration_incidence"] is False
    assert claims["primitive_atomic_coownership_conditionally_fixes_unique_incidence"] is True
    assert claims["one_universal_seed_forces_faithful_front_thermal_modules"] is False
    assert claims["faithful_dimension_exhaustive_modules_force_rank_one_atomic_matching"] is True
    assert claims["paired_cyclic_dimension_matched_modules_force_rank_one_atomic_matching"] is True
    assert claims["front_cyclicity_alone_forces_thermal_cyclicity"] is False
    assert claims["primitive_mixed_block_injectivity_forces_paired_cyclicity"] is True
    assert claims["positive_stability_and_stacked_rank_force_each_leg_complete"] is False
    assert claims["equal_mixed_block_kernels_define_unique_maximal_common_faithful_quotient"] is True
    assert claims["body_essential_seed_minimality_forces_equal_postbody_kernels"] is False
    assert claims["past_hypothesis_is_solved"] is False
    assert claims["finite_internal_interventions_identify_ontic_traversal"] is False
    assert claims["formation_budget_is_already_4d_energy"] is False
    assert claims["dark_sector_is_derived"] is False
    assert claims["decisive_empirical_temporal_signal_exists"] is False
    assert claims["nature_selection_of_the_temporal_completion_is_proved"] is False
    assert len(data["remaining_blockers"]) >= 5


def test_finite_audit_results():
    data = json.loads((ROOT / "data/derived/temporal_synthesis_audit.json").read_text())
    assert data["ledger_group_count"] == 32
    assert data["exact_cochain"]["consistent_diamond_exact"] is True
    assert data["exact_cochain"]["acyclic_inconsistent_diamond_nonexact"] is True
    assert data["eocc"]["strict_action_descent"] is True
    assert data["eocc"]["positive_actuality_certificate"] is True
    assert data["eocc"]["descent_equals_minus_certificate"] is True
    assert data["calibrated_eocc"]["clock_mobility_product_is_invariant"] is True
    assert data["calibrated_eocc"]["physical_eocc_rate_is_invariant"] is True
    assert data["calibrated_eocc"]["physical_action_release_is_positive"] is True
    assert data["calibrated_eocc"]["simultaneous_orbit_reproduces_temporal_composition"] is True
    assert data["formation_budget"]["finite_budget_identity"] is True
    assert data["interventional_simulation"]["finite_dag_and_simultaneous_relation_agree"] is True
    assert data["no_retro"]["normalized_future_kernels"] is True
    assert data["no_retro"]["early_marginal_setting_independent"] is True
    assert data["entropy_arrow"]["same_eocc_orbit_allows_positive_entropy_rate"] is True
    assert data["entropy_arrow"]["same_eocc_orbit_allows_negative_entropy_rate"] is True
    assert data["entropy_arrow"]["readout_chain_rule_identity"] is True
    assert data["entropy_arrow"]["visible_refinement_entropy_nonnegative"] is True
    assert data["entropy_arrow"]["hidden_fiber_nonfactorization_detected"] is True
    assert data["entropy_arrow"]["factorizing_control_has_no_hidden_fiber_split"] is True
    assert data["common_source_entropy"]["same_packet_has_hidden_front_novelty"] is True
    assert data["common_source_entropy"]["same_packet_allows_positive_entropy_rate"] is True
    assert data["common_source_entropy"]["same_packet_allows_negative_entropy_rate"] is True
    assert data["common_source_entropy"]["free_action_completion_has_positive_entropy_rate"] is True
    assert data["common_source_entropy"]["free_action_rate_equals_dissipation_over_theta"] is True
    assert data["common_source_entropy"]["energy_drift_can_reverse_entropy_rate"] is True
    assert data["configuration_laplacian_thermodynamics"]["logarithmic_mean_onsager_flow_equals_heat_flow"] is True
    assert data["configuration_laplacian_thermodynamics"]["configuration_laplacian_is_symmetric_positive_semidefinite"] is True
    assert data["configuration_laplacian_thermodynamics"]["laplacian_entropy_rate_matches_pair_sum"] is True
    assert data["configuration_laplacian_thermodynamics"]["laplacian_entropy_rate_is_positive_off_equilibrium"] is True
    assert data["configuration_laplacian_thermodynamics"]["relative_entropy_action_has_exact_free_action_decomposition"] is True
    assert data["configuration_laplacian_thermodynamics"]["fmt_identity_requires_negative_residual_at_equilibrium_control"] is True
    assert data["tfci_incidence"]["common_atom_lift_is_unique_identity"] is True
    assert data["tfci_incidence"]["common_atom_lift_preserves_incidence"] is True
    assert data["tfci_incidence"]["common_atom_lift_preserves_measure"] is True
    assert data["tfci_incidence"]["source_depth_activation_is_positive"] is True
    assert data["tfci_incidence"]["constant_control_incidence_is_noninjective"] is True
    assert data["tfci_incidence"]["complete_front_readout_cannot_factor_through_constant_incidence"] is True
    assert data["tfci_incidence"]["same_seed_faithful_and_nonfaithful_thermal_actions_are_unital"] is True
    assert data["tfci_incidence"]["faithful_thermal_action_has_rank_one_atoms"] is True
    assert data["tfci_incidence"]["nonfaithful_thermal_action_collapses_one_atom"] is True
    assert data["tfci_incidence"]["primitive_seed_projectors_are_orthogonal_and_exhaustive"] is True
    assert data["tfci_incidence"]["cyclic_front_evaluation_is_invertible"] is True
    assert data["tfci_incidence"]["cyclic_thermal_evaluation_is_invertible"] is True
    assert data["tfci_incidence"]["paired_cyclic_gram_is_positive_definite"] is True
    assert data["tfci_incidence"]["same_seed_noncyclic_thermal_gram_is_singular"] is True
    assert data["tfci_incidence"]["front_cyclicity_does_not_force_thermal_cyclicity"] is True
    assert data["tfci_incidence"]["joint_hessian_response_is_h_inverse_b"] is True
    assert data["tfci_incidence"]["full_rank_mixed_blocks_give_positive_work_grams"] is True
    assert data["tfci_incidence"]["positive_stable_hessian_does_not_prevent_thermal_source_erasure"] is True
    assert data["tfci_incidence"]["stacked_source_completeness_does_not_force_each_leg_complete"] is True
    assert data["tfci_incidence"]["equal_kernel_descents_define_faithful_common_quotient"] is True
    assert data["tfci_incidence"]["equal_rank_descents_can_have_different_kernels"] is True
    assert data["tfci_incidence"]["injective_master_does_not_force_equal_descent_kernels"] is True


def test_arxiv_archive_is_source_only_and_complete():
    with zipfile.ZipFile(ROOT / "arxiv_submission_source.zip") as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "figures/fig_dependency_ownership_map.pdf" in names
    assert "figures/fig_temporalization_proof_spine.pdf" in names
    assert "main.pdf" not in names
    assert not any(name.endswith((".aux", ".log", ".toc", ".out")) for name in names)
