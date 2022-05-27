from mailjet_rest import Client

api_key = '9aa5c72ce9c248d0570aa1e6cabdc9ab'
api_secret = '9bed4b34d09b8e19017768cc8264479e'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def main():
    print("Sending ======>")
    # read maile.txt
    with open('mail.txt', 'rt') as infile:
        text = infile.read()
        
    # when text start with '$' it is the key and the rest is the value
    # split the text into a list of lines
    lines = text.split('\n')
    # loop through the lines
    theMail = {}
    to = ""
    subject = ""
    body = ""

    i = 0
    for line in lines:
        # if the line starts with '$'
        
        if line.startswith('$'):
            # split the line into key and value
            key, value = line.split(' ', 1)
            
            # if the key is 'email'
            if key == '$to':
                to = value.replace("==", "").strip()
            elif key == '$subject':
                
                subject = value.replace("==", "").strip()
            elif key == '$message':
                body = value.replace("==", "").strip()
        elif line.startswith('#'):
            #reset variables
            to = ""
            subject = ""
            body = ""

        if to != "" and subject != "" and body != "":

            #add them to the dictionary
            theMail[i] = {'to': to, 'subject': subject, 'body': body}
            i += 1
            # reset the variables
            to = ""
            subject = ""
            body = ""
        # if #end is found, reset the variables
    # loop through the dictionary
    for key, value in theMail.items():
        # send the email
        send_email(value['to'], value['subject'], value['body'])
        # print(value['to'])
        # print(value['subject'])
        # print(value['body'])
    # print(theMail)

def send_email(email, subject, body):
    data = {
    'Messages': [
        {
        "From": {
            "Email": "khansom@oregonstate.edu",
            "Name": "Soman Khan"
        },
        "To": [
            {
            "Email": email,
            }
        ],
        "Subject": subject,
        "TextPart": "Greetings!",
        "HTMLPart": body,
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
# call main
if __name__ == "__main__":
    main()