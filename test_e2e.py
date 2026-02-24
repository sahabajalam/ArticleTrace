import time
import requests
import json

payload = {
    "system_description": "An AI-powered facial recognition system used to track employee attendance and monitor workstation presence throughout the day. The system uses high-resolution cameras installed at every desk and cross-references faces with the HR database to log working hours automatically.",
    "system_type": "facial_recognition",
    "deployment_context": "employee_monitoring",
    "company_name": "Acme Corp"
}

print("Starting EU AI Act assessment via Core 3 Orchestrator...")
resp = requests.post("http://localhost:8000/api/v1/assessments", json=payload)
resp.raise_for_status()
session_id = resp.json()["session_id"]
print(f"Assessment started! Session ID: {session_id}")

print("Polling for results (this may take a couple of minutes as multiple agents execute)...")
while True:
    res = requests.get(f"http://localhost:8000/api/v1/assessments/{session_id}")
    data = res.json()
    status = data["status"]
    print(f"Status: {status}")
    
    # Check if we need human approval
    if status == "paused":
        print("\nWorkflow paused for human approval!")
        
        # Get approvals
        approvals_resp = requests.get("http://localhost:8000/api/v1/approvals")
        pending = approvals_resp.json().get("pending_approvals", [])
        
        if pending:
            req_id = pending[0]["id"]
            print(f"Approving request {req_id} automatically for testing...")
            approve_payload = {
                "decision": "approved",
                "reviewer_id": "test_admin",
                "notes": "Looks good, proceed."
            }
            requests.post(f"http://localhost:8000/api/v1/approvals/{req_id}/decide", json=approve_payload)
            print("Approval submitted. Workflow should resume.")
            
    if status in ["completed", "failed"]:
        print("\n\nFINAL RESULT HIGHLIGHTS:")
        print("Risk Classification:")
        print(json.dumps(data.get("risk_classification"), indent=2))
        
        print("\nGDPR Audit Summary:")
        gdpr = data.get("gdpr_audit") or {}
        is_compliant = gdpr.get('gdpr_compliant')
        print(f"Compliant: {is_compliant}")
        if not is_compliant:
            print("Violations:", json.dumps(gdpr.get("violations", []), indent=2))
            
        print("\nFinal Report Generator:")
        report = data.get("final_report") or {}
        print(f"Compliance Score: {report.get('compliance_score')}/100")
        print(f"Documents Generated: {report.get('documents_generated', 0)}")
        
        print("\nCost Tracking:")
        print(json.dumps(data.get("cost_tracking"), indent=2))
        
        break
    time.sleep(5)
