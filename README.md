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



##Project Plan
###Sprint 1 (Weeks 2-4)

###Sprint 2 (Weeks 5-7)


##Personal Backlog  - User Stories
