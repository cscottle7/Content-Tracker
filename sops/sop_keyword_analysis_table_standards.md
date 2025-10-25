# SOP: Keyword Analysis Table Standards

| Document ID: | DWS-SOP-KEYWORD-001 |
| :--- | :--- |
| **Version:** | 1.0 |
| **Status:** | Final |
| **Approved By:** | Craig Cottle |
| **Date of Issue:** | 01-Sep-2025 |
| **Next Review Date:** | 01-Mar-2026 |

---

## 1.0 Purpose

This Standard Operating Procedure (SOP) establishes mandatory standards for keyword analysis table formatting and data presentation within the Autonomous Agentic Marketing System. This SOP ensures all keyword research outputs are presented in consistent, professional table formats with verified data only, eliminating estimated search volumes and providing actionable insights for SEO strategy development whilst maintaining data accuracy and professional presentation standards.

## 2.0 Scope

This SOP applies to all keyword research and analysis activities, including:
- Primary keyword research tables and strategic keyword selection
- Competitive keyword analysis and gap identification
- Long-tail keyword opportunity mapping and content planning
- SERP feature analysis and ranking opportunity assessment
- Local SEO keyword research and geographic targeting
- All outputs from keyword_researcher and competitive_intelligence_searcher agents

## 3.0 Definitions

* **Keyword Analysis Table**: Structured data presentation format for keyword research findings with verified metrics
* **Search Volume**: Actual monthly search volume data obtained through SERPAPI or verified sources (no estimates permitted)
* **Keyword Difficulty**: Competition metric based on actual SERP analysis and ranking data
* **Search Intent**: Classified user intent behind keyword searches (informational, navigational, transactional, commercial)
* **SERP Features**: Special elements in search results (featured snippets, local pack, images, videos)
* **Verified Data**: Keyword metrics obtained through API sources or direct SERP analysis (not estimated)

## 4.0 Procedures

### 4.1 Procedure: Standard Keyword Analysis Table Format

Establish consistent table structure for all keyword research outputs.

#### **Primary Keyword Analysis Table Template:**

```markdown
| Keyword | Search Volume | Keyword Difficulty | Search Intent | SERP Features | Current Rank | Opportunity Score | Priority |
|---------|---------------|-------------------|---------------|---------------|--------------|------------------|----------|
| orthodontist canberra | 1,847/month | 67/100 | Commercial | Local Pack, Reviews | Not Ranking | 8.5/10 | High |
| invisalign canberra | 892/month | 72/100 | Commercial | Local Pack, Ads | Position 7 | 7.2/10 | High |
| dental braces canberra | 634/month | 58/100 | Commercial | Local Pack | Position 12 | 6.8/10 | Medium |
| orthodontist near me | 2,340/month | 78/100 | Commercial | Local Pack, Maps | Not Ranking | 9.1/10 | High |
```

#### **Column Definitions and Requirements:**

1. **Keyword Column**:
   - **Format**: Exact keyword phrase as researched
   - **Casing**: Use lowercase unless proper nouns require capitalization
   - **Length**: Full keyword phrase, no truncation
   - **Validation**: Must match exactly what was searched in tools

2. **Search Volume Column**:
   - **Format**: `[NUMBER]/month` (e.g., "1,847/month")
   - **Data Source**: SERPAPI integration ONLY - no estimates
   - **Validation**: Must be actual API data or mark as "Unable to verify"
   - **Forbidden**: NO estimated volumes (e.g., "~2,000", "approximately 1,500")

3. **Keyword Difficulty Column**:
   - **Format**: `[NUMBER]/100` (e.g., "67/100")
   - **Source**: SERPAPI difficulty score or calculated from SERP analysis
   - **Calculation**: Based on actual top 10 competitor domain authority
   - **Alternative**: If no API data, use "Requires Analysis" instead of guessing

4. **Search Intent Column**:
   - **Options**: Commercial, Informational, Navigational, Transactional
   - **Determination**: Based on SERP feature analysis and top result content
   - **Mixed Intent**: Use "Commercial/Informational" for hybrid intents
   - **Validation**: Must align with actual SERP results observed

5. **SERP Features Column**:
   - **Format**: Comma-separated list (e.g., "Local Pack, Reviews, Ads")
   - **Options**: Local Pack, Featured Snippet, Images, Videos, Shopping, Ads, Reviews
   - **Source**: Direct SERP observation via browser automation
   - **Completeness**: List all observed features, not just primary ones

6. **Current Rank Column**:
   - **Format**: "Position [NUMBER]" or "Not Ranking" or "Page 2+"
   - **Source**: Actual SERP scraping or SERPAPI ranking data
   - **Validation**: Must be verified position, not estimated
   - **Updates**: Include date of ranking check

