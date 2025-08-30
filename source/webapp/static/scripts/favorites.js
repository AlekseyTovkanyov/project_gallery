async function makeRequest(url, method = "POST", body) {
    let headers = {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
    };

    const response = await fetch(url, {
        method: method,
        headers: headers,
        body: JSON.stringify(body)
    });

    if (response.ok || response.status === 204) {
        if (response.status === 204) {
            return {};
        }
        return await response.json();
    } else {
        let error = await response.text();
        console.error('Request failed:', error);
        throw new Error(error);
    }
}

async function onClickFavorite(event) {
    event.preventDefault();

    let button = event.currentTarget;
    let photoId = button.dataset.photoId;
    let albumId = button.dataset.albumId;
    let action = button.dataset.action;

    button.disabled = true;

    let url = `/favorites/${action}/`;
    let body = {};

    if (photoId) {
        body.photo_id = photoId;
    }
    if (albumId) {
        body.album_id = albumId;
    }

    try {
        let data = await makeRequest(url, action === 'add' ? 'POST' : 'DELETE', body);

        if (action === 'add') {
            button.textContent = 'Удалить из избранного';
            button.dataset.action = 'remove';
            button.className = 'btn btn-sm btn-danger';
        } else if (action === 'remove') {
            button.textContent = 'Добавить в избранное';
            button.dataset.action = 'add';
            button.className = 'btn btn-sm btn-success';
        }
    } catch (error) {
        console.error('Error handling favorite button click:', error);
    } finally {
        button.disabled = false;
    }
}

function onLoad() {
    let favoriteButtons = document.querySelectorAll('[data-js="favorite-button"]');
    for (let button of favoriteButtons) {
        button.addEventListener('click', onClickFavorite);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.addEventListener('load', onLoad);