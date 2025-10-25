# SOP: Screenshot and Media Management Standards

| Document ID: | DWS-SOP-MEDIA-001 |
| :--- | :--- |
| **Version:** | 1.0 |
| **Status:** | Final |
| **Approved By:** | Craig Cottle |
| **Date of Issue:** | 01-Sep-2025 |
| **Next Review Date:** | 01-Mar-2026 |

---

## 1.0 Purpose

This Standard Operating Procedure (SOP) establishes mandatory standards for screenshot capture, storage, and media management within the Autonomous Agentic Marketing System. This SOP ensures all visual evidence is properly captured, consistently organized, and readily accessible for client reports and internal documentation whilst maintaining professional presentation standards and efficient file management protocols.

## 2.0 Scope

This SOP applies to all screenshot and media capture activities, including:
- Website analysis screenshots and visual documentation
- Performance testing visual evidence and comparative analyses
- Competitive intelligence visual research and documentation
- Error documentation and technical issue reporting
- Client deliverable visual assets and supporting materials
- All agents utilizing browser automation tools (Playwright MCP)

## 3.0 Definitions

* **Screenshot**: Digital image capture of web page, application interface, or system state for documentation purposes
* **Visual Evidence**: Screenshots and media files that support analysis findings and recommendations
* **Project Folder**: Designated directory structure for organizing all project-related media assets
* **Naming Convention**: Standardized file naming protocol ensuring consistent organization and easy retrieval
* **Media Asset**: Any visual content including screenshots, exported charts, diagrams, or supporting imagery
* **Archive Structure**: Hierarchical folder organization system for long-term media storage and retrieval

## 4.0 Procedures

### 4.1 Procedure: Screenshot Storage Organization

Establish consistent project folder structure for all media assets.

#### **Step 1: Project Folder Creation**
Create standardized directory structure for every project:

```
PROJECT_NAME/
├── screenshots/
│   ├── website_analysis/
│   │   ├── homepage/
│   │   ├── product_pages/
│   │   ├── service_pages/
│   │   └── error_pages/
│   ├── performance_testing/
│   │   ├── gtmetrix_results/
│   │   ├── core_web_vitals/
│   │   └── comparison_charts/
│   ├── competitive_analysis/
│   │   ├── competitor_websites/
│   │   ├── social_media/
│   │   └── content_examples/
│   ├── accessibility_testing/
│   │   ├── accessibility_tree/
│   │   ├── contrast_issues/
│   │   └── navigation_testing/
│   └── technical_issues/
│       ├── errors/
│       ├── warnings/
│       └── before_after/
├── exported_data/
│   ├── reports/
│   ├── charts/
│   └── raw_data/
└── client_deliverables/
    ├── final_screenshots/
    └── presentation_assets/
```

#### **Step 2: Mandatory Folder Implementation**
All agents must implement this structure:

1. **Project Root Folder**: `C:\Users\cscot\Documents\Agents\Bigger Boss Agent\projects\[CLIENT_NAME]_[PROJECT_TYPE]_[DATE]`
2. **Screenshot Subfolder**: Always use `/screenshots/[ANALYSIS_TYPE]/` structure
3. **Auto-Creation**: Agents must create required folders before first screenshot
4. **Validation**: Verify folder existence before saving any media assets

### 4.2 Procedure: Screenshot Naming Conventions

Implement standardized file naming for all captured media.

#### **Standard Naming Pattern:**
```
[AGENT_NAME]_[PAGE_TYPE]_[ELEMENT]_[TIMESTAMP]_[SEQUENCE].png
```

#### **Naming Examples:**
```
technical_seo_analyst_homepage_meta_tags_20250901_143022_001.png
performance_tester_gtmetrix_results_core_web_vitals_20250901_143045_001.png
accessibility_checker_contrast_issues_navigation_menu_20250901_143108_001.png
competitive_intelligence_homepage_hero_section_20250901_143131_001.png
```

#### **Naming Component Rules:**
1. **Agent Name**: Use exact agent name from agent definition
2. **Page Type**: homepage, product_page, service_page, about_page, contact_page
3. **Element**: Specific element or section being documented
4. **Timestamp**: YYYYMMDD_HHMMSS format (24-hour time)
5. **Sequence**: 3-digit sequence number (001, 002, 003)
6. **Extension**: Always use .png for screenshots, .jpg for compressed images

### 4.3 Procedure: Agent Screenshot Implementation

Define mandatory screenshot capture protocols for each agent type.

#### **Technical SEO Analyst Screenshots:**
```markdown
**Required Screenshots:**
1. **Full Homepage**: Complete page capture including above/below fold
2. **Meta Tag Inspection**: Browser developer tools showing meta tags
3. **Page Titles**: Title tag display in browser tab and source code
4. **Heading Structure**: H1-H6 hierarchy visualization
5. **Error Pages**: 404, 500, and other error states if found

**Implementation Code:**
```python
# Use browser_take_screenshot tool with proper naming
screenshot_path = f"projects/{project_name}/screenshots/website_analysis/homepage/technical_seo_analyst_homepage_full_page_{timestamp}_001.png"
browser_take_screenshot(
    filename=screenshot_path,
    fullPage=True
)
```

#### **Performance Tester Screenshots:**
```markdown
**Required Screenshots:**
1. **GTMetrix Results**: Complete GTMetrix dashboard with scores
2. **Core Web Vitals**: Detailed performance metrics display  
3. **Network Waterfall**: Resource loading timeline visualization
4. **Performance Comparison**: Before/after optimization comparisons
5. **Mobile Performance**: Mobile-specific performance results

