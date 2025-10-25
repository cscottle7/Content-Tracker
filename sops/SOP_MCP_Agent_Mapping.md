# SOP: MCP Agent Mapping & Tooling Strategy

## 1.0 Purpose
This document defines the official mapping of specialist AI sub-agents to their required Model Context Protocol (MCP) tools. It also establishes the security and governance framework for using the MCP ecosystem. The guiding principles are **Security by Design** and the **Principle of Least Privilege**.

## 2.0 The Two-Tiered Tooling Strategy
Our agentic model is divided into a high-level "Conductor" and low-level "Specialists." Their toolsets MUST remain distinct to ensure a clear separation of concerns.

* **Conductor AI (`workflow_orchestrator`):** This agent operates at a high level of abstraction. It MUST only be equipped with MCPs that interact with project-level, cloud-based APIs.
* **Specialist AIs (`dev_implement`, `test_generate`, etc.):** These agents operate at the implementation level. They MUST only be equipped with MCPs that interact with the local development environment.

## 3.0 Agent-to-MCP Tool Mappings
The Orchestrator AI is responsible for enforcing these permissions.

| Agent (Sub-Agent) | Role in Workflow | Required MCP Tools |
| :--- | :--- | :--- |
| **`workflow_orchestrator`** | Conductor / Orchestrator | `Official GitHub MCP`, `Jira MCP`, `Slack MCP` |
| **`dev_implement`** | Core Developer | `Official Git MCP`, `Filesystem MCP` |
| **`test_generate`** | QA Engineer | `Filesystem MCP`, `Docker MCP` (for tests) |
| **`security_audit`** | Security Auditor | `Filesystem MCP`, `GitHub MCP` (read-only history) |
| **`asset_find`** | Research Assistant | `Web Search MCP`, `GitMCP` (for doc retrieval) |

## 4.0 Security Gateway Mandate
The MCP standard explicitly delegates security responsibility to the implementer. Therefore, the **`workflow_orchestrator` MUST function as a security gateway.**
* It is responsible for managing all OAuth 2.1 with PKCE authentication flows for remote MCP servers.
* It MUST enforce explicit, granular user consent for every action that modifies state.
* It is responsible for sanitizing all data passed between agents and tools.

## 5.0 "Trust but Verify" Vetting Protocol
The MCP ecosystem contains a mix of official and community-driven servers of varying quality. A data exposure incident has been documented with a community server.
* **Mandate:** Before any new community-driven MCP server is integrated, it MUST undergo a formal security audit.
* **Procedure:** The audit will be performed by the `security_audit` agent using the **"SOP: Automated MCP Auditing Protocol"** as its knowledge base. A "Low Risk" score is required for approval.
* **Preference:** Official servers from tool vendors (e.g., Atlassian, GitHub) are strongly preferred.

## 6.0 The Composite MCP Roadmap
To improve robustness and efficiency, our development roadmap will prioritize creating **Composite MCPs**. These are high-level tools that encapsulate complex, multi-step workflows into a single, reliable command.
* **Example Candidate:** `create_pr_from_staged_changes`
* **Internal Workflow:**
    1.  Call the `Official Git MCP` to `git_add`.
    2.  Call the `Official Git MCP` to `git_commit`.
    3.  Call the `Official Git MCP` to `git_push`.
    4.  Call the `Official GitHub MCP` to `create_pull_request`.