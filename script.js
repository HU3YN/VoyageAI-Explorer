// script.js
// ============================================
// MOCK API FOR GITHUB PAGES
// ============================================
console.log('🔧 Running on GitHub Pages - Using mock API');

// Check if we're on GitHub Pages
const isGitHubPages = window.location.hostname.includes('github.io');

// Mock API function for GitHub Pages
async function mockTravelAPI(destination, days, budget, interests) {
    console.log('📡 Mock API called with:', { destination, days, budget, interests });
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Return mock travel plan
    return {
        success: true,
        plan: {
            destination: destination,
            duration: `${days} days`,
            budget: `$${budget}`,
            summary: `AI-generated ${days}-day trip to ${destination} with ${interests.join(', ')} activities.`,
            itinerary: generateMockItinerary(destination, days, interests),
            recommendations: [
                `Visit the main attractions in ${destination}`,
                `Try local cuisine within your $${budget} budget`,
                `Explore ${interests.join(' and ')}-related activities`
            ],
            tips: [
                "Book accommodations in advance",
                "Check local weather forecasts",
                "Carry local currency for small purchases"
            ]
        }
    };
}

function generateMockItinerary(destination, days, interests) {
    const itinerary = [];
    for (let i = 1; i <= days; i++) {
        itinerary.push({
            day: i,
            title: `Day ${i}: ${destination} Exploration`,
            activities: [
                `Morning: ${interests[0] || 'Sightseeing'} tour`,
                `Afternoon: Local cuisine experience`,
                `Evening: ${interests[1] || 'Cultural'} activities`
            ]
        });
    }
    return itinerary;
}

