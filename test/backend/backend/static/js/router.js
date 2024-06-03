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

//SPA Request GET, load page /matchmaking/...
function loadPageMatchmaking(pagePath, pushState = true) {
    $.ajax({
        url: `/matchmaking/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                 history.pushState({ path: pagePath, content: response.html }, '', `/matchmaking/${pagePath}`);
            }
            bindFormEvent();
            if (typeof initializeGame === 'function') {
                initializeGame();
            } 
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
            if (typeof initializeGame === 'function' && pagePath === 'play') {
                initializeGame();
            }
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
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
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
                    localStorage.setItem('access_token', response.access_token);
                    localStorage.setItem('refresh_token', response.refresh_token);
                    localStorage.setItem('csrf_token', response.csrf_token);
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

    $('#Set_image').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success image changed");
               
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });

    $('#Set_username').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success username changed");
               
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
    

    // Setting change the Password
    $('#Set_password').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success password changed");
               
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });

    // Setting change the 2factor
    $('#2faForm').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success 2faForm");
               
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });

    $('#enable_2fa').off('change').on('change', function(e) {
        e.preventDefault();
        bindFormEvent()
        $('#2faForm').submit();
        
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
                    localStorage.setItem('access_token', response.access_token);
                    localStorage.setItem('refresh_token', response.refresh_token);
                    localStorage.setItem('csrf_token', response.csrf_token);
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

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            $('#imagePreview').attr('src', e.target.result);
        }
        
        reader.readAsDataURL(input.files[0]); // convert to base64 string
    }
}

$(document).ready(function() {
    bindFormEvent();

    $("#file-upload").change(function() {
        readURL(this);
    });

    $(document).on('pjax:end', function() {
        bindFormEvent();
    });

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

