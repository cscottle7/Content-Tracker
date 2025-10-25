# SOP: Client File Organization Standards

| Document ID: | DWS-SOP-FILEORG-001 |
| :--- | :--- |
| **Version:** | 1.0 |
| **Status:** | Final |
| **Approved By:** | Craig Cottle |
| **Date of Issue:** | 04-Sep-2025 |
| **Next Review Date:** | 04-Mar-2026 |

---

## 1.0 Purpose

This Standard Operating Procedure (SOP) establishes mandatory file organization standards ensuring all agents maintain consistent, professional, and scalable folder structures for client projects. With proper file organization reducing project delivery times by up to 50% and improving team collaboration efficiency by 75%, this SOP implements research-backed organizational frameworks that ensure zero files are created outside designated client directories whilst maintaining seamless project navigation and handover capabilities.

## 2.0 Scope

This SOP applies to all AI agents, human reviewers, and project personnel working within the Bigger Boss Agent System, including:
- All `SiteSpect`, `ContentForge`, and `StrategyNexus` squad outputs
- Project initialization, file creation, and document management activities
- Client deliverable organization and archival processes
- Cross-project file sharing and reference management
- Template standardization and folder structure maintenance

## 3.0 Definitions

* **Client Folder Structure:** The mandatory hierarchical organization system for all client-related files within the `clients/` directory
* **Domain-Based Naming:** File naming convention using client domain format (e.g., `clientname_com_au`)
* **Subfolder Standardization:** Consistent use of strategy/, research/, content/, technical/, and implementation/ directories
* **Project Navigation Hub:** The README.md file serving as the central navigation point for all project documentation
* **File Provenance:** Complete tracking of file origin, creation, and modification history
* **Cross-Project References:** Links between related files across different client folders

## 4.0 Procedures

### 4.1 Procedure: Mandatory Client Folder Creation Protocol

All client work must begin with proper folder structure establishment.

#### **Step 1: Client Folder Initialization**
**MANDATORY:** All client files MUST be created within the designated client folder structure.

1. **Primary Folder Creation:**
   - Navigate to `clients/` directory in project root
   - Create client folder using exact format: `{client_domain_name}/`
   - Examples: `sydneycoachcharter_com_au/`, `precisionuppergisurgery_com_au/`
   - **NEVER** create files in root directory or random locations
   - **NEVER** use spaces, special characters, or capital letters in folder names

2. **Subfolder Structure Implementation:**
   - Create ALL required subfolders during initialization:
     ```
     clients/{client_domain_name}/
     ├── README.md                    # Project navigation hub (MANDATORY)
     ├── PROJECT_OVERVIEW.md          # Executive summary (MANDATORY)
     ├── strategy/                    # Strategic planning documents
     ├── research/                    # Market intelligence & analysis
     ├── content/                     # Content strategy & guidelines
     ├── technical/                   # Technical audits & recommendations
     ├── implementation/              # Execution tracking
     └── assets/                      # Supporting materials (optional)
     ```

3. **Folder Structure Validation:**
   - Verify all mandatory folders exist before creating first document
   - Confirm folder naming follows exact specification above
   - Test folder accessibility and write permissions
   - Document folder creation timestamp and responsible agent

#### **Step 2: README.md Project Navigation Hub Creation**
**MANDATORY:** Every client folder MUST contain a comprehensive README.md file.

1. **Navigation Hub Requirements:**
   - Include complete project overview and objectives
   - List all major deliverables with file locations
   - Provide status updates for ongoing work
   - Include team member responsibilities and contacts
   - Link to all major documents with brief descriptions

2. **README.md Structure Standard:**
   ```markdown
   # {Client Name} - Project Overview
   
   ## Project Status
   - **Start Date:** DD/MM/YYYY
   - **Current Phase:** [Discovery/Strategy/Implementation/Complete]
   - **Last Updated:** DD/MM/YYYY
   - **Primary Contact:** [Name]
   
   ## Project Objectives
   [Brief description of project goals]
   
   ## Folder Navigation
   ### 📁 /strategy/
   - [research_brief.md](strategy/research_brief.md) - Project foundation
   - [implementation_plan.md](strategy/implementation_plan.md) - Execution roadmap
   
   ### 📁 /research/
   - [competitive_analysis.md](research/competitive_analysis.md) - Market intelligence
   - [audience_personas.md](research/audience_personas.md) - Target audience
   
   ### 📁 /content/
   - [content_strategy.md](content/content_strategy.md) - Content planning
   - [audience_style_guide.md](content/audience_style_guide.md) - Brand standards
   
   ### 📁 /technical/
   - [technical_audit.md](technical/technical_audit.md) - Technical analysis
   - [ai_optimization_guide.md](technical/ai_optimization_guide.md) - AI integration
   
   ### 📁 /implementation/
   - [execution_tracking_report.md](implementation/execution_tracking_report.md) - Progress tracking
   ```

### 4.2 Procedure: File Naming and Location Standards

