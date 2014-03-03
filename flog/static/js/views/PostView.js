/* ========================================================================
 * View JS File for Writr
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore',
    'jquery',
    'marked'
], function (Backbone, _, $, marked) {

    var DELETE_CONFIRM_MESSAGE = '<span class="useicons">&#xe623;</span> Are You Sure?';

    var PostView = Backbone.View.extend({

        bindings: {
            /* Post List Items */
            'a.title'                    : 'title',
            'span.kind'                  : 'kind',

            /* Post Setting Items */
            'input.title'                : 'title',
            'input.slug'                 : 'slug',
            'input.link_url'             : 'link_url',
            'input.category'             : 'category',
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

            /* Single Page Items */
            '.title.editor'              : 'title',
            '.link_url.editor'           :  {
                observe: 'link_url',
                updateView: false,
            },
            '.category.editor'            : {
                observe: 'category',
            },
            '.content.editor' : {
                observe: 'content',
                updateMethod: 'text',
                updateView: false,
            },
            '.word-count' : 'words',
        },

        events: {
            'click .settings-toggle'    : '_togglePostSettings', 
            'click .delete-button'      : '_deletePost', 
            'click .confirm-button'     : '_deletePost',
            'click .publish-button'     : '_togglePostPublished',
        },

        _togglePostSettings: function(e, postPage) {
            if(!$(e.target).closest('a').length || postPage === true){
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
            var self = this;

            if ($targ.hasClass('no')) {
                console.log('here');
                $targ.parent()
                    .html('Delete');
            }

            if ($targ.hasClass('confirm')) {
                self.model.destroy({
                    error:  function(model, resp) {
                        console.log(resp);
                    }
                });
                self.$el.animate({
                    opacity: 0.05,
                    left: "-=2000",
                    height: "0"
                  }, 1000, function() {
                    // Animation complete.
                    $('html, body').animate({scrollTop:0}, 'slow');
                    self.remove();
                    self.unbind();
                  });
            } else {
                $targ
                     .html(DELETE_CONFIRM_MESSAGE + ' <br/>')
                     .append('<div class="button button-mini confirm-button confirm">Delete</div>')
                     .append('<div class="button button-mini confirm-button no">Keep</div>');
            }
        },

        initialize: function(opts) {
            this.contentPreviewActive = false;

            this.listenTo(this.model, 'change:title change:category \
                            change:link_url change:pub_date  change:slug \
                            change:published change:kind', this.model.checkSave);

            if (this.$el.hasClass('post-edit')) {
                this.adjustContentSize();

                this.listenTo(this.model, 'change:content', this.model.checkSave);
                this.listenTo(this.model, 'change:content', this.adjustContentSize);
            }

            this.render();
        },

        render: function() {
            this.stickit();
            console.log(this);
            return this;
        },

        adjustContentSize: function() {
            $("textarea").height( $("textarea")[0].scrollHeight );
        },

        toggleContentPreview: function() {
            if (this.contentPreviewActive === true) {
                this.$el.find('.content.editor').show()
                this.$el.find('.content-preview').hide()
                this.contentPreviewActive = false;
            } else {
                var content = this.model.get('content');
                if (!_.isUndefined(this.model.get('content'))) {
                    content = marked(this.model.get('content'));
                }
                this.$el.find('.content.editor').hide()
                this.$el.find('.content-preview')
                    .html(content)
                    .show()
                this.contentPreviewActive = true;
            }
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