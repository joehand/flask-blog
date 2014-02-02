/* ========================================================================
 * AdminView file
 * Author: JoeHand
 * ========================================================================
 */
 
define([
    'backbone',
    'underscore',
    'jquery',
    'views/PostView',
    'models/PostModel',
], function (Backbone, _, $, PostView, PostModel) {


    var PageView = Backbone.View.extend({

        events: {
            'click .preview-button'  : '_toggleContentPreview',
            'click .settings-button' : '_togglePostSettings'
        },

        _togglePostSettings: function(e) {
            this.$el.toggleClass('settings-active')
            this.postView._togglePostSettings(e, true);
        },

        _toggleContentPreview: function(e) {
            console.log('previewing');
            e.preventDefault();

            this.$el.toggleClass('content-preview-active')
            this.postView.toggleContentPreview();
        },

        initialize: function(options) {
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