[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/lPRy1kM1)

<!-- README.md -->
<div align="center">
  <h1>MasterColorMixer</h1>
  <p><em>A toddler-friendly color mixing web app built with Python 3.12+, FastAPI, and a simple web UI.</em></p>
</div>


<h2 id="toc">Table of Contents</h2>
<ol>
  <li><a href="#charter">Project Charter</a></li>
  <li><a href="#plan">Two-Sprint Plan</a></li>
  <li><a href="#backlog">Personal Backlog</a></li>
  <li><a href="#trends">Trends Note</a></li>
  <li><a href="#run">How to Run Locally</a></li>
  <li><a href="#srs">Software Requirements Specification (SRS)</a></li>
</ol>

<h2 id="charter">Project Charter</h2>
<p>
  <strong>Purpose:</strong> <em>MasterColorMixer</em>  project is a fun and educational color-mixing web application designed for toddlers (ages 2–5). This application will help introduce basic concepts of color theory and interaction in a safe and tidy, child-friendly interface. Children start with three base colors (red, blue, yellow) then drag and drop up to two colors at a time into a “mixing bin” to discover new colors. When a color object is clicked on, the app speaks the color's name; when a new color is discovered, its name is spoken as immediate feedback. The experience promotes early learning by connecting visual play with auditory reinforcement while modeling SOLID software engineering practices.
</p>
<p>
  <strong>Objectives:</strong> 
  <ul>
    <li>Provide an interactive learning experience for toddlers focused on colors</li>
    <li>Deliver a Python 3.12+ service exposing a versioned HTTP API via FastAPI</li>
    <li>Implement a small, accessible web UI</li>
    <li>Support CRUD and persistence with a lightweight database</li>
    <li>Demonstrate Agile and SDLC principles in a Python-based application</li>
    <li>Provide clear documentation, tests, and a one-command local run</li>
    <li>The MVP aims for up to 20 unlockable colors, a reset (“Clear”) function for the mixing area, and reliable text-to-speech for color names</li>
      <ol>
        <li>base palette (red, blue, yellow)</li>
        <li>drag-and-drop of exactly two colors into a mixing area</li>
        <li>generation and display of the mixed color</li>
        <li>unlocking and persisting newly discovered colors (up to 20 total)</li>
        <li>a “Clear” control to reset the mix area</li>
        <li>audible color names on tap/click and post-mix using text-to-speech libraries like pyttsx3</li>
        <li>The API provides color resources, text to speech () and mixing operations</li>
        <li>the database persists unlocked colors by session/user</li>
      </ol>
  </ul>
</p>
<p>
  <strong>Stakeholders:</strong> 
  <ul>
  <li>Primary Stakeholders: Toddlers ages 2-5</li>
  <li>Secondary Stakeholders: Parents or Teachers supervising play and/or tracking progress</li>
  <li>Developer: Amanda Crotty, solo developer for this COP4504 - October 2025 course, responsible for planning, implementation, and maintenance</li>
  <li>Instructor: Franklin Castillo, course facilitator providing guidance and evaluation based on SDLC & Agile adherence</li>
  </ul>
</p>
<p>
  <strong>Risks:</strong> 
  <ul>
    <li>Time constraint: balance coursework and implementation with approximately 18 hours per week</li>
    <li>Scope creep: avoid adding advanced game mechanics outside of the MVP scope</li>
    <li>Accesibility: Ensuring sound playback, visiaul clarity, and color contrasts are toddler appropriate</li>
    <li>Dependency management: managing virtual environments and python package versions</li>
  </ul>
</p>

<p>
  <strong>Success Criteria:</strong> 
  <ul>
    <li>The application supports all MVP features:
        <ul>
        <li>Start the game with 3 basic colors (red, blue, yellow)</li>
        <li>Play color names aloud on click and when a new color is formed</li>
        <li>Allow for drag-and-drop mixing of two colors as combinations are discovered</li>
        <li>Unlock up to 20 colors as combinations are discovered</li>
        <li>Support clear functionality to reset the mixing area</li>
        <li>Support clear functionality to reset the game area to the basic colors without restarting the application</li>
      </ul>
    </li>
    <li>Code is modular and includes unit tests</li>
    <li>Documentation is complete (README, CONTRIBUTING, SRS traceability)</li>
    <li>App deploys and runs locally via command: TBD</li>
  </ul>


<h2 id="plan">Two-Sprint Plan</h2>

