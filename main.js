document.addEventListener('DOMContentLoaded', () => {
    const resumeForm = document.querySelector('#resumeForm');
    const resumeInput = document.querySelector('#resumeFile');
    const roleSuggestion = document.querySelector('.role-suggestion');
    const jobMatchesContainer = document.querySelector('#jobMatches');
    const errorMessage = document.querySelector('#errorMessage');
    const successMessage = document.querySelector('#successMessage');
    const submitButton = resumeForm?.querySelector('button[type="submit"]');

    function displayError(message) {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 5000);
        } else {
            alert(message);
        }
    }

    function showSuccess(message) {
        if (successMessage) {
            successMessage.textContent = message;
            successMessage.style.display = 'block';
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 5000);
        }
    }

    function displayJobMatches(bestRole, roleScore, matches) {
        if (roleSuggestion) {
            roleSuggestion.innerHTML = `Best Role: <strong>${bestRole}</strong> (Match Score: ${roleScore}%)`;
        }

        if (jobMatchesContainer) {
            jobMatchesContainer.innerHTML = '';

            if (!matches || matches.length === 0) {
                jobMatchesContainer.innerHTML = '<p>No matching jobs found.</p>';
                return;
            }

            matches.forEach(job => {
                const jobElement = document.createElement('div');
                jobElement.classList.add('job-match');
                jobElement.innerHTML = `
                    <div class="job-title">
                        <a href="${job.url || '#'}" target="_blank">${job.title || 'Untitled Job'}</a>
                    </div>
                    <div class="job-desc">${job.description || 'No description available.'}</div>
                    <p>Company: ${job.company || 'N/A'} | Location: ${job.location || 'N/A'} | Score: ${job.score || 0}%</p>
                `;
                jobMatchesContainer.appendChild(jobElement);
            });
        }
    }

    if (resumeForm) {
        resumeForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (!resumeInput.files[0]) {
                displayError("Please upload a resume file.");
                return;
            }

            const file = resumeInput.files[0];
            if (file.type !== "application/pdf") {
                displayError("Only PDF resumes are supported.");
                return;
            }

            const formData = new FormData();
            formData.append('resumeFile', file);

            // Loading state
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Analyzing...';
            }

            // Optional timeout
            const controller = new AbortController();
            setTimeout(() => controller.abort(), 15000); // 15 seconds

            try {
                const response = await fetch('/match', {
                    method: 'POST',
                    body: formData,
                    signal: controller.signal
                });

                if (!response.ok) {
                    const text = await response.text();
                    console.error('Server response:', text);
                    throw new Error(`HTTP ${response.status}: ${text}`);
                }

                const data = await response.json();
                if (data.error) throw new Error(data.error);

                displayJobMatches(data.best_role, data.role_score, data.matches);
                showSuccess("Resume analyzed successfully!");

            } catch (error) {
                if (error.name === 'AbortError') {
                    displayError('Request timed out. Please try again.');
                } else {
                    displayError(error.message || 'Failed to analyze resume.');
                }
                console.error(error);
            } finally {
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Analyze Resume';
                }
            }
        });
    }

    if (resumeInput) {
        resumeInput.addEventListener('change', () => {
            if (roleSuggestion) roleSuggestion.innerHTML = '';
            if (jobMatchesContainer) jobMatchesContainer.innerHTML = '';
            if (errorMessage) errorMessage.style.display = 'none';
            if (successMessage) successMessage.style.display = 'none';
        });
    }
});
