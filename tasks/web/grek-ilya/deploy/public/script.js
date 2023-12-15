let editor;

$(document).ready(function () {
    editor = CodeMirror.fromTextArea(document.getElementById('code'), {
        mode: 'javascript',
        theme: 'default',
        lineNumbers: true,
        extraKeys: {"Ctrl-Space": "autocomplete"}
    });
    
    $('#libraries').select2();

    const urlParams = parseQueryString(window.location.search);
    const codeFromParams = urlParams.code;

    if (codeFromParams) {
        editor.setValue(decodeURIComponent(codeFromParams));
    } else {
        const savedCode = localStorage.getItem('savedCode');
        if (savedCode) {
            editor.setValue(savedCode);
        }
    }
    const savedLibraries = localStorage.getItem('savedLibraries');
    if (savedLibraries) {
        const librariesArray = savedLibraries.split(',');
        $('#libraries').val(librariesArray).trigger('change');
    }
        initializeSidebar();
    const savedTheme = localStorage.getItem('savedTheme');
    if (savedTheme) {
        editor.setOption('theme', savedTheme);
        $('#themes').val(savedTheme).trigger('change');
    }

    
});

function initializeSidebar() {
    const savedCodes = getSavedCodes();
    const sidebarList = $('#sidebarList');

    savedCodes.forEach((savedCode, index) => {
        const listItem = $('<li>', {
            class: 'list-group-item',
            text: (savedCode.name || `Code ${index + 1}`)
        });

        listItem.append($('<button>', {
            class: 'btn btn-danger btn-sm float-right',
            text: 'Delete',
            style: 'margin-left: 5px;',

        }).on('click', function (event) {
            event.stopPropagation();
            savedCodes.splice(index, 1);
            localStorage.setItem('savedCodes', JSON.stringify(savedCodes));
            updateSidebar();
        }));

        listItem.on('click', function () {
            editor.setValue(savedCode.code);

            sidebarList.find('li').removeClass('active');

            listItem.addClass('active');
        });

        sidebarList.append(listItem);
    });
}

function updateLibrariesAndThemes() {
    const savedLibraries = localStorage.getItem('savedLibraries');
    const librariesArray = savedLibraries ? savedLibraries.split(',') : [];
    $('#libraries').val(librariesArray).trigger('change');

    const savedTheme = localStorage.getItem('savedTheme') || 'default';
    editor.setOption('theme', savedTheme);
    $('#themes').val(savedTheme).trigger('change');
}


$('#themes').on('change', function () {
    const selectedTheme = $(this).val();
    editor.setOption('theme', selectedTheme);
    localStorage.setItem('savedTheme', selectedTheme);
});

function updateSidebar() {
    const savedCodes = getSavedCodes();
    const sidebarList = $('#sidebarList');
    sidebarList.empty();
    savedCodes.forEach((savedCode, index) => {
        const listItem = $('<li>', {
            class: 'list-group-item',
            text: savedCode.name || `Code ${index + 1}`
        });

        listItem.on('click', function () {
            editor.setValue(savedCode.code);

            sidebarList.find('li').removeClass('active');

            listItem.addClass('active');
        });

        sidebarList.append(listItem);
    });
}

function runCode() {
    const code = editor.getValue();
    const libraries = $('#libraries').val();
    const resultFrame = document.getElementById('result');
    const resultFrameDoc = resultFrame.contentDocument || resultFrame.contentWindow.document;

    try {
        resultFrameDoc.open();
        if (libraries) {
            for (const library of libraries) {
                resultFrameDoc.write('<script src="' + library + '"></script>');
            }
        }
        resultFrameDoc.write('<script>' + code + '</script>');
        resultFrameDoc.close();

        localStorage.setItem('savedCode', code);
        localStorage.setItem('savedLibraries', libraries ? libraries.join(',') : '');

        updateSidebar();
    } catch (error) {
        console.error(error);
        resultFrameDoc.open();
        resultFrameDoc.write('<p style="color: red;">Error during code execution.</p>');
        resultFrameDoc.close();
    }
}

function updateSidebar() {
    const savedCodes = getSavedCodes();
    const sidebarList = $('#sidebarList');
    sidebarList.empty();

    savedCodes.forEach((savedCode, index) => {
        const listItem = $('<li>', {
            class: 'list-group-item',
            text: savedCode.name || `Code ${index + 1}`
        });

        listItem.on('click', function () {
            editor.setValue(savedCode.code);
        });

        sidebarList.append(listItem);
    });
}

function parseQueryString(queryString) {
    const params = {};

    queryString = queryString.startsWith('?') ? queryString.slice(1) : queryString;

    const pairs = queryString.split('&');

    for (const pair of pairs) {
        const [key, value] = pair.split('=');
        const keys = key.split(/[\[\]]/).filter(Boolean);
        let current = params;

        for (let i = 0; i < keys.length; i++) {
            const k = decodeURIComponent(keys[i]);

            if (i === keys.length - 1) {
                current[k] = decodeURIComponent(value || '');
            } else {
                current[k] = current[k] || (isFinite(keys[i + 1]) ? [] : {});
                current = current[k];
            }
        }
    }

    return params;
}



function clearCode() {
    editor.setValue('');
    $('#libraries').val([]).trigger('change');
    localStorage.removeItem('savedCode');
    localStorage.removeItem('savedLibraries');

    updateSidebar();
}

function loadLibrary() {
    const libraryUrl = prompt('Enter the URL of the external library:');
    if (libraryUrl) {
        $('#libraries').append(new Option(libraryUrl, libraryUrl, true, true)).trigger('change');
    }
}

function changeTheme() {
    const selectedTheme = $('#themes').val();
    editor.setOption('theme', selectedTheme);

    localStorage.setItem('savedTheme', selectedTheme);
}

function shareCode() {
    const code = encodeURIComponent(editor.getValue());
    const libraries = encodeURIComponent($('#libraries').val().join(','));
    const url = `${window.location.origin}${window.location.pathname}?code=${code}&libraries=${libraries}`;

    const linkContainer = $('#shareLink');
    linkContainer.empty();
    const linkElement = $('<a>', {
        href: url,
        text: 'Share this link',
        target: '_blank',
        rel: 'noopener noreferrer'
    });
    linkContainer.append(linkElement);
    linkContainer.show();
}

function getSavedCodes() {
    const savedCodesString = localStorage.getItem('savedCodes');
    return savedCodesString ? JSON.parse(savedCodesString) : [];
}

function saveCode() {
    const currentCode = editor.getValue();
    const savedCodes = getSavedCodes();

    const codeName = prompt('Enter a name for this code (optional):');

    savedCodes.push({
        name: codeName,
        code: currentCode
    });

    localStorage.setItem('savedCodes', JSON.stringify(savedCodes));

    updateSidebar();
}
