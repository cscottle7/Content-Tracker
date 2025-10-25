# SOP: British English Content Standards

| Document ID: | DWS-SOP-CONTENT-004 |
| :--- | :--- |
| **Version:** | 1.0 |
| **Status:** | Final |
| **Approved By:** | Craig Cottle |
| **Date of Issue:** | 26-Aug-2025 |
| **Next Review Date:** | 26-Aug-2026 |

---

## 1.0 Purpose

This Standard Operating Procedure (SOP) establishes mandatory standards for British English usage across all content outputs from the Autonomous Agentic Marketing System. It ensures consistent British spelling conventions, terminology, punctuation, grammar, and cultural context whilst providing automated validation mechanisms to maintain 100% compliance across all agent outputs, content generation workflows, and client deliverables.

## 2.0 Scope

This SOP applies to all human writers, editors, AI agents (including `@content_drafter`, `@content_reviewer`, `@sitespect_orchestrator`, and all specialist agents), automated systems, and quality assurance processes responsible for generating, reviewing, or approving written content. It governs all text outputs including:

- Website audit reports and technical documentation
- Content briefs and strategic recommendations  
- Marketing materials and client communications
- Internal documentation and operational procedures
- Email communications and correspondence
- Social media content and advertisements

## 3.0 Definitions

* **British English:** The variety of English used in the United Kingdom, characterised by specific spelling conventions, vocabulary choices, punctuation rules, and cultural references.
* **Authoritative Sources:** Recognised British English style guides including Oxford Style Manual, Cambridge Style Guide, Government Digital Service (GDS) style guide, and BBC News style guide.
* **Automated Validation:** Software-based checking mechanisms that verify compliance with British English standards without human intervention.
* **Cultural Context Compliance:** Use of terminology, references, and expressions appropriate to British business and cultural contexts.
* **Quality Gate:** A mandatory checkpoint where content must demonstrate full British English compliance before advancement to the next workflow stage.

## 4.0 Procedures

### 4.1 Procedure: British English Spelling Standards

All content must use exclusively British English spelling conventions as defined by the Oxford English Dictionary and Cambridge Dictionary.

#### **4.1.1 Core Spelling Rules**

**Mandatory British Spellings:**

* **-our endings (not -or):**
  - colour, honour, favour, behaviour, neighbour
  - flavour, labour, humour, vigour, parlour
  - **Exception:** glamor/glamour (both acceptable, prefer glamour)

* **-ise endings (not -ize):**
  - realise, organise, recognise, specialise, analyse
  - criticise, emphasise, summarise, categorise, finalise
  - **Exceptions:** capsize, prize (noun), size (always -ize)

* **-re endings (not -er):**
  - centre, theatre, metre, litre, fibre
  - calibre, sceptre, spectre, sabre, acre
  - **Exception:** meter (measuring device), liter (in scientific contexts)

* **Double 'l' in British forms:**
  - travelling, modelling, labelling, signalling
  - cancelled, marvellous, counsellor, jewellery
  - skilful, wilful, instalment, enrolment

* **-ence endings preference:**
  - defence (not defense), licence (noun), offence
  - pretence, practice (noun), advice (noun)
  - **Note:** license (verb), practise (verb), advise (verb)

#### **4.1.2 Technology and Business Terms**

**British-Specific Technology Terms:**
- programme (computer program, but "program" for software)
- mobile phone (not cell phone)
- website optimisation (not optimization)
- colour scheme, colour palette
- customisation, personalisation

**Business and Professional Terms:**
- cheque (not check for payment)
- CV (not resume)
- full stop (not period)
- postcode (not zip code)
- turnover (not revenue in many contexts)

### 4.2 Procedure: British Terminology and Vocabulary Standards

#### **4.2.1 Mandatory British Terms**

Replace American equivalents with British terms consistently:

**Business and Professional Context:**
* lift (not elevator)
* ground floor (not first floor)
* car park (not parking lot)
* timetable (not schedule - in certain contexts)
* whilst (acceptable alongside while)
* amongst (acceptable alongside among)
* holiday (not vacation)
* autumn (not fall)

**Digital Marketing Context:**
* click-through rate (hyphenated)
* optimisation (not optimization)
* personalisation (not personalization)
* analyse (not analyze)
* colour coding, colour theory

