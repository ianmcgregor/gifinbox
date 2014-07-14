(function() {
	var images = document.querySelectorAll('img');

	function isScrolledIntoView(el) {
		var height = window.innerHeight;
	    var top = window.pageYOffset;
	    var bottom = top + height;
	    var elTop = el.getBoundingClientRect().top + top;
	    var elBottom = elTop + el.offsetHeight;
	    return elBottom >= top && elTop <= bottom;
	}

	function loadImage(el) {
		if(!el.hasAttribute('src')) {
			var src = el.getAttribute('data-src');
			el.setAttribute('src', src);
		}
		el.style.visibility = 'visible';
	}

	function loadImages() {
		for (var i = 0; i < images.length; i++) {
			var el = images[i];
			if(isScrolledIntoView(el)) {
				loadImage(el);
			}
			else {
				el.style.visibility = 'hidden';
			}
		}
	}

	document.addEventListener('scroll', loadImages);
	window.addEventListener('resize', loadImages);

	var l = images.length;
	for (var i = 0; i < l; i++) {
		var img = images[i];
		img.classList.add('placeholder');
		img.style.height = Math.round(window.innerWidth*0.75) + 'px';
		img.onload = function() {
			this.style.height = 'auto';
			//this.parentElement.style.height = this.height + 'px';
		};
		if(i < 3) {
			loadImage(img);
		}
	}
}());