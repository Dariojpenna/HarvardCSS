document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //Creat Elements
  const divBody = document.createElement("div")
  const divInfo = document.createElement("div")
  const divReplay = document.createElement("div")
  const btnReplay = document.createElement("button")
  
  //Addin class to divs
   divBody.className = "bodyMail";
   divInfo.className = "info"
   divReplay.className = "replay"

  //Add replay Button
  btnReplay.innerHTML = "Replay"
  btnReplay.className ="btn-replay"

  //Put divs in mails view
  document.querySelector("#mails").append(divInfo)
  document.querySelector("#mails").append(divBody)
  document.querySelector("#mails").append(divReplay)
  document.querySelector(".replay").append(btnReplay)
   
  // By default, load the inbox
  load_mailbox('inbox');
});



function compose_email() {

  // Show compose view and hide other views
  document.querySelector("#error").style.display = "none";
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mails').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  

  //send mail
  document.querySelector("form").onsubmit= function(){
    
    //Obtaining the values
    const mail = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;
    
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: mail,
          subject: subject,
          body: body
        })
        
    }).then(response => {
      if (!response.ok) throw Error(response.status);
      
      return load_mailbox('inbox');
    })
    .then(response => console.log("ok"))
    .catch(function(){
      document.querySelector("#error").style.display = "block";
      document.querySelector("#error").innerHTML = "Error ! The address don't exist";
      document.querySelector("#error").style.backgroundColor = "rgb(218,76,76)";
      document.querySelector("#error").style.border = "2px solid red";
      document.querySelector("#error").style.textAlign = "center";
      document.querySelector("#error").style.borderRadius = "5px";
      document.querySelector("#error").style.width = "50%";
      document.querySelector("#error").style.margin = "auto";
      document.querySelector("#error").style.height = "30px";
      document.querySelector("#error").style.display = "block"


      
    })
  
    return false;
    
  }
  
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mails').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    var url = "/emails/"  + mailbox;
    

    fetch(url)
    .then(response => response.json())
    .then(emails => {

      // Print emails
      //Create Div, ul,li and p for emails
      const div1 = document.createElement('div');
      const ul = document.createElement('ul');
      
      div1.append(ul);

      //make loop for mails
      emails.forEach(element => {
        
        const li = document.createElement("li")
        const p1 = document.createElement('p');
        const p2 = document.createElement('p');
        const p3 = document.createElement('p');
        const btnArchive = document.createElement("button")

        //If we are in inbox we show the sender, if we are in sent, we show the recipient
        p1.innerHTML = mailbox === "sent"?element.recipients[0].bold():element.sender.bold();

        //Add subject and time
        p2.innerHTML = element.subject;
        p3.innerHTML = element.timestamp;

        //Add clas to the archive button 
        btnArchive.className= "btn btn-primary"

        //If we are in inbox,the button shows archive, if we are in archive view, then show unarchive
        btnArchive.innerHTML = mailbox === "inbox"?"Archive": mailbox === "archive"?"Unarchive":btnArchive.style.display = 'none';

        //Add class yo p elements
        p1.className = "sender"
        p2.className = "sect"
        p3.className = "timeStamp"

        //Add p and btn to li
        li.append(btnArchive)
        li.append(p1)
        li.append(p2)
        li.append(p3)

        ul.append(li)

        
        

        //Function to archive messages
        btnArchive.addEventListener("click", function(){
          const idUrl = "/emails/"+element.id
          
          fetch(idUrl, {
            method: 'PUT',
            body: JSON.stringify({
                //Select true or false according if we are in inbox or archive view
                archived: mailbox==="inbox"?true:false

            })
          })
          
          //after archive or unarchive load inbox view
          setTimeout(load_mailbox,300,'inbox');
           
        })

        // ... do something else with emails ...
        //function to see mails Body
        p1.addEventListener("click", function(){
          
        //Chose only mails content view
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        document.querySelector('#mails').style.display = 'block';


        //Create mails view
        let newElement = element.body.replaceAll("On", "<br><br>On")
        document.querySelector(".bodyMail").innerHTML = newElement +"<br>";
        document.querySelector(".info").innerHTML =  "<b>To: </b>" + element.recipients + "<br>  <b>From: </b>"+element.sender+ "<br> <b>Subject: </b>"+ element.subject+"<br><b>Date: </b>"+ element.timestamp;
          

        //Replay function
        document.querySelector(".btn-replay").addEventListener("click", function(ev){

          ev.preventDefault();
          
          compose_email();

          document.querySelector('#compose-recipients').value = element.sender;

          //Select Subject according if we have a Re: or not
          let subject = element.subject;
          if(subject.startsWith("Re: ")){
            subject = subject
          }else{
              subject = "Re: "+ element.subject;
           }
          document.querySelector('#compose-subject').value = subject;
          
          document.querySelector('#compose-body').value= '\nOn ' + element.timestamp + ", " + element.sender + " wrote:  " + element.body;

        })
          
           //MODIFICAR A LEIDO
          const idUrl = "/emails/"+element.id

          fetch(idUrl, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
          
        })

        //select class according to this reading or not
        mailbox != "sent" && element.read?li.className="readed":""
      })
      
      //Adding a div in emails-view
      div1.className = "div1"
      document.querySelector('#emails-view').append(div1);
      
      
    });
    

}

