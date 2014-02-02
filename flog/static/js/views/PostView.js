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

    var DELETE_CONFIRM_MESSAGE = '<span class="useicons">&#xe623;</span> Are You Sure?';

    var PostView = Backbone.View.extend({

        bindings: {
            '.editable.title'            : 'title',
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
            /*'.content' : {
                observe: 'content',
                updateMethod: 'html',
                //onSet: 'processContent',
            },*/
        },

        events: {
            'click .settings-toggle'    : '_togglePostSettings', 
            'click .delete-button'      : '_deletePost', 
            'click .confirm-button'     : '_deletePost',
            'click .publish-button'     : '_togglePostPublished',
        },

        _togglePostSettings: function(e) {
            if(!$(e.target).closest('a').length){
                e.preventDefault();
                this.$el.find('.settings').slideToggle( '1500', 'linear', function() {
                    $(this).toggleClass('hidden');
                });
            }
        },

        _togglePostPublished: function(e) {
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
                     .html(SAVE_CONFIRM_MESSAGE + ' <br/>')
                     .append('<div class="button button-mini confirm-button confirm">Delete</div>')
                     .append('<div class="button button-mini confirm-button no">Keep</div>');
            }
        },

        initialize: function(opts) {
            this.listenTo(this.model, 'change:title change:category \
                            change:link_url change:pub_date  change:slug \
                            change:published change:kind', this.model.checkSave);

            if (this.$el.hasClass('post-full')) {
                this.listenTo(this.model, 'change:content', this.model.checkSave);
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
        }
    });

    return PostView;
});