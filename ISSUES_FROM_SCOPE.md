# Issues to Create from Issue #1 Scope Definition

This document breaks down the comprehensive scope definition in Issue #1 into specific, actionable GitHub issues. Each issue below should be created as a separate GitHub issue.

## Foundation and Architecture Issues

### Issue: Define Metadata Schema for Samples and Devices
**Priority: High**
**Labels: enhancement, architecture, metadata**

Define the metadata schema for storing sample and device information as mentioned in the scope document.

**Description:**
Create a comprehensive metadata schema that captures:
- Device name and identification
- Electrode connections and configuration
- Sample type and properties
- Physical parameters (dimensions, materials, etc.)
- Environmental conditions during measurement

**Acceptance Criteria:**
- [ ] JSON schema definition for sample metadata
- [ ] JSON schema definition for device metadata  
- [ ] Documentation with examples
- [ ] Validation functions for metadata
- [ ] Integration with measurement framework

**References:** Issue #1 - "Metadata Schema - To be determined"

---

### Issue: Define Metadata Schema for Instruments
**Priority: High**
**Labels: enhancement, architecture, metadata**

Define the metadata schema for capturing instrument settings and configuration.

**Description:**
Create a comprehensive metadata schema that captures:
- Instrument model, serial number, and version information
- Configuration parameters and settings
- Calibration data and dates
- Connection parameters (address, interface type)
- Operational limits and safety parameters

**Acceptance Criteria:**
- [ ] JSON schema definition for instrument metadata
- [ ] Auto-capture of instrument settings during measurements
- [ ] Documentation with examples
- [ ] Integration with qcodes instrument drivers
- [ ] Validation and consistency checks

**References:** Issue #1 scope - "All metadata from the instruments... is saved"

---

### Issue: Implement Data Model with Independent/Dependent Variables
**Priority: High**
**Labels: enhancement, architecture, data-model**

Implement the core data structure based on independent and dependent variables principle.

**Description:**
Design and implement the fundamental data model that:
- Clearly separates parameters set (independent) vs parameters measured (dependent)
- Uses qcodes dataset as foundation
- Supports HDF5 and JSON export formats
- Includes versioning for data structure evolution
- Maintains backward compatibility

**Acceptance Criteria:**
- [ ] Core data structure implementation
- [ ] Integration with qcodes datasets
- [ ] HDF5 export functionality
- [ ] JSON export functionality  
- [ ] Data versioning system
- [ ] Documentation and examples
- [ ] Unit tests for data model

**References:** Issue #1 scope - "Data structure is based on the principle of dependent and independent variables"

---

## Safety and Limits Issues

### Issue: Implement Instrument Safety Limits and Pre-checks
**Priority: High**
**Labels: enhancement, safety, limits**

Implement comprehensive safety limit checking before measurements start.

**Description:**
Create a safety system that:
- Defines configurable instrument limits
- Performs pre-measurement validation
- Prevents unsafe parameter combinations
- Validates against instrument specifications
- Provides clear error messages for limit violations

**Acceptance Criteria:**
- [ ] Limit definition schema/format
- [ ] Pre-measurement validation engine
- [ ] Integration with instrument drivers
- [ ] Configurable safety thresholds
- [ ] Clear error reporting
- [ ] Documentation for setting up limits
- [ ] Unit tests for limit checking

**References:** Issue #1 scope - "Instrument limits are checked before... measurements for safety"

---

### Issue: Implement Runtime Safety Monitoring and Interlocks
**Priority: High**
**Labels: enhancement, safety, runtime**

Implement continuous safety monitoring during measurements with interlock capabilities.

**Description:**
Create runtime safety monitoring that:
- Continuously monitors instrument parameters during measurements
- Implements software interlocks for critical limits
- Provides automatic shutdown on safety violations
- Logs all safety events with timestamps
- Allows configurable monitoring intervals

