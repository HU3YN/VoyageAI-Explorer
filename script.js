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
        <div style="
            background: rgba(40, 45, 70, 0.9); 
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 35px; 
            margin: 40px 0; 
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3),
                        inset 0 1px 0 rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
            animation: noticeAppear 0.8s ease-out;
        ">
            <!-- Animated border top -->
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: var(--gradient-primary);
                background-size: 200% 100%;
                animation: gradientFlow 3s linear infinite;
            "></div>
            
            <!-- Title -->
            <h4 style="
                margin-top: 0; 
                margin-bottom: 25px;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent; 
                display: flex; 
                align-items: center; 
                gap: 15px;
                font-size: 1.8rem;
                font-weight: 800;
                text-shadow: 0 5px 15px rgba(255, 107, 53, 0.2);
            ">
                <span style="font-size: 2rem;">🐳</span> 
                Setup & Run Instructions
            </h4>
            
            <!-- Intro -->
            <div style="color: var(--text-light); margin-bottom: 25px; line-height: 1.7; font-size: 1.05rem;">
                <p>This demo uses <strong style="color: var(--primary-orange);">sample data</strong>. For the <strong style="color: var(--accent-orange);">full AI-powered experience</strong>, follow these steps to run VoyageAI Explorer locally with Docker:</p>
            </div>
            
            <!-- Step 1 -->
            <div class="setup-step" style="
                background: rgba(30, 35, 60, 0.7);
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                border-left: 4px solid var(--primary-orange);
                transition: all 0.3s ease;
            ">
                <h5 style="
                    color: var(--text-dark);
                    margin-top: 0;
                    margin-bottom: 15px;
                    font-size: 1.2rem;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <span style="
                        background: var(--primary-orange);
                        color: white;
                        width: 28px;
                        height: 28px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 0.9rem;
                        font-weight: bold;
                    ">1</span>
                    Step 1 — Install Docker
                </h5>
                <p style="color: var(--text-light); margin-bottom: 15px; line-height: 1.6;">
                    Download and install Docker Desktop:
                </p>
                <div style="
                    background: rgba(20, 25, 45, 0.9);
                    padding: 15px;
                    border-radius: 8px;
                    margin: 15px 0;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                ">
                    <a href="https://www.docker.com/products/docker-desktop/" target="_blank" 
                       style="
                            color: var(--primary-orange);
                            text-decoration: none;
                            font-weight: 600;
                            display: inline-flex;
                            align-items: center;
                            gap: 8px;
                            transition: all 0.3s ease;
                       "
                       onmouseover="this.style.color='var(--accent-orange)'; this.style.gap='10px';"
                       onmouseout="this.style.color='var(--primary-orange)'; this.style.gap='8px';">
                       🌐 https://www.docker.com/products/docker-desktop/
                    </a>
                </div>
                <p style="color: var(--text-light); margin-bottom: 10px; line-height: 1.6;">
                    After installing, restart and open Docker Desktop and wait until it says:
                </p>
                <div style="
                    background: rgba(76, 175, 80, 0.1);
                    border: 1px solid rgba(76, 175, 80, 0.3);
                    color: #C8E6C9;
                    padding: 12px 15px;
                    border-radius: 6px;
                    margin: 10px 0;
                    font-family: 'Courier New', monospace;
                    font-size: 0.95rem;
                ">
                    Engine running
                </div>
                <p style="color: var(--text-light); margin-top: 15px; line-height: 1.6;">
                    Verify installation:
                </p>
                <pre style="
                    margin: 10px 0;
                    padding: 15px;
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 8px;
                    overflow-x: auto;
                    color: var(--text-light);
                    font-family: 'Courier New', monospace;
                    font-size: 0.9rem;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                ">docker --version
docker compose version</pre>
            </div>
            
            <!-- Step 2 -->
            <div class="setup-step" style="
                background: rgba(30, 35, 60, 0.7);
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                border-left: 4px solid var(--accent-orange);
                transition: all 0.3s ease;
            ">
                <h5 style="
                    color: var(--text-dark);
                    margin-top: 0;
                    margin-bottom: 15px;
                    font-size: 1.2rem;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <span style="
                        background: var(--accent-orange);
                        color: white;
                        width: 28px;
                        height: 28px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 0.9rem;
                        font-weight: bold;
                    ">2</span>
                    Step 2 — Clone the project
                </h5>
                <pre style="
                    margin: 10px 0;
                    padding: 15px;
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 8px;
                    overflow-x: auto;
                    color: var(--text-light);
                    font-family: 'Courier New', monospace;
                    font-size: 0.9rem;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                ">git clone https://github.com/HU3YN/VoyageAI-Explorer.git

