$(document).ready(function () {
    // Add custom CSS for popups
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            .school-popup h3 { margin-bottom: 5px; }
            .school-popup p { margin: 3px 0; font-size: 13px; }
            .view-details-btn { cursor: pointer; }
            .leaflet-popup-content { min-width: 200px; }
            #schoolDetailsPanel { box-shadow: -5px 0 15px rgba(0,0,0,0.2); }
            #schoolDetailsOverlay { backdrop-filter: blur(2px); transition: opacity 0.3s; }
            .school-icon-legend { display: flex; align-items: center; margin-bottom: 5px; }
            .school-icon-legend img { width: 20px; height: 20px; margin-right: 10px; }
        `)
        .appendTo('head');
        
    // --------------------------------Define different icons for school types
    var privateSchoolIcon = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/128/17573/17573589.png', // Private school icon
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });
    
    
    var communitySchoolIcon = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/128/1183/1183386.png', // Community school icon
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });
    
    var defaultSchoolIcon = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/128/1691/1691970.png', // Default school icon
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });

   

    // Initialize Leaflet map
    var map = L.map('map').setView([27.7, 85.3], 7); // Center on Nepal
    
    // Define multiple base map layers
    var baseMaps = {
        "OpenStreetMap": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }),
        "OpenTopoMap": L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a>',
            maxZoom: 17
        }),
        "Esri WorldImagery": L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            maxZoom: 18
        }),
        "Stamen Terrain": L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.png', {
            attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        })
    };
    
    // Add the default map layer to the map
    baseMaps["OpenStreetMap"].addTo(map);
    
    // Create a layer for markers
    var markersLayer = L.layerGroup().addTo(map);
    
    // Add layer control to switch between base maps
    L.control.layers(baseMaps, null, {collapsed: false}).addTo(map);
    
    // Add Nepal border
    $.getJSON('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_0_countries.geojson', function(data) {
        // Filter to get only Nepal
        L.geoJSON(data, {
            filter: function(feature) {
                return feature.properties.ADMIN === "Nepal";
            },
            style: {
                color: 'black',
                weight: 3,
                fillColor: 'transparent',
                fillOpacity: 0
            }
        }).addTo(map);
    });

    // Modify the fetchSchools function to use the correct parameter name
    function fetchSchools(province = "", district = "", municipalityType = "", schoolType = "") {
        $.ajax({
            url: `http://127.0.0.1:8000/api/schools/?province=${province}&district=${district}&municipality_type=${municipalityType}&school_type=${schoolType}`,
            type: "GET",
            dataType: "json",
            success: function (data) {
                console.log("Data received from backend:", data);
                console.log("Filter applied - School Type:", schoolType);
                // Rest of your code remains the same
                if (data && data.length > 0) {
                    console.log("First school:", data[0]);
                } else {
                    console.log("No schools received");
                }
                updateSchoolList(data);
                updateMap(data);
                
                // Update district dropdown if province changes and district is empty
                if (province && !district) {
                    updateDistrictOptions(data);
                }
                
                // Update active filters display
                updateActiveFilters();
            },
            error: function (xhr, status, error) {
                // Error handling remains the same
                console.error("Error fetching schools:", status, error);
                console.log("Response:", xhr.responseText);
                console.log("Status code:", xhr.status);
                $("#schoolList").html("<p>Error loading schools. Check console for details.</p>");
            }
        });
    }

    // Function to update the district dropdown based on the selected province
    function updateDistrictOptions(schools) {
        // Get unique districts from the filtered schools
        const districts = [...new Set(schools
            .filter(school => school.district) // Filter out null/undefined districts
            .map(school => school.district))]; // Extract district names
        
        // Sort districts alphabetically
        districts.sort();
        
        // Generate options HTML
        let options = '<option value="">All Districts</option>';
        districts.forEach(district => {
            options += `<option value="${district}">${district}</option>`;
        });
        
        // Update the dropdown
        $("#districtFilter").html(options);
    }

    // Function to update school list
    function updateSchoolList(schools) {
        if (schools.length === 0) {
            $("#schoolList").html("<div class='text-center p-4'>No schools found matching your criteria.</div>");
            return;
        }
        
        let html = "<div class='grid gap-3'>";
        schools.forEach(school => {
            html += `
                <div class='school-item border rounded-lg p-3 hover:bg-gray-50 cursor-pointer transition-colors' data-lat='${school.latitude}' data-lng='${school.longitude}' data-id='${school.id}'>
                    <div class='font-bold text-blue-600 mb-1'><i class="fa fa-graduation-cap" aria-hidden="true" style="color: black;"></i> ${school.name}</div>
                    <div class='text-sm text-gray-600 flex flex-wrap items-center'>
                        <span class='flex items-center mr-2 mb-1'><i class="fa fa-location-arrow" aria-hidden="true" style="font-size:12px;"></i>${school.address}</span>
                        ${school.province ? `<span class='text-xs bg-blue-100 px-2 py-1 rounded-full mb-1'>Province ${school.province}</span>` : ''}
                    </div>
                    <div class='text-xs text-gray-500 mt-1'>${school.school_type || 'School'} · ${school.established_year ? `Est. ${school.established_year}` : ''}</div>
                </div>
            `;
        });
        html += "</div>";
        
        $("#schoolList").html(html);
        
        // Add click event for each school item
        $(".school-item").on("click", function() {
            const lat = $(this).data('lat');
            const lng = $(this).data('lng');
            const id = $(this).data('id');
            
            // Pan map to location
            map.setView([lat, lng], 14);
            
            // Find and open the marker popup
            markersLayer.eachLayer(function(layer) {
                if (layer.getLatLng().lat === lat && layer.getLatLng().lng === lng) {
                    layer.openPopup();
                }
            });
            
            // Show details
            showSchoolDetails(id);
            
            // Highlight selected school
            $(".school-item").removeClass("bg-blue-50 border-blue-300");
            $(this).addClass("bg-blue-50 border-blue-300");
        });
    }

    // Function to update map with appropriate markers based on school type
    function updateMap(schools) {
        markersLayer.clearLayers(); // Remove previous markers
        
        schools.forEach(school => {
            // Determine which icon to use based on school type
            let icon;
            let schoolType = (school.school_type || "").toLowerCase();
            
            if (schoolType.includes("private")) {
                icon = privateSchoolIcon;
            } else if (schoolType.includes("community")) {
                icon = communitySchoolIcon;
            } else {
                icon = defaultSchoolIcon;
            }
            
            // Create popup content
            const popupContent = `
                <div class="school-popup">
                    <h3 class="text-lg font-bold">${school.name}</h3>
                    <div class="mt-2">
                        <p><strong>Address:</strong> ${school.address}</p>
                        <p><strong>Province:</strong> ${school.province || 'N/A'}</p>
                        <p><strong>Type:</strong> ${school.school_type || 'N/A'}</p>
                        <p><strong>Established:</strong> ${school.established_year || 'N/A'}</p>
                        <p><strong>Contact:</strong> ${school.contact_number || 'N/A'}</p>
                    </div>
                    <div class="mt-2">
                        <button class="view-details-btn bg-blue-500 text-white px-2 py-1 rounded text-sm" 
                                data-school-id="${school.id}">View Full Details</button>
                    </div>
                </div>`;
    
            // Create marker with appropriate icon
            let marker = L.marker([school.latitude, school.longitude], { icon: icon })
                .bindPopup(popupContent)
                .addTo(markersLayer);
        });
    }

    // Event delegation for the view-details button in popups
    $(document).on('click', '.view-details-btn', function() {
        const schoolId = $(this).data('school-id');
        showSchoolDetails(schoolId);
    });

