document.addEventListener("DOMContentLoaded", function() {
    if (document.querySelector("#followUnfollowButton")){
        document.querySelector("#followUnfollowButton").addEventListener("click", () => follow())
    }
    document.querySelectorAll(".likeButton").forEach(button => {
        button.onclick = function () {
            like(this.dataset.postid, this)
        }
    })
    document.querySelectorAll(".editButton").forEach(button => {
        button.onclick = function () {
            edit(this.dataset.postid, this)
        }
    })
})

function follow() {
    const profileId = document.querySelector("#followUnfollowButton").dataset.profile
    
    fetch('/follow', {
        method: "POST",
        body: JSON.stringify({ 
            profileId: profileId
        })
    })
    .then((response) => response.json())
    .then(result => {
        if (result.error) {
            create_error_alert(result.error)
        } else {
            currentlyFollowing = document.querySelector("#followUnfollowButton").innerHTML
            currentlyFollowing === "Unfollow" ? document.querySelector("#followUnfollowButton").innerHTML = "Follow" : document.querySelector("#followUnfollowButton").innerHTML = "Unfollow"
        }
    })
}

function like(postId, btn) {
    fetch('/like', {
        method: "POST",
        body: JSON.stringify({
            postId: postId
        })
    })
    .then((response) => response.json())
    .then(result => {
        if(result.error) {
            create_error_alert(result.error)
        } else {
            btn.innerHTML === "Unlike" ? btn.innerHTML = "Like" : btn.innerHTML = "Unlike"
        }
    })
}

function create_error_alert(alert_msg) {
    const element = document.createElement('div')
    element.innerHTML = alert_msg
    element.setAttribute("role", "alert")
    element.setAttribute("class", "alert alert-danger")
    document.querySelector(".container").append(element)
}

function edit(postId, btn) {
    document.getElementById(postId).setAttribute("contenteditable", true)
    btn.innerHTML = "Save"
    btn.removeEventListener("click", edit)
    btn.addEventListener("click", () => save(postId, btn))

}

function save(postId, btn) {
    const post = document.getElementById(postId)
    post.setAttribute("contenteditable", false)
    btn.innerHTML = "Edit"

    fetch(`/save`, {
        method: "PUT",
        body: JSON.stringify({
            postId: postId,
            content: post.innerHTML
        })
    })
    .then((response => response.json))
    .then(result => {
        if (result.error) {
            create_error_alert(result.error)
        }
    })

    btn.removeEventListener("click", save)
    btn.addEventListener("click", () => edit(postId, btn))
}