#!/usr/bin/env python3
"""
Script to generate GitHub issue content from the scope breakdown.
This creates individual issue files that can be used to create GitHub issues.
"""

import os
from pathlib import Path

# Issue data structure based on the breakdown in ISSUES_FROM_SCOPE.md
ISSUES = [
    {
        "title": "Define Metadata Schema for Samples and Devices",
        "priority": "High",
        "labels": ["enhancement", "architecture", "metadata"],
        "description": """Create a comprehensive metadata schema that captures:
- Device name and identification
- Electrode connections and configuration  
- Sample type and properties
- Physical parameters (dimensions, materials, etc.)
- Environmental conditions during measurement""",
        "acceptance_criteria": [
            "JSON schema definition for sample metadata",
            "JSON schema definition for device metadata",
            "Documentation with examples", 
            "Validation functions for metadata",
            "Integration with measurement framework"
        ],
        "references": "Issue #1 - 'Metadata Schema - To be determined'"
    },
    {
        "title": "Define Metadata Schema for Instruments", 
        "priority": "High",
        "labels": ["enhancement", "architecture", "metadata"],
        "description": """Create a comprehensive metadata schema that captures:
- Instrument model, serial number, and version information
- Configuration parameters and settings
- Calibration data and dates
- Connection parameters (address, interface type)
- Operational limits and safety parameters""",
        "acceptance_criteria": [
            "JSON schema definition for instrument metadata",
            "Auto-capture of instrument settings during measurements",
            "Documentation with examples",
            "Integration with qcodes instrument drivers", 
            "Validation and consistency checks"
        ],
        "references": "Issue #1 scope - 'All metadata from the instruments... is saved'"
    },
    {
        "title": "Implement Data Model with Independent/Dependent Variables",
        "priority": "High", 
        "labels": ["enhancement", "architecture", "data-model"],
        "description": """Design and implement the fundamental data model that:
- Clearly separates parameters set (independent) vs parameters measured (dependent)
- Uses qcodes dataset as foundation
- Supports HDF5 and JSON export formats
- Includes versioning for data structure evolution
- Maintains backward compatibility""",
        "acceptance_criteria": [
            "Core data structure implementation",
            "Integration with qcodes datasets",
            "HDF5 export functionality",
            "JSON export functionality",
            "Data versioning system",
            "Documentation and examples",
            "Unit tests for data model"
        ],
        "references": "Issue #1 scope - 'Data structure is based on the principle of dependent and independent variables'"
    },
    {
        "title": "Implement Instrument Safety Limits and Pre-checks",
        "priority": "High",
        "labels": ["enhancement", "safety", "limits"], 
        "description": """Create a safety system that:
- Defines configurable instrument limits
- Performs pre-measurement validation
- Prevents unsafe parameter combinations
- Validates against instrument specifications
- Provides clear error messages for limit violations""",
        "acceptance_criteria": [
            "Limit definition schema/format",
            "Pre-measurement validation engine",
            "Integration with instrument drivers",
            "Configurable safety thresholds",
            "Clear error reporting",
            "Documentation for setting up limits",
            "Unit tests for limit checking"
        ],
        "references": "Issue #1 scope - 'Instrument limits are checked before... measurements for safety'"
    },
    {
        "title": "Implement Runtime Safety Monitoring and Interlocks",
        "priority": "High",
        "labels": ["enhancement", "safety", "runtime"],
        "description": """Create runtime safety monitoring that:
- Continuously monitors instrument parameters during measurements
- Implements software interlocks for critical limits
- Provides automatic shutdown on safety violations
- Logs all safety events with timestamps
- Allows configurable monitoring intervals""",
        "acceptance_criteria": [
            "Runtime monitoring framework",
            "Configurable interlock system", 
            "Automatic shutdown procedures",
            "Safety event logging",
            "Recovery and restart capabilities",
            "Performance optimization for monitoring overhead",
            "Integration tests with safety scenarios"
        ],
        "references": "Issue #1 scope - 'Instrument limit policies: pre-checks, continuous checks, interlocks'"
    },
    {
        "title": "Implement Safe Pause/Resume/Stop for Measurements",
        "priority": "Medium",
        "labels": ["enhancement", "runtime-control"],
        "description": """Create runtime control capabilities that:
- Allow safe pausing of measurements without data loss
- Enable resuming from exact pause point
- Implement clean stopping with data preservation
- Handle instrument state management during pauses
- Provide transaction/rollback semantics for partial data""",
        "acceptance_criteria": [
            "Pause functionality with state preservation",
            "Resume capability from pause point",
            "Safe stop with data integrity",
            "Instrument state management",
            "Transaction semantics for data",
            "Recovery from unexpected interruptions",
            "User interface for runtime control",
            "Integration tests for all control scenarios"
        ],
        "references": "Issue #1 scope - 'Safe pause/resume/stop for scans' and 'Transaction/rollback semantics'"
    },
    {
        "title": "Implement Runtime Parameter Adaptation", 
        "priority": "Medium",
        "labels": ["enhancement", "runtime-control", "adaptive"],
        "description": """Create adaptive measurement capabilities that:
- Allow modification of scan parameters during execution
- Implement adaptive current limits based on real-time conditions
- Support 2D field-temperature sweeps with adaptive parameters
- Maintain data consistency during parameter changes
- Log all parameter modifications with timestamps""",
        "acceptance_criteria": [
            "Runtime parameter modification interface",
            "Adaptive limit algorithms",
            "Support for multi-dimensional adaptive scans",
            "Data consistency during parameter changes", 
            "Parameter change logging and history",
            "Examples of adaptive measurements",
            "Integration with safety limits"
        ],
        "references": "Issue #1 scope - 'Adapt scan parameters mid-run' and '2D field–temperature sweep with adaptive current limit'"
    },
    {
        "title": "Implement Comprehensive Error Handling and Recovery",
        "priority": "Medium",
        "labels": ["enhancement", "error-handling", "recovery"],
        "description": """Create error handling system that:
- Handles instrument communication errors gracefully
- Manages limit trip scenarios safely
- Implements timeout handling with retries
- Provides safe shutdown procedures on errors
- Enables recovery and restart capabilities
- Logs all errors with context information""",
        "acceptance_criteria": [
            "Communication error handling",
            "Limit trip recovery procedures",
            "Timeout and retry mechanisms",
            "Safe shutdown on critical errors",
            "Error logging and diagnostics",
            "Recovery and restart capabilities",
            "Error classification and escalation",
            "Integration tests for error scenarios"
        ],
        "references": "Issue #1 scope - 'Handling of instrument comms errors, limit trips, timeouts; retries and safe shutdown'"
    },
    {
        "title": "Specify Minimum QCodes Version and Dependencies",
        "priority": "Medium", 
        "labels": ["enhancement", "dependencies", "documentation"],
        "description": """Establish clear dependency requirements:
- Specify minimum qcodes version with justification
- Define compatibility matrix for key dependencies
- Document any version-specific features used
- Create dependency update strategy
- Ensure compatibility testing across versions""",
        "acceptance_criteria": [
            "Minimum qcodes version specification in pyproject.toml",
            "Dependency compatibility matrix documentation",
            "Version-specific feature documentation",
            "Automated compatibility testing setup",
            "Dependency update guidelines",
            "Migration guide for version updates"
        ],
        "references": "Issue #1 scope - 'Minimum supported qcodes version to be specified'"
    },
    {
        "title": "Develop Testing Strategy and Framework",
        "priority": "Medium",
        "labels": ["enhancement", "testing", "ci-cd"],
        "description": """Create testing framework that:
- Tests measurement workflows end-to-end
- Validates safety and limit checking
- Tests error handling and recovery
- Includes performance and stability testing
- Supports both real and simulated instruments
- Integrates with CI/CD pipeline""",
        "acceptance_criteria": [
            "Unit testing framework setup",
            "Integration testing for measurements",
            "Safety and limits testing",
            "Error scenario testing", 
            "Performance and stress testing",
            "Instrument simulation for testing",
            "CI/CD integration",
            "Code coverage requirements and reporting"
        ],
        "references": "Issue #1 scope - 'Testing Strategy - To be determined'"
    },
    {
        "title": "Create CLI Interface and Usage Examples",
        "priority": "Low",
        "labels": ["enhancement", "user-interface", "examples"],
        "description": """Create user-friendly interface and examples:
- Basic CLI for common measurement tasks
- Example scripts for typical use cases
- Tutorial documentation for new users
- Best practices guide
- Integration examples with common instruments""",
        "acceptance_criteria": [
            "Basic CLI implementation",
            "Example measurement scripts",
            "Tutorial documentation",
            "Best practices documentation",
            "Integration examples for popular instruments",
            "CLI help and documentation",
            "Installation and setup guide"
        ],
        "references": "Issue #1 scope - 'No GUI features are planned beyond basic CLI/examples'"
    },
    {
        "title": "Review Current Quantify vs QCodes Architecture Decision",
        "priority": "High",
        "labels": ["architecture", "review", "breaking-change"],
        "description": """The current implementation uses quantify_core framework, but the scope document specifies using qcodes as the foundation. This needs architectural review:
- Evaluate benefits/drawbacks of current quantify_core approach
- Compare with pure qcodes implementation
- Assess migration effort if change is needed
- Make architectural decision and document rationale""",
        "acceptance_criteria": [
            "Architecture comparison document",
            "Performance and feature analysis",
            "Migration effort assessment", 
            "Architectural decision record (ADR)",
            "Implementation plan for chosen approach",
            "Update scope document if needed"
        ],
        "references": "Issue #1 scope states 'Use qcodes as the foundation' but current code uses quantify_core"
    }
]

