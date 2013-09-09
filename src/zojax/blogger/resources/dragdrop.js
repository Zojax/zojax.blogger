$(document).ready(function() {

    // Sort
    $(".form-widgets-text .multi-widget").children().each(function(index) {
        if ($(this).attr('id') == 'form-widgets-text-'+index+'-row') {
            $('#form-widgets-text-'+index+'-widgets-position').val(index);
        }
    });

    $(".form-widgets-buttons .multi-widget").children().each(function(index) {
        if ($(this).attr('id') == 'form-widgets-buttons-'+index+'-row') {
            $('#form-widgets-buttons-'+index+'-widgets-position').val(index);
        }
    });

    $( ".form-widgets-text .multi-widget" ).sortable({
        connectWith: ".form-widgets-text .multi-widget",
        axis: "y",
        update: function(event, ui) {
            parent = ui.item.parent();
            parent.children().each(function(index) {
                var Id = $(this).attr('id');
                Id = Id.replace('form-widgets-text-', '');
                Id = Id.replace('-row', '');
                $('#form-widgets-text-'+Id+'-widgets-position').val(index);
            });
        }
    }).disableSelection();

    $( ".form-widgets-buttons .multi-widget" ).sortable({
        connectWith: ".form-widgets-buttons .multi-widget",
        axis: "y",
        update: function(event, ui) {
            parent = ui.item.parent();
            parent.children().each(function(index) {
                var Id = $(this).attr('id');
                Id = Id.replace('form-widgets-buttons-', '');
                Id = Id.replace('-row', '');
                $('#form-widgets-buttons-'+Id+'-widgets-position').val(index);
            });
        }
    }).disableSelection();

    // Expand-collapse
    $(".form-widgets-text .multi-widget .row > div.widget").hide();
    $(".form-widgets-buttons .multi-widget .row > div.widget").hide();

    $(".form-widgets-text .multi-widget .row > div.label").addClass("closed");
    $(".form-widgets-buttons .multi-widget .row > div.label").addClass("closed");

    var toggleItem = function() {
        var $glideElement = $(this);
	    if ($glideElement.next().is(":hidden")) {
		    // show it
		    $glideElement.removeClass("closed");
		    $glideElement.addClass("open");
		    $glideElement.next().slideDown();
	    } else {
		    // hidde it
		    $glideElement.removeClass("open");
		    $glideElement.addClass("closed");
		    $glideElement.next().slideUp();
	    }
	    return false;
    }

    $(".form-widgets-text .multi-widget .row > div.label").click(toggleItem);
    $(".form-widgets-buttons .multi-widget .row > div.label").click(toggleItem);
});
