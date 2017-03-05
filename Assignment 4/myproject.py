import os
import json
import requests
from flask import Flask, request, Response
import unicodedata
import datetime
import random
import time
from textblob import TextBlob

application = Flask(__name__)

# SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')

# slack_inbound_url = 'https://hooks.slack.com/services/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'

slack_inbound_url = 'https://hooks.slack.com/services/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'


@application.route('/slack', methods=['POST'])
def inbound():
    # Adding a delay so that all bots don't answer at once (could overload the API).
    # This will randomly choose a value between 0 and 10 using a uniform distribution.
    delay = random.uniform(0, 10)
    time.sleep(delay)
    response = {'username': 'abishek_bot', 'icon_emoji': ':robot_face:'}
    ip_address = request.remote_addr
    # if request.form.get('token') == SLACK_WEBHOOK_SECRET:
    channel = request.form.get('channel_name')
    username = request.form.get('user_name')
    text = unicodedata.normalize('NFKD', request.form.get('text')).encode('ascii', 'ignore')

    inbound_message = username + " in " + channel + " says: " + text
    # if username in ['zac.wentzell']:
    #     response['text'] = 'Hey dude!'
    #
    #     r = requests.post(slack_inbound_url, json=response)

    owner_name = 'abishekrathan'
    my_chatbot_name = 'abishek_bot'
    if username != my_chatbot_name and username in [owner_name, 'zac.wentzell']:
        #Task 1
        if "BOTS_RESPOND" in text and username == 'zac.wentzell':
            response['text'] = 'Hello, my name is {0}. I belong to {1}. I live at {2}'.format(my_chatbot_name, username, ip_address)
            # Task 3
        else:
            if "I_NEED_HELP_WITH_CODING" in text:
                results = str("")
                text_search_collection = text.split(':')
                keyword = text_search_collection[1].replace(" ", "%20")
                tag_removed_list = keyword.split('[')
                query = tag_removed_list[0]
                tag_collection = []
                if "[" in text:
                    tag_collection = text.replace("]", "").split("[")
                    del tag_collection[0]
                    for item in tag_collection:
                        query = query + "&tagged=" + item.strip(' ')
                        r = requests.get(
                            'https://api.stackexchange.com/2.2/search/advanced?page=5&pagesize=5&order=asc&sort=relevance&q={0}&accepted=True&site=stackoverflow'.format(
                                query))

                    json_object = r.json()
                    for value in json_object['items']:
                        title = value['title']
                        link = '<' + value['link'] + '|Link>'
                        date = value['creation_date']
                        date_in_format = datetime.datetime.fromtimestamp(date).strftime('%c')
                        responses = value['answer_count']
                        results = results + "\n" + title + " " + link + " "+str(
                            responses) + "responses" + " " + date_in_format + "\n"
                    response['text'] = "Here are some useful links\n" + results
                # Task 2
                else:
                    r = requests.get(
                        'https://api.stackexchange.com/2.2/search/advanced?page=5&pagesize=5&order=asc&sort=relevance&q={0}&accepted=True&site=stackoverflow'.format(
                            keyword))
                    json_object = r.json()
                    for value in json_object['items']:
                        title = value['title']
                        link = '<' + value['link'] + '|Link>'
                        date = value['creation_date']
                        date_in_format = datetime.datetime.fromtimestamp(date).strftime('%c')
                        responses = value['answer_count']
                        results = results + "\n" + title + " " + link + " "+str(
                            responses) + "responses" + " " + date_in_format + "\n"
                        response['text'] = "Here are some useful links\n" + results
                    # Task 4

        if "WEATHER" in text and username == 'zac.wentzell':
            text_search_collection = text.split(":")
            keyword = text_search_collection[1]
            if len(keyword) == 5:

                r = requests.get('http://api.wunderground.com/api/f60c5992ed69dce7/conditions/forecast/yesterday/settings/q/{0}.json'.format(keyword))

            else:

                query = text_search_collection[1].replace(",", "").split(" ")
                length = len(query)
                r = requests.get('http://api.wunderground.com/api/f60c5992ed69dce7/conditions/forecast/yesterday/settings/q/{0}/{1}.json'.format(query[length - 1], query[length - 2]))

            json_object = r.json()
            # current forecast for the given location
            location = json_object['current_observation']['display_location']['full']
            weather = json_object['current_observation']['weather']
            temp = json_object['current_observation']['temperature_string']
            feels_like = json_object['current_observation']['feelslike_string']
            wind_dir = json_object['current_observation']['wind_string']
            wind_gust = json_object['current_observation']['wind_gust_mph']
            # tomorrow's weather forecast
            tomorrow_fc = json_object['forecast']['txt_forecast']['forecastday'][2]['fcttext']
            tomorrow_high = json_object['forecast']['simpleforecast']['forecastday'][1]['high'][
                'fahrenheit']
            tomorrow_low = json_object['forecast']['simpleforecast']['forecastday'][1]['low'][
                'fahrenheit']
            today_high = json_object['forecast']['simpleforecast']['forecastday'][0]['high'][
                'fahrenheit']
            today_low = json_object['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
            today_qpf = json_object['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['in']
            tomorrow_qpf = json_object['forecast']['simpleforecast']['forecastday'][1]['qpf_allday'][
                'in']
            # yesterday's weather forecast
            yesterday_high = json_object['history']['dailysummary'][0]['maxtempi']
            yesterday_low = json_object['history']['dailysummary'][0]['mintempi']
            yesterday_qpf = json_object['history']['dailysummary'][0]['precipi']

            response['text'] = "*Here is the weather report for:*\n"+str(location) +"\n" +str(weather)+"\n"+str(temp)+"\n"+"*Feels like:*"+str(feels_like)+"\n"+str(wind_dir)+"\n"+"*Gusts:*"+str(wind_gust)+"\n"+"*Tomorrow* \n"+str(tomorrow_fc)+"\n"+"*High: *"+str(tomorrow_high)+"* | Low: *"+str(tomorrow_low)+"\n"+"*Precipitation: *"+str(tomorrow_qpf)+"\n"+"*Today*"+"\n"+"*High: *"+str(today_high)+"* | Low: *"+str(today_low)+"\n"+"*Precipitation: *"+str(today_qpf)+"\n"+"*Yesterday *\n"+"*High: *"+str(yesterday_high)+"* | Low: *"+str(yesterday_low)+"\n"+"*Precipitation: *"+str(yesterday_qpf)


        r = requests.post(slack_inbound_url, json=response)
    print inbound_message
    print request.form

    return Response(), 200


@application.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)
