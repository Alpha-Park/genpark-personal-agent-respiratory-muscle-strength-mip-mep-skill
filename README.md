# Respiratory Muscle Strength (MIP/MEP) Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](https://github.com/alphaparkinc/genpark-personal-agent-respiratory-muscle-strength-mip-mep-skill)
[![OpenClaw Ready](https://img.shields.io/badge/OpenClaw-Compatible-purple.svg)](https://github.com/alphaparkinc/genpark-personal-agent-respiratory-muscle-strength-mip-mep-skill)
[![MCP Protocol](https://img.shields.io/badge/MCP-Standard-orange.svg)](https://modelcontextprotocol.io/)

A sovereign personal agent capability for computational respiratory physiology, evaluating Maximal Inspiratory (MIP) and Expiratory (MEP) Pressures in cmH2O, Black & Hyatt models, and diaphragmatic pump strength.

## Architecture

```mermaid
flowchart TD
    PatientData["Demographics: Age & Sex"] --> NormativeModel["Black & Hyatt Prediction Equations (MIP_pred & MEP_pred)"]
    MIPMEPData["Measured Static Pressures: MIP (cmH2O) & MEP (cmH2O)"] --> RatioEngine["Percentage of Predicted Force: (Measured / Predicted) * 100%"]
    NormativeModel --> RatioEngine
    RatioEngine --> DMRI["Diaphragmatic Muscle Resilience Index (DMRI: 0 - 100)"]
    DMRI --> IMTPlan["OpenClaw / Hermes Inspiratory Muscle Training (50% MIP) Prescriptions"]
```

## Quickstart

```python
from client import RespiratoryMuscleStrengthClient

client = RespiratoryMuscleStrengthClient()

# Assess respiratory pressures (32-year-old male)
res = client.evaluate_respiratory_pressures(
    measured_mip_cmh2o=132.0,
    measured_mep_cmh2o=245.0,
    age_years=32.0,
    is_female=False
)

print("MIP % Predicted:", res["pct_predicted_mip"], "%")
print("MEP % Predicted:", res["pct_predicted_mep"], "%")
print("Resilience Score:", res["diaphragmatic_resilience_index"], "/ 100")
print("Status:", res["status"])
```

## MCP Server Integration

Add to your `claude_desktop_config.json` or OpenClaw tool registry:

```json
{
  "mcpServers": {
    "respiratory-muscle-strength": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-respiratory-muscle-strength-mip-mep-skill/mcp_server.py"]
    }
  }
}
```

## License
MIT License.
