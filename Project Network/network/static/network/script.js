function getCSRFToken() {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length, cookie.length);
        }
    }
    return '';
}

function editPost(postId) {
    const contentElement = document.getElementById(`post-content-${postId}`);
    const originalContent = contentElement.innerHTML.trim();

    contentElement.innerHTML = `
        <textarea id="edit-content-${postId}" class="form-control">${originalContent}</textarea>
        <button class="btn btn-primary mt-2" onclick="savePost(${postId})">Save</button>
        <button class="btn btn-secondary mt-2" onclick="cancelEdit(${postId}, '${originalContent}')">Cancel</button>
    `;
}

function savePost(postId) {
    const newContent = document.getElementById(`edit-content-${postId}`).value.trim();

    if (!newContent) {
        alert("Content cannot be empty.");
        
        return;
    }

    fetch(`/edit_post/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },

        body: `content=${encodeURIComponent(newContent)}`


    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {

            alert(data.error);
        } else {
            document.getElementById(`post-content-${postId}`).innerHTML = data.content;
        }
    })
}

function cancelEdit(postId, originalContent) {
    document.getElementById(`post-content-${postId}`).innerHTML = originalContent;
}
function toggleLike(postId) {

    fetch(`/like_unlike_post/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        }


    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            
            alert(data.error);
        } else {
            document.getElementById(`like-count-${postId}`).innerText = data.like_count;
            const likeButton = document.getElementById(`like-btn-${postId}`);
            likeButton.innerText = data.liked ? 'Unlike' : 'Like';

        }
    })
}

function submitComment(event, postId) {
    event.preventDefault();

    const commentContent = document.getElementById("comment-content").value.trim();

    if (!commentContent) {
        alert("Comment cannot be empty.");
        return;
    }

    fetch(`/add_comment/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken(),
        },
        body: `content=${encodeURIComponent(commentContent)}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const commentsContainer = document.getElementById("comments-container");
            const newComment = document.createElement("div");
            newComment.className = "comment mb-2";
            newComment.innerHTML = `
                <strong>${data.user}</strong>: ${data.content}
                <br>
                <small class="text-muted">${data.timestamp}</small>
            `;
            commentsContainer.appendChild(newComment);
            document.getElementById("comment-content").value = ""; // Clear the input
        }
    })
    .catch(error => console.error("Error:", error));

    location.reload(true)
}
