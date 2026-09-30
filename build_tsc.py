#!/usr/bin/env python3
"""Build the machine-readable SOC 2 Trust Services Criteria dataset.

Source verified against the AICPA 2017 Trust Services Criteria (TSP Section 100,
with 2022 revised points of focus): 61 criteria total.
  - Security (Common Criteria, mandatory for every SOC 2): 33
  - Availability (optional): 3
  - Processing Integrity (optional): 3 -> actually 5, see below
  - Confidentiality (optional): 2
  - Privacy (optional): 18

Summaries and evidence suggestions are original plain-English text written for
this dataset, not AICPA verbatim. Criterion IDs are factual identifiers.
"""
import json, csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

SERIES = {
    "CC1": "Control Environment",
    "CC2": "Communication and Information",
    "CC3": "Risk Assessment",
    "CC4": "Monitoring Activities",
    "CC5": "Control Activities",
    "CC6": "Logical and Physical Access Controls",
    "CC7": "System Operations",
    "CC8": "Change Management",
    "CC9": "Risk Mitigation",
    "A1": "Availability",
    "PI1": "Processing Integrity",
    "C1": "Confidentiality",
    "P": "Privacy",
}

CATEGORIES = {
    "Security": {"code": "CC", "required": True,
                 "description": "Protection of information and systems against unauthorized access. The Common Criteria apply to every SOC 2 engagement."},
    "Availability": {"code": "A1", "required": False,
                     "description": "Information and systems are available for operation and use as committed or agreed."},
    "Processing Integrity": {"code": "PI1", "required": False,
                     "description": "System processing is complete, valid, accurate, timely, and authorized."},
    "Confidentiality": {"code": "C1", "required": False,
                     "description": "Information designated as confidential is protected as committed or agreed."},
    "Privacy": {"code": "P", "required": False,
                     "description": "Personal information is collected, used, retained, disclosed, and disposed of as committed and in line with privacy objectives."},
}

