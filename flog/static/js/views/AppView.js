/* ========================================================================
 * AppView file
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore',
    'jquery',
], function (Backbone, _, $) {
    var SAVE_ICON_HIGHLIGHT = 3000, //time to highlight the save icon after saving 
        WINDOW_CLOSE_MESSAGE = "========================= \
                                Content not saved! Please save before going. \
                                ========================="; 

    var AppView = Backbone.View.extend({

        events: {
            'click .fullscreen' : '_toggleFullscreen',
            'click .save'       : '_forceSave'
        },

        _toggleFullscreen: function(event) {
            console.log('toggling full screen');
            if ((!document.mozFullScreen && !document.webkitIsFullScreen)) {
                Utils.launchFullscreen(document.documentElement);
            } else {
                Utils.exitFullscreen();
            }
        },

        _forceSave: function(event) {
            this.saveContent();
        },

        initialize: function(opt) {
            var self = this;

            $(window).on("beforeunload", function(event) { self.checkSaveBeforeClose(event, self.model); });

            if (opt.childView != null) {
                /* Require our child views for specific page */
                require(['views/' + opt.childView], function (View) {
                    self.childView = new View({ el:$('.main').get(0), collection:self.collection, model:self.model });
                    self.render();
                });
            } else {
                self.render();
            }

            this.listenTo(this.collection, 'change', this.setDirtyContent, this);
            this.listenTo(this.collection, 'sync', this.serverSync, this);
            this.listenTo(this.collection, 'error', this.serverError, this);
        },

        render: function() {
            console.log(this);
            return this;
        },

        setDirtyContent: function() {
            this.model.set('contentDirty', true);
        },

        serverError: function() {
            console.error('Server Error');
        },

        serverSync: function() {
            console.info('server sync');
            this.model.set('contentDirty', false);
            this.showVisualSave();
        },

        showVisualSave: function() {
            var $icon = this.$el.find('.save');

            $icon.addClass('saving');
            setTimeout(function(){$icon.removeClass('saving')}, SAVE_ICON_HIGHLIGHT);
        },

        checkSaveBeforeClose: function(e, model) {
            if (model.get('contentDirty')) {
                e = window.event;

                if (e) {
                    e.returnValue = WINDOW_CLOSE_MESSAGE;
                }
                return WINDOW_CLOSE_MESSAGE;
            }
        }

    });

    return AppView;
});