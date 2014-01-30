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
            'keyup .content'     : '_checkSyntax',
            'click .settings'    : '_toggleOverlay',   
            'click .overlay'     : '_toggleOverlay',
            'click .delete'      : '_deletePost',
            'change .select'     : '_saveSelect',
        },

        _checkSyntax: function(e) {
            console.log(e)

            if (e.which === 13) {
                console.log('enter?');
            }
        },

        _toggleOverlay: function(e) {
            e.preventDefault();

            var $targ = $(e.currentTarget);
            if ($targ.hasClass('settings')) {
                this.$el.find('.overlay').toggleClass('hidden');
            } else if ($targ.hasClass('overlay') && e.target == e.currentTarget)  {
                this.$el.find('.overlay').toggleClass('hidden');
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


        initialize: function(opt) {
            this.model.on('change:title change:slug change:published change:kind', this.checkSave, this);

            if (this.$el.hasClass('post-full')) {
                this.model.on('change:content', this.checkSave, this);
            }

            this.stickit();
        },

        render: function() {
            /* update the text after changes 
            TODO: This is too general. Do I want to send html over wire?
            _.each(this.model.attributes, function(val, attr) {
                this.$el.find('*[data-field="' + attr + '"]').text(this.model.get(attr));
            }, this);*/

            return this;
        },

        processContent: function(content) {
            console.log('process content');
            console.log(content);
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