7. **Opportunity Score Column**:
   - **Format**: `[NUMBER]/10` (e.g., "8.5/10")
   - **Calculation**: (Search Volume Weight × 0.4) + (Low Competition Weight × 0.3) + (Intent Match × 0.3)
   - **Transparency**: Include scoring methodology in report appendix
   - **Objectivity**: Based on measurable factors, not subjective assessment

8. **Priority Column**:
   - **Options**: High, Medium, Low
   - **Criteria**: High (8.0+), Medium (6.0-7.9), Low (Below 6.0)
   - **Business Alignment**: Consider business goals in priority assignment
   - **Resource Consideration**: Factor implementation difficulty

### 4.2 Procedure: Competitive Keyword Analysis Table

Specialized table format for competitive keyword intelligence.

#### **Competitive Keyword Gap Analysis Table:**

```markdown
| Keyword | Our Rank | Competitor A | Competitor B | Competitor C | Search Volume | Gap Severity | Action Required |
|---------|----------|--------------|--------------|--------------|---------------|--------------|----------------|
| invisalign cost canberra | Not Ranking | Position 2 | Position 4 | Position 6 | 456/month | Critical | Create pricing page |
| orthodontist reviews canberra | Position 8 | Position 1 | Position 3 | Position 5 | 234/month | High | Improve review strategy |
| best orthodontist canberra | Not Ranking | Position 1 | Not Ranking | Position 7 | 178/month | Medium | Content gap |
```

#### **Competitive Analysis Column Requirements:**

1. **Competitor Columns**:
   - **Format**: "Position [NUMBER]" or "Not Ranking"
   - **Consistency**: Use same competitors across entire analysis
   - **Verification**: All positions verified via actual SERP checks
   - **Updates**: Include analysis date for all competitive positions

