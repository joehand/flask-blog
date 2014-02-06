/* ========================================================================
 * AppView file
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore',
    'jquery',
    'Utils',
    'views/AdminView', //need these here to get included in build. another way to do this?
    'views/PageView',
], function (Backbone, _, $, Utils) {

    var SUB_VIEW_EL = '.main',
        RADIO_CHECK = '&#xe628;',
        RADIO_EMPTY = '&#xe627;',
        SAVE_DELAY = 4000, //time to show saved message 
        SAVING_MESSAGE = "Saving...",
        SAVED_MESSAGE = "Saved",
        WINDOW_CLOSE_MESSAGE = "========================= \
                                Content not saved! Please save before going. \
                                ========================="; 

    var AppView = Backbone.View.extend({

        events: {
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
            this.$el
                .find('.save-message')
                .text(SAVING_MESSAGE);
        },

        serverError: function() {
            console.error('Server Error');
        },

        serverSync: function() {
            console.info('server sync');
            this.model.set('contentDirty', false);
            this.showSaved();
            //this.checkDirty();
        },

        checkDirty: function() {
            // TODO: re-write this for my use case
            console.log('check dirty');
            if (this.collection.dirtyModels().length > 0) {
                console.log('has dirty');
                // we are offline, start checking when server is back
                Utils.checkOnlineStatus(this);
            }
        },

        showSaved: function() {
            var $el = this.$el,
                $saveEl = $el.find('.save-message');
            $el.addClass('saving');
            $saveEl.text(SAVED_MESSAGE);
            setTimeout(function(){
                $el.removeClass('saving');
                $saveEl.text('')
            }, SAVE_DELAY);
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