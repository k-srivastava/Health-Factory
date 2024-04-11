function getValidData(dataJSON, fields) {
    const dataName = document.getElementById('search-box').value.toLowerCase();
    const validData = [];

    // Show the name of the first five pieces of data if the search box is empty.
    if (dataName === '') {
        return dataJSON.slice(0, 5);
    }

    for (let data of dataJSON) {
        for (let field of fields) {
            if (data[field].toString().toLowerCase().includes(dataName)) {
                validData.push(data);
                break;
            }
        }
    }

    return validData.slice(0, 6);
}

function getMatchingResult(dataJSON, fields, validListID, dataType) {
    const validData = getValidData(dataJSON, fields);

    const validList = document.getElementById(validListID);
    validList.innerHTML = null;

    for (let data of validData) {
        const li = document.createElement('li');

        let innerHTML = `<li>${data.id}`;
        for (let field of fields) {
            if (field !== 'id') {
                innerHTML += ` ${data[field]}`;
            }
        }
        innerHTML += `</li>`;
        li.innerHTML = innerHTML;

        li.addEventListener('click', () => {
            window.location.href = `${dataType}/${data.id}`
        });

        validList.appendChild(li);
    }
}