// Function to show detailed school information
function showSchoolDetails(schoolId) {
    // Fetch specific school details
    $.ajax({
        url: `http://127.0.0.1:8000/api/schools/${schoolId}/`,
        type: "GET",
        dataType: "json",
        success: function(school) {
            // Create modal or sidebar with detailed information
            const detailsHTML = `
                <div class="p-6 relative">
                    <button id="closeDetailsBtn" class="absolute top-4 right-4 text-gray-500 hover:text-gray-800">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                    
                    <h2 class="text-2xl font-bold mb-6 pr-8">${school.name}</h2>
                    
                    <div class="space-y-4">
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <h3 class="text-sm uppercase text-gray-500 font-medium mb-2">Location</h3>
                            <p class="mb-1"><i class="fas fa-map-marker-alt text-gray-400 mr-2"></i>${school.address}</p>
                            <p><i class="fas fa-globe-asia text-gray-400 mr-2"></i>Province ${school.province || 'N/A'}</p>
                        </div>
                        
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <h3 class="text-sm uppercase text-gray-500 font-medium mb-2">School Info</h3>
                            <div class="grid grid-cols-2 gap-y-2">
                                <p><span class="font-medium">Type:</span> ${school.school_type || 'N/A'}</p>
                                <p><span class="font-medium">Est. Year:</span> ${school.established_year || 'N/A'}</p>
                                <p><span class="font-medium">Students:</span> ${school.student_count || 'N/A'}</p>
                                <p><span class="font-medium">Staff:</span> ${school.staff_count || 'N/A'}</p>
                            </div>
                        </div>
                        
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <h3 class="text-sm uppercase text-gray-500 font-medium mb-2">Contact</h3>
                            <p class="mb-1"><i class="fas fa-phone text-gray-400 mr-2"></i>${school.contact_number || 'N/A'}</p>
                            <p class="mb-1"><i class="fas fa-envelope text-gray-400 mr-2"></i>${school.email || 'N/A'}</p>
                            <p>${school.website ? 
                                `<a href="${school.website}" target="_blank" class="text-blue-600 hover:underline flex items-center">
                                    <i class="fas fa-globe text-gray-400 mr-2"></i>Visit Website
                                    <svg class="w-3 h-3 ml-1" fill="currentColor" viewBox="0 0 20 20">
                                        <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                                    </svg>
                                </a>` : '<i class="fas fa-globe text-gray-400 mr-2"></i>N/A'}
                            </p>
                        </div>
                        
                        ${school.facilities ? `
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <h3 class="text-sm uppercase text-gray-500 font-medium mb-2">Facilities</h3>
                            <p>${school.facilities}</p>
                        </div>` : ''}
                        
                        <div class="mt-6 text-center">
                            <button class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md shadow-sm transition duration-200">
                                Get Directions
                            </button>
                        </div>
                    </div>
                </div>`;
            
            // Remove any existing overlay and panel first to avoid duplicates
            $('#schoolDetailsOverlay, #schoolDetailsPanel').remove();
            
            // Add overlay and panel with very high z-index values
            $('body').append(`
                <div id="schoolDetailsOverlay" class="fixed inset-0 bg-black bg-opacity-50 z-[9998]"></div>
                <div id="schoolDetailsPanel" class="fixed top-0 right-0 h-full w-96 bg-white shadow-lg z-[9999] overflow-y-auto transform translate-x-full transition-transform duration-300">${detailsHTML}</div>
            `);
            
            // Make sure Leaflet controls are below our overlay
            $('.leaflet-control-container').css('z-index', '400');
            
            // Ensure the panel is above popups
            $('.leaflet-popup').css('z-index', '700');
            
            // Show the panel with animation
            setTimeout(() => {
                $('#schoolDetailsPanel').css('transform', 'translateX(0)');
            }, 50);
            
            // Add event listener to close button
            $('#closeDetailsBtn').click(function() {
                $('#schoolDetailsPanel').css('transform', 'translateX(100%)');
                setTimeout(() => {
                    $('#schoolDetailsOverlay').remove();
                }, 300);
            });
            
            // Also close when clicking overlay
            $('#schoolDetailsOverlay').click(function() {
                $('#closeDetailsBtn').click();
            });
            
            // Make sure map is properly sized
            if (typeof map !== 'undefined') {
                setTimeout(() => {
                    map.invalidateSize();
                }, 350);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error fetching school details:", error);
        }
    });
}

    // Fetch schools when province filter is changed
    $("#provinceFilter").change(function () {
        let selectedProvince = $(this).val();
        let selectedDistrict = ""; // Reset district when province changes
        let selectedMunicipalityType = $("#municipalityTypeFilter").val();
        let selectedSchoolType = $("#schoolTypeFilter").val();
        
        // Clear district selection when province changes
        $("#districtFilter").val("");
        
        fetchSchools(selectedProvince, selectedDistrict, selectedMunicipalityType, selectedSchoolType);
    });

    $("#districtFilter").change(function () {
        let selectedProvince = $("#provinceFilter").val();
        let selectedDistrict = $(this).val();
        let selectedMunicipalityType = $("#municipalityTypeFilter").val();
        let selectedSchoolType = $("#schoolTypeFilter").val();
        
        fetchSchools(selectedProvince, selectedDistrict, selectedMunicipalityType, selectedSchoolType);
    });

    $("#municipalityTypeFilter").change(function () {
        let selectedProvince = $("#provinceFilter").val();
        let selectedDistrict = $("#districtFilter").val();
        let selectedMunicipalityType = $(this).val();
        let selectedSchoolType = $("#schoolTypeFilter").val();
        
        fetchSchools(selectedProvince, selectedDistrict, selectedMunicipalityType, selectedSchoolType);
    });

    // Add this with your other event listeners
    $("#schoolTypeFilter").change(function () {
        let selectedProvince = $("#provinceFilter").val();
        let selectedDistrict = $("#districtFilter").val();
        let selectedMunicipalityType = $("#municipalityTypeFilter").val();
        let selectedSchoolType = $(this).val();
        
        fetchSchools(selectedProvince, selectedDistrict, selectedMunicipalityType, selectedSchoolType);
    });

    // Update the clear filters button to reset school type too
    $("#clearFilters").click(function() {
        // Reset all dropdowns
        $("#provinceFilter").val("");
        $("#districtFilter").val("");
        $("#municipalityTypeFilter").val("");
        $("#schoolTypeFilter").val("");
        
        // Fetch all schools
        fetchSchools("", "", "", "");
    });

    // Load all schools initially
    fetchSchools("", "", "", "");

    // Test API connectivity directly
    console.log("Testing API connectivity...");
    fetch('http://127.0.0.1:8000/api/schools/')
        .then(response => {
            console.log("API Status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("API Test Data:", data);
        })
        .catch(error => {
            console.error("API Test Error:", error);
        });

    // Call this after your map is initialized
    addMapLegend(map);
    
    // Set up filter handlers
    setupFilterHandlers();
    
    // Initialize active filters on page load
    updateActiveFilters();
    
    // Add document-level event delegation for the clear button
    $(document).on("click", "#clearActiveFilters", function(e) {
        e.preventDefault();
        
        console.log("Clear button clicked via delegation");
        
        // Reset all dropdowns
        $("#provinceFilter").val("");
        $("#districtFilter").val("");
        $("#municipalityTypeFilter").val("");
        $("#schoolTypeFilter").val("");
        
        // Clear active filters display
        $("#activeFilters").html('');
        
        // Fetch all schools
        fetchSchools("", "", "", "");
    });
});

