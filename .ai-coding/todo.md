# TODO Checklist for Conway Bio Integration

This checklist is designed to guide the integration of the lifegame package with the Conway Bio updater. **Important:** After completing each prompt, stop and create a commit using the Conventional Commits specification with a commit message ending with the line:
```
#2 integrate lifegame with conway-bio
```

## Checklist Items

### Prompt 1: Refactor Conway Bio to Use Lifegame Package
- [x] **Import Lifegame Functions:**  
- Import necessary functions from the lifegame package (load_grid_from_string, step, render_full)
- [x] **Use Lifegame Grid Format:**  
- Refactor the script to use the lifegame package's grid format and functions
- [x] **Maintain Functionality:**  
- Ensure the script still fetches, parses, evolves, and updates the GitHub bio
- [x] **Error Handling:**  
- Add appropriate error handling for all operations
- [x] **GitHub Actions Compatibility:**  
- Ensure the script works in the GitHub Actions environment
- [x] **Improve Development Environment:**  
- Set up mise to manage uv for Python environment management
- Create a .mise.toml file in the root directory
- Configure mise to automatically activate the Python environment
- [x] **Modernize Dependency Management:**  
- Convert from requirements.txt to pyproject.toml in the root
- Include all necessary dependencies in pyproject.toml
- Configure the root project to include lifegame as a development dependency
- [x] **Local Testing:**  
- Test the script locally before committing
- [ ] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #2 integrate lifegame with conway-bio
 ```

---

### Prompt 1.5: Enhance Conway Bio with Rich Rendering Options
- [ ] **Add Command-Line Arguments:**  
- Use argparse to add command-line options
- Expose rule variations (Standard Conway, Day & Night, HighLife)
- Add display mode options (full block or half block characters)
- Include grid initialization options (random, from file)
- [ ] **Add Randomization Feature:**  
- Implement a `--randomize` option that uses the day of the year
- Use modulo arithmetic to select options based on the date
- Create variety in bio updates over time
- [ ] **Add Preview Mode:**  
- Implement a `--preview` option to show evolution without updating GitHub bio
- Allow displaying multiple iterations locally
- [ ] **Ensure Backward Compatibility:**  
- Maintain default behavior matching the original script
- Ensure GitHub Actions workflow still works without changes
- [ ] **Add Documentation:**  
- Add help text to the script
- Include code comments explaining the options
- Update README.md with new features
- [ ] **Test Enhanced Features:**  
- Test the script locally with various option combinations
- [ ] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #2 integrate lifegame with conway-bio
 ```

---

### Prompt 2: Update GitHub Actions Workflow
- [ ] **Docker Configuration:**  
- Modify the workflow to use Dockerfile.lifegame as the base
- Add any additional dependencies needed for conway-bio.py
- [ ] **Workflow Steps:**  
- Update steps to ensure lifegame is properly installed
- Configure the workflow to run the refactored conway-bio.py script
- [ ] **Trigger Verification:**  
- Verify that the workflow can be triggered manually and on schedule
- [ ] **Error Handling:**  
- Add appropriate error handling and logging to the workflow
- [ ] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #2 integrate lifegame with conway-bio
 ```

---

### Prompt 3: Create a Custom Docker Image for Conway Bio
- [ ] **Create Dockerfile.conway-bio:**  
- Extend the lifegame Docker image
- Add necessary dependencies (requests, python-dotenv)
- Copy conway-bio.py into the image
- Set appropriate entrypoint
- [ ] **Update Workflow:**  
- Update GitHub Actions workflow to use the new Docker image
- [ ] **Documentation:**  
- Add build instructions to README.md
- [ ] **Local Testing:**  
- Verify the Docker image can be built and run locally
- [ ] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #2 integrate lifegame with conway-bio
 ```

---

### Prompt 4: Documentation and Testing
- [ ] **README Updates:**  
- Add section explaining how the Conway Bio updater works
- Include instructions for running locally
- Document GitHub Actions configuration
- [ ] **Test Script:**  
- Create a test script that mocks GitHub API calls
- Verify correct grid evolution
- Test error handling
- [ ] **CI/CD Integration:**  
- Update CI/CD workflow to include Conway Bio tests
- [ ] **Code Comments:**  
- Add detailed comments to conway-bio.py explaining lifegame integration
- [ ] **Commit:**  
- **Stop and create a commit** with a commit message ending with:  
 ```
 #2 integrate lifegame with conway-bio
 ```