Establish consistent naming conventions and location rules for all client files.

#### **Step 1: File Naming Convention Implementation**
**Apply consistent naming across all client documents:**

1. **Primary Document Naming:**
   - Format: `{CLIENT_PREFIX}_{document_type}.md`
   - Examples: `SYDNEYCOACHCHARTER_competitive_analysis.md`
   - Use ALL CAPS for client prefix (domain without extensions)
   - Use lowercase with underscores for document type
   - Replace dots and hyphens in domain with underscores

2. **Subfolder Document Naming:**
   - When using standardized subfolders, use descriptive naming:
   - Examples: `competitive_analysis.md`, `audience_personas.md`
   - Maintain consistency with template structure
   - Avoid redundant client prefixes in subfolder documents

3. **Special Document Types:**
   - Progress tracking: `execution_tracking_report.md`
   - Project checklists: `PROJECT_CHECKLIST.md`
   - Overview documents: `PROJECT_OVERVIEW.md`
   - Raw data files: Store in `raw_data/` subfolder when needed

#### **Step 2: Mandatory File Location Rules**
**Enforce strict location requirements for all document types:**

1. **Strategic Documents Location:**
   - **MUST** be placed in `clients/{domain}/strategy/` folder
   - Include: research briefs, implementation plans, positioning strategy
   - Link from main README.md with clear descriptions
   - Maintain consistent cross-references between strategic documents

2. **Research Documents Location:**
   - **MUST** be placed in `clients/{domain}/research/` folder
   - Include: competitive analysis, audience personas, keyword research
   - Ensure research supports strategic recommendations
   - Maintain data provenance and source attribution

3. **Content Documents Location:**
   - **MUST** be placed in `clients/{domain}/content/` folder
   - Include: content strategy, style guides, content plans
   - Link content recommendations to audience research
   - Maintain brand consistency across all content documents

4. **Technical Documents Location:**
   - **MUST** be placed in `clients/{domain}/technical/` folder
   - Include: technical audits, SEO recommendations, AI optimization
   - Ensure technical recommendations align with strategic objectives
   - Maintain technical accuracy and source verification

5. **Implementation Documents Location:**
   - **MUST** be placed in `clients/{domain}/implementation/` folder
   - Include: execution tracking, milestone checklists, progress reports
   - Update regularly throughout project lifecycle
   - Maintain accountability and progress transparency

### 4.3 Procedure: Cross-Project File Management

Handle situations requiring file sharing or references across multiple clients.

#### **Step 1: Reference Documentation Protocol**
**When referencing files from other client projects:**

1. **Permitted Cross-References:**
   - Industry benchmark data (anonymized)
   - Template frameworks and methodologies
   - Best practice examples (client-anonymized)
   - Technical standards and procedures

2. **Cross-Reference Implementation:**
   - Create copies of relevant documents in current client folder
   - Remove all client-specific information and branding
   - Add clear attribution noting source methodology
   - Update references to reflect current client context

3. **Prohibited Cross-References:**
   - Direct links to other client folders
   - Client-specific data or strategies
   - Confidential analysis or recommendations
   - Proprietary research or competitive intelligence

#### **Step 2: Template and Asset Management**
**Maintain reusable templates while preserving client confidentiality:**

1. **Template Storage:**
   - Store generic templates in `clients/CLIENT_FOLDER_TEMPLATE/`
   - Maintain template versions separate from client work
   - Update templates based on successful client implementations
   - Document template changes and version history

2. **Asset Sharing Protocol:**
   - Copy reusable assets to current client folder
   - Customize all assets for current client branding
   - Remove any references to previous client work
   - Maintain asset quality and professional standards

### 4.4 Procedure: Folder Structure Compliance Monitoring

Implement systematic monitoring to ensure ongoing compliance with organization standards.

#### **Step 1: Automated Compliance Checking**
**Regular verification of folder structure adherence:**

1. **Structure Validation Checks:**
   - Daily automated scans for files in incorrect locations
   - Verification that all client folders contain mandatory README.md
   - Confirmation of proper subfolder structure implementation
   - Detection of naming convention violations

2. **Non-Compliance Detection:**
   - Generate automated alerts for files in root directory
   - Flag folders missing mandatory subfolders
   - Identify files with incorrect naming conventions
   - Report missing or incomplete README.md files

3. **Compliance Correction Protocol:**
   - Immediate notification to responsible agent for corrections
   - 24-hour maximum timeline for compliance corrections
   - Escalation to project manager for repeated violations
   - Documentation of corrections made and prevention measures

#### **Step 2: Quality Assurance Review Process**
**Human verification of automated compliance monitoring:**

1. **Weekly Structure Audits:**
   - Manual review of all new client folder creations
   - Verification of README.md completeness and accuracy
   - Confirmation of proper file organization within subfolders
   - Assessment of cross-project reference appropriateness

2. **Monthly Comprehensive Review:**
   - Complete audit of all active client folder structures
   - Review of folder naming consistency across all projects
   - Assessment of template updates and implementation
   - Documentation of organizational improvements needed

