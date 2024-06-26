function clearAllIntervals() {
    var id = window.setInterval(function() {}, 0);
    while (id--) {
        window.clearInterval(id);
    }
}

//SPA Request GET, load page /user/...
function loadPageUsers(pagePath, pushState = true) {
    if(pagePath === "home")
        clearAllIntervals(); 

    $.ajax({
        url: `/users/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/users/${pagePath}`);
            }
            localStorage.setItem('current_url', `/users/${pagePath}/`);
            // urls = localStorage.getItem('current_url');
            bindFormEvent();
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load page /tournaments/...
function loadPageTournament(pagePath, tournamentName = '', pushState = true) {
    if(!pagePath) {
        return(console.log("I got you haha: ", pagePath));}
    $.ajax({
        url: `/tournaments/${pagePath}/?tournament_name=${tournamentName}`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/tournaments/${pagePath}`);
            }
            localStorage.setItem('current_url', `/tournaments/${pagePath}/?tournament_name=${tournamentName}`);
            // urls = localStorage.getItem('current_url');
            bindFormEvent();
            if (document.getElementById('tournament-name')) {
                initTournamentPage();
            }
            initializeGameTournament();
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load play tournament `/${response.tournament_name}/play/${response.game_id}/`
function loadPagePlayTournament(tournament_name, game_id, pushState = true) {
    if(!tournament_name || !game_id) {
        return(console.error("tournamet_name or game_id doesn't exist", pagePath));}
    let pagePath = `${tournament_name}/play/${game_id}`
    $.ajax({
        url: `/tournaments/${pagePath}`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/tournaments/${pagePath}`);
            }
            localStorage.setItem('current_url', `/tournaments/${pagePath}`);
            // urls = localStorage.getItem('current_url');
            bindFormEvent();
            initializeGameTournament();
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
            localStorage.setItem('current_url', `/matchmaking/${pagePath}/`);
            // urls = localStorage.getItem('current_url');
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
            console.log("pagePath: ", pagePath);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/games/${pagePath}`);
            }
            localStorage.setItem('current_url', `/games/${pagePath}/`);
            // urls = localStorage.getItem('current_url');
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
                localStorage.setItem('current_url', `/users/${pagePath}/`);
                // urls = localStorage.getItem('current_url');
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
            localStorage.setItem('current_url', `/blockchain/${pagePath}/`);
            // urls = localStorage.getItem('current_url');
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
            localStorage.setItem('current_url', `/aouth/${pagePath}/`);
            localStorage.setItem('last_url_from_popstate', "");
            // urls = localStorage.getItem('current_url');
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
            localStorage.setItem('current_url', `/users/friend-profile/${username}/`);
            // urls = localStorage.getItem('current_url');
            bindFormEvent(); 
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//set localstorage for connection via 42AOUTH with 2FA enable
function setLocalStorageAndLoadPage() {
    const accessToken = document.getElementById('access_token').value;
    const refreshToken = document.getElementById('refresh_token').value;
    const csrfToken = document.getElementById('csrf_token').value;
    const redirectUrl = document.getElementById('redirect_url').value;

    if (accessToken && refreshToken && csrfToken) {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        localStorage.setItem('csrf_token', csrfToken);

        loadPageUsers(redirectUrl.replace(/^\//, ''), true);
    } else {
        console.error('Missing tokens');
        window.location.href = '/login';  // Redirect to login page or handle appropriately
    }
}

function clean_matchmaking(){
    fetch('/users/redirect/')
    .then(response => response.json())
    .then(data => {
        if (data.redirect === 'home') {
            console.log("pourquoi")
        }     
    })
    .catch(error => {
        console.error('Error Clean:', error);
    });
}
function leaveMatchmakingQueu() {
    fetch('/matchmaking/matchmaking_remote_leave/');
}

//SPA Request POST, Form register, login, 2FA
function bindFormEvent() {

    window.onbeforeunload = async function() {
        urls = localStorage.getItem('current_url');
        if (urls === "/matchmaking/matchmaking_remote" || urls === "/matchmaking/matchmaking_remote/") {
            const message = "Are you sure you want to leave the matchmaking queue?";
            event.returnValue = message;  // Standard way to set a confirmation dialog message
    
            // This return statement is required for some browsers to display the dialog
            return message;
        }
    }
    window.addEventListener('unload', async function() {
        urls = localStorage.getItem('current_url');
    
        if (urls === "/matchmaking/matchmaking_remote" || urls === "/matchmaking/matchmaking_remote/") {
            leaveMatchmakingQueu();
            clean_matchmaking();
            console.log("You left the matchmaking Queue ><");
        }
    });

    window.addEventListener('popstate', async function(event)
    {
        last_url = localStorage.getItem('last_url_from_popstate');
        urls = localStorage.getItem('current_url');
        if (last_url){
            if(last_url === urls){
                console.log("solutionare");
                localStorage.setItem('last_url_from_popstate', "");
                return ;
            }
        }
        console.log("POpypstate urls: ", urls);
        localStorage.setItem('last_url_from_popstate', urls);

        if (urls === "/users/home" || urls === "/users/home/") {
            console.log("joja");
            window.history.pushState(null, null, window.location.href);
            loadPageUsers('home');
            // window.history.pushState(null, null, window.location.href);
        }
        else if (urls === "/games/results" || urls === "/games/results/"){
            window.history.pushState(null, null, window.location.href);
            loadPageUsers('home');
        }
        else if (window.location.pathname === '/aouth/twofactor/') {
            window.history.pushState(null, null, window.location.href);
            loadPageAouth('aouth_logout');
        }
        else if (event.state) {
            console.log("aloura2 et: ")
            $('#app-content').html(event.state.content);
            bindFormEvent();
        }
    },{ once: true });

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
    

    //connectTournament
    $('#connectTournament').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success')
                    loadPageTournament(response.redirectUrl.replace(/^\//, ''), true);
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });

    //generateTournament
    $('#generateTournament').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success')
                    loadPageTournament(response.redirectUrl.replace(/^\//, ''), true);
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
                // bindFormEvent();
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
    

      
    
});


function setupGoBackButton() {
    $('#goBackButton').on('click', function() {
        window.history.back();
    });
}