// Change this function to accept the map as a parameter
function addMapLegend(map) {
    // Create a legend control
    var legend = L.control({ position: 'bottomright' });
    
    legend.onAdd = function(map) {
        var div = L.DomUtil.create('div', 'info legend bg-white p-3 rounded shadow-md');
        
        div.innerHTML = `
            <h4 class="font-medium mb-2">School Types</h4>
            <div class="school-icon-legend">
                <img src="https://cdn-icons-png.flaticon.com/128/17573/17573589.png" alt="Private School">
                <span>Private School</span>
            </div>
            <div class="school-icon-legend">
                <img src="https://cdn-icons-png.flaticon.com/128/1183/1183386.png" alt="Community School">
                <span>Community School</span>
            </div>
            <div class="school-icon-legend">
                <img src="https://cdn-icons-png.flaticon.com/128/1691/1691970.png" alt="Other School">
                <span>Other Types</span>
            </div>
        `;
        
        div.style.cssText = 'background-color: white; padding: 10px; border-radius: 5px;';
        return div;
    };
    
    legend.addTo(map);
}

// Updated updateActiveFilters function with better event handling
function updateActiveFilters() {
    const province = $("#provinceFilter").val();
    const district = $("#districtFilter").val();
    const municipalityType = $("#municipalityTypeFilter").val();
    const schoolType = $("#schoolTypeFilter").val();
    
    let filterHTML = '';
    
    if (province || district || municipalityType || schoolType) {
        // Change from justify-between to just a flex container with gap
        filterHTML = '<div class="flex flex-wrap items-center gap-3">';
        
        // Active filters tags first
        filterHTML += '<span class="font-medium text-xs text-gray-500">Active Filters:</span>';
        
        if (province) {
            filterHTML += `<span class="inline-block bg-blue-100 text-blue-800 rounded-full px-2 py-0.5 text-xs">Province: ${province}</span>`;
        }
        
        if (district) {
            filterHTML += `<span class="inline-block bg-blue-100 text-blue-800 rounded-full px-2 py-0.5 text-xs">District: ${district}</span>`;
        }
        
        if (municipalityType) {
            filterHTML += `<span class="inline-block bg-blue-100 text-blue-800 rounded-full px-2 py-0.5 text-xs">Municipality: ${municipalityType}</span>`;
        }
        
        if (schoolType) {
            filterHTML += `<span class="inline-block bg-blue-100 text-blue-800 rounded-full px-2 py-0.5 text-xs">Type: ${schoolType}</span>`;
        }
        
        // Clear button right after the filter tags (not wrapped in its own div)
        filterHTML += '<button id="clearActiveFilters" class="bg-red-100 hover:bg-red-200 text-red-700 font-medium px-3 py-0.5 rounded-md text-xs transition-colors flex items-center shadow-sm">';
        filterHTML += '<i class="fas fa-times-circle mr-1"></i> Clear</button>';
        
        filterHTML += '</div>';
    }
    
    // Update the DOM
    $("#activeFilters").html(filterHTML);
    
    // Add direct event listener to the button we just created
    if (province || district || municipalityType || schoolType) {
        // Using setTimeout to ensure DOM is updated before adding the event
        setTimeout(() => {
            $("#clearActiveFilters").on("click", function(e) {
                e.preventDefault();
                
                // Reset all dropdowns
                $("#provinceFilter").val("");
                $("#districtFilter").val("");
                $("#municipalityTypeFilter").val("");
                $("#schoolTypeFilter").val("");
                
                // Clear active filters display
                $("#activeFilters").html('');
                
                // Fetch all schools
                fetchSchools("", "", "", "");
                
                console.log("Clear filters clicked");
            });
        }, 0);
    }
}

// Add unified filter handler
function setupFilterHandlers() {
    $("#provinceFilter, #districtFilter, #municipalityTypeFilter, #schoolTypeFilter").on("change", function() {
        let selectedProvince = $("#provinceFilter").val();
        let selectedDistrict = $("#districtFilter").val();
        let selectedMunicipalityType = $("#municipalityTypeFilter").val();
        let selectedSchoolType = $("#schoolTypeFilter").val();
        
        // Special handling for province change
        if ($(this).attr('id') === 'provinceFilter') {
            // Reset district when province changes
            selectedDistrict = "";
            $("#districtFilter").val("");
        }
        
        fetchSchools(selectedProvince, selectedDistrict, selectedMunicipalityType, selectedSchoolType);
    });
}
