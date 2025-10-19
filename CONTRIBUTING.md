<!-- CONTRIBUTING.md -->
<div align="center">
  <h1>Contributing to MasterColorMixer</h1>
  <p><em>Guidelines for commits, branches, and pull requests.</em></p>
</div>

<h2>Branch Policy</h2>
<p>
  This project uses a <strong>lightweight branching strategy</strong> modeled after professional Git workflows to ensure clarity and maintainability, even in a solo development environment.
</p>
<ul>
  <li><code>main</code> — The <strong>stable release branch</strong>. Only code that is tested, documented, and ready for review or submission is merged here. </li>
  <li><code>dev</code> — The <strong>active development branch</strong>. All new features, fixes, and experiments branch off from <code>dev</code>.</li>
  <li><strong>Feature branches</strong> follow the naming convention:
    <br/>
    <code>feature/&lt;short-description&gt;</code> (e.g., <code>feature/color-audio</code> or <code>feature/mixing-logic</code>)
  </li>
  <li><strong>Fix branches</strong> follow the naming convention:
    <br/>
    <code>fix/&lt;issue-or-bug-description&gt;</code> (e.g., <code>fix/ui-drag-drop</code>)
  </li>
  <li>After work is completed on a feature branch, open a Pull Request (PR) into <code>dev</code> for review. Once validated and tested, merge <code>dev</code> into <code>main</code> for final release tagging.</li>
</ul>

<h2>Commit Message Conventions</h2>
<p>
  All commits should follow a consistent convention to make the project history easy to navigate and understand. Each commit message should be desriptive and detailed
</p>
<p>Examples:</p>
<pre><code>feature UI - add drag-and-drop color mixing
bugfix API - correct POST /mix response for invalid input
documentation README - update SRS and traceability sections
tests MIXING - add unit test for two-color combination
</code></pre>
<p>
  <strong>Types</strong> may include:
  <code>feature</code>, <code>bugfix</code>, <code>documentation</code>, <code>tests</code>, <code>refactor</code>, <code>style</code>, <code>chore</code>.
</p>

<h2>Pull Request (PR) Conventions</h2>
<p>Each PR should represent a complete, testable unit of work and include clear documentation of its purpose and scope (in the form of a User Story).</p>
<ul>
  <li>PR titles should include the User Story ID and a brief description of the work. <code>US09 - feature add sound effects for color names</code>.</li>
  <li>Before submitting a PR:
    <ul>
      <li>Run all tests locally with <code>pytest</code>.</li>
      <li>Ensure <code>README.md</code> and/or <code>SRS</code> are updated if behavior or requirements changed.</li>
      <li>Verify that any new REQ-IDs are mapped in the traceability table.</li>
    </ul>
  </li>
  <li>Include a concise description of:
    <ul>
      <li>What was added or fixed</li>
      <li>Relevant REQ-IDs or user stories</li>
      <li>Testing steps or screenshots for QA (if applicable)</li>
    </ul>
  </li>
  <li>Each PR should close or reference a User Stort or issue (when applicable):  
  <li>After merging to dev, squash commits and delete the feature branch to keep the repo clean.</li>
</ul>

<h2>Testing & Quality Assurance</h2>
<ul>
  <li>All new code must include unit tests in the <code>tests/</code> directory.</li>
  <li>Each test file should target a single module or function.</li>
  <li>Maintain ≥80% test coverage for critical logic.</li>
  <li>Run all tests before committing</li>
  <li>Perform manual tests of the UI for every major feature change.</li>
</ul>

<h2>Code Style & Documentation</h2>
<ul>
  <li>Use meaningful variable names; avoid unnecessary abbreviations.</li>
  <li>Document new endpoints in <code>README.md</code> or <code>docs/</code> as they are introduced.</li>
</ul>

<h2>Merge Process Summary</h2>
<ol>
  <li>Create or update an issue for the planned change.</li>
  <li>Branch from <code>dev</code> using the correct naming convention.</li>
  <li>Commit frequently using standardized messages.</li>
  <li>Open a PR into <code>dev</code> with clear description, test results, and screenshots if needed.</li>
  <li>Review your own PR (solo review checklist): code clarity, style, testing, and documentation updates.</li>
  <li>Merge to <code>dev</code> after verification.</li>
  <li>After stable testing and documentation pass, merge <code>dev</code> → <code>main</code> for release tagging.</li>
</ol>


<h2>Solo Review Checklist</h2>
<p>Before merging any branch, confirm that:</p>
<ul>
  <li>All unit tests pass.</li>
  <li>Functionality matches acceptance criteria from the linked user story.</li>
  <li>Documentation and diagrams are updated if architecture changed.</li>
  <li>No debug prints, commented-out code, or temporary files remain.</li>
</ul>

<hr/>
<p align="center">
  <em>“Commit early and often, perform itterative testing, always update documention.”</em><br/>
  — <strong>MasterColorMixer Project Guidelines</strong>
</p>