# (id, category, series, title, summary, evidence list, priority)
CRITERIA = [
# ---------------- CC1 Control Environment ----------------
("CC1.1", "Security", "CC1", "Integrity and ethical values",
 "Leadership sets the tone: the company defines and demonstrates integrity and ethical values, and holds people to them.",
 ["Signed code of conduct", "Ethics policy acknowledgment records", "Board minutes showing values discussion"], "high"),
("CC1.2", "Security", "CC1", "Independent board oversight",
 "Whoever governs the company (board, owners, advisors) oversees controls independently from day-to-day management.",
 ["Board charter or operating agreement", "Meeting minutes showing oversight of security", "Org chart showing reporting lines"], "high"),
("CC1.3", "Security", "CC1", "Structure, reporting lines, and responsibilities",
 "The org chart is real: structures, reporting lines, and who owns which controls are defined, assigned, and kept current.",
 ["Current org chart", "RACI or responsibility matrix", "Job descriptions with security duties"], "high"),
("CC1.4", "Security", "CC1", "Commitment to competence",
 "The company hires, trains, and retains people competent for their control responsibilities, including security training.",
 ["Hiring criteria for technical roles", "Security awareness training completion records", "Performance review templates"], "high"),
("CC1.5", "Security", "CC1", "Accountability for controls",
 "People are held accountable for their control responsibilities, with consequences when controls fail.",
 ["Accountability language in role descriptions", "Disciplinary policy", "Management review records"], "high"),
# ---------------- CC2 Communication and Information ----------------
("CC2.1", "Security", "CC2", "Internal communication of control responsibilities",
 "Control objectives and responsibilities are communicated internally so everyone knows what is expected of them.",
 ["All-hands or onboarding decks covering security", "Internal wiki or policy portal", "Acknowledgment logs"], "high"),
("CC2.2", "Security", "CC2", "External communication with customers and partners",
 "The company communicates system operation, commitments, and relevant control info to customers and business partners.",
 ["Status page and incident communications", "Customer-facing security documentation", "M SA or DPA security exhibits"], "high"),
("CC2.3", "Security", "CC2", "Communication with regulators and authorities",
 "The company knows which regulators and authorities matter and communicates with them as required, including breach notification duties.",
 ["Breach notification procedure", "Regulatory contact list", "Records of past notifications, if any"], "high"),
# ---------------- CC3 Risk Assessment ----------------
("CC3.1", "Security", "CC3", "Defined objectives for risk identification",
 "Objectives are specific enough that risks to meeting them can actually be identified.",
 ["Documented security objectives", "Risk assessment scope statement"], "high"),
("CC3.2", "Security", "CC3", "Risk identification and analysis",
 "The company identifies and analyzes risks to achieving its objectives, and decides how to manage them.",
 ["Risk register", "Risk assessment report", "Risk treatment decisions"], "high"),
("CC3.3", "Security", "CC3", "Fraud risk assessment",
 "Fraud gets its own look: incentives, pressures, and opportunities for fraud are assessed explicitly.",
 ["Fraud risk assessment section", "Segregation of duties analysis", "Whistleblower or reporting channel"], "high"),
("CC3.4", "Security", "CC3", "Assessment of significant changes",
 "Big changes (new product, new vendor, new infrastructure, leadership change) trigger a fresh risk look.",
 ["Change-triggered risk review records", "New vendor onboarding risk review"], "high"),
# ---------------- CC4 Monitoring ----------------
("CC4.1", "Security", "CC4", "Ongoing and separate control evaluations",
 "Controls are checked both continuously (monitoring) and periodically (separate evaluations like internal audits or pen tests).",
 ["Continuous monitoring dashboards", "Penetration test reports", "Internal audit or self-assessment records"], "high"),
("CC4.2", "Security", "CC4", "Evaluation and communication of deficiencies",
 "Control failures and gaps are identified, rated by severity, reported to the right people, and fixed on a timeline.",
 ["Deficiency log with severity ratings", "Remediation tracking", "Management reporting on open findings"], "high"),
# ---------------- CC5 Control Activities ----------------
("CC5.1", "Security", "CC5", "Control activities that mitigate risk",
 "Control activities are chosen and built to actually mitigate the risks identified, not just check a box.",
 ["Control matrix mapping risks to controls", "Control design documentation"], "high"),
("CC5.2", "Security", "CC5", "Technology general controls",
 "IT general controls cover the tech stack: access, changes, operations, and data backup for the systems that matter.",
 ["IT general controls policy", "Backup and restore test logs", "Job scheduling and operations procedures"], "high"),
("CC5.3", "Security", "CC5", "Policies deployed through procedures",
 "Policies are not shelfware: they are deployed through real procedures, assigned owners, and followed in practice.",
 ["Information security policy suite", "Procedure documents with owners", "Policy exception log"], "high"),
# ---------------- CC6 Logical and Physical Access ----------------
("CC6.1", "Security", "CC6", "System boundaries protected against unauthorized access",
 "The logical boundary of the system is defined and defended: firewalls, network segmentation, and edge controls keep outsiders out.",
 ["Network diagrams", "Firewall rule reviews", "VPC and segmentation documentation"], "critical"),
("CC6.2", "Security", "CC6", "Registration and authorization of new users",
 "New users, both employees and external, are registered and their access authorized before they get in.",
 ["Access request and approval tickets", "Onboarding checklist with access provisioning"], "critical"),
("CC6.3", "Security", "CC6", "Timely removal of access for departing users",
 "When people leave or change roles, their access is removed or adjusted promptly, not whenever someone remembers.",
 ["Offboarding checklist with access revocation", "Termination tickets with timestamps", "Periodic access review showing leavers removed"], "critical"),
("CC6.4", "Security", "CC6", "Physical access restrictions",
 "Physical access to facilities, data centers, and server rooms is restricted to authorized people.",
 ["Badge access logs", "Data center SOC 2 report or attestation", "Visitor logs"], "critical"),
("CC6.5", "Security", "CC6", "Protection against unauthorized asset disposal",
 "Hardware and media leaving the company are tracked and sanitized so data does not walk out the door.",
 ["Asset disposal records", "Drive destruction certificates", "Media sanitization log"], "critical"),
("CC6.6", "Security", "CC6", "Role-based logical access and least privilege",
 "Access follows roles and least privilege: people get the minimum access their job needs, enforced by the system.",
 ["Role-based access matrix", "MFA enforcement evidence", "Privileged access reviews"], "critical"),
("CC6.7", "Security", "CC6", "Controls over data transmission and portable media",
 "Data in transit is protected (encryption), and movement of data onto portable media or outside the boundary is restricted.",
 ["TLS configuration evidence", "DLP or egress control records", "Encryption-in-transit documentation"], "critical"),
("CC6.8", "Security", "CC6", "Prevention of unauthorized software",
 "Only approved software runs in the environment: unauthorized software is prevented or detected.",
 ["Approved software inventory", "Endpoint protection console reports", "Application allowlisting policy"], "critical"),
# ---------------- CC7 System Operations ----------------
("CC7.1", "Security", "CC7", "Vulnerability identification and remediation",
 "Vulnerabilities are found (scanning, threat intel) and fixed on a risk-based timeline.",
 ["Vulnerability scan reports", "Patch records with timelines", "Threat intel subscription or feed"], "critical"),
("CC7.2", "Security", "CC7", "Monitoring of system components",
 "Infrastructure and software are monitored for anomalies: uptime, performance, and security signals.",
 ["SIEM or monitoring dashboards", "Alerting rules and alert history", "Log retention configuration"], "critical"),
("CC7.3", "Security", "CC7", "Security event triage and evaluation",
 "Anomalies get triaged: the company evaluates whether something is a real security event and how bad it is.",
 ["Triage procedures", "Event tickets with severity classification", "Escalation records"], "critical"),
("CC7.4", "Security", "CC7", "Incident response",
 "When a security event becomes an incident, the response plan kicks in: contain, eradicate, recover, learn.",
 ["Incident response plan", "Tabletop exercise records", "Past incident reports with lessons learned"], "critical"),
("CC7.5", "Security", "CC7", "Corrective actions from monitoring",
 "Monitoring findings turn into fixes: corrective actions are identified, tracked, and verified.",
 ["Corrective action log", "Verification of fix effectiveness"], "critical"),
# ---------------- CC8 Change Management ----------------
("CC8.1", "Security", "CC8", "Controlled change management process",
 "Changes to infrastructure, software, and procedures go through a controlled process: request, test, approve, implement, review.",
 ["Change tickets with approvals", "Deployment pipeline with gates", "Emergency change records"], "critical"),
# ---------------- CC9 Risk Mitigation ----------------
("CC9.1", "Security", "CC9", "Business disruption risk mitigation",
 "Risks of business disruption are identified and mitigated: continuity and disaster recovery are planned, not improvised.",
 ["Business continuity plan", "Disaster recovery plan", "BIAs for critical processes"], "high"),
("CC9.2", "Security", "CC9", "Vendor and business partner risk management",
 "Vendors and partners with access to the system are risk-assessed, contracted with security commitments, and monitored.",
 ["Vendor risk assessments", "Vendor list with criticality ratings", "Vendor SOC 2 reports on file"], "critical"),
# ---------------- A1 Availability ----------------
("A1.1", "Availability", "A1", "Capacity planning and monitoring",
 "Capacity is planned and monitored so the system stays available under expected and peak demand.",
 ["Capacity plans and forecasts", "Utilization monitoring and alerts", "Load test results"], "high"),
("A1.2", "Availability", "A1", "Backup and recovery procedures",
 "Backup and recovery procedures exist and are operated so the system can be restored after a failure.",
 ["Backup procedures and schedules", "Backup success logs", "Recovery runbooks"], "high"),
("A1.3", "Availability", "A1", "Recovery plan testing",
 "Recovery plans are actually tested, not just written: tests prove restore works within committed timeframes.",
 ["Disaster recovery test plans and results", "RTO and RPO measurements"], "high"),
# ---------------- PI1 Processing Integrity ----------------
("PI1.1", "Processing Integrity", "PI1", "Quality information for processing objectives",
 "The company defines what good data looks like: data definitions, product specs, and quality requirements for processing.",
 ["Data dictionaries", "Product and service specifications"], "high"),
("PI1.2", "Processing Integrity", "PI1", "Controls over system inputs",
 "Inputs are checked for completeness and accuracy before processing: bad data gets caught at the door.",
 ["Input validation rules", "Error and rejection logs", "Reconciliation procedures"], "high"),
("PI1.3", "Processing Integrity", "PI1", "Controls over system processing",
 "Processing itself is controlled: authorized, complete, accurate, and timely, with errors detected and corrected.",
 ["Processing controls documentation", "Error detection and correction logs", "Batch and transaction controls"], "high"),
("PI1.4", "Processing Integrity", "PI1", "Controls over system outputs",
 "Outputs are complete, accurate, timely, protected, and delivered only to intended parties.",
 ["Output distribution controls", "Output accuracy checks", "Delivery logs"], "high"),
("PI1.5", "Processing Integrity", "PI1", "Controls over stored data",
 "Data at rest, inputs in queue, and outputs awaiting delivery are stored completely, accurately, and protected.",
 ["Data storage procedures", "Archive and retention controls", "Storage integrity checks"], "high"),
# ---------------- C1 Confidentiality ----------------
("C1.1", "Confidentiality", "C1", "Identification and protection of confidential information",
 "Confidential information is identified when received or created, marked, and protected for its retention period.",
 ["Data classification policy", "Confidential data inventory", "Handling procedures"], "high"),
("C1.2", "Confidentiality", "C1", "Disposal of confidential information",
 "When retention ends, confidential information is destroyed in a way that prevents recovery.",
 ["Disposal procedures", "Destruction certificates or logs"], "high"),
# ---------------- P Privacy ----------------
("P1.1", "Privacy", "P", "Privacy notice to data subjects",
 "People are told what you collect, why, and what their rights are, in clear language, before or when you collect it.",
 ["Published privacy notice", "Notice version history", "Evidence of notice delivery"], "high"),
("P2.1", "Privacy", "P", "Choice and consent communication",
 "Data subjects are told their choices about collection, use, and disclosure, and consent is obtained where required.",
 ["Consent records", "Opt-in and opt-out mechanisms", "Consent for new purposes"], "high"),
("P3.1", "Privacy", "P", "Collection limited to stated objectives",
 "Collection is limited to personal information needed for the stated privacy objectives, gathered fairly and lawfully.",
 ["Data minimization review", "Collection method documentation"], "high"),
("P3.2", "Privacy", "P", "Explicit consent before collecting sensitive information",
 "For sensitive personal information, explicit consent is communicated, obtained, and documented before collection.",
 ["Sensitive data consent records", "Consent documentation retention"], "high"),
("P4.1", "Privacy", "P", "Use limited to identified purposes",
 "Personal information is used only for the purposes it was collected for, unless law requires otherwise.",
 ["Purpose limitation review", "New-use approval records"], "high"),
("P4.2", "Privacy", "P", "Retention consistent with objectives",
 "Personal information is kept no longer than needed for the stated purposes, and protected while retained.",
 ["Retention schedule", "Retention enforcement evidence"], "high"),
("P4.3", "Privacy", "P", "Secure disposal of personal information",
 "When personal information is no longer needed, it is anonymized, disposed of, or destroyed so it cannot be recovered.",
 ["Disposal procedures", "Deletion request log", "Destruction verification"], "high"),
("P5.1", "Privacy", "P", "Data subject access to personal information",
 "Identified and authenticated individuals can see what personal information you hold about them and get a copy.",
 ["Access request log", "Identity verification procedure", "Response records"], "high"),
("P5.2", "Privacy", "P", "Correction of personal information on request",
 "People can correct their personal information, corrections flow to third parties who got the bad data, and denials are explained.",
 ["Correction request log", "Third-party correction notices", "Denial communications"], "high"),
("P6.1", "Privacy", "P", "Third-party disclosure only with consent",
 "Personal information goes to third parties only with consent, for the purposes collected, and only to parties with proper agreements.",
 ["Third-party disclosure log", "Data processing agreements", "Consent records for disclosures"], "high"),
("P6.2", "Privacy", "P", "Records of authorized disclosures",
 "A complete, accurate, timely record exists of every authorized disclosure of personal information.",
 ["Disclosure register", "Reconciliation of disclosures"], "high"),
("P6.3", "Privacy", "P", "Records of unauthorized disclosures and breaches",
 "Detected or reported unauthorized disclosures, including breaches, are recorded completely, accurately, and promptly.",
 ["Breach register", "Detection and reporting records"], "high"),
("P6.4", "Privacy", "P", "Vendor privacy commitments and compliance checks",
 "Vendors with access to personal information sign privacy commitments, and their compliance is checked periodically with corrective action when needed.",
 ["Vendor privacy addenda", "Vendor compliance assessments", "Corrective action records"], "high"),
("P6.5", "Privacy", "P", "Vendor breach notification commitments",
 "Vendors commit to notify you of actual or suspected unauthorized disclosures, and those notifications reach the right people fast.",
 ["Vendor notification clauses", "Notification handling records"], "high"),
("P6.6", "Privacy", "P", "Breach notification to data subjects and regulators",
 "Breaches and incidents are notified to affected people, regulators, and others as required, through an established process.",
 ["Breach notification procedure", "Notification records and timelines"], "high"),
("P6.7", "Privacy", "P", "Accounting of disclosures on request",
 "On request, data subjects get an accounting of the personal information held about them and who it was disclosed to.",
 ["Accounting request log", "Response records"], "high"),
("P7.1", "Privacy", "P", "Accuracy and completeness of personal information",
 "Personal information collected and kept is accurate, up to date, complete, and relevant for its purpose.",
 ["Data quality checks", "Accuracy review records"], "high"),
("P8.1", "Privacy", "P", "Privacy inquiry and complaint handling",
 "There is a real process for privacy questions, complaints, and disputes: intake, resolution, communication, and monitoring for repeat issues.",
 ["Complaint log with resolutions", "Contact channel published in notice", "Compliance monitoring records"], "high"),
]

