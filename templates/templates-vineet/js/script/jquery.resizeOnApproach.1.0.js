(function($){
    $.fn.resizeOnApproach = function(settings){
    
    
    
        var config = {
            'elementDefault': 35,
            'elementClosest': 55,
            'triggerDistance': 200,
			'setWidthAndHeight':false
			
        };
        
        if (settings) 
            $.extend(config, settings);
        
       
        
        
        var setWidthAndHeight=config.setWidthAndHeight;
        var expandIcon = this;
        var imgSize = config.elementDefault;
        var imgMax = config.elementClosest;
        var trigger = config.triggerDistance
        
        var max = imgMax - imgSize;
        
        var factor = max / trigger;
        var resized = false;
        $(document).ready(function(){
            expandIcon.each(function(){
                this.style.width = imgSize + 'px';
				if (setWidthAndHeight) {
				           this.style.height = imgSize + 'px';
				}
            });
        });

        $(document).mousemove(function(e){
       
        
               
			   
        
            var mouseX = e.pageX;
            var mouseY = e.pageY;
            expandIcon.each(function(){
                //how far away the top left corner of the element is from the corner of the window
                var pos = $(this).offset();
                //calculate the distance from the mouse poiter to the centre of the square. Sum takes into account that the image position is taken from corner
                var dist = distToSqEdge(this.width, pos.left +
                (this.width / 2), pos.top +
                (this.height / 2), mouseX, mouseY);
                //set the distance to zero if inside the square
                
                if (dist < trigger) {
                    if (dist < 0) {
                        dist = 0;
                    }
                    resized = true;
                    var size = imgSize +
                    (max - (dist * factor));
                    this.style.width = size + 'px';
					if (setWidthAndHeight) {
						this.style.height = size + 'px';
					}
                }
                else {
                    this.style.width = imgSize + 'px';
					if (setWidthAndHeight) {
					       this.style.height = imgSize + 'px';
					}
                }
                
            });
            
        });
    }
    
})(jQuery)





















//returns the distance from the edge of the square of the given width and centre C to the
//point P. If the distance is negative, the mouse in within the square
function distToSqEdge(sqWidth, cx, cy, px, py){
    //length of line from point to centre
    var pl = Math.sqrt((cx - px) * (cx - px) +
    (cy - py) *
    (cy - py));
    
    //the x and y length of the line
    vx = px - cx;
    vy = py - cy;
    
    //determine the unit vector to the side the line intersects the square
    var Xx = 0;
    var Xy = 0;
    if (vx > vy) {
        if (vx > -vy) {
            Xx = 1;
        }
        else {
            Xy = 1;
        }
    }
    else {
        if (vx > -vy) {
            Xy = -1;
        }
        else {
            Xx = -1;
        }
    }
    
    // determine the unit vector of line to mouse point
    vlength = Math.sqrt((vx * vx) + (vy * vy));
    
    vux = vx / vlength;
    
    vuy = vy / vlength;
    
    cosA = vux * Xx + vuy * Xy;
    
    //distance from centre to the edge of the square
    centreToSqEdge = Math.abs((0.5 * sqWidth) / cosA);
    
    mouseToSquareEdge = vlength - centreToSqEdge;
    return mouseToSquareEdge;
    
}
