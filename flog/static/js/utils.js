/* ========================================================================
 * Utils JS File for Writr
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore',
    'jquery',
    'marked',
], function (Backbone, _, $, marked) {

    marked.setOptions({
        sanitize: false,
        smartypants: true
    });

    Utils = {
        extractEditableText: function (text) {
            var outText = '', temp = '',
                $elem = $(document.createElement('div')).html(text);

            /* get text not in children first */
            outText = marked($elem
                .clone()    //clone the element
                .children() //select all the children
                .remove()   //remove all the children
                .end()  //again go back to selected element
                .text());

            if ($elem.children().length > 0) { 
                $elem.children().each(function() {
                    tag = this.tagName;

                    if (_.contains(['P', 'BR', 'DIV'], tag)) {
                        temp = this.innerHTML;
                        temp = $('<div/>').html(temp).text();
                        temp = marked(temp);
                    } else {
                        if ($(this).text().length > 0) {
                            temp = $(this).wrap('<div>').parent().html();
                        } else {
                            temp = ''
                        }
                    }

                    outText += temp;
                }); 
            }

            outText += '<br/>'; // better functionality with br at end

            return(outText.replace(/\r?\n/g, ""));
        },

        // Find the right method, call on correct element
        launchFullscreen : function(element) {
            if(element.requestFullscreen) {
                element.requestFullscreen();
            } else if(element.mozRequestFullScreen) {
                element.mozRequestFullScreen();
            } else if(element.webkitRequestFullscreen) {
                element.webkitRequestFullscreen();
            } else if(element.msRequestFullscreen) {
                element.msRequestFullscreen();
            }
        },

        exitFullscreen : function () {
            if(document.exitFullscreen) {
                document.exitFullscreen();
            } else if(document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if(document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            }
        },
    };

    return Utils;
});