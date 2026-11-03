---
name: genpark-personal-agent-respiratory-muscle-strength-mip-mep-skill
description: Deterministic evaluation of Maximal Inspiratory Pressure (MIP), Maximal Expiratory Pressure (MEP), Black & Hyatt norms, and diaphragmatic pump resilience.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Respiratory Muscle Strength (MIP/MEP) Skill

## Overview
The `genpark-personal-agent-respiratory-muscle-strength-mip-mep-skill` brings clinical respiratory mechanics analytics to sovereign personal agents. Maximal Inspiratory Pressure (MIP) measures the contractile force of the diaphragm and external intercostals during a maximal effort from residual volume. Maximal Expiratory Pressure (MEP) assesses the force of abdominal wall muscles and internal intercostals from total lung capacity. Using the standard Black & Hyatt age- and sex-stratified normative equations, this skill identifies isolated diaphragmatic weakness and guides Inspiratory Muscle Training (IMT) load regimens.

## Physiological Model & Mathematics
1. **Black & Hyatt Prediction Equations**:
   - **Males**:
     $$\text{MIP}_{\text{pred}} = 143 - (0.55 \times \text{Age}) \quad \text{cmH}_2\text{O}$$
     $$\text{MEP}_{\text{pred}} = 268 - (1.03 \times \text{Age}) \quad \text{cmH}_2\text{O}$$
   - **Females**:
     $$\text{MIP}_{\text{pred}} = 104 - (0.51 \times \text{Age}) \quad \text{cmH}_2\text{O}$$
     $$\text{MEP}_{\text{pred}} = 170 - (0.53 \times \text{Age}) \quad \text{cmH}_2\text{O}$$
2. **Percentage of Predicted Pressure**:
   $$\%\text{MIP} = \frac{\text{MIP}_{\text{meas}}}{\text{MIP}_{\text{pred}}} \times 100\%, \quad \%\text{MEP} = \frac{\text{MEP}_{\text{meas}}}{\text{MEP}_{\text{pred}}} \times 100\%$$
   - **Normal Function**: $\ge 80\%$.
   - **Clinically Significant Weakness / LLN**: $< 65\%$.
3. **Diaphragmatic Muscle Resilience Index ($DMRI$)**:
   Standardized 0 to 100 rating mapping composite ventilatory pump capacity.

## Tools & Endpoints
- `evaluate_respiratory_pressures`: Computes predicted MIP/MEP, % of predicted, weakness patterns, and diaphragmatic resilience score.
