document.addEventListener("DOMContentLoaded", () => {

    if (document.getElementById("make-post") != null) {
        const post_button = document.getElementById("make-post")


        // Add event listener to post button
        post_button.addEventListener("click", () => {
            make_post(post_button)
        })
    }

    // Add event listeners to like buttons
    like_buttons = document.querySelectorAll('.btn.btn-primary.mr-2')
    like_buttons.forEach(button => {
        button.addEventListener("click", () => {
            const spans = button.querySelectorAll('span')
            like_post(spans[0], spans[1])
        })
    });

    // Add event listeners to edit buttons
    edit_buttons = document.querySelectorAll('.btn.btn-danger.mr-2')
    edit_buttons.forEach(button => {
        button.addEventListener("click", (event) => {
            const clicked_button = event.target
            edit_post(clicked_button)
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

                    // select the inserted HTML
                    latest_post = document.getElementById('post-box').nextElementSibling
                    latest_post.id = "animate-post"

                    // Add event listeners to the new like buttons.
                    let new_lk_btns = []
                    new_lk_btns.push(document.querySelector('.btn.btn-primary.mr-2'))
                    new_lk_btns.forEach(button => {
                        button.addEventListener("click", () => {
                            const spans = button.querySelectorAll('span')
                            like_post(spans[0], spans[1])
                        })
                    })

                    // Add event listeners to the new edit buttons.
                    let new_edt_btns = []
                    new_edt_btns.push(document.querySelector(('.btn.btn-danger.mr-2')))
                    new_edt_btns.forEach(button => {
                        button.addEventListener("click", () => {
                            edit_post(button)
                        })
                    })

                    // Clear "empty" message if present
                    empty = document.getElementById("empty")
                    if (empty != null){
                        empty.style.display = "none"
                    }

                })
                .catch(error => {
                    console.log(error)
                })
    })

    // and reset the comment box
    document.getElementById("id_body").value = ''
}


function like_post(left_btn, right_btn){
    // Make fetch request to like post

    fetch("/like", {
        method: "POST",
        body: JSON.stringify({
            "post-id": left_btn.dataset.postid,
        })
    })
    .then(response => response.json())
    .then(response => {

        // Update label
        if (left_btn.innerHTML === "Like"){
            left_btn.innerHTML = "Unlike"
        } else {
            left_btn.innerHTML = "Like"
        }

        // Update like count
        right_btn.innerHTML = `👌 ${response['count']}`

        })
    .catch(error => {
        console.log(error)
    })
}

function edit_post(clicked_button){

    // Replace text with textarea
    old_element = clicked_button.parentNode.parentNode.querySelector(".card-text")
    txt = old_element.innerHTML
    txt_area = document.createElement('textarea')
    txt_area.setAttribute('class', 'post-box form-control')
    txt_area.style.height = '100px'
    txt_area.value = txt
    
    old_element.parentNode.replaceChild(txt_area, old_element)

    // Hide button
    clicked_button.style.display = "none"

    // Add save button
    save_button = document.createElement('button')
    save_button.setAttribute("class", "btn btn-danger mr-2")
    save_button.textContent = "Save"
    clicked_button.parentNode.appendChild(save_button)

    // Add event listener
    save_button.addEventListener("click", (event) => {

        // Get new post
        new_txt = txt_area.value

        // Make fetch request to edit
        fetch("/edit", {
            "method": "POST",
            "body": JSON.stringify({
                "post_id": clicked_button.dataset.postid,
                "new_content": new_txt
            })
        })
        .then(data => data.json())
        .then(data => {
            old_element.innerHTML = data["post"]
            txt_area.parentNode.replaceChild(old_element, txt_area)

            // Change buttons
            clicked_button.style.display = "inline"
            save_button.style.display = "none"
            
        })
    })
}