[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/lPRy1kM1)

#MasterColorMixer

Project Charter

Purpose: The MasterColorMixer project is a fun and educational color-mixing web application designed for toddlers. The application allows for young users to explore colors and their relationships by dragging and dropping colors into a bin to mix them. Users will be able to click on a color to hear its name. Users can discover new colors by mixing two colors, the new color will be heard aloud for the user. This application will help introduce basic concepts of color theory and interaction in a safe and tidy, child-friendly interface. This application also demonstrates SOLID software engineering practices using Python 3.12+, FastAPI, and a simple web UI.

Objectives:
- Provide an interactive learning experience for toddlers focused on colors.
- Demonstrate Agile and SDLC principles in a Python-based application.

Stakeholders:
- Primary Users - Toddlers ages 2-5
- Secondary Users - Parents or Teachers supervising play and/or tracking progress.
- Developer - Amanda Crotty, solo developer for this COP4504 - October 2025 course.
- Instructor -  Franklin Castillo, course facilitator providing guidance and evaluation.

Risks:
- Time constraint: balance coursework and implementation with approximately 18 hours per week.
- Scope creep: avoid adding advanced game mechanics outside of the MVP scope.
- Accesibility: Ensuring sound playback, visiaul clarity, and color contrasts are toddler appropriate.
- Dependency management: managing virtual environments and python package versions.

Success Criteria:
- The application supports all MVP features:
  -- Start the game with 3 basic colors (red, blue, yellow).
  -- Play color names aloud on click and when a new color is formed.
  -- Allow for drag-and-drop mixing of two colors as combinations are discovered.
  -- Unlock up to 20 colors as combinations are discovered.
  -- Support clear functionality to reset the mixing area.
  -- Support clear functionality to reset the game area to the basic colors without restarting the application.
- Code is modular and includes unit tests.
- Documentation is complete (README, CONTRIBUTING, SRS traceability).
- App deploys and runs locally via command:
