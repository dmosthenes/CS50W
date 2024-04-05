document.addEventListener("DOMContentLoaded", () => {

    const post_button = document.getElementById("make-post")


    // Add event listener to post button
    post_button.addEventListener("click", () => {
        make_post(post_button)
    })

    // Add event listeners to like buttons
    like_buttons = document.querySelectorAll('.btn.btn-primary.mr-2')
    like_buttons.forEach(button => {
        button.addEventListener("click", (event) => {

            const clicked_button = event.target;

            like_post(clicked_button)

        })

    });


    // Add event listeners to reply buttons
    reply_buttons = document.querySelectorAll('.btn.btn-secondary.mr-2')

    reply_buttons.forEach(button => {
        button.addEventListener("click", (event) => {

            const clicked_button = event.target

            reply_post(clicked_button)

        })
    })

})

function make_post(post_button){

    // Get post content
    const comment = document.getElementById("id_body").value

    if (comment === ""){
        alert("Post is empty.")
        return null
    }

    
    fetch('/get_user')
        .then(response => response.json())
        .then(user => {
            // Make fetch request to create new post
            fetch("/post", {
                method: "POST",
                body: JSON.stringify({
                    "comment": comment,
                    "user": user.user.id
                })
            })
                .then(response => response.text())
                // Once post is created, 
                // append it after the post button
                .then(data => {

                    const new_post = data

                    document.getElementById('post-box').insertAdjacentHTML('afterend', new_post)

                    empty = document.getElementById("empty")
                    empty.style.display = "none"

                    // post_button.insertAdjacentHTML('afterend', new_post)

                })
                .catch(error => {
                    console.log(error)
                })

})

    // and reset the comment box
    document.getElementById("id_body").value = ''
}


// function get_user() {
//     // Get the currently logged in user
//     fetch('/get_user')
//     .then(response => response.json())
//     .then(data => {
//         return data.user
//     })
//     .catch(error => {
//         console.log(error)
//     })
// }


function like_post(clicked_button){
    // Make fetch request to like post
    fetch()

    // Update like count on post

}

function reply_post(clicked_button){
    // Make fetch request to reply
    fetch()

    // Attach new comment to post

}