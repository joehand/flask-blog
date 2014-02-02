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
            'a.title'                    : 'title',
            'input.title'                : 'title',
            'input.slug'                 : 'slug',
            'input.link_url'             : 'link_url',
            'input.category'             : 'category',
            'span.kind'                  : 'kind',
            'input[type=radio].kind '    : {
                observe: 'kind',
                updateModel: function(val, e, opts) {
                    return !_.isUndefined(val); //something was being tricky and making undefined
                }
            },
            'input.pub_date'             : {
                observe: 'pub_date',
                updateView: false,
            },
            '.content' : {
                observe: 'content',
                updateMethod: 'html',
                onSet: 'processContent',
            },
        },

        events: {
            'click .settings-toggle'    : '_toggleOverlay', 
            'click .delete-button'      : '_deletePost', 
            'click .confirm-button'      : '_deletePost',
            'change .select'            : '_saveSelect',
            'click .publish-button'     : '_togglePublished',
        },

        _togglePublished: function(e) {
            var $targ = $(e.currentTarget),
                published = this.model.get('published');
            
            if (!published) {
                $targ.html('Unpublish');
            } else {
                $targ.html('Publish!');
            }

            this.model.set('published', !published);
            $targ.toggleClass('published');
            this.$el.toggleClass('published');
        },

        _toggleOverlay: function(e) {
            if(!$(e.target).closest('a').length){
                e.preventDefault();
                this.$el.find('.settings').slideToggle( '1500', 'linear', function() {
                    $(this).toggleClass('hidden');
                });
            }
        },

        _deletePost: function(e) {
            var $targ = $(e.target);

            if ($targ.hasClass('no')) {
                console.log('here');
                $targ.parent()
                    .html('Delete');
            }

            if ($targ.hasClass('confirm')) {
                this.model.destroy({
                    error:  function(model, resp) {
                        console.log(resp);
                    }
                });
                this.$el.animate({
                    opacity: 0.05,
                    left: "-=2000",
                    height: "0"
                  }, 1000, function() {
                    // Animation complete.
                    $('html, body').animate({scrollTop:0}, 'slow');
                    this.remove();
                  });
            } else {
                $targ
                     .html('<span class="useicons">&#xe623;</span> Are You Sure? <br/>')
                     .append('<div class="button button-mini confirm-button confirm">Delete</div>')
                     .append('<div class="button button-mini confirm-button no">Keep</div>');
            }

        },

        _saveSelect: function(e) {
            var val = $(e.currentTarget).val(),
                field = $(e.currentTarget).data('select');

            this.model.set(field, val);
        },

        initialize: function(opts) {
            this.model.on('change:title change:category \
                            change:link_url change:pub_date  change:slug \
                            change:published change:kind', this.checkSave, this);

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