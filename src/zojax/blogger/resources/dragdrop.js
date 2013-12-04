$(document).ready(function() {

    var NO_TOGGLE = false;
    if ($('.row').length == 1) {
        $("#form-widgets-pages-buttons-remove").hide();
    }
    // Sort
    var sortItems;
    (sortItems =  function () {
        $(".form-widgets-pages .multi-widget input.text-widget").each(function(index) {
                $(this).val(index);
            });
    })();

    $( '.form-widgets-pages .multi-widget').sortable({
        axis: "y",
        update: function(event, ui) {
            sortItems();
            var NO_TOGGLE = false;
        },
        start : function(event, ui){
            NO_TOGGLE = true;
            if (typeof(tinyMCE) != 'undefined'){
                tinyMCE.execCommand('mceRemoveControl', false, ui.item.find('textarea').attr('id'));
            }
        },
        stop : function(event, ui){
            if (typeof(tinyMCE) != 'undefined'){
                tinyMCE.execCommand('mceAddControl', false, ui.item.find('textarea').attr('id'));
                ui.item.find('a.mceResize').mousedown(function (){
                    return false;
                });
            }
        }
    });

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
            $("a.mceResize").mousedown(function (){
                return false;
            });
	    } else {
		    // hidde it
		    $glideElement.removeClass("open");
		    $glideElement.addClass("closed");
		    $glideElement.next().slideUp();
	    }
	    return false;
    }

    $(".form-widgets-pages .multi-widget .row > div.label").click(toggleItem);

    $("#form-widgets-pages-buttons-remove").click(function(){
        if ($('.form-widgets-pages input[type=checkbox]').length == $('.form-widgets-pages input[type=checkbox]:checked').length) {
            $('.form-widgets-pages').addClass('error');
            $('label[for=form-widgets-pages]').after('<div class="error">You can\'t remove all pages</div>');
            return false;
        }
    });

    $('div.widget > script').remove()
});