**Acceptance Criteria:**
- [ ] Runtime monitoring framework
- [ ] Configurable interlock system
- [ ] Automatic shutdown procedures
- [ ] Safety event logging
- [ ] Recovery and restart capabilities
- [ ] Performance optimization for monitoring overhead
- [ ] Integration tests with safety scenarios

**References:** Issue #1 scope - "Instrument limit policies: pre-checks, continuous checks, interlocks"

---

## Runtime Control and Adaptability Issues

### Issue: Implement Safe Pause/Resume/Stop for Measurements
**Priority: Medium**
**Labels: enhancement, runtime-control**

Implement safe pause, resume, and stop functionality for long-running measurements.

**Description:**
Create runtime control capabilities that:
- Allow safe pausing of measurements without data loss
- Enable resuming from exact pause point
- Implement clean stopping with data preservation
- Handle instrument state management during pauses
- Provide transaction/rollback semantics for partial data

**Acceptance Criteria:**
- [ ] Pause functionality with state preservation
- [ ] Resume capability from pause point
- [ ] Safe stop with data integrity
- [ ] Instrument state management
- [ ] Transaction semantics for data
- [ ] Recovery from unexpected interruptions
- [ ] User interface for runtime control
- [ ] Integration tests for all control scenarios

**References:** Issue #1 scope - "Safe pause/resume/stop for scans" and "Transaction/rollback semantics"

---

### Issue: Implement Runtime Parameter Adaptation
**Priority: Medium**
**Labels: enhancement, runtime-control, adaptive**

Enable real-time adaptation of scan parameters during measurement execution.

**Description:**
Create adaptive measurement capabilities that:
- Allow modification of scan parameters during execution
- Implement adaptive current limits based on real-time conditions
- Support 2D field-temperature sweeps with adaptive parameters
- Maintain data consistency during parameter changes
- Log all parameter modifications with timestamps

**Acceptance Criteria:**
- [ ] Runtime parameter modification interface
- [ ] Adaptive limit algorithms
- [ ] Support for multi-dimensional adaptive scans
- [ ] Data consistency during parameter changes
- [ ] Parameter change logging and history
- [ ] Examples of adaptive measurements
- [ ] Integration with safety limits

**References:** Issue #1 scope - "Adapt scan parameters mid-run" and "2D field–temperature sweep with adaptive current limit"

---

## Error Handling and Recovery Issues

### Issue: Implement Comprehensive Error Handling and Recovery
**Priority: Medium**
**Labels: enhancement, error-handling, recovery**

Implement robust error handling for various failure scenarios.

**Description:**
Create error handling system that:
- Handles instrument communication errors gracefully
- Manages limit trip scenarios safely
- Implements timeout handling with retries
- Provides safe shutdown procedures on errors
- Enables recovery and restart capabilities
- Logs all errors with context information

**Acceptance Criteria:**
- [ ] Communication error handling
- [ ] Limit trip recovery procedures
- [ ] Timeout and retry mechanisms
- [ ] Safe shutdown on critical errors
- [ ] Error logging and diagnostics
- [ ] Recovery and restart capabilities
- [ ] Error classification and escalation
- [ ] Integration tests for error scenarios

**References:** Issue #1 scope - "Handling of instrument comms errors, limit trips, timeouts; retries and safe shutdown"

---

## Framework and Integration Issues

### Issue: Specify Minimum QCodes Version and Dependencies
**Priority: Medium**
**Labels: enhancement, dependencies, documentation**

Define and document minimum supported qcodes version and other dependencies.

**Description:**
Establish clear dependency requirements:
- Specify minimum qcodes version with justification
- Define compatibility matrix for key dependencies
- Document any version-specific features used
- Create dependency update strategy
- Ensure compatibility testing across versions

**Acceptance Criteria:**
- [ ] Minimum qcodes version specification in pyproject.toml
- [ ] Dependency compatibility matrix documentation
- [ ] Version-specific feature documentation
- [ ] Automated compatibility testing setup
- [ ] Dependency update guidelines
- [ ] Migration guide for version updates

**References:** Issue #1 scope - "Minimum supported qcodes version to be specified"

---