**Financial and Business Terms:**
* turnover (for annual revenue in many contexts)
* profit and loss account (not income statement)
* limited company (Ltd)
* value added tax (VAT)
* pounds sterling (£)

#### **4.2.2 Cultural Context Requirements**

**British Cultural References:**
- Use British examples and case studies where possible
- Reference UK regulatory standards (GDPR, UK GDPR, ICO)
- Include British business practices and conventions
- Use appropriate British institutional references

**Time and Date Formats:**
- DD/MM/YYYY date format (e.g., 26/08/2025)
- 24-hour time format acceptable (13:00 not 1:00 PM)
- British holiday references (bank holidays, not national holidays)

### 4.3 Procedure: British English Punctuation and Grammar Rules

#### **4.3.1 Punctuation Standards**

**Quotation Marks:**
- Use single quotes for primary quotations: 'This is correct'
- Use double quotes for quotations within quotations: 'He said "hello" to me'
- Punctuation outside quotation marks unless part of quoted material
- Correct: The system includes 'advanced features'.
- Incorrect: The system includes 'advanced features.'

**Punctuation in Lists:**
- Oxford comma optional but be consistent within documents
- Prefer no comma before 'and' in simple lists
- Use comma before 'and' in complex lists for clarity

**Apostrophes:**
- Its (possessive) vs it's (it is)
- 1990s (not 1990's)
- Company's (singular possessive) vs companies' (plural possessive)

**Hyphenation:**
- Well-known (when used as adjective before noun)
- Twenty-one, thirty-five (compound numbers)
- E-commerce, e-mail (hyphenated forms acceptable)
- Up-to-date (when used as adjective)

#### **4.3.2 Grammar Conventions**

**Verb Forms:**
- Use "have got" alongside "have" (both acceptable)
- Collective nouns can take singular or plural verbs (government is/are)
- Prefer "shall" in formal contexts, "will" in informal

**Prepositions:**
- Different from/to (both acceptable, prefer "from")
- At weekends (not on weekends)
- In the street (not on the street)
- Write to someone (not write someone)

### 4.4 Procedure: Automated Validation Framework

#### **4.4.1 Pre-Generation Validation**

Before content generation begins:

1. **Language Model Configuration:**
   - Configure all AI agents to prioritise British English
   - Set spell-checking dictionaries to British English (en-GB)
   - Implement automated British English prompts in agent instructions
   - Validate language locale settings across all systems

2. **Template Validation:**
   - Ensure all content templates use British English defaults
   - Validate form fields, error messages, and UI text
   - Check automated email templates and notifications
   - Verify report templates and documentation standards

#### **4.4.2 Real-Time Content Validation**

During content generation and review:

1. **Automated Spell-Check Implementation:**
   ```
   Required Tools:
   - Hunspell British English dictionary (en_GB)
   - Grammar checking with British English rules
   - Style checking for American/British variants
   - Custom dictionary for business terms
   ```

2. **Pattern-Based Validation:**
   - Automated detection of American spellings
   - Flag common American/British variations
   - Check date formats and currency symbols
   - Validate terminology consistency

3. **Quality Gate Integration:**
   - British English validation must pass before content approval
   - Automated flagging of non-compliant content
   - Integration with existing quality control protocols
   - Mandatory validation report generation

#### **4.4.3 Validation Checklist Automation**

**Automated Checklist Items:**
- [ ] All -ise endings used (not -ize)
- [ ] All -our endings used (not -or)
- [ ] All -re endings used (not -er)
- [ ] British terminology implemented
- [ ] Single quotes used for primary quotations
- [ ] DD/MM/YYYY date format used
- [ ] Currency in pounds sterling (£)
- [ ] British cultural context appropriate
- [ ] No American spellings detected
- [ ] Grammar rules comply with British conventions

### 4.5 Procedure: Quality Assurance and Review Process

#### **4.5.1 Multi-Layer Review Protocol**

**Layer 1: Automated Validation**
- Run British English spell-check and grammar validation
- Apply pattern matching for common American variants
- Generate compliance report with specific issues identified
- Auto-flag content requiring manual review

**Layer 2: Agent Self-Assessment**
- AI agents must verify British English compliance before output
- Include British English confidence scoring in agent responses
- Document any assumptions about regional preferences
- Flag uncertain terminology for human review

**Layer 3: Human Quality Review**
- Manual review by British English-fluent reviewer
- Validation of cultural context appropriateness
- Assessment of professional communication standards
- Final approval authority for British English compliance

#### **4.5.2 Error Handling and Correction Protocols**

**Common Error Patterns and Corrections:**

1. **American Spellings Detection:**
   - Automated replacement suggestions
   - Pattern-based correction recommendations
   - Manual review for context-sensitive corrections
   - Learning algorithms to improve detection

2. **Terminology Inconsistencies:**
   - Flag mixed British/American terminology
   - Provide standardised replacement options
   - Maintain consistency checking across documents
   - Update style guides based on common issues

3. **Cultural Context Issues:**
   - Review business practice references
   - Validate regulatory and legal references
   - Check currency and measurement units
   - Verify time zone and date conventions

## 5.0 Integration Points

### 5.1 Quality Control Anti-Hallucination Protocol Integration

This SOP integrates with DWS-SOP-QUALITY-001 to ensure:
- British English validation forms part of confidence scoring
- Source verification includes validation of British English sources
- Quality gates include mandatory language compliance checks
- Human review processes incorporate British English expertise

### 5.2 Content Substance and Humanisation SOP Alignment

Coordination with DWS-SOP-CONTENT-003 ensures:
- Writing style guidelines reflect British English conventions
- Voice and tone requirements use British cultural context
- Professional communication standards align with British business practices
- Content credibility includes appropriate British references

### 5.3 Technical Validation System Requirements

Integration with technical validation systems:
- Automated British English checking in content pipelines
- API integration with British English validation services
- Real-time language compliance monitoring
- Performance metrics for British English accuracy

## 6.0 Tools and Resources

### 6.1 Required Validation Tools

**Primary British English Resources:**
- Oxford English Dictionary (online access)
- Cambridge Dictionary (British English section)
- Collins Dictionary British English
- Government Digital Service (GDS) style guide
- BBC News style guide

**Automated Validation Software:**
- Hunspell with British English dictionary (en_GB)
- LanguageTool with British English rules
- Grammarly set to British English
- Microsoft Editor configured for British English
- Custom validation scripts for business terminology

### 6.2 Reference Materials

**Style Guide Hierarchy (in order of authority):**
1. Oxford Style Manual
2. Cambridge Style Guide  
3. Government Digital Service style guide
4. BBC News style guide
5. Guardian and Observer style guide
6. Times style guide

**Specialist Resources:**
- British English business writing guides
- UK marketing communication standards
- Digital marketing terminology guides
- Professional services communication standards

## 7.0 Success Criteria and Monitoring

### 7.1 Compliance Metrics

**Mandatory Targets:**
- **100% British English Spelling Compliance:** Zero American spellings in final outputs
- **95%+ Terminology Consistency:** Consistent use of British terms across all content
- **100% Automated Validation Pass Rate:** All content must pass automated British English checks
- **24-hour Review SLA:** Maximum time for British English compliance review

### 7.2 Quality Monitoring Framework

**Daily Monitoring:**
- Automated validation pass/fail rates
- Common error pattern identification
- Processing time for compliance reviews
- Agent British English accuracy scoring

**Weekly Review:**
- Comprehensive accuracy assessment
- Reviewer feedback analysis
- Error pattern trend analysis
- Tool effectiveness evaluation

**Monthly Optimisation:**
- Validation rule refinement
- Dictionary and terminology updates
- Review process efficiency analysis
- Training needs assessment

### 7.3 Continuous Improvement Protocol

**Quarterly Reviews:**
- Complete SOP effectiveness assessment
- Integration with new tools and systems
- Style guide updates and revisions
- Benchmark comparison with industry standards

**Annual Audit:**
- Comprehensive British English compliance audit
- External expert review of standards
- Technology and tool upgrade assessment
- Complete process optimisation review

## 8.0 Common American to British English Conversions

### 8.1 High-Priority Business Terms

| American Term | British Term | Context Usage |
|---------------|--------------|---------------|
| optimize | optimise | SEO optimisation, website optimisation |
| analyze | analyse | Data analyse, competitor analyse |
| organization | organisation | Business organisation, client organisation |
| customize | customise | Website customisation, service customisation |
| color | colour | Brand colour, colour scheme, colour palette |
| program | programme | Training programme, marketing programme |
| center | centre | Contact centre, cost centre, shopping centre |
| theater | theatre | Marketing theatre, user experience theatre |
| license | licence (noun) | Software licence, user licence |
| practice | practise (verb) | Best practise guidelines, practise implementation |
| check | cheque | Payment by cheque, cheque processing |
| vacation | holiday | Holiday marketing, holiday periods |
| fall | autumn | Autumn campaign, autumn launch |

### 8.2 Technical and Digital Marketing Terms

| American Term | British Term | Usage Context |
|---------------|--------------|---------------|
| cell phone | mobile phone | Mobile marketing, mobile optimisation |
| zip code | postcode | Address validation, local SEO |
| parking lot | car park | Location-based marketing |
| elevator | lift | User journey, navigation design |
| apartment | flat | Property marketing, local content |
| sidewalk | pavement | Local business references |
| trash/garbage | rubbish | Waste management clients, environmental content |
| gas | petrol | Automotive clients, local content |
| cookie | biscuit | Food industry content (context-dependent) |

### 8.3 Measurement and Currency

| American Standard | British Standard | Application |
|------------------|------------------|-------------|
| MM/DD/YYYY | DD/MM/YYYY | All date references |
| $ (dollar) | £ (pound) | Pricing, budget references |
| zip code | postcode | Address forms, local SEO |
| miles | miles (same) | Distance measurements |
| feet/inches | metres/centimetres | Technical specifications |

## 9.0 Error Escalation and Exception Handling

### 9.1 Error Classification System

**Level 1 - Automated Correction:**
- Simple spelling variations (color → colour)
- Standard terminology substitutions
- Date format corrections
- Currency symbol replacements

**Level 2 - Review Required:**
- Context-dependent term choices
- Technical terminology validation
- Cultural reference appropriateness
- Complex grammar construction issues

**Level 3 - Expert Consultation:**
- Industry-specific terminology disputes
- Client preference conflicts
- Regulatory compliance language
- Brand voice adaptation requirements

### 9.2 Exception Approval Process

**Client Specification Exceptions:**
- Document client requests for American English
- Require written approval for exceptions
- Maintain consistency within client projects
- Regular review of exception justifications

**Technical Term Exceptions:**
- Software interface terms (may retain American spelling)
- Quoted material from American sources
- Brand names and trademarked terms
- API documentation and technical specifications

## 10.0 Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| **System Orchestrator** | Ensures all workflows implement British English compliance checks |
| **AI Agents** | Apply British English standards to all generated content and self-validate compliance |
| **Content Reviewers** | Conduct expert British English review within defined SLA timeframes |
| **Quality Assurance Lead** | Monitor British English compliance metrics and coordinate improvements |
| **Technical Lead** | Maintain automated validation tools and integration systems |
| **Project Manager** | Ensure SOP compliance across all client deliverables and internal documentation |

## 11.0 Implementation Timeline

### 11.1 Phase 1 - Immediate Implementation (Week 1)
- Configure all AI agents for British English defaults
- Implement automated spell-checking with British English dictionaries
- Update content templates and documentation standards
- Begin automated validation of existing content

### 11.2 Phase 2 - System Integration (Week 2)
- Integrate British English validation into quality control workflows
- Train human reviewers on British English standards
- Implement real-time validation in content generation pipelines
- Establish monitoring and reporting systems

### 11.3 Phase 3 - Optimisation and Monitoring (Ongoing)
- Continuous monitoring of compliance metrics
- Regular updates to validation rules and terminology
- Quarterly review of standards and tool effectiveness
- Annual comprehensive audit and improvement planning

---

**Document Control:**
- This SOP establishes the authoritative British English standards for all system outputs
- Changes require approval from Quality Assurance Lead and Project Manager
- All system users must acknowledge understanding of British English requirements
- Compliance is mandatory and subject to continuous monitoring and audit