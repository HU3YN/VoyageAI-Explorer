// script.js - VoyageAI Explorer
// ============================================
// COMPLETE VERSION WITH GITHUB PAGES SUPPORT
// ============================================

console.log('🚀 VoyageAI Explorer loaded');

// Check if we're on GitHub Pages
const isGitHubPages = window.location.hostname.includes('github.io');

if (isGitHubPages) {
    console.log('🌐 GitHub Pages mode: Using mock data');
    addDemoModeBanner();
}

// ============================================
// MOCK DATA GENERATORS
// ============================================

// Mock API function for GitHub Pages
async function mockTravelAPI(userInput, totalDays) {
    console.log('📡 Mock API called with:', { userInput, totalDays });
    
    // Simulate API delay (1-2 seconds)
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000));
    
    // Extract interests from user input
    const interests = extractInterestsFromInput(userInput);
    
    // Generate mock itinerary
    const itinerary = generateMockItinerary(userInput, totalDays);
    const matched_interests = [];
    const activity_interest_map = generateActivityInterestMap(itinerary, interests);
    
    // Ensure matched_interests is properly structured as an array of arrays
    itinerary.forEach((city, idx) => {
        // For each city, assign some interests - ALWAYS return an array
        const cityInterests = Array.isArray(interests) ? 
            interests.slice(0, Math.min(3, interests.length)) : 
            ['culture', 'food', 'nature'];
        
        matched_interests[idx] = cityInterests;
    });
    
    return {
        success: true,
        itinerary: itinerary,
        matched_interests: matched_interests, // Array of arrays
        activity_interest_map: activity_interest_map
    };
}

// Generate mock itinerary based on user input
function generateMockItinerary(userInput, totalDays) {
    console.log('🎭 Generating mock itinerary for:', userInput);
    
    const destinations = [
        { name: "Kyoto, Japan", region: "Asia", country: "Japan", description: "Ancient temples, gardens, and traditional tea houses" },
        { name: "Santorini, Greece", region: "Europe", country: "Greece", description: "White-washed buildings with blue domes overlooking the Aegean Sea" },
        { name: "Banff, Canada", region: "North America", country: "Canada", description: "Stunning mountain landscapes and glacial lakes" },
        { name: "Queenstown, New Zealand", region: "Oceania", country: "New Zealand", description: "Adventure capital with breathtaking scenery" },
        { name: "Marrakech, Morocco", region: "Africa", country: "Morocco", description: "Vibrant markets, palaces, and gardens" },
        { name: "Rio de Janeiro, Brazil", region: "South America", country: "Brazil", description: "Famous beaches, Carnival, and iconic landmarks" },
        { name: "Reykjavik, Iceland", region: "Europe", country: "Iceland", description: "Northern lights, geothermal pools, and waterfalls" },
        { name: "Sydney, Australia", region: "Oceania", country: "Australia", description: "Iconic opera house, beaches, and harbor" },
        { name: "Bali, Indonesia", region: "Asia", country: "Indonesia", description: "Tropical paradise with beaches, temples, and rice terraces" },
        { name: "Paris, France", region: "Europe", country: "France", description: "Romantic city of lights with world-class art and cuisine" }
    ];
    
    // Parse user input for destination hints
    const inputLower = userInput.toLowerCase();
    let selectedDestinations = [];
    
    // Try to match user input with destinations
    if (inputLower.includes('japan') || inputLower.includes('kyoto') || inputLower.includes('asia') || inputLower.includes('temple')) {
        selectedDestinations = [destinations[0], destinations[8]];
    } else if (inputLower.includes('greece') || inputLower.includes('santorini') || inputLower.includes('europe') || inputLower.includes('island')) {
        selectedDestinations = [destinations[1], destinations[6], destinations[9]];
    } else if (inputLower.includes('canada') || inputLower.includes('banff') || inputLower.includes('mountain') || inputLower.includes('hiking')) {
        selectedDestinations = [destinations[2], destinations[3]];
    } else if (inputLower.includes('beach') || inputLower.includes('coast') || inputLower.includes('ocean')) {
        selectedDestinations = [destinations[1], destinations[5], destinations[7], destinations[8]];
    } else if (inputLower.includes('adventure') || inputLower.includes('hiking') || inputLower.includes('outdoor')) {
        selectedDestinations = [destinations[2], destinations[3], destinations[6]];
    } else if (inputLower.includes('food') || inputLower.includes('cuisine') || inputLower.includes('wine')) {
        selectedDestinations = [destinations[0], destinations[4], destinations[9]];
    } else if (inputLower.includes('culture') || inputLower.includes('history') || inputLower.includes('art')) {
        selectedDestinations = [destinations[0], destinations[4], destinations[9]];
    } else {
        // Default: mix of popular destinations
        selectedDestinations = destinations.slice(0, Math.min(3, Math.ceil(totalDays / 2)));
    }
    
    // Shuffle and select destinations
    const shuffled = [...selectedDestinations].sort(() => Math.random() - 0.5);
    const finalDestinations = shuffled.slice(0, Math.min(3, Math.ceil(totalDays / 2)));
    
    // Generate itinerary days
    const itinerary = [];
    let dayCounter = 1;
    
    for (let i = 0; i < finalDestinations.length && dayCounter <= totalDays; i++) {
        const dest = finalDestinations[i];
        const daysAtDestination = Math.min(Math.max(2, Math.floor(totalDays / finalDestinations.length)), totalDays - dayCounter + 1);
        
        for (let day = 1; day <= daysAtDestination && dayCounter <= totalDays; day++) {
            itinerary.push({
                destination: dest.name,
                country: dest.country,
                region: dest.region,
                description: dest.description,
                days: daysAtDestination,
                score: Math.floor(Math.random() * 30) + 70, // 70-100% match score
                activities: generateDailyActivities(dest, day, daysAtDestination, inputLower),
                itinerary_suggestion: generateItinerarySuggestion(dest, daysAtDestination)
            });
            dayCounter++;
        }
    }
    
    return itinerary;
}