**Storage Location:** `projects/{project_name}/screenshots/performance_testing/`
```

#### **Accessibility Checker Screenshots:**
```markdown
**Required Screenshots:**
1. **Accessibility Tree**: Browser accessibility inspector view
2. **Contrast Issues**: Specific color contrast problems highlighted
3. **Keyboard Navigation**: Focus states and navigation paths
4. **Screen Reader Testing**: Screen reader output or simulation
5. **WCAG Violations**: Specific accessibility rule violations

**Storage Location:** `projects/{project_name}/screenshots/accessibility_testing/`
```

### 4.4 Procedure: Screenshot Quality Standards

Ensure all captured media meets professional standards.

#### **Technical Quality Requirements:**
1. **Resolution**: Minimum 1920x1080 for desktop, 375x667 for mobile
2. **Format**: PNG for interface screenshots, JPEG for content images
3. **Compression**: Balance file size with visual clarity (PNG: lossless, JPEG: 90% quality)
4. **Consistency**: Same browser, same window size for comparable screenshots
5. **Completeness**: Capture complete elements, avoid partial content

#### **Visual Quality Standards:**
1. **Clarity**: All text must be readable at 100% zoom
2. **Context**: Include enough surrounding content for context
3. **Annotations**: Use browser tools to highlight specific elements when needed
4. **Consistency**: Maintain consistent browser appearance across screenshots
5. **Documentation**: Each screenshot should clearly demonstrate specific findings

### 4.5 Procedure: Media Asset Management

Establish protocols for long-term media storage and retrieval.

#### **Archive Management:**
```markdown
**Monthly Archive Process:**
1. **Project Completion**: Move completed projects to archive folder
2. **Compression**: ZIP project folders with date stamps
3. **Backup**: Ensure archived projects included in backup procedures
4. **Retention**: Maintain archives for minimum 12 months
5. **Cleanup**: Remove temporary and duplicate screenshots

**Archive Structure:**
```
archives/
├── 2025/
│   ├── 01_January/
│   ├── 02_February/
│   └── ...
└── completed_projects/
    ├── project_name_YYYYMMDD.zip
    └── ...
```

#### **Quality Assurance Validation:**
1. **Screenshot Verification**: Confirm all required screenshots captured
2. **Naming Validation**: Verify all files follow naming conventions  
3. **Folder Structure**: Ensure proper organization and completeness
4. **File Integrity**: Check for corrupted or incomplete image files
5. **Documentation**: Verify screenshots support analysis findings

## 5.0 Agent Implementation Requirements

### 5.1 Mandatory Screenshot Commands

All agents with browser automation capabilities MUST implement:

#### **Pre-Screenshot Setup:**
```python
import os
from datetime import datetime

# Create project structure
project_name = "CLIENT_NAME_PROJECT_TYPE_20250901"
screenshot_dir = f"projects/{project_name}/screenshots/{agent_type}/"
os.makedirs(screenshot_dir, exist_ok=True)

# Generate timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
```

#### **Screenshot Capture Protocol:**
```python
# Standard screenshot with proper naming
screenshot_filename = f"{agent_name}_{page_type}_{element}_{timestamp}_{sequence:03d}.png"
screenshot_path = os.path.join(screenshot_dir, screenshot_filename)

# Take screenshot using Playwright MCP
browser_take_screenshot(
    filename=screenshot_path,
    fullPage=True  # For full page captures
)

# Document screenshot in report
report_entry = f"Screenshot captured: {screenshot_filename} - {description}"
```

### 5.2 Error Handling and Fallbacks

#### **Screenshot Failure Protocol:**
```python
try:
    browser_take_screenshot(filename=screenshot_path)
    screenshot_success = True
except Exception as e:
    screenshot_success = False
    error_log = f"Screenshot failed: {str(e)}"
    
    # Document failure in report
    report_entry = f"⚠️ Screenshot capture failed: {error_log}"
    
    # Attempt alternative capture method if available
    try:
        browser_take_screenshot(filename=screenshot_path, element=specific_element)
    except:
        report_entry += " - All screenshot methods failed"
```

### 5.3 Integration with Reporting System

#### **Screenshot References in Reports:**
```markdown
**Required Report Integration:**
- Every screenshot must be referenced in analysis text
- Include relative path to screenshot in report
- Provide clear description of what screenshot demonstrates
- Link screenshots to specific findings and recommendations

**Report Format Example:**
```markdown
### Technical SEO Issues Identified

The homepage title tag analysis revealed several optimization opportunities 
(see screenshot: `screenshots/website_analysis/homepage/technical_seo_analyst_homepage_meta_tags_20250901_143022_001.png`):

1. **Title Length**: Current title is 73 characters, exceeding 60-character limit
2. **Meta Description Missing**: No meta description found in source code
3. **H1 Tag Duplication**: Multiple H1 tags detected on single page
```

## 6.0 Quality Assurance and Compliance

### 6.1 Screenshot Audit Checklist

Before project completion, verify:

- [ ] All required screenshots captured per agent requirements
- [ ] Proper folder structure implemented and populated
- [ ] File naming conventions followed consistently
- [ ] Screenshot quality meets professional standards
- [ ] All screenshots referenced in corresponding reports
- [ ] Project folder ready for client delivery or archival
- [ ] Backup procedures include all media assets

### 6.2 Performance Monitoring

Track screenshot management effectiveness:

1. **Capture Success Rate**: Percentage of successful screenshot attempts
2. **Storage Utilization**: Monitor disk space usage and optimization opportunities
3. **Retrieval Efficiency**: Time required to locate specific screenshots
4. **Client Satisfaction**: Feedback on visual documentation quality
5. **Compliance Rate**: Adherence to naming and organization standards

This comprehensive screenshot management SOP ensures all visual evidence is consistently captured, properly organized, and readily available for analysis and client deliverables whilst maintaining professional standards and efficient workflows.