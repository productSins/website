from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import requests
from bs4 import BeautifulSoup
import re



# Create your views here.



@api_view(['GET'])
def scrape_data(request):

    if(request.method == "GET"):
        url = str(request.GET.get('website'))
        source = requests.get(url).text
        soup = BeautifulSoup(source,'lxml')

        h_count = len(soup.find_all(['h1','h2']))
        p_count = len(soup.find_all('p'))

        # only_count = len(soup.find_all(string = re.compile(r"(?:^|\W)only(?:$|\W)",re.I))) 
        only_count = len(soup.find_all(string=re.compile(r'\bOnly\b',re.I))) 
        only_found = False
        if(only_count > 0):
            only_found = True

        img_count = len(soup.find_all('img'))

        case_count = len(soup.find_all(string=re.compile(r'\bCase Studies|Use Case|Stories of Success|Success Stories\b',re.I)))
        case_found = False
        if(case_count > 0):
            case_found = True
        
        demo_count = len(soup.find_all(string = re.compile(r'\bRequest Demo| Request a Demo\b',re.I)))
        demo_found = False
        if(demo_count > 0):
            demo_found = True

        text_only = soup.get_text()
        text_count = len(text_only.split())
        question_count = text_only.count('?')

        button_content = []
        button_lengths = []
        for data in soup.find_all('button'):
            button_content.append(data.get_text())
        
        for content in button_content:
            button_lengths.append(len(content.split()))
        
        button_exceed = False
        for length in button_lengths:
            if(length > 3):
                button_exceed = True


        for data in soup.find_all(re.compile('^h[1-6]$'),limit = 1):
            header_content = ''.join(data.findAll(text = True))
        header_length = len(header_content.split())

    data = {'h_count': h_count, 
            'header_length': header_length,
            'p_count': p_count,
            'only_found': only_found,
            'img_count': img_count,
            'case_found': case_found,
            'demo_found': demo_found,
            'text_only': text_count,
            'question_count': question_count,
            'button_lengths': button_lengths,
            'button_content': button_content,                                                     
            'button_exceed': button_exceed,                                           
            }



    
    return Response(status = status.HTTP_200_OK, data = {'h_count': h_count, 
                                                         'header_length': header_length,
                                                         'p_count': p_count,
                                                         'only_found': only_found,
                                                         'img_count': img_count,
                                                         'case_found': case_found,
                                                         'demo_found': demo_found,
                                                         'text_only': text_count,
                                                         'question_count': question_count,
                                                         'button_lengths': button_lengths,
                                                         'button_content': button_content,
                                                         'button_exceed': button_exceed,
                                                        })
    
    
        

    





    
        

    






    
    
        

    





