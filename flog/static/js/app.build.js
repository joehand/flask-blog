/* Builds the minified js file*/
({
    out: "../build/app.min.js",
    name: 'app',
    optimize: "uglify2",
    findNestedDependencies: true,
    paths: {
        'jquery'             : 'libs/jquery-2.0.3',
        'underscore'         : 'libs/underscore',
        'backbone'           : 'libs/backbone',
        'backboneStick'      : 'libs/backbone.stickit',
        'marked'             : 'libs/marked'
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
    }
})