<h3>Sprint 1 (Weeks 2–4) Requirements, Design, Decisions, Inclusivity & Skeleton</h3>
<ul>
  <li><strong>Week 2 (SRS & UML)</strong>
    <ul>
      <li>Write the SRS:
        <em>scope, stakeholders, assumptions, functional & nonfunctional requirements, acceptance criteria, glossary</em>.</li>
      <li>Create <strong>1 Class Diagram</strong> (domain + interfaces) and <strong>2 Sequence Diagrams</strong> (core use cases, each with one alternative path).</li>
      <li>Build the <strong>traceability table</strong> (REQ-IDs → classes → sequence diagrams → planned tests).</li>
      <li>Update README to include SRS, UML, and traceability.</li>
    </ul>
  </li>
  <li><strong>Week 3 (ADR & Paper Prototype)</strong>
    <ul>
      <li>Write <code>docs/adr/0001-architecture.md</code> (Lightweight ADR format):
        <em>context, decision (monolith), status, consequences, risks, alternatives</em>.</li>
      <li>Create paper prototype walkthroughs for <strong>two end-to-end tasks</strong> (happy path + one alternative path each). Tag steps with related REQ-IDs.</li>
      <li>Update UML & README per ADR constraints and prototype findings; list what changed and which REQ-IDs are supported.</li>
    </ul>
  </li>
  <li><strong>Week 4 (Inclusivity & Project Skeleton)</strong>
    <ul>
      <li>Run an <strong>Inclusivity Heuristic Review</strong> on the two tasks:
        document heuristic, affected screen/step, related REQ-ID, severity, proposed fix, plus 2–4 annotated screenshots.</li>
      <li>Submit a <strong>prioritized issue list</strong> (top 5) with target sprint + acceptance criteria.</li>
      <li>Commit the <strong>project skeleton</strong>:
        repo structure, package layout, stub <em>main/API</em> module, README quickstart that runs “hello” locally, and a <strong>tests/</strong> folder with one passing placeholder test.</li>
    </ul>
  </li>
</ul>

<h3>Sprint 2 (Weeks 5–7) Core Implementation, Data Structures/Algorithms, Quality & Feature PR</h3>
<ul>
  <li><strong>Week 5 (Data Structures & Benchmarks)</strong>
    <ul>
      <li>Create <code>ds/</code> with <em>DynamicArray, Stack, RingBufferQueue, HashSet</em> APIs.</li>
      <li>Add Unit Tests <code>tests/test_ds.py</code></li>
      <li>Add <code>bench/bench_ds.py</code> with timeit microbenchmarks.</li>
      <li>Write a ~500-word analysis mapping Big-O expectations to empirical results, including methods and complexities table.</li>
    </ul>
  </li>
  <li><strong>Week 6 (Algorithms & Quality Assessment)</strong>
    <ul>
      <li>Implement <em>binary search, mergesort, quicksort</em> in <code>alg/</code>; exercise at least one in the app path (e.g., sorting palette).</li>
      <li>Write a ~500-word quality assessment memo citing concrete smells/hotspots with evidence and a justified change/no-change decision.</li>
      <li>Add unit tests for algorithm paths and any hotspot discussed, with pass fail results.</li>
    </ul>
  </li>
  <li><strong>Week 7 (Ship Major Feature, PR Workflow, Debugging)</strong>
    <ul>
      <li>Implement a <strong>major feature</strong> tied to <strong>≥3 REQ-IDs</strong> (e.g., unlock logic up to 20 colors, mixing rules, and Text-To-Speech feedback).</li>
      <li>Work on a feature branch → open PR → self-review → merge.</li>
      <li>Add characterization + unit tests (include one initially failing edge case).</li>
      <li>Use <code>pdb</code> to isolate/fix one defect; document commands used and lessons learned.</li>
    </ul>
  </li>
</ul>

<p><em>Week 8 (post-sprint):</em> Final integration, passing test suite, documentation pack in <code>docs/</code>, short user guide, packaging instructions, presentation video, and a release tag.</p>

<h2 id="backlog">Personal Backlog</h2>

