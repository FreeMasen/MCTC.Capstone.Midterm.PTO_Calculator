const gulp = require('gulp');
const sass = require('gulp-sass');
const bs = require('browser-sync');
const exec = require('child_process').exec;
const path = require('path');

gulp.task('runserver', () => {
    let proc = exec('python app.py');
});

gulp.task('browser-sync', ['runserver'], () => {
    bs({
        notify: true,
        proxy: 'localhost:5000'
    })
});

gulp.task('scss', () => {
    return gulp.src(['website/static/scss/*.scss'])
            .pipe(sass().on('error', sass.logError))
            .pipe(gulp.dest('website/static/css'))
});

gulp.task('watch', () => {
    gulp.watch(['website/static/scss/*.scss'], ['scss'])
    gulp.watch(['website/**/*.html',
                'website/**/*.js',
                'website/**/*.css'])
        .on('change', bs.reload);
});

gulp.task('default', ['watch', 'browser-sync'])