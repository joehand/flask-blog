/* ========================================================================
 * Utils JS File for Writr
 * Author: JoeHand
 * ========================================================================
 */
define(['backbone', 'jquery'], function(Backbone, $) {
    var SERVER_CHECK_TIMEOUT = 5000; //time to wait between pinging server to see if it is up.

    var timeout;

    Utils = {
        checkOnlineStatus: function(obj) {
            var collection = obj.collection,
                model = obj,
                app_model = obj.parent_model;

            function checkOnline() {
                $.ajax({
                    type: 'GET',
                    success: function() { 
                        if (app_model.get('app_offline') === true) {
                            collection.syncDirtyAndDestroyed();
                            app_model.set('app_offline', false);
                            console.info('Offline data synced');
                        }
                    },
                    error: function() { 
                        console.info('Server Not Connected, Trying Again in 5 sec');
                        app_model.set('app_offline', true);

                        if(timeout) {
                            clearTimeout(timeout);
                            timeout = null;
                        }

                        timeout = setTimeout(checkOnline, SERVER_CHECK_TIMEOUT)
                    },
                });
            }
            checkOnline();
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