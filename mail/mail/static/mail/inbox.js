document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#display-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Make POST request to send email
  document.querySelector('.btn.btn-primary').onclick = send_email

  function send_email(event){
    event.preventDefault()
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result)
    })
    .catch(error => {
      console.log(error)
    })
  
    // Load the sent mailbox
    load_mailbox('sent')
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#display-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the corresponding emails for the mailbox
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Create an element for each email
    emails.forEach(add_email);
  })
}

function add_email(email) {
      
  // Create new email element
  let message = document.createElement('div');
  message.className = 'emailDiv'
  message.style.backgroundColor = (email.read) ? 'lightgrey' : 'white'
  message.style.padding = '10px'
  message.style.border = '2px solid gray'
  message.style.borderRadius = '10px'
  message.style.cursor = 'pointer'
  message.addEventListener('click', function() {

    display_email(email)

    // fetch(`emails/${email.id}`)
    // .then(response => response.json())
    // .then(email => {
    //   console.log(email)
    //   display_email(email)
    // })

  })

  message.onmouseover = function() {
    msgs = document.getElementsByClassName('emailDiv')
    for (let i = 0; i < msgs.length; i++){
      if (msgs[i] == message){
        continue
      } else {
        msgs[i].style.opacity = '0.5'
      }

    }
  }

  message.onmouseleave = function() {
    msgs = document.getElementsByClassName('emailDiv')
    for (let i = 0; i < msgs.length; i++){
      msgs[i].style.opacity = '1'
      }
    }
  
  // Add the timestamp element as a child
  let time = document.createElement('p');
  time.className = 'time'
  time.innerHTML = email.timestamp
  message.appendChild(time)

  // Add the sender element as a child
  let sender = document.createElement('p');
  sender.className = 'sender'
  sender.innerHTML = email.sender
  sender.style.fontWeight = 'bold'
  message.appendChild(sender)

  // Add the subject element as a child
  let subject = document.createElement('p');
  subject.className = 'subject'
  subject.innerHTML = email.subject
  message.appendChild(subject)

      // Add element to the DOM
      document.querySelector('#emails-view').append(message)
      document.querySelector('#emails-view').append(document.createElement('br'))

  }

function display_email(email){

  document.querySelector('#display-email').innerHTML = ''

  // Update email's read status
  fetch(`emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#display-email').style.display = 'block';

  // Create Email box
  let box = document.createElement('div')
  box.className = 'emailOutline'
  box.style.border = '2px solid black'
  box.style.padding = '10px'
  box.style.borderRadius = '10px'


  // Add Email subject
  let subject = document.createElement('p')
  subject.className = 'subject'
  subject.innerHTML = email.subject
  box.appendChild(subject)

  // Add sender
  let sender = document.createElement('p')
  sender.className = 'sender'
  sender.innerHTML = email.sender
  box.appendChild(sender)

  // Add recipients
  let recipients = document.createElement('p')
  recipients.className = 'recipients'
  recipients.innerHTML = email.recipients
  box.appendChild(recipients)

  // Add timestamp
  let timestamp = document.createElement('p')
  timestamp.className = 'timestamp'
  timestamp.innerHTML = email.timestamp
  box.appendChild(timestamp)

  // Add body
  body = document.createElement('p')
  body.className = 'body'
  body.innerHTML = email.body
  box.appendChild(body)

  // Add archive button
  archive = document.createElement('button')
  archive.className = 'btn btn-primary'
  archive.innerHTML = 'Archive'
  box.appendChild(archive)
  archive.onclick = archiveEmail(email)


  document.querySelector('#display-email').append(box)
}

function archiveEmail(email){
  fetch(`emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({
      archive: true
    })
  })
  .then(response => response.json())
  .then(res => {
    console.log(res)
  }
  )
  .catch(error => {
    console.log(error)
  })
}