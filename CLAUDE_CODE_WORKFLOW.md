# **Claude Code Workflow (v2.0)**

This document serves as the master operational guide for the AI-Native Development Workflow. It outlines the available specialist agents, the standard operational doctrines, and field manuals for advanced use cases.

---

### **Part 1: High-Level Sub-Agent Directory**

This directory details the core specialist agents available to the Director.

**1\. `@brief_creator` (The DevPilot)**

* **Description:** This agent acts as a project ignition specialist. It conducts a structured interview with you to gather all the strategic and technical requirements for a new project. Its goal is to produce a comprehensive `CLAUDE.md` file, which serves as the project's master plan or "constitution".  
* **When to Use It:** At the very beginning of a new project, before any other planning has occurred.  
* **Example Prompt:** `@brief_creator I need to start a new project to build a personal blog website.`

**2\. `@context_assembler` (The Tech Librarian)**

* **Description:** An automated research agent that gathers technical context. It analyses the `CLAUDE.md` file to identify the project's technology stack and then fetches the latest official documentation for each technology to produce a `PROJECT_CONTEXT.md` file.  
* **When to Use It:** After the `CLAUDE.md` file is complete, to provide the subsequent agents with up-to-date technical information.  
* **Example Prompt:** `@context_assembler Please analyse the attached @CLAUDE.md file and assemble the project context.`

**3\. `@plan_synthesizer` (The Chief Software Architect) v2.0**

* **Description:** The core of the planning phase. This agent ingests the `CLAUDE.md`, parses its "Strategic Constraint Tags", and dynamically assembles a bespoke "Cognitive Squad" of three specialist agents from the `@PERSONA_LIBRARY.md`. It orchestrates their debate and synthesizes their conflicting advice into an optimal `task_deps.md` development plan, complete with an "Architect's Rationale".  
* **When to Use It:** After the project brief and context are finalised. This agent replaces the legacy `@plan_creator`.  
* **Example Prompt:** `@plan_synthesizer Using the attached @CLAUDE.md and @PROJECT_CONTEXT.md, generate the optimal development plan.`

**4\. `@workflow_orchestrator` (The Autonomous Conductor)**

* **Description:** The primary execution engine. It takes a completed and human-approved `task_deps.md` file and executes the tasks autonomously, managing dependencies and ensuring the project is completed according to the plan.  
* **When to Use It:** For the autonomous execution of a fully planned project.  
* **Example Prompt:** `@workflow_orchestrator Execute the attached @task_deps.md development plan.`

**5\. `@squad_coordinator` (The Investigation Lead)**

* **Description:** An orchestration agent designed for ambiguous, non-linear problems. It manages a "Cognitive Squad" of specialist analyst agents, tasking them to conduct parallel investigations. It then synthesizes their disparate findings into a single, comprehensive report for human review and decision-making.  
* **When to Use It:** When faced with an analytical challenge that requires investigation rather than implementation, such as debugging, UX analysis, or security auditing.  
* **Example Prompt:** `@squad_coordinator Assemble the 'Bug Hunter Squad' to investigate the attached bug report and system logs.`

**6\. `@quality_assessor` (The QA Analyst)**

* **Description:** An objective code analysis agent. It performs a quantitative analysis of a codebase based on the definitions in `METRICS.md` and generates a "Quality Scorecard" used for benchmarking and ensuring code quality.  
* **When to Use It:** After a feature is complete or as part of a benchmark protocol to measure system performance.  
* **Example Prompt:** `@quality_assessor Please analyze the codebase in the 'src' directory and generate a Quality Scorecard.`

**7\. The Developer Persona Library** *These specialist agents reside in `@PERSONA_LIBRARY.md` and are orchestrated by the `@plan_synthesizer`, not intended for direct use.*