<table>
  <thead>
    <tr>
      <th>ID</th><th>User Story</th><th>Acceptance Criteria</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>US01</td><td>As a developer, I want to define the project’s **purpose, stakeholders, risks, and success criteria**, so that I have a clear charter for my project.</td><td>
      A 500-word Project Charter exists in README.md and covers all four required sections.</td></tr>
    <tr><td>US02</td><td>As a developer, I want to **create an SRS (scope, requirements, and traceability)** so that all future work is tied to testable REQ-IDs.</td><td>
      SRS (750–1000 words) includes numbered REQ-IDs, class + sequence diagrams, and traceability table.</td></tr>
    <tr><td>US03</td><td>As a developer, I want to **choose an architecture (monolith or microservice)** and document it, so that implementation is consistent and justified for a solo project.</td><td>
      ADR created in `/docs/adr/0001-architecture.md` following lightweight ADR format with context, decision, consequences, and rationale.</td></tr>
    <tr><td>US04</td><td>As a developer, I want to **prototype the main user flow** (mixing two colors and hearing a sound), so that I can validate usability before coding.</td><td>
      Two paper prototype walkthroughs (each with an alternative path) included in README, tagged to REQ-IDs.</td></tr>
    <tr><td>US05</td><td>As a developer, I want to **evaluate inclusivity and accessibility** of my UI flows, so that the app is usable for all toddlers.</td><td>
      Inclusivity heuristic review documented with REQ-IDs, severity, proposed fixes, and annotated screenshots.</td></tr>
    <tr><td>US06</td><td>As a developer, I want to **establish a working project skeleton** (repo, packages, “hello world” endpoint, and passing test), so that I have a base to build upon.</td><td>
      Directory structure created with FastAPI `main.py`, test placeholder passes, quickstart instructions verified.</td></tr>
    <tr><td>US07</td><td>As a user, I want to see 3 base colors so I can start mixing.I want to hear a color’s name on tap/click.</td><td>
      On load, 3 color spheres appear; each clickable; clicking any sphere triggers correct audio output.</td></tr>
    <tr><td>US08</td><td>As a user, I want to drag exactly two colors into a bowl to mix. I want to be able to move a color out of the bowl.</td><td>
      UI drag-drop works with exactly two inputs; third color blocked.</td></tr>
    <tr><td>US09</td><td>As a user, I want to **see and hear the name of the mixed color**, so that I can connect color and language learning.</td><td>
      API returns hex + name; new sphere displays in bowl.</td></tr>
    <tr><td>US10</td><td>As a user, I want to **unlock and save new colors** (up to 20 total) so that I can expand my palette.</td><td>
      SQLite session stores unlocked colors; capped at 20;</td></tr>
    <tr><td>US11</td><td>As a user, I want to **reset the mixing area** so that I can start a new mix anytime.I want to **reset the color palette** so that I can "discover" colors again.</td><td>
      “Clear” button resets UI and re-enables drag-drop; "Clear Palette" button reset the color palette to the basic colors.</td></tr>
    <tr><td>US12</td><td>As a developer, I want to **analyze and benchmark data structures** (DynamicArray, Stack, Queue, HashSet), so I can choose efficient tools for my app.</td><td>
      DS package implemented with tests and timeit benchmarks; analysis report (~500 words) included.</td></tr>
    <tr><td>US13</td><td>As a developer, I want to **implement core algorithms** (binary search, mergesort, quicksort), so that I can sort or search within my color data efficiently.</td><td>
      Algorithms coded in `alg/` package; at least one used in app; tested and documented in quality memo.</td></tr>
    <tr><td>US14</td><td>As a developer, I want to **perform a quality assessment and refactor if needed**, so that the final codebase is maintainable and evidence-based.</td><td>
      500-word memo with smells/hotspots evidence; either change or defend no change; all tests passing.</td></tr>
    <tr><td>US15</td><td>As a developer, I want to **add a major feature tied to ≥3 REQ-IDs** and merge it through a full PR workflow, so that my app grows incrementally and professionally.</td><td>
      Major feature branch → PR → review → merge; feature implements at least 3 REQ-IDs; self-review note included.</td></tr>
    <tr><td>US16</td><td>As a developer, I want to **debug one real issue using `pdb`**, so I can practice professional debugging techniques.</td><td>
      Short note included with commands and lesson learned.</td></tr>
    <tr><td>US17</td><td>As a developer, I want to **assemble final documentation, tests, and presentation**, so that my final submission meets all Week 8 deliverables.</td><td>
      Final docs (SRS, UML, ADR, inclusivity review, DS/alg results, user guide, and 5-min video) committed and release tagged.</td></tr>
  </tbody>
</table>


