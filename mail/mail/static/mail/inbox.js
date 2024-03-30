document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipients = '', subject = '', body = '') {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#display-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

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
    load_mailbox('sent', true)
  }
}

function load_mailbox(mailbox, sent=false) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#display-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // If sent, play animation
  if (sent) {

    anim_box = document.createElement('div')
    anim_box.className = "sent-banner"
    anim_box.innerHTML = "Email sent."

  
    document.querySelector('#emails-view').append(anim_box)

    anim_box.addEventListener('animationend', () => {
      anim_box.remove()
    }
    )
  }

  // Get the corresponding emails for the mailbox
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    if (emails.length === 0) {
      // Leave message in case of no emails
      emptyMessage = document.createElement('div')
      emptyMessage.innerHTML = "No emails."
      document.querySelector('#emails-view').append(emptyMessage)
    } else {
    // Create an element for each email
    emails.forEach(add_email);
    }
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
  box.style.border = '1px solid black'
  box.style.padding = '10px'
  box.style.borderRadius = '10px'

  // Add sender
  let sender = document.createElement('p')
  sender.className = 'sender email-inner';
  sender.innerHTML = `From: ${email.sender}`
  box.appendChild(sender)

  // Add recipients
  let recipients = document.createElement('p')
  recipients.className = 'recipients email-inner'
  recipients.innerHTML = `To: ${email.recipients}`
  box.appendChild(recipients)

  // Add Email subject
  let subject = document.createElement('p')
  subject.className = 'subject email-inner'
  subject.innerHTML = `Subject: ${email.subject}`
  box.appendChild(subject)

  // Add timestamp
  let timestamp = document.createElement('p')
  timestamp.className = 'timestamp email-inner'
  timestamp.innerHTML = `Sent: ${email.timestamp}`
  box.appendChild(timestamp)

  // Add body
  body = document.createElement('p')
  body.className = 'body email-inner'
  body.innerHTML = email.body
  box.appendChild(body)

  // Add flexbox
  let flexContainer = document.createElement('div');
  flexContainer.style.display = 'flex';
  flexContainer.style.flexDirection = 'row';
  flexContainer.style.justifyContent = 'space-between';
  flexContainer.style.alignContent = 'center';

  // Add archive button
  archive = document.createElement('button')
  archive.className = 'btn btn-primary'
  archive.innerHTML = (email.archived) ? 'Unarchive' : 'Archive'
  flexContainer.appendChild(archive)
  archive.onclick = function() {
    archiveEmail(email);
  }

  // Add reply button
  reply = document.createElement('button')
  reply.className = 'btn btn-primary'
  reply.innerHTML = 'Reply'
  flexContainer.appendChild(reply)
  reply.onclick = function() {
    write_reply(email);
  }

  // Add flex container to box
  box.appendChild(flexContainer)


  document.querySelector('#display-email').append(box)
}

function archiveEmail(email){
  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !email.archived
    })
  })
  .then(res => {
    console.log(res)

    if (!email.archived) {
      load_mailbox('archive');
    } else {
      load_mailbox('inbox')
    }
  }
  )
  .catch(error => {
    console.log(error)
  })

}

function write_reply(email){

  compose_email(email.sender, 
    `re: ${email.subject}`, 
    `\n\n\n\nOn ${email.timestamp}, ${email.sender} wrote:\n\t ${email.body}`)

}