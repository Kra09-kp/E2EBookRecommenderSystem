let books = [];  // global books list
let loadingInterval = null;


function showLoading(messages) {
  const modalElement = document.getElementById('loadingModal');
  const loadingMsg = document.getElementById('loadingMsg');
  
  // Stop previous interval
  if (loadingInterval) clearInterval(loadingInterval);
  
  let index = 0;
  loadingMsg.innerText = messages[index];

  // Show modal
  if (!window._loadingModal) {
    window._loadingModal = new bootstrap.Modal(modalElement, {backdrop: 'static', keyboard: false});
  }
  window._loadingModal.show();

  // Only rotate if multiple messages
  if (messages.length > 1) {
    loadingInterval = setInterval(() => {
      index = (index + 1) % messages.length;
      loadingMsg.innerText = messages[index];
    }, 5000);
  } else {
    loadingInterval = null; // single message, no rotation
  }
}

function hideLoading() {
  // Stop interval
  if (loadingInterval) {
    clearInterval(loadingInterval);
    loadingInterval = null;
  }

  // Hide modal
  if (window._loadingModal) {
    window._loadingModal.hide();
  }
}


// Fetch books once from backend
async function fetchBooks() {
  try {
    const res = await fetch("/books");
    const data = await res.json();
    console.log("Books fetch response:", data.books ? data.books.length : data);
    if (data.books && data.books.length > 0) {
      books = data.books;
    } else {
      console.warn("Model not trained. Please train the model first.");
      showLoading(["First, You need to train the Model:)"]);
      setTimeout(hideLoading, 2000);
    }

  } catch (err) {
    console.error("Error fetching books:", err);
    showLoading(["⚠️ Failed to fetch books. Please check backend."]);
    setTimeout(hideLoading, 2000);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  await fetchBooks(); // Load books at page start

  const bookInput = document.getElementById("bookInput");
  const suggestions = document.getElementById("suggestions");

  let currentIndex = -1; // Track which suggestion is active

  bookInput.addEventListener("input", () => {
    const query = bookInput.value.toLowerCase();
    suggestions.innerHTML = "";
    currentIndex = -1;

    if (!query || books.length === 0) return;

    const filtered = books.filter(book =>
      book.toLowerCase().includes(query)
    ).slice(0, 7);

    if (filtered.length === 0) return;

    filtered.forEach(book => {
      const li = document.createElement("li");
      li.classList.add("list-group-item", "list-group-item-action");
      li.textContent = book;

      li.addEventListener("click", () => {
        bookInput.value = book;
        suggestions.innerHTML = "";
        fetchRecommendations(book);
      });

      suggestions.appendChild(li);
    });
  });

  // Keyboard navigation
  bookInput.addEventListener("keydown", (e) => {
    const items = suggestions.querySelectorAll("li");
    if (items.length === 0) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      currentIndex = (currentIndex + 1) % items.length;
      updateActive(items);
    } 
    else if (e.key === "ArrowUp") {
      e.preventDefault();
      currentIndex = (currentIndex - 1 + items.length) % items.length;
      updateActive(items);
    } 
    else if (e.key === "Enter") {
      e.preventDefault();
      if (currentIndex >= 0) {
        const selected = items[currentIndex];
        bookInput.value = selected.textContent;
        suggestions.innerHTML = "";
        fetchRecommendations(selected.textContent);
      }
    }
  });
function updateActive(items) {
  items.forEach((item, idx) => {
    if (idx === currentIndex) {
      item.classList.add("active-suggestion");
      item.scrollIntoView({ block: "nearest" }); // Auto-scroll if needed
    } else {
      item.classList.remove("active-suggestion");
    }
  });
  }
});


const steps = [
  "Data Ingestion",
  "Data Validation",
  "Data Transformation",
  "Model Training",
];

