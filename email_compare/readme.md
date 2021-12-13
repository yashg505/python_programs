The main purpose of this program is to filter out files between two individual.
Some conditions to filter out the files:
1. We will limit the results to those with limited circulation i.e. with 20 or fewer recipients in order to filter out blanket emails sent to all and sundry.
2. The parameter "suspects" is dictionary in the format shown, containing the email details of the individuals under investigation. Specifically the keys give the account/directory names
   and the values give a list of the email address(es) associated with that account. 
   red_flags = {"lay-k": ["kenneth.lay@enron.com", "klay@enron.com"],
                "skilling-j": ["skilling@enron.com", "jeff.skilling@enron.com"]}
3. The return type is a list of "email objects", specifically of type email.message.Message.

The email data is based on major Enron company fraud. https://en.wikipedia.org/wiki/Enron_scandal
