document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('form').onsubmit = send_email

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Clear out any emails that exists
  const email_container = document.querySelector(".email-container")
  if (email_container) email_container.remove()

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    const container = document.createElement("div")
    container.setAttribute("id", "container")
    container.setAttribute("class", "container")
    document.querySelector("#emails-view").append(container)
    emails.forEach(email => {
      const rowContainer = document.createElement("div")
      email.read === true ? rowContainer.setAttribute("class", "row read border border-secondary") : rowContainer.setAttribute("class", "row unread border border-secondary")
      rowContainer.dataset.emailId = email.id
      rowContainer.dataset.read = email.read
      rowContainer.setAttribute("id", email.id)
      container.appendChild(rowContainer)

      addColToRow(email.sender, rowContainer)
      addColToRow(email.subject, rowContainer)
      addColToRow(email.timestamp, rowContainer)

      rowContainer.addEventListener("click", () => view_email(rowContainer.dataset.emailId))
      rowContainer.style.cursor = "pointer"
    })
  })
}

function send_email(){
  const recipients = document.querySelector('#compose-recipients').value.split(",").map(element => element.trim()).join()
  const subject = document.querySelector('#compose-subject').value.trim()
  const body = document.querySelector('#compose-body').value.trim()

  fetch('/emails', {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then((response) => response.json())
  .then(result => {
    if (result.error) {
      create_error_alert(result.error)
    } else load_mailbox("sent")
  })
  return false
}

function addColToRow(content, row) {
  const col = document.createElement("div")
  col.innerHTML = content
  col.setAttribute("class", "col-sm")
  row.appendChild(col)
}

function create_error_alert(alert_msg) {
  const element = document.createElement('div')
  element.innerHTML = alert_msg
  element.setAttribute("role", "alert")
  element.setAttribute("class", "alert alert-danger")
  document.querySelector("#alert-container").append(element)
}

function view_email(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(response => {
    if (response.error) {
      create_error_alert(response.error)
    } else {
      const subject = response.subject
      const sender = response.sender
      const body = response.body
      const timestamp = response.timestamp
      const containerToAppend = document.createElement("div")
      containerToAppend.dataset.archive = response.archive
      containerToAppend.dataset.archive = response.id
      containerToAppend.setAttribute("class", "email-container")

      createDiv("email-subject", subject, containerToAppend)
      createDiv("email-sender", sender, containerToAppend)
      createDiv("email-body", body, containerToAppend)
      createDiv("email-timestamp", timestamp, containerToAppend)

      const buttonContent = response.archived ? "Unarchive" : "Archive"
      const archive_button = createButton("btn btn-dark", buttonContent, containerToAppend)
      archive_button.addEventListener("click", () => archiveEmail(email_id))

      const replyButton = createButton("btn btn-primary", "Reply", containerToAppend)
      replyButton.addEventListener("click", () => reply(sender, subject, timestamp, body))

      document.querySelector("#email-view").appendChild(containerToAppend)

      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
      
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#email-view').style.display = 'block';
    }
  })
}

function createDiv(divName, divContent, containerToAppend) {
  const element = document.createElement('div')
  element.innerHTML = divContent
  element.setAttribute("class", divName)
  containerToAppend.appendChild(element)
}

function archiveEmail(email_id, isArchived) {
  const responseToSend = isArchived ? false : true

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: responseToSend
    })
  })

  load_mailbox('inbox')
}

function createButton(buttonName, buttonContent, containerToAppend) {
  const button = document.createElement("button")
  button.innerHTML = buttonContent
  button.setAttribute("type", "button")
  button.setAttribute("class", buttonName)
  containerToAppend.append(button)

  return button
}

function reply(sender, subject, timestamp, body) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none'
  document.querySelector('#email-view').style.display = 'none'
  document.querySelector('#compose-view').style.display = 'block'

  document.querySelector('#compose-recipients').value = sender

  if (subject.slice(0,2) === "Re") {
    document.querySelector('#compose-subject').value = subject
  } else document.querySelector('#compose-subject').value = `Re: ${subject}`

  document.querySelector('#compose-body').value = `On ${timestamp} ${sender} wrote:
  ${body}`
}