// Generate daily activities
function generateDailyActivities(destination, dayNum, totalDays, userInput) {
    const baseActivities = [
        `Explore ${destination.name.split(',')[0]} city center`,
        `Visit local markets and shops`,
        `Try traditional ${destination.country} cuisine`,
        `Guided tour of historical sites`,
        `Free time for personal exploration`,
        `Sunset viewing at popular spots`,
        `Cultural experience or workshop`,
        `Nature walk or scenic drive`,
        `Visit museums or art galleries`,
        `Relax at local cafes or parks`
    ];
    
    // Filter activities based on user interests
    let filteredActivities = [...baseActivities];
    
    if (userInput.includes('food') || userInput.includes('cuisine')) {
        filteredActivities = filteredActivities.filter(a => a.includes('cuisine') || a.includes('cafes') || a.includes('markets'));
    }
    if (userInput.includes('adventure') || userInput.includes('hiking')) {
        filteredActivities = filteredActivities.filter(a => a.includes('Nature walk') || a.includes('scenic drive'));
    }
    if (userInput.includes('culture') || userInput.includes('history')) {
        filteredActivities = filteredActivities.filter(a => a.includes('historical') || a.includes('Cultural') || a.includes('museums'));
    }
    if (userInput.includes('beach') || userInput.includes('relax')) {
        filteredActivities = filteredActivities.filter(a => a.includes('Relax') || a.includes('Sunset') || a.includes('parks'));
    }
    
    // Select 3-4 activities for the day
    const numActivities = 3 + (dayNum % 2); // 3 or 4 activities
    const selected = [];
    
    for (let i = 0; i < numActivities; i++) {
        const activityIndex = (dayNum * 7 + i) % filteredActivities.length;
        selected.push(filteredActivities[activityIndex]);
    }
    
    // Add arrival/departure notes
    if (dayNum === 1) {
        selected.unshift(`Arrival in ${destination.name} - check into accommodation`);
    }
    if (dayNum === totalDays) {
        selected.push(`Prepare for next destination departure`);
    }
    
    return selected;
}

