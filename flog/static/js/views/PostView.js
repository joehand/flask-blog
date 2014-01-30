/* ========================================================================
 * View JS File for Writr
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore',
    'jquery',
    'utils'
], function (Backbone, _, $, Utils) {

    var SAVE_DELAY = 2000;  //delay after typing is over until we try to save

    var saveTimeout;

    var PostView = Backbone.View.extend({

        events: {
            'keyup .editable'    : '_saveChange',
            'click .delete'      : '_deletePost',
            'click .settings'    : '_toggleOverlay',   
            'click .overlay'     : '_toggleOverlay',
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

        _saveChange: function(e) {
            var $targ = $(e.currentTarget),
                field = $targ.data('field');

            this.model.set(field, $targ.text())
        },

        _toggleOverlay: function(e) {
            var $targ = $(e.currentTarget);
            if ($targ.hasClass('settings')) {
                this.$el.find('.overlay').toggleClass('hidden');
            } else if ($targ.hasClass('overlay') && e.target == e.currentTarget)  {
                this.$el.find('.overlay').toggleClass('hidden');
            }
            
        },

        initialize: function(opt) {
            this.model.on('change:title change:content change:slug', this.checkSave, this);
        },

        render: function() {
            /* update the text after changes */
            _.each(this.model.attributes, function(val, attr) {
                this.$el.find('*[data-field="' + attr + '"]').text(this.model.get(attr));
            }, this);

            return this;
        },

        checkSave: function(modelAttr) {
            var self = this;

            if(saveTimeout) {
                clearTimeout(saveTimeout);
                saveTimeout = null;
            }

            saveTimeout = setTimeout(
                function() {
                    self.model.save(null, {
                        wait:true,
                        success: function(model, rsp) {
                            self.render();
                        }
                    });
            }, SAVE_DELAY)                
        }
       
    });

    return PostView;
});