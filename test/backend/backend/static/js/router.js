//SPA Request GET, load page /user/...
function loadPageUsers(pagePath, pushState = true) {
    $.ajax({
        url: `/users/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/users/${pagePath}`);
            }
            bindFormEvent(); 
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load page /user/...
function loadPageGames(pagePath, pushState = true) {
    $.ajax({
        url: `/games/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/games/${pagePath}`);
            }
            bindFormEvent(); 
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load Setting page
function loadPageUsersSettings(pagePath, pushState = true) {
    event.preventDefault();
    var profileData = $('#profileData');

    if (profileData.is(':visible')) {
        profileData.hide();
    } else {
        $.ajax({
            url: `/users/${pagePath}/`,
            success: function(response) {
                $('#profileData').html(response.html);
                $('#profileData').show();
                bindFormEvent(); 
            },
            error: function(error) {
                console.error('Error loading the page:', error);
            }
        });
    }
}

//SPA Request GET, load page /Blockchain/...
function loadPageBlockchain(pagePath, pushState = true) {
    $.ajax({
        url: `/blockchain/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/blockchain/${pagePath}`);
            }
            bindFormEvent(); 
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load page /Aouth/...
function loadPageAouth(pagePath, pushState = true) {
    console.log("load page Aouth", pagePath)
    $.ajax({
        url: `/aouth/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/${pagePath}`);
            }
            bindFormEvent(); 
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load page profile of a friend /user/...
function loadPageFriendProfile(username, pushState = true) {
    $.ajax({
        url: `/users/friend-profile/${username}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: `/users/friend-profile/${username}`, content: response.html }, '', `/users/friend-profile/${username}`);
            }
            bindFormEvent(); 
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request POST, Form register, login, 2FA
function bindFormEvent() {
    //REgister
    $('#registerForm').off('submit').on('submit', function(e) {
        e.preventDefault();
        console.log("Form submit event caught");
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Response received:", response);
                if (response.status === 'success') {
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                } else {
                    console.log('Success with unexpected status:', response.message);
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
                
            }
        });
    });

    //TwoFactor'twoFactorAouth"
    $('#twoFactorAouth').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success') {
                    loadPageUsers(response.redirectUrl.replace(/^\//, ''), true);
                } else {
                    console.log('Success with unexpected status:', response.message);
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });

    //Auth login 
    $('#loginForm').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Response received:", response);
                if (response.redirectUrl == 'home') {
                    loadPageUsers(response.redirectUrl.replace(/^\//, ''), true);
                }
                else if (response.status === 'success') {
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                } else {
                    console.log('Success with unexpected status:', response.message);
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });

    $('#searchFriends').off('submit').on('submit', function(e) {
        e.preventDefault();
        const queryData = $(this).serialize();
        
        $.ajax({
            type: 'GET',
            url: this.action,
            data: queryData,
            success: function(response) {
                $('#app-content').html(response.html);
                history.pushState({ path: '', content: response.html }, '', window.location.pathname);
                bindFormEvent();
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
    
    $('#AddFriends').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                loadPageUsers('friend', true);
                bindFormEvent();
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
}


$(document).ready(function() {
    bindFormEvent();
    history.replaceState({ path: window.location.pathname, content: $('#app-content').html() }, '', window.location.pathname);

    $('body').on('click', '#goBackButton', function()
    {
        window.history.back();
    });

    window.addEventListener('popstate', function(event) {
        if (window.location.pathname === '/aouth/twofactor/') {
            loadPageAouth('aouth_logout'); 
        }
        else if (event.state) {
            $('#app-content').html(event.state.content);
            bindFormEvent();
        }
    });
});


function setupGoBackButton() {
    $('#goBackButton').on('click', function() {
        window.history.back();
    });
}

function loadProfileDataJson() {
    event.preventDefault();
    var profileData = $('#profileData');

    if (profileData.is(':visible')) {
        profileData.hide();
    } else {
        $.ajax({
            url: `generate_profile_json/`,
            type: 'GET',
            success: function(data) {
                var profileDiv = $('<div>').addClass('profile-section');

                Object.keys(data).forEach(function(key) {
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