// Generate itinerary suggestion
function generateItinerarySuggestion(destination, days) {
    const suggestions = [
        `Spend your mornings exploring cultural sites and afternoons trying local food. Evenings are perfect for walks around the city.`,
        `Balance active exploration with relaxation time. Consider splitting days between city attractions and natural surroundings.`,
        `Mix guided tours with independent exploration to get both expert insights and personal discovery time.`,
        `Start with major attractions early to avoid crowds, then explore neighborhoods at a leisurely pace.`
    ];
    return suggestions[Math.floor(Math.random() * suggestions.length)];
}

// Extract interests from user input
function extractInterestsFromInput(userInput) {
    const interests = ['culture', 'food', 'nature', 'adventure', 'beach', 'history', 'shopping', 'relaxation', 'art', 'photography'];
    const inputLower = userInput.toLowerCase();
    const matched = interests.filter(interest => inputLower.includes(interest));
    
    // If no specific interests matched, return some defaults based on common words
    if (matched.length === 0) {
        if (inputLower.includes('hiking') || inputLower.includes('mountain')) return ['adventure', 'nature'];
        if (inputLower.includes('museum') || inputLower.includes('temple')) return ['culture', 'history'];
        if (inputLower.includes('shop') || inputLower.includes('market')) return ['shopping', 'culture'];
        if (inputLower.includes('relax') || inputLower.includes('spa')) return ['relaxation', 'beach'];
        return ['culture', 'food', 'nature']; // Default interests
    }
    
    return matched.slice(0, 4); // Limit to 4 interests
}

// Generate activity-interest mapping
function generateActivityInterestMap(itinerary, interests) {
    const map = {};
    itinerary.forEach((day, index) => {
        const dayMap = {};
        if (Array.isArray(day.activities)) {
            day.activities.forEach((activity, activityIndex) => {
                if (activity) {
                    // Assign 1-2 interests to each activity
                    const numInterests = 1 + (activityIndex % 2);
                    const assignedInterests = [];
                    for (let i = 0; i < numInterests && i < interests.length; i++) {
                        assignedInterests.push(interests[(activityIndex + i) % interests.length]);
                    }
                    dayMap[activity] = [...new Set(assignedInterests)]; // Remove duplicates
                }
            });
        }
        map[index] = dayMap;
    });
    return map;
}

