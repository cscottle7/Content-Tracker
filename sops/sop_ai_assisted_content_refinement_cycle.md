# SOP: AI-Assisted Content Refinement Cycle

| | |
|---|---|
| **Document ID:** | DWS-SOP-CONTENT-001 |
| **Version:** | 1.0 |
| **Status:** | Final |
| **Author:** | Doc Architect |
| **Date of Issue:** | 05 August 2025 |
| **Applies To:** | `@content_refiner` AI Agent |

---

### 1.0 Purpose

To establish a formal, systematic procedure for the `@content_refiner` AI agent to follow when revising a content draft. The goal of this SOP is to ensure that all revisions, based on a structured audit report, are implemented accurately, coherently, and verifiably.

### 2.0 Scope

This SOP governs the entire operational workflow of the `@content_refiner` agent. Adherence is mandatory for all tasks involving the revision of a content draft based on an audit report supplied by a human editor or the `@content_reviewer` agent.

### 3.0 Definitions

* **Audit Report:** A structured document detailing required revisions for a content draft. It must contain a section titled "Consolidated Actionable Revisions".
* **Content Draft:** The original text document that is the subject of the revision cycle.
* **Internal Checklist:** An ordered, internal list of tasks created by the agent by parsing the Audit Report. This serves as the agent's work plan.
* **Revised Draft:** The final output document after the agent has applied all required edits and performed all verification steps.

### 4.0 Procedure

The agent must execute the following four steps in strict sequential order.

#### 4.1 Step 1: Ingestion and Checklist Formulation

1.  **Ingest Inputs:** Receive the source **Content Draft** and the accompanying **Audit Report**.
2.  **Parse Revisions:** Locate and parse the "Consolidated Actionable Revisions" section within the Audit Report.
3.  **Create Checklist:** Transform each actionable point from the list into a sequential **Internal Checklist**.
4.  **Confirm Understanding:** Output a confirmation message stating that the checklist has been created and the revision process is beginning.

#### 4.2 Step 2: Systematic Edit Implementation

1.  **Address Sequentially:** Begin with the first item on the **Internal Checklist**.
2.  **Apply Edit:** Apply the single, specified revision directly to the **Content Draft**.
3.  **Mark as Complete:** Once the edit is applied, mark the corresponding checklist item as complete.
4.  **Iterate:** Proceed to the next item on the checklist and repeat this process until all items have been marked as complete.

#### 4.3 Step 3: Holistic Coherence Review

1.  **Initiate Review:** After implementing the final edit from the checklist, initiate a full, end-to-end read-through of the entire **Revised Draft**.
2.  **Analyse Flow and Consistency:** The primary goal of this review is to evaluate the document for:
    * Narrative and logical flow.
    * Stylistic and tonal consistency.
    * Grammatical correctness and readability.
3.  **Self-Correct:** Identify and correct any awkward phrasing, logical discontinuities, or stylistic clashes that may have been introduced by the individual edits.

#### 4.4 Step 4: Final Verification and Output

1.  **Perform Final Check:** Conduct a final verification by comparing the **Revised Draft** against the original **Internal Checklist**.
2.  **Verify All Points:** For each item on the checklist, confirm that the required revision was implemented successfully and remains present in the final text. This is a critical self-critique step to ensure 100% compliance with the audit.
3.  **Finalise Output:** Once every checklist item is verified as successfully addressed, the procedure is complete. The final, verified **Revised Draft** is now ready for output.

### 5.0 Output Requirements

* The sole output of this procedure is the final, fully-vetted **Revised Draft**.
* The agent must present this draft along with a concluding statement confirming that all required revisions from the audit report have been implemented and verified.