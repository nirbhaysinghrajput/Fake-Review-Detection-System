
/**
 * script.js — Fake Review Detection System
 * Includes anonymous Google Analytics event tracking.
 */

document.addEventListener("DOMContentLoaded", () => {

  // ─── Analytics Helper ──────────────────────────────────────
  function trackEvent(eventName, parameters = {}) {
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, parameters);
    }
  }

  // ─── DOM Elements ──────────────────────────────────────────
  const reviewInput        = document.getElementById("reviewInput");
  const detectBtn          = document.getElementById("detectBtn");
  const detectBtnText      = document.getElementById("detectBtnText");
  const detectSpinner      = document.getElementById("detectSpinner");
  const clearBtn           = document.getElementById("clearBtn");
  const charCount          = document.getElementById("charCount");
  const errorMsg           = document.getElementById("errorMsg");
  const resultSection      = document.getElementById("resultSection");
  const analyzeAnotherBtn  = document.getElementById("analyzeAnotherBtn");

  // Result display elements
  const reviewedTextDisplay = document.getElementById("reviewedTextDisplay");
  const verdictBadge       = document.getElementById("verdictBadge");
  const verdictText        = document.getElementById("verdictText");
  const confidencePercent  = document.getElementById("confidencePercent");
  const confidenceBar      = document.getElementById("confidenceBar");
  const fakeProb           = document.getElementById("fakeProb");
  const genuineProb        = document.getElementById("genuineProb");
  const reasonsTitle       = document.getElementById("reasonsTitle");
  const patternsList       = document.getElementById("patternsList");

  // Example pills
  const examplePills       = document.querySelectorAll(".example-pill");

  // About modal dialog
  const aboutDialog        = document.getElementById("aboutDialog");
  const openAboutBtn       = document.getElementById("openAboutBtn");
  const closeAboutBtn      = document.getElementById("closeAboutBtn");
  const dialogOkBtn        = document.getElementById("dialogOkBtn");

  // ─── Character Counter ─────────────────────────────────────
  function updateCharCount() {
    const len = reviewInput.value.length;
    charCount.textContent = `${len.toLocaleString()} / 2,000`;
    charCount.style.color = len >= 1900 ? "#dc2626" : "";
  }

  reviewInput.addEventListener("input", () => {
    updateCharCount();
    if (errorMsg.hidden === false) {
      hideError();
    }
  });

  // ─── Clear Button ──────────────────────────────────────────
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      reviewInput.value = "";
      updateCharCount();
      hideError();
      reviewInput.focus();
    });
  }

  // ─── Example Pills ─────────────────────────────────────────
  examplePills.forEach(pill => {
    pill.addEventListener("click", () => {

      // Track example selection
      trackEvent("example_clicked");

      const text = pill.getAttribute("data-review");
      if (text) {
        reviewInput.value = text;
        updateCharCount();
        hideError();
        reviewInput.scrollIntoView({ behavior: "smooth", block: "center" });
        reviewInput.focus();
      }
    });
  });

  // ─── Detect Button / Submission ────────────────────────────
  detectBtn.addEventListener("click", async () => {
    const reviewText = reviewInput.value.trim();

    // Client-side validation
    if (!reviewText) {
      showError("Please enter a review before analyzing.");
      reviewInput.focus();
      return;
    }

    const wordCount = reviewText.split(/\s+/).filter(Boolean).length;
    if (wordCount < 3) {
      showError("Please enter at least 3 words for meaningful analysis.");
      reviewInput.focus();
      return;
    }

    hideError();
    setLoading(true);

    // Track valid review submission
    trackEvent("review_submitted");

    // Measure analysis duration
    const analysisStartTime = Date.now();

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ review: reviewText }),
      });

      const data = await response.json();

      if (!response.ok) {

        // Track server/API failure
        trackEvent("analysis_failed", {
          failure_reason: "server_error",
          status_code: response.status
        });

        showError(data.error || "An error occurred while analyzing the review.");
        return;
      }

      // Track successful analysis
      trackEvent("analysis_completed", {
        prediction_type: data.prediction === "Fake Review" ? "fake" : "genuine",
        analysis_duration_ms: Date.now() - analysisStartTime
      });

      // Display results
      renderResults(reviewText, data);

    } catch (err) {

      // Track network or request failure
      trackEvent("analysis_failed", {
        failure_reason: "request_error"
      });

      showError("Could not reach the server. Please verify the application is running.");

    } finally {
      setLoading(false);
    }
  });

  // ─── Render Results ────────────────────────────────────────
  function renderResults(submittedText, data) {
    const isFake = data.prediction === "Fake Review";

    // 1. Show analyzed text
    reviewedTextDisplay.textContent = submittedText;

    // 2. Verdict badge with subtle dot
    verdictBadge.className = `verdict-tag ${isFake ? "verdict-fake" : "verdict-genuine"}`;
    verdictText.textContent = isFake ? "FAKE REVIEW" : "GENUINE REVIEW";

    // 3. Confidence meter
    const confidenceVal = Math.round(data.confidence);
    confidencePercent.textContent = `${confidenceVal}%`;

    confidenceBar.className = `progress-fill ${isFake ? "fill-fake" : "fill-genuine"}`;
    confidenceBar.style.width = "0%";
    const progressTrack = confidenceBar.parentElement;
    if (progressTrack) {
      progressTrack.setAttribute("aria-valuenow", confidenceVal);
    }

    // Smooth subtle fill animation
    requestAnimationFrame(() => {
      setTimeout(() => {
        confidenceBar.style.width = `${confidenceVal}%`;
      }, 50);
    });

    // 4. Probability breakdown
    const fakePercent = (data.fake_probability * 100).toFixed(1);
    const genuinePercent = (data.genuine_probability * 100).toFixed(1);
    fakeProb.textContent = `${fakePercent}%`;
    genuineProb.textContent = `${genuinePercent}%`;

    // 5. Reasons / suspicious patterns
    patternsList.innerHTML = "";
    if (data.reasons && data.reasons.length > 0) {
      reasonsTitle.textContent = "Why this review was flagged";
      data.reasons.forEach(reason => {
        const li = document.createElement("li");
        li.textContent = reason;
        patternsList.appendChild(li);
      });
    } else {
      reasonsTitle.textContent = "Analysis notes";
      const li = document.createElement("li");
      li.className = "reasons-empty";
      li.textContent = "No major suspicious writing patterns detected.";
      patternsList.appendChild(li);
    }

    // 6. Reveal section and scroll smoothly into view
    resultSection.hidden = false;
    resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // ─── Analyze Another Review ────────────────────────────────
  analyzeAnotherBtn.addEventListener("click", () => {
    resultSection.hidden = true;
    reviewInput.value = "";
    updateCharCount();
    hideError();
    reviewInput.scrollIntoView({ behavior: "smooth", block: "center" });
    reviewInput.focus();
  });

  // ─── Helpers ───────────────────────────────────────────────
  function setLoading(loading) {
    detectBtn.disabled = loading;
    if (detectSpinner) {
      detectSpinner.hidden = !loading;
    }
    detectBtnText.textContent = loading ? "Analyzing review..." : "Detect Review";
  }

  function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.hidden = false;
  }

  function hideError() {
    errorMsg.hidden = true;
    errorMsg.textContent = "";
  }

  // ─── About Modal Handling ──────────────────────────────────
  if (aboutDialog && openAboutBtn) {
    openAboutBtn.addEventListener("click", () => {

      // Track About section usage
      trackEvent("about_opened");

      if (typeof aboutDialog.showModal === "function") {
        aboutDialog.showModal();
      } else {
        aboutDialog.setAttribute("open", "");
      }
    });

    const closeDialog = () => {
      if (typeof aboutDialog.close === "function") {
        aboutDialog.close();
      } else {
        aboutDialog.removeAttribute("open");
      }
    };

    if (closeAboutBtn) closeAboutBtn.addEventListener("click", closeDialog);
    if (dialogOkBtn) dialogOkBtn.addEventListener("click", closeDialog);

    // Close on backdrop click
    aboutDialog.addEventListener("click", (e) => {
      if (e.target === aboutDialog) {
        closeDialog();
      }
    });
  }

});
