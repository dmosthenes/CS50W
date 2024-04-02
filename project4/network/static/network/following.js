// // 
// document.addEventListener("DOMContentLoaded", () => {

//     // Show profile view and hide modify view
//     profile_view = document.getElementById("profile-view")
//     profile_view.style.display = "block"
//     modify_view = document.getElementById("modify-view")
//     modify_view.style.display = "none"

//     // Add listener to the modify button
//     modify_button = document.getElementById("modify")

//     if (modify_button){

//         modify_button.addEventListener("click", () => {

//             modify_profile()

//     })
// }

//     // Update follow button

//     // Add listener to the follow button
//     follow_button = document.getElementById("follow")

//     if (follow_button){

//         follow_button.addEventListener("click", () => {
            
//             follow(follow_button.value)
//     })
// }

// })

// function modify_profile() {
//     // switch to html form
//     profile_view.style.display = "none"
//     modify_view.style.display = "block"

// }

// function follow(following) {
//     // add a new follow to database
//     fetch('/follow', {
//         method:"POST",
//         body: JSON.stringify({
//             follower: follow_button.dataset.user1,
//             followed: follow_button.dataset.user2,
//             following: following
//         })
//     })
//     .then(response => {
//         console.log(response)
//         // Display following animation

//         // reverse value of button and label
//         follow_reverse()
//     })
//     .catch(error => {
//         console.log(error)
//     })

//     // animate follow button on successful follow
// }

// function follow_reverse() {

//     follow_button.innerHTML = (follow_button.innerHTML === "Follow") ? "Unfollow" : "Follow"
//     follow_button.value = (follow_button.value === "True") ? "False" : "True"
// }