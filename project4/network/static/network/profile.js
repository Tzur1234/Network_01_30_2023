
document.addEventListener('DOMContentLoaded', () =>{
    // Add eventListener to like Button
    document.body.addEventListener('click', like_status);// change 

    // Add Event listener 
    document.body.addEventListener('click', setFollow)

    // add event listener for editcard
    document.body.addEventListener('click', editpost);

    // add event listener for editcard
    document.body.addEventListener('click', editpost);
})


function alert() {

}



function setFollow(event){
    if(event.target.className === 'btn btn-primary follow'){
        desire_follow_state = true
        console.log(`"follow" ubtton was pressed`)
    }
    else if(event.target.className === 'btn btn-secondary unfollow'){
        desire_follow_state = false
        console.log(`"unfollow" button was pressed`)
    }
    else{
        // exit
        return;
    }
    // update follow mode by using fetch API
    console.log (event.target.dataset.user_id)
    fetch('/setFollow', {
        method: 'PUT',
        body: JSON.stringify({
            desire_follow_state: desire_follow_state,
            user_id: event.target.dataset.user_id  
        })
    })
    .then(response => response.json())
    .then((data ) => {
        // update buttom type
        console.log(data)
        if(desire_follow_state){
        event.target.innerHTML = 'Unfollow';
        event.target.className = 'btn btn-secondary unfollow';
        }
        else{    
        event.target.innerHTML = 'Follow';
        event.target.className = 'btn btn-primary follow';
        
        }
        // Update the number of following and followers
        event.target.previousElementSibling.previousElementSibling.innerHTML = `Followers ${data['followers']}`
        event.target.previousElementSibling.innerHTML = `Following ${data['following']}`
    })
}



// Update user likes
function like_status(event) {
    // status to change
    if (event.target.className === 'btn btn-primary like') {
        change_status_like_to = true;
    }
    else if (event.target.className === 'btn btn-secondary unlike') {
        change_status_like_to = false;
    }
    else {
        // exit function
        return;
    }

    // post_id
    post_id = event.target.dataset.id

    // Fetch API - PUT
    fetch('/changelike', {
        method: 'POST',
        body: JSON.stringify({
            change_status_like_to: change_status_like_to,
            post_id: post_id
        })
    })
        .then(response => response.json())
        .then(result => {
            // update the LikeButton (UI)
            if (change_status_like_to) {
                event.target.className = 'btn btn-secondary unlike';
                event.target.innerHTML = 'Unlike'
            }
            else {
                event.target.className = 'btn btn-primary like';
                event.target.innerHTML = 'Like';
            }
            // update the number of likes for the post
            console.log(`(${result.likes} Likes)`)
            small = event.target.previousElementSibling.firstElementChild;
            small.innerHTML = '';
            small.append(`(${result.likes} Likes)`)


        });
}