async function startTraining() {
  // Show pipeline
  document.getElementById("pipelineContainer").classList.remove("d-none");
  const msgBox = document.getElementById("trainingMessage");
  const eventSource = new EventSource("/train-stream");

  let manuallyClosed = false; // Track if we closed the connection
  eventSource.onmessage = async function (event) {
    const msg = event.data;
    console.log("SSE message:", msg);
    // Update steps based on message
    steps.forEach((step, idx) => {
      const stepEl = document.querySelector(`.pipeline-step[data-step="${idx}"]`);

      if (!stepEl) return;

      if (msg.includes(step + " started")) {
        msgBox.classList.remove("show", "error");
        msgBox.classList.add("d-none");
        stepEl.classList.add("active");
        stepEl.classList.remove("completed", "error");
        stepEl.querySelector(".circle").innerHTML = "*";
      }
      if (msg.includes(step + " completed")) {
        stepEl.classList.remove("active", "error");
        stepEl.classList.add("completed");
        stepEl.querySelector(".circle").innerHTML ='<i class="bi bi-check-lg"></i>';
      }
      if (msg.includes(step + " failed")) {
        console.log("Error message:", msg);
        stepEl.classList.remove("active");
        stepEl.classList.add("error");
        stepEl.querySelector(".circle").innerHTML = '<i class="bi bi-x-lg"></i>';
        manuallyClosed = true;
        eventSource.close();
        // Show error message
        msgBox.textContent = "❌ Training failed! Please try again.";
        msgBox.classList.remove("d-none", "success");
        msgBox.classList.add("error", "show");

      }
    });

    if (msg.includes("Training completed")) {
      // console.log("SSE message:", msg);
      manuallyClosed = true;
      eventSource.close();
      await fetchBooks(); // Refresh books after training
      // remove the pipeline container
      
      // Show success message
      msgBox.textContent = "✅ Training completed! Now you can do prediction.";
      msgBox.classList.remove("d-none", "error");
      msgBox.classList.add("success", "show");

      // Hide pipeline after short delay
      setTimeout(() => {
        document.getElementById("pipelineContainer").classList.add("d-none");
      }, 3000);
    }
  };
    
  eventSource.onerror = (err) => {
  if (manuallyClosed) {
    console.log("SSE closed intentionally.");
    return;
  }
    console.error("SSE failed:", err);
    eventSource.close();
    msgBox.textContent = "⚠️ Connection lost. Please try again.";
    msgBox.classList.remove("d-none", "success");
    msgBox.classList.add("error", "show");
};
}

/* --------- fetch & display recommendations (example) --------- */

  // Fetch top 5 recommendations
// Fetch recommendations when a book is selected
async function fetchRecommendations(book) {
  try {
    const msgBox = document.getElementById("trainingMessage");
    msgBox.classList.add("show");
    msgBox.textContent = "Fetching recommendations...";
    msgBox.classList.remove("d-none");
    msgBox.classList.add("success", "show");
    const res = await fetch(`/recommend?book=${encodeURIComponent(book)}`);
    const data = await res.json();
    console.log("Recommendations:", data);
    msgBox.classList.remove("show");
    msgBox.classList.add("d-none");

    // Display recommendations
    const recommendationsDiv = document.getElementById("recommendations");
    recommendationsDiv.innerHTML = " <div><h5>Here is the Recommended Books: </h5></div>";

    data["recommendations"].forEach(item => {
      const col = document.createElement("div");
      col.classList.add("col-md-3", "mb-4");

      col.innerHTML = `
     
      <div class="card shadow-lg border-0 h-100 rounded-4 overflow-hidden recommendation-card">
        <div class="img-container position-relative">
          <img src="${item.poster}" class="card-img-top" alt="${item.title}">
          <div class="overlay">
            <div class="overlay-text">${item.title}</div>
          </div>
        </div>
      </div>`;


      recommendationsDiv.appendChild(col);
    });
  } catch (err) {
    console.error("Error fetching recommendations:", err);
  }
}