* **Core Personas:**  
  * `@dev_pragmatist`: Optimised for speed, simplicity, and immediate delivery (YAGNI).  
  * `@dev_custodian`: Focussed on long-term maintainability and code clarity (SOLID).  
  * `@dev_innovator`: Driven by technical excellence, performance, and elegant solutions.  
* **Specialist Personas (Selected by Tags):**  
  * `@dev_security_hawk`: A security specialist who mitigates vulnerabilities (OWASP Top 10).  
  * `@dev_performance_tuner`: An optimization expert focused on speed and resource efficiency.  
  * `@dev_ux_advocate`: A front-end specialist focused on accessible and user-centric design.  
  * `@dev_data_engineer`: A data specialist for designing schemas and transformation pipelines.

**8\. Legacy Agents (Deprecated)** *These agents are preserved for benchmarking and historical reference but should not be used for new projects.*

* **`@plan_creator` (Legacy):** The original single-path planning agent. **Superseded by `@plan_synthesizer`**, which provides a more robust, multi-perspective planning process.  
* **`@dev_implement` (Legacy):** The original monolithic implementation agent. **Superseded by the dynamic squad of adversarial developer personas**, which produces higher-quality, more considered code.

---

### **Part 2: The End-to-End Workflow Doctrine**

This doctrine mandates a strict, phased approach to ensure reliability and provide critical points for human oversight.

**Phase 1: Project Ignition**

* **Agent:** `@brief_creator`  
* **Goal:** To translate a high-level idea into a comprehensive and unambiguous project constitution (`CLAUDE.md`).  
* **Outcome:** A complete `CLAUDE.md` file, reviewed and approved by the Human Director.

**Phase 2: Context Assembly**

* **Agent:** `@context_assembler`  
* **Goal:** To provide all subsequent agents with the most current technical information relevant to the project's stack.  
* **Outcome:** A `PROJECT_CONTEXT.md` file containing relevant documentation.

**Phase 3: Strategic Synthesis & Planning**

* **Agent:** `@plan_synthesizer`  
* **Goal:** To parse the "Strategic Constraint Tags" within the `CLAUDE.md` file and dynamically assemble the optimal three-agent "Cognitive Squad" from the `@PERSONA_LIBRARY.md`. The agent then orchestrates their adversarial debate to resolve conflicts, weigh trade-offs, and produce a single, coherent, and strategically-sound plan.  
* **Outcome:** A `task_deps.md` file containing a granular, step-by-step development plan, accompanied by an "Architect's Rationale" that justifies the choice of agents and the final plan.

**Phase 4: Final Review & Approval (Human-in-the-Loop)**

* **Agent:** Human Director  
* **Goal:** To conduct a final "pre-flight check" of the generated plan (`task_deps.md`), critically evaluating the "Architect's Rationale" to ensure the plan aligns with the strategic goals of the `CLAUDE.md` before authorising execution.  
* **Outcome:** Explicit human approval to proceed.

**Phase 5: Autonomous Execution**

* **Agent:** `@workflow_orchestrator`  
* **Goal:** To autonomously execute the approved `task_deps.md` plan, managing the entire development process from code generation to task completion.  
* **Outcome:** The completed software feature or project, as defined in the plan.

---

### **Part 3: The Developer's Field Manual**

This section contains blueprints and guides for advanced, non-standard operational patterns.

**Manual 1: Squad-Based Operations: A Framework for Ambiguous Problem-Solving**

* **1\. Purpose & Doctrine:** The "Plan-Then-Execute" doctrine is highly effective for well-defined features but is ill-suited for ambiguous problems like debugging, root cause analysis, or UX friction identification. For these tasks, we employ a "Cognitive Squad" model. A squad is a team of specialist agents managed by a coordinator. Their goal is not to execute a linear plan, but to perform parallel analysis from multiple perspectives and synthesize their findings into a single, comprehensive report for human review and decision-making.  
* **2\. When to Deploy a Squad:** Deploy a squad when the problem is one of investigation and analysis, not implementation.  
* **3\. Blueprint: The "UX Friction Hunter" Squad:**  
  * **Squad Composition:** Coordinator: `@squad_coordinator`, Agent 1: `@ux_analyst`, Agent 2: `@data_miner`, Agent 3: `@user_empath`.  
  * **Workflow:** The Director tasks the `@squad_coordinator` with the high-level problem. The Coordinator tasks the three specialist agents to conduct their analyses in parallel. Each specialist returns a structured report. The Coordinator synthesizes these into a single "Friction & Opportunity Analysis" document.

