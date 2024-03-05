const filePath = '../../static/images';

/**
 * Change the image displayed on the homepage of the application based on what thumbnail is currently selected.
 * @param {string} imageSource Relative path of the image within the static/images directory.
 */
function thumbnailPicker(imageSource) {
    document.querySelector('.current-image').src = `${filePath}/${imageSource}`;
}