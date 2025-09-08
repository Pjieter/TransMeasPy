# TransMeasPy

Instrument-agnostic electronic transport measurement framework built on top of qcodes. TransMeasPy structures experiments around independent (set) and dependent (measured) variables, captures comprehensive instrument and sample metadata for reproducibility, enforces safety limits, and supports adaptable, stoppable measurements.

Status: Early planning. Expect API changes.

## Why TransMeasPy
- Instrument-agnostic: use qcodes drivers to control a wide range of instruments.
- Reproducible by default: persist instrument states, environment, and sample metadata.
- Safe and robust: preflight limit checks, continuous monitoring, and safe shutdown on violations.
- Adaptive experiments: change scan parameters during long runs without losing data.
- Metadata-first: dependent/independent variable model with rich, versioned metadata.

## Features
- Define measurements using independent (set) and dependent (measure) variables.
- Collect and store full instrument and sample/device metadata alongside data.
- Safe to stop at any point with consistent, partial dataset persistence.
- Adapt parameters (e.g., sweep ranges, step sizes) while measuring.
- Instrument limit validation before starting; optional continuous limit enforcement.
- Plugin-friendly architecture to add instruments and measurement types.

## Scope
- Electronic transport measurements using qcodes as the basis for instrument drivers.
- Dataset organization around independent/dependent variables.
- Comprehensive metadata capture (instruments, sample/device, environment).
- Safety-first execution with pre-checks and ongoing checks.
- Runtime control: pause/resume/stop and live parameter adaptation.

## Non-goals and boundaries
- Not a general framework for non-transport modalities (out of initial scope).
- No GUI beyond CLI/examples for the MVP.
- Does not include development of new qcodes drivers (relies on existing drivers).
- No built-in ML analytics (can be added externally).

## Target users and use cases
- Experimental physicists, lab technicians, and students.
- Example use cases:
  - 2D field–temperature sweep with adaptive current limit.
  - Repeatable multi-parameter measurement with full metadata capture.
  - Long-running scan where ranges are adjusted live based on intermediate results.

## Installation
TransMeasPy is in early development; install from source for now.

Prerequisites:
- Python >= 3.10 (recommended 3.12+)
- qcodes (minimum version: TBD)
- HDF5 (via h5py) if using HDF5-backed datasets


## Contributing
Contributions are welcome! Please open an issue to discuss proposed changes. PRs with tests and examples are encouraged.
Guidelines (TBD): coding standards, commit conventions, and review process.

## License
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgments
- Built on top of qcodes and the wider Python scientific ecosystem.