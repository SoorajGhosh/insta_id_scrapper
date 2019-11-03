import requests
from bs4 import BeautifulSoup
import lxml
import json

flag = True

def get_user():
    while True:
        input_url = input("Enter the url of the account or the username: ")
    
        #checking if url or username
        if input_url[:5] == "https":
            url_link = input_url
        else:
            url_link = f'https://instagram.com/{input_url}?igshid=bgt4d8ck3eef'

        url = url_link.split('?')[0]
    
        r = requests.get(url)
    
        if r.status_code ==200:
            break
        else:
            print('Wrong Url or username. Check Again..!')
            pass
    
    return  r.text       
    


def main(soup):
    #grabbing the 3rd script in the list which contains most of the valuable info
    ext_detail = soup.find_all('script', type='text/javascript')[3]

    #splitting to focus on main content
    context = ext_detail.text.split("window._sharedData = ")
    profile = context[1].split(',"hostname"')[0]

    #focusing on content and adding the } to complete the json format
    all_details = json.loads(profile+"}")

    #getting the user detials
    usr_details = all_details['entry_data']['ProfilePage'][0]['graphql']['user']


    profile_detail_dict = {'p_username': usr_details['username'],
    'p_full_name': usr_details['full_name'],
    'p_bio': usr_details['biography'],
    'p_followers': usr_details['edge_followed_by']['count'],
    'p_following': usr_details['edge_follow']['count'],
    'p_profile_pic_hd': usr_details['profile_pic_url_hd'],
    'p_video_count': usr_details['edge_felix_video_timeline']['count'],
    'p_photos_count': usr_details['edge_owner_to_timeline_media']['count'],
    'p_is_private': usr_details['is_private'],
    'p_is_verified': usr_details['is_verified'],
    'p_is_bussiness_account': usr_details['is_business_account'],
    'p_is_joined_recently':usr_details['is_joined_recently'],
    'p_fb_page': usr_details['connected_fb_page'],}


    for item in profile_detail_dict.items():
        print(item)





while flag:
    source_code = get_user()
    soup = BeautifulSoup(source_code,'lxml')
    main(soup=soup)
    while True:    
        again = input("Enter \"y\" to see someone else or \"q\" to quit: ")
        if again.lower() == "q":
            flag = False
            break
        elif again.lower() == "y":
            break
        else:
            pass