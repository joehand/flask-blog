requirejs.config({
    paths: {
        'jquery'             : 'libs/jquery-2.1.1',
        'underscore'         : 'libs/underscore',
        'backbone'           : 'libs/backbone',
        'backboneStick'      : 'libs/backbone.stickit',
        'marked'             : 'libs/marked',
        's3upload'           : 'libs/s3upload',
        'caret'              : 'libs/jquery.caret',
        'atwho'              : 'libs/jquery.atwho',
        'modals'             : 'libs/modal',
        'slide'              : 'libs/bigSlide',
    },
    shim: {
        backbone: {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },
        backboneStick: {
            deps: ['backbone'],
        },
        underscore: {
            exports: '_'
        },
        marked: {
            exports: 'marked'
        },
        s3upload: {
            deps: ['jquery', 'underscore'],
            exports: 'S3Upload'
        },
        caret: {
            deps: ['jquery']
        },
        atwho: {
            deps: ['jquery', 'caret']
        },
        modals: {
            deps: ['jquery']
        },
        slide: {
            deps: ['jquery']
        },
    }
});

// Load the main app module to start the app
requirejs(["main"]);
