"""
Example usage for Respiratory Muscle Strength (MIP/MEP) Skill.
Demonstrates analyzing maximal static respiratory pressures against Black & Hyatt norms.
"""

from client import RespiratoryMuscleStrengthClient


def main():
    client = RespiratoryMuscleStrengthClient()

    print("=== 1. Evaluating Respiratory Pressures (32-Year-Old Male Athlete) ===")
    res_athlete = client.evaluate_respiratory_pressures(
        measured_mip_cmh2o=132.0,
        measured_mep_cmh2o=245.0,
        age_years=32.0,
        is_female=False
    )

    print(f"Measured MIP: {res_athlete['measured_mip_cmh2o']} cmH2O (Predicted: {res_athlete['predicted_mip_cmh2o']} cmH2O, {res_athlete['pct_predicted_mip']}%)")
    print(f"Measured MEP: {res_athlete['measured_mep_cmh2o']} cmH2O (Predicted: {res_athlete['predicted_mep_cmh2o']} cmH2O, {res_athlete['pct_predicted_mep']}%)")
    print(f"Diaphragmatic Resilience Score: {res_athlete['diaphragmatic_resilience_index']} / 100")
    print(f"Status: {res_athlete['status']}")
    print(f"Interpretation: {res_athlete['physiological_interpretation']}")
    print(f"Guidance: {res_athlete['actionable_guidance']}")

    print("\n=== 2. Evaluating Pressures with Isolated Diaphragmatic Fatigue ===")
    res_fatigue = client.evaluate_respiratory_pressures(
        measured_mip_cmh2o=72.0,
        measured_mep_cmh2o=220.0,
        age_years=32.0,
        is_female=False
    )

    print(f"MIP % Predicted: {res_fatigue['pct_predicted_mip']}% | MEP % Predicted: {res_fatigue['pct_predicted_mep']}%")
    print(f"Status: {res_fatigue['status']}")
    print(f"Guidance: {res_fatigue['actionable_guidance']}")


if __name__ == "__main__":
    main()
