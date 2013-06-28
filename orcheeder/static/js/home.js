
$(document).ready(function() {
    $("a.suggestion").click(function() {
        $("input[name='q']").val($(this).text());
    });
    if (window.location.hash) {
        $("ul#taxon-tabs li > a[href='" + window.location.hash + "']").click()
        window.scrollTo(0,0);
    }
});

