from email.parser import Parser
from email.policy import compat32
import os
def emails_between(m_list, m_dict):
    """
    the function takes email-ID list as input and go through email
    files to check out emails between the input mailIDs.
    it prints "to", "from", "subject" and "body"
    """
    mail_object = []
    for root, dirs, files in os.walk("maildir"):
        for file in files:
            try:
                with open(os.path.join(root, file)) as fp:
                    headers = Parser(policy=compat32).parse(fp)
                to_mail = headers['to'].split()
                from_mail = headers['from']
                for i in m_dict:
                        mail_id = m_dict[i]
                        if from_mail in mail_id:
                            for j in m_dict:
                                if j!=i:
                                    suspectEmailIdListTo = m_dict[j]
                                    for k in suspectEmailIdListTo:
                                        if k in to_mail:
                                            mail_object.append(headers)
            except:
                continue
        
    return mail_object
def mail_list():
    """
    this function only flattens the email dictionary 
    so it can be used as input for email_between().
    """
    red_flags = {
            "lay-k": ["kenneth.lay@enron.com", "klay@enron.com"],
            "skilling-j": ["skilling@enron.com", "jeff.skilling@enron.com"]
            }
    
    #printing the object type
    m_list = [i for sublist in red_flags.values() for i in sublist]
    print(emails_between(m_list, red_flags))
mail_list()
