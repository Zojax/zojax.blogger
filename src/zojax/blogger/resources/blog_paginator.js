$(document).ready(function (){
    $('#pager_container').pajinate({
        items_per_page : 1,
//        num_page_links_to_display : 1,
        item_container_id: '.post-pages',
        show_first_last: false,
        nav_label_info : '{0} of {2}',
//        nav_order : ["first", "prev", "next", "last"],
        jquery_ui_active: "hidden",
        jquery_ui_default: "hidden",
        jquery_ui: true,
        nav_label_prev : '« Prev',
        nav_label_next : 'Next »',
        abort_on_small_lists: true

    });

    $("a.show-all").click(function(){
        $("#pager_container li").show();
        $(".page_navigation").hide();
        $(this).hide();
        $(".paginate-post").show();
        return false;
    });

    $("a.paginate-post").click(function(){
        $(".page_navigation").show();
        $(this).hide();
        $("a.show-all").show();
        gotopage(0);
        return false;
    });
});

