/*
 *
 * Copyright (c) 2006 Sam Collett (http://www.texotela.co.uk)
 * Licensed under the MIT License:
 * http://www.opensource.org/licenses/mit-license.php
 * 
 */

/*
 * Converts image and link elements to thumbnails
 *
 * @name     jThumb
 * @author   Joan Piedra (http://www.joanpiedra.com)
 * @example  $("a.thumb, img.thumb").thumbs();
 *
 */
jQuery.fn.thumbs = function()
{
	/*return this.wrap('<div class="thumb-img"><div class="thumb-inner">' + '</div><div class="thumb-strip"></div><div class="thumb-zoom"></div></div>'); */
    return this.wrap('<div class="thumb-outer"><div class="thumb-img"><div class="thumb-inner">' + '</div></div><div class="thumb-zoom"></div></div>');
}

/*
 * Absolute positions the image in the middle of the thumbnail frame
 *
 * @name     jThumbImg
 * @author   Joan Piedra (http://www.joanpiedra.com)
 * @example  $("a.thumb img, img.thumb").thumbsImg();
 *
 */
jQuery.fn.thumbsImg = function()
{
	return this.each(
		function()
		{
		  jQuery(this).center(); /* needs jquery.center.js */
		 
		}
	)
}