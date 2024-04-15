function loadPersoPage() {
    $.ajax({
        url: '/api/perso-content/', // Ensure this URL is correctly routed to your `view_perso` view
        success: function(response) {
            console.log('Sucess:', response);
            $('#app-content').html(response.html);
            history.pushState({path: '/perso'}, '', '/perso');
        },
        error: function(error) {
            console.log('Error loading the page:', error);
        }
    });
}


function loadProfileDataJson() {
    var profileData = $('#profileData');

    // Vérifier si le profil est déjà affiché
    if (profileData.is(':visible')) {
        // Si c'est le cas, le cacher
        profileData.hide();
    } else {
        $.ajax({
            url: 'api/generate_profile_json/',
            type: 'GET',
            success: function(data) {
                var profileDiv = $('<div>').addClass('profile-section');

                Object.keys(data).forEach(function(key) {
                    // Créer un compartiment pour chaque propriété
                    var propertyDiv = $('<div>').addClass('profile-property');
                    propertyDiv.append('<span class="property-label">' + key + ': </span>');
                    propertyDiv.append('<span class="property-value">' + data[key] + '</span>');
                    profileDiv.append(propertyDiv);
                });
                // profileDiv.append('<h3>Username</h3><div class="profile-data">' + data.username + '</div>');
                // profileDiv.append('<h3>Email</h3><div class="profile-data">' + data.email + '</div>');
                // profileDiv.append('<h3>Age</h3><div class="profile-data">' + data.age + '</div>');
                $('#profileData').html(profileDiv);
                $('#profileData').show();
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }
}