cd VoyageAI-Explorer</pre>
                <p style="color: var(--text-light); margin-top: 15px; line-height: 1.6; font-size: 0.95rem;">
                    This folder is in your <code style="background: rgba(255, 255, 255, 0.1); padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace;">C:\Users\your_profile_name</code>
                </p>
            </div>
            
            <!-- Step 3 -->
            <div class="setup-step" style="
                background: rgba(30, 35, 60, 0.7);
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                border-left: 4px solid #667eea;
                transition: all 0.3s ease;
            ">
                <h5 style="
                    color: var(--text-dark);
                    margin-top: 0;
                    margin-bottom: 15px;
                    font-size: 1.2rem;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <span style="
                        background: #667eea;
                        color: white;
                        width: 28px;
                        height: 28px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 0.9rem;
                        font-weight: bold;
                    ">3</span>
                    Step 3 — Create your API key file
                </h5>
                <p style="color: var(--text-light); margin-bottom: 15px; line-height: 1.6;">
                    This project uses a <code style="background: rgba(255, 255, 255, 0.1); padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace;">.env</code> file to store secrets. If you do not have an API key the program will still work it just will not have all AI semantic search capabilities (just keyword searching).
                </p>
                <pre style="
                    margin: 10px 0;
                    padding: 15px;
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 8px;
                    overflow-x: auto;
                    color: var(--text-light);
                    font-family: 'Courier New', monospace;
                    font-size: 0.9rem;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                ">cp .env.example .env</pre>
                <p style="color: var(--text-light); margin-top: 15px; margin-bottom: 10px; line-height: 1.6;">
                    Open <code style="background: rgba(255, 255, 255, 0.1); padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace;">.env</code> and add your OpenAI API key:
                </p>
                <pre style="
                    margin: 10px 0;
                    padding: 15px;
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 8px;
                    overflow-x: auto;
                    color: var(--text-light);
                    font-family: 'Courier New', monospace;
                    font-size: 0.9rem;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                ">OPENAI_API_KEY=sk-your-api-key-here</pre>
                <div style="
                    background: rgba(255, 107, 53, 0.1);
                    border: 1px solid rgba(255, 107, 53, 0.3);
                    color: #FFD8B5;
                    padding: 12px 15px;
                    border-radius: 6px;
                    margin-top: 15px;
                    font-size: 0.95rem;
                ">
                    ⚠️ <strong>Important:</strong> Do NOT upload this file to GitHub.
                </div>
            </div>
            
            <!-- Step 4 -->
            <div class="setup-step" style="
                background: rgba(30, 35, 60, 0.7);
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                border-left: 4px solid #4CAF50;
                transition: all 0.3s ease;
            ">
                <h5 style="
                    color: var(--text-dark);
                    margin-top: 0;
                    margin-bottom: 15px;
                    font-size: 1.2rem;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <span style="
                        background: #4CAF50;
                        color: white;
                        width: 28px;
                        height: 28px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 0.9rem;
                        font-weight: bold;
                    ">4</span>
                    Step 4 — Run the app
                </h5>
                <pre style="
                    margin: 10px 0;
                    padding: 15px;
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 8px;
                    overflow-x: auto;
                    color: var(--text-light);
                    font-family: 'Courier New', monospace;
                    font-size: 0.9rem;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                ">docker compose up --build</pre>
                <p style="color: var(--text-light); margin-top: 15px; line-height: 1.6;">
                    This will take about <strong style="color: var(--accent-orange);">10-15 minutes</strong> to build.
                </p>
                <p style="color: var(--text-light); margin-top: 10px; line-height: 1.6;">
                    Docker will:
                </p>
                <ul style="color: var(--text-light); margin: 10px 0; padding-left: 20px; line-height: 1.8;">
                    <li>Create a Linux container</li>
                    <li>Install Python</li>
                    <li>Install all dependencies</li>
                    <li>Start the FastAPI server</li>
                </ul>
            </div>
            
            <!-- Step 5 -->
            <div class="setup-step" style="
                background: rgba(30, 35, 60, 0.7);
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                border-left: 4px solid #FFC107;
                transition: all 0.3s ease;
            ">
                <h5 style="
                    color: var(--text-dark);
                    margin-top: 0;
                    margin-bottom: 15px;
                    font-size: 1.2rem;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <span style="
                        background: #FFC107;
                        color: black;
                        width: 28px;
                        height: 28px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 0.9rem;
                        font-weight: bold;
                    ">5</span>
                    Step 5 — Open the app
                </h5>
                <div style="
                    background: rgba(255, 193, 7, 0.1);
                    border: 1px solid rgba(255, 193, 7, 0.3);
                    color: #FFF3CD;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 15px 0;
                    font-family: 'Courier New', monospace;
                    font-size: 1rem;
                    text-align: center;
                    font-weight: 600;
                ">
                    Open your browser:
                    <div style="margin-top: 10px; font-size: 1.2rem;">
                        <a href="http://localhost:8000" target="_blank" 
                           style="color: #FFD54F; text-decoration: none;"
                           onmouseover="this.style.textDecoration='underline'; this.style.color='#FFECB3';"
                           onmouseout="this.style.textDecoration='none'; this.style.color='#FFD54F';">
                           🌐 http://localhost:8000
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- GitHub Button -->
            <div style="text-align: center; margin-top: 30px;">
                <a href="https://github.com/HU3YN/VoyageAI-Explorer" target="_blank" 
                   style="
                        display: inline-flex;
                        align-items: center;
                        gap: 12px;
                        background: var(--gradient-primary); 
                        color: white; 
                        padding: 15px 30px; 
                        border-radius: 10px; 
                        text-decoration: none;
                        font-weight: 700; 
                        font-size: 1.1rem;
                        transition: all 0.3s ease;
                        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
                        border: none;
                        letter-spacing: 0.5px;
                   "
                   onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 12px 30px rgba(255, 107, 53, 0.6)';"
                   onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 25px rgba(255, 107, 53, 0.4)';">
                   <span style="font-size: 1.3rem;">⭐</span> 
                   Get Full Version on GitHub →
                </a>
            </div>
            
            <!-- Animation keyframes -->
            <style>
                @keyframes noticeAppear {
                    from {
                        opacity: 0;
                        transform: translateY(30px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                @keyframes gradientFlow {
                    0% { background-position: 0% 50%; }
                    100% { background-position: 200% 50%; }
                }
                .setup-step:hover {
                    transform: translateX(5px);
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                }
            </style>
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