**Manual 2: The Pre-Flight Check Prompt** *Before initiating Phase 5 (Autonomous Execution), it is best practice for the Human Director to perform a final validation using this prompt.*

You are an Expert AI Systems Architect and Project Manager. Your task is to conduct a final, comprehensive review of a new project... Your analysis must be based on: The project constitution: `@claude.md`, The development plan: `@task_deps.md`. Perform the following steps: 1\. Validate Project Constitution. 2\. Validate Plan Coherence. 3\. Check Task Granularity. Your final output should be a single "Pre-Flight Check Report".

**Manual 3: Blueprint: The "Bug Hunter" Squad** *This squad is designed to systematically investigate bug reports, moving from vague symptoms to a precise root cause hypothesis and evidence.*

* **Squad Composition:**  
  1. **Coordinator:** `@squad_coordinator` \- Manages the workflow and synthesizes the final report.  
  2. **Agent 1:** `@symptom_analyst` \- Analyzes user reports, error messages, and logs to form a precise, testable hypothesis of the root cause.  
  3. **Agent 2:** `@code_archaeologist` \- Scans the codebase, git history, and recent pull requests to find the exact lines of code related to the hypothesis.  
  4. **Agent 3:** `@test_strategist` \- Based on the findings, proposes a strategy for writing a failing test that reliably reproduces the bug.  
* **Workflow:**  
  1. The Director tasks the `@squad_coordinator` with a bug report.  
  2. The Coordinator tasks the `@symptom_analyst` to generate a root cause hypothesis.  
  3. The Coordinator passes the hypothesis to the `@code_archaeologist` to find the evidentiary code.  
  4. The Coordinator provides all findings to the `@test_strategist` to design a reproduction case.  
  5. The Coordinator synthesizes these reports into a single "Root Cause Analysis & Verification Plan" for the Human Director.

**Manual 4: The Benchmark Protocol for Workflow A/B Testing** *This protocol provides a standardized method for using the `@quality_assessor` to objectively compare the performance of different agentic workflows.*

* **1\. Define a Standardized Test Case:**

  1. Create a self-contained development task that is representative of typical work. This task should be documented in a `CLAUDE.md` file. Example: "Implement a REST API endpoint that accepts a user ID and returns the user's profile from a mock database, including error handling for a non-existent user."  
* **2\. Execute Workflow A (Control Group):**

  1. Run the test case task using your baseline workflow. For example, use the legacy agents (`@plan_creator`, `@dev_implement`) to generate the code in a directory named `output_legacy`.  
* **3\. Execute Workflow B (Test Group):**

  1. Run the exact same test case task using the new workflow you wish to test. For example, use the `@plan_synthesizer` and the adversarial personas to generate the code in a directory named `output_persona`.  
* **4\. Generate Quality Scorecards:**

  1. Invoke the `@quality_assessor` on both output directories.  
  2. **Prompt 1:** `@quality_assessor Please analyze the codebase in the 'output_legacy' directory and generate a Quality Scorecard.`  
  3. **Prompt 2:** `@quality_assessor Please analyze the codebase in the 'output_persona' directory and generate a Quality Scorecard.`  
* **5\. Compare and Analyze:**

  1. Compare the two generated scorecards side-by-side. Use the objective data (e.g., Maintainability Index, Cyclomatic Complexity) to determine which workflow produced a higher-quality output according to the standards defined in `METRICS.md`.

