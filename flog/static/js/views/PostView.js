/* ========================================================================
 * View JS File for Writr
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore',
    'jquery',
    'utils',
], function (Backbone, _, $, Utils) {

    var SAVE_DELAY = 2000;  //delay after typing is over until we try to save

    var saveTimeout;

    var PostView = Backbone.View.extend({

        bindings: {
            '.title'   : 'title',
            '.content' : {
                observe: 'content',
                updateMethod: 'html',
                onSet: 'processContent',
            }
        },

        events: {
            'click .settings-toggle'    : '_toggleOverlay', 
            'click .delete'      : '_deletePost',
            'change .select'     : '_saveSelect',
        },

        _toggleOverlay: function(e) {
            if(!$(e.target).closest('a').length){
                e.preventDefault();
                this.$el.find('.settings').slideToggle( '1500', "linear", function() {
                    $(this).toggleClass('hidden');
                });
            }
        },


        _deletePost: function(e) {
            /* TODO: give a warning first */
            this.model.destroy({
                error:  function(model, resp) {
                    console.log(resp);
                }
            });

            this.remove();
        },
        _saveSelect: function(e) {
            var val = $(e.currentTarget).val(),
                field = $(e.currentTarget).data('select');

            this.model.set(field, val);
        },

        initialize: function(opts) {
            this.model.on('change:title change:slug change:published change:kind', this.checkSave, this);

            if (this.$el.hasClass('post-full')) {
                this.model.on('change:content', this.checkSave, this);
            }

            this.stickit();
        },

        render: function() {
            return this;
        },

        checkFilter: function(filter) {
            if (this.model.isInFilter(filter)) {
                this.shown = true;
                this.$el.slideDown().removeClass('hidden');
                return true;
            } else {
                this.shown = false;
                this.$el.slideUp().addClass('hidden');
                return false;
            }
        },

        processContent: function(content) {
            content = Utils.extractEditableText(content)
            return content.trim();
        },

        checkSave: function() {
            var self = this;

            console.log('checking save');
            console.log(this.model.changed);

            if(saveTimeout) {
                clearTimeout(saveTimeout);
                saveTimeout = null;
            }

            saveTimeout = setTimeout(
                function() {
                    self.model.save(null, {
                        wait:true,
                        success: function(model, rsp) {
                            /* TODO: This is too general. Do I want to send html over wire?
                            self.render();*/
                        }
                    });
            }, SAVE_DELAY)                
        }
       
    });

    return PostView;
});