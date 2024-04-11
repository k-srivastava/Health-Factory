function redirectToPath(currentType, currentID, newType, newID) {
    const currentURL = window.location.href;
    console.log(currentURL);

    window.location.href = currentURL.replace(
        `${currentType}/${currentID}`, `${newType}/${newID}`
    );
}
