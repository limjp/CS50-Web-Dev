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
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

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
      container.appendChild(rowContainer)

      addColToRow(email.sender, rowContainer)
      addColToRow(email.subject, rowContainer)
      addColToRow(email.timestamp, rowContainer)
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
      const element = document.createElement('div')
      element.innerHTML = result.error
      element.setAttribute("role", "alert")
      element.setAttribute("class", "alert alert-danger")
      document.querySelector("#alert-container").append(element)
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