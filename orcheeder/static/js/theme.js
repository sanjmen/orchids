$(function() {
    // Topbar active tab support
    $(".topbar li").removeClass("active");

    var class_list = $("body").attr("class").split(/\s+/);
    $.each(class_list, function(index, item) {
        var selector = "ul.nav li#tab_" + item;
        $(selector).addClass("active");
    });

    $("#account_logout").click(function(e) {
        e.preventDefault();
        $(this).closest("form").submit();
    });
});

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

$(document).ready(function(){
    var i;
    $('.thumbnail').click(function(e) {
        i = this.getElementsByTagName('IMG')[0].cloneNode();
        })
    $('#myModal').on('shown', function() {
        $('.modal-header').append('<h3>'+i.getAttribute('alt')+'</h3>');
        $('.modal-body').append(i);
        })
    $('#myModal').on('hidden', function() {
        $('.modal-body').empty();
        $('.modal-header h3').empty();
    })
    $('#tips-tabs .nav-tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    })
    $('.btn.btn-success.genus-button').appendTo($('.pagination'));
});