### **Architect's Rationale**

**1\. Chosen Cognitive Squad:**

* `@dev_persona_1`: (Reason for selection, linked to CLAUDE.md tags)  
* `@dev_persona_2`: (Reason for selection, linked to CLAUDE.md tags)  
* `@dev_persona_3`: (Reason for selection, linked to CLAUDE.md tags)

**2\. Key Debate & Conflict Summary:**

* (A brief summary of the core architectural trade-off identified during the adversarial debate. E.g., "The primary conflict was between the Pragmatist's simple, monolithic approach for speed and the Innovator's recommendation for a more complex, scalable microservices architecture.")

**3\. Synthesized Decision & Justification:**

* (The final architectural decision and a clear justification for why it was chosen. E.g., "The synthesized plan adopts the Pragmatist's approach for the user-facing API but uses the Innovator's scalable pattern for the asynchronous data processing service, which was identified as the highest-risk component for future bottlenecks.")

---

\---

\#\#\# \*\*Template 2: Squad Analysis Report\*\*

\* \*\*Used By:\*\* \`@squad\_coordinator\`

\* \*\*Purpose:\*\* To deliver the synthesized findings of any investigative squad (e.g., "UX Friction Hunter", "Bug Hunter").

---

### **Squad Analysis Report**

**1\. Objective:**

* (A clear, one-sentence statement of the investigation's goal. E.g., "To investigate user reports of checkout page slowness and identify the root cause.")

**2\. Assembled Squad Composition:**

* `@squad_coordinator`  
* `@analyst_persona_1`: (Role in this investigation)  
* `@analyst_persona_2`: (Role in this investigation)  
* `@analyst_persona_3`: (Role in this investigation)

**3\. Synthesized Summary of Findings:**

* (A high-level summary of the most critical findings, synthesized from the reports of all squad members. E.g., "The investigation concludes that the perceived slowness is not due to backend latency, but rather a front-end issue where the 'Place Order' button remains disabled for 3-4 seconds while third-party analytics scripts load.")

**4\. Actionable Recommendations:**

* **Recommendation 1:** (A clear, actionable recommendation. E.g., "Modify the front-end to load analytics scripts asynchronously so they do not block the UI thread.")  
* **Recommendation 2:** (E.g., "Implement a loading state for the 'Place Order' button to provide immediate user feedback.")

---

\---

\#\#\# \*\*Template 3: Strategic Directive Request\*\*

\* \*\*Used By:\*\* \`@plan\_synthesizer\` or \`@squad\_coordinator\`

\* \*\*Purpose:\*\* To formally escalate a high-stakes architectural or strategic conflict to the Human Director when the agents cannot reach an optimal synthesis on their own.

---

### **\!\! STRATEGIC DIRECTIVE REQUIRED \!\!**

**Unresolved Conflict:** A high-stakes architectural conflict regarding \[Topic, e.g., Data Consistency Model\] could not be resolved. A strategic directive is required.

---

**Option A: \[Proposal Name, e.g., Strong Consistency\]**

* **Advocated By:** `@dev_custodian`  
* **Core Claim:** All services must see the same data at the same time to ensure correctness.  
* **Pros:** Guarantees data correctness; simplifies application logic.  
* **Cons:** Introduces high latency; reduces system availability during network partitions.  
* **Required Trade-off:** This approach prioritizes data integrity over system performance and availability.

---

**Option B: \[Proposal Name, e.g., Eventual Consistency\]**

* **Advocated By:** `@dev_innovator`  
* **Core Claim:** Services should operate asynchronously, allowing for temporary inconsistencies to maximize performance.  
* **Pros:** Offers high availability and low latency; scales well.  
* **Cons:** Application logic must handle stale data; increased complexity.  
* **Required Trade-off:** This approach prioritizes performance and availability over immediate data consistency.