3. **Quarterly Standards Update:**
   - Review and update folder structure template as needed
   - Incorporate lessons learned from project implementations
   - Update this SOP based on operational feedback
   - Train all agents on any structural changes

### 4.5 Procedure: Project Lifecycle File Management

Maintain organization throughout project phases from initiation to completion.

#### **Step 1: Project Phase Organization**
**Adapt file organization as projects evolve:**

1. **Discovery Phase Organization:**
   - Focus on `/strategy/` and `/research/` folder development
   - Maintain regular README.md updates with discovery progress
   - Document all initial research and analysis findings
   - Establish foundation for subsequent project phases

2. **Implementation Phase Organization:**
   - Shift focus to `/implementation/` folder for progress tracking
   - Maintain `/content/` and `/technical/` folders for deliverables
   - Archive completed discovery materials appropriately
   - Update README.md to reflect current project status

3. **Completion Phase Organization:**
   - Create final deliverable summaries in each subfolder
   - Consolidate all project learnings and recommendations
   - Prepare comprehensive project handover documentation
   - Archive all working materials while preserving accessibility

#### **Step 2: Archive and Maintenance Protocols**
**Ensure long-term organization and accessibility:**

1. **Active Project Maintenance:**
   - Weekly cleanup of duplicate or outdated files
   - Regular README.md updates reflecting current project status
   - Maintenance of consistent file naming across all documents
   - Verification of cross-references and link accuracy

2. **Project Completion Archive:**
   - Create comprehensive final project summary
   - Archive all development materials in organized structure
   - Maintain client folder structure for future reference
   - Document project completion and handover details

3. **Long-term Storage Management:**
   - Preserve all client folders in original structure
   - Maintain README.md files for future project reference
   - Regular backup verification and data integrity checks
   - Periodic review of archived projects for template improvements

## 5.0 Integration Points

### 5.1 CLAUDE.md Configuration Alignment
Directly implements and expands upon CLAUDE.md file organization requirements:
- Enforces mandatory `clients/{client_domain}/` folder structure
- Implements standardized subfolder organization exactly as specified
- Requires README.md creation as project navigation hub
- Maintains consistent file naming conventions throughout

### 5.2 Quality Control Integration
Aligns with DWS-SOP-QUALITY-001 for systematic quality assurance:
- Implements automated compliance monitoring for file organization
- Establishes quality gates for folder structure verification
- Requires documentation of all organizational decisions and changes
- Integrates with existing anti-hallucination protocols for data integrity

### 5.3 Content Production Workflow Integration
Connects with content production SOPs for seamless workflow:
- Provides organized foundation for all content creation activities
- Ensures content files are properly categorized and accessible
- Maintains consistency between file organization and content standards
- Facilitates efficient content review and approval processes

## 6.0 Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| **All AI Agents** | Create files only in designated client folders following exact structure requirements |
| **Project Initiators** | Establish proper client folder structure before beginning any client work |
| **Content Creators** | Place all content files in appropriate subfolders with correct naming conventions |
| **Quality Reviewers** | Verify file organization compliance during all document reviews |
| **Project Managers** | Monitor overall folder structure compliance and coordinate corrections |
| **System Administrators** | Maintain automated compliance monitoring and template updates |

## 7.0 Success Criteria

### 7.1 Organizational Compliance Targets
- **100% client folder compliance:** All client files must exist within designated client folders
- **Zero root directory files:** No client-related files permitted outside client folder structure
- **100% README.md coverage:** Every client folder must contain comprehensive navigation hub
- **95% naming convention compliance:** All files must follow established naming standards

### 7.2 Operational Efficiency Standards
- **50% reduction in file location time:** Standardized structure enables rapid document access
- **24-hour maximum correction time:** Non-compliance issues resolved within one business day
- **100% template utilization:** All new client projects must use standardized folder template
- **Zero cross-project confidentiality breaches:** Maintain complete client data separation

## 8.0 Risk Management

### 8.1 Critical Risks and Mitigation Strategies
| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|-------------------|
| **Files Created Outside Client Folders** | High | Medium | Automated monitoring with immediate alerts |
| **Inconsistent Folder Structure** | Medium | High | Mandatory template usage and regular audits |
| **Cross-Project Data Leakage** | High | Low | Strict cross-reference protocols and anonymization |
| **README.md Maintenance Failures** | Medium | Medium | Automated checks and manual review requirements |

### 8.2 Continuous Improvement Protocol
- Weekly monitoring of compliance rates and correction requirements
- Monthly review of folder structure effectiveness and user feedback
- Quarterly template updates based on operational learnings
- Annual comprehensive review of organizational standards and industry best practices

---

**Document Control:**
- This SOP supersedes all previous file organization procedures
- Changes require approval from Project Management and Quality Assurance leads
- All agents must acknowledge understanding of folder structure requirements
- Compliance monitoring is mandatory and subject to regular audit