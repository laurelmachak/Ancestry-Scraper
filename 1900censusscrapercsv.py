import mechanize
import cookielib
from bs4 import BeautifulSoup
from os import path, execl
import pyexcel as pe
import sys
import winsound
#Imports all the libraries we will need

NAME_BOX = 0
AGE_BOX = 1
YEAR_BOX = 2
GENDER_BOX = 3
RACE_BOX = 4
BIRTHPLACE_BOX = 5
MARITAL_BOX = 6
RELATION_BOX = 7
HOME_BOX = 8
IMM_BOX = 9
MEMBERS_BOX =10
TOTAL_BOXES = 11

tdl = [["Name:","Age:","Birth Year:","Gender:","Race:","Birthplace:","Marital Status:","Relation to Head of House:","Home in 1900:","Immigration Year:","Household Members:"]]



WAIT_TIME = 0.01

RECORDS_PER_PAGE  = 20

working_list = [""] * TOTAL_BOXES
#Sets up the coordinates and the two lists we'll be using in processing

def process_data(page, record):
    global working_list
    with open(path.join(path.join("pages","round" + str(page) + "page" + str(record) + ".html"))) as html: #Open the html file for processing
        soup = BeautifulSoup(html, "html.parser")
        working_list[NAME_BOX] = findput("Name:",soup) #Use a helper function to assign the data one box at a time
        working_list[AGE_BOX] = findput("Age",soup)
        working_list[YEAR_BOX] = findput("Birth Year",soup)
        working_list[GENDER_BOX] = findput("Gender:",soup)
        working_list[RACE_BOX] = findput("Race:",soup)
        working_list[BIRTHPLACE_BOX]  =  findput("Birthplace:",soup)
        working_list[MARITAL_BOX] = findput("Marital Status:",soup)
        working_list[RELATION_BOX] = findput("Relation",soup)
        working_list[HOME_BOX] = findput("Home in 1900:", soup)
        working_list[IMM_BOX] = findput("Immigration",soup)
        working_list[MEMBERS_BOX] = membersput(soup)
    return working_list
        
def findput(field, soup): #Search for the key and the accompanying data
    for tag in soup.find_all("tr"):
        if field in str(tag):
            return tag.td.text
    return ""

def membersput(soup): #Iterate through the members of the family, saving each
    con = ""
    for tag in soup.find_all("a"):
        if "View Record" in str(tag):
            if con == "":
                con = tag.text.strip()
            else: 
                con += (", " + tag.text.strip())
    return con            

def main():
    global working_list
    global tdl
    urls = [""]
    br = mechanize.Browser()
    
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    #All of the above jjust set up the browser
    br.open("http://www.ancestrylibrary.com/")
    br.follow_link(br.find_link(url_regex="cat=35"))
    br.follow_link(br.find_link(url_regex="fedcen"))
    br.follow_link(br.find_link(url_regex="7602"))
    br.open("http://search.ancestrylibrary.com/cgi-bin/sse.dll?db=1900usfedcen&gss=sfs28_ms_db&new=1&rank=1&msT=1&MS_AdvCB=1&gsfn_x=1&gsln_x=1&msbpn__ftp_x=1&msrpn__ftp=New%20York%20City%20(All%20Boroughs)%2C%20New%20York%2C%20USA&msrpn=1652382&msrpn_PInfo=6-%7C0%7C1652393%7C0%7C2%7C3244%7C35%7C1652382%7C0%7C0%7C0%7C&msrpn_x=1&msrpn__ftp_x=1&msypn__ftp_x=1&msfng_x=1&msfns_x=1&msmng_x=1&msmns_x=1&msbng0_x=1&mssng0_x=1&mssns0_x=1&mscng0_x=1&_83004002_x=1&_8200C010__ftp_x=1&_82008010__ftp_x=1&MSAV=-1&uidh=fph")
    #Follows the appropriate links. Since the Ancestry website uses some kind of cookie-based protection, you can't access internal links without
    #A trail showing how you naviigated the website
    try:
        with open("urls.txt","r") as urlfile:
            texttofile = urlfile.read()
            list_of_lines = texttofile.split("\n")
            print(list_of_lines)
            highest = int(list_of_lines[len(list_of_lines)-3].split(":",1)[0])
            br.open(list_of_lines[len(list_of_lines)-3].split(":",1)[1].strip()) #This tries to open a text file that contains stored urls of the
            #pages that have been opened previously, allowing for the program to continue from where it left off
    except: 
        texttofile = ""
        print "No data found, starting from scratch"  
        highest = 0
        urls[0] = br.geturl()   
        texttofile += urls[0] + "\n" #If it can't find the file, starts from the original url
    did_fail = False
    while True:
        print "round ", highest / RECORDS_PER_PAGE
        a= br.links(url_regex="sse.dll\?indiv")
        for number, item in enumerate(a): #Creates a list of all urls matching the above search, and iterates through, saving the files
            url = str(item).split(" url='",1)[1].split("', text=",1)[0]
            br.retrieve(("http://search.ancestrylibrary.com" + url), path.join("pages", "round" + str(highest/RECORDS_PER_PAGE) + "page" + str(number) + ".html"))
        br.retrieve(br.geturl(), str(highest/RECORDS_PER_PAGE) + ".html") #Saves the index page as well
        html = open(str(highest/RECORDS_PER_PAGE) + ".html", "r") 
        soup = BeautifulSoup(html, "html.parser")
        if "The page you tried to access is no longer available" in soup.get_text() and did_fail == False:
            sound = "beep"
            winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
            execl(sys.executable, sys.executable, *sys.argv)
            #sys.exit(0)
            #print "FAILED!!! RETRYING"
            #time.sleep(15)
            #br.follow_link(urls[len(urls)-1])
            #did_fail = True
            continue
        else:
            did_fail = False
            highest += RECORDS_PER_PAGE
        searchreg = "fh=" + str(highest) + "&"
        for link in br.links(url_regex = searchreg):
            urls.append(link)
            with open("urls.txt","w") as urlfile:
                urlfile.seek(0)
                urlfile.truncate()
                texttofile += (str(highest) + ": " + urls[len(urls)-1].absolute_url + "\n")
                urlfile.write(texttofile)
                urlfile.close()
            print "http://search.ancestrylibrary.com" + str(link).split(" url='",1)[1].split("', text=",1)[0]
            br.follow_link(link) #This searches for the link to the next page, then follows it and writes the link to the text file mentioned earlier
            break
        else:
            break
            
    current_page = 0
    current_record = 0                
    while path.exists(path.join("pages","round" + str(current_page) + "page" + str(current_record) + ".html")): #Once all the pages are downloaded,
        #Iterate through them and process them using beautifulsoup.
        working_list = [""] * TOTAL_BOXES 
        print "Processing page " + str(current_page) + " record  " + str(current_record)
        tdl.append(process_data(current_page,current_record))
        if current_record != 19:
            current_record += 1
        else:
            current_page +=  1
            current_record = 0
    sheet = pe.Sheet(tdl)
    sheet.save_as("1900censusrecords.csv")
        
if __name__ == "__main__": #Runs the main function
    main()