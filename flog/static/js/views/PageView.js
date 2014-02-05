/* ========================================================================
 * AdminView file
 * Author: JoeHand
 * ========================================================================
 */
 
define([
    'backbone',
    'underscore',
    'jquery',
    'utils',
    'views/PostView',
    'models/PostModel',
], function (Backbone, _, $, Utils, PostView, PostModel) {


    var PageView = Backbone.View.extend({

        events: {
            'click .fullscreen-button'      : '_toggleFullscreen',
            'click .preview-button'         : '_toggleContentPreview',
            'click .settings-button'        : '_togglePostSettings',
            'click .settings-close'         : '_togglePostSettings'
        },

        _toggleFullscreen: function(e) {
            if ((!document.mozFullScreen && !document.webkitIsFullScreen)) {
                Utils.launchFullscreen(document.documentElement);
            } else {
                Utils.exitFullscreen();
            }
            this.$el.find('.contract').toggleClass('hidden');
            this.$el.find('.expand').toggleClass('hidden');
            this.$el.toggleClass('zen-writing');
        },

        _togglePostSettings: function(e) {
            console.log('clicked')
            this.$el.toggleClass('settings-active')
            this.postView._togglePostSettings(e, true);
        },

        _toggleContentPreview: function(e) {
            e.preventDefault();

            this.$el.toggleClass('content-preview-active');
            this.postView.toggleContentPreview();
            this.$el.find('.preview').toggleClass('hidden');
            this.$el.find('.edit').toggleClass('hidden');
        },

        initialize: function(opts) {
            this.model.set('contentPreviewActive', false);
            this.initPosts();
            this.render();
        },

        initPosts: function() {
            var postView, el, postID;

            postId = $('.post-edit').data('id');
            el = $('*[data-id="' + postId + '"]').get(0);
            model = this.collection.get(postId);
            if (!_.isUndefined(el)) {
                this.postView = new PostView({model:model,el:el});
            }
        },

        render: function() {
            console.log('Page View rendered');
            console.log(this);
            return this;
        },

    });

    return PageView;
});