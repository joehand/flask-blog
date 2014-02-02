/* ========================================================================
 * AppView file
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore',
    'jquery',
    'views/AdminView', //need these here to get included in build. another way to do this?
    'views/PageView',
], function (Backbone, _, $) {

    var SUB_VIEW_EL = '.main',
        RADIO_CHECK = '&#xe628;',
        RADIO_EMPTY = '&#xe627;',
        SAVE_ICON_HIGHLIGHT = 3000, //time to highlight the save icon after saving 
        NO_CONTENT_SAVE_MESSAGE = "All content saved!",
        WINDOW_CLOSE_MESSAGE = "========================= \
                                Content not saved! Please save before going. \
                                ========================="; 

    var AppView = Backbone.View.extend({

        events: {
            'click .fullscreen'       : '_toggleFullscreen',
            'click .save-button'      : '_forceSave',
            'click .radio-button'     : '_toggleRadio',
        },

        _toggleRadio: function(e) {
            var $targ = $(e.currentTarget);

            if (!$targ.hasClass('active')) {
                $targ.parent().find('.radio-button.active')
                    .removeClass('active')
                    .find('.useicons')
                    .html(RADIO_EMPTY)
                    .parent()
                    .find('input')
                    .attr("checked", false);

                $targ.addClass('active')
                    .find('input')
                    .attr("checked", "checked")
                    .trigger("change") // needed to fire model update from stickit
                    .parent()
                    .find('.useicons')
                    .html(RADIO_CHECK);
            }
        },

        _toggleFullscreen: function(e) {
            console.log('toggling full screen');
            if ((!document.mozFullScreen && !document.webkitIsFullScreen)) {
                Utils.launchFullscreen(document.documentElement);
            } else {
                Utils.exitFullscreen();
            }
        },

        _forceSave: function(e) {
            if (this.model.get('contentDirty') === true){
                this.collection.save();
            } else {
                console.info('No changes to save');
                /* flash message */
                $el = $('<span class="no-save-hint">' + 
                        NO_CONTENT_SAVE_MESSAGE + '</span>');
                $(e.currentTarget).after($el);
                setTimeout(function(){
                    $el.slideUp("fast", function(){$(this).remove();});
                }, SAVE_ICON_HIGHLIGHT/2);
            }
        },

        initialize: function(opt) {
            var self = this;

            $(window).on("beforeunload", function(event) { self.checkSaveBeforeClose(event, self.model); });

            if (opt.childView != null) {
                /* Require our child views for specific page */
                require(['views/' + opt.childView], function (View) {
                    self.childView = new View({ 
                        el:$(SUB_VIEW_EL).get(0), 
                        collection:self.collection, 
                        model:self.model
                    });
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
            var $el = this.$el;
            $el.addClass('saving');
            setTimeout(function(){$el.removeClass('saving')}, SAVE_ICON_HIGHLIGHT);
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