let books = [];  // global books list

// Fetch books once from backend
async function fetchBooks() {
  try {
    const res = await fetch("/books");
    data = await res.json();
    books = data.books; // assuming response is { books: [...] }
    console.log("Fetched books:", books.length);
  } catch (err) {
    console.error("Error fetching books:", err);
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


/* --------- fetch & display recommendations (example) --------- */   

  // Fetch top 5 recommendations
// Fetch recommendations when a book is selected
async function fetchRecommendations(book) {
  try {
    const res = await fetch(`/recommend?book=${encodeURIComponent(book)}`);
    const data = await res.json();
    console.log("Recommendations:", data);

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
      </div>
`;


      recommendationsDiv.appendChild(col);
    });
  } catch (err) {
    console.error("Error fetching recommendations:", err);
  }
}
