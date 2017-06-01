function convertToJsArray(jsonArray){
	tmpArray = new Array();

	for (var i = 0; i < jsonArray.length; i++){
			tmpArray.push(jsonArray[i]);
	}

	return tmpArray;
}

d3.selection.prototype.moveToFront = function(){
	return this.each(function(){
		this.parentNode.appendChild(this);
	});
};

d3.selection.prototype.moveToBack = function(){
	return this.each(function(){
		var firstChild = this.parentNode.firstChild;
		if (firstChild){
			this.parentNode.insertBefore(this, firstChild);
		}
	});
};


function getCookie(c_name){
	if (document.cookie.length > 0){
	    c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1){
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
       }
 	}
	return "";
}


function measureStringWidth(text, font){
	var canvas = document.createElement("canvas");
	var ctx = canvas.getContext("2d");
	ctx.font = font;
	return ctx.measureText(text).width;
}