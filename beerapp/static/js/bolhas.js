(function($) {
        
    $(function() {
        $('<div id="beer"></div>').appendTo('#container').bolha();
        
    });
    
    
    var __bolha = function(href) {
        if (href.indexOf('beer') > -1) {
            $(document.body).addClass('bolha');
        }
        else {
            $(document.body).removeClass('bolha');
        }
    }
    
    $.fn.bolha = function() {
        
        return this.each(function() {
            var $obj = $(this);
            
            var count = 200;
            
            var $container = $('#beer');
            
            var $c = null;
            
            $c = $("<div/>").addClass('b1-container').appendTo($container);
            for (var i = 0; i < count; i++) {
                
                
                var x = parseInt(Math.random() * window.innerWidth);
                var y = parseInt(Math.random() * 3000);
                
                $("<div/>").css({left:x+'px',top:y+'px'}).addClass('b1').addClass('bubble').appendTo($c);
                
            }

            $c = $("<div/>").addClass('b2-container').appendTo($container);
            for (var i = 0; i < count; i++) {
                                
                var x = parseInt(Math.random() * window.innerWidth);
                var y = parseInt(Math.random() * 3000);
                
                $("<div/>").css({left:x+'px',top:y+'px'}).addClass('b2').addClass('bubble').appendTo($c);
                
            }

            $c = $("<div/>").addClass('b3-container').appendTo($container);
            for (var i = 0; i < count; i++) {
                                
                var x = parseInt(Math.random() * window.innerWidth);
                var y = parseInt(Math.random() * 1000);
                
                $("<div/>").css({left:x+'px',top:y+'px'}).addClass('b3').addClass('bubble').appendTo($c);
                
            }

            $c = $("<div/>").addClass('b4-container').appendTo($container);
            for (var i = 0; i < count; i++) {
                
                var x = parseInt(Math.random() * window.innerWidth);
                var y = parseInt(Math.random() * 3000);
                
                $("<div/>").css({left:x+'px',top:y+'px'}).addClass('b4').addClass('bubble').appendTo($c);
                
            }
            
            __bolha(window.location.href);
            
        });
        
    }
    
        
})(jQuery);
