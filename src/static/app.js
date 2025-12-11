// Function to fetch activities from API
async function fetchActivities() {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const messageDiv = document.getElementById("message");

  try {
    const response = await fetch("/activities");
    const activities = await response.json();

    // Clear loading message
    activitiesList.innerHTML = "";
    // Reset activity select options (keep placeholder)
    activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

    // Populate activities list
    Object.entries(activities).forEach(([name, details]) => {
      const activityCard = document.createElement("div");
      activityCard.className = "activity-card";

      const spotsLeft = details.max_participants - details.participants.length;

      const title = document.createElement("h4");
      title.textContent = name;

      const desc = document.createElement("p");
      desc.textContent = details.description;

      const schedule = document.createElement("p");
      schedule.innerHTML = `<strong>Schedule:</strong> ${details.schedule}`;

      const availability = document.createElement("p");
      availability.innerHTML = `<strong>Availability:</strong> ${spotsLeft} spots left`;

      const participantsSection = document.createElement("div");
      participantsSection.className = "participants-section";
      participantsSection.innerHTML = `<strong>Participants:</strong>`;

      const ul = document.createElement("ul");
      ul.className = "participants-list";

      if (details.participants.length === 0) {
        const li = document.createElement("li");
        li.innerHTML = '<em>No participants yet</em>';
        ul.appendChild(li);
      } else {
        details.participants.forEach((p) => {
          const li = document.createElement("li");

          const span = document.createElement("span");
          span.className = "participant-email";
          span.textContent = p;

          const btn = document.createElement("button");
          btn.className = "delete-btn";
          btn.type = "button";
          btn.title = "Unregister";
          btn.textContent = "✖";
          btn.dataset.activity = name;
          btn.dataset.email = p;

          // Click handler for unregister
          btn.addEventListener("click", async (e) => {
            e.preventDefault();
            const activityName = e.currentTarget.dataset.activity;
            const email = e.currentTarget.dataset.email;

            try {
              const res = await fetch(
                `/activities/${encodeURIComponent(activityName)}/unregister?email=${encodeURIComponent(email)}`,
                { method: "DELETE" }
              );

              const result = await res.json();

              if (res.ok) {
                messageDiv.textContent = result.message;
                messageDiv.className = "success";
                // Refresh activities list
                fetchActivities();
              } else {
                messageDiv.textContent = result.detail || "Failed to unregister";
                messageDiv.className = "error";
              }
              messageDiv.classList.remove("hidden");
              setTimeout(() => messageDiv.classList.add("hidden"), 5000);
            } catch (err) {
              messageDiv.textContent = "Failed to unregister. Please try again.";
              messageDiv.className = "error";
              messageDiv.classList.remove("hidden");
              console.error("Error unregistering:", err);
            }
          });

          li.appendChild(span);
          li.appendChild(btn);
          ul.appendChild(li);
        });
      }

      participantsSection.appendChild(ul);

      activityCard.appendChild(title);
      activityCard.appendChild(desc);
      activityCard.appendChild(schedule);
      activityCard.appendChild(availability);
      activityCard.appendChild(participantsSection);

      activitiesList.appendChild(activityCard);

      // Add option to select dropdown
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      activitySelect.appendChild(option);
    });
  } catch (error) {
    activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
    console.error("Error fetching activities:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        // Refresh activity list to show new participant
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