def build():
    criteria = []
    for cid, cat, series, title, summary, evidence, priority in CRITERIA:
        criteria.append({
            "id": cid,
            "category": cat,
            "series": series,
            "series_name": SERIES[series],
            "title": title,
            "summary": summary,
            "typical_evidence": evidence,
            "priority": priority,
        })
    dataset = {
        "framework": "AICPA Trust Services Criteria",
        "edition": "2017 Trust Services Criteria (TSP Section 100), with 2022 revised points of focus",
        "total_criteria": len(criteria),
        "categories": CATEGORIES,
        "series": SERIES,
        "notes": [
            "Security (Common Criteria) is mandatory for every SOC 2 engagement.",
            "Availability, Processing Integrity, Confidentiality, and Privacy are included only when the entity commits to them in the engagement scope.",
            "Type I reports assess control design at a point in time; Type II reports assess operating effectiveness over a period, typically 3 to 12 months.",
            "Summaries and evidence suggestions are original plain-English guidance, not AICPA text. This dataset is a readiness aid, not an audit opinion.",
        ],
        "criteria": criteria,
    }
    with open(os.path.join(DATA, "tsc.json"), "w") as f:
        json.dump(dataset, f, indent=2)
    with open(os.path.join(DATA, "tsc.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "category", "series", "series_name", "title", "summary", "typical_evidence", "priority"])
        for c in criteria:
            w.writerow([c["id"], c["category"], c["series"], c["series_name"], c["title"], c["summary"], "; ".join(c["typical_evidence"]), c["priority"]])
    # counts
    from collections import Counter
    print("total:", len(criteria))
    print("by category:", dict(Counter(c["category"] for c in criteria)))
    print("by series:", dict(Counter(c["series"] for c in criteria)))
    print("by priority:", dict(Counter(c["priority"] for c in criteria)))

if __name__ == "__main__":
    build()
