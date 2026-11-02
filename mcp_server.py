"""
MCP Server for Respiratory Muscle Strength (MIP/MEP) & Diaphragmatic Pump.
Exposes JSON-RPC endpoints for evaluating maximal static respiratory pressures against normative models.
"""

import json
import sys
from client import RespiratoryMuscleStrengthClient

client = RespiratoryMuscleStrengthClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_respiratory_pressures",
                        "description": "Evaluates Maximal Inspiratory Pressure (MIP) and Maximal Expiratory Pressure (MEP) in cmH2O against Black & Hyatt normative equations.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "measured_mip_cmh2o": {"type": "number", "description": "Maximal inspiratory pressure in cmH2O (e.g. 115.0)"},
                                "measured_mep_cmh2o": {"type": "number", "description": "Maximal expiratory pressure in cmH2O (e.g. 185.0)"},
                                "age_years": {"type": "number", "description": "Subject age in years (e.g. 35.0)"},
                                "is_female": {"type": "boolean", "default": False, "description": "True for female reference formula"}
                            },
                            "required": ["measured_mip_cmh2o", "measured_mep_cmh2o", "age_years"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "evaluate_respiratory_pressures":
            res = client.evaluate_respiratory_pressures(
                measured_mip_cmh2o=args.get("measured_mip_cmh2o", 115.0),
                measured_mep_cmh2o=args.get("measured_mep_cmh2o", 185.0),
                age_years=args.get("age_years", 35.0),
                is_female=args.get("is_female", False)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
