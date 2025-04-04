document
  .getElementById("prompt-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const prompt = document.getElementById("prompt").value;
    const numImages = document.getElementById("num-images").value;
    const status = document.getElementById("status");
    const imagesDiv = document.getElementById("images");

    status.textContent = "Generating content...";
    imagesDiv.innerHTML = ""; // Clear previous images

    try {
      const response = await fetch("http://localhost:5500/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
          numImages: parseInt(numImages),
        }),
      });

      if (!response.ok) throw new Error("Failed to generate content");

      const data = await response.json();
      data.imageUrls.forEach((url) => {
        const img = document.createElement("img");
        img.src = url;
        imagesDiv.appendChild(img);
      });
      status.textContent = "Content generated successfully!";
    } catch (error) {
      console.error("Error:", error);
      status.textContent = "Error generating content. Please try again.";
    }
  });