function editpost(event) {
    button_press = event.target
    console.log(button_press.parentNode)
    if (button_press.id === 'editmypost') {

        // get all items
        items = document.querySelectorAll(`[data-id="${button_press.dataset.id}"]`)
        console.log(items)

        // get the text-card content
        card_content = items[0]
        console.log(card_content)

        // get the edit button
        edit_button = items[3]
        console.log(edit_button)


        // create new save button
        save_button = createEl('savebutton', button_press.dataset.id)

        // create text area element
        textarea = createEl('textarea', button_press.dataset.id, card_content.innerHTML)


        // replace text-card with the textarea card 
        button_press.parentNode.replaceChild(textarea, card_content)


        // replacce the edit with the replace button 
        button_press.parentNode.replaceChild(save_button, edit_button)

    }
    // check if press edit-button
    if (button_press.id === 'savemypost') {

        // get all items with a specific data-set attribute
        items = document.querySelectorAll(`[data-id="${button_press.dataset.id}"]`)
        console.log(items)

        // get the text-card content from items
        textarea = items[0]
        console.log(textarea)

        // get the edit button from items
        save_button = items[3]
        console.log(save_button)


        // create new edit button
        edit_button = createEl('editbutton', button_press.dataset.id)
        console.log(edit_button)
        // create card-content 
        card_content = createEl('card-content', button_press.dataset.id, textarea.value)
        console.log(card_content)

        //Fetch API - PUT
        fetch('/editpost', {
            method: 'POST',
            body: JSON.stringify({
                post_id: button_press.dataset.id,
                new_content: textarea.value
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);

            // replace content textarea content-card (UI)
        button_press.parentNode.replaceChild(card_content, textarea)

        // replace buttons (UI)
        button_press.parentNode.replaceChild(edit_button, save_button)

        });
        

    }

    event.preventDefault()
}

// create a specified element
function createEl(elementype, post_id, content) {
    if (elementype === 'savebutton') {
        save_button = document.createElement('button');
        save_button.className = 'btn btn-success m-5';
        save_button.setAttribute('id', 'savemypost')
        save_button.innerHTML = 'Save';
        save_button.setAttribute("data-id", post_id)

        return save_button;
    }
    if (elementype === 'editbutton') {
        edit_button = document.createElement('button');
        edit_button.className = 'btn btn-warning m-5';
        edit_button.setAttribute('id', 'editmypost')
        edit_button.innerHTML = 'Edit';
        edit_button.setAttribute("data-id", post_id);

        return edit_button;
    }
    if (elementype === 'textarea') {
        textarea = document.createElement('textarea');
        textarea.setAttribute('name', 'editcontent');
        textarea.setAttribute('id', 'editcontent');
        textarea.setAttribute('cols', '60');
        textarea.setAttribute('rows', '10');
        textarea.setAttribute("data-id", post_id)

        //  Insert new content
        textarea.innerHTML = content;

        return textarea;
    }
    if (elementype === 'card-content') {
        text_p = document.createElement('p');
        text_p.className = 'card-text'
        text_p.innerHTML = content;
        text_p.setAttribute("data-id", post_id)

        return text_p;
    }
}










// Create Card for each post
// return post card element with the post info
// function createCardElement(post) {

//     // header card
//     header_card = document.createElement('div');
//     header_card.className = 'card-header'
//     header_card.innerHTML = post.date


//     //card title - username
//     username = document.createElement('h5');
//     username.className = 'card-title'
//     username.innerHTML = post.username

//     // link user name
//     link = document.createElement('a');
//     link.setAttribute('href', `profile/${post.user_id}`)
//     link.append(username)



//     // card text
//     text_p = document.createElement('p');
//     text_p.className = 'card-text'
//     text_p.innerHTML = post.content
//     text_p.setAttribute('data-id', post.post_id)


//     br = document.createElement('br');

//     // small class - number of likes
//     small = document.createElement('small');
//     small.className = 'text-muted like-count';
//     small.innerHTML = `(${post.likes} Likes)`

//     // Check if the current user gave already like to the current post
//     button_like = document.createElement('a');
//     if (post.user_gave_like === true) {
//         button_like.className = 'btn btn-secondary unlike';
//         button_like.innerHTML = 'Unlike'
//     }
//     else {
//         button_like.className = 'btn btn-primary like';
//         button_like.innerHTML = 'Like'
//     }
//     // set post id
//     button_like.setAttribute("data-id", post.post_id)




//     text_p2 = document.createElement('p');
//     text_p2.className = 'card-text';
//     text_p2.append(small);
//     text_p2.setAttribute("data-id", post.post_id)


//     // card body
//     body_card = document.createElement('div');
//     body_card.className = 'card-body';
//     body_card.append(link);
//     body_card.append(text_p);
//     body_card.append(text_p2);
//     body_card.append(button_like);

//     // if the user wrote the post - show edit button  
//     if (post.postowner) {
//         edit_button = document.createElement('button');
//         edit_button.className = 'btn btn-warning m-5';
//         edit_button.setAttribute('id', 'editmypost')
//         edit_button.innerHTML = 'Edit';
//         edit_button.setAttribute("data-id", post.post_id)
//         body_card.append(edit_button)

//     }



//     // main card
//     main_card = document.createElement('div');
//     main_card.className = 'card text-left my-5';
//     main_card.append(header_card)
//     main_card.append(br)
//     main_card.append(body_card)

//     return main_card

// }