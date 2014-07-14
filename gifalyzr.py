import email
import imaplib
import os
import json
from time import gmtime, strftime
from pprint import pprint
from dateutil.parser import parse
import re

# directory where to save gifs
detach_dir = './gifs'
# email creds
user = "ian@stinkdigital.com"
# open text file containing gmail password
pwdfile = open(".pwd", "r")
pwd = pwdfile.read()
pwdfile.close()
# open current json file
with open("gifs.json") as json_file:
    json_data = json.load(json_file)
# current array of gifs
gifs = json_data["gifs"]
labels = json_data["labels"]
# get current timestamp
timestamp = json_data["timestamp"]
# close file
json_file.close()
#print(gifs)
#print(timestamp)
# save new timestamp
json_data["timestamp"] = strftime("%d-%b-%Y", gmtime())
# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com", "993")
m.login(user, pwd)
# use m.list() to get all the mailboxes
# data = m.list()
# select mailbox
m.select("[Gmail]/All Mail")
# get everyone emails since last timestamp
resp, items = m.search(None, "TO", "everyone@stinkdigital.com", "SENTSINCE", timestamp)
# get the mail ids
items = items[0].split()
# print total
#print "TOTAL:" + str(len(items))
# loop through from newest
#for emailid in reversed(items):
for emailid in items:
    #print emailid
    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1] # getting the mail content
    mail = email.message_from_string(email_body) # parsing the mail content to get a mail object
    #pprint(data)
    # check if any attachments at all
    if mail.get_content_maintype() != 'multipart':
        continue

    # print sender and subject
    name = mail["From"].partition(" ")[0]
    date = parse(mail["Date"]).strftime('%a %d %b %Y %H:%M')
    label = name + ", " + date
    print label
    #print "["+mail["From"]+"] :" + mail["Subject"]

    # we use walk to create a generator so we can iterate on the parts and forget about the recursive headache
    for part in mail.walk():
        # multipart are just containers, so we skip them
        if part.get_content_maintype() == 'multipart':
            continue
        # is this part an attachment?
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        # if no filename skip
        if not filename:
            continue

        print filename
        if filename.lower().endswith('.gif'):
            print filename
            newfilename = re.sub("[^A-Za-z0-9_\-.]", "", filename)
            att_path = os.path.join(detach_dir, newfilename)
            # check if already exists
            if not os.path.isfile(att_path):
                # write the image file
                print(att_path + " " + label)
                #gifs.append(att_path)
                #labels.append(label)
                gifs.insert(0, att_path)
                labels.insert(0, label)
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

# write new json data
with open('gifs.json', 'w') as outfile:
  json.dump(json_data, outfile)
  outfile.close()