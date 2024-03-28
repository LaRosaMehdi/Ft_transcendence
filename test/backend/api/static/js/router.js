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
    $.ajax({
        url: 'api/generate_profile_json/',
        type: 'GET',
        success: function(data) {
            var profileDiv = $('<div>').addClass('profile-section');
            profileDiv.append('<h3>Username</h3><div class="profile-data">' + data.username + '</div>');
            profileDiv.append('<h3>Email</h3><div class="profile-data">' + data.email + '</div>');
            profileDiv.append('<h3>Age</h3><div class="profile-data">' + data.age + '</div>');
            $('#profileData').html('<pre>' + JSON.stringify(data, null, 2) + '</pre>');
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

