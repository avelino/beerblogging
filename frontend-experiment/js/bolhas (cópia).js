(function($) {
            
    var count = 150;
        
    $(function() {
        var mousex=oldmx=0;
        var mousey=oldmy=0;
        var alterx=altery=0;
        var cookies=new Array();
        var cookies_top=new Array();
        var cookies_left=new Array();
        var cookies_spd=new Array();
        var dist;
        var time=0;
        var st=0;
        var margin=150;
        var tam;

        $(document).mousemove(function(e){
            mousex=e.pageX;
            mousey=e.pageY;
        }); 

        $('<div id="cookie-master"></div>').appendTo('#container-cookies').bolha();

        for (var i = 0; i < count; i++) {
              cookies[i]=  $('#'+i);
                var atual = $("#"+i).css('top');
                var abc = "";
                abc = atual;
                abc = abc.substring(0, abc.length - 2);
                cookies_top[i]=Number(abc);            
                atual = $("#"+i).css('left');
                abc = "";
                abc = atual;
                abc = abc.substring(0, abc.length - 2);  
                cookies_left[i]=Number(abc);
                tam= parseInt(Math.random()*5)+7;
                cookies[i].css('width', (tam)+'px');  
                cookies[i].css('height', (tam)+'px');
                cookies_spd[i]=0-((Math.random()*2)+1)    
        }
        function animaCookie() {    
            time++;
            if((mousex==0)&&(mousey==0)){
                alterx=altery=0;
            }else{
                alterx=(mousex-oldmx);
                altery=(mousey-oldmy);                
            }
            oldmx=mousex;
            oldmy=mousey;
            //if(time%2 == 1){                
                st=$(window).scrollTop() ;
                sh=$(window).height() ;                
            //}
            for (var i = 0; i < count; i++) {

                cookies_top[i]+= cookies_spd[i];

                if(cookies_top[i]<250){
                    cookies[i].css('opacity', (70-(250-cookies_top[i]))/140);
                    //cookies_spd[i]=
                }else{
                    cookies[i].css('opacity', 0.5);
                }

                if((cookies_top[i]< st-margin)||(cookies_top[i]< 180)){
                    var y = parseInt(Math.random() * margin)+st+sh;
                    if(y>$(document).height()-10){                    
                        y =$(document).height()- parseInt(Math.random() * 150);
                    }
                    cookies_top[i]=y;
                }
                if(cookies_top[i]> st+sh+margin){                    
                    var y = st-parseInt(Math.random() * margin);
                    cookies_top[i]=y;
                }

                dist=Math.sin(cookies_top[i]/40)*20;
                /*
                var hip=Math.sqrt(((cookies_left[i]-mousex)*(cookies_left[i]-mousex))+((cookies_top[i]-mousey)*(cookies_top[i]-mousey)));            
                if(hip<200){       
                    cookies_left[i]+=alterx*((200-hip)/2000);
                    cookies_top[i]+=altery*((200-hip)/2000);
                }
                */
                if((cookies_left[i]+dist)< 30){
                    cookies_left[i]=(window.innerWidth-30)+(cookies_left[i]-30);
                }
                if((cookies_left[i]+dist)>window.innerWidth-30){
                    cookies_left[i]=30+(cookies_left[i]-(window.innerWidth-30));
                }

                cookies[i].css('top', cookies_top[i]+'px');
                cookies[i].css('left', cookies_left[i]+dist+'px');
            }
            window.setTimeout(animaCookie, 1);
        }
        
        animaCookie();

    });
    
    $.fn.bolha = function() {
        
        return this.each(function() {
            var $obj = $(this);
            for (var i = 0; i < count; i++) {
                
                var x = parseInt(Math.random() * window.innerWidth);
                var y = parseInt(Math.random() *(300+$(window).height()))+$(window).scrollTop()-100;
                
                $("<div id='" + i + "'></div>").css({left:x+'px',top:y+'px'}).addClass('cookie').appendTo('#cookie-master');
                
            }
            
        });
        
    }
    
        
})(jQuery);
