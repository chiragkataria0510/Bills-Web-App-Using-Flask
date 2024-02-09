$(document).ready(function() {
    $("input[type='radio']").change(function() {
        if ($(this).val() == "yes") {
            $("#ifYes").show(800);
        } else {
            $("#ifYes").hide(800);
        }
    });
});
