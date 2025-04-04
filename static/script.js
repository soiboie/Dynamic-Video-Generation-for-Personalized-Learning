document
  .getElementById("prompt-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    
    // Get form values
    const prompt = document.getElementById("prompt").value;
    const numImages = document.getElementById("num-images").value;
    const status = document.getElementById("status");
    const imagesDiv = document.getElementById("images");

    // Update status
    status.textContent = "Generating content...";
    imagesDiv.innerHTML = ""; // Clear previous images
    
    console.log("Sending request with prompt:", prompt, "and numImages:", numImages);

    try {
      // Use relative URL to avoid CORS issues
      const response = await fetch("/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
          numImages: parseInt(numImages),
        }),
      });

      console.log("Response status:", response.status);
      
      // Better error handling
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server error:", errorText);
        throw new Error(`Failed to generate content: ${response.status} ${errorText}`);
      }

      // Parse JSON response safely
      const data = await response.json();
      console.log("Received data:", data);
      
      if (data.imageUrls && data.imageUrls.length > 0) {
        data.imageUrls.forEach((url) => {
          const img = document.createElement("img");
          img.src = url;
          img.className = "generated-image";
          img.alt = "AI generated image for: " + prompt;
          imagesDiv.appendChild(img);
        });
        status.textContent = "Content generated successfully!";
      } else {
        throw new Error("No images were returned from the server");
      }
    } catch (error) {
      console.error("Detailed error:", error);
      status.textContent = "Error generating content: " + error.message;
    }
  });