// ============================================
// MAIN APPLICATION CODE (YOUR EXISTING CODE)
// ============================================
// ... your existing code continues below ...
document.getElementById("planTripButton").addEventListener("click", async () => {
    const userInput = document.getElementById("userInput").value.trim();
    const totalDays = parseInt(document.getElementById("daysInput").value) || 3;

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p class='loading'>🌍 Planning your perfect trip...</p>";

    // Validate input
    if (!userInput) {
        resultsDiv.innerHTML = "<p class='error'>⚠️ Please tell us about your interests first!</p>";
        return;
    }

    if (totalDays < 1 || totalDays > 30) {
        resultsDiv.innerHTML = "<p class='error'>⚠️ Please choose between 1 and 30 days.</p>";
        return;
    }

    try {
        const response = await fetch("/plan-trip", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_input: userInput, days: totalDays })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            resultsDiv.innerHTML = `<p class='error'>⚠️ ${data.error}</p>`;
            return;
        }

        const itinerary = data.itinerary || [];
        const matched_interests = data.matched_interests || [];
        const activity_interest_map = data.activity_interest_map || [];

        resultsDiv.innerHTML = "";

        if (itinerary.length === 0) {
            resultsDiv.innerHTML = "<p class='error'>😕 No destinations found. Try different interests like 'beaches', 'food', 'hiking', or 'culture'.</p>";
            return;
        }

        // Calculate total cities and region changes
        const numCities = itinerary.length;
        let currentRegion = null;
        let regionChanges = 0;
        
        itinerary.forEach((city, idx) => {
            const region = city.region || 'Other';
            if (idx > 0 && region !== currentRegion && currentRegion !== null) {
                regionChanges++;
            }
            currentRegion = region;
        });
        
        // Add a summary header
        const summaryHTML = `
            <div class="trip-summary">
                <h2>Your ${totalDays}-Day Adventure</h2>
                <p>Visiting <strong>${numCities} amazing ${numCities === 1 ? 'destination' : 'destinations'}</strong> based on your interests: <strong>${userInput}</strong></p>
                ${regionChanges > 0 ? `<p class="route-info">✈️ Optimized route with ${regionChanges} ${regionChanges === 1 ? 'region change' : 'region changes'} to minimize travel</p>` : ''}
                <div class="trip-stats">
                    <div class="stat">
                        <div class="stat-value">${totalDays}</div>
                        <div class="stat-label">Days</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${numCities}</div>
                        <div class="stat-label">${numCities === 1 ? 'City' : 'Cities'}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${itinerary.reduce((sum, city) => sum + (city.activities?.length || 0), 0)}</div>
                        <div class="stat-label">Activities</div>
                    </div>
                </div>
            </div>
        `;
        resultsDiv.innerHTML += summaryHTML;

        // Display timeline with region headers
        let currentDay = 1;
        let lastRegion = null;
        
        itinerary.forEach((city, idx) => {
            const cityDays = city.days || 1;
            const startDay = currentDay;
            const endDay = currentDay + cityDays - 1;
            currentDay = endDay + 1;

            const matchPercentage = city.score || 0;
            const cityMatchedInterests = matched_interests[idx] || [];
            const activityMap = activity_interest_map[idx] || {};

            const matchColor = getMatchColor(matchPercentage);
            
            // Check if we're entering a new region
            const currentRegion = city.region || 'Other';
            let regionHeaderHTML = '';
            
            if (currentRegion !== lastRegion && currentRegion !== 'Other') {
                regionHeaderHTML = `
                    <div class="region-header">
                        <div class="region-icon">🌍</div>
                        <div class="region-name">${currentRegion}</div>
                    </div>
                `;
                lastRegion = currentRegion;
            }
            
            // Create activity list with AI-matched interests
            const activitiesHTML = city.activities.map(activity => {
                const matchedForActivity = activityMap[activity] || [];
                if (matchedForActivity.length > 0) {
                    const badges = matchedForActivity.map(interest => 
                        `<span class="activity-badge">${interest}</span>`
                    ).join(" ");
                    return `<li class="matched-activity">
                        ${activity} 
                        <div class="activity-matches">${badges}</div>
                    </li>`;
                }
                return `<li>${activity}</li>`;
            }).join("");

            const interestBadges = cityMatchedInterests.length > 0 
                ? cityMatchedInterests.map(i => `<span class="badge">${i}</span>`).join(" ")
                : '<span class="badge no-match">Popular destination</span>';

            // Format day range
            const dayRange = cityDays === 1 
                ? `Day ${startDay}` 
                : `Days ${startDay}-${endDay}`;
            
            const dayInfo = cityDays === 1 
                ? '1 day' 
                : `${cityDays} days`;

            const cityHTML = `
                ${regionHeaderHTML}
                <div class="day-card">
                    <div class="day-header">
                        <div class="day-info-group">
                            <div class="day-number">${dayRange}</div>
                            <div class="duration-badge">${dayInfo}</div>
                        </div>
                        <div class="match-score" style="background-color: ${matchColor}">
                            ${matchPercentage}% match
                        </div>
                    </div>
                    
                    <h3 class="destination-name">
                        ${city.destination}, ${city.country}
                    </h3>
                    
                    <p class="description">${city.description}</p>
                    
                    <div class="interests-section">
                        <strong>Why this destination:</strong>
                        <div class="interest-badges">${interestBadges}</div>
                    </div>
                    
                    <div class="activities-section">
                        <strong>Things to do (${city.activities.length} activities):</strong>
                        <ul class="activities-list">${activitiesHTML}</ul>
                    </div>
                    
                    ${cityDays > 1 && city.itinerary_suggestion ? `
                        <div class="itinerary-suggestion">
                            <strong>Suggested Itinerary:</strong>
                            <p>${city.itinerary_suggestion.replace(/\*/g, '').trim()}</p>
                        </div>
                    ` : ''}
                </div>
            `;
            resultsDiv.innerHTML += cityHTML;
        });

        // Add travel tips
        const tipsHTML = `
            <div class="trip-tips">
                <h3>💡 Travel Tips</h3>
                <ul>
                    <li><strong>Day Distribution:</strong> ${totalDays <= 3 ? 'Short trips focus on one destination per day for deeper exploration' : totalDays <= 7 ? 'We recommend 2-3 days per city to really experience each destination' : totalDays <= 14 ? 'Spending 3-4 days per city gives you time to explore like a local' : 'Longer stays (4-5 days) let you discover hidden gems and enjoy a relaxed pace'}</li>
                    <li><strong>Highlighted Activities:</strong> Activities with badges specifically match your interests based on AI analysis</li>
                    <li><strong>Geographic Routing:</strong> Cities are grouped by region to minimize long-haul flights and maximize your time exploring</li>
                    <li><strong>Book in Advance:</strong> Reserve accommodations and popular attractions early, especially during peak seasons</li>
                    <li><strong>Local Transportation:</strong> Research transit options between cities and within each destination</li>
                </ul>
            </div>
        `;
        resultsDiv.innerHTML += tipsHTML;

    } catch (error) {
        resultsDiv.innerHTML = `<p class='error'>❌ Error planning trip: ${error.message}. Please try again.</p>`;
        console.error("Error:", error);
    }
});

// Helper function to get color based on match percentage
function getMatchColor(percentage) {
    if (percentage >= 80) return "#4CAF50"; // Green - Excellent match
    if (percentage >= 60) return "#8BC34A"; // Light green - Good match
    if (percentage >= 40) return "#FFC107"; // Yellow - Moderate match
    if (percentage >= 20) return "#FF9800"; // Orange - Fair match
    return "#FF5722"; // Red - Low match
}

// Add Enter key support
document.getElementById("userInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        document.getElementById("planTripButton").click();
    }

});