### Issue: Develop Testing Strategy and Framework
**Priority: Medium**
**Labels: enhancement, testing, ci-cd**

Develop comprehensive testing strategy for the measurement framework.

**Description:**
Create testing framework that:
- Tests measurement workflows end-to-end
- Validates safety and limit checking
- Tests error handling and recovery
- Includes performance and stability testing
- Supports both real and simulated instruments
- Integrates with CI/CD pipeline

**Acceptance Criteria:**
- [ ] Unit testing framework setup
- [ ] Integration testing for measurements
- [ ] Safety and limits testing
- [ ] Error scenario testing
- [ ] Performance and stress testing
- [ ] Instrument simulation for testing
- [ ] CI/CD integration
- [ ] Code coverage requirements and reporting

**References:** Issue #1 scope - "Testing Strategy - To be determined"

---

### Issue: Create CLI Interface and Usage Examples
**Priority: Low**
**Labels: enhancement, user-interface, examples**

Develop basic command-line interface and comprehensive usage examples.

**Description:**
Create user-friendly interface and examples:
- Basic CLI for common measurement tasks
- Example scripts for typical use cases
- Tutorial documentation for new users
- Best practices guide
- Integration examples with common instruments

**Acceptance Criteria:**
- [ ] Basic CLI implementation
- [ ] Example measurement scripts
- [ ] Tutorial documentation
- [ ] Best practices documentation
- [ ] Integration examples for popular instruments
- [ ] CLI help and documentation
- [ ] Installation and setup guide

**References:** Issue #1 scope - "No GUI features are planned beyond basic CLI/examples"

---

## Documentation and User Experience Issues

### Issue: Create Comprehensive Documentation for Repeatable Measurements
**Priority: Medium**
**Labels: documentation, user-experience**

Create documentation that enables easy repetition and traceability of experiments.

**Description:**
Develop documentation that:
- Explains the measurement framework concepts
- Provides step-by-step guides for common measurements
- Documents metadata schemas and their usage
- Includes troubleshooting guides
- Explains safety and limit configuration

**Acceptance Criteria:**
- [ ] Conceptual framework documentation
- [ ] Step-by-step measurement guides
- [ ] Metadata schema documentation
- [ ] Safety configuration guide
- [ ] Troubleshooting documentation
- [ ] API reference documentation
- [ ] Migration guide from other frameworks

**References:** Issue #1 scope - "Enable easy repetition and traceability of experiments"

---

## Architecture Review Issue

### Issue: Review Current Quantify vs QCodes Architecture Decision
**Priority: High**
**Labels: architecture, review, breaking-change**

Review the current use of quantify_core vs pure qcodes as specified in the scope.

**Description:**
The current implementation uses quantify_core framework, but the scope document specifies using qcodes as the foundation. This needs architectural review:
- Evaluate benefits/drawbacks of current quantify_core approach
- Compare with pure qcodes implementation
- Assess migration effort if change is needed
- Make architectural decision and document rationale

**Acceptance Criteria:**
- [ ] Architecture comparison document
- [ ] Performance and feature analysis
- [ ] Migration effort assessment
- [ ] Architectural decision record (ADR)
- [ ] Implementation plan for chosen approach
- [ ] Update scope document if needed

**References:** Issue #1 scope states "Use qcodes as the foundation" but current code uses quantify_core

---

## Summary

This breakdown creates **12 distinct issues** from the original scope document, organized by priority and functional area. Each issue is specific, actionable, and includes clear acceptance criteria. The issues are designed to be worked on in logical order, with foundation and architecture issues taking priority over user-facing features.

**Recommended Creation Order:**
1. Architecture Review (quantify vs qcodes)
2. Metadata schemas (samples/devices and instruments)  
3. Data model implementation
4. Safety limits and pre-checks
5. Runtime safety monitoring
6. Dependencies and testing strategy
7. Error handling and recovery
8. Runtime control features
9. Documentation and examples
10. CLI interface

This approach ensures that core architectural decisions are made first, followed by foundational components, safety features, and finally user-facing functionality.