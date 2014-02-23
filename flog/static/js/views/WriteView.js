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
    'atwho',
    'modals',
], function (Backbone, _, $, Utils, PostView, PostModel) {

    var WriteView = Backbone.View.extend({

        events: {
            'click .fullscreen-button'      : '_toggleFullscreen',
            'click .preview-button'         : '_toggleContentPreview',
            'click .settings-button'        : '_togglePostSettings',
            'click .settings-close'         : '_togglePostSettings',
            'change .image-upload input'    : '_beginImageUpload',
        },

        _beginImageUpload: function(e) {
            // make sure image was chosen
            // TODO: check file types(?), could also do on server-side?
            if (e.currentTarget.value !== '') {
                this.initS3Upload(e);
            }
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

            this.$contentInput = $('textarea.content');
            this.initAutoComplete();

            if (this.model.get('daily_words')) {
                this.updateProgressBar();
                this.listenTo(this.postView.model, 'change:content', this.updateProgressBar, this);
            }

            this.render();
        },

        render: function() {
            console.log('Page View rendered');
            console.log(this);

            return this;
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

        initAutoComplete: function() {
            var self = this,
                $inputEl = this.$contentInput,
                autoComplete = [
                    {'name' : 'image', 'content' : '![img]()'},
                    {'name':"link", 'content':'[link]()'},
                ];

            $inputEl.on("inserted.atwho", function(event, $li, context) {
                $inputEl.caret('pos', context.query.head_pos + 6);
            });

            $inputEl.atwho({ 
                at: "[", 
                data: autoComplete,
                tpl: "<li data-value='${content}'>${name}</li>",
                callbacks: {
                    before_insert: function(value, $li) {
                        if (value.indexOf("img") != -1) {
                            // get ready to upload image
                            self.showImageUpload();
                        }

                        return value;
                     }
                }
            });
        },

        updateProgressBar: function() {
            var $el = $('.progress-bar'),
                goal = $el.data('goal'),
                count = this.postView.model.get('words');
            if (goal > count) {
                $el.width(count/goal * 100 + '%');
                if (!_.isUndefined(this.postView.model.get('end_time'))) {
                    this.postView.model.set('end_time', undefined); // reset if we finished before
                }
            } else if (!_.isUndefined(count)) {
                $el.addClass('met');
                $el.width('100%');
                if (_.isUndefined(this.postView.model.get('end_time'))) {
                    this.postView.model.set('end_time', Date.now());
                }
            }
        },

        showImageUpload: function() {
            // Simulate Input Click to Show File Browser
            $('.image-upload input[type=file]').trigger('click');
            $('.image-upload').modal('show')
        },

        insertTextAtCurrentPos: function(text) {
            // Insert Text At Current Caret Position
            var output = '',
                source = this.$contentInput.val(),
                pos = this.$contentInput.caret('pos');

            output = source.substring(0, pos) + text + source.substring(pos);
            this.$contentInput.val(output);
        },

        initS3Upload: function(e) {
            var self = this,
                fileName = 'imgs/' + this.postView.model.get('slug') + '-' + 
                            e.currentTarget.value.replace(/^.*\\/, '');

            if (!_.isUndefined(fileName)) {
                var s3upload = new S3Upload({
                    file_dom_selector: 'image-upload',
                    s3_sign_put_url: self.model.get('signS3URL'),
                    s3_object_name: fileName,

                    onProgress: function(percent, message) {
                        $('.status').html(percent + '% ' + message);
                    },
                    onFinishS3Put: function(url) {
                        // insert image URL in text area
                        self.insertTextAtCurrentPos(url);
                        self.$contentInput.trigger('change');
                        $('.status').html('<span class="small-caps">Uploaded to</span><br/>'+ url);
                        $(".image-preview").html('<img src="'+url+'" style="max-width:300px;" />');
                    },
                    onError: function(status) {
                        $('.status').html('Error: ' + status);
                    }
                });   
            }
            
        },

    });

    return WriteView;
});