// Add demo mode banner
function addDemoModeBanner() {
    const banner = document.createElement('div');
    banner.id = 'demo-banner';
    banner.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 14px;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 500;
        animation: slideIn 0.5s ease-out;
    `;
    
    const keyframes = `
        @keyframes slideIn {
            from { transform: translateX(100px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    
    const styleSheet = document.createElement('style');
    styleSheet.textContent = keyframes;
    document.head.appendChild(styleSheet);
    
    banner.innerHTML = `
        <span>🌐 Demo Mode</span>
        <small style="opacity: 0.9;">Mock Data</small>
    `;
    
    // Add tooltip on hover
    banner.title = "This is a demo version. Clone the repository locally for real AI-powered trip planning.";
    
    document.body.appendChild(banner);
}

// ============================================
// MAIN APPLICATION LOGIC
// ============================================

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
        // ========== GITHUB PAGES MODE ==========
        if (isGitHubPages) {
            console.log('🌐 Using mock API for GitHub Pages');
            
            // Show demo processing message
            resultsDiv.innerHTML = "<p class='loading'>🎭 Generating demo itinerary... (GitHub Pages Mode)</p>";
            
            const mockResult = await mockTravelAPI(userInput, totalDays);
            
            // Process mock result like real API response
            const itinerary = mockResult.itinerary || [];
            const matched_interests = mockResult.matched_interests || [];
            const activity_interest_map = mockResult.activity_interest_map || {};

            resultsDiv.innerHTML = "";

            if (itinerary.length === 0) {
                resultsDiv.innerHTML = "<p class='error'>😕 No destinations found. Try different interests like 'beaches', 'food', 'hiking', or 'culture'.</p>";
                return;
            }

            displayResults(itinerary, matched_interests, activity_interest_map, totalDays, userInput);
            
            // Add demo notice
            addDemoResultsNotice();
            return;
        }
        
        // ========== LOCAL DEVELOPMENT MODE ==========
        // Original API call (only runs locally)
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
        const activity_interest_map = data.activity_interest_map || {};

        resultsDiv.innerHTML = "";

        if (itinerary.length === 0) {
            resultsDiv.innerHTML = "<p class='error'>😕 No destinations found. Try different interests like 'beaches', 'food', 'hiking', or 'culture'.</p>";
            return;
        }

        displayResults(itinerary, matched_interests, activity_interest_map, totalDays, userInput);

    } catch (error) {
        console.error('API Error:', error);
        
        // Show user-friendly error
        resultsDiv.innerHTML = `
            <div class='error'>
                <p>⚠️ ${isGitHubPages ? 'Demo mode error' : 'Connection Error'}</p>
                <p>${isGitHubPages ? 
                    'Please refresh and try again.' : 
                    'Failed to connect to server. Using demo data instead.'}</p>
            </div>
        `;
        
        // Fallback to mock data (for local errors)
        if (!isGitHubPages) {
            setTimeout(async () => {
                try {
                    const mockResult = await mockTravelAPI(userInput, totalDays);
                    resultsDiv.innerHTML = "";
                    displayResults(mockResult.itinerary, mockResult.matched_interests, 
                                 mockResult.activity_interest_map, totalDays, userInput);
                    addFallbackNotice();
                } catch (fallbackError) {
                    resultsDiv.innerHTML = `<p class='error'>❌ Both API and fallback failed. Please check your connection.</p>`;
                }
            }, 1000);
        }
    }
});

// ============================================
// DISPLAY FUNCTIONS
// ============================================

