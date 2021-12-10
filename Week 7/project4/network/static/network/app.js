document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("#followUnfollowButton").addEventListener("click", () => follow())
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

function create_error_alert(alert_msg) {
    const element = document.createElement('div')
    element.innerHTML = alert_msg
    element.setAttribute("role", "alert")
    element.setAttribute("class", "alert alert-danger")
    document.querySelector(".container").append(element)
}