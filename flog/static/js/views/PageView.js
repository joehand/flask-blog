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
    'caret',
], function (Backbone, _, $, Utils, PostView, PostModel) {

    var keys = []

    var PageView = Backbone.View.extend({

        events: {
            'click .fullscreen-button'      : '_toggleFullscreen',
            'click .preview-button'         : '_toggleContentPreview',
            'click .settings-button'        : '_togglePostSettings',
            'click .settings-close'         : '_togglePostSettings',
            'keypress .content.editor'      : '_checkYoself',
            'change .image-upload input'    : 's3_upload'
        },

        _checkYoself: function(e) {
            if (e.which == 33) {
                //exclamation point
                keys.unshift(e.which);
            } else if (e.which == 91 && keys.length == 1) {
                //left square bracket
                var top = $('.content.editor').caret('position').top;
                console.log('i think we have image!');

                $('.image-upload').css({'top':top, 'display':'block'});
                keys = [];
            } else {
                // empty our history
                keys = [];
            }

            console.log('checking yourself');
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

        s3_upload: function(e) {
            console.log('s3 change');
            console.log(e.currentTarget.value);
            var fileName = 'imgs/' + this.postView.model.get('slug') + '-' + 
                            e.currentTarget.value.replace(/^.*\\/, '');

            
            var s3upload = new S3Upload({
                file_dom_selector: 'image-upload',
                s3_sign_put_url: '/admin/sign_s3/',
                s3_object_name: fileName,

                onProgress: function(percent, message) {
                    $('.status').html(percent + '% ' + message);
                },
                onFinishS3Put: function(url) {
                    $('.status').html('Done @ '+ url);
                    //$("#preview").html('<img src="'+url+'" style="width:300px;" />');
                },
                onError: function(status) {
                    $('.status').html('Error: ' + status);
                }
            });
        },

    });

    return PageView;
});