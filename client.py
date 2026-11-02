"""
Respiratory Muscle Strength (MIP/MEP) & Diaphragmatic Pump Engine.
Provides deterministic, zero-dependency modeling of Maximal Inspiratory Pressure (MIP),
Maximal Expiratory Pressure (MEP), Black & Hyatt age/sex normative benchmarks, and respiratory pump power.
"""

from typing import Dict, Any, List, Optional


class RespiratoryMuscleStrengthClient:
    """
    Deterministic client for calculating Maximal Inspiratory (MIP) and Expiratory (MEP) Pressures in cmH2O.
    Pure Python standard library implementation based on Black & Hyatt and ATS/ERS Respiratory Muscle Testing standards.
    """

    def __init__(self):
        pass

    def evaluate_respiratory_pressures(
        self,
        measured_mip_cmh2o: float,
        measured_mep_cmh2o: float,
        age_years: float,
        is_female: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates MIP and MEP against Black & Hyatt normative equations:
        Males:
          MIP_pred = 143 - (0.55 * age)
          MEP_pred = 268 - (1.03 * age)
        Females:
          MIP_pred = 104 - (0.51 * age)
          MEP_pred = 170 - (0.53 * age)
        """
        if measured_mip_cmh2o <= 0 or measured_mep_cmh2o <= 0 or age_years < 10.0:
            return {"error": "Pressures and age must be positive values"}

        age = max(18.0, min(90.0, age_years))

        if is_female:
            mip_pred = round(104.0 - (0.51 * age), 1)
            mep_pred = round(170.0 - (0.53 * age), 1)
        else:
            mip_pred = round(143.0 - (0.55 * age), 1)
            mep_pred = round(268.0 - (1.03 * age), 1)

        pct_mip = round((measured_mip_cmh2o / mip_pred) * 100.0, 1)
        pct_mep = round((measured_mep_cmh2o / mep_pred) * 100.0, 1)

        # Diaphragmatic Muscle Resilience Index (DMRI, 0 - 100):
        # Average of % predicted MIP and MEP mapped to 0-100 scale (100% = 85 score)
        mean_pct = (pct_mip + pct_mep) / 2.0
        if mean_pct >= 80.0:
            dmri = min(100.0, 75.0 + ((mean_pct - 80.0) / 20.0) * 20.0)
        elif mean_pct >= 60.0:
            dmri = 50.0 + ((mean_pct - 60.0) / 20.0) * 24.0
        elif mean_pct >= 40.0:
            dmri = 25.0 + ((mean_pct - 40.0) / 20.0) * 24.0
        else:
            dmri = max(5.0, (mean_pct / 40.0) * 24.0)

        dmri_score = round(min(100.0, max(5.0, dmri)), 1)

        is_diaphragm_weak = pct_mip < 65.0
        is_expiratory_weak = pct_mep < 65.0

        if dmri_score >= 80.0:
            status = "ROBUST_RESPIRATORY_PUMP_STRENGTH"
            interpretation = f"Normal inspiratory ({pct_mip}% pred) and expiratory ({pct_mep}% pred) contractile force; diaphragm and abdominal pump fully intact."
            guidance = "Ventilatory muscle endurance is optimal. Full capacity for strenuous athletic hyperpnea."
        elif is_diaphragm_weak and not is_expiratory_weak:
            status = "ISOLATED_INSPIRATORY_DIAPHRAGMATIC_WEAKNESS"
            interpretation = f"Attenuated MIP ({pct_mip}% pred) with preserved MEP; indicates diaphragmatic or external intercostal fatigue/atrophy."
            guidance = "Implement Inspiratory Muscle Training (IMT) protocol: 30 breaths twice daily at 50% of MIP using a threshold resistance device."
        elif is_expiratory_weak and not is_diaphragm_weak:
            status = "ISOLATED_EXPIRATORY_ABDOMINAL_WEAKNESS"
            interpretation = f"Attenuated MEP ({pct_mep}% pred); indicates abdominal wall and internal intercostal muscle deconditioning."
            guidance = "Incorporate forced exhalation drills, abdominal core bracing, and cough clearance training."
        elif is_diaphragm_weak and is_expiratory_weak:
            status = "GENERALIZED_RESPIRATORY_MUSCLE_FATIGUE"
            interpretation = f"Bilateral respiratory muscle weakness (MIP {pct_mip}%, MEP {pct_mep}%); compromised ventilatory pump reserve."
            guidance = "Recommend clinical pulmonology review, rule out phrenic nerve impairment or generalized neuromuscular fatigue."
        else:
            status = "MILD_RESPIRATORY_PUMP_ATTENUATION"
            interpretation = f"Borderline pressures (MIP {pct_mip}%, MEP {pct_mep}%); mild deconditioning."
            guidance = "Add deep diaphragmatic breathing against resistance and maintain posture extension."

        return {
            "measured_mip_cmh2o": measured_mip_cmh2o,
            "predicted_mip_cmh2o": mip_pred,
            "pct_predicted_mip": pct_mip,
            "measured_mep_cmh2o": measured_mep_cmh2o,
            "predicted_mep_cmh2o": mep_pred,
            "pct_predicted_mep": pct_mep,
            "diaphragmatic_resilience_index": dmri_score,
            "status": status,
            "physiological_interpretation": interpretation,
            "actionable_guidance": guidance
        }