function displayResults(itinerary, matched_interests, activity_interest_map, totalDays, userInput) {
    const resultsDiv = document.getElementById("results");
    
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
                    <div class="stat-value">${itinerary.reduce((sum, city) => sum + (Array.isArray(city.activities) ? city.activities.length : 0), 0)}</div>
                    <div class="stat-label">Activities</div>
                </div>
            </div>
        </div>
    `;
    resultsDiv.innerHTML = summaryHTML;

    // Display timeline with region headers
    let currentDay = 1;
    let lastRegion = null;
    
    itinerary.forEach((city, idx) => {
        const cityDays = city.days || 1;
        const startDay = currentDay;
        const endDay = currentDay + cityDays - 1;
        currentDay = endDay + 1;

        const matchPercentage = city.score || 0;
        
        // FIXED: Always ensure cityMatchedInterests is an array
        let cityMatchedInterests = [];
        if (matched_interests && Array.isArray(matched_interests)) {
            const interestsForCity = matched_interests[idx];
            if (Array.isArray(interestsForCity)) {
                cityMatchedInterests = interestsForCity;
            } else if (interestsForCity) {
                cityMatchedInterests = [interestsForCity]; // Convert to array if it's a single value
            }
        }
        
        // If still empty, use some defaults
        if (cityMatchedInterests.length === 0) {
            cityMatchedInterests = ['culture', 'adventure', 'food'].slice(0, Math.floor(Math.random() * 3) + 1);
        }
        
        const activityMap = activity_interest_map && activity_interest_map[idx] ? activity_interest_map[idx] : {};

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
        
        // Ensure activities is an array
        const cityActivities = Array.isArray(city.activities) ? city.activities : [];
        
        // Create activity list with AI-matched interests
        const activitiesHTML = cityActivities.map((activity, activityIdx) => {
            if (!activity) return '';
            
            const matchedForActivity = activityMap[activity] || [];
            const matchedForActivityArray = Array.isArray(matchedForActivity) ? matchedForActivity : [];
            
            if (matchedForActivityArray.length > 0) {
                const badges = matchedForActivityArray.map(interest => 
                    `<span class="activity-badge">${interest}</span>`
                ).join(" ");
                return `<li class="matched-activity">
                    ${activity} 
                    <div class="activity-matches">${badges}</div>
                </li>`;
            }
            return `<li>${activity}</li>`;
        }).join("");

        // FIXED: Safe mapping for cityMatchedInterests
        const interestBadges = Array.isArray(cityMatchedInterests) && cityMatchedInterests.length > 0 
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
                    ${city.destination || 'Unnamed Destination'}, ${city.country || 'Unknown Country'}
                </h3>
                
                <p class="description">${city.description || 'No description available.'}</p>
                
                <div class="interests-section">
                    <strong>Why this destination:</strong>
                    <div class="interest-badges">${interestBadges}</div>
                </div>
                
                ${cityActivities.length > 0 ? `
                <div class="activities-section">
                    <strong>Things to do (${cityActivities.length} activities):</strong>
                    <ul class="activities-list">${activitiesHTML}</ul>
                </div>
                ` : ''}
                
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
}

// Helper function to get color based on match percentage
function getMatchColor(percentage) {
    if (percentage >= 80) return "#4CAF50"; // Green - Excellent match
    if (percentage >= 60) return "#8BC34A"; // Light green - Good match
    if (percentage >= 40) return "#FFC107"; // Yellow - Moderate match
    if (percentage >= 20) return "#FF9800"; // Orange - Fair match
    return "#FF5722"; // Red - Low match
}

// Add demo notice to results
function addDemoResultsNotice() {
    const notice = document.createElement('div');
    notice.className = 'demo-notice';
    notice.innerHTML = `
        <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 20px; margin: 30px 0; border-radius: 8px;">
            <h4 style="margin-top: 0; color: #1565c0; display: flex; align-items: center; gap: 10px;">
                🌐 GitHub Pages Demo Mode
            </h4>
            <p>This itinerary was generated with <strong>sample data</strong> for demonstration purposes.</p>
            <p>For <strong>real AI-powered travel planning with VoyageAI</strong>:</p>
            <div style="background: white; padding: 15px; border-radius: 6px; margin: 15px 0;">
                <pre style="margin: 0; font-size: 14px; overflow-x: auto;">
git clone https://github.com/HU3YN/VoyageAI-Explorer.git
cd VoyageAI-Explorer
# Set up backend server for full AI features</pre>
            </div>
            <p style="margin: 15px 0;">
                <a href="https://github.com/HU3YN/VoyageAI-Explorer" target="_blank" 
                   style="display: inline-block; background: #2196f3; color: white; 
                          padding: 10px 20px; border-radius: 5px; text-decoration: none;
                          font-weight: bold;">
                   Get Full Version on GitHub →
                </a>
            </p>
        </div>
    `;
    
    const resultsDiv = document.getElementById("results");
    if (resultsDiv) {
        resultsDiv.appendChild(notice);
    }
}

// Add fallback notice
function addFallbackNotice() {
    const notice = document.createElement('div');
    notice.innerHTML = `
        <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; 
                    margin: 20px 0; border-radius: 4px; font-size: 14px;">
            <p style="margin: 0; color: #856404;">
                ⚠️ Showing demo data (server connection failed)
            </p>
        </div>
    `;
    
    const resultsDiv = document.getElementById("results");
    if (resultsDiv) {
        resultsDiv.prepend(notice);
    }
}

// Add Enter key support
document.getElementById("userInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        document.getElementById("planTripButton").click();
    }
});

// Initialize
console.log('✅ VoyageAI Explorer ready');
