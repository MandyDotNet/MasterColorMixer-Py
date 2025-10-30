# ADR 0001 — Architecture Decision for the Master Color Mixer Application

- **Date:** 2025-10-30
- **Status:** Accepted

## Context
The Master Color Mixer is a small desktop application designed for young children, focusing on accessibility. The project has a very tight timeline of about eight weeks and is being built by a single developer. For a project of this size, architecture that allows for fast development without requiring a lot of time to set up or maintain complex infrastructure, is required.

What the application needs to do:
- Provide a simple user interface (UI) where a child can tap/click to hear a color's name, drag colors to a mixing area to mix them (REQ-1 to REQ-6, REQ-13).
- Save the child's progress or preferences locally on their computer, not on the internet (REQ-22). SQLite will be used for this.
- Have a few simple internal tools for testing and automated processes (REQ-14, REQ-20).
- Work perfectly offline, as it's a desktop app. Local or pyttsx3 library will be used for Text-to-Speech (TTS) capabilities (REQ-21).
- Be easy to test to best ensure it works correctly for its young users (REQ-14, REQ-20).
- Not require any advanced scaling. Since it's a desktop application, there is no concern regarding millions of simultaneous users.
- Require very little effort to operate and maintain after deployment, as we have limited time for "operational" tasks.

## Decision
**Monolith.** A single deployable process (all-in-one application, no microservice applications) with clear internal layers:
- UI (using Tkinter) The visual part of the program for the child to interact with (REQ-1 to REQ-8).
- Domain/Services (mixing algorithm, TTS orchestration) The brain of the application.
- Persistence (SQLite) This layer handles saving and loading data locally on the user's device (REQ-6, REQ-20).
- Internal API (FastAPI) Run a small web API to create tests/automation and programatic control of the application (REQ-9). For developer's use only, is not a public interface.

 
## Consequences
**Positive**
- Minimal deployment and operational efforts. Only need to manage one codebase and one simple deployment process.
- Straightforward local dev/test. All parts of the application run together in the same process, making it much easier to debug and iterate quickly.
- Fewer integration seams, as all parts of the program can communicate without a network.
- Simpler end-to-end testing, because there is no network reliance, reducing the number of failure points.

**Negative**
- Tight Coupling Risk. Different layers in the application can become too dependent on each other. Changes to the application can become harder and riskier over time.
- A monolith scales as a single unit. If, for example, the TTS service needed a lot more processing power, we couldn't just scale that one piece. We'd have to scale the entire application. However, for a desktop app with no external scaling needs, this is not a concern.

**Mitigations**
- Enforce package boundaries (ui/, domain/, infra/, api/) remain in their different areas in the program structure.
- Keep services user interface-driven (a `TTSService` with a specific speak() function, `ColorRepo` with a specific mix() function).
- Write focused tests for individual parts of the application and simple tests for the internal API to ensure they work as expected.

## Risks
- **Risk:** Feature creep makes the monolith messy. Project needs to remain focused on required deliverables.
  **Mitigation:** Follow coding standards, enforce our module boundaries, and keep code changes small and focused. This will allow for faster, safer refactoring.
- **Risk:** A future decision to create a mobile or web version of the app would require a complete redesign of architecture and requirements.
  **Mitigation:** Keep domain clean, free of UI services, making the core logic reusable.

## Alternatives Considered
- **Microservices:** Overhead (setting up and managing infrastructure, monitoring, security, auth, CI/CD) exceeds scope of the project and expected delivered value.
- **Serverless backend:** Offline is a goal, so the idea of a cloud-based serverless approach (like AWS Lambda) was rejected because it introduces a cloud dependency and latency. It doesn't meet the requirement of being offline-friendly.
- **Plugin/hexagonal split across processes:** While a good idea academically, it's far too much for a project of this size and timeline.

## Why this fits a solo 8-week project
A monolith maximizes build speed and learning outcomes with minimal tooling risk. It lets one developer ship UI, algorithm, TTS, persistence, and tests coherently without spending weeks on service boundaries and deployment pipelines. For MasterColorMixer, monolith is the right choice. It maximizes build speed and learning outcomes due to minization of tooling risks (learning curves).
