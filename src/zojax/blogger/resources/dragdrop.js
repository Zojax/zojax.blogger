$(document).ready(function() {

    var NO_TOGGLE = false;
    // Sort
    $(".form-widgets-pages .multi-widget").children().each(function(index) {
        if ($(this).attr('id') == 'form-widgets-pages-'+index+'-row') {
            $('#form-widgets-pages-'+index+'-widgets-position').val(index);
        }
    });

    $( ".form-widgets-pages .multi-widget" ).sortable({
        connectWith: ".form-widgets-pages .multi-widget",
        axis: "y",
        update: function(event, ui) {
            parent = ui.item.parent();
            parent.children().each(function(index) {
                var Id = $(this).attr('id');
                Id = Id.replace('form-widgets-pages-', '');
                Id = Id.replace('-row', '');
                $('#form-widgets-pages-'+Id+'-widgets-position').val(index);
            });
        },
        start : function(){
            NO_TOGGLE = true;
        }
    }).disableSelection();

    // Expand-collapse
    $(".form-widgets-pages .multi-widget .row > div.widget").hide();

    $(".form-widgets-pages .multi-widget .row > div.label").addClass("closed");

    var toggleItem = function() {
        if (NO_TOGGLE) {
            NO_TOGGLE = false;
            return false;
        }
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

    $(".form-widgets-pages .multi-widget .row > div.label").click(toggleItem);
});
