$(document).ready(function (){
    $('#pager_container').pajinate({items_per_page : 1,
        num_page_links_to_display : 1,
        item_container_id: '.post-pages',
        show_first_last: false});

    $("a.show-all").click(function(){
        $("#pager_container li").show();
        $(this).hide();
        $(".page_navigation").hide();
        return false;
    });
});

