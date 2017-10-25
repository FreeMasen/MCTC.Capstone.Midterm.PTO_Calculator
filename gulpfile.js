const gulp = require('gulp');
const sass = require('gulp-sass');
const bs = require('browser-sync');
const exec = require('child_process').spawn;
const path = require('path');

gulp.task('runserver', () => {
    let proc = exec('python', ['app.py']);
    proc.stdout.on('data', data => {
        console.log(data.toString());
    });
    proc.stderr.on('data', data => {
        console.error(data.toString());
    });
    proc.stdin.on('data', data => {
        console.log(data.toString())
    })
    proc.on('close', code => {
        console.log('closing app.py with code', code);
    });
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