def generate_issue_files():
    """Generate individual GitHub issue files."""
    output_dir = Path("github_issues")
    output_dir.mkdir(exist_ok=True)
    
    for i, issue in enumerate(ISSUES, 1):
        # Create filename from title
        filename = issue["title"].lower().replace(" ", "_").replace("/", "_") + ".md"
        filepath = output_dir / filename
        
        # Generate issue content
        content = f"""# {issue['title']}

**Priority:** {issue['priority']}
**Labels:** {', '.join(issue['labels'])}

## Description

{issue['description']}

## Acceptance Criteria

"""
        for criteria in issue['acceptance_criteria']:
            content += f"- [ ] {criteria}\n"
            
        content += f"""
## References

{issue['references']}

## Additional Notes

This issue is derived from the comprehensive scope definition in Issue #1: "Define Scope, Objectives, and Project Boundaries for TransMeasPy Python Package".

---

*This issue was generated from the scope breakdown. Please review and adjust as needed before creating the GitHub issue.*
"""

        # Write file
        with open(filepath, 'w') as f:
            f.write(content)
            
        print(f"Generated issue {i}: {filepath}")

if __name__ == "__main__":
    print("Generating GitHub issue files from scope breakdown...")
    generate_issue_files()
    print(f"\nGenerated {len(ISSUES)} issue files in the 'github_issues' directory.")
    print("\nTo create the issues on GitHub:")
    print("1. Review each generated file")
    print("2. Copy the content to create new GitHub issues")
    print("3. Apply the suggested labels and priority")