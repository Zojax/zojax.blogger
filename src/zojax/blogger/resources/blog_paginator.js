$(document).ready(function (){
    var createSlider = function(){
        var _slider = $('.post-pages').bxSlider({
            infiniteLoop: false,
            adaptiveHeight: true,
            nextSelector: '.next',
            prevSelector: '.prev',
            nextText: '',
            prevText: '',
            onSlideBefore: function($slideElement, oldIndex, newIndex) {
                $('.info').text((_slider.getCurrentSlide()+1) + ' of ' + _slider.getSlideCount());

            }
        });
        $('.info').text((_slider.getCurrentSlide()+1) + ' of ' + _slider.getSlideCount());
        return _slider
    }

    var slider = createSlider();

    $("a.show-all").click(function(){
        slider.destroySlider();
        $(this).hide();
        $('.page_navigation').hide();
        $("a.paginate-post").show();
        return false;
    });

    $("a.paginate-post").click(function(){
        $(this).hide();
        slider.reloadSlider();
        $('.info').text((slider.getCurrentSlide()+1) + ' of ' + slider.getSlideCount());
        $("a.show-all").show()
        $('.page_navigation').show();
        return false;
    });

});