2. **Gap Severity Column**:
   - **Calculation**: Based on competitor ranking advantage and search volume
   - **Categories**: Critical (3+ competitors ranking, we're not), High (2+ ahead), Medium (1-2 ahead)
   - **Quantification**: Objective criteria, not subjective assessment

3. **Action Required Column**:
   - **Specificity**: Concrete action items, not generic recommendations
   - **Examples**: "Create pricing page", "Optimize title tags", "Build backlinks"
   - **Feasibility**: Realistic actions based on current website capabilities

### 4.3 Procedure: Long-Tail Keyword Opportunity Table

Specialized format for long-tail keyword research and content planning.

#### **Long-Tail Opportunity Analysis Table:**

```markdown
| Long-Tail Keyword | Parent Topic | Search Volume | Competition | Content Type | Content Status | Implementation Priority |
|-------------------|--------------|---------------|-------------|--------------|----------------|------------------------|
| how much does invisalign cost in canberra | invisalign cost | 89/month | Low | FAQ/Pricing | Missing | High |
| best orthodontist for adults canberra | adult orthodontics | 67/month | Medium | Service Page | Needs Optimization | Medium |
| invisalign vs braces comparison | orthodontic options | 156/month | Medium | Comparison Article | Missing | High |
| orthodontist payment plans canberra | payment options | 78/month | Low | Financing Page | Missing | High |
```

#### **Long-Tail Specific Column Requirements:**

1. **Parent Topic Column**:
   - **Purpose**: Group related long-tail keywords for content planning
   - **Consistency**: Use consistent parent topic naming across analysis
   - **Strategy**: Align with existing content pillars and service offerings

2. **Content Type Column**:
   - **Options**: Service Page, FAQ, Blog Post, Comparison Article, Local Page
   - **Matching**: Align content type with search intent and user journey stage
   - **Strategy**: Consider existing content architecture and gaps

3. **Content Status Column**:
   - **Options**: Missing, Needs Optimization, Adequate, Strong
   - **Assessment**: Based on actual page analysis, not assumptions
   - **Objectivity**: Measurable criteria for each status level

4. **Implementation Priority Column**:
   - **Factors**: Search volume × content gap × business impact
   - **Resource**: Consider content creation resources and timeline
   - **Strategy**: Align with broader content marketing strategy

### 4.4 Procedure: Local SEO Keyword Table

Specialized format for location-based keyword research.

#### **Local SEO Keyword Analysis Table:**

```markdown
| Local Keyword | Location Modifier | Search Volume | Local Pack Present | GMB Opportunity | Local Competitors | Distance Factor |
|---------------|-------------------|---------------|-------------------|-----------------|-------------------|-----------------|
| orthodontist canberra | canberra | 1,847/month | Yes | High | 8 competitors | City-level |
| orthodontist belconnen | belconnen | 234/month | Yes | Medium | 3 competitors | Suburb-level |
| orthodontist kingston | kingston | 156/month | No | High | 1 competitor | Suburb-level |
| orthodontist near me | [user location] | 2,340/month | Yes | High | Variable | Dynamic |
```

#### **Local SEO Column Requirements:**

1. **Location Modifier Column**:
   - **Specificity**: Exact location terms used in keyword
   - **Hierarchy**: City, suburb, region, or proximity-based
   - **Relevance**: Must align with business service areas

2. **Local Pack Present Column**:
   - **Format**: Yes/No based on actual SERP observation
   - **Impact**: Critical for local SEO strategy development
   - **Verification**: Direct SERP analysis required

3. **GMB Opportunity Column**:
   - **Assessment**: High/Medium/Low based on current GMB optimization
   - **Factors**: Reviews, photos, posts, Q&A optimization level
   - **Actionability**: Directly tied to Google My Business improvements

4. **Local Competitors Column**:
   - **Count**: Number of local businesses in local pack/top 10
   - **Analysis**: Competitor strength assessment in local results
   - **Strategy**: Inform competitive positioning approach

### 4.5 Procedure: Data Validation and Quality Assurance

Ensure all keyword analysis tables meet accuracy standards.

#### **Pre-Publication Validation Checklist:**

```markdown
### Table Quality Assurance Checklist
- [ ] All search volumes from SERPAPI or marked "Unable to verify"
- [ ] No estimated or approximated data in any cells
- [ ] All competitor positions verified via actual SERP checks
- [ ] SERP features observed and documented accurately
- [ ] Opportunity scores calculated using documented methodology
- [ ] Priority assignments follow established criteria
- [ ] Table formatting consistent across entire document
- [ ] Column headers match approved template exactly
- [ ] All data points traceable to source tools or methods
```

#### **Forbidden Data Presentation:**

```markdown
❌ NEVER USE IN KEYWORD TABLES:
- "~1,500/month" (estimated volume)
- "High competition" (without numeric score)
- "Appears to rank position 3" (unverified ranking)
- "Probably has local pack" (unverified SERP feature)
- "Good opportunity" (without scoring criteria)
- "TBD" or "Unknown" (without explanation)
- "Approximately 500 searches" (estimated language)
```

#### **Required Data Attribution:**

```markdown
✅ REQUIRED SOURCE DOCUMENTATION:
- "Source: SERPAPI data retrieved [DATE]"
- "SERP analysis conducted [DATE] via Playwright"
- "Competitor positions verified [DATE]"
- "Opportunity scores calculated using [METHODOLOGY]"
- "Rankings checked [DATE] from [LOCATION]"
```

## 5.0 Agent Implementation Requirements

### 5.1 Keyword Researcher Agent Integration

#### **Table Generation Code Template:**
```python
def generate_keyword_table(keywords_data):
    """Generate standardized keyword analysis table"""
    
    table_headers = [
        "Keyword", "Search Volume", "Keyword Difficulty", 
        "Search Intent", "SERP Features", "Current Rank", 
        "Opportunity Score", "Priority"
    ]
    
    verified_rows = []
    for keyword in keywords_data:
        # Validate all data points
        if keyword.get('search_volume') != 'estimated':
            row = format_keyword_row(keyword)
            verified_rows.append(row)
        else:
            # Trigger resolution for estimated data
            trigger_serpapi_verification(keyword['term'])
    
    return generate_markdown_table(table_headers, verified_rows)
```

### 5.2 Quality Assurance Integration

#### **Automatic Table Validation:**
```python
def validate_keyword_table(table_content):
    """Validate keyword table meets SOP standards"""
    
    validation_errors = []
    
    # Check for forbidden estimation language
    forbidden_terms = ['estimated', 'approximately', '~', 'around']
    for term in forbidden_terms:
        if term in table_content:
            validation_errors.append(f"Estimation language detected: {term}")
    
    # Verify required columns present
    required_columns = ["Search Volume", "Keyword Difficulty", "Current Rank"]
    for column in required_columns:
        if column not in table_content:
            validation_errors.append(f"Missing required column: {column}")
    
    return validation_errors
```

## 6.0 Success Metrics

### 6.1 Data Quality Metrics
- **Verification Rate**: Percentage of keyword data from verified sources
- **Estimation Elimination**: Zero estimated data points in final tables
- **Source Attribution**: 100% of data points traceable to tools/methods

### 6.2 Strategic Impact Metrics  
- **Opportunity Identification**: Number of high-value keyword gaps discovered
- **Implementation Success**: Ranking improvements for prioritized keywords
- **Client Action Rate**: Percentage of table recommendations implemented

This comprehensive keyword analysis table SOP ensures all keyword research outputs provide verified, actionable data in professional, consistent formats that drive effective SEO strategy development.